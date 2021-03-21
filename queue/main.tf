provider "aws" {
  profile = "personal"
  region = "eu-west-1"
}

resource "aws_sqs_queue" "queue" {
  name = "test-distributed-tracing"
}

data "aws_iam_policy_document" "queue_access" {
  statement {
    actions = ["sqs:*"]
    principals {
      type = "AWS"
      identifiers = [aws_iam_user.queue_user.arn]
    }
  }
}

resource "aws_sqs_queue_policy" "queue_access" {
  queue_url = aws_sqs_queue.queue.id
  policy = data.aws_iam_policy_document.queue_access.json
}

resource "aws_iam_user" "queue_user" {
  name = "test-distributed-tracing"
  force_destroy = true
}

resource "aws_iam_access_key" "queue_user_key" {
  user = aws_iam_user.queue_user.name
}

output "queue_url" {
  value = aws_sqs_queue.queue.id
}

output "access_key_id" {
  value = aws_iam_access_key.queue_user_key.id
}

# Usually not a good idea in production
output "access_key_secret" {
  value = aws_iam_access_key.queue_user_key.secret
}
