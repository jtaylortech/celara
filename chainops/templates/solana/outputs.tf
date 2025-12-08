output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.validator.id
}

output "public_ip" {
  description = "Public IP address"
  value       = aws_instance.validator.public_ip
}

output "ssh_command" {
  description = "SSH command to connect"
  value       = "ssh ubuntu@${aws_instance.validator.public_ip}"
}

output "rpc_endpoint" {
  description = "Solana RPC endpoint"
  value       = "http://${aws_instance.validator.public_ip}:8899"
}

output "websocket_endpoint" {
  description = "Solana WebSocket endpoint"
  value       = "ws://${aws_instance.validator.public_ip}:8900"
}
