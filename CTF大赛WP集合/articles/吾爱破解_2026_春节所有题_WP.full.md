---
title: 吾爱破解 2026 春节所有题 WP
contest: 吾爱破解 2026 春节解题
year: 2026
difficulty: hard
vuln_type: misc_unknown
tags:
- 吾爱破解
- 春节领红包
- Native verifyAndDecrypt
- WASM genFlag
- SHA-256 0x2026 次
- hook crypto.getRandomValues
- HMAC16
- Frida hook
- ctf_request
- audit_log_id
attack_chain:
- 'Native verifyAndDecrypt: plain[i] = cipher[i] ^ keystream[i] ^ feedback[i]'
- 第一块 feedback 来自 IV, 之后每块 = 当前密文块
- 'Native 函数偏移: startSessionBytes 0x247b0 / checkRhythm 0x24da8 / updateExp 0x24ea4'
- decryptFrames 0x2541c / verifyAndDecrypt 0x257dc / setDebugBypass 0x25c90
- 'Native 验签成功判定: h1.a.S((byte[]) obj) == null'
- WASM genFlag(uid, voice) + checkCode 0x2026 次 SHA-256 比较 currentHash
- '14 字节 key: 00 01 01 01 01 01 01 00 01 00 01 00 05 02'
- '映射表: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!'
- hook crypto.getRandomValues 截 17 字节随机
- 64 字节 flag hex → sub_1400CF090 转换 + sub_1400CF270 长度 0x40
- sub_1400CF910 核心校验 (反调试) + sub_1400D3B20 64 字节最终比较
- Frida hook 0xD3B20 onEnter 截 lastY + 反调试清零
- '复核链路: ctf_request=口令 (非 access_token) + audit_log_id 用被拒访问完整编号'
key_payload: '''verifyAndDecrypt feedback XOR + WASM 0x2026 SHA-256 + Frida hook 0xD3B20 64 字节'''
one_liner: '吾爱破解 2026 春节: Native verifyAndDecrypt 反馈链 + WASM 0x2026 次 SHA-256 + Frida hook 64 字节比较点。'
lesson: Native 验签成功判定要找 h1.a.S((byte[]) obj) == null 这种"成功条件"；WASM crypto.getRandomValues 必 hook 拿 17 字节随机种子；Frida hook 0xD3B20 onEnter 拿 64 字节目标值是 Windows RE 标准姿势。
quality: high
full_path: 吾爱破解_2026_春节所有题_WP.full.md
meta_path: 吾爱破解_2026_春节所有题_WP.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '吾爱破解 2026 春节所有题 WP。吾爱破解 2026 春节: Native verifyAndDecrypt 反馈链 + WASM 0x2026 次 SHA-256 + Frida hook 64 字节比较点。。关键路径：Native verifyAndDecrypt: plain[i] = cipher[i] ^ keystream[i] ^ feedback[i] → 第一块 fee...'
category: misc
subcategory: misc_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/303229.html
reasoning_chain:
- '吾爱破解 2026 春节领红包 WP, Native verifyAndDecrypt 函数 plain[i] = cipher[i] ^ keystream[i] ^ feedback[i] → 触发点: feedback 链式 XOR'
- '假设: 第一块 feedback 来自 IV, 之后每块 = 当前密文块 → 动作: IDA 分析 verifyAndDecrypt (偏移 0x257dc) → 观察: Native 函数 startSessionBytes 0x247b0 / checkRhythm 0x24da8'
- 'Native 验签成功判定: h1.a.S((byte[]) obj) == null → 假设: 找 .a.S 函数签名 → 动作: 跟踪字节码 S 函数'
- 'WASM genFlag(uid, voice) + checkCode 0x2026 次 SHA-256 → 触发点: 0x2026=8230 次 SHA-256 比较 currentHash → 假设: 逆向 WASM 找出 hash 链'
- '观察: 14 字节 key: 00 01 01 01 01 01 01 00 01 00 01 00 05 02 + 映射表 abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!'
- '动作: hook crypto.getRandomValues 截 17 字节随机 → Frida hook 0xD3B20 onEnter 截 lastY 64 字节 + 反调试清零 → 假设: 64 字节比较拿到 lastY 即可倒推 → 完成'
failed_attempts:
- '试图不解密直接调 verifyAndDecrypt → 失败: 缺 keystream'
- '试图纯静态分析 WASM → 失败: 0x2026 次 SHA-256 必须动态跑'
key_observations:
- Native 验签成功判定要找 h1.a.S((byte[]) obj) == null 这种'成功条件'
- WASM crypto.getRandomValues 必 hook 拿 17 字节随机种子
- Frida hook 0xD3B20 onEnter 拿 64 字节目标值是 Windows RE 标准姿势
- ctf_request=口令 (非 access_token) + audit_log_id 用被拒访问完整编号
- 反调试清零要在 hook 同时绕过
prerequisites:
- IDA Pro Native 逆向
- WASM 字节码逆向 (wasm2c / wasm-decompile)
- Frida hook 原理 (Interceptor.attach / onEnter / onLeave)
- SHA-256 算法
---
# 吾爱破解 2026 春节所有题 WP

