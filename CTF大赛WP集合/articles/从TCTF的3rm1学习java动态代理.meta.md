---
title: 从TCTF的3rm1学习java动态代理
contest: TCTF/0CTF 3rm1
year: 2022
difficulty: medium
vuln_type: deserialize
tags: [Java, 动态代理, InvocationHandler, Proxy.newProxyInstance, 反射, 字段修改, 反序列化, AOP]
attack_chain:
  - 静态代理 StudentInnovation 包装 Student 实现 SubmitWork() 与 count++
  - JDK 动态代理 InvocationHandler.invoke 拦截所有方法
  - Proxy.newProxyInstance(classLoader, interfaces, handler) 返回代理对象
  - handler.setStudent 反射修改 object 字段切换目标
  - 嵌套代理: myProxy(backdoor) 作为 ProxyHandler.object
  - 反射 field.set(handler, proxyInstance) 替换目标为恶意 backdoor
  - proxyHello.attack() 实际调用 backdoor.exec("calc")
  - 触发动态代理链 invoke → method.invoke(object) → Runtime.exec
key_payload: 'Proxy.newProxyInstance(classLoader, new Class[]{Teacher.class}, backdoorhandler)'
one_liner: 通过 Java 动态代理 + 反射修改 InvocationHandler.object 字段实现 AOP 链式攻击。
lesson: Java 反序列化链常与动态代理耦合，Proxy.newProxyInstance + InvocationHandler 可实现任何接口的包装；通过反射修改 handler 私有 object 字段可把任意类注入到调用链。
quality: medium
---

# 从TCTF的3rm1学习java动态代理

## 概览
- **来源**: ctfiot 62847，跳跳糖安全团队投稿
- **目标**: 学习 Java 动态代理从入门到反序列化利用
- **难度**: ⭐⭐⭐

## 静态代理 → 动态代理
- **静态**: `StudentInnovation implements Event` 包装 Student，构造时检查 `stu.getClass() == Student.class`
- **动态**: `ProxyHandler implements InvocationHandler` + `Proxy.newProxyInstance`
  ```java
  Event proxyHello = (Event) Proxy.newProxyInstance(
      s1.getClass().getClassLoader(),
      s1.getClass().getInterfaces(),
      handler);
  proxyHello.SubmitWork();  // 实际调用 handler.invoke()
  ```

## 3rm1 反序列化核心
```java
public Object invoke(Object proxy, Method method, Object[] args) {
    System.out.println("method is " + method.getName());
    method.invoke(this.object.getObject(), args);  // 触发嵌套调用
    return null;
}
```

## 反射字段修改注入
```java
A t = new A();
Backdoor backdoor = new Backdoor();
InvocationHandler backdoorhandler = new myProxy(backdoor);  // myProxy.invoke 返回 this.object
Teacher proxyInstance = (Teacher) Proxy.newProxyInstance(
    backdoor.getClass().getClassLoader(),
    new Class[]{Teacher.class}, backdoorhandler);

InvocationHandler handler = new ProxyHandler(t);
Field field = handler.getClass().getDeclaredField("object");
field.setAccessible(true);
field.set(handler, proxyInstance);  // 反射替换 object 字段

Teacher proxyHello = (Teacher) Proxy.newProxyInstance(
    t.getClass().getClassLoader(), t.getClass().getInterfaces(), handler);
proxyHello.attack();  // → Backdoor.attack() → Runtime.exec("calc")
```

## 教学意义
- AOP 日志埋点基础
- 反序列化 gadget chain 中 `TemplatesImpl + InvocationHandler` 经典组合
