---
title: Flare-ON 9th 之第八题BackDoor
contest: Flare-ON 9 (2022)
year: 2022
difficulty: hard
vuln_type: reverse
tags:
- rev
- csharp
- dotnet
- flareon
- dnslib
- dns-tunnel
- arc4
- powershell
- cil-body
attack_chain:
- C#反混淆：dnlib解析方法体
- flareon_wrap_decrypt解包装方法（Nop+Call+flare_71）
- flareon_decrypt解flared方法：RC4(0x12784adf, sec_data)
- DNS隧道协议：dnslib自定义TestResolver
- op=[2,10,8,19,...]操作序列→base32 dns子域
- 解密flag：arc4(hashlib.md5(ps), ...)
- powershell -exec bypass -enc base64命令
key_payload: ps = "powershell -exec bypass -enc " + base64 + "..."
one_liner: Flare-ON 9 第8题BackDoor：C#反混淆+DNS隧道+RC4解密flag
lesson: flareon_wrap_decrypt基于Nop+Call+flare_71模式识别包装方法
quality: high
full_path: Flare-ON_9th_之第八题BackDoor.full.md
meta_path: Flare-ON_9th_之第八题BackDoor.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: Flare-ON 9th 之第八题BackDoor。Flare-ON 9 第8题BackDoor：C#反混淆+DNS隧道+RC4解密flag。关键路径：C#反混淆：dnlib解析方法体 → flareon_wrap_decrypt解包装方法（Nop+Call+flare_71） → flareon_decrypt解flared方法：RC4(0x12784adf, sec_data)。经验：f...
category: reverse
subcategory: reverse
tools_used:
- C
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/84092.html
reasoning_chain:
- 触发点：C# .NET 程序 + dnlib 解析 → 假设：方法体混淆
- 动作：dnlib 加载 Assembly → 假设：找 flareon_wrap_decrypt 模式
- 动作：识别 Nop+Nop+Call+flare_71 序列 → 观察：包装方法模式
- 假设：flareon_wrap_decrypt 解包装方法 → 动作：循环 typeDef.Methods 替换真方法体
- 动作：flareon_decrypt 解 flared 方法：RC4(0x12784adf, sec_data) → 观察：sec_data = GetSectionData(hash_text)
- 假设：flare.flare_71 + rc4 是关键 deobfusc 步骤 → 动作：执行 → 观察：方法体解密
- 动作：dnslib 自定义 TestResolver → 假设：DNS 隧道协议
- 动作：op=[2,10,8,19,...] → 22 个操作 → base32 拼成 dns 子域 → 观察：A 记录 192.0.0.x
- 动作：解析 DNS 序列 → 假设：还原 powershell 脚本 → base64 解码 → arc4(hashlib.md5(ps), data)
- 观察：flag = arc4_decrypt(...) → 完成
failed_attempts:
- 试图直接 ilspy 反编译 → 失败：方法体已混淆
- 试图用 .NET Reflector → 失败：需商业版
- 试图手工还原 IL → 失败：必须批量替换
key_observations:
- dnlib 是 .NET 二进制解析最佳开源库（替代 ilspy/Reflector）
- RC4 加密 key {0x12,0x78,0xAB,0xDF} 固定
- DNS 隧道常被用于 C2 通信（dnslib TestResolver 模拟）
- powershell -exec bypass -enc base64 是常见执行链
- ARC4 = RC4 别名，PyCryptodome 提供 Crypto.Cipher.ARC4
prerequisites:
- .NET / CIL 字节码基础
- dnlib API（MethodDef / OpCodes / Instruction）
- RC4 流密码原理
- DNS 协议 + dnslib 库
---
# Flare-ON 9th 之第八题BackDoor

> 原文: https://www.ctfiot.com/84092.html
> ID: 84092

一

概述

二

C#反混淆

