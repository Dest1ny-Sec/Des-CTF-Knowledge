# AliyunCTF2025 题解之 Jtools Fury 反序列化利用分析

> 原文: https://www.ctfiot.com/229693.html
> ID: 229693

AliyunCTF 2025 Jtools ：

通过 hutool 构建 Web 服务，对提交的请求参数进行 fury.deserialize 反序列化，同时上下文环境中引入了 com.github.ifeilong 依赖。

Fury序列化过滤机制

Fury Java 序列化指南

https://fury.apache.org/zh-CN/docs/guide/java_object_graph_guide/

Fury 中定义了很多 Serializer 子类，分别用于对不同类型的对象进行序列化，比如 HashMap 对应 AbstractMapSerializer ， PriorityQueue 对应 AbstractCollectionSerializer 等。通过调试发现，序列化时会在 org.apache.fury.resolver.ClassResolver#createSerializer 处通过 DisallowedList#checkNotInDisallowedList 进行黑名单检测：

黑名单来自于 fury/disallowed.txt 文件，包含了常见的一些反序列化 gadget ，因此解题思路主要是尝试从 feilong 和 hutool 等第三方依赖中寻找新的 gadget ，或者借助二次反序列化进行 Bypass 。

二次反序列化

其中 ValidateObjectInputStream 重载了 resolveClass 函数，存在过滤：

但是搜索找到调用点 cn.hutool.core.util.ObjectUtil#deserialize ，其默认初始化的黑白名单为 null ，即通过 ObjectUtil#deserialize 反序列化将不会受到黑白名单影响 ：

继续反向搜索寻找 source 调用点，找到一个动态代理类 MapProxy#invoke 函数可达，并且通过审计发现传递的数据流可控：

因此可以考虑通过动态代理触发 invoke 函数，进而触发二次反序列化。需要注意的是，触发 Convert#convert 的前提条件是代理函数名称不能为 hashCode 、 toString 等：

尝试通过 PriorityQueue 反序列化执行 compare 函数来触发动态代理的 invoke ，调用过程如下：

-> org.apache.fury.Fury#deserialize-> java.util.PriorityQueue#siftUpUsingComparator-> com.feilong.core.util.comparator.PropertyComparator#compare-> cn.hutool.core.map.MapProxy#invoke [Proxy.newProxyInstance]-> cn.hutool.core.convert.Convert#convert-> cn.hutool.core.convert.Convert#convertWithCheck-> cn.hutool.core.convert.ConverterRegistry#convert-> cn.hutool.core.convert.ConverterRegistry#convertSpecial-> cn.hutool.core.convert.AbstractConverter#convert-> cn.hutool.core.convert.impl.BeanConverter#convertInternal-> cn.hutool.core.util.ObjectUtil#deserialize-> cn.hutool.core.util.SerializeUtil#deserialize-> cn.hutool.core.io.IoUtil#readObj-> cn.hutool.core.io.ValidateObjectInputStream#readObject [黑白名单为null]

PropertyComparator gadget

-> java.util.PriorityQueue#readObject-> com.feilong.core.util.comparator.PropertyComparator#compare-> com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl#getOutputProperties

实现RCE

