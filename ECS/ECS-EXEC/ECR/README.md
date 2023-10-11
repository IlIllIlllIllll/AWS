## ECS Images
---
```shell
aws ecr create-repository --repository-name <ECR Name> --region <Region>
```

```go
package main

import (
   "github.com/gin-gonic/gin"
   "net/http"
)

func health(c *gin.Context) {
   c.String(http.StatusOK, "OK")
}

func product(c *gin.Context) {
   c.String(http.StatusOK, "Product")
}

func main() {
   router := gin.Default()

   router.GET("/health", health)

   router.GET("/v1/product", product)

   router.Run(":8080")
}
```

### Dockerfile
```Dockerfile
FROM golang:alpine
WORKDIR /app
COPY ./app.go .
RUN go mod init app
RUN apk --no-cache add curl
RUN go mod tidy
RUN go build app.go
EXPOSE 8080
CMD ["./app"]
```