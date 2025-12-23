variable "rules" {
  description = "Lista de reglas de firewall"
  type = list(object({
    port = number
    cidr = string
    protocol = string
  }))
}

# Genera un objeto JSON con la política completa
output "policy_json" {
  value = jsonencode({
    firewall_policy = {
      created_at = timestamp()
      rules = [for r in var.rules : {
        allow = "${r.protocol}:${r.port}"
        from  = r.cidr
      }]
    }
  })
}
