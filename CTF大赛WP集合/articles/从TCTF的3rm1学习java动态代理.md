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
```



```
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
```



```
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
```



```
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
```



```
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
```



```
public class main {
    public static void main(String[] args) {
        //被代理的学生张三，他的作业提交由代理对象monitor（课代表）完成
        Student s1 = new Student("张三");
        InvocationHandler handler = new ProxyHandler(s1);
        Event proxyHello = (Event) Proxy.newProxyInstance(s1.getClass().getClassLoader(), s1.getClass().getInterfaces(), handler);
        proxyHello.SubmitWork();
    }
}
```



```
package test;

public interface Teacher {
    Object getObject();
    void attack();
}
```



```
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
```



```
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
```



```
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
```



```
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
```



```
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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/10-1665715767.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/1-1665715767.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/9-1665715768.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/5-1665715768.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/2-1665715769.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/6-1665715772.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/2-1665715773.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/9-1665715773.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/6-1665715774.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/10-1665715776.png)