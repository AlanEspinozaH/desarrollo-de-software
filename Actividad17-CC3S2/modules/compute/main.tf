variable "subnet_id" {
  type = string
}

resource "null_resource" "instance" {
  triggers = {
    subnet = var.subnet_id
  }
}

output "instance_ip" {
  value = "192.168.1.10"
}
