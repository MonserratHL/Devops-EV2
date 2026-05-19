output "ecr_backend_ventas_url" {
  description = "URL del repositorio ECR para backend ventas"
  value       = aws_ecr_repository.backend_ventas.repository_url
}

output "ecr_backend_despachos_url" {
  description = "URL del repositorio ECR para backend despachos"
  value       = aws_ecr_repository.backend_despachos.repository_url
}

output "ecr_frontend_url" {
  description = "URL del repositorio ECR para frontend"
  value       = aws_ecr_repository.frontend.repository_url
}
