## Buildspec - Force Rolling Update
---
### Buildspec Secsion
- pre_build
    - Environment AccountID
    - Environment Product ECR Name
    - Environment Stress ECR Name
    - Login ECR
    - Environment Product ECR URL
    - Environment Stress ECR URL
    - Environment Image Tag
- build
    - Docker Build Product Image
    - Docker Build Stress Image
- post_build
    - Docker Push ECR Product
    - Docker Push ECR Stress
    - ECS Update Rolling Update Force with Product
    - ECS Update Rolling Update Force with Stress