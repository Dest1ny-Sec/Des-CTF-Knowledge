---
title: 从TCTF的3rm1学习java动态代理
contest: TCTF/0CTF 3rm1
year: 2022
difficulty: medium
vuln_type: deserialize
tags:
- Java
- 动态代理
- InvocationHandler
- Proxy.newProxyInstance
- 反射
- 字段修改
- 反序列化
- AOP
attack_chain:
- 静态代理 StudentInnovation 包装 Student 实现 SubmitWork() 与 count++
- JDK 动态代理 InvocationHandler.invoke 拦截所有方法
- Proxy.newProxyInstance(classLoader, interfaces, handler) 返回代理对象
- handler.setStudent 反射修改 object 字段切换目标
- '嵌套代理: myProxy(backdoor) 作为 ProxyHandler.object'
- 反射 field.set(handler, proxyInstance) 替换目标为恶意 backdoor
- proxyHello.attack() 实际调用 backdoor.exec("calc")
- 触发动态代理链 invoke → method.invoke(object) → Runtime.exec
key_payload: '''Proxy.newProxyInstance(classLoader, new Class[]{Teacher.class}, backdoorhandler)'''
one_liner: 通过 Java 动态代理 + 反射修改 InvocationHandler.object 字段实现 AOP 链式攻击。
lesson: Java 反序列化链常与动态代理耦合，Proxy.newProxyInstance + InvocationHandler 可实现任何接口的包装；通过反射修改 handler 私有 object 字段可把任意类注入到调用链。
quality: medium
full_path: 从TCTF的3rm1学习java动态代理.full.md
meta_path: 从TCTF的3rm1学习java动态代理.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 从TCTF的3rm1学习java动态代理。通过 Java 动态代理 + 反射修改 InvocationHandler.object 字段实现 AOP 链式攻击。。关键路径：静态代理 StudentInnovation 包装 Student 实现 SubmitWork() 与 count++ → JDK 动态代理 InvocationHandler.invoke 拦截所有方法 → Proxy....
category: web
subcategory: deserialization
tools_used:
- Java
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/62847.html
reasoning_chain:
- StudentInnovation 静态代理包装 Student → 触发点：JDK 动态代理模式
- InvocationHandler.invoke 拦截所有方法 → Proxy.newProxyInstance(classLoader, interfaces, handler)
- handler.setStudent 反射修改 object 字段切换目标 → 触发点：动态替换代理目标
- 嵌套代理 myProxy(backdoor) 作为 ProxyHandler.object → 反射 field.set
- proxyHello.attack() 实际调用 backdoor.exec('calc') → 触发动态代理链
- invoke → method.invoke(object) → Runtime.exec 完成
failed_attempts:
- 试图用 cglib 动态代理 → 失败：JDK Proxy 是接口代理
- 试图直接反射调 Runtime.exec → 失败：需要触发链上下文
- 试图序列化 Proxy 对象 → 失败：Proxy 实现类是动态生成
key_observations:
- Java 反序列化链常与动态代理耦合，Proxy.newProxyInstance + InvocationHandler 可实现任何接口的包装
- 通过反射修改 handler 私有 object 字段可把任意类注入到调用链
- AOP 切面思路：invoke 拦截 → method.invoke 转发 → 反序列化时构造任意 method 调用
prerequisites:
- Java 反射机制（field.set/method.invoke）
- JDK 动态代理原理（Proxy/InvocationHandler）
- Java 反序列化链构造（readObject → invoke）
- JVM 类加载与 classLoader 机制
---
# 从TCTF的3rm1学习java动态代理

> 原文: https://www.ctfiot.com/62847.html
> ID: 62847

推荐阅读：

Edge浏览器-通过XSS获取高权限从而RCE

The End of AFR?

java免杀合集

ATT&CK中的攻与防——T1059

若依(RuoYi)管理系统后台sql注入漏洞分析

跳跳糖持续向广大安全从业者征集高质量技术文章，可以是漏洞分析，事件分析，渗透技巧，安全工具等等。

