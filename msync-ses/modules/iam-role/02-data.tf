# AWS Region and Caller Identity
data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

# IAM Policy Document
data "aws_iam_policy_document" "iam-policy-document" {
  statement {
    sid = "AllowCloudWatchLogStream"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]

    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${local.lambda_function_name}:*",
    ]
  }

  statement {
    sid = "AllowSQSSendMessage"

    actions = [
      #"sqs:SendMessage"
      "sqs:*"
    ]

    resources = [
      "arn:aws:sqs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${local.queue_name}"
    ]
  }

  statement {
    sid = "AllowKMSDecryption"

    actions = [
      "kms:Decrypt",
      "kms:Encrypt",
      "kms:GenerateDataKey",
      "kms:GenerateDataKeyPair"
    ]

    resources = [
      "${var.kms_key_arn}"
    ]
  }
  statement {
    sid = "AllowSES"

    actions = [
      "ses:SendRawEmail",
      "ses:SendEmail",
      "ses:SendTemplatedEmail"
    ]

    resources = [
      "*"
    ]
  }

}