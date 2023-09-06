module "msync_sqs" {
  source                    = "../modules/sqs"
  sqs_queue_base_name       = var.sqs_queue_base_name
  delay_seconds             = var.delay_seconds
  max_message_size          = var.max_message_size
  message_retention_seconds = var.message_retention_seconds
  receive_wait_time_seconds = var.receive_wait_time_seconds
  kms_key_alias             = var.kms_key_alias
}

module "msync_lambda_execution_role" {
  source                    = "../modules/iam-role"
  iam_role_name             = var.iam_role_name
  iam_policy_name           = var.iam_policy_name
  lambda_function_base_name = var.lambda_function_base_name
  dynamodb_table_base_name  = var.dynamodb_table_base_name
  sns_topic_base_name       = var.sns_topic_base_name
  sqs_queue_base_name       = var.sqs_queue_base_name
  s3_bucket_base_name       = var.s3_bucket_base_name
  s3_default_folder         = var.s3_default_folder
}

module "msync_lambda_function" {
  source                         = "../modules/lambda"
  lambda_function_base_name      = var.lambda_function_base_name
  lambda_function_description    = var.lambda_function_description
  iam_role_name                  = var.iam_role_name
  memory_size                    = var.memory_size
  timeout                        = var.timeout
  runtime                        = var.runtime
  dead_letter_queue_arn          = module.msync_sqs.sqs_queue_arn
  reserved_concurrent_executions = var.reserved_concurrent_executions
}
