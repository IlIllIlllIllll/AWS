## Kinesis Agent - Regular Expression Example
---
### Log Format
```
127.0.0.1:42014 - - GET /healthz HTTP/1.1 200
```

<br>

### Regular Expression Sample - Scenario 1
```json
"matchPattern": "^([^:]*):[^ ]* - - ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*)",
"customFieldNames": ["host", "method", "path", "protocol", "statuscode"]
```

```json
{
    "host": "127.0.0.1",
    "method": "GET",
    "path": "/healthz",
    "protocol": "HTTP/1.1",
    "statuscode": "200"
}
```

<br>

### Regular Expression Sample - Scenario 2
```json
"matchPattern": "^([^ ]*) - - ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*)",
"customFieldNames": ["host", "method", "path", "protocol", "statuscode"]
```

```json
{
    "host": "127.0.0.1:42014",
    "method": "GET",
    "path": "/healthz",
    "protocol": "HTTP/1.1",
    "statuscode": "200"
}
```

<br>

### Regular Expression Sample - Scenario 3
```json
"matchPattern": "^.+(?=:)",
"customFieldNames": ["host"]
```

```json
{
    "host": "127.0.0.1"
}