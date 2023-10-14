## S3 - Route53 Web Site Hosting
---
```
aws s3 mb s3://we.web.local
``` 
```
aws s3 cp index.html s3://we.web.local
```

<br>

![Create S3 Static Web Stie Hosting](https://github.com/IlIllIlllIllll/AWS/raw/main/S3/Route53%20Static%20Web%20Site%20Hosting/img/image-1.png)

![Change to Bucket Access](https://github.com/IlIllIlllIllll/AWS/raw/main/S3/Route53%20Static%20Web%20Site%20Hosting/img/image-2.png)

![Apply S3 Bucket Policy ](https://github.com/IlIllIlllIllll/AWS/raw/main/S3/Route53%20Static%20Web%20Site%20Hosting/img/image-3.png)

![Create Route53 Domain](https://github.com/IlIllIlllIllll/AWS/raw/main/S3/Route53%20Static%20Web%20Site%20Hosting/img/image-4.png)

![Create Route53 Domain](https://github.com/IlIllIlllIllll/AWS/raw/main/SS3/Route53%20Static%20Web%20Site%20Hosting/img/image-5.png)

![Create Route53 Record](https://github.com/IlIllIlllIllll/AWS/raw/main/S3/Route53%20Static%20Web%20Site%20Hosting/img/image-6.png)

![Result Value](https://github.com/IlIllIlllIllll/AWS/raw/main/S3/Route53%20Static%20Web%20Site%20Hosting/img/image-7.png)

<br>

> Error <br> <span style="color:red"> Cannot retrieve endpoint suggestions </span> <br> 해당 에러는 S3 Bucket이 Public Access 설정이 되어 있지 않아 발생하는 에러입니다. S3 Bucket을 Public Access 및 S3 Bucket Policy를 활성해주면 됩니다.

> S3 - Rotue53 Web Site Hosting <br/>
https://repost.aws/questions/QUJNe3VZr9QsylqlwZreikTQ/trying-to-create-a-record-in-route53-shows-no-resources-found <br/>  https://docs.aws.amazon.com/ko_kr/Route53/latest/DeveloperGuide/troubleshooting-s3-bucket-website-hosting.html

![S3 Route53](https://github.com/IlIllIlllIllll/AWS/raw/main/S3/Route53%20Static%20Web%20Site%20Hosting/img/image-8.png)