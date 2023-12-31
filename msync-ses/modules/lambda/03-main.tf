## Lambda Function
resource "aws_lambda_function" "lambda-function" {

  filename                       = "../modules/lambda/code/msync.zip"
  function_name                  = local.lambda_function_name
  description                    = var.lambda_function_description
  role                           = local.lambda_execution_role_arn
  handler                        = "sqs.sqs"
  memory_size                    = var.memory_size
  timeout                        = var.timeout
  runtime                        = var.runtime
  source_code_hash               = data.archive_file.package_zip.output_base64sha256
  # source_code_hash = filebase64sha256(data.archive_file.package_zip.output_path)
  reserved_concurrent_executions = var.reserved_concurrent_executions

  dead_letter_config {
    target_arn = var.dead_letter_queue_arn
  }
  environment {
    variables = {
      # DYNAMODB_TABLE_NAME = "${local.dynamodb_table_name}"
      # SNS_TOPIC_ARN       = "${var.sns_topic_arn}"
      QUEUE_URL = "https://sqs.eu-central-1.amazonaws.com/615263381294/msync-sqs-queue-dev-eu-central-1"
    }
  }

  tags = local.tags
}

## Lambda Asynchronous DLQ Config
resource "aws_lambda_function_event_invoke_config" "lambda-fucntion-dlq-config" {
  function_name                = aws_lambda_function.lambda-function.function_name
  maximum_event_age_in_seconds = 1800
  maximum_retry_attempts       = 2
}