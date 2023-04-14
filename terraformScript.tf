# Define the AWS provider
provider "aws" {
  region = "us-west-2" # Change it with your region
}

# Create a Kinesis Stream
resource "aws_kinesis_stream" "example_kinesis_stream" {
  name = "example-kinesis-stream"
  shard_count = 1 #Desired number of shards
}

# Create an IAM role for the Lambda function
resource "aws_iam_role" "example_lambda_role" {
  name = "example-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Attach necessary policies to the Lambda role
resource "aws_iam_role_policy_attachment" "example_lambda_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole" 
  role       = aws_iam_role.example_lambda_role.name
}

# Create a Lambda function
resource "aws_lambda_function" "example_lambda_function" {
  filename = "example_lambda_function.zip" 
  function_name = "example-lambda-function"
  role = aws_iam_role.example_lambda_role.arn
  handler = "lambda_function.lambda_handler" 
  runtime = "python3.8" 
  source_code_hash = filebase64sha256("example_lambda_function.zip") 
  depends_on = [
    aws_kinesis_stream.example_kinesis_stream # Ensure Lambda function depends on Kinesis Stream
  ]
}

# Create an S3 bucket
resource "aws_s3_bucket" "example_s3_bucket" {
  bucket = "example-s3-bucket" 
}

# Create S3 bucket event trigger for Lambda function
resource "aws_s3_bucket_notification_configuration" "example_s3_bucket_notification" {
  rule {
    status = "Enabled"
    lambda_function_configuration {
      lambda_function_arn = aws_lambda_function.example_lambda_function.arn
      events = ["s3:ObjectCreated:*"] # Add desired S3 event types
    }
  }

  depends_on = [
    aws_lambda_function.example_lambda_function # Ensure S3 bucket event trigger depends on Lambda function
  ]
}
