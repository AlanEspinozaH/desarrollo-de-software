package terraform.no_secret_outputs

__rego_metadata__ := {
  "id": "TF-OUT-001",
  "title": "Evitar outputs con nombre de 'secret'",
  "severity": "high"
}

deny[msg] {
  some k
  output := input.planned_values.outputs[k]
  contains(lower(k), "secret")
  msg := sprintf("Output '%s' aparenta exponer un secreto", [k])
}