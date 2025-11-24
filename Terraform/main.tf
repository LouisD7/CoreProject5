provider "aws" {
  region = "eu-west-2"
}

# aws_lambda_function.access_patient_data defines a Lambda function named access_patient_data. The function's code is located in the terraform.zip file in the build directory, and it uses the Python 3.14 runtime. The function's handler is defined as lambda_function.lambda_handler, and it assumes the IAM role defined by aws_iam_role.lambda_exec.
resource "aws_lambda_function" "access_patient_data" {
  function_name    = "access_patient_data"
  filename         = "../build/terraform.zip"
  source_code_hash = filebase64sha256("../build/terraform.zip")
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.13"
  role             = aws_iam_role.lambda_exec.arn
}

# aws_cloudwatch_log_group.access_patient_data defines a log group to store log messages from your Lambda function for 30 days. By convention, Lambda stores logs in a group with the name /aws/lambda/<Function Name>.
resource "aws_cloudwatch_log_group" "access_patient_data" {
  name = "/aws/lambda/${aws_lambda_function.access_patient_data.function_name}"

  retention_in_days = 7
}

#aws_iam_role.lambda_exec defines an IAM role that allows Lambda to access resources in your AWS account.
resource "aws_iam_role" "lambda_exec" {
  name = "serverless_lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
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

# aws_iam_role_policy_attachment.lambda_policy attaches a policy the IAM role. The AWSLambdaBasicExecutionRole is an AWS managed policy that allows your Lambda function to write to CloudWatch logs.
resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
