resource "aws_vpc" "redshift_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "redshift-vpc-${random_pet.suffix.id}"
  }
}

resource "aws_internet_gateway" "redshift_igw" {
  vpc_id = aws_vpc.redshift_vpc.id
  tags = {
    Name = "redshift-igw-${random_pet.suffix.id}"
  }
}

resource "aws_route_table" "redshift_route_table" {
  vpc_id = aws_vpc.redshift_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.redshift_igw.id
  }

  tags = {
    Name = "redshift-rt-${random_pet.suffix.id}"
  }
}

resource "aws_route_table_association" "redshift_rt_assoc_1" {
  subnet_id      = aws_subnet.redshift_subnet_1.id
  route_table_id = aws_route_table.redshift_route_table.id
}

resource "aws_route_table_association" "redshift_rt_assoc_2" {
  subnet_id      = aws_subnet.redshift_subnet_2.id
  route_table_id = aws_route_table.redshift_route_table.id
}

resource "aws_subnet" "redshift_subnet_1" {
  vpc_id                  = aws_vpc.redshift_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "eu-west-1a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "redshift_subnet_2" {
  vpc_id                  = aws_vpc.redshift_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "eu-west-1b"
  map_public_ip_on_launch = true
}

resource "aws_redshift_subnet_group" "redshift_subnet_group" {
  name       = "redshift-subnet-group-${random_pet.suffix.id}"
  subnet_ids = [aws_subnet.redshift_subnet_1.id, aws_subnet.redshift_subnet_2.id]
}

resource "aws_security_group" "redshift_sg" {
  name        = "redshift-sg-${random_pet.suffix.id}"
  description = "Security group for Redshift clusters"
  vpc_id      = aws_vpc.redshift_vpc.id

  ingress {
    from_port   = 5439
    to_port     = 5439
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow Redshift access"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}