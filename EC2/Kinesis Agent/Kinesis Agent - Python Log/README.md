## Kinesis Agnet - Custom Log
---
### Kinesis Agent - Kinesis Data Stream
```json
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
```

<br>

```shell
aws kinesis create-stream --stream-name <KDS Name>
```

<br>

```shell
sudo yum instlal -y aws-kinesis-agent
```

<br>

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

<br>

```shell
vim /etc/aws-kinesis/agent.json
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

<br>

```shell
sudo chown aws-kinesis-agent-user:aws-kinesis-agent-user -R <path>
```

<br>

> ![filePattern User](https://github.com/IlIllIlllIllll/AWS/raw/main/EC2/Kinesis%20Agent/Kinesis%20Agent%20-%20Python%20Log/img/image-1.png)

<br>

```shell
vim /etc/sysconfig/aws-kinesis-agent
# Set AWS credentials for accessing Amazon Kinesis Stream and Amazon Kinesis Firehose
#
# AWS_ACCESS_KEY_ID=<Access Key>
# AWS_SECRET_ACCESS_KEY=<Secret Access Key>
# AWS_DEFAULT_REGION=<region>
#
# AGENT_ARGS=""
# AGENT_LOG_LEVEL="INFO"
```

<br>

```shell
sudo service aws-kinesis-agent restart
sudo chkconfig aws-kinesis-agent on
```
<br>

```shell
sudo tail -f /var/log/aws-kinesis-agent/aws-kinesis-agent.log
```

<br>

![Successed Record in KDS](https://github.com/IlIllIlllIllll/AWS/raw/main/EC2/Kinesis%20Agent/Kinesis%20Agent%20-%20Python%20Log/img/image-2.png)

<br>

### 주의 
> 만약 /home/ec2-user경로에 Log File이 존재시 Parsing에 대해서 Error가 발생합니다. 