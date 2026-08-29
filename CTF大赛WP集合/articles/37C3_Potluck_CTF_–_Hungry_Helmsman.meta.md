---
title: 37C3 Potluck CTF – Hungry Helmsman
contest: 37C3 Potluck CTF
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [Kubernetes, kubeconfig, RBAC, namespace权限, PodSecurity restricted, ResourceQuota, NetworkPolicy, flag-sender, flag-reciever, nc -l 监听, busybox]
attack_chain:
  - nc challenge10.play.potluckctf.com 8888 拿 Kubeconfig (含 token JWT)
  - kubectl --kubeconfig config 切换上下文
  - kubectl get ns 看到 flag-sender + flag-reciever 两个 namespace
  - kubectl get pods -n flag-sender 看到 flag-sender-xxx pod, command=while true; do echo $FLAG | nc 1.1.1.1 80; done
  - kubectl auth can-i --list -n flag-reciever 看到 pods.* create/delete 权限
  - 创建 busybox pod, PodSecurity restricted 要求: allowPrivilegeEscalation=false, drop=["ALL"], runAsNonRoot=true, seccompProfile=RuntimeDefault
  - ResourceQuota 要求: limits.cpu 200m, limits.memory 100M, requests.cpu 100m, requests.memory 50M
  - 加 resources.requests/limits + securityContext
  - NetworkPolicy 允许 ns=flag-sender + app=flag-sender 入向任意端口
  - 改 busybox args 为 ["sh", "-c", "nc -l -v -p 80"] 在 80 端口监听, 接收 flag-sender 的 $FLAG 外发
key_payload: 'Kubeconfig token / RBAC pods.* create/delete / PodSecurity restricted securityContext / ResourceQuota 50M/100m / NetworkPolicy ns=flag-sender + app=flag-sender / busybox nc -l -v -p 80'
one_liner: 37C3 Potluck CTF Hungry Helmsman — Kubernetes RBAC+PodSecurity+ResourceQuota+NetworkPolicy 链：拿 Kubeconfig → 创建受约束 pod → 监听 80 端口等 flag-sender nc 推 $FLAG。
lesson: K8s RBAC 边界是 namespace；PodSecurity restricted 是 v1.25+ 默认；NetworkPolicy 控制 ingress/egress 是常见容器逃逸限制；busybox 镜像通常白名单。
quality: high
---

# 37C3 Potluck CTF – Hungry Helmsman

## 速读
37C3 (2023 年 Chaos Communication Congress) 旗下 Potluck CTF — 经典 K8s RBAC 题目。

## 步骤
1. **拿 Kubeconfig** — `nc challenge10.play.potluckctf.com 8888` 返回含 JWT token
2. **看权限** — `kubectl auth can-i --list -n flag-reciever` 看到 pods/services create/delete
3. **创建 pod 遇 PodSecurity restricted** — 需 securityContext 全套:
   - allowPrivilegeEscalation: false
   - runAsNonRoot: true
   - capabilities.drop: ["ALL"]
   - seccompProfile.type: RuntimeDefault
4. **遇 ResourceQuota** — 需 resources.requests/limits:
   - requests.cpu=50m, memory=50M
   - limits.cpu=200m, memory=100M
5. **网络策略** — NetworkPolicy 允许 ns=flag-sender + app=flag-sender 任意入向端口
6. **监听收 flag** — 改 pod args 为 `nc -l -v -p 80`，等 flag-sender 外发 $FLAG
