# Innovatech Chile - Proyecto Semestral DevOps EP2

Sistema de gestión de ventas y despachos contenedorizado con Docker, desplegado en AWS EC2 mediante CI/CD con GitHub Actions.

## Arquitectura

| Servicio | Puerto | Acceso |
|----------|--------|--------|
| Frontend (nginx + React) | 80 / 8080 | Público (Internet) |
| Backend Ventas (Spring Boot) | 8080 | Solo red interna / frontend |
| Backend Despachos (Spring Boot) | 8081 | Solo red interna / frontend |
| MySQL 8 | 3306 | Solo backends |

## Requisitos cumplidos (EP2)

- Dockerfiles multi-stage con usuario no root
- `docker-compose.yml` con redes, volúmenes y healthchecks
- Publicación de imágenes en Amazon ECR
- Pipeline CI/CD en GitHub Actions (rama `deploy`)
- Infraestructura AWS con Terraform (ECR + VPC + EC2)
- Solo el frontend es accesible desde Internet

## Estrategia de ramas Git

| Rama | Uso |
|------|-----|
| `main` | Código estable en producción |
| `develop` | Integración de desarrollo |
| `deploy` | Dispara el pipeline de despliegue a AWS |
| `feature/*` | Nuevas funcionalidades |
| `fix/*` | Corrección de errores |

Flujo recomendado: `feature/*` → `develop` → `main` → merge a `deploy` para publicar.

## Ejecución local con Docker

```bash
cd "proyecto semestral"
cp .env.example .env
docker compose up -d --build
```

Acceder a: http://localhost

## Terraform

### Etapa 1 - Repositorios ECR

```bash
cd infra/etapa_1
terraform init
terraform apply
```

### Etapa 2 - VPC, EC2, Security Groups

> **Importante:** Ejecuta primero `etapa_1` (ECR). La etapa 2 reutiliza esos repositorios y no los vuelve a crear.

```bash
cd infra/etapa_2
terraform init
terraform apply -var="key_pair_name=TU_KEY_PAIR" -var="db_password=TU_PASSWORD"
```

## Secrets de GitHub (Settings → Secrets)

| Secret | Descripción |
|--------|-------------|
| `AWS_ACCESS_KEY_ID` | Credencial AWS |
| `AWS_SECRET_ACCESS_KEY` | Credencial AWS |
| `AWS_SESSION_TOKEN` | Token de sesión (si aplica) |
| `EC2_BACKEND_HOST` | IP/host del EC2 backend |
| `EC2_FRONTEND_HOST` | IP/host del EC2 frontend |
| `EC2_BACKEND_PRIVATE_IP` | IP privada del backend para proxy nginx |
| `EC2_SSH_PRIVATE_KEY` | Llave PEM para SSH |
| `DB_NAME` | Nombre de la base de datos |
| `DB_PASSWORD` | Contraseña MySQL |

## Pipeline CI/CD

- **CI** (`ci.yml`): se ejecuta en PR/push a `develop`, construye y valida los contenedores.
- **CD** (`deploy.yml`): se ejecuta al hacer push a `deploy`, publica en ECR y despliega en EC2.
