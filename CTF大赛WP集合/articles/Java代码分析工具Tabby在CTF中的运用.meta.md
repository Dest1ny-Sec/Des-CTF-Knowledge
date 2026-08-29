---
title: Java 代码分析工具 Tabby 在 CTF 中的运用
contest: 工具介绍
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags: [Tabby, Java 静态分析, soot, Neo4j, 反序列化 gadget 查找, Hessian]
attack_chain: |
  1. Tabby 简介: 专门针对 Java 语言的静态分析工具，基于 soot 框架生成代码属性图，使用 Neo4j 存储
  2. 扩展 tabby-path-finder: 污点分析扩展 (https://github.com/wh1t3p1g/tabby-path-finder)
  3. 题目 1: 2022 长城杯 b4bycoffee (rome 反序列化 ban 了 BadAttributeValueExpException/ObjectBean/ToStringBean/TemplatesImpl/Runtime)
     - 黑名单漏了 EqualsBean，HashMap.readObject -> hash -> EqualsBean.hashCode -> beanHashCode -> CoffeeBean.toString
     - tabby 查询:
       match (source: Method {NAME:"readObject",CLASSNAME:"java.util.HashMap"})
       match (sink: Method {NAME:"toString"})
       call tabby.algo.findJavaGadget(source, sinks, 12, false) yield path
       return path limit 1
     - 结果: HashMap#readObject -> putVal -> Object#equals -> XString#equals -> CoffeeBean#toString
  4. 题目 2: 2022 TCTF HessianOnlyJdk (hessian 反序列化仅 JDK 链)
     - hessian 特性: 可反序列化不继承 Serializable 的类; 起始方法可为 equals/hashCode/compareTo; 不能恢复 Iterator/Map/List
     - tabby 查询:
       match (source: Method) where source.NAME in ["equals","hashCode","compareTo"]
       match (sink: Method {IS_SINK:true}) where sink.NAME =~ "invoke" and sink.VUL =~ "CODE" and sink.CLASSNAME =~ "java.lang.reflect.Method"
       call tabby.algo.allSimplePaths(sinks,sources, 15, false) yield path
       return path limit 1
     - 结果: java.util.Hashtable#equals -> Hashtable#get -> ... -> sun.reflect.misc.MethodUtil.invoke (静态 public)
key_payload: |
  # Tabby Java 静态分析 Cypher 查询:
  
  # 1. readObject -> toString gadget 链:
  match (source: Method {NAME:"readObject",CLASSNAME:"java.util.HashMap"})
  match (sink: Method {NAME:"toString"})
  with source, collect(sink) as sinks
  call tabby.algo.findJavaGadget(source, sinks, 12, false) yield path
  where none(n in nodes(path) where n.CLASSNAME in ["javax.management.BadAttributeValueExpException", ...])
  return path limit 1
  
  # 2. hessian equals/hashCode/compareTo -> Method.invoke 链:
  match (source: Method) where source.NAME in ["equals","hashCode","compareTo"]
  with collect(source) as sources
  match (sink: Method {IS_SINK:true}) where sink.NAME =~ "invoke" and sink.VUL =~ "CODE" and sink.CLASSNAME =~ "java.lang.reflect.Method"
  with sources, collect(sink) as sinks
  call tabby.algo.allSimplePaths(sinks, sources, 15, false) yield path
  where none(n in nodes(path) where (n.CLASSNAME =~ "java.util.Iterator" or ...))
  return path limit 1
  
  # 3. 查静态 public 方法作为 sink:
  match (m1: Method) where m1.VUL="CODE" and m1.IS_STATIC=true and m1.IS_PUBLIC=true
  return m1 limit 50
  # 结果含 sun.reflect.misc.MethodUtil.invoke
one_liner: 用 Tabby (soot + Neo4j) 静态分析 Java 代码属性图 + Cypher 查询，自动化找反序列化 gadget 链和 hessian JDK-only 链。
lesson: |
  - Tabby 适合做"长链 gadget 自动发现"，比手工翻 ysoserial 链快
  - tabby.algo.findJavaGadget 是 BFS/DFS 找 source 到 sink 的最短链
  - tabby.algo.allSimplePaths 是所有简单路径 (限制长度)
  - 黑名单分析: query 中 where none(n in nodes(path) where n.CLASSNAME in [...]) 排除黑名单类
  - hessian 反序列化三特性: 不强制 Serializable / 起点三选一 / 不能恢复集合
  - sun.reflect.misc.MethodUtil.invoke 是静态 public 代码执行点 (hessian + JDK only 关键)
quality: high
---

# Java 代码分析工具 Tabby 在 CTF 中的运用

> 来源: ctfiot.com 64572

## 工具简介

**Tabby** 是专门针对 Java 语言的静态代码分析工具：
- 基于 soot 框架生成 Java 代码属性图 (CPG)
- 使用 Neo4j 存储调用关系
- 支持 Cypher 查询语句查询代码调用链

**扩展 tabby-path-finder**：污点分析扩展，链路节点较长时比普通查询更精准。
- https://github.com/wh1t3p1g/tabby-path-finder

## 题目 1: 2022 长城杯 b4bycoffee

反编译 jar 发现反序列化点 + rome 依赖。

**黑名单：**
```java
this.list = new ArrayList<>();
this.list.add(BadAttributeValueExpException.class.getName());
this.list.add(ObjectBean.class.getName());
this.list.add(ToStringBean.class.getName());
this.list.add(TemplatesImpl.class.getName());
this.list.add(Runtime.class.getName());
```

**黑名单漏了 EqualsBean**：HashMap.readObject -> hash -> EqualsBean.hashCode -> beanHashCode -> CoffeeBean.toString

**Tabby 查询：**
```cypher
match (source: Method {NAME:"readObject", CLASSNAME:"java.util.HashMap"})
match (sink: Method {NAME:"toString"})
with source, collect(sink) as sinks
call tabby.algo.findJavaGadget(source, sinks, 12, false) yield path
where none(n in nodes(path) where n.CLASSNAME in [
    "javax.management.BadAttributeValueExpException",
    "com.sun.jmx.snmp.SnmpEngineId",
    "com.sun.xml.internal.ws.api.BindingID",
    "javax.swing.text.html.HTML\$UnknownTag"
])
return path limit 1
```

**结果路径：**
```
java.util.HashMap#readObject
  -> java.util.HashMap#putVal
  -> java.lang.Object#equals
  -> com.sun.org.apache.xpath.internal.objects.XString#equals
  -> com.example.b4bycoffee.model.CoffeeBean#toString
```

## 题目 2: 2022 TCTF HessianOnlyJdk

**Hessian 反序列化三特性：**
1. 可反序列化不继承 Serializable 的类
2. 起始方法可为 equals/hashCode/compareTo
3. 反序列化时不能恢复 Iterator/Map/List 类型的值

**Tabby 查询：**
```cypher
match (source: Method) where source.NAME in ["equals","hashCode","compareTo"]
with collect(source) as sources
match (sink: Method {IS_SINK:true})
where sink.NAME =~ "invoke" and sink.VUL =~ "CODE"
  and sink.CLASSNAME =~ "java.lang.reflect.Method"
with sources, collect(sink) as sinks
call tabby.algo.allSimplePaths(sinks, sources, 15, false) yield path
where none(n in nodes(path) where
    (n.CLASSNAME =~ "java.util.Iterator" or
     n.CLASSNAME =~ "java.util.Enumeration" or
     n.CLASSNAME =~ "java.util.Map" or
     n.CLASSNAME =~ "java.util.List" or
     n.CLASSNAME =~ "jdk.nashorn.internal.ir.UnaryNode" or
     n.CLASSNAME =~ "com.sun.jndi.ldap.ClientId" or
     n.CLASSNAME =~ "org.apache.catalina.webresources.TrackedInputStream"))
return path limit 1
```

**查静态 public 代码执行点：**
```cypher
match (m1: Method)
where m1.VUL="CODE" and m1.IS_STATIC=true and m1.IS_PUBLIC=true
return m1 limit 50
// 结果含: sun.reflect.misc.MethodUtil.invoke
```

**最终链：** java.util.Hashtable#equals -> Hashtable#get -> ... -> sun.reflect.misc.MethodUtil.invoke (静态 public)

## 评价

Tabby 是 Java 反序列化研究的高效工具：把"手工翻 ysoserial 链"变成"Cypher 查询"。亮点是 `findJavaGadget` 和 `allSimplePaths` 两个过程能快速找 source-sink 路径，配合 `where none(...)` 排除黑名单类，是长链 gadget 自动化研究的标杆。

但 Tabby 入门门槛高（需要 Neo4j + Cypher 语法基础），并且只支持 Java，不像 CodeQL 跨语言。