通过审核且发布将予以500RMB-1000RMB不等的奖励，具体文章要求可以查看“投稿须知”。

阅读更多原创技术文章，戳“阅读全文”


```
public interface Event {
    void SubmitWork();
}
public class Student implements Event{
    String name;

    public Student(String n) {
        this.name = n;
    }

    @Override
    public void SubmitWork() {
        System.out.println(this.name + "提交作业");
    }

}
package test;

public class StudentInnovation implements Event{
    Student student;
    int count = 0; //收到的作业数量

    public StudentInnovation(Student stu){
        // 只代理学生对象
        if(stu.getClass() == Student.class) {
            this.student = (Student)stu;
        }
    }

    public void setStudent(Student student) {
        this.student = student;
    }

    @Override
    public void SubmitWork() {
        this.student.SubmitWork();
        this.count += 1;
        System.out.println("已收作业数量为" + this.count);
    }
}
package test;

public class main {
    public static void main(String[] args) {
        //被代理的学生张三，他的作业提交由代理对象monitor（课代表）完成
        Student s1 = new Student("张三");
        Student s2 = new Student("李四");
        Student s3 = new Student("王五");
        //生成代理对象，并将张三传给代理对象
        StudentInnovation monitor = new StudentInnovation(s1);
        //向课代表提交作业
        monitor.SubmitWork();
        monitor.setStudent(s2);
        monitor.SubmitWork();
        monitor.setStudent(s3);
        monitor.SubmitWork();
    }
}
package test;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;

public class ProxyHandler implements InvocationHandler {
    private Object object;
    int count = 0; //收到的作业数量

    public void setStudent(Student student) {
        this.object = student;
    }
    public ProxyHandler(Object object){
        this.object = object;
    }
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        method.invoke(object, args);
        this.count += 1;
        System.out.println("已收作业数量为" + this.count);
        return null;
    }
}
public class main {
    public static void main(String[] args) {
        //被代理的学生张三，他的作业提交由代理对象monitor（课代表）完成
        Student s1 = new Student("张三");
        InvocationHandler handler = new ProxyHandler(s1);
        Event proxyHello = (Event) Proxy.newProxyInstance(s1.getClass().getClassLoader(), s1.getClass().getInterfaces(), handler);
        proxyHello.SubmitWork();
    }
}
package test;

public interface Teacher {
    Object getObject();
    void attack();
}
package test;

public class A implements Teacher{
    Object object;
    @Override
    public Object getObject() {
        return null;
    }

    @Override
    public void attack() {
        System.out.println("attack");
    }
}
package test;

import java.io.IOException;

public class Backdoor implements Teacher{
    @Override
    public Object getObject() {
        return null;
    }

    @Override
    public void attack()  {
        try {
            Runtime.getRuntime().exec("calc");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;

public class myProxy implements InvocationHandler {
    private Object object;

    public myProxy(Object o){
        this.object = o;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        return this.object;
    }
}
package test;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;

public class ProxyHandler implements InvocationHandler {
    private A object;
    public ProxyHandler(Object object){
        this.object = (A) object;
    }
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        System.out.println("method is " + method.getName());
        method.invoke(this.object.getObject(), args);
        return null;
    }
}
public class main {
    public static void main(String[] args) throws NoSuchFieldException, IllegalAccessException {
        A t = new A();
        Backdoor backdoor = new Backdoor();
        InvocationHandler backdoorhandler = new myProxy(backdoor);
        Teacher proxyInstance = (Teacher) Proxy.newProxyInstance(backdoor.getClass().getClassLoader(), new Class[]{Teacher.class}, backdoorhandler);

        InvocationHandler handler = new ProxyHandler(t);
        Field field = handler.getClass().getDeclaredField("object");
        field.setAccessible(true);
        field.set(handler,proxyInstance);
        Teacher proxyHello = (Teacher) Proxy.newProxyInstance(t.getClass().getClassLoader(), t.getClass().getInterfaces(), handler);
        proxyHello.attack();
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
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]