> 原文: https://www.ctfiot.com/303229.html
> ID: 303229

作者论坛账号：LiuXing0327

plain[i] = cipher[i] ^ keystream[i] ^ feedback[i]

第一块的 feedback 来自文件头里的 IV（sub_140008310读入）

每处理完一块后 feedback = 当前密文块（下一块用）

是关键资源。

输入字符串会进入NativeBridge.verifyAndDecrypt()，其返回字节后续会被h1.a.S(...)解析。

成功判定点是：h1.a.S((byte[]) obj) == null时走“验证成功”。

Java 方法

Native 偏移

startSessionBytes

0x247b0

checkRhythm

0x24da8

updateExp

0x24ea4

decryptFrames

0x2541c

verifyAndDecrypt

0x257dc

setDebugBypass

0x25c90

解包得到目标位图

将输入字符串转位图

比较位图

sub_2dcdc：key 生成

sub_2ddf8：version=2 解包核心

输出改写后的 pack 数据并还原位图读文本

点击“生成验证码”会调用wasm_bindgen.gen(uid, voice)。

生成后会把 currentHash 赋值为 challenge.h。

点击“提交”时执行checkCode(code, currentHash)。

checkCode 逻辑是：code 连续做 0x2026 次 SHA-256，再和 currentHash 比较。

WASM 侧随机输入来自crypto.getRandomValues，长度固定为 17 字节（可 hook 验证）。

映射表：abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!。

14 字节 key：00 01 01 01 01 01 01 00 01 00 01 00 05 02。

sub_1400CF090：把输入 flag 的 hex 文本转字节。

sub_1400CF270：长度校验（必须是 0x40 字节）。

sub_1400CF910：核心校验调度（含反调试）。

sub_1400FD790：目标值生成（混淆太严重）。

sub_1400D3B20：最终 64 字节比较点。

先把输入的长度除以 2（每两位 hex 组成 1 字节）

分支判断 0-9 / a-f / A-F。

组合方式为 (high << 4) | low 写入输出缓冲。

多处反调试。

目标缓冲生成后进入最终比较调用。

比较前明确mov r8d, 40h，随后call sub_1400D3B20

公众号设置“星标”，您不会错过新的消息通知

如开放注册、精华文章和周边活动等公告


