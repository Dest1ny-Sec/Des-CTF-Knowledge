---
title: 2026 数字中国创新大赛初赛 wp 之大批量文件处理（docx 身份证号批量提取）
contest: 2026 数字中国创新大赛
year: 2026
difficulty: easy
vuln_type:
- misc_unknown
- web_unknown
tags:
- 数字中国 2026 初赛
- 大批量文件处理
- docx 提取 word/document.xml
- ET.parse iter t 标签
- 身份证号正则 d{17}[dXx]
- 老旧 15 位 + 现代 18 位
- 连续数字 + 分段存储空格短横
- 字体颜色白色隐藏
attack_chain:
- 打开 word 的"显示/隐藏"选项看隐藏文本
- docx = zip → word/document.xml → ET.parse iter t 标签
- 拼接纯文本
- 正则 d{17}[dXx] 18 位身份证
- 老旧 15 位身份证
- 分段存储情况：空格 / 短横
key_payload: ET.parse iter t 标签 + re.finditer d{17}[dXx]
one_liner: 2026 数字中国大批量文件处理：docx 提取纯文本 + 18 位身份证号正则批量提取 + 15 位老版兼容。
lesson: docx 实质是 zip + XML；批量提取 = zipfile + ET.parse + iter + 正则；身份证 18 位正则 d{17}[dXx] 是国内取证/数据安全赛事必考。
quality: medium
full_path: 2026数字中国创新大赛初赛wp之大批量文件处理.full.md
meta_path: 2026数字中国创新大赛初赛wp之大批量文件处理.meta.md
images_removed: true
images_removed_count: 5
schema_version: v3.0.0-P0
summary: 2026 数字中国创新大赛初赛 wp 之大批量文件处理（docx 身份证号批量提取）。2026 数字中国大批量文件处理：docx 提取纯文本 + 18 位身份证号正则批量提取 + 15 位老版兼容。。关键路径：打开 word 的"显示/隐藏"选项看隐藏文本 → docx = zip → word/document.xml → ET.parse iter t 标签 → 拼接纯文本。经验：d...
category: misc
subcategory: misc_other
subcategories:
- misc_other
- web_other
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 5
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/307055.html
reasoning_chain:
- 打开 word 显示/隐藏选项看隐藏文本 → 触发点：白色字体 + 隐藏字符
- docx = zip + word/document.xml → 动作：ET.parse iter t 标签
- 观察：t 标签是段落文本节点 → 假设：身份证号以纯文本形式存
- 假设：拼接纯文本 → 正则 \d{17}[\dXx] 提取 18 位身份证
- 老旧 15 位身份证兼容 → 动作：正则 \d{15}
- 分段存储：空格/短横 → 动作：re.sub 清洗后再次匹配
failed_attempts:
- docx2txt 库 → 失败：不提取隐藏 t 标签
- 直接 grep .docx → 失败：docx 是 zip 压缩二进制
- PyPDF2 → 失败：docx 不是 PDF
key_observations:
- docx 实质是 zip + XML（word/document.xml），可 zipfile + ET.parse
- 批量提取 = zipfile + ET.parse + iter t 标签 + 正则
- 身份证 18 位正则 \d{17}[\dXx] 是国内取证必考
- 老版 15 位身份证兼容（不常用）
- 显示/隐藏选项看隐藏文本 + 字体颜色白色是 docx 取证入口
prerequisites:
- docx = zip + word/document.xml 结构
- xml.etree.ElementTree iter 解析
- re 正则（\d{17}[\dXx]）
- Python zipfile 模块
---
# 2026数字中国创新大赛初赛wp之大批量文件处理

> 原文: https://www.ctfiot.com/307055.html
> ID: 307055

缘起

一全选看看是不是字体颜色白色隐藏

打开word的隐藏选项

importreimportzipfilefrompathlibimportPathfromxml.etreeimportElementTreeasET
# 1defextract_text_from_docx(docx_path): text ="" try: withzipfile.ZipFile(docx_path)asdocx_zip: withdocx_zip.open('word/document.xml')asdocument_xml: tree = ET.parse(document_xml) root = tree.getroot() foreleminroot.iter(): ifelem.tag.endswith('}t'): text += elem.text +' ' exceptExceptionase: print(f"Error processing{docx_path}:{e}") returntext.strip()
# 2deffind_idcards(text:
str) ->list: results = [] pattern_18 =r'b(d{17}[dXx])b' formatchinre.finditer(pattern_18, text): id_num =match.group(1) ifid_numnotinresults: results.append(id_num) returnresultsif__name__ =='__main__': all_results = [] docx_files =list(Path("./docs").rglob('*.docx')) total =len(docx_files) print(f"找到{total}个 Word 文档") idcard = [] fori, filepathinenumerate(docx_files,1): text = extract_text_from_docx(filepath) idcards = find_idcards(text) iflen(idcards) >0: print(f"[{i}/{total}] 扫描:{filepath.name}- 发现{len(idcards)}个身份证号")

这是一个简单的抽取word纯文本的简单方式

这个是一个最简单的判断身份证的方式：

其实这里注意2点：

1、身份证分老旧（15位、18位）

2、表现格式：就是一串连续的数字，还是分段存储的（可能是空格、短横等等）


```
importreimportzipfilefrompathlibimportPathfromxml.etreeimportElementTreeasET
# 1defextract_text_from_docx(docx_path): text ="" try: withzipfile.ZipFile(docx_path)asdocx_zip: withdocx_zip.open('word/document.xml')asdocument_xml: tree = ET.parse(document_xml) root = tree.getroot() foreleminroot.iter(): ifelem.tag.endswith('}t'): text += elem.text +' ' exceptExceptionase: print(f"Error processing{docx_path}:{e}") returntext.strip()
# 2deffind_idcards(text:
str) ->list: results = [] pattern_18 =r'b(d{17}[dXx])b' formatchinre.finditer(pattern_18, text): id_num =match.group(1) ifid_numnotinresults: results.append(id_num) returnresultsif__name__ =='__main__': all_results = [] docx_files =list(Path("./docs").rglob('*.docx')) total =len(docx_files) print(f"找到{total}个 Word 文档") idcard = [] fori, filepathinenumerate(docx_files,1): text = extract_text_from_docx(filepath) idcards = find_idcards(text) iflen(idcards) >0: print(f"[{i}/{total}] 扫描:{filepath.name}- 发现{len(idcards)}个身份证号")
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]