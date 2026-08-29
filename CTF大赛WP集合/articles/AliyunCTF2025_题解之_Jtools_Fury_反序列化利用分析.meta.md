---
title: AliyunCTF 2025 Jtools Fury 反序列化利用分析
contest: AliyunCTF
year: 2025
difficulty: hard
vuln_type: deserialize
tags: [Apache Fury, hutool, feilong, DisallowedList, MapProxy动态代理, Convert.convertWithCheck, BeanConverter, ObjectUtil.deserialize, ValidateObjectInputStream 黑白名单null, PropertyComparator, TemplatesImpl#getOutputProperties, 二次反序列化]
attack_chain:
  - hutool 构建 Web, fury.deserialize 处理请求参数
  - 类黑名单 checkNotInDisallowedList 在 createSerializer 触发
  - 二次反序列化: ValidateObjectInputStream 重载 resolveClass 但默认黑白名单 null
  - 调用点 ObjectUtil#deserialize 不受黑白名单影响
  - 触发链: PriorityQueue.readObject → PropertyComparator.compare → TemplatesImpl.getOutputProperties
  - 二次链: PropertyComparator → MapProxy.invoke(Proxy) → Convert.convert → BeanConverter.convertInternal → ObjectUtil.deserialize → ValidateObjectInputStream.readObject (黑白名单 null)
  - 走两次反序列化,第二次绕过黑名单
key_payload: 'PriorityQueue + PropertyComparator + MapProxy + Convert + BeanConverter + ObjectUtil.deserialize + ValidateObjectInputStream(黑白名单null) / 二次反序列化绕黑名单'
one_liner: AliyunCTF 2025 Jtools — Apache Fury 二次反序列化绕黑名单：PriorityQueue + PropertyComparator + hutool MapProxy 动态代理 + Convert + BeanConverter + ObjectUtil.deserialize 链触发二次反序列化。
lesson: hutool ObjectUtil.deserialize 默认黑白名单 null;动态代理 MapProxy#invoke 是触发 Convert 转换的入口;PropertyComparator 走 feilong PropertyUtilsBean.getProperty 是 feilong 依赖特色。
quality: high
---

# AliyunCTF 2025 Jtools Fury 反序列化利用分析

## 速读
AliyunCTF 2025 Jtools — Apache Fury + hutool + feilong 反序列化链。

## 黑名单 bypass 思路
```java
// 黑白名单初始化为 null
public static <T> T deserialize(byte[] bytes) {
    return IoUtil.readObj(new ByteArrayInputStream(bytes));
}
```

## 调用链 (二次反序列化)
```
Fury.deserialize
  → PriorityQueue.siftUpUsingComparator
  → PropertyComparator.compare
  → com.feilong.lib.beanutils.PropertyUtilsBean.getProperty
  → TemplatesImpl.getOutputProperties   [RCE]
```

## 调用链 (二次反序列化绕黑名单)
```
PriorityQueue.siftUpUsingComparator
  → PropertyComparator.compare
  → com.feilong.core.bean.PropertyValueObtainer
  → com.feilong.lib.beanutils.PropertyUtilsBean.getProperty
  → $Proxy0.invoke  [MapProxy 动态代理]
  → cn.hutool.core.map.MapProxy.invoke
  → cn.hutool.core.convert.Convert.convert
  → ConverterRegistry.convert
  → AbstractConverter.convert
  → BeanConverter.convertInternal
  → cn.hutool.core.util.ObjectUtil.deserialize  [二次反序列化, 黑白名单 null]
  → ValidateObjectInputStream.readObject
```

## 关键点
- 动态代理方法名不能是 hashCode/toString (避触发 Convert 短路)
- feilong PropertyComparator 走 PropertyUtilsBean 是新入口
- 二次反序列化 (hutool ObjectUtil) 走 IoUtil 走 ValidateObjectInputStream 不走 Fury 黑名单
