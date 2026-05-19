# Devops-EV2 — Innovatech Chile

Repositorio del proyecto semestral **DevOps EP2**: aplicación contenedorizada desplegada en **AWS** con **Terraform** y **GitHub Actions**.

## Documentación principal

Toda la documentación técnica, diagramas de arquitectura AWS, guías de Terraform y CI/CD están en:

**[proyecto semestral/README.md](proyecto%20semestral/README.md)**

## Vista rápida

| Componente | Tecnología |
|------------|------------|
| Frontend | React + Vite + nginx |
| Backends | Spring Boot 3 (ventas :8080, despachos :8081) |
| Base de datos | MySQL 8 |
| Infraestructura | Terraform (ECR + VPC + 3 EC2) |
| CI/CD | GitHub Actions (`ci.yml` + `deploy.yml`) |

## Diagrama de arquitectura

<p align="center">
  <img src="proyecto%20semestral/docs/arquitectura-aws.svg" alt="Arquitectura AWS" width="900"/>
</p>

## Ramas

| Rama | Pipeline |
|------|----------|
| `develop` / `main` | Integración continua (Docker Compose) |
| `deploy` | Despliegue continuo (ECR + EC2) |

---

[Ver README completo →](proyecto%20semestral/README.md)
