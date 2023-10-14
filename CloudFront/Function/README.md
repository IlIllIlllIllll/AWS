## CloudFront - Functions
---
### Access - Request URL
```javascript
function handler(event) {
    var request = event.request;
    var uri = request.uri;
    
    // Check whether the URI is missing a file name.
    if (uri.endsWith('/test/')) {
        request.uri += 'index.html';
    } 
    // Check whether the URI is missing a file extension.
    else if (!uri.includes('.')) {
        request.uri += '/index.html';
    }

    return request;
}
```

<br>

![Test CloudFront Function](https://github.com/IlIllIlllIllll/AWS/raw/main/CloudFront/Function/img/image-1.png)

![COnnect CloudFront Function](https://github.com/IlIllIlllIllll/AWS/raw/main/CloudFront/Function/img/image-2.png)