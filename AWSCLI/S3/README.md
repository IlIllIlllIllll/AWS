## S3
---
### S3 Create

#### Create S3 Bucket
```
aws s3 mb s3://<S3 Bucket Name> --region <Region>
```

#### Create S3 Bucket Folder
```
aws s3api put-object --bucket <S3 Bucket Name> --key "<Folder Name>/" --region <Region>
```

#### Create S3 Bucket File
```
aws s3api put-object --bucket <S3 Bucket Name> --key "<File Name>" --region <Region>
```

---

### S3 Delete
#### Delete S3 Bucket
```
aws s3 rb s3://<S3 Bucket Name> --region <Region>
```

#### Force Delete S3 Bucket
```
aws s3 rb s3://<S3 Bucket Name> --region <Region> --force
```

#### Delete S3 File
```
aws s3 rm s3://<S3 Bucket Name>/<File name>
```

### Delete S3 File on All Object
```
aws s3 rm s3://<S3 Bucket Name>/<Folder> --recursive
```

---

### S3 Select
#### Select S3 Bucket List
```
aws s3 ls 
```

#### Select S3 Bucket Folder List
```
aws s3 ls s3://<S3 Bucket Name>
```

---

### S3 Upload

#### Upload File on S3 Bucket
```
aws s3 cp <File Name> s3://<S3 Bucket Name>
```

#### Upload Folder on S3 Bucket
```
aws s3 cp <Folder Name> s3://<S3 Bucket Name>
```

####
```
aws s3 sync s3://<S3 Bucket Name>
```

---

### S3 Move
#### Move S3 Bucket Folder on S3 Bucket
```
aws s3 mv s3://<S3 Bucket Name> s3://<S3 Bucket Name>/
```

#### Move S3 Bucket File on Folder
```
aws s3 mv <File Name> s3://<S3 Bucket Name>
```

#### Move S3 Bucket Folder on Folder
```
aws s3 mv s3://<S3 Bucket name>/<File Name> <Path>
```