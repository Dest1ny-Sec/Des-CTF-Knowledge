---
title: 详解第九届XCTF国际网络攻防联赛总决赛0解PWN题
contest: 第九届 XCTF 国际网络攻防联赛 总决赛
year: 2024
difficulty: hard
vuln_type: pwn_unknown
tags: [C++, stdlib, vtable, type-confusion, vector-realloc, cookie-check, srand-rand, base64-decode, AES-decrypt, rsa-cpp]
attack_chain:
- main用std::random_device+rand()生成salt,init srand+seccomp设置+write salt to file
- All-Pwn-Red-Book App菜单:1.create note 2.list 3.edit 4.show 5.delete 6.exit
- 三种Type对象:Type_A(0x18,vtable+password+val)+Type_B(0x40,vtable+password+note_content[0x30])+Type_C(0x30,vtable+password+content*+len+capacity)
- 存放指针数量过大时重新申请chunk,旧chunk遗留note指针→UAF/double-free
- vtable边界检查:((((vtable - vtable_TypeA) <<58) | ((unsigned__int64)(vtable - vtable_TypeA) >>6)) > 3)→ud1崩溃
- 编辑note设置password需要满足sub_6C8A0:长度=32,所有字符'!'-'~',且至少3类(大写/小写/数字/特殊),且在特定haystack中memmem找不到
- TypeA_edit调rand()%sub_6E750(obj_)作为val,受srand seed影响
- 内容用base64解码后sub_6F930(256字节)做AES解密
- sub_6C5A0生成key,sub_6E0F0存储
- 关键漏洞:vec_push_back_ptr触发realloc时旧chunk被free,vec中ptr仍指向已释放chunk
key_payload: All-Pwn-Red-Book app RCE
one_liner: 第九届XCTF总决赛0解PWN题"All-Pwn-Red-Book App"详解,std::vector push_back realloc导致旧chunk遗留+UAF,vtable边界检查防type confusion,base64+AES+RSA加密链路。
lesson: std::vector push_back触发realloc会遗留旧指针,这是C++ PWN的经典漏洞;vtable boundary check通过差值编码((x<<58)|(x>>6))>3实现;密码学实现用C++的std::string+base64+AES+RSA要注意调用链。
quality: high
---

## 题目列表

1道0解PWN:All-Pwn-Red-Book App

## 关键考点

### 题目结构
- main: std::random_device + srand(rand()%0xFFFFFF0F)生成salt
- write salt to file
- init srand + seccomp
- 菜单循环 6个选项

### 三种Type对象
- Type_A(0x18):vtable + password + val
- Type_B(0x40):vtable + password + note_content[0x30]
- Type_C(0x30):vtable + password + content* + len + capacity

### 关键漏洞
- 存放指针数量过大时,vec_push_back_ptr触发realloc
- 新chunk分配存放指针,旧chunk free但vec中ptr仍指向已释放chunk
- UAF/double-free基础

### vtable边界检查
- `(((vtable - vtable_TypeA) <<58) | ((unsigned__int64)(vtable - vtable_TypeA) >>6)) > 3`
- 编译期类型检查:Type A/B/C对应差值0/1/2,差值3合法;>3触发ud1崩溃
- type confusion必须绕过此检查

### 密码设置
- sub_6C8A0验证:
  - 长度必须=32
  - 所有字符'!'-'~'(ASCII 33-126)
  - 至少3类字符(大写/小写/数字/特殊)
  - 在特定haystack中memmem找不到
- 合法密码写入*(_QWORD *)(a1+8) = sub_6CA10(s)

### 加密链路
- 输入base64 → sub_6CAB0解码 → sub_6F930(256字节)AES解密
- sub_6C5A0生成key
- sub_6E0F0存储
- sub_6BD00设置密码
- sub_6DE60获取内容
- sub_6DEC0写入内容

### 利用思路
- UAF vec元素→修改已释放chunk的vtable指针
- 绕过vtable边界检查((x<<58)|(x>>6))>3
- 调rand()%sub_6E750(obj_)作为val,salt+rand()可控
- AES解密逻辑可逆

## 实战价值
- C++ PWN经典漏洞:std::vector realloc遗留UAF指针
- vtable boundary check是C++二进制常见的type confusion防护
- 密码学实现用C++的std::string+base64+AES是常见组合
- 0解题是CTF最难的一类,需要创新思路
