provider "aws" {
  region = "eu-west-2"
}

# aws_lambda_function.access_patient_data defines a Lambda function named access_patient_data. The function's code is located in the terraform.zip file in the build directory, and it uses the Python 3.14 runtime. The function's handler is defined as lambda_function.lambda_handler, and it assumes the IAM role defined by aws_iam_role.lambda_exec.
resource "aws_lambda_function" "access_patient_data" {
  function_name    = "access_patient_data"
  filename         = "../build/terraform.zip"
  source_code_hash = filebase64sha256("../build/terraform.zip")
  handler          = "aws.patient_data_lambda.lambda_handler"
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

# aws_apigatewayv2_api.patient_api defines an API Gateway HTTP API named patient_api.
resource "aws_apigatewayv2_api" "patient_api" {
  name          = "patient_api"
  protocol_type = "HTTP"
}

# aws_apigatewayv2_stage.patient_api_stage defines a stage for the API Gateway named patient_data_lambda_stage. The stage is set to auto-deploy changes, and it includes access log settings that send logs to a CloudWatch log group.
resource "aws_apigatewayv2_stage" "patient_api_stage" {
  api_id = aws_apigatewayv2_api.patient_api.id

  name        = "patient_data_lambda_stage"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
}

# aws_apigatewayv2_integration.access_patient_data configures the API Gateway to use your Lambda function.
resource "aws_apigatewayv2_integration" "access_patient_data" {
  api_id = aws_apigatewayv2_api.patient_api.id

  integration_uri    = aws_lambda_function.access_patient_data.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

# aws_apigatewayv2_route.access_patient_data defines a route for the API Gateway. The route listens for GET requests to the /hello path and routes them to the Lambda function integration defined earlier.
resource "aws_apigatewayv2_route" "access_patient_data" {
  api_id = aws_apigatewayv2_api.patient_api.id

  route_key = "GET /hello"
  target    = "integrations/${aws_apigatewayv2_integration.access_patient_data.id}"
}

# aws_cloudwatch_log_group.api_gw defines a log group to store access logs for the aws_apigatewayv2_stage.patient_api_stage API Gateway stage.
resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.patient_api.name}"

  retention_in_days = 7
}

# aws_lambda_permission.api_gw grants the API Gateway permission to invoke the Lambda function.
resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.access_patient_data.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.patient_api.execution_arn}/*/*"
}
