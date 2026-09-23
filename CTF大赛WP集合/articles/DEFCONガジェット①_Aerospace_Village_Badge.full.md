---
title: DEFCON ガジェット① Aerospace Village Badge
contest: DEFCON
year: 2023
difficulty: easy
vuln_type: misc_unknown
tags:
- badge
- hardware
- wifi
- base64
- moongoku
- ipv4
- sao
attack_chain:
- 看 Badge 边缘的刻印 MVNtYWxsU3RlcA==
- Base64 解码得 1SmallStep
- 当 Wifi 密码连 WrightStuff AP
- 看另一侧"First moonwalk data as ipv4
- 解 IPv4 数据包
- 莱特兄弟 / James Webb SAO
key_payload: 物理 Base64 刻印 + Wifi 密码
one_liner: DEFCON Aerospace Village Badge 硬件解谜，刻印 Base64 当 Wifi 密码。
lesson: 硬件 Badge 谜题第一步永远看边缘/背面刻印 + 物理连接器。
quality: high
full_path: DEFCONガジェット①_Aerospace_Village_Badge.full.md
meta_path: DEFCONガジェット①_Aerospace_Village_Badge.meta.md
images_removed: true
images_removed_count: 1
schema_version: v3.0.0-P0
summary: DEFCON ガジェット① Aerospace Village Badge。DEFCON Aerospace Village Badge 硬件解谜，刻印 Base64 当 Wifi 密码。。关键路径：看 Badge 边缘的刻印 MVNtYWxsU3RlcA== → Base64 解码得 1SmallStep → 当 Wifi 密码连 WrightStuff AP。经验：硬件 Badge 谜题...
category: misc
subcategory: misc_other
time_required: quick
difficulty_score: 2
code_blocks_count: 0
images_count: 1
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/130703.html
reasoning_chain:
- 在 DEFCON Aerospace Village 买 Badge 'The Wright Stuff'（莱特兄弟）$80 → 触发点：物理 Badge 解谜
- 动作：观察 Badge 边缘有刻印 'MVNtYWxsU3RlcA==' → 假设：Base64（末尾 == 是标准 Base64 特征）
- 动作：echo 'MVNtYWxsU3RlcA==' | base64 -d → 观察：'1SmallStep' → 触发点：解谜线索
- 假设：背面左下角有 Wifi 开关 + 之前解出 '1SmallStep' 是密码 → 动作：连接 SSID='WrightStuff' + 密码='1SmallStep'
- 观察：连接成功 → 假设：另一面 'First moonwalk data as ipv4' → 动作：把人类首次登月日期 1969-07-21 转 IP
- 动作：1969.07.21 → 假设：默认网关 7.21.19.69（对应年份 1969 + 月 7 + 日 21 + 12 月）→ 动作：访问 7.21.19.69
- 假设：Badge 还有 SAO（Simple Add-On）插槽 → JWT（詹姆斯韦伯太空望远镜）SAO → 假设：拼接莱特兄弟 + 詹姆斯韦伯 = 答案
failed_attempts:
- 试图用 Unix epoch time 转换 1969-07-21 → 失败：日期转换复杂，不如直接默认网关 IP
- 试图直接 ping Badge → 失败：Badge 是 AP 模式不是 station
- 试图只看正面不解 Wifi → 失败：必须连接 Wifi 才能拿到后续线索
key_observations:
- 硬件 Badge 谜题第一步永远看边缘/背面刻印 + 物理连接器
- Base64 末尾 == 是标准编码特征，立刻识别尝试解码
- Wifi 密码常藏在 Badge 物理刻印 / 二维码 / LED 闪烁中
- '''As ipv4'' 类提示要把日期或数字转 IP（默认网关 7.21.19.69 是经典 1969-07-21 映射）'
- SAO 插槽 + 历史人物名（莱特兄弟 + 詹姆斯韦伯）= Aerospace 主题答案
prerequisites:
- Linux/Mac base64 命令行（base64 -d / echo）
- Wifi 连接（SSID + WPA2 密码）
- IPv4 地址格式 + 默认网关概念
- 硬件 Badge 物理接口（Wifi/Switch/SAO 插槽）
---
# DEFCONガジェット① Aerospace Village Badge

> 原文: https://www.ctfiot.com/130703.html
> ID: 130703

Aerospace Village 航天村

DEFCONの会場では様々な「Village」があり、テーマに合わせた展示、CTF、ワークショップ、トークなどが行われる

在DEFCON会场，将有各种“村庄”，包括主题展览，CTF，研讨会，讲座等。

参加型のイベントが多いのが特徴である 它的特点是许多参与性活动。

Aerospace Villageでは航空宇宙産業に関連する展示が行われており、そこでバッジを購入した

航空航天村有一个与航空航天工业有关的展览，我在那里买了一个徽章。

ロケットエンジンや宇宙服（っぽいもの）が展示されていた

展出了火箭发动机和宇航服。

Badgeの購入 购买徽章

多くのVillageではバッジが売っており、寄付金を集めている

许多村庄出售徽章并收集捐款。

売り切れることが多く、欲しいものは早めに購入するのがおすすめ（こうして散財がはかどる）

他们经常卖光，所以建议早点买你想要的东西（这样你可以挥霍）。

バッジは様々な仕掛けがあり、謎解きや何らかの機能を持っていることが多い

徽章有各种噱头，经常解谜或具有某种功能

今回購入したバッジはThe Wright Stuffという名前で飛行機を発明したライト兄弟にちなんでいる

我这次买的徽章是以 The Wright Stuff 发明飞机的莱特兄弟的名字命名的。

価格は$80 (12000円） 价格：80美元（12，000日元）

SAO (Simple Add-On)と呼ばれるバッジにアドオンできるものもある

有些可以添加到名为SAO（简单附加组件）的徽章中

自分はJWT(ジェイムズ・ウェッブ宇宙望遠鏡)のSAOを購入した

我买了一个SAO JWT （詹姆斯韦伯太空望远镜）

SAOの装着 穿着 SAO

SAOをバッジ本体に装着するためにはんだ付けが必要だったため、Soldering Villageに向かった

由于需要焊接才能将 SAO 连接到徽章主体，因此我们前往 Soldering Village

大勢の方がガジェットを作ったり、バッジを完成させたりして、熱心にはんだ付けをしている

许多人正在制作小工具，完成徽章，并急切地焊接

この光景はDEFCONでしか見れない 这种奇观只能在DEFCON看到

自分も空席を見つけてバッジを完成させた 我找到了一个空座位并完成了我的徽章

ライト兄弟が衛星にまたがっており、真ん中の金属に触れると衛星のLEDの色が変わる

莱特兄弟跨在卫星上，触摸中间的金属会改变卫星LED的颜色

Badgeの謎解き 解开徽章之谜

以降、ネタバレになるため、自分で謎解きしたい方は読まないでください。

从现在开始，它将是一个剧透，所以如果你想自己解开谜团，请不要阅读它。

BadgeはLEDを光らせるだけではない 徽章不仅使 LED 发光

背面を見ると左下にWifiのスイッチがあり、WifiのAPとして動作するようだ

如果你看背面，左下角有一个开关， Wifi 它似乎可以作为Wifi AP工作

実際にAPを探すと、WrightStuffというSSIDが出てくる

当您实际查找AP时，SSID WrightStuff 显示

ただし、鍵がかかっており、パスワードが必要 但是，它已被锁定并需要密码

バッジの端をよく見ると何かが刻印されている 如果你仔细观察徽章的边缘，你可以看到上面刻着什么东西。

MVNtYWxsU3RlcA==

== が２つあるので、Base64と分かり、デコードをすると1SmallStepとなる

由于有两个 ==，我们知道 Base64 ，当解码时， 1SmallStep 它变成了

これをWifiのパスワードとして利用すると接続できる

您可以使用此密码作为 Wifi 的密码进行连接

また逆側を見ると 如果你再看另一边，

First moonwalk data as ipv4と書かれている  First moonwalk data as ipv4 据记载，

人類が初めて月に降り立ったのは1969年7月21日ということでこれをIPアドレスに変換する必要がある

人类于 1969 年 7 月 21 日首次登陆月球，因此有必要将其转换为 IP 地址。

日付をUnix Epoch Timeで4バイトに変換するのかなと思ったが、デフォルトゲートウェイのIPアドレスが7.21.19.69だったため、その必要はないと悟った

我想知道我是否会在 Unix 纪元时间将日期转换为 4 个字节，但我意识到我不需要它，因为默认网关 7.21.19.69 的 IP 地址是

ブラウザでそのIPアドレスにアクセスするとWebサーバにアクセスできた

当我使用浏览器访问 IP 地址时，我能够访问 Web 服务器。

バッジのコンセプトの説明がある 有关于徽章概念的解释

バッジのLEDを細かく制御するコントロールパネルが表示された

显示了一个控制面板，可以精细控制徽章的 LED。

またSAOを制御することもでき、Car Hacking VillageのSAOに合わせた制御もできるそうである

它也可以控制SAO，似乎可以根据SAO Car Hacking Village 来控制

謎解きはここで終わりではなく、続きがあるようだ 谜题并没有到此结束，似乎还有延续

ちなみにこのWebサーバのCookieにはこんなものがある

顺便说一下，这个网络服务器上有一个cookie这样的东西

『SAOがもっと欲しいなら、@cybertestpilotを見つけて、「The Eagle Has Landed」と伝えよ』と書いてある

“如果你想要更多的SAO，找到@cybertestpilot并告诉他们’鹰已经降落’。

チャレンジがまだまだありそうだけど一旦ここまで。

仍然有很多挑战，但仅此而已。

最後に 最后

同僚はこれを現地でスマホ一台で解いてた 我的同事用本地的一部智能手机解决了这个问题。

WifiのAP + Webサーバが載っているLEDをピカピカさせるバッジでしかないけど、DEFCONに行くとこういうのが楽しい

它只是一个徽章，使 Wifi AP + Web 服务器所在的 LED 闪亮，但当你去 DEFCON 时，这种乐趣

皆様もDEFCON行かれる際はぜひ #badgelife を楽しんでください

请享受 #badgelife，当你去DEFCON时

原文始发于qiita：DEFCONガジェット① Aerospace Village Badge

---
## 附图

[图片已移除]