---
title: SUCTF 2025 Writeup - XMCVE-Polaris
contest: SUCTF
year: 2025
team: XMCVE-Polaris
rank: 4
difficulty: medium
vuln_type: web_unknown
tags: [php-unserialize, cake-php, react-promise, oss-version, ssti, magic-method-chain]
attack_chain:
- SU_OSS: ls 找 oss 旧版本文件
- SU_POP: 入口 /ser?ser=base64 → React\Promise\Internal\RejectedPromise __destruct
- reason 拼接触发 __toString → Cake\Http\Response
- stream = new Cake\ORM\Table 触发 __call('rewind')
- BehaviorRegistry._methodMap = ['rewind' => ['z', 'generate']]
- MockClass.generate() eval(classCode) call_user_func
- system($_GET[1]) 弹 shell
- flag 在 /root/flag.txt，suid find 提权
- SU_photogallery: php -S 内置服务器源码泄露 /unzip.php
- check_extension/chech_base 关键词+base64 双重过滤
- 魔改 zip 注释 + Unicode 文件名绕过
- SU_Checkin: 23 位密码 SePassWordLen23SUCTF + Jasypt PBEWithMD5AndDES
- 3 位爆破字典 (62^3=238328)
- Onchain Magician: Solidity 0.8.28 magic box ecrecover 签名复用
- isOpened 状态重放 + chainId
key_payload: /ser?ser=<base64(serialize($a))>
one_liner: SUCTF 2025 XMCVE-Polaris 第 4，PHP 反序列化新链 + Solidity 签名复用 + 内置服务器源码泄露。
lesson: CakePHP 链子 fix 时只改头/尾，中间常被保留；找链应优先按中间环节搜索。
quality: high
---
# SUCTF 2025 – XMCVE-Polaris 第 4

## SU_OSS
题目给了一个 OSS 桶，ls 后查看历史版本，下载旧版本拿到 flag。

## SU_POP
入口 `/ser?ser=base64`。入口点位于 `vendor/symfony/process/Process.php` 的 `__destruct`，但有 `__wakeup` 限制。改用 `React\Promise\Internal\RejectedPromise::__destruct` 触发拼接 `reason`。

链子全文：
1. `RejectedPromise.__destruct` → `error_log("Unhandled ... $this->reason")`
2. `Cake\Http\Response.__toString` → `stream->rewind(); getContents()`
3. `Cake\ORM\Table.__call('rewind', [])` → BehaviorRegistry.call
4. BehaviorRegistry._methodMap = `['rewind' => ['z', 'generate']]` → MockClass.generate
5. `MockClass.__construct` 设 classCode = `system($_GET[1])` + mockName = `test`
6. `generate()` 中 `eval($this->classCode)` → 系统命令执行
7. flag 在 `/root/flag.txt`：`suid find / -name flag.txt -exec cat {} \;` 提权

## SU_photogallery
`php -S` 内置服务器存在源码泄露，`unzip.php` 完整源码可读。`check_extension` 限制 jpg/jpeg/png/gif；`check_content` 用 25 个关键词正则 + base64 双重黑名单。绕过：文件末尾追加非图片扩展名 + 在注释中藏 payload。

## SU_Checkin
23 位密码前缀 `SePassWordLen23SUCTF`，最后 3 位爆破字典。加密方式 `Jasypt PBEWithMD5AndDES`，解密后即得 flag。

## Onchain Magician
Solidity 0.8.28 `MagicBox`。`getMessageHash` 用 keccak256("I want to open the magic box", msg.sender, address(this), block.chainid)。`ecrecover` 验签 + `alreadyUsedSignatureHash` 防止重放。链上观察 `block.chainid` 固定 + 不存储 nonce → 跨链复用签名（同一 chainId 即可）。
