## Kinesis Agnet - Custom Log
---
### Kinesis Agent - Kinesis Data Stream
```json
cat <<EOF>> put-kds.json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "cloudwatch:PutMetricData",
                "kinesis:PutRecords"
            ],
            "Resource": "*"
        }
    ]
}
EOF
```

```shell
aws kiensis create-stream --stream-name <KDS Name>
```

```shell
sudo yum instlal -y aws-kinesis-agent
sudo systemctl start aws-kinesis-agent
sudo chkconfig aws-kinesis-agent on
```

```python
import logging
import json
from datetime import datetime
import calendar
import random
import time

logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(asctime)s %(message)s')



def put_to_stream(id, value, timestamp):
    payload = {
                'random': str(value),
                'timestamp': str(timestamp),
                'id': id
              }

    response ='Putting to stream: ' + str(payload)
    logging.debug(response)


while True:
    value = random.randint(1, 100)
    timestamp = calendar.timegm(datetime.utcnow().timetuple())
    id = 'stream-1'

    put_to_stream(id, value, timestamp)

    time.sleep(5)
```

```shell
vi /etc/aws-kinesis/agent.json
{
    "cloudwatch.emitMetrics":true,
    "kinesis.endpoint":"https://kinesis.ap-northeast-2.amazonaws.com",
    "flows":[
       {
          "filePattern":"<Log Path>*",
          "kinesisStream":"<KDS Name>"
       }
    ]
 }
```

```shell
sudo chown aws-kinesis-agent-user:aws-kinesis-agent-user -R /opt/kinesis-stream
```
> ![filePattern User](https://github.com/IlIllIlllIllll/AWS/raw/main/EC2/kinesis-agent/img/image-1.png)

```shell
vim /etc/sysconfig/aws-kinesis-agent
# Set AWS credentials for accessing Amazon Kinesis Stream and Amazon Kinesis Firehose
#
# AWS_ACCESS_KEY_ID=<Access Key>
# AWS_SECRET_ACCESS_KEY=<Secret Access Key>
# AWS_DEFAULT_REGION=ap-northesat-2
#
# AGENT_ARGS=""
# AGENT_LOG_LEVEL="INFO"
```

```shell
sudo service aws-kinesis-agent start
```

```shell
sudo tail -f /var/log/aws-kinesis-agent/aws-kinesis-agent.log
```
![Successed Record in KDS](https://github.com/IlIllIlllIllll/AWS/raw/main/EC2/kinesis-agent/img/image-2.png)