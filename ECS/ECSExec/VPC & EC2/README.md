```YAML
Description:  2Subnet-3AZ

Parameters:
  EnvironmentName:
    Description: prefixed to resource names
    Type: String
    Default: "skills"    

  VpcCIDR:
    Description: VPC-CIDR
    Type: String
    Default: 10.0.0.0/16

  PublicSubnet1CIDR:
    Description: Public1-CIDR
    Type: String
    Default: 10.0.2.0/24

  PublicSubnet2CIDR:
    Description: Public2-CIDR
    Type: String
    Default: 10.0.3.0/24

  PrivateSubnet1CIDR:
    Description: Private1-CIDR
    Type: String
    Default: 10.0.0.0/24

  PrivateSubnet2CIDR:
    Description: Private2-CIDR
    Type: String
    Default: 10.0.1.0/24

  LatestAmiId:
    Type: 'AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>'
    Default: '/aws/service/ami-amazon-linux-latest/al2023-ami-minimal-kernel-default-x86_64'

Resources:
#VPC
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Ref VpcCIDR
      EnableDnsSupport: true
      EnableDnsHostnames: true
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-vpc

#InternetGateway
  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-IGW

  InternetGatewayAttachment:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      InternetGatewayId: !Ref InternetGateway
      VpcId: !Ref VPC

#Subnet
  #Public Subnet
  PublicSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [ 0, !GetAZs '' ]
      CidrBlock: !Ref PublicSubnet1CIDR
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-public-a

  PublicSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [ 1, !GetAZs  '' ]
      CidrBlock: !Ref PublicSubnet2CIDR
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-public-b

  #Private Subnet
  PrivateSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [ 0, !GetAZs  '' ]
      CidrBlock: !Ref PrivateSubnet1CIDR
      MapPublicIpOnLaunch: false
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-private-a

  PrivateSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [ 1, !GetAZs  '' ]
      CidrBlock: !Ref PrivateSubnet2CIDR
      MapPublicIpOnLaunch: false
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-private-b

  #NatGateway
  NatGateway1EIP:
    Type: AWS::EC2::EIP
    DependsOn: InternetGatewayAttachment
    Properties:
      Domain: vpc

  NatGateway2EIP:
    Type: AWS::EC2::EIP
    DependsOn: InternetGatewayAttachment
    Properties:
      Domain: vpc

  NatGateway1:
    Type: AWS::EC2::NatGateway
    Properties:
      AllocationId: !GetAtt NatGateway1EIP.AllocationId
      SubnetId: !Ref PublicSubnet1
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-NGW-a

  NatGateway2:
    Type: AWS::EC2::NatGateway
    Properties:
      AllocationId: !GetAtt NatGateway2EIP.AllocationId
      SubnetId: !Ref PublicSubnet2
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-NGW-b

#Route Table
  #Public Route Table
  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-public-rt

  DefaultPublicRoute:
    Type: AWS::EC2::Route
    DependsOn: InternetGatewayAttachment
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref InternetGateway

  PublicSubnet1RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PublicRouteTable
      SubnetId: !Ref PublicSubnet1

  PublicSubnet2RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PublicRouteTable
      SubnetId: !Ref PublicSubnet2

  #Private Route Table
  PrivateRouteTable1:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-private-a-rt

  DefaultPrivateRoute1:
    Type: AWS::EC2::Route
    Properties:
      RouteTableId: !Ref PrivateRouteTable1
      DestinationCidrBlock: 0.0.0.0/0
      NatGatewayId: !Ref NatGateway1

  PrivateSubnet1RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PrivateRouteTable1
      SubnetId: !Ref PrivateSubnet1

  PrivateRouteTable2:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-private-b-rt

  DefaultPrivateRoute2:
    Type: AWS::EC2::Route
    Properties:
      RouteTableId: !Ref PrivateRouteTable2
      DestinationCidrBlock: 0.0.0.0/0
      NatGatewayId: !Ref NatGateway2

  PrivateSubnet2RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PrivateRouteTable2
      SubnetId: !Ref PrivateSubnet2

  #Public EC2
  BastionInstance:
    Type: 'AWS::EC2::Instance'
    Properties:
      ImageId: !Ref LatestAmiId
      InstanceType: t3.small
      SecurityGroupIds:
        - !Ref BastionSecurityGroup
      SubnetId: !Ref PublicSubnet1
      KeyName: test
      IamInstanceProfile: !Ref AdminInstanceProfile
      UserData: 
        Fn::Base64: !Sub |
          #!/bin/bash
          yum update -y
          yum install -y curl jq
          echo "Port 2222" >> /etc/ssh/sshd_config
          systemctl restart sshd
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-bastion-ec2

  #private EC2
  PirvateEC2Instance:
    Type: 'AWS::EC2::Instance'
    Properties:
      ImageId: !Ref LatestAmiId
      InstanceType: t3.small
      SecurityGroupIds:
        - !Ref PrivateEC2SecurityGroup
      SubnetId: !Ref PrivateSubnet1
      KeyName: test
      IamInstanceProfile: !Ref AdminInstanceProfile
      UserData: 
        Fn::Base64: !Sub |
          #!/bin/bash
          yum update -y
          yum install -y curl jq
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-ec2

  #Public Security Group
  BastionSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: "bastion-SG"
      VpcId: !Ref VPC
      SecurityGroupIngress:
      - IpProtocol: tcp
        FromPort: 2222
        ToPort: 2222
        CidrIp: 0.0.0.0/0
      SecurityGroupEgress:
      - IpProtocol: tcp
        FromPort: 22
        ToPort: 22
        CidrIp: 0.0.0.0/0
      - IpProtocol: tcp
        FromPort: 443
        ToPort: 443
        CidrIp: 0.0.0.0/0
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-EC2-SG

  #private Security Group
  PrivateEC2SecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: "Private-SG"
      VpcId: !Ref VPC
      SecurityGroupIngress:
      - IpProtocol: tcp
        FromPort: 22
        ToPort: 22
        CidrIp: 0.0.0.0/0
      SecurityGroupEgress:
      - IpProtocol: tcp
        FromPort: 22
        ToPort: 22
        CidrIp: 0.0.0.0/0
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-EC2-SG

  #IAM
  AdminIAMRole:
    Type: AWS::IAM::Role
    DeletionPolicy: Retain
    Properties:
      RoleName: !Sub ${EnvironmentName}-admin-role
      AssumeRolePolicyDocument: 
        Version: "2012-10-17"
        Statement: 
          - Effect: "Allow"
            Principal: 
              Service: 
                - "ec2.amazonaws.com"
            Action: 
              - "sts:AssumeRole"
      Path: "/"
      ManagedPolicyArns:
        - "arn:aws:iam::aws:policy/AdministratorAccess"

  AdminInstanceProfile:
    Type: AWS::IAM::InstanceProfile
    Properties:
      Path: /
      Roles:
      - !Ref 'AdminIAMRole'

Outputs:
  VPC:
    Description: "VPC"
    Value: !Ref VPC
    Export:
      Name:
        'Fn::Sub': '${AWS::StackName}-VPC'

  PublicSubnets:
    Description: A list of the public subnets
    Value: !Join [ ",", [ !Ref PublicSubnet1, !Ref PublicSubnet2 ]]

  PrivateSubnets:
    Description: A list of the private subnets
    Value: !Join [ ",", [ !Ref PrivateSubnet1, !Ref PrivateSubnet2 ]]

  PublicSubnet1:
    Description: "Public Subnet AZ a"
    Value: !Ref PublicSubnet1
    Export:
      Name:
        'Fn::Sub': '${AWS::StackName}-public-a'

  PublicSubnet2:
    Description: "Public Subnet AZ b"
    Value: !Ref PublicSubnet2
    Export:
      Name:
        'Fn::Sub': '${AWS::StackName}-public-b'

  PrivateSubnet1:
    Description: "Private Subnet AZ a"
    Value: !Ref PrivateSubnet1
    Export:
      Name:
        'Fn::Sub': '${AWS::StackName}-private-a'

  PrivateSubnet2:
    Description: "Private Subnet AZ b"
    Value: !Ref PrivateSubnet2
    Export:
      Name:
        'Fn::Sub': '${AWS::StackName}-private-b'

  BastionInstance:
    Description: "bastion Instance"
    Value: !Ref BastionInstance
    Export:
      Name:
          'Fn::Sub': '${AWS::StackName}-bastion-Instance'

  PirvateEC2Instance:
    Description: "private Instance"
    Value: !Ref PirvateEC2Instance
    Export:
      Name:
          'Fn::Sub': '${AWS::StackName}-private-Instance'

  BastionSecurityGroup:
    Description: "bastion Group"
    Value: !Ref BastionSecurityGroup
    Export:
      Name:
          'Fn::Sub': '${AWS::StackName}-bastion-SG'

  PrivateEC2SecurityGroup:
    Description: "private Group"
    Value: !Ref PrivateEC2SecurityGroup
    Export:
      Name:
          'Fn::Sub': '${AWS::StackName}-private-SG'

  AdminIAMRole:
    Description: "Private Instance"
    Value: !GetAtt AdminIAMRole.Arn
    Export:
      Name:
          'Fn::Sub': '${AWS::StackName}-Admin-role'
```