```
复制代码隐藏代码_BYTE *__cdeclsub_401620(inta1){ _BYTE *result;// eax *(_DWORD *)a1 =758280311; *(_DWORD *)(a1 +4) =1663511336; *(_DWORD *)(a1 +8) =1880974179; *(_DWORD *)(a1 +12) =494170226; *(_DWORD *)(a1 +16) =842146570; *(_DWORD *)(a1 +20) =657202491; *(_DWORD *)(a1 +24) =658185525; *(_BYTE *)(a1 +30) =99; *(_WORD *)(a1 +28) =12323; result = (_BYTE *)a1;// 对前 31 字节逐个 XOR 0x42do *result++ ^=0x42u;while( result != (_BYTE *)(a1 +31) ); *(_BYTE *)(a1 +31) =0;returnresult;}
复制代码隐藏代码importstructdata = [758280311,1663511336,1880974179,494170226,842146570,657202491,658185525]raw =b''.join(struct.pack(' (64- n)) defror64(x, n):
return(x >> n) | ((x << (64- n)) &0xffffffffffffffff) deff(k): x = rol64(k,3) for_inrange(8): x = ((x <<8) &0xffffffffffffffff) | s[(x >>56) &0xff] returnx deff_inv(y): t =int.from_bytes(bytes(inv[b]forbiny.to_bytes(8,"big")),"big") returnror64(t,3) png =b"x89PNGrnx1an"state0 =int.from_bytes(bytes(ct[i] ^ png[i] ^ iv[i]foriinrange(8)),"little") key = f_inv(state0) fb =bytearray(iv) out =bytearray() crc =0xffffffffforoffinrange(0,len(ct),8): c = ct[off:
off +8] st = f(key) key = st ks = st.to_bytes(8,"little") p =bytes(c[i] ^ ks[i] ^ fb[i]foriinrange(8)) fb[:] = c out += p crc = zlib.crc32(p, crc) pad = out[-1] pt =bytes(out[:-pad])if0< pad <=8elsebytes(out) Path("flag.png").write_bytes(pt) m = re.search(rb"flag{[^}]+}", pt) print(m.group().decode())
复制代码隐藏代码sub_2dcdcsub_2ddf8
复制代码隐藏代码importstruct frompathlibimportPath FILE_PATH ="pack.dec.bin"defunpack_1bpp(frame:
bytes, w:
int, h:
int) ->bytes: out =bytearray(w * h) foriinrange(w * h): b = frame[i >>3] out[i] = (b >> (7- (i &7))) &1 returnbytes(out) defrender(bits:
bytes, w:
int, h:
int, on="#", off=" "): foryinrange(h): row = bits[y * w:(y +1) * w] print("".join(onifpelseoffforpinrow)) defmain(): buf = Path(FILE_PATH).read_bytes() ifbuf[:4] !=b"HJM1": raiseValueError(f"not HJM1 file, len={len(buf)}") ver, frames, w, h = struct.unpack("<4I", buf[4:20]) frame_bytes = (w * h +7) //8 need = frames * frame_bytes iflen(buf) < need: raiseValueError(f"file too short, len={len(buf)}, need={need}") payload_off =len(buf) - need frame0 = buf[payload_off:
payload_off + frame_bytes] print(f"HJM1 v{ver}, frames={frames}, w={w}, h={h}, payload_off=0x{payload_off:x}") bits = unpack_1bpp(frame0, w, h) render(bits, w, h) if__name__ =="__main__": main()
复制代码隐藏代码constchallenge = wasm_bindgen.gen(uid, voice)currentHash = challenge.h
复制代码隐藏代码checkCode(code, currentHash)
复制代码隐藏代码(() =>{constkeyBytes =Uint8Array.from([0x00,0x01,0x01,0x01,0x01,0x01,0x01,0x00,0x01,0x00,0x01,0x00,0x05,0x02]);consttable ="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!";letlastRand =null;if(!window.__grv_hooked__) { constorig = crypto.getRandomValues.bind(crypto); crypto.getRandomValues=(arr) =>{ constret =orig(arr); if(arr && arr.length===17) lastRand =newUint8Array(arr); returnret; }; window.__grv_hooked__=true; }functiondecodeFromJ(j) { leta =0, f =1, b =0, h =0, c =0, i =0, l =0; constout = []; while(true) { constt0 = j[f -1]; l = t0; h = (l | (h <<8)); c = b; while(true) { i = (h >> (b = c +2)) &63; out.push(table[i]); a++; c -=6; if(b >5)continue; break; } b = c +8; constcont = f !==37; f += cont ?1:0; if(!cont)break; } if(c !== -8) out.push(table[(l << (-2- c)) &63]); returnout.join(""); }asyncfunctionhmac16(first21) { constkey =awaitcrypto.subtle.importKey("raw", keyBytes, {name:"HMAC",hash:"SHA-256"},false, ["sign"]); constsig =awaitcrypto.subtle.sign("HMAC", key, first21); returnnewUint8Array(sig).slice(0,16); }window.genFlag=async(uid =2355817, voice ="c") => { document.getElementById("uid").value=String(uid); document.getElementById("voice").value= voice; lastRand =null; document.getElementById("checkbox-text").click(); awaitnewPromise(r=>setTimeout(r,1200)); if(!lastRand)thrownewError("No random number captured"); constj =newUint8Array(37); j[0] = lastRand[0] ^ (uid &0xff); j[1] = lastRand[1] ^ ((uid >>>8) &0xff); j[2] = lastRand[2] ^ ((uid >>>16) &0xff); j[3] = lastRand[3] ^ ((uid >>>24) &0xff); j.set(lastRand.slice(0,8),4); j.set(lastRand.slice(8,16),12); j[20] = lastRand[16]; j.set(awaithmac16(j.slice(0,21)),21); constcode =decodeFromJ(j); constflag =`flag{${code}}`; document.getElementById("verifyInput").value= flag; return{ flag, code }; };})();
复制代码隐藏代码awaitgenFlag(uid,"c")
复制代码隐藏代码loc_1400CF0F5:
shl bpl,4or bpl,dlcmp rax,rdijz short loc_1400CF140
复制代码隐藏代码解码后长度必须是 =64字节输入长度必须是 =128个hex字符
复制代码隐藏代码importfrida importglob importtime # 你的 uiduid ="uid"targets = glob.glob( "【2026春节】解题领红包之十 {Windows 高级题} 出题老师：Poner.exe") ifnottargets: raiseSystemExit("target exe not found") target = targets[0] js =r''' const base = Process.enumerateModules()[0].base; function p(off){ return base.add(off); } const f_cd490 = new NativeFunction(p(0xCD490), 'uint64', ['pointer','pointer']); const g_b418 = p(0x2632418); const g_b419 = p(0x2632419); let lastY = ''; function toHex(ptr, n){ const u = new Uint8Array(ptr.readByteArray(n)); let s = ''; for (let i = 0; i < u.length; i++) { let h = u[i].toString(16); if (h.length < 2) h = '0' + h; s += h; } return s;} Interceptor.attach(p(0xD3B20), { onEnter(args){ lastY = toHex(args[1], 64); }}); Interceptor.attach(p(0x0C1B90), { onLeave(ret){ ret.replace(ptr(0)); } }); Interceptor.attach(p(0x09B30), { onLeave(ret){ ret.replace(ptr(0)); } }); rpc.exports = { derive(uid){ g_b418.writeU8(0); g_b419.writeU8(0); lastY = ''; const pUid = Memory.allocUtf16String(uid); const pDummy = Memory.allocUtf16String('00'.repeat(64)); f_cd490(pUid, pDummy); return lastY; }, verify(uid, flag){ g_b418.writeU8(0); g_b419.writeU8(0); const pUid = Memory.allocUtf16String(uid); const pFlag = Memory.allocUtf16String(flag); return f_cd490(pUid, pFlag).toString(); }}; '''pid = frida.spawn([target]) session = frida.attach(pid) script = session.create_script(js) script.load() frida.resume(pid) time.sleep(1) api = script.exports_sync flag = api.derive(uid) ret = api.verify(uid, flag) print("uid =", uid) print("flag =", flag) print("verify_ret =", ret) frida.kill(pid)
复制代码隐藏代码ctf_request填的是口令本身，不是 access_token； audit_log_id 一定要用“被拒访问时返回的完整编号”，别截断别改； 而且只认“同一会话里最近那次拒绝”出来的编号，跨会话或旧编号都不行； 复核这段链路别配太杂，越单一越不容易断； 复核凭据是有时效、且一次性的，失败后要重新触发拒绝再拿新编号； 另外，复核阶段拿到的凭据只是打通流程，最终读密卷还需要后续凭据。
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