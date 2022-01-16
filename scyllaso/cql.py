from time import sleep
from datetime import datetime, timedelta
import uuid
import socket

from scyllaso.ssh import SSH
from scyllaso.util import log_machine, log_important, run_parallel

#
# Contains the 'cqlsh' abstraction that executes CQL commands on some remote
# node using SSH.
#
class cqlsh:

    def __init__(self, ip, ssh_user, ssh_options, username=None, password=None):
        self.ip = ip
        self.ssh_user = ssh_user
        self.ssh_options = ssh_options
        self.username = username
        self.password = password
        self.started = False

    def __new_ssh(self, ip):
        return SSH(ip, self.ssh_user, self.ssh_options)

    def wait_for_cql_start(self, timeout=7200, connect_timeout=10, max_tries_per_second=2):
        log_important(f"cql: wait for start")
        wait_for_cql_start(self.ip, timeout,connect_timeout, max_tries_per_second)
        log_important(f"cqlsh: running")

    def exec(self, cql):
        """
        Executes a CQL command.

        Parameters
        ----------
        cql: str
            The CQL command
        """

        if not self.started:
            self.wait_for_cql_start()
            self.started = True

        script_name = str(uuid.uuid4())+".cql"
        log_important(f"cqlsh exec: [{cql}]")
        ssh = self.__new_ssh(self.ip)
        ssh.exec(f"touch {script_name}")
        ssh.exec(f"echo \"{cql}\" > {script_name}")
        cmd = "cqlsh "
        if self.username:
            cmd += f"-u {self.username} "
        if self.password:
            cmd += f"-p {self.password} "
        cmd += f"-f {script_name}"
        ssh.exec(cmd)
        ssh.exec(f"rm {script_name}")
        log_important(f"cqlsh done")


def wait_for_cql_start(node_ips, timeout=7200, connect_timeout=10, max_tries_per_second=2):
    log_machine(node_ips, 'Waiting for CQL port to start (meaning node bootstrap finished). This could take a while.')

    backoff_interval = 1.0 / max_tries_per_second
    timeout_point = datetime.now() + timedelta(seconds=timeout)

    feedback_interval = 20
    print_feedback_point = datetime.now() + timedelta(seconds=feedback_interval)

    if type(node_ips) is not list:
        node_ips = [ node_ips ]

    while datetime.now() < timeout_point:
        next_node_ips = []
        for node_ip in node_ips:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(connect_timeout)
                try:
                    sock.connect((node_ip, 9042))
                except:
                    # There was a problem connecting to CQL port.
                    sleep(backoff_interval)
                    if datetime.now() > print_feedback_point:
                        print_feedback_point = datetime.now() + timedelta(seconds=feedback_interval)
                        log_machine(node_ip, 'Still waiting for CQL port to start...')
                    next_node_ips.append(node_ip)

                else:
                    log_machine(node_ip, 'Successfully connected to CQL port.')
        node_ips = next_node_ips
        if not node_ips:
            return

    raise TimeoutError(f'Waiting for CQL to start timed out after {timeout} seconds for node(s): {node_ips}.')
