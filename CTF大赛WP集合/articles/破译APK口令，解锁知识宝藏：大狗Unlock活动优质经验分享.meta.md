---
title: 破译APK口令，解锁知识宝藏：大狗Unlock活动优质经验分享
contest: 大狗Unlock活动
year: 2024
difficulty: easy
vuln_type: reverse
tags: [APK逆向, jadx反编译, AndroidManifest.xml, Frida hook, 云真机平台, ROT偏移, cyberchef, Check类异或, 静态+动态双解]
attack_chain: jadx反编译APK→AndroidManifest.xml定位MainActivity→静态算法分析（ROT21偏移/异或）→云真机+Frida hook动态取随机数/修改Checker.code.value=512→提交flag
key_payload: "ROT21偏移:chr(ord(char)-21)+26补偿;Dagou{Unlok_HOOK_0x1};Checker.code.value=512;frida Java.use + 复制片段"
one_liner: 大狗Unlock 1-5题全解：APK静态jadx+ROT21/异或+动态Frida hook+云真机
lesson: 大狗云真机平台+Frida hook组合；APK定位用AndroidManifest.xml的LAUNCHER；ROT偏移负数补偿
quality: medium
---

# 破译APK口令，解锁知识宝藏：大狗Unlock活动优质经验分享

**赛事**：大狗Unlock活动（2024，知察社区）

**性质**：APK破解活动，5题全解

**核心工具**：
- jadx（APK反编译）
- 大狗云真机平台
- Frida hook
- cyberchef（赛博厨子）

**题目一：ROT21偏移**
```python
def transform_string():
    original_string = "Yvbjp{Pigjf_CJJF_0s1}"
    transformed_string = []
    for char in original_string:
        if 'a' <= char <= 'z':
            char = chr(ord(char) - 21)
            if char < 'a':
                char = chr(ord(char) + 26)
        elif 'A' <= char <= 'Z':
            char = chr(ord(char) - 21)
            if char < 'A':
                char = chr(ord(char) + 26)
        transformed_string.append(char)
    return ''.join(transformed_string)

transform_string()
# Dagou{Unlok_HOOK_0x1}
```

**动态解法**：
- Frida复制get_random为片段
- 启动APP加载脚本+重启
- 得到随机数 → 计算i*2+4 = i2 → 提交

**题目二：CyberChef直接解密**
- 静态：找到key+密文+加密算法
- cyberchef赛博厨子直接解密
- 动态：Frida修改Checker.code.value=512
- 重启APP点击Click me!得flag

**题目三：异或**
- MainActivity仅做界面
- Check.get_flag函数
- 异或运算 → cyberchef解

**关键技巧**：
- AndroidManifest.xml 定位 `android.intent.category.LAUNCHER` 找启动类
- jadx右键复制Frida片段
- Frida修改Java静态字段：`Checker.code.value=512`
- 大狗云真机+Frida组合

**质量评估**：中（5题解法框架完整）
