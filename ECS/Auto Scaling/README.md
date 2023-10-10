### ECS - Auto Scaling
---
![Enable Service Auto Scaling](https://github.com/IlIllIlllIllll/AWS/raw/main/ECS/Auto%20Scaling/img/image-1.png)

![Setting Service Auto Scaling](https://github.com/IlIllIlllIllll/AWS/raw/main/ECS/Auto%20Scaling/img/image-2.png)

<br>
Minimum number of tasks : Task의 최소 개수를 정의합니다.
Desired number of tasks : 동작시킬 Task의 개수를 정의합니다.
Maximum number of tasks : Task의 최종 개수를 정의합니다
IAM role for Service Auto Scaling : Service Auto Scaling을 위한 IAM Role을 생성합니다.
> 처음 IAM Role for Service Auto Scaling생성 시 자동으로 생성됩니다.

<br>

![Setting Service Auto Scaling](https://github.com/IlIllIlllIllll/AWS/raw/main/ECS/Auto%20Scaling/img/image-3.png)

<br>
Scaling policy type : Scaling 방식을 정의합니다.
- Target Tracking : ECS Service의 사용량에 따라 Scaling을 정의합니다.
- Step Scaling : CloudWatch Alarm을 통하여 해당 통계값이 어떠한 조건일 때 Scaling 할 것인지를 정의합니다.

> ![Explain Service Auto Scaling](https://github.com/IlIllIlllIllll/AWS/raw/main/ECS/Auto%20Scaling/img/image-4.png) <br>
![Explain Service Auto Scaling](https://github.com/IlIllIlllIllll/AWS/raw/main/ECS/Auto%20Scaling/img/image-5.png) <br>
![Explain Service Auto Scaling](https://github.com/IlIllIlllIllll/AWS/raw/main/ECS/Auto%20Scaling/img/image-6.png)
