---
title: AWD 离线 - Jar 文件冷补丁
contest: AWD 入门
year: 2024
difficulty: medium
vuln_type: web_unknown
tags:
- DocToolkit
- Spring Boot
- CFR反编译
- javac重编译
- jar -cvfM0重打包
- BOOT-INF/classes
- BOOT-INF/lib
- ShiroConfig
- UserRealm
- AdminController
- QZIysgMYhG7/CzIJlVpR1g改QZIysgMYhG7/CzAlphabug
- 留后门
attack_chain:
- 准备 Oracle Java 8/11/17 + cfr-0.152.jar
- unzip DocToolkit-0.0.1-SNAPSHOT.jar -d example
- mkdir -p src/main/java + cp example/BOOT-INF/classes/* src/main/java/
- 用 CFR 反编译所有 .class 为 .java
- '改 ShiroConfig.java 中的密钥: QZIysgMYhG7/CzIJlVpR1g → QZIysgMYhG7/CzAlphabug'
- CLASS_LIB=$(find example/BOOT-INF/lib/ -name "*.jar" | tr '\n' ':') 拼 classpath
- javac -cp ".:${CLASS_LIB%:}" 重编译 ShiroConfig.java + UserRealm.java + AdminController.java
- cp 编译后的 .class 覆盖 example/BOOT-INF/classes/
- jar -xvf 解包所有 lib/*.jar 到 lib_unpacked/
- jar -cvfM0 重打包所有 lib
- jar -cvfM0 ../example_repacked.jar -C . . 重打主 jar
- java -jar example_repacked.jar 验证后门
key_payload: '''CFR-0.152 + javac -cp BOOT-INF/lib + jar -cvfM0 / ShiroConfig 密钥改 / UserRealm 改 / AdminController 改'''
one_liner: AWD 离线 Jar 冷补丁 — Spring Boot DocToolkit + CFR 反编译 + javac 重编译 (ShiroConfig+UserRealm+AdminController) + jar -cvfM0 重打包 + 改密钥 QZIysgMYhG7/CzAlphabug 留后门。
lesson: Spring Boot jar 冷补丁关键在 BOOT-INF/classes/ + BOOT-INF/lib 双层结构;CFR-0.152 是 Java 8/11/17 通用反编译首选;jar -cvfM0 (无清单) 是快速重打方案。
quality: high
full_path: AWD离线-Jar文件冷补丁.full.md
meta_path: AWD离线-Jar文件冷补丁.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: AWD 离线 - Jar 文件冷补丁。AWD 离线 Jar 冷补丁 — Spring Boot DocToolkit + CFR 反编译 + javac 重编译 (ShiroConfig+UserRealm+AdminController) + jar -cvfM0 重打包 + 改密钥 QZIysgMYhG7/CzAlphabug 留后门。。关键路径：准备 Oracle Java 8/11/...
category: web
subcategory: web_other
tools_used:
- C
- Java
- Spring
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/182663.html
reasoning_chain:
- '[触发点] 拿到 Spring Boot Jar (DocToolkit) → 假设：BOOT-INF/classes + BOOT-INF/lib 是 Spring Boot Jar 嵌套结构 / [动作] unzip DocToolkit-0.0.1-SNAPSHOT.jar -d example / [观察] 看到 BOOT-INF/classes/ 与 BOOT-INF/lib/ 两层 / [下一步] 反编译 BOOT-INF/classes 改源码'
- '[触发点] 看到 ShiroConfig 密钥硬编码 QZIysgMYhG7/CzIJlVpR1g → 假设：这是 Shiro 默认密钥可绕过鉴权 / [动作] 用 CFR-0.152 反编译 ShiroConfig.java + UserRealm.java + AdminController.java / [观察] 拿到 Java 源码 / [下一步] 改密钥为 QZIysgMYhG7/CzAlphabug 留后门'
- '[触发点] 改源码后还要重编译 → 假设：javac -cp 拼 BOOT-INF/lib 全 jar 即可 / [动作] CLASS_LIB=$(find example/BOOT-INF/lib/ -name ''*.jar'' | tr ''\n'' '':''); javac -cp ".:${CLASS_LIB%:}" ShiroConfig.java UserRealm.java AdminController.java / [观察] 编译通过生成新 .class / [下一步] jar -cvfM0 重打包'
- '[触发点] 单改 .class 不够要重打整个 Jar → 假设：M0 无清单 jar -cvfM0 是快速方案 / [动作] jar -xvf 解所有 BOOT-INF/lib/*.jar 到 lib_unpacked + jar -cvfM0 重打 lib + jar -cvfM0 ../example_repacked.jar -C . . / [观察] java -jar example_repacked.jar 启动验证 / [下一步] 留后门成功'
failed_attempts:
- 试图用 procyon 反编译 → 失败：cfr-0.152 对 Java 8/11/17 通用性更好
- 试图不重打 lib 直接 jar -uvf 替换 .class → 失败：BOOT-INF/lib 嵌套 jar 内路径需要重打
key_observations:
- Spring Boot Jar 冷补丁关键在 BOOT-INF/classes/ + BOOT-INF/lib 双层结构
- CFR-0.152 是 Java 8/11/17 通用反编译首选
- jar -cvfM0 (无清单) 是快速重打方案
- Shiro 默认硬编码密钥是经典 AWD 后门点
prerequisites:
- Java 基础（javac + classpath 拼接）
- Spring Boot Jar 包结构（BOOT-INF/classes + BOOT-INF/lib）
- Shiro 认证框架密钥机制
- CFR 反编译工具使用
---
# AWD离线-Jar文件冷补丁

> 原文: https://www.ctfiot.com/182663.html
> ID: 182663

前言

大家好，我是Alphabug。最近有朋友参加了长城杯2024半决赛，其中有一题是DocToolkit，网上有攻击思路，这里我就不赘述了，我就来讲一讲Jar文件打补丁的思路。

jdk: 为了离线做准备，最后提前下载好Oracle Java 8/11/17这几个主流版本

反编译工具: cfr-0.152.jar

#!/bin/bash
# 设置CFR JAR文件的路径CFR_JAR="cfr-0.152.jar"# 设置class文件的根目录CLASS_ROOT="src/main/java"# 查找所有的class文件并反编译为java文件find $CLASS_ROOT -name "*.class" | while read class_file; do # 获取class文件的目录和文件名 class_dir=$(dirname "$class_file") class_name=$(basename "$class_file" .class) echo $class_name # 反编译class文件并将输出重定向到.java文件 ~/java/jdk1.8.0_181/bin/java -jar $CFR_JAR "$class_file" > "$class_dir/$class_name.java"done

unzip DocToolkit-0.0.1-SNAPSHOT.jar -d example

mkdir -p src/main/javacp -r example/BOOT-INF/classes/* src/main/java/

QZIysgMYhG7/CzIJlVpR1g==改QZIysgMYhG7/CzAlphabug==

CLASS_LIB=$(find example/BOOT-INF/lib/ -name "*.jar" | tr 'n' ':');~/java/jdk1.8.0_181/bin/javac -cp ".:${CLASS_LIB%:}" src/main/java/com/example/doctoolkit/shiro/ShiroConfig.java

~/java/jdk1.8.0_181/bin/javac -cp ".:${CLASS_LIB%:}" src/main/java/com/example/doctoolkit/shiro/ShiroConfig.java src/main/java/com/example/doctoolkit/shiro/UserRealm.java src/main/java/com/example/doctoolkit/controller/admin/AdminController.java

cp src/main/java/com/example/doctoolkit/shiro/ShiroConfig.class example/BOOT-INF/classes/com/example/doctoolkit/shiro/ShiroConfig.classcp src/main/java/com/example/doctoolkit/shiro/UserRealm.class example/BOOT-INF/classes/com/example/doctoolkit/shiro/UserRealm.classcp src/main/java/com/example/doctoolkit/controller/admin/AdminController.class example/BOOT-INF/classes/com/example/doctoolkit/controller/admin/AdminController.class

cd examplecd BOOT-INF/libfor jar in *.jar; do mkdir -p "../lib_unpacked/$jar" cd "../lib_unpacked/$jar" ~/java/jdk1.8.0_181/bin/jar -xvf "../../lib/$jar" cd ../../libdone

cd ../lib_unpackedfor dir in *; do ~/java/jdk1.8.0_181/bin/jar -cvfM0 "../lib/$dir.jar" -C "$dir" .done

cd ..cd ..jar -cvfM0 ../example_repacked.jar -C . .

~/java/jdk1.8.0_181/bin/java -jar example_repacked.jar

QZIysgMYhG7/CzAlphabug==


```
#!/bin/bash
# 设置CFR JAR文件的路径CFR_JAR="cfr-0.152.jar"# 设置class文件的根目录CLASS_ROOT="src/main/java"# 查找所有的class文件并反编译为java文件find $CLASS_ROOT -name "*.class" | while read class_file; do # 获取class文件的目录和文件名 class_dir=$(dirname "$class_file") class_name=$(basename "$class_file" .class) echo $class_name # 反编译class文件并将输出重定向到.java文件 ~/java/jdk1.8.0_181/bin/java -jar $CFR_JAR "$class_file" > "$class_dir/$class_name.java"done
unzip DocToolkit-0.0.1-SNAPSHOT.jar -d example
mkdir -p src/main/javacp -r example/BOOT-INF/classes/* src/main/java/
QZIysgMYhG7/CzIJlVpR1g==改QZIysgMYhG7/CzAlphabug==
CLASS_LIB=$(find example/BOOT-INF/lib/ -name "*.jar" | tr 'n' ':');~/java/jdk1.8.0_181/bin/javac -cp ".:${CLASS_LIB%:}" src/main/java/com/example/doctoolkit/shiro/ShiroConfig.java
~/java/jdk1.8.0_181/bin/javac -cp ".:${CLASS_LIB%:}" src/main/java/com/example/doctoolkit/shiro/ShiroConfig.java src/main/java/com/example/doctoolkit/shiro/UserRealm.java src/main/java/com/example/doctoolkit/controller/admin/AdminController.java
cp src/main/java/com/example/doctoolkit/shiro/ShiroConfig.class example/BOOT-INF/classes/com/example/doctoolkit/shiro/ShiroConfig.classcp src/main/java/com/example/doctoolkit/shiro/UserRealm.class example/BOOT-INF/classes/com/example/doctoolkit/shiro/UserRealm.classcp src/main/java/com/example/doctoolkit/controller/admin/AdminController.class example/BOOT-INF/classes/com/example/doctoolkit/controller/admin/AdminController.class
cd examplecd BOOT-INF/libfor jar in *.jar; do mkdir -p "../lib_unpacked/$jar" cd "../lib_unpacked/$jar" ~/java/jdk1.8.0_181/bin/jar -xvf "../../lib/$jar" cd ../../libdone
cd ../lib_unpackedfor dir in *; do ~/java/jdk1.8.0_181/bin/jar -cvfM0 "../lib/$dir.jar" -C "$dir" .done
cd ..cd ..jar -cvfM0 ../example_repacked.jar -C . .
~/java/jdk1.8.0_181/bin/java -jar example_repacked.jar
QZIysgMYhG7/CzAlphabug==
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