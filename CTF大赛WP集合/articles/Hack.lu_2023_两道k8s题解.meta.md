---
title: Hack.lu 2023 两道k8s题解
contest: Hack.lu 2023
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [k8s, kubernetes, crd, operator, flagrequest, anti-bruteforce, watch]
attack_chain:
  - 题目：两个 K8s 题目涉及 CRD
  - Flagrequest CRD + Flagprotector CRD
  - 创建 name=give-flag Flagrequest
  - 必须含 hack.lu/challenge-name 标签
  - spec.anti-bruteforce = "Bi$wmX4PBTQLGe%AIKPO19$ussap4w"
  - Kubernetes Python operator 监听 watch
  - 删除 flagprotector CRD（不删除则被拒）
  - 创建合法 Flagrequest
  - Operator 创建 Flag CRD 返回 flag
key_payload: metadata.name=give-flag + labels.hack.lu/challenge-name=give-flag + spec.anti-bruteforce=Bi$wmX4PBTQLGe%AIKPO19$ussap4w
one_liner: Hack.lu 2023 K8s：CRD Flagrequest+operator+anti-bruteforce token
lesson: K8s CRD challenge常需理解operator watch流程+反token条件
quality: high
---

# Hack.lu 2023 两道k8s题解

## 题目信息
- 比赛：Hack.lu 2023
- 类别：Kubernetes
- 主办：FluxFingers

## 关键攻击链
### 1. CRD 定义
- `ctf.fluxfingers.hack.lu/v1`
- Kind: Flagrequest / Flagprotector / Flag

### 2. 攻击流程
```python
def check_flagrequest(obj, crds, group, version, flagprotector_plural):
    fp = crds.list_namespaced_custom_object(group, version, "flagprotector", flagprotector_plural)
    if len(fp["items"]) > 0:
        return False, "A Flagprotector is deployed somewhere in the cluster, you need to delete it first!"
    
    fr = json.loads(json.dumps(obj))
    if "metadata" not in fr.keys():
        return False, "Flagrequest: Missing metadata"
    if "labels" not in fr["metadata"].keys():
        return False, "Flagrequest: Missing labels"
    if "hack.lu/challenge-name" not in fr["metadata"]["labels"].keys():
        return False, "Flagrequest: Missing label hack.lu/challenge-name"
    if "give-flag" != fr["metadata"]["name"]:
        return False, "Flagrequest: I dont like the request name, it should be 'give-flag'"
    if "spec" not in fr.keys():
        return False, "Flagrequest: Missing spec"
    if "anti-bruteforce" not in fr["spec"].keys():
        return False, "Flagrequest: 'anti-bruteforce' is missing in the spec"
    if "Bi$wmX4PBTQLGe%AIKPO19$ussap4w" != fr["spec"]["anti-bruteforce"]:
        return False, "Flagrequest: Anti-bruteforce token invalid!"
    return True, "Good Job!"
```

### 3. Flagrequest YAML
```yaml
apiVersion: ctf.fluxfingers.hack.lu/v1
kind: Flagrequest
metadata:
  name: give-flag
  namespace: default
  labels:
    hack.lu/challenge-name: give-flag
spec:
  anti-bruteforce: "Bi$wmX4PBTQLGe%AIKPO19$ussap4w"
```

### 4. Operator 监听
```python
stream = watch.Watch().stream(crds.list_namespaced_custom_object, group, version, "default", flagrequest_plural)
for event in stream:
    t = event["type"]
    if t == "ADDED":
        accepted, error = check_flagrequest(...)
        if accepted:
            crds.create_namespaced_custom_object(...)  # 创建 Flag CRD
```

## 评分
- quality: high（K8s CRD + operator watch + anti-bruteforce token 完整流程）
