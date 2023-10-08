## KDF - Transfor Record

```python
import json
import base64

def lambda_handler(event, context):
    output = []

    for record in event['records']:
        print(record['recordId'])
        payload = base64.b64decode(record['data']).decode('utf-8')
        payload2 = transfor_data(payload)
        print(payload)
        

        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(payload2.encode('utf-8')).decode('utf-8')
        }
        output.append(output_record)

    print('Successfully processed {} records.'.format(len(event['records'])))

    return {'records': output}

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

    return json.dumps(body)alidation']['Id']
    return invalidation_id
```