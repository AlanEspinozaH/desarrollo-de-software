variable "records" {
  description = "Mapa de Hostname -> IP"
  type        = map(string)

  # Validación: Rechazar nombres con espacios o caracteres raros
  validation {
    condition     = alltrue([for host, ip in var.records : can(regex("^[a-z0-9.-]+$", host))])
    error_message = "Los nombres de host solo pueden contener minúsculas, números, puntos y guiones."
  }
}

output "dns_mapping" {
  value = var.records
}
