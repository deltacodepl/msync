######################################## Project Name ##############################################
variable "project_name" {
  description = "The name of the project"
  type        = string
  default     = "msync-ses"
}
######################################## Environment Name ##########################################
variable "environment_name" {
  description = "The name of the environment"
  type        = string
  default     = "dev"
}

######################################## SQS Queue #################################################
variable "sqs_queue_base_name" {
  description = "The base name of the SQS Queue"
  type        = string
  default     = "msync-sqs-queue"
}

variable "delay_seconds" {
  description = "SQS queue delay seconds"
  type        = number
  default     = 0
}

variable "max_message_size" {
  description = "SQS queue maximum message size"
  type        = number
  default     = 2048
}

variable "message_retention_seconds" {
  description = "SQS queue message retention period in seconds"
  type        = number
  default     = 1500
}
variable "receive_wait_time_seconds" {
  description = "SQS queue receive wait time in seconds"
  type        = number
  default     = 1
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

variable "lambda_function_description" {
  description = "The description of the lambda function"
  type        = string
  default     = "Lambda function description"
}

variable "memory_size" {
  description = "The allocated memory size of the lambda function in MB"
  type        = number
  default     = 128
}

variable "runtime" {
  description = "The runtime the lambda function"
  type        = string
  default     = "python3.11"
}

variable "timeout" {
  description = "The timeout period of the lambda function in seconds"
  type        = number
  default     = 3
}

variable "reserved_concurrent_executions" {
  description = "The reserved concurrency for the lambda function."
  type        = number
  default     = 2
}

variable "kms_key_alias" {
  type = string
  default = "kms-msync-ses"
  
}

variable "rotation_enabled" {
  type = bool
  default = false

}


variable "user_arn" {
  type = string
  default = "arn:aws:iam::615263381294:user/koadmin"
  
}

variable key_spec {
  default = "SYMMETRIC_DEFAULT"
}

variable enabled {
  default = true
}
######################################## CloudWatch Alarm ##########################################
# variable "cloudwatch_alarm_type" {
#   description = "The CloudWatch Alarm metric type"
#   type        = string
#   default     = "duration"
# }

# variable "cloudwatch_alarm_statistics" {
#   description = "The CloudWatch Alarm statistics"
#   type        = string
#   default     = "Average"
# }

# variable "cloudwatch_metric_name" {
#   description = "The CloudWatch Alarm metric name"
#   type        = string
#   default     = "Duration"
# }

# variable "cloudwatch_alarm_period" {
#   description = "The CloudWatch Alarm period in seconds"
#   type        = number
#   default     = 900
# }

# variable "cloudwatch_alarm_evaluation_period" {
#   description = "The CloudWatch Alarm evaluation period"
#   type        = number
#   default     = 2
# }

# variable "cloudwatch_alarm_comparison_operator" {
#   description = "The CloudWatch Alarm comparison operator"
#   type        = string
#   default     = "GreaterThanOrEqualToThreshold"
# }

# variable "cloudwatch_alarm_threshold" {
#   description = "The CloudWatch Alarm threshold"
#   type        = number
#   default     = 10
# }

# variable "cloudwatch_alarm_description" {
#   description = "The CloudWatch Alarm description"
#   type        = string
#   default     = ""
# }

# variable "datapoints_to_alarm" {
#   description = "The CloudWatch Alarm datapoints to alarm"
#   type        = number
#   default     = 1
# }