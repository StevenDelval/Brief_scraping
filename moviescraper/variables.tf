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