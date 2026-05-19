variable "aws_region" {
  description = "Región de AWS"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
  default     = "innovatech"
}

variable "key_pair_name" {
  description = "Nombre del key pair EC2 en AWS"
  type        = string
}

variable "db_password" {
  description = "Contraseña root de MySQL"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "Nombre de la base de datos"
  type        = string
  default     = "innovatech_db"
}
