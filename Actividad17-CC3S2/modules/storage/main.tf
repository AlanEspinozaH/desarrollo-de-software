resource "local_file" "bucket_mock" {
  content  = "bucket-simulado"
  filename = "${path.module}/bucket.txt"
}
output "bucket_name" {
  value = "bucket-local-v1"
}
