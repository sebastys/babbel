provider "aws" {
  region = "eu-north-1" # Change to your desired AWS region
}

# Create an S3 bucket
resource "aws_s3_bucket" "example_bucket" {
  bucket_prefix = "example-bucket"
}

# Create a Kinesis Stream
resource "aws_kinesis_stream" "example_kinesis_stream" {
  name             = "example-stream"
  shard_count      = 1
  retention_period = 24

  tags = {
    Environment = "dev"
  }
}

# Create a Lambda function
resource "aws_lambda_function" "example_lambda_function" {
  filename      = "lambda_function.zip" # Provide your Lambda function code here
  function_name = "example-lambda"
  role          = aws_iam_role.example_lambda_role.arn
  handler       = "lambda_function.handler"
  runtime       = "python3.8"

  depends_on = [
    aws_iam_policy_attachment.example_lambda_policy_attachment
  ]
}

# Create an IAM role for the Lambda function
resource "aws_iam_role" "example_lambda_role" {
  name = "example_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Attach an IAM policy to the Lambda function role
resource "aws_iam_policy_attachment" "example_lambda_policy_attachment" {
  name = "babbel"
  policy_arn = aws_iam_policy.example_lambda_policy.arn
  roles      = [aws_iam_role.example_lambda_role.name]
  
}

# Create an IAM policy for the Lambda function
resource "aws_iam_policy" "example_lambda_policy" {
  name = "example_lambda_policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "kinesis:PutRecord",
          "kinesis:PutRecords"
        ]
        Effect = "Allow"
        Resource = aws_kinesis_stream.example_kinesis_stream.arn
      },
      {
        Action = "s3:PutObject"
        Effect = "Allow"
        Resource = aws_s3_bucket.example_bucket.arn
      }
    ]
  })
}

