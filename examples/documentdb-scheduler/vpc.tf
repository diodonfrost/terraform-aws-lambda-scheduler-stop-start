resource "aws_vpc" "documentdb" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "documentdb-vpc-${random_pet.suffix.id}"
  }
}

resource "aws_subnet" "documentdb_1" {
  vpc_id                  = aws_vpc.documentdb.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "eu-west-1a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "documentdb_2" {
  vpc_id                  = aws_vpc.documentdb.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "eu-west-1b"
  map_public_ip_on_launch = true
}

resource "aws_docdb_subnet_group" "documentdb" {
  name       = "documentdb-subnet-group-${random_pet.suffix.id}"
  subnet_ids = [aws_subnet.documentdb_1.id, aws_subnet.documentdb_2.id]
}
