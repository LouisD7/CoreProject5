output "patient_api_base_url" {
  description = "Base URL for patient API Gateway stage."

  value = aws_apigatewayv2_stage.patient_api_stage.invoke_url
}
