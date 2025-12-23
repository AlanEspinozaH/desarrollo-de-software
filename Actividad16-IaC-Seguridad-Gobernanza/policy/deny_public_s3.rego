package terraform.s3_public_block

__rego_metadata__ := {
  "id": "TF-S3-001",
  "title": "Prohibir buckets públicos (ACL)",
  "severity": "high"
}

# Ejemplo didáctico: marca deny si se detecta recurso s3 con ACL 'public-read' en el plan
deny[msg] {
  some i
  rc := input.resource_changes[i]
  rc.type == "aws_s3_bucket"
  rc.change.after.acl == "public-read"
  msg := sprintf("S3 bucket '%s' tiene ACL pública", [rc.name])
}