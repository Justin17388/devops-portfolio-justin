terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = ">= 5.0" }
  }
}

provider "aws" {
  region = var.region
}

# Access logs bucket (private)
resource "aws_s3_bucket" "logs" {
  bucket        = "${var.bucket_name}-logs"
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "logs" {
  bucket                  = aws_s3_bucket.logs.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Website bucket (needs public READ for website hosting)
resource "aws_s3_bucket" "site" {
  bucket        = var.bucket_name
  force_destroy = true
}

# Encryption at rest ✅
resource "aws_s3_bucket_server_side_encryption_configuration" "site" {
  bucket = aws_s3_bucket.site.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Versioning ✅
resource "aws_s3_bucket_versioning" "site" {
  bucket = aws_s3_bucket.site.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Access logging ✅ → to private logs bucket
resource "aws_s3_bucket_logging" "site" {
  bucket        = aws_s3_bucket.site.id
  target_bucket = aws_s3_bucket.logs.id
  target_prefix = "s3-access/"
}

# Required for static website (index/error) ✅
resource "aws_s3_bucket_website_configuration" "this" {
  bucket = aws_s3_bucket.site.id
  index_document { suffix = "index.html" }
  error_document { key = "404.html" }
}

# Public access block must be relaxed for static website.
#checkov:skip=CKV_AWS_56: Static website needs public GET; write & list remain blocked
resource "aws_s3_bucket_public_access_block" "site" {
  bucket                  = aws_s3_bucket.site.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# Least-privilege public READ only ✅
#checkov:skip=CKV_AWS_54: Website requires anonymous GetObject
data "aws_iam_policy_document" "public_read" {
  statement {
    sid     = "PublicReadGetObject"
    effect  = "Allow"
    actions = ["s3:GetObject"]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    resources = ["${aws_s3_bucket.site.arn}/*"]
  }
}

resource "aws_s3_bucket_policy" "public_read" {
  bucket = aws_s3_bucket.site.id
  policy = data.aws_iam_policy_document.public_read.json
}

resource "aws_s3_object" "index" {
  bucket       = aws_s3_bucket.site.id
  key          = "index.html"
  content_type = "text/html"
  content      = "<h1>Hello from Terraform S3 Static Site</h1>"
}

resource "aws_s3_object" "error" {
  bucket       = aws_s3_bucket.site.id
  key          = "404.html"
  content_type = "text/html"
  content      = "<h1>Not Found</h1>"
}

output "website_endpoint" {
  value = aws_s3_bucket_website_configuration.this.website_endpoint
}
