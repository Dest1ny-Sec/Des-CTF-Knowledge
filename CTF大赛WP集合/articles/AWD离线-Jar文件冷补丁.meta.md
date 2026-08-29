---
title: AWD 离线 - Jar 文件冷补丁
contest: AWD 入门
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [DocToolkit, Spring Boot, CFR反编译, javac重编译, jar -cvfM0重打包, BOOT-INF/classes, BOOT-INF/lib, ShiroConfig, UserRealm, AdminController, QZIysgMYhG7/CzIJlVpR1g改QZIysgMYhG7/CzAlphabug, 留后门]
attack_chain:
  - 准备 Oracle Java 8/11/17 + cfr-0.152.jar
  - unzip DocToolkit-0.0.1-SNAPSHOT.jar -d example
  - mkdir -p src/main/java + cp example/BOOT-INF/classes/* src/main/java/
  - 用 CFR 反编译所有 .class 为 .java
  - 改 ShiroConfig.java 中的密钥: QZIysgMYhG7/CzIJlVpR1g → QZIysgMYhG7/CzAlphabug
  - CLASS_LIB=$(find example/BOOT-INF/lib/ -name "*.jar" | tr '\n' ':') 拼 classpath
  - javac -cp ".:${CLASS_LIB%:}" 重编译 ShiroConfig.java + UserRealm.java + AdminController.java
  - cp 编译后的 .class 覆盖 example/BOOT-INF/classes/
  - jar -xvf 解包所有 lib/*.jar 到 lib_unpacked/
  - jar -cvfM0 重打包所有 lib
  - jar -cvfM0 ../example_repacked.jar -C . . 重打主 jar
  - java -jar example_repacked.jar 验证后门
key_payload: 'CFR-0.152 + javac -cp BOOT-INF/lib + jar -cvfM0 / ShiroConfig 密钥改 / UserRealm 改 / AdminController 改'
one_liner: AWD 离线 Jar 冷补丁 — Spring Boot DocToolkit + CFR 反编译 + javac 重编译 (ShiroConfig+UserRealm+AdminController) + jar -cvfM0 重打包 + 改密钥 QZIysgMYhG7/CzAlphabug 留后门。
lesson: Spring Boot jar 冷补丁关键在 BOOT-INF/classes/ + BOOT-INF/lib 双层结构;CFR-0.152 是 Java 8/11/17 通用反编译首选;jar -cvfM0 (无清单) 是快速重打方案。
quality: high
---

# AWD 离线 - Jar 文件冷补丁

## 速读
长城杯 2024 半决赛 DocToolkit 复盘 — Spring Boot jar 离线打补丁留后门。

## 步骤

### 1. 准备
- Oracle Java 8/11/17
- CFR-0.152.jar (反编译)

### 2. 解 jar
```bash
unzip DocToolkit-0.0.1-SNAPSHOT.jar -d example
mkdir -p src/main/java
cp -r example/BOOT-INF/classes/* src/main/java/
```

### 3. CFR 反编译
```bash
find $CLASS_ROOT -name "*.class" | while read class_file; do
    ~/java/jdk1.8.0_181/bin/java -jar $CFR_JAR "$class_file" > "$class_dir/$class_name.java"
done
```

### 4. 改 Shiro 密钥
- `QZIysgMYhG7/CzIJlVpR1g` → `QZIysgMYhG7/CzAlphabug`

### 5. 重编译
```bash
CLASS_LIB=$(find example/BOOT-INF/lib/ -name "*.jar" | tr '\n' ':')
~/java/jdk1.8.0_181/bin/javac -cp ".:${CLASS_LIB%:}" \
    src/main/java/com/example/doctoolkit/shiro/ShiroConfig.java \
    src/main/java/com/example/doctoolkit/shiro/UserRealm.java \
    src/main/java/com/example/doctoolkit/controller/admin/AdminController.java
```

### 6. 覆盖 class
```bash
cp src/main/java/.../ShiroConfig.class example/BOOT-INF/classes/.../ShiroConfig.class
```

### 7. 重打包
```bash
cd example/BOOT-INF/lib
for jar in *.jar; do
    mkdir -p "../lib_unpacked/$jar"
    cd "../lib_unpacked/$jar"
    ~/java/jdk1.8.0_181/bin/jar -xvf "../../lib/$jar"
    cd ../../lib
done

cd ../lib_unpacked
for dir in *; do
    ~/java/jdk1.8.0_181/bin/jar -cvfM0 "../lib/$dir.jar" -C "$dir" .
done

cd ../..
jar -cvfM0 ../example_repacked.jar -C . .
~/java/jdk1.8.0_181/bin/java -jar example_repacked.jar
```
