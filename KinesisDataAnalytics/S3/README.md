## Kiensis Data Analytics - NoteBook
---
### KDS NoteBook - S3
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
'connector' = 'filesystem',
'path' = 's3a://wsi-bucket-2023/output/',
'format' = 'json',
'sink.partition-commit.policy.kind' = 'success-file'
);
```

<br>

**Select Table**
```sql
%flink.ssql(type=update)
select * from wsi_logs;
```
![Select KDA NoteBook Table](https://github.com/IlIllIlllIllll/AWS/raw/main/KinesisDataAnalytics/S3/img/image-1.png)

<br>

---
### Upload S3
```
%flink.ssql(type=update)
-- %flink.ssql(type=update, parallelism=4)
INSERT INTO wsi-bucket-2023/output/
SELECT
TUMBLE_END(event_time, INTERVAL '1' MINUTE ) as window_end_time,
AVG(buffer) as avg_price,
ip,
network_input,
title,
DATE_FORMAT(event_time, 'yyyy-MM-dd') as dt,
DATE_FORMAT(event_time, 'HH') as ht
FROM game_table
WHERE buffer > 90
GROUP BY TUMBLE(event_time, INTERVAL '1' MINUTE), event_time, title, network_input, ip;
```