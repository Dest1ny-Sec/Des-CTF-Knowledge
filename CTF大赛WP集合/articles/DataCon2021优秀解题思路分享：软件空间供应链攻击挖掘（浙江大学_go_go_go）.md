# DataCon2021优秀解题思路分享：软件空间供应链攻击挖掘（浙江大学 go_go_go）

> 原文: https://www.ctfiot.com/74661.html
> ID: 74661


```
另外我们拿到了1.1.3以前的zlib的静态常量数组，通过搜索该数组，我们可以通过排除法，确定zlib的版本范围，从而确定是否包含CVE-2002-0059(zlib 1.0.0-1.1.3)
v1.0.5~v1.1.3:
local const uInt cplext[31] = { /* Extra bits for literal codes 257..285 */
 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2,
 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 0, 112, 112}; /* 112==invalid */
v0.71~1.0:
local uInt cplext[] = { /* Extra bits for literal codes 257..285 */
 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2,
 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 0, 192, 192}; /* 192==invalid */
v1.0以后，都去除了这个数组：
 {0,1,2,4,5,7,8,10,11,12,16,22,23,26}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/img_6375d3a03a130.png)