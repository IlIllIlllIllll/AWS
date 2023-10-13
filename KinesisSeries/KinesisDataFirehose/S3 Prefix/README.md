## Kinesis Data Firehose - S3 Save Prefix
---
Kinesis Data Firehose에서 S3로 데이터를 전송하는 Prefix는 다음과 같습니다.
```
<S3 Bucket>/Year/Month/Day/Hour/
```
> 해당 값은 UTC 기준으로 업로드 됩니다.

---
### Timestamp
```
!{timestamp:yyyy} #년
!{timestamp:MM} #월
!{timestamp:dd} #일
!{timestamp:HH} #시
```

<br>

### Error Output Type
```
!{firehose:error-output-type} #해당 S3 Error Prefix 값을 가져옵니다.
```

<br>

### Random Value
```
!{firehose:random-string} #11자의 무작위의 문자열을 생성합니다.
```

> S3 Svae Prefix - https://docs.aws.amazon.com/ko_kr/firehose/latest/dev/s3-prefixes.html