output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.validator.id
}

output "public_ip" {
  description = "Public IP address"
  value       = aws_instance.validator.public_ip
}

output "private_ip" {
  description = "Private IP address"
  value       = aws_instance.validator.private_ip
}

output "ssh_command" {
  description = "SSH command to connect"
  value       = "ssh ubuntu@${aws_instance.validator.public_ip}"
}

output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.validator.id
}

output "security_group_id" {
  description = "Security group ID"
  value       = aws_security_group.validator.id
}
