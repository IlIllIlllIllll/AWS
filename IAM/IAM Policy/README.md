> ABAC - https://whchoi98.gitbook.io/aws-iam/iam-tag <br>
IAM Action - https://docs.aws.amazon.com/ko_kr/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html <br>
IAM Policy - https://inpa.tistory.com/entry/AWS-%F0%9F%93%9A-IAM-Policy-JSON-%EA%B5%AC%EC%A1%B0-Arn-%EB%AC%B8%EB%B2%95-%EC%A0%95%EB%A6%AC?category=947441

---
## Json Format
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ownEC2",
            "Effect": "Allow",
            "Action": "ec2:*",
            "Resource": "*"
        }
    ]
}
```
<br>

## IAM Policy Components
---
### Version
- 정책 요소는 정책의 처리에 사용할 언어 구문 규칙을 지정합니다. 구성요소는 2012, 2008이 있습니다. 서로 다른 버전을 사용해서 서로 다른 부분이 있습니다. 사용 가능한 모든 정책 기능을 사용하려면 모든 정책에서 Version 요소 다음의 Statement 요소를 포함 시켜야 합니다.

```
"Version": "2012-10-17"
```

<br>

### Id
- 정책 식별자를 지정합니다.
```
"Id": "cd3ad3d9-2776-4ef1-a904-4c229d1642ee"
```

<br>

### Statement
- 정책의 주요 요소로서 필수입니다. 단일 문 또는 개별 문의 배열을 포함할 수 있습니다. 개별문 블록은 중괄호 {}로 묶어줘야 합니다. 여러 문을 사용할 경우 대괄호 []로 묶어줘야 합니다.
```
"Statement": [
	{...},
	{...},
	{...}
]
```

<br>

### Sid
- 정책 문에 입력되는 식별자를 제공할 수 있습니다. ASCII 대문자(A~Z), 소문자(a~z), 및 숫자(0~9)를 지원합니다. Sid 값은 JSON 정책 내 고유성이 보장되어야 합니다.
```
"Sid": "1"
```

<br>

### Effect
- 해당 요소는 필수입니다. 허용(allow), 명시적 거부(explicit deny) 중 하나를 지정해줍니다. 해당 Effect는 액세스의 허용 여부를 정의합니다. Effect의 유호 값은 Allow, Deny로 구성됩니다.
```
"Effect":"Allow"
"Effect":"Deny"
```

<br>

### Action
- 특정 작업의 허용 또는 거부 여부를 지정합니다. Action 또는 NotAction 요소가 반드시 추가되어야 합니다.
```
"Action": "ec2:StartInstances”
```

<br>

### Resource
- Resource 요소는 문에서 다루는 객체를 지정합니다. Resource, NotResource 요소는 반드시 추가되어야 합니다. Arn을 사용하여 지정합니다. 특 Arn으로 설정하면 특정 리소스에 대해 액세스를 허용할 수 있으며, 작업이 적용되는 리소스 목록을 지정할 수 있습니다.
```
"Resource": "arn:aws:sqs:ap-northeast-2:account-ID-without-hyphens:queue1”
"Resource": "*"
```

<br>

### Condition
- Condition 요소를 사용하여 정책의 효력이 발생하는 시점에 대한 조건을 지정할 수 있습니다.
```
"Condition": {
	"StringEquals": {
		"aws:username": "admin"
	}
}
```
> AWS Username이 admin인 사람에게 권한을 부여합니다. <br>
aws:username 이 부분에서 aws는 리소스를 가르킵니다.
즉, ec2:username : admion으로 되어있다면, ec2 중 username이라는 Key를 가지고 admin이라는 Value를 가지고 있다면 그 리소스를 가르키는 것입니다.

<br>

### Condition Example
EC2에 대한 모든 작업을 허용하는 정책입니다. 모든 리소스가 작업을 할 수 있습니다. <br>
그러나 하나의 조건이 있습니다. EC2 리소스의 Tag 중 owner: username에 따라 작업의 가능 여부가 판단됩니다. <br>
즉, EC2 Tag 중 owner key 값이 자신의 계정으로 되어있는 EC2만 시작, 정시, 삭제, Tag 수정이 가능하게 구성합니다.
```json
{
    "Sid": "ownEC2",
    "Effect": "Allow",
    "Action": "ec2:*",
    "Resource": "*",
    "Condition": {
        "StringEquals": {
            "ec2:ResourceTag/owner": "${aws:username}"
        }
    }
}
```

<br>

- 리소스 태그에 따라서 행동할 수 있게 하는 방법은 아래 ResourceTag에 team(key):devops(value)가 있으면 도메인 설정을 보고 업데이트 할 수 있습니다.

<br>

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "es:UpdateDomainConfig",
                "es:DescribeDomain",
                "es:DescribeDomainConfig"
            ],
            "Effect": "Allow",
            "Resource": "*",
            "Condition": {
                "ForAnyValue:StringEquals": {
                    "aws:ResourceTag/team": [ //important
                        "devops"
                    ]
                }
            }
        }
    ]
}
```

<br>

- 사용자마다 EC2 인스턴스를 다룰 수 있도록 하는 태그 기반 정책입니다. 해당 username을 변수로 지정해서 사용자가 로그인하면 username에 적용됩니다.

<br>

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "iam:CreateAccessKey",
            "Resource": "arn:aws:iam::*:user/${aws:username}"
        },
        {
            "Sid": "UserList",
            "Effect": "Allow",
            "Action": "iam:ListUsers",
            "Resource": "*"
        },
        {
            "Sid": "ec2GetAll",
            "Effect": "Allow",
            "Action": [
                "ec2:Describe*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "ownEC2",
            "Effect": "Allow",
            "Action": "ec2:*",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "ec2:ResourceTag/owner": "${aws:username}"
                }
            }
        }
    ]
}
```