getOutputProperties:506, TemplatesImpl (com.sun.org.apache.xalan.internal.xsltc.trax)invoke0:-1, NativeMethodAccessorImpl (sun.reflect)invoke:62, NativeMethodAccessorImpl (sun.reflect)invoke:43, DelegatingMethodAccessorImpl (sun.reflect)invoke:498, Method (java.lang.reflect)invokeMethod:1922, PropertyUtilsBean (com.feilong.lib.beanutils) [2]getSimpleProperty:1095, PropertyUtilsBean (com.feilong.lib.beanutils)getSimpleProperty:1079, PropertyUtilsBean (com.feilong.lib.beanutils)getProperty:825, PropertyUtilsBean (com.feilong.lib.beanutils)getProperty:162, PropertyUtils (com.feilong.lib.beanutils)getDataUseApache:89, PropertyValueObtainer (com.feilong.core.bean)obtain:70, PropertyValueObtainer (com.feilong.core.bean)getProperty:577, PropertyUtil (com.feilong.core.bean)compare:430, PropertyComparator (com.feilong.core.util.comparator)siftDownUsingComparator:721, PriorityQueue (java.util)siftDown:687, PriorityQueue (java.util)heapify:736, PriorityQueue (java.util)readObject:796, PriorityQueue (java.util)invoke0:-1, NativeMethodAccessorImpl (sun.reflect)invoke:62, NativeMethodAccessorImpl (sun.reflect)invoke:43, DelegatingMethodAccessorImpl (sun.reflect)invoke:498, Method (java.lang.reflect)invokeReadObject:1185, ObjectStreamClass (java.io)readSerialData:2345, ObjectInputStream (java.io)readOrdinaryObject:2236, ObjectInputStream (java.io)readObject0:1692, ObjectInputStream (java.io)readObject:508, ObjectInputStream (java.io)readObject:466, ObjectInputStream (java.io)readObj:615, IoUtil (cn.hutool.core.io)readObj:582, IoUtil (cn.hutool.core.io)readObj:563, IoUtil (cn.hutool.core.io)deserialize:65, SerializeUtil (cn.hutool.core.util)deserialize:594, ObjectUtil (cn.hutool.core.util)convertInternal:81, BeanConverter (cn.hutool.core.convert.impl)convert:58, AbstractConverter (cn.hutool.core.convert)convert:288, ConverterRegistry (cn.hutool.core.convert)convert:307, ConverterRegistry (cn.hutool.core.convert)convertWithCheck:765, Convert (cn.hutool.core.convert)convert:718, Convert (cn.hutool.core.convert)convert:689, Convert (cn.hutool.core.convert)invoke:147, MapProxy (cn.hutool.core.map)getDigester:-1, $Proxy0 (com.sun.proxy)invoke0:-1, NativeMethodAccessorImpl (sun.reflect)invoke:62, NativeMethodAccessorImpl (sun.reflect)invoke:43, DelegatingMethodAccessorImpl (sun.reflect)invoke:498, Method (java.lang.reflect)invokeMethod:1922, PropertyUtilsBean (com.feilong.lib.beanutils) [1]getSimpleProperty:1095, PropertyUtilsBean (com.feilong.lib.beanutils)getSimpleProperty:1079, PropertyUtilsBean (com.feilong.lib.beanutils)getProperty:825, PropertyUtilsBean (com.feilong.lib.beanutils)getProperty:162, PropertyUtils (com.feilong.lib.beanutils)getDataUseApache:89, PropertyValueObtainer (com.feilong.core.bean)obtain:70, PropertyValueObtainer (com.feilong.core.bean)getProperty:577, PropertyUtil (com.feilong.core.bean)compare:430, PropertyComparator (com.feilong.core.util.comparator)siftUpUsingComparator:669, PriorityQueue (java.util)siftUp:645, PriorityQueue (java.util)offer:344, PriorityQueue (java.util)add:321, PriorityQueue (java.util)readSameTypeElements:694, AbstractCollectionSerializer (org.apache.fury.serializer.collection)generalJavaRead:672, AbstractCollectionSerializer (org.apache.fury.serializer.collection)readElements:595, AbstractCollectionSerializer (org.apache.fury.serializer.collection)read:73, CollectionSerializer (org.apache.fury.serializer.collection)read:28, CollectionSerializer (org.apache.fury.serializer.collection)readDataInternal:972, Fury (org.apache.fury)readRef:865, Fury (org.apache.fury)deserialize:797, Fury (org.apache.fury)deserialize:718, Fury (org.apache.fury)


```
-> org.apache.fury.Fury#deserialize-> java.util.PriorityQueue#siftUpUsingComparator-> com.feilong.core.util.comparator.PropertyComparator#compare-> cn.hutool.core.map.MapProxy#invoke [Proxy.newProxyInstance]-> cn.hutool.core.convert.Convert#convert-> cn.hutool.core.convert.Convert#convertWithCheck-> cn.hutool.core.convert.ConverterRegistry#convert-> cn.hutool.core.convert.ConverterRegistry#convertSpecial-> cn.hutool.core.convert.AbstractConverter#convert-> cn.hutool.core.convert.impl.BeanConverter#convertInternal-> cn.hutool.core.util.ObjectUtil#deserialize-> cn.hutool.core.util.SerializeUtil#deserialize-> cn.hutool.core.io.IoUtil#readObj-> cn.hutool.core.io.ValidateObjectInputStream#readObject [黑白名单为null]
```



```
-> java.util.PriorityQueue#readObject-> com.feilong.core.util.comparator.PropertyComparator#compare-> com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl#getOutputProperties
```



