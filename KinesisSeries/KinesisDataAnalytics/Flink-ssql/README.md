## Kiensis Data Analytics - NoteBook
---
### KDA NoteBook - Query
**Sample Table**
```sql
%flink.ssql
CREATE TABLE IF NOT EXISTS log_table (
  `time` TIMESTAMP(3),
  `ip` STRING,
  `http_method` STRING,
  `request_path` STRING,
  `http_version` STRING,
  `http_status` STRING,
  `response_time` DOUBLE,
  WATERMARK FOR `time` AS `time` - INTERVAL '5' SECOND
)
WITH (
  'connector' = 'kinesis',
  'stream' = 'my-stream',
  'aws.region' = 'ap-northeast-2',
  'scan.stream.initpos' = 'TRIM_HORIZON',
  'format' = 'json'
);
```

---

<br>

**최근 10분간 요청량 조회**
```sql
%flink.ssql
SELECT count(*) AS COUNT
FROM log_table
WHERE ts >= LOCALTIMESTAMP - INTERVAL '10' MINUTES;
```

<br>

**최근 10분 동안 경로/메소드/상태코드 별 카운트 분석**
```sql
%flink.ssql
SELECT `http_method`, `request_path`, `http_status`, COUNT(*) AS `COUNT`
FROM log_table
WHERE `time` >= LOCALTIMESTAMP - INTERVAL '10' MINUTES
GROUP BY `http_method`, `request_path`, `http_status`;
```

<br>

**10분 단위로 윈도우 생성 후 요청량 분석 (TUMBLE 윈도우)**
```sql
%flink.ssql
SELECT window_start, window_end, COUNT(*)
  FROM TABLE(
      TUMBLE(TABLE log_table, DESCRIPTOR(`time`), INTERVAL '10' MINUTES))
  GROUP BY window_start, window_end;
```

<br>

**10분 단위로 윈도우 생성 후 경로/메소드/상태코드 별 카운트 분석 (TUMBLE 윈도우)**
```sql
%flink.ssql
SELECT window_start, window_end, `http_method`, `request_path`, `http_status`, COUNT(*) AS `count`
  FROM TABLE(
      TUMBLE(TABLE log_table, DESCRIPTOR(`time`), INTERVAL '10' MINUTES))
  GROUP BY  window_start, window_end, `http_method`, `request_path`, `http_status`
```

<br>

**10분 단위로 윈도우 생성 후 요청량 분석 (SLIDE 윈도우, 5분 허용)**
```sql
SELECT window_start, window_end, COUNT(*)
  FROM TABLE(
    HOP(TABLE log_table, DESCRIPTOR(`time`), INTERVAL '5' MINUTES, INTERVAL '10' MINUTES))
  GROUP BY window_start, window_end;
```

<br>

**10분 단위로 윈도우 생성 후 경로/메소드/상태코드 별 카운트 분석 (SLIDE 윈도우, 5분 허용)**
```sql
%flink.ssql
SELECT window_start, window_end, `http_method`, `request_path`, `http_status`, COUNT(*) AS `count`
  FROM TABLE(
      HOP(TABLE log_table, DESCRIPTOR(`time`), INTERVAL '5' MINUTES, INTERVAL '10' MINUTES))
  GROUP BY  window_start, window_end, `http_method`, `request_path`, `http_status`;
```