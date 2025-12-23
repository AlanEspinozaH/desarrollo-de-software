resource "null_resource" "vpc" {
  triggers = {
    id = "vpc-local-123"
  }
}
output "vpc_id" {
  value = "vpc-local-123"
}
output "subnet_id" {
  value = "subnet-local-456"
}

