terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Pull the latest Amazon Linux 2 AMI
data "aws_ami" "amz2" {
  most_recent = true
  owners      = ["137112412989"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# Use the default VPC/subnets for simplicity
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}


# Security group allows HTTP and SSH
resource "aws_security_group" "bookstore_sg" {
  name        = "bookstore-sg"
  description = "Allow HTTP and SSH"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Launch EC2 instance and bootstrap with user_data.sh
resource "aws_instance" "bookstore" {
  ami           = data.aws_ami.amz2.id
  instance_type = var.instance_type

  # was: element(data.aws_subnet_ids.default.ids, 0)
  subnet_id = data.aws_subnets.default.ids[0]

  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.bookstore_sg.id]
  key_name                    = var.key_name

  user_data = templatefile("${path.module}/user_data.sh", {
    repo_url = var.github_repo_url
    app_dir  = var.app_dir
  })

  tags = { Name = "Web Server of Bookstore" }
}



