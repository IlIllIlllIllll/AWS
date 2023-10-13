## Code Series EC2


1. Create code commit
    ```bash
    aws codecommit create-codecommit --repository-name aws-codecommit --region ap-northeast-2
    ```
2. git-remote-codecommit install
    ```bash
    pip install git-remote-codecommit
    ```
    If you proceed with Amazon linux2, install the pip package and then install the git package.
    ```bash
    yum install -y python-pip
    yum install -y git
    ```
3. Clones the repository.
    ```bash
    git clone codecommit::ap-northeast-2://aws-codecommit
    ```

## install codedeploy agent

1. shell script

    ```bash
    #!/bin/bash
    yum update -y
    yum install -y ruby
    yum install -y wget
    cd /home/ec2-user
    wget https://aws-codedeploy-ap-northeast-2.s3.ap-northeast-2.amazonaws.com/latest/install
    chmod +x ./install
    sudo ./install auto
    sudo service codedeploy-agent start
    ```
