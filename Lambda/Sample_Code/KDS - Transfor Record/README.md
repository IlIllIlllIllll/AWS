## KDS - Transfor Record
**event**
```json
{
  "Records": [
    {
      "kinesis": {
        "partitionKey": "partitionKey-03",
        "kinesisSchemaVersion": "1.0",
        "data": "eyJ0aW1lIjoiMjAyMy0xMC0wNSAwNzoyODo0MyIsImhvc3QiOiIxMjcuMC4wLjEiLCJtZXRob2QiOiJHRVQiLCJwYXRoIjoiL3YxL2NvbG9yL21lbG9uIiwicHJvdG9jb2wiOiJIVFRQLzEuMSIsInN0YXR1c19jb2RlIjoiMjAwIn0=",
        "sequenceNumber": "49545115243490985018280067714973144582180062593244200961",
        "approximateArrivalTimestamp": 1428537600
      },
      "eventSource": "aws:kinesis",
      "eventID": "shardId-000000000000:49545115243490985018280067714973144582180062593244200961",
      "invokeIdentityArn": "arn:aws:iam::EXAMPLE",
      "eventVersion": "1.0",
      "eventName": "aws:kinesis:record",
      "eventSourceARN": "arn:aws:kinesis:EXAMPLE",
      "awsRegion": "us-east-1"
    }
  ]
}
```

<br>

```python
import base64
import json

def lambda_handler(event, context):
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        payload2 = transfor_data(payload)

def transfor_data(payload):
    data = json.loads(payload)
    data = data["log"]
    data = data.split()
    
    ls = []
    for i in data:
        ls.append(i)
    
    body = {
        "string": ls[0],
        "string": ls[1],
        "string": ls[2],
        "string": ls[3],
        "string": ls[4],
        "string": ls[5],
    }

    return json.dumps(body)
```