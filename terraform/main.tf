# Configure the AWS provider
provider "aws" {
  region                   = "eu-west-2"
  shared_credentials_files = ["$HOME/.aws/credentials"]
}

terraform {
  backend "s3" {
    bucket         = "zifo-ds-eu"
    key            = "skill-graph/terraform-state/terraform.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "skills-tracker-lock-table"
    encrypt        = true
  }
}

# SSH
resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "aws_key_pair" "deployer" {
  key_name   = "deployer-key"
  public_key = tls_private_key.ssh_key.public_key_openssh
}

## Network resources

resource "aws_vpc" "skills_tracker_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "Skills Tracker VPC"
  }
}

resource "aws_security_group" "skills_tracker_security_group" {
  name        = "skills_tracker_security_group"
  description = "Security group that allows all outbound traffic"
  vpc_id      = aws_vpc.skills_tracker_vpc.id

  ingress {
    protocol         = "tcp"
    from_port        = 80
    to_port          = 80
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    protocol         = "tcp"
    from_port        = 443
    to_port          = 443
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    protocol         = "tcp"
    from_port        = 8000
    to_port          = 8000
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    protocol         = "tcp"
    from_port        = 22
    to_port          = 22
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    protocol         = "-1"
    from_port        = 0
    to_port          = 0
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

# Create the public subnet
resource "aws_subnet" "skills_tracker_public_subnet" {
  vpc_id                  = aws_vpc.skills_tracker_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "Skills Tracker Public Subnet"
  }
}

# Create the Internet gateway
resource "aws_internet_gateway" "shrnaseq_igw" {
  vpc_id = aws_vpc.skills_tracker_vpc.id

  tags = {
    Name = "Skills Tracker Internet Gateway"
  }
}

# Create the route table for the public subnet
resource "aws_route_table" "shrnaseq_public_route_table" {
  vpc_id = aws_vpc.skills_tracker_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.shrnaseq_igw.id
  }

  tags = {
    Name = "Skills Tracker Public Route Table"
  }
}

# Associate the public subnet with the public route table
resource "aws_route_table_association" "shrnaseq_public_subnet_association" {
  subnet_id      = aws_subnet.skills_tracker_public_subnet.id
  route_table_id = aws_route_table.shrnaseq_public_route_table.id
}

## IAM

resource "aws_iam_policy" "ecr_read" {
  name        = "ecr-read-policy"
  description = "Policy to allow reading from ECR"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetAuthorizationToken"
        ],
        Resource = "*",
        Effect   = "Allow"
      }
    ]
  })
}

resource "aws_iam_role" "skills_tracker_ec2_role" {
  name = "SkillsTracker-EC2"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecr_read_attach" {
  role       = aws_iam_role.skills_tracker_ec2_role.name
  policy_arn = aws_iam_policy.ecr_read.arn
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "skills_tracker_ec2_profile"
  role = aws_iam_role.skills_tracker_ec2_role.name
}

## EC2

resource "aws_instance" "skills_tracker_ec2" {
  ami                    = "ami-0eb260c4d5475b901"
  instance_type          = "t2.medium"
  iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name
  key_name               = aws_key_pair.deployer.key_name
  vpc_security_group_ids = [aws_security_group.skills_tracker_security_group.id]
  subnet_id              = aws_subnet.skills_tracker_public_subnet.id
  tags = {
    Name = "SkillsTracker-Test"
  }
  user_data = file("../scripts/initialise_ec2.sh")
}

resource "aws_eip" "skills_tracker_public_ip" {
  instance = aws_instance.skills_tracker_ec2.id
}

resource "aws_eip_association" "skills_tracker_eip_assoc" {
  instance_id   = aws_instance.skills_tracker_ec2.id
  allocation_id = aws_eip.skills_tracker_public_ip.id
}

## Route 53

resource "aws_route53_record" "skills_tracker_record" {
  zone_id = "Z08968053PXG7F1APWLYQ"
  name    = "skills.zifo-tech.com"
  type    = "A"
  ttl     = "300"
  records = [aws_eip.skills_tracker_public_ip]
}
