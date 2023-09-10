
######################################## Project Name ##############################################
variable "project_name" {
  description = "The name of the project"
  type        = string
  default     = ""
}

######################################## Environment Name ##########################################
variable "environment_name" {
  description = "The name of the environment"
  type        = string
  default     = "dev"
}

######################################## IAM Role / Policy #########################################
variable "iam_role_name" {
  description = "The name of the IAM Role"
  type        = string
  default     = "iam-role"
}

variable "iam_policy_name" {
  description = "The name of the IAM Policy"
  type        = string
  default     = "iam-policy"
}
######################################## Lambda Function  ##########################################
variable "lambda_function_base_name" {
  description = "The base name of the lambda function"
  type        = string
  default     = "lambda-function-name"
}

######################################## SQS Queue #################################################
variable "sqs_queue_base_name" {
  description = "The base name of the SQS Queue"
  type        = string
  default     = "sqs-queue"
}

variable "kms_key_arn" {
  type = string
  default = ""
}

######################################## Local Variables ###########################################
locals {
  tags = tomap({
    Environment = var.environment_name
    ProjectName = var.project_name
  })
}

locals {
  lambda_function_name = "${var.lambda_function_base_name}-${var.environment_name}-${data.aws_region.current.name}"
}
locals {
  queue_name = "${var.sqs_queue_base_name}-${var.environment_name}-${data.aws_region.current.name}"
}
