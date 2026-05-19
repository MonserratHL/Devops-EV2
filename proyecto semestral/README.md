# Innovatech Chile - Proyecto Semestral DevOps EP2

Sistema de gestión de ventas y despachos contenedorizado con Docker, desplegado en AWS EC2 mediante CI/CD con GitHub Actions.

## Arquitectura en AWS (3 EC2 + VPC con subredes)

```
                    Internet
                        |
                        v
              +-------------------+
              |  EC2 Frontend   |  subred publica (10.0.1.0/24)
              |  nginx + React  |  puerto 80 abierto a Internet
              +--------+--------+
                       | proxy :8080 / :8081 (IP privada backend)
                       v
              +-------------------+
              |  EC2 Backend      |  subred publica (sin APIs expuestas a Internet)
              |  Spring Boot x2   |  SG: solo frontend puede conectar
              +--------+--------+
                       | MySQL :3306 (IP privada BD)
                       v
              +-------------------+
              |  EC2 Database     |  subred privada (10.0.2.0/24)
              |  MySQL en Docker  |  SG: solo backend puede conectar
              +-------------------+
```

| EC2 en consola AWS | Rol | Subred | Puertos expuestos a Internet |
|--------------------|-----|--------|------------------------------|
| `innovatech-frontend` | React + nginx | Publica | Solo **80** (HTTP) |
| `innovatech-backend` | APIs ventas/despachos | Publica* | **Ninguno** (solo SSH admin) |
| `innovatech-database` | MySQL 8 en Docker | **Privada** | **Ninguno** (solo SSH admin) |

\*El backend esta en subred publica para que el pipeline pueda hacer SSH y pull desde ECR; el **Security Group** bloquea 8080/8081 desde Internet y solo permite trafico desde el SG del frontend.

### Por que 3 EC2 es lo correcto para la evaluacion

- **Subredes compartidas en la misma VPC** (`10.0.0.0/16`): publica + privada con NAT.
- **Comunicacion por puertos privados**: frontend → backend → base de datos, cada salto restringido por Security Group.
- **Solo el frontend accesible desde Internet**, como pide la pauta EP2.
- **Volumen Docker** `innovatech-mysql-data` en la instancia de datos para persistencia.

### Ver la base de datos

1. Consola AWS → **EC2** → instancia **`innovatech-database`**.
2. Usa la IP publica de esa instancia (solo para SSH) o conecta desde el backend:

```bash
ssh -i mi-key-duoc.pem ec2-user@IP_PUBLICA_DATABASE
sudo docker exec -it mysql mysql -u root -p innovatech_db
```

Tras cambiar la arquitectura, ejecuta de nuevo `terraform apply` en `infra/etapa_2`.

### Por que la pagina parece "no hacer nada"

Es **parcialmente normal** en este proyecto:

1. **La portada es estatica**: carrusel, cards y footer cargan sin backend.
2. **Los datos aparecen al pulsar "Consultar"** en las tarjetas (ordenes de compra o despacho).
3. **`db.json` solo sirve para desarrollo local** con json-server; en AWS los datos vienen de MySQL via APIs.
4. Si las APIs fallan (502), las tablas quedan vacias. Revisa `DB_PASSWORD`, `EC2_BACKEND_PRIVATE_IP` y `EC2_DB_PRIVATE_IP` en GitHub.

Tras el despliegue, el backend de ventas carga **4 ordenes de ejemplo** automaticamente si la BD esta vacia.

## Arquitectura de puertos

| Servicio | Puerto | Acceso |
|----------|--------|--------|
| Frontend (nginx + React) | 80 / 8080 | Público (Internet) |
| Backend Ventas (Spring Boot) | 8080 | Solo red interna / frontend |
| Backend Despachos (Spring Boot) | 8081 | Solo red interna / frontend |
| MySQL 8 | 3306 | Solo EC2 database (subred privada) |

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
| `EC2_DB_PRIVATE_IP` | IP **privada** de la instancia database (`terraform output database_private_ip`) |
| `EC2_SSH_PRIVATE_KEY` | Llave PEM para SSH |
| `DB_NAME` | Nombre de la base de datos |
| `DB_PASSWORD` | Contraseña MySQL |

## Historial del pipeline (para la presentacion)

El pipeline en la rama `deploy` tuvo fallos iniciales que se corrigieron (trazabilidad DevOps):

| Problema | Causa | Solucion |
|----------|-------|----------|
| ECR duplicado | Repos ya creados en etapa 1 | Data sources en etapa 2 |
| State lock | `terraform apply` colgado | `terraform force-unlock` |
| `invalid reference format` | Variables no llegaban al EC2 por SSH | `envs:` + password ECR desde Actions |
| `permission denied` docker.sock | `ec2-user` sin permisos | `sudo docker` en el script |
| APIs 502 | Backends caidos o `DB_HOST` incorrecto | Secret `EC2_DB_PRIVATE_IP` + datos de ejemplo |

Runs recientes exitosos: [Actions](https://github.com/MonserratHL/Devops-EV2/actions/workflows/deploy.yml).

## Pipeline CI/CD

- **CI** (`ci.yml`): se ejecuta en PR/push a `develop`, construye y valida los contenedores.
- **CD** (`deploy.yml`): se ejecuta al hacer push a `deploy`, publica en ECR y despliega en EC2.
