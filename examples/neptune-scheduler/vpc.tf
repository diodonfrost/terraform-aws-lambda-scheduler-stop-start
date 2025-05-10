resource "aws_vpc" "neptune" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "neptune-vpc-${random_pet.suffix.id}"
  }
}

resource "aws_subnet" "neptune_1" {
  vpc_id                  = aws_vpc.neptune.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "eu-west-1a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "neptune_2" {
  vpc_id                  = aws_vpc.neptune.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "eu-west-1b"
  map_public_ip_on_launch = true
}

resource "aws_neptune_subnet_group" "test" {
  name       = "neptune-subnet-group-${random_pet.suffix.id}"
  subnet_ids = [aws_subnet.neptune_1.id, aws_subnet.neptune_2.id]
}
