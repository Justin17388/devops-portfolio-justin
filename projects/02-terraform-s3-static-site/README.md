# Terraform — S3 Static Website

Creates an S3 bucket configured for static website hosting.

## Usage
```bash
terraform init
terraform apply -var="bucket_name=<unique-name>" -auto-approve
