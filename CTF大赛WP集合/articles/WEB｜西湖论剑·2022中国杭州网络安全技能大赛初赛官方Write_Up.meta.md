---
title: WEB｜西湖论剑 2022 中国杭州网络安全技能大赛初赛官方 Write Up
contest: 西湖论剑 2022 WEB 初赛
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [tomcat_multipart_parse, double_slash_bypass, fastjson1248_toString, spring_hot_swappable_target_source, node_http_split, ejs_prototype_pollution, php_zend_extension_rc4, sudo_chmod, json_object_length_16]
attack_chain: 扭转乾坤:Apache+Tomcat 双层 改 Content-Type: multipart//form-data 绕过 multipart 解析 → easy_api:springmvc 双 // 绕过 loginFilter + CustomObjectInputStream 黑名单+HotSwappableTargetSource→XString→toString→TemplatesImpl 反序列化 → Node Magical Login:checkcode={"length":16} 触发 try-catch 报错跳出长度检查 → real_easy_node:Node 8.1.2 http 拆分 → curl SSRF 到 127.0.0.1:3000 /copy 路由 → constructor.prototype.outputFunctionName ejs 模板污染 RCE → unusual php:php.ini 加载 zend_test.so RC4 加密上传的 shell + sudo chmod 777 /flag
key_payload: {"checkcode":{"length":16}} / {"constructor.prototype.outputFunctionName":"a=1; return global.process.mainModule.constructor._load('child_process').execSync('cat /flag.txt');//"} / rc4 key=abcsdfadfjiweur
one_liner: 2022 西湖论剑 WEB 5 题官方 WP，tomcat 解析绕过 + Spring 反序列化 toString 链 + Node 8.1.2 HTTP 拆分 + EJS 模板污染 + PHP Zend 扩展 RC4 加密上传，五连击。
lesson: 经典 "双 // 绕过 Spring filter" + "Node 8.x HTTP 拆分" + "EJS constructor.prototype 绕 __proto__ 过滤"是 2022 经典三件套。
quality: high
---
