output "private_key" {
  value     = tls_private_key.ssh_key.private_key_pem
  sensitive = true
}

output "api_ip" {
  value = aws_eip.skills_tracker_public_ip.public_ip
}
