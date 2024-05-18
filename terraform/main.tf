provider "aws" {
  region = "us-west-1"
}

resource "aws_instance" "example" {
  ami           =  "ami-05f06113543f45964" 
  instance_type = "t2.micro"
  tags = {
    Name = "terraform-example"
  }
}