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

resource "azurerm_container_registry" "acr" {
  name                = var.container_registry_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = true
  depends_on = [azurerm_postgresql_flexible_server.postgresql]
}

resource "null_resource" "docker_push" {
  provisioner "local-exec" {
    command = <<EOT
    ACR_NAME=${azurerm_container_registry.acr.name}
    RESOURCE_GROUP=${azurerm_resource_group.rg.name}
    ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query "loginServer" --output tsv)
    ACR_IMAGE_NAME=${var.image_name}

    az acr login --name $ACR_NAME
    docker tag $ACR_IMAGE_NAME $ACR_LOGIN_SERVER/$ACR_IMAGE_NAME
    docker push $ACR_LOGIN_SERVER/$ACR_IMAGE_NAME

    EOT
  }
  depends_on = [azurerm_container_registry.acr]
}


resource "azurerm_container_group" "container_group" {
  name                = var.container_group_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  ip_address_type     = "Public"
  os_type             = "Linux"
  image_registry_credential{
    server = azurerm_container_registry.acr.login_server
    username = azurerm_container_registry.acr.admin_username
    password = azurerm_container_registry.acr.admin_password
  }

  container {
    name   = var.container_name
    image  = "${azurerm_container_registry.acr.login_server}/${var.image_name}"
    cpu    = "1"
    memory = "1"

    ports {
      port     = 80
      protocol = "TCP"
    }

    environment_variables = {
      IS_POSTGRES = var.IS_POSTGRES
      DB_USERNAME = var.DB_USERNAME
      DB_HOSTNAME = "${azurerm_postgresql_flexible_server.postgresql.name}.postgres.database.azure.com"
      DB_PORT = var.DB_PORT
      DB_NAME = var.DB_NAME
    }

    secure_environment_variables = {
      DB_PASSWORD = var.DB_PASSWORD
    }
  }

  depends_on = [null_resource.docker_push]
}