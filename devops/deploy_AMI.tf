provider "aws" {
  region = "eu-west-3"
}

# Variables normalement dans un autre fichier (variables.tf) mais pour faire simple.... ca marche aussi !!!
variable "env" {
  type    = string
  default = "dev"
}

variable "EC2_IP" {
  type = string
}


terraform {
  backend "s3" {
  }
}


####################################################################
# On recherche la derniere AMI créée avec le Name TAG PackerAnsible-Apache
data "aws_ami" "docker" {
  owners = ["self"]
  filter {
    name   = "state"
    values = ["available"]

  }
  filter {
    name   = "tag:Name"
    values = ["${var.env}-DOCKER-AMI"]
  }
  most_recent = true
}


# On recupere les ressources reseau
## VPC
data "aws_vpc" "docker" {
  tags = {
    Name = "${var.env}-vpc"
  }
}

## Subnets
data "aws_subnet" "subnet-public-1" {
  tags = {
    Name = "${var.env}-subnet-public-1"
  }
}

## AZ zones de disponibilités dans la région
data "aws_availability_zones" "all" {}

########################################################################
# Security Groups
## ASG
resource "aws_security_group" "sg-docker" {
  name   = "${var.env}-sg-docker"
  vpc_id = data.aws_vpc.docker.id
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port       = 5000
    protocol        = "tcp"
    to_port         = 5000
    cidr_blocks = ["94.239.158.84/32","46.193.68.237/32" ]
  }
  ingress {
    from_port       = 80
    protocol        = "tcp"
    to_port         = 80
    cidr_blocks = ["94.239.158.84/32","46.193.68.237/32" ]
  }
  ingress {
    from_port   = 22
    protocol    = "tcp"
    to_port     = 22
    cidr_blocks = ["94.239.158.84/32","46.193.68.237/32","${var.EC2_IP}/32"] # on authorise en entrée de l'ASG que le flux venant de l'ELB
  }
  lifecycle {
    create_before_destroy = true
  }
}

##########################################################################
# ASG Launch Configuration


resource "aws_instance" "sentiment_server" {
  ami      = data.aws_ami.docker.id
  subnet_id = data.aws_subnet.subnet-public-1.id
  instance_type = "t2.micro"
  key_name = "jenkins"
   tags = {
    Name = "${var.env}-sentiment-server"
  }
  #  key_name = ""  # Si vous voulez utiliser une KeyPair pour vous connecter aux instances
  vpc_security_group_ids = [aws_security_group.sg-docker.id]
  lifecycle {
    create_before_destroy = true
  }
}

output "sentiment_server_public_ip" {
  description = "The public IP of the sentiment_server instance"
  value       = aws_instance.sentiment_server.public_ip
}
