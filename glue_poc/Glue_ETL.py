# Define the S3 bucket
resource "aws_s3_bucket" "example_bucket" {
  bucket = "example-bucket"
}

# Define the Lambda function
resource "aws_lambda_function" "example_lambda" {
  filename      = "example_lambda.zip"
  function_name = "example_lambda"
  role          = aws_iam_role.example_lambda.arn
  handler       = "example_lambda.handler"
  runtime       = "nodejs14.x"
}

# Define the IAM role for the Lambda function
resource "aws_iam_role" "example_lambda" {
  name = "example_lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Define the Glue job
resource "aws_glue_job" "example_glue_job" {
  name     = "example_glue_job"
  role_arn = aws_iam_role.example_glue_job.arn

  command {
    name        = "glueetl"
    script_location = "s3://example-bucket/glue-job-script.py"
  }

  default_arguments = jsonencode({
    "--job-language" = "python"
    "--job-bookmark-option" = "job-bookmark-enable"
    "--enable-metrics" = ""
  })
}

# Define the IAM role for the Glue job
resource "aws_iam_role" "example_glue_job" {
  name = "example_glue_job_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

# Define the S3 bucket notification configuration
resource "aws_s3_bucket_notification" "example_bucket_notification" {
  bucket = aws_s3_bucket.example_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.example_lambda.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "folder-name/"
  }
}

# Grant permissions to the Lambda function and Glue job
resource "aws_lambda_permission" "example_lambda_permission" {
  statement_id  = "example_lambda_permission"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.example_lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.example_bucket.arn
}

resource "aws_glue_trigger" "example_glue_trigger" {
  name = "example_glue_trigger"
  type = "S3"
  actions {
    job_name = aws_glue_job.example_glue_job.name
    job_run_timeout = 60
    notification_property {
      notify_delay_after = 0
    }
    arguments = {
      "--s3_source_path" = "s3://example-bucket/folder-name/"
      "--s3_destination_path" = "s3://example-bucket/glue-job-output/"
    }
  }
  predicate {
    conditions {
      logical_operator = "EQUALS"
      job_name = aws_glue_job.example_glue_job.name
      state = "SUCCEEDED"

