## ECR
---
#### Create ECR Repository
```
aws ecr create-repository --repository-name <ECR Name> --region <Region>
```

#### Delete ECR Repository
```
aws ecr delete-repository --repository-name <ECR Name> --force --region <Region>
```

#### Delete ECR Image
```
aws ecr batch-delete-image --repository-name <ECR Name> --image-ids imageTag=<Image Tag> --region <Region>
```

#### Create ECR Repository with Image Scaning
```
aws ecr create-repository --repository-name <ECR Name> --image-scanning-configuration scanOnPush=true --region <Region>
```

#### Create ECR Repository with Image Tag Mutability
```
aws ecr create-repository --repository-name <ECR Name> --image-tag-mutability <Value>
```
> MUTABLE : Image Tag 덮어쓰기 가능 <br>
IMMUTABLE : Image Tag 덮어쓰기 불가능