private static void flareon_wrap_decrypt(IList<TypeDef> typeDefs) { foreach (var typeDef in typeDefs) foreach (var methodDef in typeDef.Methods) if (methodDef.Module.Name == Assembly.ManifestModule.ScopeName && methodDef.HasBody && methodDef.Body.Instructions.Count > 2 && methodDef.Body.Instructions[0].OpCode == OpCodes.Nop && methodDef.Body.Instructions[1].OpCode == OpCodes.Nop) { var is_wrap = false; var find_true_call = false; MethodDef true_call_MethodDef = null; var is_get_all_args = false; var args_token = new int[2]; var Instructions = methodDef.Body.Instructions; for (var i = 0; i < Instructions.Count; i++) { if (!find_true_call && Instructions[i].OpCode == OpCodes.Call) { find_true_call = true; true_call_MethodDef = (MethodDef)Instructions[i].Operand; } if (Instructions[i].OpCode == OpCodes.Ldsfld && Instructions[i + 1].OpCode == OpCodes.Ldsfld) { args_token[0] = ((FieldDef)Instructions[i].Operand).MDToken.ToInt32(); args_token[1] = ((FieldDef)Instructions[i + 1].Operand).MDToken.ToInt32(); Console.WriteLine("---------------------"); Console.WriteLine(Instructions[i].Operand.ToString()); Console.WriteLine(Instructions[i + 1].Operand.ToString()); Console.WriteLine("---------------------"); is_get_all_args = true; } if (Instructions[i].OpCode == OpCodes.Call && Instructions[i].Operand.ToString().Contains("flare_71") && is_get_all_args) { is_wrap = true; } } if (is_wrap && find_true_call) { CurrentMethod = methodDef; var fieldInfo0 = Assembly.Modules.FirstOrDefault().ResolveField(args_token[0]); var fieldInfo1 = Assembly.Modules.FirstOrDefault().ResolveField(args_token[1]); var arg0 = (Dictionary)fieldInfo0.GetValue(null); var arg1 = (byte[])fieldInfo1.GetValue(null); Console.WriteLine(methodDef.FullName); var dm = flare.flare_71(Assembly.Modules.FirstOrDefault(), true_call_MethodDef.MDToken.ToInt32(), arg0, arg1); var methodBody = MethodBodyReader.CreateCilBody(AssemblyWriter.moduleDef, arg1, null, true_call_MethodDef.Parameters, 1, true_call_MethodDef.Body.MaxStack, (uint)(arg1.Length), true_call_MethodDef.Body.LocalVarSigTok, GenericParamContext.Create(true_call_MethodDef)); true_call_MethodDef.FreeMethodBody(); true_call_MethodDef.Body = methodBody; Console.WriteLine(true_call_MethodDef.Name); } } }

private static void flareon_decrypt(IList<TypeDef> typeDefs){ foreach (var typeDef in typeDefs) foreach (var methodDef in typeDef.Methods) if (methodDef.Module.Name == Assembly.ManifestModule.ScopeName && methodDef.ToString().Contains("flared")) { Console.WriteLine(methodDef.Name); var token = methodDef.MDToken.ToInt32(); var method = Assembly.Modules.FirstOrDefault()?.ResolveMethod(token); var ILcode = method.GetMethodBody().GetILAsByteArray(); var hash_text = flare.flared_66(Assembly.Modules.FirstOrDefault(), token); byte[] sec_data = GetSectionData(hash_text); byte[] decrypted_IL_code = flare.rc4(new byte[] { 18, 120, 171, 223 }, sec_data); var dm = flare.flared_67(Assembly.Modules.FirstOrDefault(), decrypted_IL_code, token); Console.WriteLine(sec_data.Length); var methodBody = MethodBodyReader.CreateCilBody(AssemblyWriter.moduleDef, decrypted_IL_code, null, methodDef.Parameters, 1, methodDef.Body.MaxStack, (uint)(decrypted_IL_code.Length), methodDef.Body.LocalVarSigTok, GenericParamContext.Create(methodDef)); if(methodDef.Body.HasExceptionHandlers) { Console.WriteLine(methodDef.Name+": " +methodDef.Body.ExceptionHandlers.Count); } methodDef.FreeMethodBody(); methodDef.Body = methodBody; } }

三

DNS隧道协议

from dnslib import *from dnslib.server import *import sysimport time class TestResolver: def __init__(self): self.data=[] op=[2, 10, 8, 19, 11, 1, 15, 13, 22, 16, 5, 12, 21, 3, 18, 17, 20, 14, 9, 7, 4] for i in op: op_str=str(i) payload_len=len(op_str) s=['43'] for k in range(payload_len): s.append(str(ord(op_str[k]))) s=s+(4-len(s))*["0"] pl='.'.join(s) self.data+=(['192.0.0.%d'%(payload_len+1)]+[pl]) self.data=100*self.data print(self.data) self.pos=0 def resolve(self,request,handler): reply = request.reply() qname = request.q.qname qtype = request.q.qtype if "flare-on.com" in str(qname) and QTYPE[qtype]=='A': answer = RR(rname=qname,ttl=60, rdata=A(self.data[self.pos])) self.pos+=1 reply.add_answer(answer) return reply reply.header.rcode = getattr(RCODE,'NXDOMAIN') return reply def main(): resolver = TestResolver() logger = DNSLogger(prefix=False) dns_server = DNSServer(resolver,port=53, address='0.0.0.0', logger=logger) dns_server.start_thread() try: while True: time.sleep(600) sys.stderr.flush() sys.stdout.flush() 
except KeyboardInterrupt: sys.exit(0)if __name__ == '__main__': main()

四

解密flag

