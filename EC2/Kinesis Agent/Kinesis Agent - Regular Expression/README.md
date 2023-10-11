## Kinesis Agnet - Regular Expression
---
### Kinesis Agent - Kinesis Data Stream
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "cloudwatch:PutMetricData",
                "kinesis:PutRecords"
            ],
            "Resource": "*"
        }
    ]
}
```

<br>

```shell
aws kinesis create-stream --stream-name <KDS Name>
```

<br>

```shell
sudo yum instlal -y aws-kinesis-agent
```

<br>

```go
package main

import (
	"github.com/gin-gonic/gin"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
)

func main() {
	// 로그 파일 생성
	logFile, err := os.Create("app.log")
	if err != nil {
		panic(err)
	}
	defer logFile.Close()

	// Gin 엔진 설정
	router := gin.Default()

	// 로깅 미들웨어 추가
	router.Use(func(c *gin.Context) {
		// 클라이언트 주소를 IPv4 형식으로 변환
		clientAddr := strings.Replace(c.Request.RemoteAddr, "[::1]", "127.0.0.1", -1)

		// 원하는 로그 포맷 생성
		logMsg := clientAddr + " - - " + c.Request.Method + " " + c.FullPath() + " " +
			c.Request.Proto + " " + strconv.Itoa(c.Writer.Status()) // 정수를 문자열로 변환

		// 로그 파일에 기록
		logFile.WriteString(logMsg + "\n")

		// 기본 로그 출력
		log.Print(logMsg)

		c.Next()
	})

	// Health Check 엔드포인트
	router.GET("/healthz", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"Status": "OK"})
	})

	// 정적 메시지 엔드포인트
	router.GET("/v1/static", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"msg": "web static"})
	})

	// 서버 시작
	router.Run(":8080")
}
```

<br>

```shell
vim /etc/aws-kinesis/agent.json
{
    "cloudwatch.emitMetrics":true,
    "kinesis.endpoint":"https://kinesis.ap-northeast-2.amazonaws.com",
    "flows":[
       {
          "filePattern":"<Log Path>*",
          "kinesisStream":"<KDS Name>",
          "dataProcessingOptions": [
                {
                    "optionName": "LOGTOJSON",
                    "logFormat": "COMMONAPACHELOG",
                    "matchPattern": "^([ ^:]*) - - ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*)",
                    "customFieldNames": ["host", "method", "path", "protocol", "statuscode"]
                }
            ]
        }
    ]
}
```

<br>

```shell
sudo chown aws-kinesis-agent-user:aws-kinesis-agent-user -R <path>
```

<br>

> ![filePattern User](https://github.com/IlIllIlllIllll/AWS/raw/main/EC2/Kinesis%20Agent/Kinesis Agent/Kinesis Agent - Regular Expression/img/image-1.png)

<br>

```shell
vim /etc/sysconfig/aws-kinesis-agent
# Set AWS credentials for accessing Amazon Kinesis Stream and Amazon Kinesis Firehose
#
# AWS_ACCESS_KEY_ID=<Access Key>
# AWS_SECRET_ACCESS_KEY=<Secret Access Key>
# AWS_DEFAULT_REGION=<region>
#
# AGENT_ARGS=""
# AGENT_LOG_LEVEL="INFO"
```

<br>

```shell
sudo service aws-kinesis-agent restart
sudo chkconfig aws-kinesis-agent on
```
<br>

```shell
sudo tail -f /var/log/aws-kinesis-agent/aws-kinesis-agent.log
```

<br>

![Successed Record in KDS](https://github.com/IlIllIlllIllll/AWS/raw/main/EC2/Kinesis%20Agent/Kinesis%20Agent%20-%20Python%20Log/img/image-2.png)

<br>

### 주의 
> 만약 /home/ec2-user경로에 Log File이 존재시 Parsing에 대해서 Error가 발생합니다.