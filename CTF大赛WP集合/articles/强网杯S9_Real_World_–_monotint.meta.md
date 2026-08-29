---
title: 强网杯S9 Real World monotint - V8 CVE-2024-12695 FinalizationRegistry利用
contest: 强网杯S9线下赛
year: 2025
difficulty: hard
vuln_type: web_unknown
tags: [V8, CVE-2024-12695, FinalizationRegistry, unregister_token, Object.assign, Object.builtins, JSWeakRef, SimpleNumberDictionary, OOB_arr, 越界写, 浏览器沙箱逃逸, hash_map, register/weak_cell, addrof, AAR, AW, 0x300R, monotint, chromium_no_sandbox]
attack_chain: patch V8 src/builtins/builtins-object-gen.cc删ObjectAssign properties hash check + js-weak-refs.cc CHECK→DCHECK → 0x300R monotint浏览器nday → 适配CVE-2024-12695 → 编译chromium 139.0.7258.128 v8_enable_sandbox=false → registry.register触发unregister_token hash生成 → Object.assign覆盖properties → 越界写入victim_arr → corrupt_obj_get_hash预测hash → construct_oob_arr用register触发地址预测写key_list_prev → 错位字节resize构造稳定OOB → cage_read/cage_write实现addrof+AAR+AW → 沙箱逃逸到gnome-calculator弹计算器
key_payload: Object.assign绕过properties hash check + SimpleNumberDictionary越界写 + 错位字节resize + V8 sandbox escape
one_liner: 强网杯S9 Real World monotint:0x300R浏览器nday CVE-2024-12695 V8 FinalizationRegistry越界写到沙箱逃逸弹计算器。
lesson: V8 FinalizationRegistry + Object.assign组合漏洞:unregister_token在register时分配hash,Object.assign会覆盖properties指向PropertyArray绕过hash check;SimpleNumberDictionary越界写可破坏OOB arr;CVE-2024-12695需patch ObjectAssign+JSFinalizationRegistry::RemoveCellFromUnregisterToken;V8 sandbox逃逸用cage_read/cage_write稳定原语;浏览器nday完整利用链:patch+编译+JS+escape。
quality: high
---
