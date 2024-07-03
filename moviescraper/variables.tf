variable "resource_group_location" {
  type        = string
  description = "Location of the resource group."
}

variable "resource_group_name" {
  type        = string
  description = "The resource group name."
}

variable "storage_account_name" {
  type        = string
  description = "The storage account name."
}

variable "postgres_name" {
  description = "The name of the PostgreSQL server"
  type        = string
}

variable "admin_user" {
  description = "The administrator username for the PostgreSQL server"
  type        = string
}

variable "admin_password" {
  description = "The administrator password for the PostgreSQL server"
  type        = string
}

variable "postgres_ip_access_start" {
  description = "The public IP address range that can access the PostgreSQL server"
  default     = ""
  type        = string
}
variable "postgres_ip_access_end" {
  description = "The public IP address range that can access the PostgreSQL server"
  default     = ""
  type        = string
}


variable "container_registry_name" {
  type        = string
  description = "The container registry name."
}

variable "image_name" {
  type        = string
  description = "The image docker name."
}

variable "container_group_name" {
  type        = string
  description = "The container group name."
}

variable "container_name" {
  type        = string
  description = "The container name."
}

variable "IS_POSTGRES" {
  type        = string
  description = "Variable env fo container : If Postgres database is used."
}

variable "DB_USERNAME" {
  type        = string
  description = "Variable env fo container : Postgres username."
}


variable "DB_PORT" {
  type        = string
  description = "Variable env fo container : Postgres port."
}

variable "DB_NAME" {
  type        = string
  description = "Variable env fo container : Postgres database name."
}

variable "DB_PASSWORD" {
  type        = string
  description = "Variable env fo container : Postgres password."
}