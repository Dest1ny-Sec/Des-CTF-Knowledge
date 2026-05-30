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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/8-1716251836.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/5-1716251839.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/0-1716251844.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/10-1716251847.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/1-1716251850.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/3-1716251853.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/2-1716251857.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/0-1716251861.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/6-1716251865.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/0-1716251868.png)