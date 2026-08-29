---
title: 【WP】第七届"湖湘杯" House OF Emma 设计思路与解析
contest: 湖湘杯
year: 2021
difficulty: hard
vuln_type: pwn_unknown
tags: [House-of-Emma, _IO_cookie_jumps, _IO_cookie_file, cookie_read_function, cookie_write_function, PTR_DEMANGLE, large-bin-attack, glibc-2.35]
attack_chain: large bin attack 写 _IO_list_all + 触发 _IO_flush_all_lockp → 调 __doallocate/伪造 _IO_FILE + vtable = _IO_cookie_jumps（不被检查）/cookie_read_function = system 触发 RCE
key_payload: _IO_cookie_jumps vtable 不在检查表 +  large bin attack
one_liner: 第七届湖湘杯 House of Emma 高级 IO 攻击，利用 _IO_cookie_jumps vtable + large bin attack 绕 vtable 检查。
lesson: _IO_cookie_jumps 是 _IO_FILE_plus vtable 检查白名单外的合法 vtable；_IO_cookie_file 结构体含 cookie_read_function 指针可被劫持；large bin attack 写 _IO_list_all 是触发 _IO_flush_all_lockp 的经典手法。
quality: high
---

# 【WP】第七届"湖湘杯" House OF Emma 设计思路与解析

## 概览
第七届湖湘杯 House of Emma 高级 IO 攻击题目设计与解析，基于 _IO_cookie_jumps vtable 攻击。

## 核心结构

### _IO_cookie_jumps vtable
```c
static const struct _IO_jump_t _IO_cookie_jumps libio_vtable = {
    JUMP_INIT_DUMMY,
    JUMP_INIT(finish, _IO_file_finish),
    JUMP_INIT(overflow, _IO_file_overflow),
    JUMP_INIT(underflow, _IO_file_underflow),
    JUMP_INIT(uflow, _IO_default_uflow),
    JUMP_INIT(pbackfail, _IO_default_pbackfail),
    JUMP_INIT(xsputn, _IO_file_xsputn),
    JUMP_INIT(xsgetn, _IO_default_xsgetn),
    JUMP_INIT(seekoff, _IO_cookie_seekoff),
    JUMP_INIT(seekpos, _IO_default_seekpos),
    JUMP_INIT(setbuf, _IO_file_setbuf),
    JUMP_INIT(sync, _IO_file_sync),
    JUMP_INIT(doallocate, _IO_file_doallocate),
    JUMP_INIT(read, _IO_cookie_read),
    JUMP_INIT(write, _IO_cookie_write),
    JUMP_INIT(seek, _IO_cookie_seek),
    JUMP_INIT(close, _IO_cookie_close),
    JUMP_INIT(stat, _IO_default_stat),
    JUMP_INIT(showmanyc, _IO_default_showmanyc),
    JUMP_INIT(imbue, _IO_default_imbue),
};
```

### _IO_cookie_read 函数
```c
static ssize_t
_IO_cookie_read (FILE *fp, void *buf, ssize_t size)
{
    struct _IO_cookie_file *cfile = (struct _IO_cookie_file *) fp;
    cookie_read_function_t *read_cb = cfile->__io_functions.read;
#ifdef PTR_DEMANGLE
    PTR_DEMANGLE (read_cb);
#endif

    if (read_cb == NULL)
        return -1;

    return read_cb (cfile->__cookie, buf, size);
}
```

### _IO_cookie_write 函数
```c
static ssize_t
_IO_cookie_write (FILE *fp, const void *buf, ssize_t size)
{
    struct _IO_cookie_file *cfile = (struct _IO_cookie_file *) fp;
    cookie_write_function_t *write_cb = cfile->__io_functions.write;
#ifdef PTR_DEMANGLE
    PTR_DEMANGLE (write_cb);
#endif

    if (write_cb == NULL) {
        fp->_flags |= _IO_ERR_SEEN;
        return 0;
    }

    ssize_t n = write_cb (cfile->__cookie, buf, size);
    if (n < size)
        fp->_flags |= _IO_ERR_SEEN;

    return n;
}
```

## 攻击链

### 1. large bin attack
- 申请两个 large bin chunk
- free 一个到 unsorted bin
- 申请更大 size，让原 large bin chunk 重新插入 large bin
- 通过 UAF 篡改 large bin chunk 的 `bk_nextsize`
- 触发 `_int_malloc` 中的 large bin unlink 链
- 写 `_IO_list_all` 为 fake `_IO_FILE` 地址

### 2. 触发 _IO_flush_all_lockp
- 触发 `malloc_printerr` → `__libc_message` → `_IO_flush_all_lockp`
- 遍历 `_IO_list_all` 链
- 找到 fake `_IO_FILE` 触发 `__doallocate`（vtable 虚函数）

### 3. fake _IO_FILE 布局
- `_flags = 0`
- vtable 指向 `_IO_cookie_jumps`（不在 vtable 检查白名单内）
- `_wide_data->_wide_vtable` 指向 cookie 区
- `cookie_read_function = system`
- 第一次调用 read 时参数为 `__cookie`

### 4. RCE 触发
- 第一次 `_IO_file_doallocate` 调 vtable[0] 不会触发 read
- 第二次任意 IO 操作触发 `_IO_cookie_read` → `system(__cookie)`

## 经验提炼
- `_IO_cookie_jumps` 是 `_IO_FILE_plus` vtable 检查白名单外的合法 vtable
- `_IO_cookie_file` 结构体含 `cookie_read_function` 指针可被劫持
- large bin attack 写 `_IO_list_all` 是触发 `_IO_flush_all_lockp` 的经典手法
- `PTR_DEMANGLE` 在新版本 glibc 中会解密指针，但 cookie 函数是函数指针而非 vtable 入口
- `_IO_file_doallocate` 是 House of Emma 触发 RCE 的关键虚函数
- glibc 2.35+ 已加强 vtable 检查，但 `_IO_cookie_jumps` 仍合法
- House of Emma 由 NX 实验室 roderickchan 发现
- Emma 指代 `_IO_cookie_file` 中 cookie 字段
