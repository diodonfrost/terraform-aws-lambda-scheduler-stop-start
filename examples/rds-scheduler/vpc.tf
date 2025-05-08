data "aws_availability_zones" "available" {}

resource "aws_vpc" "this" {
  cidr_block = "10.103.0.0/16"
}

resource "aws_subnet" "primary" {
  availability_zone = data.aws_availability_zones.available.names[0]
  vpc_id            = aws_vpc.this.id
  cidr_block        = "10.103.98.0/24"
}

resource "aws_subnet" "secondary" {
  availability_zone = data.aws_availability_zones.available.names[1]
  vpc_id            = aws_vpc.this.id
  cidr_block        = "10.103.99.0/24"
}

resource "aws_db_subnet_group" "aurora" {
  name       = "aurora-subnet-${random_pet.suffix.id}"
  subnet_ids = [aws_subnet.primary.id, aws_subnet.secondary.id]
}
