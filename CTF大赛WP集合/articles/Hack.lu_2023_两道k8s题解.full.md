---
title: Hack.lu 2023 两道k8s题解
contest: Hack.lu 2023
year: 2023
difficulty: hard
vuln_type: web_unknown
tags:
- k8s
- kubernetes
- crd
- operator
- flagrequest
- anti-bruteforce
- watch
attack_chain:
- 题目：两个 K8s 题目涉及 CRD
- Flagrequest CRD + Flagprotector CRD
- 创建 name=give-flag Flagrequest
- 必须含 hack.lu/challenge-name 标签
- spec.anti-bruteforce = "Bi$wmX4PBTQLGe%AIKPO19$ussap4w
- Kubernetes Python operator 监听 watch
- 删除 flagprotector CRD（不删除则被拒）
- 创建合法 Flagrequest
- Operator 创建 Flag CRD 返回 flag
key_payload: metadata.name=give-flag + labels.hack.lu/challenge-name=give-flag + spec.anti-bruteforce=Bi$wmX4PBTQLGe%AIKPO19$ussap4w
one_liner: Hack.lu 2023 K8s：CRD Flagrequest+operator+anti-bruteforce token
lesson: K8s CRD challenge常需理解operator watch流程+反token条件
quality: high
full_path: Hack.lu_2023_两道k8s题解.full.md
meta_path: Hack.lu_2023_两道k8s题解.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: Hack.lu 2023 两道k8s题解。Hack.lu 2023 K8s：CRD Flagrequest+operator+anti-bruteforce token。关键路径：题目：两个 K8s 题目涉及 CRD → Flagrequest CRD + Flagprotector CRD → 创建 name=give-flag Flagrequest。经验：K8s CRD challen...
category: web
subcategory: web_other
tools_used:
- Python
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/138920.html
reasoning_chain:
- 触发点：题目涉及 K8s CRD（Flagrequest / Flagprotector）+ Python operator watch → 假设：必须构造合法 Flagrequest YAML 才能触发 operator 创建 Flag CRD
- 动作：阅读 operator.py 源码 check_flagrequest() → 观察：检查 metadata.name='give-flag' + labels.hack.lu/challenge-name='give-flag' + spec.anti-bruteforce='Bi$wmX4PBTQLGe%AIKPO19$ussap4w'
- 下一步：必须先 delete 所有 Flagprotector CRD → 动作：kubectl delete flagprotectors --all -n default
- 假设：kubectl apply Flagrequest → operator watch ADDED 事件 → 动作：构造完整 YAML 并 apply
- 观察：operator 调用 create_namespaced_custom_object 创建 Flag CRD，spec.flag 来自 os.getenv('FLAG') → 下一步：kubectl get flags 拿 flag
- 观察：spec.anti-bruteforce 是反爆破 token，硬编码在 operator.py，无需爆破
failed_attempts:
- 试图直接 kubectl get flags → 失败：Flag CRD 必须由 operator 创建
- 试图爆破 anti-bruteforce token → 失败：硬编码 'Bi$wmX4PBTQLGe%AIKPO19$ussap4w'，operator 提示 'You dont need to bruteforce'
key_observations:
- K8s CRD 题目核心是 operator.py 审计（Python kubernetes-client + watch.Watch().stream）
- Flagprotector CRD 是反作弊机制，必须先 delete 才能 apply Flagrequest
- anti-bruteforce 字段实际是反 token 提示，不是真的爆破防线
- K8s 题目常见三大 CRD：Flagrequest（题目）/ Flagprotector（防御）/ Flag（输出）
prerequisites:
- K8s CRD + CustomResourceDefinitions 基础
- Python kubernetes-client (config.load_incluster_config + watch.Watch)
- kubectl apply/get/delete YAML 操作
- JSON/YAML 序列化与 metadata.name/labels 校验
---
# Hack.lu 2023 两道k8s题解

> 原文: https://www.ctfiot.com/138920.html
> ID: 138920


```
from kubernetes import client, config, watch
import os
import uuid
import json

def read_flag():
 flag = os.getenv("FLAG")
 return str(flag)

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
 return False, "Flagrequest: Anti-bruteforce token invalid! You dont need to bruteforce! Im hiding something in the cluster, that will help you :D"

 return True, "Good Job!"

def main():
 # Define CRDs
 version = "v1"
 group = "ctf.fluxfingers.hack.lu"

 flagrequest_plural = "flagrequests"

 flagprotector_plural = "flagprotectors"

 flag_kind = "Flag"
 flag_plural = "flags"

 # Load CRDs
 crds = client.CustomObjectsApi()

 while True:
 print("Watching for flagrequests...")
 stream = watch.Watch().stream(crds.list_namespaced_custom_object, group, version, "default", flagrequest_plural)

 for event in stream:
 t = event["type"]
 flagrequest = event["object"]

 # Check if flagrequest was added
 if t == "ADDED":

 # Check if flagrequest is valid
 accepted, error = check_flagrequest(flagrequest, crds, group, version, flagprotector_plural)
 id = uuid.uuid4()
 if accepted:
 print("Flagrequest accepted, creating flag...")
 # Create flag
 crds.create_namespaced_custom_object(group, version, "default", flag_plural, {
 "apiVersion": group + "/" + version,
 "kind": flag_kind,
 "metadata": {
 "name": "flag" + str(id)
 },
 "spec": {
 "flag": read_flag(),
 "error": str(error),
 }
 })
 else:
 print("Flagrequest invalid")
 # Create flag error
 crds.create_namespaced_custom_object(group, version, "default", flag_plural, {
 "apiVersion": group + "/" + version,
 "kind": flag_kind,
 "metadata": {
 "name": "flag" + str(id)
 },
 "spec": {
 "error": str(error),
 }
 })

if __name__ == "__main__":
 print("Starting operator...")
 try:
 config.incluster_config.load_incluster_config()
 
except:
 print("Failed to load incluster config")
 exit(1)
 main()
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
