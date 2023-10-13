FROM golang:1.16.5
RUN mkdir /app
COPY main.go /app
WORKDIR /app
RUN go mod init example.com/m/v2 && go build -o main
CMD ["./main"]