```
getOutputProperties:506, TemplatesImpl (com.sun.org.apache.xalan.internal.xsltc.trax)invoke0:-1, NativeMethodAccessorImpl (sun.reflect)invoke:62, NativeMethodAccessorImpl (sun.reflect)invoke:43, DelegatingMethodAccessorImpl (sun.reflect)invoke:498, Method (java.lang.reflect)invokeMethod:1922, PropertyUtilsBean (com.feilong.lib.beanutils) [2]getSimpleProperty:1095, PropertyUtilsBean (com.feilong.lib.beanutils)getSimpleProperty:1079, PropertyUtilsBean (com.feilong.lib.beanutils)getProperty:825, PropertyUtilsBean (com.feilong.lib.beanutils)getProperty:162, PropertyUtils (com.feilong.lib.beanutils)getDataUseApache:89, PropertyValueObtainer (com.feilong.core.bean)obtain:70, PropertyValueObtainer (com.feilong.core.bean)getProperty:577, PropertyUtil (com.feilong.core.bean)compare:430, PropertyComparator (com.feilong.core.util.comparator)siftDownUsingComparator:721, PriorityQueue (java.util)siftDown:687, PriorityQueue (java.util)heapify:736, PriorityQueue (java.util)readObject:796, PriorityQueue (java.util)invoke0:-1, NativeMethodAccessorImpl (sun.reflect)invoke:62, NativeMethodAccessorImpl (sun.reflect)invoke:43, DelegatingMethodAccessorImpl (sun.reflect)invoke:498, Method (java.lang.reflect)invokeReadObject:1185, ObjectStreamClass (java.io)readSerialData:2345, ObjectInputStream (java.io)readOrdinaryObject:2236, ObjectInputStream (java.io)readObject0:1692, ObjectInputStream (java.io)readObject:508, ObjectInputStream (java.io)readObject:466, ObjectInputStream (java.io)readObj:615, IoUtil (cn.hutool.core.io)readObj:582, IoUtil (cn.hutool.core.io)readObj:563, IoUtil (cn.hutool.core.io)deserialize:65, SerializeUtil (cn.hutool.core.util)deserialize:594, ObjectUtil (cn.hutool.core.util)convertInternal:81, BeanConverter (cn.hutool.core.convert.impl)convert:58, AbstractConverter (cn.hutool.core.convert)convert:288, ConverterRegistry (cn.hutool.core.convert)convert:307, ConverterRegistry (cn.hutool.core.convert)convertWithCheck:765, Convert (cn.hutool.core.convert)convert:718, Convert (cn.hutool.core.convert)convert:689, Convert (cn.hutool.core.convert)invoke:147, MapProxy (cn.hutool.core.map)getDigester:-1, $Proxy0 (com.sun.proxy)invoke0:-1, NativeMethodAccessorImpl (sun.reflect)invoke:62, NativeMethodAccessorImpl (sun.reflect)invoke:43, DelegatingMethodAccessorImpl (sun.reflect)invoke:498, Method (java.lang.reflect)invokeMethod:1922, PropertyUtilsBean (com.feilong.lib.beanutils) [1]getSimpleProperty:1095, PropertyUtilsBean (com.feilong.lib.beanutils)getSimpleProperty:1079, PropertyUtilsBean (com.feilong.lib.beanutils)getProperty:825, PropertyUtilsBean (com.feilong.lib.beanutils)getProperty:162, PropertyUtils (com.feilong.lib.beanutils)getDataUseApache:89, PropertyValueObtainer (com.feilong.core.bean)obtain:70, PropertyValueObtainer (com.feilong.core.bean)getProperty:577, PropertyUtil (com.feilong.core.bean)compare:430, PropertyComparator (com.feilong.core.util.comparator)siftUpUsingComparator:669, PriorityQueue (java.util)siftUp:645, PriorityQueue (java.util)offer:344, PriorityQueue (java.util)add:321, PriorityQueue (java.util)readSameTypeElements:694, AbstractCollectionSerializer (org.apache.fury.serializer.collection)generalJavaRead:672, AbstractCollectionSerializer (org.apache.fury.serializer.collection)readElements:595, AbstractCollectionSerializer (org.apache.fury.serializer.collection)read:73, CollectionSerializer (org.apache.fury.serializer.collection)read:28, CollectionSerializer (org.apache.fury.serializer.collection)readDataInternal:972, Fury (org.apache.fury)readRef:865, Fury (org.apache.fury)deserialize:797, Fury (org.apache.fury)deserialize:718, Fury (org.apache.fury)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/10-1740963151.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/2-1740963151.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/1-1740963153.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/7-1740963154.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/7-1740963154.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/5-1740963155.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/5-1740963155.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/5-1740963156.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/7-1740963156.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/5-1740963157.png)