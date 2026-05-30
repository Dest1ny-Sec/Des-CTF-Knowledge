# 从一道实例题目解析 AI 在 CTF 中的解题过程

> 原文: https://www.ctfiot.com/270682.html
> ID: 270682

明文为 flag 格式（即flag{xxx}），仅包含大小写字母、数字和下划线；

加密过程分两步：第一步为变异凯撒加密，第二步为 Base64 加密；

变异凯撒规则：每个字符的偏移量不同，偏移量由字符在明文中的 “位置序号” 决定（位置从 0 开始，偏移量 = 位置序号 + 3，例如第 0 位字符偏移 3，第 1 位偏移 4，以此类推）；

最终得到的密文：aVRZM0x6QTJNVGt3Y0dGa1pTMXpOVEF3WldKa1pUQmliR2h2Y21sbmFXNWhiQzV1WkdWdWRHbG1hV05s

加密流程逆向：题目先进行 “变异凯撒加密”，再进行 “Base64 加密”，因此解密需先解 Base64，再解变异凯撒（逆向操作原则）；

Base64 解密关键点：Base64 密文通常由字母、数字、+、/组成，题目给出的密文符合该特征，可直接用标准 Base64 解密函数处理；

变异凯撒解密关键点：需明确 “位置序号” 与 “偏移量” 的对应关系 —— 解密时偏移量 = 位置序号 + 3，但方向与加密相反（加密是 “明文 + 偏移量”，解密则是 “密文 – 偏移量”），且需注意字符循环（例如字母Z减 1 得到Y，A减 1 得到Z）。

字符范围判断：明文仅包含大小写字母、数字和下划线，需确保解密后字符在该范围内；

循环偏移处理：例如数字0减 1 得到9，小写字母a减 1 得到z，避免出现非预期字符。

flag 格式中{和}未被正确处理（题目中{和}是否参与偏移？）；

部分字符大小写不符合 flag 常规（例如LaG应为lag）。

在caesar_decode函数中添加对{和}的判断（不参与偏移）；

提示 “flag 通常为小写，可检查偏移量是否存在 ±1 误差”—— 最终发现 “偏移量 = 位置序号 + 2” 更符合结果（题目可能存在表述偏差，AI 通过结果反推修正）。

帮新手理清加密流程，避免因对算法理解不深导致的方向错误；

快速生成可运行的代码，减少手动编写代码的时间（尤其对不熟悉 Python 的参赛者友好）；

当结果出错时，能根据反馈反推问题原因（如偏移量偏差、字符范围遗漏），辅助人工修正。


```
import base64# 题目给出的最终密文cipher_text = "aVRZM0x6QTJNVGt3Y0dGa1pTMXpOVEF3WldKa1pUQmliR2h2Y21sbmFXNWhiQzV1WkdWdWRHbG1hV05s"# Base64解密（注意：CTF中Base64密文可能存在URL安全编码，此处题目未说明，用标准解码）try: # 将密文转为bytes格式，再进行Base64解码 base64_decoded = base64.b64decode(cipher_text).decode('utf-8') print(f"Base64解密后的中间密文：{base64_decoded}")except Exception as e: print(f"Base64解密出错：{e}")
```



```
def caesar_decode(cipher, start_offset=3): """ 变异凯撒解密函数 :param cipher: 变异凯撒加密后的密文（即Base64解密后的结果） :param start_offset: 初始偏移量（题目中第0位偏移3，对应start_offset=3） :return: 解密后的明文 """ plain = "" for i, char in enumerate(cipher): # i为位置序号（从0开始），char为当前字符 # 计算当前字符的偏移量：偏移量=位置序号+3 offset = i + start_offset # 分类型处理字符，确保解密后在指定范围内 if char.islower(): # 小写字母：a-z（ASCII 97-122） # 解密公式：(字符ASCII码 - 偏移量 - 97) % 26 + 97 decoded_ascii = (ord(char) - offset - 97) % 26 + 97 plain += chr(decoded_ascii) elif char.isupper(): # 大写字母：A-Z（ASCII 65-90） decoded_ascii = (ord(char) - offset - 65) % 26 + 65 plain += chr(decoded_ascii) elif char.isdigit(): # 数字：0-9（ASCII 48-57） decoded_ascii = (ord(char) - offset - 48) % 10 + 48 plain += chr(decoded_ascii) elif char == '_': # 下划线（ASCII 95） # 题目未说明下划线是否偏移，根据flag格式习惯，下划线通常不偏移 plain += char else: # 若出现其他字符，可能是解密错误，暂保留原字符并提示 plain += char print(f"警告：出现未预期字符 {char}（位置{i}），需检查偏移规则") return plain# 调用函数解密中间密文（Base64解密后的结果）middle_cipher = "iTZ3LzA2MTKwcGFkZTNnzT AwWZKZTBibGhvcmxnaHVuZGVudGlm"final_plain = caesar_decode(middle_cipher)print(f"最终解密得到的明文（flag）：{final_plain}")
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757942165-wxsync-2025-09-a71f9e88b4cf6e2c49b3875ced29840c.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757942167-wxsync-2025-09-c8fe7d7681b611072999c67689610c43.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757942168-wxsync-2025-09-06a350289b8e2554f04fa0b61806d844.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757942172-wxsync-2025-09-54ba6cbafedfc7c541ab0b7b58c8671d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757942175-wxsync-2025-09-c005d717f8458368d8db9b7ce77bb9e6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757942178-wxsync-2025-09-c192bd3566c83acf6c9b833bbde28b02.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757942182-wxsync-2025-09-54498d1ec2e99634bc9df90fe2f9b91c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757942183-wxsync-2025-09-0935a9dc8ee73d622a697251ca865038.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757942185-wxsync-2025-09-44ef6830a5ef9f7739a54d858de64297.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757942186-wxsync-2025-09-a4f9b17dfffb72fffbcecaeccb511ecc.gif)