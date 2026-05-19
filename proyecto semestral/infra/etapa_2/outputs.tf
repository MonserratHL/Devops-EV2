output "frontend_public_ip" {
  description = "IP pública del frontend (único acceso desde Internet)"
  value       = aws_instance.frontend.public_ip
}

output "backend_private_ip" {
  description = "IP privada del backend (subred privada)"
  value       = aws_instance.backend.private_ip
}

output "ecr_backend_ventas_url" {
  value = aws_ecr_repository.backend_ventas.repository_url
}

output "ecr_backend_despachos_url" {
  value = aws_ecr_repository.backend_despachos.repository_url
}

output "ecr_frontend_url" {
  value = aws_ecr_repository.frontend.repository_url
}
