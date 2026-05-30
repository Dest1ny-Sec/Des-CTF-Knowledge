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
```



```
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