import hashlibfrom Crypto.Cipher import ARC4
def to_ps(c): return "powershell -exec bypass -enc "" + c + """op_str=[#74fbaf68(19,"146","JChwaW5nIC1uIDEgMTAuNjUuNDUuMyB8IGZpbmRzdHIgL2kgdHRsKSAtZXEgJG51bGw7JChwaW5nIC1uIDEgMTAuNjUuNC41MiB8IGZpbmRzdHIgL2kgdHRsKSAtZXEgJG51bGw7JChwaW5nIC1uIDEgMTAuNjUuMzEuMTU1IHwgZmluZHN0ciAvaSB0dGwpIC1lcSAkbnVsbDskKHBpbmcgLW4gMSBmbGFyZS1vbi5jb20gfCBmaW5kc3RyIC9pIHR0bCkgLWVxICRudWxs"),(18,"939","JAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4AMQAwAC4AMgAyAC4ANAAyACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwAOwAkACgAcABpAG4AZwAgAC0AbgAgADEAIAAxADAALgAxADAALgAyADMALgAyADAAMAAgAHwAIABmAGkAbgBkAHMAdAByACAALwBpACAAdAB0AGwAKQAgAC0AZQBxACAAJABuAHUAbABsADsAJAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4AMQAwAC4ANAA1AC4AMQA5ACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwAOwAkACgAcABpAG4AZwAgAC0AbgAgADEAIAAxADAALgAxADAALgAxADkALgA1ADAAIAB8ACAAZgBpAG4AZABzAHQAcgAgAC8AaQAgAHQAdABsACkAIAAtAGUAcQAgACQAbgB1AGwAbAA="),(16,"e87","JAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4ANgA1AC4ANQAxAC4AMQAxACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwAOwAkACgAcABpAG4AZwAgAC0AbgAgADEAIAAxADAALgA2ADUALgA2AC4AMQAgAHwAIABmAGkAbgBkAHMAdAByACAALwBpACAAdAB0AGwAKQAgAC0AZQBxACAAJABuAHUAbABsADsAJAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4ANgA1AC4ANQAyAC4AMgAwADAAIAB8ACAAZgBpAG4AZABzAHQAcgAgAC8AaQAgAHQAdABsACkAIAAtAGUAcQAgACQAbgB1AGwAbAA7ACQAKABwAGkAbgBnACAALQBuACAAMQAgADEAMAAuADYANQAuADYALgAzACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwA"),(15,"197","JAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4AMQAwAC4AMQAwAC4ANAAgAHwAIABmAGkAbgBkAHMAdAByACAALwBpACAAdAB0AGwAKQAgAC0AZQBxACAAJABuAHUAbABsADsAJAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4AMQAwAC4ANQAwAC4AMQAwACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwAOwAkACgAcABpAG4AZwAgAC0AbgAgADEAIAAxADAALgAxADAALgAyADIALgA1ADAAIAB8ACAAZgBpAG4AZABzAHQAcgAgAC8AaQAgAHQAdABsACkAIAAtAGUAcQAgACQAbgB1AGwAbAA7ACQAKABwAGkAbgBnACAALQBuACAAMQAgADEAMAAuADEAMAAuADQANQAuADEAOQAgAHwAIABmAGkAbgBkAHMAdAByACAALwBpACAAdAB0AGwAKQAgAC0AZQBxACAAJABuAHUAbABsAA=="),(14,"3a7","JAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4AMQAwAC4AMgAxAC4AMgAwADEAIAB8ACAAZgBpAG4AZABzAHQAcgAgAC8AaQAgAHQAdABsACkAIAAtAGUAcQAgACQAbgB1AGwAbAA7ACQAKABwAGkAbgBnACAALQBuACAAMQAgADEAMAAuADEAMAAuADEAOQAuADIAMAAxACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwAOwAkACgAcABpAG4AZwAgAC0AbgAgADEAIAAxADAALgAxADAALgAxADkALgAyADAAMgAgAHwAIABmAGkAbgBkAHMAdAByACAALwBpACAAdAB0AGwAKQAgAC0AZQBxACAAJABuAHUAbABsADsAJAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4AMQAwAC4AMgA0AC4AMgAwADAAIAB8ACAAZgBpAG4AZABzAHQAcgAgAC8AaQAgAHQAdABsACkAIAAtAGUAcQAgACQAbgB1AGwAbAA="),(10,"f38","hostname"),(17,"2e4","JAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4ANgA1AC4ANAA1AC4AMQA4ACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwAOwAkACgAcABpAG4AZwAgAC0AbgAgADEAIAAxADAALgA2ADUALgAyADgALgA0ADEAIAB8ACAAZgBpAG4AZABzAHQAcgAgAC8AaQAgAHQAdABsACkAIAAtAGUAcQAgACQAbgB1AGwAbAA7ACQAKABwAGkAbgBnACAALQBuACAAMQAgADEAMAAuADYANQAuADMANgAuADEAMwAgAHwAIABmAGkAbgBkAHMAdAByACAALwBpACAAdAB0AGwAKQAgAC0AZQBxACAAJABuAHUAbABsADsAJAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4ANgA1AC4ANQAxAC4AMQAwACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwA"),(13,"e38","bnNsb29rdXAgZmxhcmUtb24uY29tIHwgZmluZHN0ciAvaSBBZGRyZXNzO25zbG9va3VwIHdlYm1haWwuZmxhcmUtb24uY29tIHwgZmluZHN0ciAvaSBBZGRyZXNz"),(12,"570","JAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4ANgA1AC4ANAAuADUAMAAgAHwAIABmAGkAbgBkAHMAdAByACAALwBpACAAdAB0AGwAKQAgAC0AZQBxACAAJABuAHUAbABsADsAJAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4ANgA1AC4ANAAuADUAMQAgAHwAIABmAGkAbgBkAHMAdAByACAALwBpACAAdAB0AGwAKQAgAC0AZQBxACAAJABuAHUAbABsADsAJAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4ANgA1AC4ANgA1AC4ANgA1ACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwAOwAkACgAcABpAG4AZwAgAC0AbgAgADEAIAAxADAALgA2ADUALgA1ADMALgA1ADMAIAB8ACAAZgBpAG4AZABzAHQAcgAgAC8AaQAgAHQAdABsACkAIAAtAGUAcQAgACQAbgB1AGwAbAA7ACQAKABwAGkAbgBnACAALQBuACAAMQAgADEAMAAuADYANQAuADIAMQAuADIAMAAwACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwA"),(11,"818","RwBlAHQALQBOAGUAdABUAEMAUABDAG8AbgBuAGUAYwB0AGkAbwBuACAAfAAgAFcAaABlAHIAZQAtAE8AYgBqAGUAYwB0ACAAewAkAF8ALgBTAHQAYQB0AGUAIAAtAGUAcQAgACIARQBzAHQAYQBiAGwAaQBzAGgAZQBkACIAfQAgAHwAIABTAGUAbABlAGMAdAAtAE8AYgBqAGUAYwB0ACAAIgBMAG8AYwBhAGwAQQBkAGQAcgBlAHMAcwAiACwAIAAiAEwAbwBjAGEAbABQAG8AcgB0ACIALAAgACIAUgBlAG0AbwB0AGUAQQBkAGQAcgBlAHMAcwAiACwAIAAiAFIAZQBtAG8AdABlAFAAbwByAHQAIgA="),(4, "ea5","WwBTAHkAcwB0AGUAbQAuAEUAbgB2AGkAcgBvAG4AbQBlAG4AdABdADoAOgBPAFMAVgBlAHIAcwBpAG8AbgAuAFYAZQByAHMAaQBvAG4AUwB0AHIAaQBuAGcA"),(5, "bfb","net user"),(3, "113","whoami"),(1, "c2e","RwBlAHQALQBOAGUAdABJAFAAQQBkAGQAcgBlAHMAcwAgAC0AQQBkAGQAcgBlAHMAcwBGAGEAbQBpAGwAeQAgAEkAUAB2ADQAIAB8ACAAUwBlAGwAZQBjAHQALQBPAGIAagBlAGMAdAAgAEkAUABBAGQAZAByAGUAcwBzAA=="),(7, "b","RwBlAHQALQBDAGgAaQBsAGQASQB0AGUAbQAgAC0AUABhAHQAaAAgACIAQwA6AFwAUAByAG8AZwByAGEAbQAgAEYAaQBsAGUAcwAiACAAfAAgAFMAZQBsAGUAYwB0AC0ATwBiAGoAZQBjAHQAIABOAGEAbQBlAA=="),(8,"2b7","RwBlAHQALQBDAGgAaQBsAGQASQB0AGUAbQAgAC0AUABhAHQAaAAgACcAQwA6AFwAUAByAG8AZwByAGEAbQAgAEYAaQBsAGUAcwAgACgAeAA4ADYAKQAnACAAfAAgAFMAZQBsAGUAYwB0AC0ATwBiAGoAZQBjAHQAIABOAGEAbQBlAA=="),(9,"9b2","RwBlAHQALQBDAGgAaQBsAGQASQB0AGUAbQAgAC0AUABhAHQAaAAgACcAQwA6ACcAIAB8ACAAUwBlAGwAZQBjAHQALQBPAGIAagBlAGMAdAAgAE4AYQBtAGUA"),(2,"d7d","RwBlAHQALQBOAGUAdABOAGUAaQBnAGgAYgBvAHIAIAAtAEEAZABkAHIAZQBzAHMARgBhAG0AaQBsAHkAIABJAFAAdgA0ACAAfAAgAFMAZQBsAGUAYwB0AC0ATwBiAGoAZQBjAHQAIAAiAEkAUABBAEQARAByAGUAcwBzACIA"),(22,"709","systeminfo | findstr /i "Domain""),(20,"3c9974","RwBlAHQALQBOAGUAdABJAFAAQwBvAG4AZgBpAGcAdQByAGEAdABpAG8AbgAgAHwAIABGAG8AcgBlAGEAYwBoACAASQBQAHYANABEAGUAZgBhAHUAbAB0AEcAYQB0AGUAdwBhAHkAIAB8ACAAUwBlAGwAZQBjAHQALQBPAGIAagBlAGMAdAAgAE4AZQB4AHQASABvAHAA"),(21,"8e6","RwBlAHQALQBEAG4AcwBDAGwAaQBlAG4AdABTAGUAcgB2AGUAcgBBAGQAZAByAGUAcwBzACAALQBBAGQAZAByAGUAcwBzAEYAYQBtAGkAbAB5ACAASQBQAHYANAAgAHwAIABTAGUAbABlAGMAdAAtAE8AYgBqAGUAYwB0ACAAUwBFAFIAVgBFAFIAQQBkAGQAcgBlAHMAcwBlAHMA")]def get_info(key): no_ps=[10,5,3,22] for i in op_str: num=i[0] if num==key: s=i[2] if num not in no_ps: s=to_ps(s) return (num,i[1],s) FLARE15_c = [250,242,240,235,243,249,247,245,238,232,253,244,237,251,234,233,236,246,241,255,252]sh='' stack='System.Object InvokeMethod(System.Object, System.Object[], System.Signature, Boolean)System.Object Invoke(System.Object, System.Reflection.BindingFlags, System.Reflection.Binder, System.Object[], System.Globalization.CultureInfo)'key_str=''d=[]for i in FLARE15_c: op=i^ 248 print(op) d.append(op) info=get_info(op) sh+=info[1] if op!=4: key_str+=(stack+info[2]) print(sh[::-1][0:8])print(d) hx = hashlib.sha256(key_str.encode('utf8')).digest()cipher = ARC4.new(hx)with open('enc_data.bin', 'rb') as fp: enc_data = fp.read()dec_data = cipher.decrypt(enc_data)with open('dec_data.bin', 'wb') as fp: fp.write(dec_data)

看雪ID：wmsuper

https://bbs.pediy.com/user-home-651413.htm

*本文由看雪论坛 wmsuper 原创，转载请注明来自看雪社区

# 往期推荐

1.CVE-2022-21882提权漏洞学习笔记

2.wibu证书 – 初探

3.win10 1909逆向之APIC中断和实验

4.EMET下EAF机制分析以及模拟实现

5.sql注入学习分享

6.V8 Array.prototype.concat函数出现过的issues和他们的POC们

球分享

球点赞

球在看

点击“阅读原文”，了解更多！


```
一
概述
二
C#反混淆
private static void flareon_wrap_decrypt(IList<TypeDef> typeDefs) { foreach (var typeDef in typeDefs) foreach (var methodDef in typeDef.Methods) if (methodDef.Module.Name == Assembly.ManifestModule.ScopeName && methodDef.HasBody && methodDef.Body.Instructions.Count > 2 && methodDef.Body.Instructions[0].OpCode == OpCodes.Nop && methodDef.Body.Instructions[1].OpCode == OpCodes.Nop) { var is_wrap = false; var find_true_call = false; MethodDef true_call_MethodDef = null; var is_get_all_args = false; var args_token = new int[2]; var Instructions = methodDef.Body.Instructions; for (var i = 0; i < Instructions.Count; i++) { if (!find_true_call && Instructions[i].OpCode == OpCodes.Call) { find_true_call = true; true_call_MethodDef = (MethodDef)Instructions[i].Operand; } if (Instructions[i].OpCode == OpCodes.Ldsfld && Instructions[i + 1].OpCode == OpCodes.Ldsfld) { args_token[0] = ((FieldDef)Instructions[i].Operand).MDToken.ToInt32(); args_token[1] = ((FieldDef)Instructions[i + 1].Operand).MDToken.ToInt32(); Console.WriteLine("---------------------"); Console.WriteLine(Instructions[i].Operand.ToString()); Console.WriteLine(Instructions[i + 1].Operand.ToString()); Console.WriteLine("---------------------"); is_get_all_args = true; } if (Instructions[i].OpCode == OpCodes.Call && Instructions[i].Operand.ToString().Contains("flare_71") && is_get_all_args) { is_wrap = true; } } if (is_wrap && find_true_call) { CurrentMethod = methodDef; var fieldInfo0 = Assembly.Modules.FirstOrDefault().ResolveField(args_token[0]); var fieldInfo1 = Assembly.Modules.FirstOrDefault().ResolveField(args_token[1]); var arg0 = (Dictionary)fieldInfo0.GetValue(null); var arg1 = (byte[])fieldInfo1.GetValue(null); Console.WriteLine(methodDef.FullName); var dm = flare.flare_71(Assembly.Modules.FirstOrDefault(), true_call_MethodDef.MDToken.ToInt32(), arg0, arg1); var methodBody = MethodBodyReader.CreateCilBody(AssemblyWriter.moduleDef, arg1, null, true_call_MethodDef.Parameters, 1, true_call_MethodDef.Body.MaxStack, (uint)(arg1.Length), true_call_MethodDef.Body.LocalVarSigTok, GenericParamContext.Create(true_call_MethodDef)); true_call_MethodDef.FreeMethodBody(); true_call_MethodDef.Body = methodBody; Console.WriteLine(true_call_MethodDef.Name); } } }
private static void flareon_decrypt(IList<TypeDef> typeDefs){ foreach (var typeDef in typeDefs) foreach (var methodDef in typeDef.Methods) if (methodDef.Module.Name == Assembly.ManifestModule.ScopeName && methodDef.ToString().Contains("flared")) { Console.WriteLine(methodDef.Name); var token = methodDef.MDToken.ToInt32(); var method = Assembly.Modules.FirstOrDefault()?.ResolveMethod(token); var ILcode = method.GetMethodBody().GetILAsByteArray(); var hash_text = flare.flared_66(Assembly.Modules.FirstOrDefault(), token); byte[] sec_data = GetSectionData(hash_text); byte[] decrypted_IL_code = flare.rc4(new byte[] { 18, 120, 171, 223 }, sec_data); var dm = flare.flared_67(Assembly.Modules.FirstOrDefault(), decrypted_IL_code, token); Console.WriteLine(sec_data.Length); var methodBody = MethodBodyReader.CreateCilBody(AssemblyWriter.moduleDef, decrypted_IL_code, null, methodDef.Parameters, 1, methodDef.Body.MaxStack, (uint)(decrypted_IL_code.Length), methodDef.Body.LocalVarSigTok, GenericParamContext.Create(methodDef)); if(methodDef.Body.HasExceptionHandlers) { Console.WriteLine(methodDef.Name+": " +methodDef.Body.ExceptionHandlers.Count); } methodDef.FreeMethodBody(); methodDef.Body = methodBody; } }
三
DNS隧道协议
from dnslib import *from dnslib.server import *import sysimport time class TestResolver: def __init__(self): self.data=[] op=[2, 10, 8, 19, 11, 1, 15, 13, 22, 16, 5, 12, 21, 3, 18, 17, 20, 14, 9, 7, 4] for i in op: op_str=str(i) payload_len=len(op_str) s=['43'] for k in range(payload_len): s.append(str(ord(op_str[k]))) s=s+(4-len(s))*["0"] pl='.'.join(s) self.data+=(['192.0.0.%d'%(payload_len+1)]+[pl]) self.data=100*self.data print(self.data) self.pos=0 def resolve(self,request,handler): reply = request.reply() qname = request.q.qname qtype = request.q.qtype if "flare-on.com" in str(qname) and QTYPE[qtype]=='A': answer = RR(rname=qname,ttl=60, rdata=A(self.data[self.pos])) self.pos+=1 reply.add_answer(answer) return reply reply.header.rcode = getattr(RCODE,'NXDOMAIN') return reply def main(): resolver = TestResolver() logger = DNSLogger(prefix=False) dns_server = DNSServer(resolver,port=53, address='0.0.0.0', logger=logger) dns_server.start_thread() try: while True: time.sleep(600) sys.stderr.flush() sys.stdout.flush() 
except KeyboardInterrupt: sys.exit(0)if __name__ == '__main__': main()
四
解密flag
import hashlibfrom Crypto.Cipher import ARC4
def to_ps(c): return "powershell -exec bypass -enc "" + c + """op_str=[#74fbaf68(19,"146","JChwaW5nIC1uIDEgMTAuNjUuNDUuMyB8IGZpbmRzdHIgL2kgdHRsKSAtZXEgJG51bGw7JChwaW5nIC1uIDEgMTAuNjUuNC41MiB8IGZpbmRzdHIgL2kgdHRsKSAtZXEgJG51bGw7JChwaW5nIC1uIDEgMTAuNjUuMzEuMTU1IHwgZmluZHN0ciAvaSB0dGwpIC1lcSAkbnVsbDskKHBpbmcgLW4gMSBmbGFyZS1vbi5jb20gfCBmaW5kc3RyIC9pIHR0bCkgLWVxICRudWxs"),(18,"939","JAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4AMQAwAC4AMgAyAC4ANAAyACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwAOwAkACgAcABpAG4AZwAgAC0AbgAgADEAIAAxADAALgAxADAALgAyADMALgAyADAAMAAgAHwAIABmAGkAbgBkAHMAdAByACAALwBpACAAdAB0AGwAKQAgAC0AZQBxACAAJABuAHUAbABsADsAJAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4AMQAwAC4ANAA1AC4AMQA5ACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwAOwAkACgAcABpAG4AZwAgAC0AbgAgADEAIAAxADAALgAxADAALgAxADkALgA1ADAAIAB8ACAAZgBpAG4AZABzAHQAcgAgAC8AaQAgAHQAdABsACkAIAAtAGUAcQAgACQAbgB1AGwAbAA="),(16,"e87","JAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4ANgA1AC4ANQAxAC4AMQAxACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwAOwAkACgAcABpAG4AZwAgAC0AbgAgADEAIAAxADAALgA2ADUALgA2AC4AMQAgAHwAIABmAGkAbgBkAHMAdAByACAALwBpACAAdAB0AGwAKQAgAC0AZQBxACAAJABuAHUAbABsADsAJAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4ANgA1AC4ANQAyAC4AMgAwADAAIAB8ACAAZgBpAG4AZABzAHQAcgAgAC8AaQAgAHQAdABsACkAIAAtAGUAcQAgACQAbgB1AGwAbAA7ACQAKABwAGkAbgBnACAALQBuACAAMQAgADEAMAAuADYANQAuADYALgAzACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwA"),(15,"197","JAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4AMQAwAC4AMQAwAC4ANAAgAHwAIABmAGkAbgBkAHMAdAByACAALwBpACAAdAB0AGwAKQAgAC0AZQBxACAAJABuAHUAbABsADsAJAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4AMQAwAC4ANQAwAC4AMQAwACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwAOwAkACgAcABpAG4AZwAgAC0AbgAgADEAIAAxADAALgAxADAALgAyADIALgA1ADAAIAB8ACAAZgBpAG4AZABzAHQAcgAgAC8AaQAgAHQAdABsACkAIAAtAGUAcQAgACQAbgB1AGwAbAA7ACQAKABwAGkAbgBnACAALQBuACAAMQAgADEAMAAuADEAMAAuADQANQAuADEAOQAgAHwAIABmAGkAbgBkAHMAdAByACAALwBpACAAdAB0AGwAKQAgAC0AZQBxACAAJABuAHUAbABsAA=="),(14,"3a7","JAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4AMQAwAC4AMgAxAC4AMgAwADEAIAB8ACAAZgBpAG4AZABzAHQAcgAgAC8AaQAgAHQAdABsACkAIAAtAGUAcQAgACQAbgB1AGwAbAA7ACQAKABwAGkAbgBnACAALQBuACAAMQAgADEAMAAuADEAMAAuADEAOQAuADIAMAAxACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwAOwAkACgAcABpAG4AZwAgAC0AbgAgADEAIAAxADAALgAxADAALgAxADkALgAyADAAMgAgAHwAIABmAGkAbgBkAHMAdAByACAALwBpACAAdAB0AGwAKQAgAC0AZQBxACAAJABuAHUAbABsADsAJAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4AMQAwAC4AMgA0AC4AMgAwADAAIAB8ACAAZgBpAG4AZABzAHQAcgAgAC8AaQAgAHQAdABsACkAIAAtAGUAcQAgACQAbgB1AGwAbAA="),(10,"f38","hostname"),(17,"2e4","JAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4ANgA1AC4ANAA1AC4AMQA4ACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwAOwAkACgAcABpAG4AZwAgAC0AbgAgADEAIAAxADAALgA2ADUALgAyADgALgA0ADEAIAB8ACAAZgBpAG4AZABzAHQAcgAgAC8AaQAgAHQAdABsACkAIAAtAGUAcQAgACQAbgB1AGwAbAA7ACQAKABwAGkAbgBnACAALQBuACAAMQAgADEAMAAuADYANQAuADMANgAuADEAMwAgAHwAIABmAGkAbgBkAHMAdAByACAALwBpACAAdAB0AGwAKQAgAC0AZQBxACAAJABuAHUAbABsADsAJAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4ANgA1AC4ANQAxAC4AMQAwACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwA"),(13,"e38","bnNsb29rdXAgZmxhcmUtb24uY29tIHwgZmluZHN0ciAvaSBBZGRyZXNzO25zbG9va3VwIHdlYm1haWwuZmxhcmUtb24uY29tIHwgZmluZHN0ciAvaSBBZGRyZXNz"),(12,"570","JAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4ANgA1AC4ANAAuADUAMAAgAHwAIABmAGkAbgBkAHMAdAByACAALwBpACAAdAB0AGwAKQAgAC0AZQBxACAAJABuAHUAbABsADsAJAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4ANgA1AC4ANAAuADUAMQAgAHwAIABmAGkAbgBkAHMAdAByACAALwBpACAAdAB0AGwAKQAgAC0AZQBxACAAJABuAHUAbABsADsAJAAoAHAAaQBuAGcAIAAtAG4AIAAxACAAMQAwAC4ANgA1AC4ANgA1AC4ANgA1ACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwAOwAkACgAcABpAG4AZwAgAC0AbgAgADEAIAAxADAALgA2ADUALgA1ADMALgA1ADMAIAB8ACAAZgBpAG4AZABzAHQAcgAgAC8AaQAgAHQAdABsACkAIAAtAGUAcQAgACQAbgB1AGwAbAA7ACQAKABwAGkAbgBnACAALQBuACAAMQAgADEAMAAuADYANQAuADIAMQAuADIAMAAwACAAfAAgAGYAaQBuAGQAcwB0AHIAIAAvAGkAIAB0AHQAbAApACAALQBlAHEAIAAkAG4AdQBsAGwA"),(11,"818","RwBlAHQALQBOAGUAdABUAEMAUABDAG8AbgBuAGUAYwB0AGkAbwBuACAAfAAgAFcAaABlAHIAZQAtAE8AYgBqAGUAYwB0ACAAewAkAF8ALgBTAHQAYQB0AGUAIAAtAGUAcQAgACIARQBzAHQAYQBiAGwAaQBzAGgAZQBkACIAfQAgAHwAIABTAGUAbABlAGMAdAAtAE8AYgBqAGUAYwB0ACAAIgBMAG8AYwBhAGwAQQBkAGQAcgBlAHMAcwAiACwAIAAiAEwAbwBjAGEAbABQAG8AcgB0ACIALAAgACIAUgBlAG0AbwB0AGUAQQBkAGQAcgBlAHMAcwAiACwAIAAiAFIAZQBtAG8AdABlAFAAbwByAHQAIgA="),(4, "ea5","WwBTAHkAcwB0AGUAbQAuAEUAbgB2AGkAcgBvAG4AbQBlAG4AdABdADoAOgBPAFMAVgBlAHIAcwBpAG8AbgAuAFYAZQByAHMAaQBvAG4AUwB0AHIAaQBuAGcA"),(5, "bfb","net user"),(3, "113","whoami"),(1, "c2e","RwBlAHQALQBOAGUAdABJAFAAQQBkAGQAcgBlAHMAcwAgAC0AQQBkAGQAcgBlAHMAcwBGAGEAbQBpAGwAeQAgAEkAUAB2ADQAIAB8ACAAUwBlAGwAZQBjAHQALQBPAGIAagBlAGMAdAAgAEkAUABBAGQAZAByAGUAcwBzAA=="),(7, "b","RwBlAHQALQBDAGgAaQBsAGQASQB0AGUAbQAgAC0AUABhAHQAaAAgACIAQwA6AFwAUAByAG8AZwByAGEAbQAgAEYAaQBsAGUAcwAiACAAfAAgAFMAZQBsAGUAYwB0AC0ATwBiAGoAZQBjAHQAIABOAGEAbQBlAA=="),(8,"2b7","RwBlAHQALQBDAGgAaQBsAGQASQB0AGUAbQAgAC0AUABhAHQAaAAgACcAQwA6AFwAUAByAG8AZwByAGEAbQAgAEYAaQBsAGUAcwAgACgAeAA4ADYAKQAnACAAfAAgAFMAZQBsAGUAYwB0AC0ATwBiAGoAZQBjAHQAIABOAGEAbQBlAA=="),(9,"9b2","RwBlAHQALQBDAGgAaQBsAGQASQB0AGUAbQAgAC0AUABhAHQAaAAgACcAQwA6ACcAIAB8ACAAUwBlAGwAZQBjAHQALQBPAGIAagBlAGMAdAAgAE4AYQBtAGUA"),(2,"d7d","RwBlAHQALQBOAGUAdABOAGUAaQBnAGgAYgBvAHIAIAAtAEEAZABkAHIAZQBzAHMARgBhAG0AaQBsAHkAIABJAFAAdgA0ACAAfAAgAFMAZQBsAGUAYwB0AC0ATwBiAGoAZQBjAHQAIAAiAEkAUABBAEQARAByAGUAcwBzACIA"),(22,"709","systeminfo | findstr /i "Domain""),(20,"3c9974","RwBlAHQALQBOAGUAdABJAFAAQwBvAG4AZgBpAGcAdQByAGEAdABpAG8AbgAgAHwAIABGAG8AcgBlAGEAYwBoACAASQBQAHYANABEAGUAZgBhAHUAbAB0AEcAYQB0AGUAdwBhAHkAIAB8ACAAUwBlAGwAZQBjAHQALQBPAGIAagBlAGMAdAAgAE4AZQB4AHQASABvAHAA"),(21,"8e6","RwBlAHQALQBEAG4AcwBDAGwAaQBlAG4AdABTAGUAcgB2AGUAcgBBAGQAZAByAGUAcwBzACAALQBBAGQAZAByAGUAcwBzAEYAYQBtAGkAbAB5ACAASQBQAHYANAAgAHwAIABTAGUAbABlAGMAdAAtAE8AYgBqAGUAYwB0ACAAUwBFAFIAVgBFAFIAQQBkAGQAcgBlAHMAcwBlAHMA")]def get_info(key): no_ps=[10,5,3,22] for i in op_str: num=i[0] if num==key: s=i[2] if num not in no_ps: s=to_ps(s) return (num,i[1],s) FLARE15_c = [250,242,240,235,243,249,247,245,238,232,253,244,237,251,234,233,236,246,241,255,252]sh='' stack='System.Object InvokeMethod(System.Object, System.Object[], System.Signature, Boolean)System.Object Invoke(System.Object, System.Reflection.BindingFlags, System.Reflection.Binder, System.Object[], System.Globalization.CultureInfo)'key_str=''d=[]for i in FLARE15_c: op=i^ 248 print(op) d.append(op) info=get_info(op) sh+=info[1] if op!=4: key_str+=(stack+info[2]) print(sh[::-1][0:8])print(d) hx = hashlib.sha256(key_str.encode('utf8')).digest()cipher = ARC4.new(hx)with open('enc_data.bin', 'rb') as fp: enc_data = fp.read()dec_data = cipher.decrypt(enc_data)with open('dec_data.bin', 'wb') as fp: fp.write(dec_data)
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