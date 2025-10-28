output "ec2_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.bookstore.public_ip
}

output "bookstore_api_url" {
  description = "Public URL to access the Flask Bookstore API"
  value       = "http://${aws_instance.bookstore.public_dns}"
}
