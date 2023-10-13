## Kinesis Data Firehose - Dynamic Partitioning
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
```
{
   "date": 2023-08-06 11:27:45,
   "ip: 127.0.0.1,
   "methods": "GET"
   "path": /v1/app,
   "protocol": HTTP/1.1,
   "statusCode: 200
}
```

<br>

**Default Dynamic Partitioning**

<S3 Bucket>/method에 대해서 Partitioning을 진행할 시 다음과 같습니다.
```
Key     JQ experession
method  .method
```
S3 Bucket Prefix
```
!{partitionKeyFromQuery:method}
```

<br>

<S3 Bucket>/path/method에 대해서 Partitioning은 다음과 같습니다.
```
Key     JQ experession
path    .path
method  .method
```
S3 Bucket Prefix
```
!{partitionKeyFromQuery:path}/!{partitionKeyFromQuery:method}/
```

<br>

<S3 Bucket>/year/month/day에 대해서 Partitioning은 다음과 같습니다.
```
Key     JQ experession
year   .date| strptime("%Y-%m-%d %H:%M:%S")| strptime("%Y)
month  .date| strptime("%Y-%m-%d %H:%M:%S")| strptime("%m)
day    .date| strptime("%Y-%m-%d %H:%M:%S")| strptime("%d)
```
S3 Bucket Prefix
```
!{partitionKeyFromQuery:year}/!{partitionKeyFromQuery:month}/!{partitionKeyFromQuery:day}
```

<S3 Bucket>/year/method에 대해서 Partitioning은 다음과 같습니다.
```
Key     JQ experession
year    .date| strptime("%Y-%m-%d %H:%M:%S")| strptime("%Y)
method  .method
```
S3 Bucket Prefix
```
!{partitionKeyFromQuery:year}/method/
```

> Kiensis Data Firehose Dynamic Partitioning - https://velog.io/@arcokim/firehose-dynamic-partitioning