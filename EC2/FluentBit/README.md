## FluentBit
---
### Install FluentBit on EC2
```shell
curl https://raw.githubusercontent.com/fluent/fluent-bit/master/install.sh | sh
```

<br>

```shell
cat <<'EOF' > /etc/yum.repos.d/fluent-bit.repo
[fluent-bit]
name = Fluent Bit
baseurl = https://packages.fluentbit.io/amazonlinux/$releasever/$basearch/
gpgcheck=1
gpgkey=https://packages.fluentbit.io/fluentbit.key
repo_gpgcheck=1
enabled=1
EOF
```

<br>

```shell
yum install -y fluent-bit
systemctl start fluent-bit
sudo ln -s /opt/fluent-bit/bin/fluent-bit /usr/local/bin/fluent-bit
```

<br>

```shell
fluent-bit --version
Fluent Bit v2.1.9
Git commit:
```

<br>

```shell
cat /etc/fluent-bit/fluent-bit.conf | egrep -v '^$|#'
fluent-bit -c /etc/fluent-bit/fluent-bit.conf --dry-run
```

<br>

```shell
cat <<\EOF> /etc/fluent-bit/fluent-bit.conf
[SERVICE]
    Flush        1
    Log_Level    info
    Daemon       off

[INPUT]
    Name  tail
    Path <Log File Path>
    tag <Log Tag>

[OUTPUT]
    Name kinesis_streams
    Match *
    region <Region>
    stream <Kinesis Data Stream Name>

[OUTPUT]
    Name cloudwatch_logs
    Match   *
    region ap-northeast-2
    log_group_name <CloudWatch Log Group Name>
    log_stream_prefix <CloudWatch Log Stream Prefix>
    auto_create_group On
EOF
```

<br>

> EC2 Instance ID를 Tag로 지정하려면 아래와 같이 설정합니다. <br>
```shell
export instance_id=`aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" "Name=tag:Name,Values=<App EC2 Name>" --query "Reservations[].Instances[].InstanceId[]" --output text`

[INPUT]
    Name  tail
    Path <Log File Path>
    tag ${instance_id}
```

<br>

```shell
systemctl restart fluent-bit
```

<br>

```shell
nohup fluent-bit -c /etc/fluent-bit/fluent-bit.conf &
```