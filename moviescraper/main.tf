resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.resource_group_location
}

resource "azurerm_storage_account" "storage_account" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
}

resource "azurerm_postgresql_flexible_server" "postgresql" {
  name                = var.postgres_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  administrator_login          = var.admin_user
  administrator_password       = var.admin_password
  sku_name                     = "B_Standard_B1ms"
  storage_mb                   = 32768
  version                      = "13"
  public_network_access_enabled = true
  storage_tier                 = "P4"  
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "firewall_rule" {
  name             = "postgresql-rule"
  server_id        = azurerm_postgresql_flexible_server.postgresql.id
  start_ip_address = var.postgres_ip_access_start
  end_ip_address   = var.postgres_ip_access_end
}

resource "azurerm_container_registry" "container_registry" {
  name                = var.container_registry_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = true
}