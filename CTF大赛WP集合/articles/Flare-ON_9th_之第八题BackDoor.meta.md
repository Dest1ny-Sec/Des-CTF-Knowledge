---
title: Flare-ON 9th 之第八题BackDoor
contest: Flare-ON 9 (2022)
year: 2022
difficulty: hard
vuln_type: reverse
tags: [rev, csharp, dotnet, flareon, dnslib, dns-tunnel, arc4, powershell, cil-body]
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
---

# Flare-ON 9th 之第八题BackDoor

## 题目信息
- 比赛：Flare-ON 9 (2022)
- 题目：BackDoor（第八题）
- 作者：Muhammad Umair (@m_umairx)

## 关键攻击链
### 1. C# 反混淆
```csharp
private static void flareon_wrap_decrypt(IList<TypeDef> typeDefs) {
    foreach (var typeDef in typeDefs)
    foreach (var methodDef in typeDef.Methods)
    if (methodDef.Module.Name == Assembly.ManifestModule.ScopeName 
        && methodDef.HasBody 
        && methodDef.Body.Instructions.Count > 2 
        && methodDef.Body.Instructions[0].OpCode == OpCodes.Nop 
        && methodDef.Body.Instructions[1].OpCode == OpCodes.Nop) {
        // 包装方法识别：Nop+Nop+Call(flare_71)
        var is_wrap = false;
        var find_true_call = false;
        MethodDef true_call_MethodDef = null;
        var is_get_all_args = false;
        var args_token = new int[2];
        var Instructions = methodDef.Body.Instructions;
        for (var i = 0; i < Instructions.Count; i++) {
            if (!find_true_call && Instructions[i].OpCode == OpCodes.Call) {
                find_true_call = true;
                true_call_MethodDef = (MethodDef)Instructions[i].Operand;
            }
            if (Instructions[i].OpCode == OpCodes.Ldsfld && Instructions[i+1].OpCode == OpCodes.Ldsfld) {
                args_token[0] = ((FieldDef)Instructions[i].Operand).MDToken.ToInt32();
                args_token[1] = ((FieldDef)Instructions[i+1].Operand).MDToken.ToInt32();
                is_get_all_args = true;
            }
            if (Instructions[i].OpCode == OpCodes.Call && Instructions[i].Operand.ToString().Contains("flare_71") && is_get_all_args) {
                is_wrap = true;
            }
        }
        if (is_wrap && find_true_call) {
            // 解密包装方法
        }
    }
}
```

### 2. flared 方法解密
```csharp
private static void flareon_decrypt(IList<TypeDef> typeDefs) {
    foreach (var methodDef in typeDef.Methods) {
        if (methodDef.ToString().Contains("flared")) {
            var token = methodDef.MDToken.ToInt32();
            var hash_text = flare.flared_66(Assembly.Modules.FirstOrDefault(), token);
            byte[] sec_data = GetSectionData(hash_text);
            byte[] decrypted_IL_code = flare.rc4(new byte[]{18, 120, 171, 223}, sec_data);
            // 替换方法体
        }
    }
}
```

### 3. DNS 隧道协议
```python
from dnslib import *
class TestResolver:
    def __init__(self):
        self.data = []
        op = [2, 10, 8, 19, 11, 1, 15, 13, 22, 16, 5, 12, 21, 3, 18, 17, 20, 14, 9, 7, 4]
        for i in op:
            op_str = str(i)
            payload_len = len(op_str)
            s = ['43']
            for k in range(payload_len):
                s.append(str(ord(op_str[k])))
            pl = '.'.join(s)
            self.data += (['192.0.0.%d'%(payload_len+1)] + [pl])
        self.data = 100 * self.data
```

### 4. 解密 flag
```python
import hashlib
from Crypto.Cipher import ARC4
def to_ps(c):
    return "powershell -exec bypass -enc \"" + c + "\""
# op_str = [(19, "146", "JChwaW5nIC1uIDEg..."), ...]
```

## 评分
- quality: high（dnlib CIL 反混淆 + DNS 隧道 + RC4 解密 flag 完整）
