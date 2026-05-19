# Innovatech Chile - Proyecto Semestral DevOps EP2

Sistema de gestión de ventas y despachos contenedorizado con Docker, desplegado en AWS EC2 mediante CI/CD con GitHub Actions.

## Arquitectura en AWS (2 EC2 + MySQL en contenedor)

```
Internet
   |
   v
[ EC2 Frontend ]  ----proxy---->  [ EC2 Backend ]
   React + nginx      (IP privada)     Spring Ventas :8080
   puerto 80                           Spring Despachos :8081
                                       MySQL :3306 (contenedor Docker)
```

| Componente | Donde corre | Se ve en consola AWS como |
|------------|-------------|---------------------------|
| Frontend | EC2 `innovatech-frontend` | Instancia EC2 |
| APIs Spring | EC2 `innovatech-backend` | Instancia EC2 |
| **MySQL** | **Contenedor Docker en el mismo EC2 backend** | **No es una EC2 aparte** |

La base de datos **no tiene instancia EC2 propia**. Terraform la levanta con `docker run mysql:8` en el user_data del backend. Los datos persisten en el volumen Docker `innovatech-mysql-data`.

### Ver la base de datos

1. Consola AWS → **EC2** → instancia **innovatech-backend** → copiar IP publica.
2. Conectarte por SSH con tu `.pem`:

```bash
ssh -i mi-key-duoc.pem ec2-user@IP_PUBLICA_BACKEND
sudo docker ps
sudo docker exec -it mysql mysql -u root -p innovatech_db
```

3. O en consola AWS → **ECR**, **VPC**, etc. MySQL no aparece como servicio RDS ni como tercera EC2; es normal.

### Por que la pagina parece "no hacer nada"

Es **parcialmente normal** en este proyecto:

1. **La portada es estatica**: carrusel, cards y footer cargan sin backend.
2. **Los datos aparecen al pulsar "Consultar"** en las tarjetas (ordenes de compra o despacho).
3. **`db.json` solo sirve para desarrollo local** con json-server; en AWS los datos vienen de MySQL via APIs.
4. Si las APIs fallan (502), las tablas quedan vacias. Revisa que `DB_PASSWORD` y `EC2_BACKEND_PRIVATE_IP` en GitHub coincidan con Terraform.

Tras el despliegue, el backend de ventas carga **4 ordenes de ejemplo** automaticamente si la BD esta vacia.

## Arquitectura de puertos

| Servicio | Puerto | Acceso |
|----------|--------|--------|
| Frontend (nginx + React) | 80 / 8080 | Público (Internet) |
| Backend Ventas (Spring Boot) | 8080 | Solo red interna / frontend |
| Backend Despachos (Spring Boot) | 8081 | Solo red interna / frontend |
| MySQL 8 | 3306 | Solo en EC2 backend (contenedor) |

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
| `EC2_BACKEND_HOST` | IP **publica** del EC2 backend (para SSH del pipeline) |
| `EC2_FRONTEND_HOST` | IP **publica** del EC2 frontend |
| `EC2_BACKEND_PRIVATE_IP` | IP **privada** del backend (`terraform output backend_private_ip`) |
| `EC2_SSH_PRIVATE_KEY` | Llave PEM para SSH |
| `DB_NAME` | Nombre de la base de datos |
| `DB_PASSWORD` | Contraseña MySQL |

## Pipeline CI/CD

- **CI** (`ci.yml`): se ejecuta en PR/push a `develop`, construye y valida los contenedores.
- **CD** (`deploy.yml`): se ejecuta al hacer push a `deploy`, publica en ECR y despliega en EC2.
