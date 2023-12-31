terraform {
  backend "s3" {
    bucket  = "msync-tf-remote-state" 
    key     = "msync/dev/terraform.tfstate" 
    region  = "eu-central-1" 
    encrypt = true
    profile = "default"
  }
}

provider "aws" {
  region = "eu-central-1"
}