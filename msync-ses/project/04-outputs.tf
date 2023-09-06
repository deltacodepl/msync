######################################## SQS Queue #################################################
output "msync_sqs_queue_arn" {
  value = module.msync_sqs.sqs_queue_arn
}

output "msync_sqs_queue_id" {
  value = module.msync_sqs.sqs_queue_id
}

output "msync_sqs_queue_url" {
  value = module.msync_sqs.sqs_queue_url
}

output "msync_sqs_queue_tags_all" {
  value = module.msync_sqs.sqs_topic_tags_all
}

######################################## IAM Role ##################################################
output "msync_lambda_role_arn" {
  value = module.msync_lambda_execution_role.iam_role_arn
}
######################################## Lambda Function ###########################################
output "msync_lambda_function_arn" {
  value = module.msync_lambda_function.lambda_function_arn
}
