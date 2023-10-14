## SQL - CloudFront Access Log Query
---
### 가장 많은 요청한 IP, StatusCode Count 수 출력
```sql
SELECT request_ip, status, COUNT(*) AS cnt
FROM "cf_logs"."cloudfront_logs"
GROUP BY  request_ip, status
ORDER BY cnt DESC
limit 1;
```

<br>

### 가장 많은 요청한 IP, Count 수 출력
```sql
SELECT request_ip, COUNT(*) AS cnt 
FROM "cf_logs"."cloudfront_logs"
GROUP BY  request_ip
ORDER BY cnt DESC
limit 1;
```

<br>

### 가장 적게 요청한 IP, StatusCode Count 수 출력
```sql
SELECT request_ip, status, COUNT(*) AS cnt
FROM "cf_logs"."cloudfront_logs"
GROUP BY request_ip, status
ORDER BY cnt asc
limit 1;
```

---
### IP 및 User_Agent
```sql
SELECT request_ip, user_agent, COUNT(*) AS cnt
FROM "cf_logs"."cloudfront_logs"
where user_agent like 'Mozilla%'
GROUP BY request_ip, user_agent
ORDER BY cnt desc;
```

> CloudFront Access Log Query on Athena - https://boomkim.github.io/2019/06/07/athena-cf-log-analysis/