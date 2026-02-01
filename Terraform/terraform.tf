terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.92"
    }
  }

  backend "s3" {
    bucket = "patient-lambda-terraform-state"
    region = "eu-west-2"
    key    = "Terraform/terraform.tfstate"
  }

  required_version = ">= 1.2"
}
