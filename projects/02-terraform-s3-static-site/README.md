# Terraform — S3 Static Website

This project provisions an AWS S3 bucket configured for static website hosting using Terraform. It demonstrates infrastructure-as-code fundamentals, AWS cloud architecture, remote state discipline, and secure, repeatable deployments.

# What This Project Demonstrates

-Provisioning AWS resources using Terraform

-Creating an S3 bucket configured as a static website

-Managing bucket policies, access control, and hosting

-Idempotent deployments using terraform apply

-Clean Terraform structure: variables, outputs, files, and modules

-Practical IaC workflow for Cloud Engineer roles

# Tech Stack

Cloud: AWS S3

IaC: Terraform (HCL)

CLI Tools: AWS CLI, Terraform CLI

Version Control: Git & GitHub

# Architecture Overview

User → S3 Static Website Endpoint → Hosted Files (HTML/CSS/JS)

AWS services created:

-S3 Bucket

-Static website hosting enabled (index.html, error.html)

-Configured public-read policy (or CloudFront-ready if locked down)

-Website endpoint output after apply

# Project Structure
```bash
.
├── main.tf            # Core S3 configuration + hosting setup
├── variables.tf       # Input variables
├── outputs.tf         # Exposed outputs (bucket name, website URL)
├── index.html         # Example site content
├── error.html
└── README.md
```

## How to Deploy
```bash
aws configure
terraform init
terraform apply
```
--Terraform will output the website endpoint URL.

--Open it in the browser and you’ll see your hosted static site.

# Security Considerations

-Public access only applied specifically for website hosting

-Bucket versioning & encryption can be added as enhancements

-Designed to work cleanly with CloudFront + TLS if needed

-Follows IaC best practices: no manual console clicking

# Real-World Use Case

-Marketing/static landing pages

-Documentation sites

-Simple internal dashboards

-Hosting frontends for serverless apps

-Quick prototypes

# Future Enhancements

-CloudFront + ACM for HTTPS

-Route 53 for custom domain

-Remote Terraform backend (S3 + DynamoDB)

-CI/CD pipeline to auto-deploy site changes
