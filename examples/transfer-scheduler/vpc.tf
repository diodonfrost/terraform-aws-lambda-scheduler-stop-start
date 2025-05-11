resource "aws_vpc" "transfer" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "transfer-vpc-${random_pet.suffix.id}"
  }
}

resource "aws_subnet" "transfer_1" {
  vpc_id                  = aws_vpc.transfer.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "eu-west-1a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "transfer_2" {
  vpc_id                  = aws_vpc.transfer.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "eu-west-1b"
  map_public_ip_on_launch = true
}
