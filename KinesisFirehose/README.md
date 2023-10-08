## Kinesis Data Firehose
---
**Kinesis Data Firehose Dynamic Partitioning란?**

지정된 값에 따라 그룹화된 데이터를 전달하는 것을 의합니다.

Kinesis Data Firehose에서 S3로 데이터를 전송하는 Prefix는 다음과 같습니다.
```
<S3 Bucket>/Year/Month/Day/Hour/
```
> 해당 값은 UTC 기준으로 업로드 됩니다.

---
### Kinesis Data Firehose Dynamic Partitioning
#### Example Log
**Transfor Log**
```
{
   "date": 2023-08-06 11:27:45,641,
   "IP: 127.0.0.1,
   "Methods": "GET"
   "Path": /v1/app,
   "Protocol": HTTP/1.1,
   "StatusCode: 200
}
```

<br>

**Default Dynamic Partitioning**

Method에 대해서 Partitioning은 다음과 같습니다.
```
Key     JQ experession
Method  .Method
```
