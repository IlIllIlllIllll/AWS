## Buildspec - Force Rolling Update
---
### Buildspec Secsion
- pre_build
    - Environment AccountID
    - Environment ECR Name
    - Login ECR
    - Environment ECR URL
    - Environment Image Tag
- build
    - Docker Build Image
- post_build
    - Docker Push ECR
    - Change to Image on Taskdefinition
- artifacts
    - 'appspec.yaml'
    - 'taskdef.json'