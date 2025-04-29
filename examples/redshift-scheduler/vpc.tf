resource "aws_vpc" "redshif" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "redshift-vpc-${random_pet.suffix.id}"
  }
}

resource "aws_subnet" "redshift_1" {
  vpc_id                  = aws_vpc.redshif.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "eu-west-1a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "redshift_2" {
  vpc_id                  = aws_vpc.redshif.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "eu-west-1b"
  map_public_ip_on_launch = true
}

resource "aws_redshift_subnet_group" "redshif" {
  name       = "redshift-subnet-group-${random_pet.suffix.id}"
  subnet_ids = [aws_subnet.redshift_1.id, aws_subnet.redshift_2.id]
}
