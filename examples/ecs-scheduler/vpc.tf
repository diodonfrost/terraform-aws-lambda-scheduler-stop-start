resource "aws_vpc" "this" {
  cidr_block = "10.103.0.0/16"

  tags = {
    terratest_tag = var.random_tag
  }
}

resource "aws_subnet" "primary" {
  availability_zone = data.aws_availability_zones.available.names[0]
  vpc_id            = aws_vpc.this.id
  cidr_block        = "10.103.98.0/24"

  tags = {
    terratest_tag = var.random_tag
  }
}

resource "aws_subnet" "public" {
  availability_zone = data.aws_availability_zones.available.names[0]
  vpc_id            = aws_vpc.this.id
  cidr_block        = "10.103.99.0/24"

  tags = {
    terratest_tag = var.random_tag
  }
}


resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.this.id
  tags = {
    terratest_tag = var.random_tag
  }
}

resource "aws_route_table_association" "rt_assocations_public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table" "primary_rt" {
  vpc_id = aws_vpc.this.id
  tags = {
    terratest_tag = var.random_tag
  }
}

resource "aws_route_table_association" "rt_assocations_primary" {
  subnet_id      = aws_subnet.primary.id
  route_table_id = aws_route_table.primary_rt.id
}


#####
# Gateways
#####
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.this.id
  tags = {
    terratest_tag = var.random_tag
  }
}

# NAT Gateways
resource "aws_eip" "nat_gw_eip" {
  vpc = true
  tags = {
    terratest_tag = var.random_tag
  }
}

resource "aws_nat_gateway" "nat_gw" {
  allocation_id = aws_eip.nat_gw_eip.id
  subnet_id     = aws_subnet.public.id
  tags = {
    terratest_tag = var.random_tag
  }
}

resource "aws_route" "to_igw" {
  route_table_id         = aws_route_table.public_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

resource "aws_route" "primary_to_ngw" {
  route_table_id         = aws_route_table.primary_rt.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat_gw.id
}
