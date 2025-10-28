variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "key_name" {
  description = "Existing EC2 key pair name for SSH"
  type        = string
}

variable "ssh_cidr" {
  description = "CIDR allowed for SSH access"
  type        = string
  default     = "0.0.0.0/0" # Restrict to your IP for real use
}

variable "github_repo_url" {
  description = "HTTPS URL of your GitHub repo containing docker-compose.yml"
  type        = string
}

variable "app_dir" {
  description = "Relative path (from repo root) to docker-compose.yml"
  type        = string
  default     = "."
}
