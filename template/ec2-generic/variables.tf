variable "owner" {
    default = "peter.veentjer@scylladb.com"
}

variable "region" {
    default = "us-east-2"
}
 
variable "keypair_name" {
    default = "pveentjer"
}

variable "public_key_location" {
    default = "../key.pub"
}

variable "private_key_location" {
    default = "../key"
}

# ============ cluster ===============

variable "cluster_size" {
    default = "1"
}

variable "cluster_instance_type" {
    default = "c5.2xlarge"
}

variable "cluster_name" {
    default = "cluster pveentjer"
}

variable "cluster_user" {
    default = "centos"
}

variable "scylla_ami" {
    #  4.1.2-0.20200715.3e6c6d5f582    
    default = "ami-0fefb980cbfe6750a"
}


# ============ prometheus instance ===============

variable "prometheus_instance_type" {
    default = "c5.xlarge"
}

variable "prometheus_ami" {
    # Ubuntu Server 18.04 
    default = "ami-0dd9f0e7df0f0a138"
}

# ============ prometheus instance ===============

variable "loadgenerator_instance_type" {
    default = "c5.4xlarge"
}

variable "loadgenerator_size" {
    default = "1"
}

variable "loadgenerator_ami" {
    default = "ami-0996d3051b72b5b2c"
}

variable "loadgenerator_user" {
    default = "ubuntu"
}
