terraform {
  required_version = ">= 1.6.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

provider "null" {}

resource "null_resource" "example" {
  triggers = {
    id = "actividad16"
  }
}

# Cambia el nombre a 'secret_token' si quieres forzar un deny de política de ejemplo
output "hello_message" {
  value = "Hello from IaC!"
}