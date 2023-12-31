# AWS Region and Caller Identity
data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

# Lambda code zip file
data "archive_file" "package_zip" {
  type        = "zip"
  source_dir = "${var.code_dir}"
  output_path = "${path.module}/code/msync.zip"
}