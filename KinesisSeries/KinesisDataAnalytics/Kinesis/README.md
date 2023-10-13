## Kiensis Data Analytics - NoteBook
---
### KDS NoteBook - Kinesis
**Create Table**
```sql
%flink.ssql(type=update)

DROP TABLE IF EXISTS wsi_logs;

CREATE TABLE wsi_logs (
`host` VARCHAR,
`method` VARCHAR,
`path` VARCHAR,
`protocol` VARCHAR,
`statuscode` INTEGER
)
WITH (
'connector' = 'kinesis',
'stream' = 'wsi-stream',
'aws.region' = 'ap-northeast-2',
'scan.stream.initpos' = 'LATEST',
'format' = 'json'
);
```

<br>

**Select Table**
```sql
%flink.ssql(type=update)
select * from wsi_logs;
```
![Select KDA NoteBook Table](https://github.com/IlIllIlllIllll/AWS/raw/main/KinesisDataAnalytics/Kinesis/img/image-1.png)