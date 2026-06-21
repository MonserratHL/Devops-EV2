output "frontend_public_ip" {
  description = "IP publica del frontend (unico acceso desde Internet)"
  value       = aws_instance.frontend.public_ip
}

output "backend_private_ip" {
  description = "IP privada del backend (proxy nginx y despliegue via bastion)"
  value       = aws_instance.backend.private_ip
}

output "database_private_ip" {
  description = "IP privada de MySQL (solo accesible desde backend)"
  value       = aws_instance.database.private_ip
}

output "ecr_backend_ventas_url" {
  value = data.aws_ecr_repository.backend_ventas.repository_url
}

output "ecr_backend_despachos_url" {
  value = data.aws_ecr_repository.backend_despachos.repository_url
}

output "ecr_frontend_url" {
  value = data.aws_ecr_repository.frontend.repository_url
}
