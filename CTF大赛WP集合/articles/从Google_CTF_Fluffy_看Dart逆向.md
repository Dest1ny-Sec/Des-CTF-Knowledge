# 从Google CTF Fluffy 看Dart逆向

> 原文: https://www.ctfiot.com/261979.html
> ID: 261979

// 0x358708:DecompressPointer r2
//     0x358708:add             x2, x2, HEAP, lsl #32

寄存器

用途

说明

用于类型跳转（vtable）调用、类 ID 映射等

当前线程指针（Thread* thr）

GC、栈检查等使用

常量池指针（ObjectPool* pp）

用于加载常量、内联缓存等

Heap 基地址

解压压缩指针

虚拟栈指针

传递更多参数 / spill slot

_QWORD (__usercall *)@<X0>(DartObjectPool *pool@<X27>, DartThread *thread@<X26>, _QWORD *stack@<X15>, _QWORD@<X1>, _QWORD@<X2>, _QWORD@<X4>)

staticintsaveSecret(unsignedchar* res, constvoid* token, int token_len, int pin, constvoid* secret, int secret_len) {
unsignedchar* token_bytes = malloc(token_len);
int token_bytes_len = b62decode(token_bytes, token, token_len);
assert(token_bytes_len == 8);
memcpy(res, secret, secret_len);
for (int i = 0; i < pin; i++) {
for (int j = 0; j < secret_len; j++) {
            res[j] = rol1(res[j] + token_bytes[j % token_bytes_len], j & 7);
        }
unsignedchar tmp = res[secret_len - 1];
memmove(res + 1, res, secret_len - 1);
        res[0] = tmp;
update_token_bytes(token_bytes, token_bytes_len, pin, i);
    }
free(token_bytes);
return b62encode(res, res, secret_len);
}
staticvoidupdate_token_bytes(unsignedchar* token_bytes, int token_bytes_len, int pin, int round) {
unsignedchar tmp = token_bytes[0];
memmove(token_bytes, token_bytes + 1, token_bytes_len - 1);
    token_bytes[token_bytes_len - 1] = tmp;
for (int j = 0; j < token_bytes_len; j++) {
        token_bytes[j] = ror1(token_bytes[j], (pin ^ ((round & 3) + 1)) & 7);
    }
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <gmp.h>
#include <openssl/sha.h>
#include <pthread.h>
#include <assert.h>

staticunsignedcharrol1(unsignedchar x, int n) {
return (x << n) | (x >> (8 - n));
}

staticunsignedcharror1(unsignedchar x, int n) {
return (x >> n) | (x << (8 - n));
}

staticvoidreverse_str(unsignedchar* s, int n) {
for (int i = 0, j = n - 1; i < j; i++, j--) {
unsignedchar tmp = s[i];
        s[i] = s[j];
        s[j] = tmp;
    }
}

staticvoidbytes_to_long(mpz_t* res, constunsignedchar* s, int n) {
mpz_set_ui(*res, 0);
for (int i = 0; i < n; i++) {
mpz_mul_ui(*res, *res, 256);
mpz_add_ui(*res, *res, s[i]);
    }
}

staticintlong_to_bytes(unsignedchar* res, constmpz_t* v) {
mpz_t t;
mpz_init(t);
mpz_set(t, *v);
int l = 0;
while (mpz_cmp_ui(t, 0)) {
        res[l++] = mpz_get_ui(t) & 0xff;
mpz_fdiv_q_ui(t, t, 256);
    }
mpz_clear(t);
reverse_str(res, l);
return l;
}

staticconstchar* b62table = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
staticunsignedchar b62table_r[256];

staticvoidinit_b62table() {
for (int i = 0; i < strlen(b62table); i++) {
        b62table_r[b62table[i] & 0xff] = i;
    }
}

staticintb62encode(unsignedchar* res, constunsignedchar* s, int n) {
if (!b62table_r['z']) {
init_b62table();
    }
mpz_t v;
mpz_init(v);

bytes_to_long(&v, s, n);
int l = 0;
mpz_t mod;
mpz_init(mod);
while (mpz_cmp_ui(v, 0)) {
mpz_mod_ui(mod, v, 62);
        res[l++] = b62table[mpz_get_ui(mod)];
mpz_fdiv_q_ui(v, v, 62);
    }
mpz_clear(mod);
mpz_clear(v);
reverse_str(res, l);
    res[l] = 0;
return l;
}

staticintb62decode(unsignedchar* res, constunsignedchar* s, int n) {
if (!b62table_r['z']) {
init_b62table();
    }
mpz_t v;
mpz_init(v);
for (int i = 0; i < n; i++) {
mpz_mul_ui(v, v, 62);
mpz_add_ui(v, v, b62table_r[s[i]]);
    }
int l = long_to_bytes(res, &v);
mpz_clear(v);
    res[l] = 0;
return l;
}

staticintgenerate_token(char* res, time_t ts) {
if (!ts) {
        ts = time(NULL);
    }
char buffer[256];
sprintf(buffer, "gctf25_%ld", ts);
unsignedchar hash[20];
SHA1((unsignedchar*) buffer, strlen(buffer), hash);
return b62encode((unsignedchar*) res, hash, 8);
}

staticvoidupdate_token_bytes(unsignedchar* token_bytes, int token_bytes_len, int pin, int round) {
unsignedchar tmp = token_bytes[0];
memmove(token_bytes, token_bytes + 1, token_bytes_len - 1);
    token_bytes[token_bytes_len - 1] = tmp;
for (int j = 0; j < token_bytes_len; j++) {
        token_bytes[j] = ror1(token_bytes[j], (pin ^ ((round & 3) + 1)) & 7);
    }
}

staticintsaveSecret(unsignedchar* res, constvoid* token, int token_len, int pin, constvoid* secret, int secret_len) {
unsignedchar* token_bytes = malloc(token_len);
int token_bytes_len = b62decode(token_bytes, token, token_len);
assert(token_bytes_len == 8);
memcpy(res, secret, secret_len);
for (int i = 0; i < pin; i++) {
for (int j = 0; j < secret_len; j++) {
            res[j] = rol1(res[j] + token_bytes[j % token_bytes_len], j & 7);
        }
unsignedchar tmp = res[secret_len - 1];
memmove(res + 1, res, secret_len - 1);
        res[0] = tmp;
update_token_bytes(token_bytes, token_bytes_len, pin, i);
    }
free(token_bytes);
return b62encode(res, res, secret_len);
}

staticintrestoreSecret(unsignedchar* res, constvoid* token, int token_len, int pin, constvoid* encrypted, int encrypted_len) {
unsignedchar* token_bytes = malloc(0x18);
int token_bytes_len = b62decode(token_bytes, token, token_len);
int res_len = b62decode(res, encrypted, encrypted_len);
unsignedchar* token_bytes_list = malloc(pin * token_bytes_len);
for (int i = 0; i < pin; i++) {
memcpy(token_bytes_list + i * token_bytes_len, token_bytes, token_bytes_len);
update_token_bytes(token_bytes, token_bytes_len, pin, i);
    }
free(token_bytes);

for (int i = pin - 1; i >= 0; i--) {
unsignedchar* _token_bytes = token_bytes_list + i * token_bytes_len;
unsignedchar tmp = res[0];
for (int j = 0; j < res_len - 1; j++) {
            res[j] = res[j + 1];
        }
        res[res_len - 1] = tmp;
for (int j = 0; j < res_len; j++) {
            res[j] = ror1(res[j], j & 7) - _token_bytes[j % token_bytes_len];
        }
    }
free(token_bytes_list);
return res_len;
}

staticunsignedcharrestoreSecretWithPrecomputedAt(int index, constunsignedchar* token_bytes_list, int token_bytes_len, int pin, constunsignedchar* res_start, int res_len) {
assert(index >= 0 && index < res_len);

unsignedchar c = res_start[(index + pin) % res_len];
for (int i = pin - 1; i >= 0; i--) {
constunsignedchar* token_bytes = token_bytes_list + i * token_bytes_len;
constint c_index = (index + i) % res_len;
        c = ror1(c, c_index & 7) - token_bytes[c_index % token_bytes_len];
    }
return c;
}

staticintrestoreSecretWithPrecomputed(unsignedchar* res, constunsignedchar* token_bytes_list, int token_bytes_len, int pin, constunsignedchar* res_start, int res_len) {
memcpy(res, res_start, res_len);
for (int i = pin - 1; i >= 0; i--) {
constunsignedchar* token_bytes = token_bytes_list + i * token_bytes_len;
unsignedchar tmp = res[0];
memmove(res, res + 1, res_len - 1);
        res[res_len - 1] = tmp;
for (int j = 0; j < res_len; j++) {
// const int res_index = (j + pin - i) % res_len;
// res[res_index] = ror1(res[res_index], j & 7) - token_bytes[j % token_bytes_len];
            res[j] = ror1(res[j], j & 7) - token_bytes[j % token_bytes_len];
        }
    }
return res_len;
}

staticintis_printable(constunsignedchar* s, int n) {
for (int i = 0; i < n; i++) {
if (s[i] < 0x20 || s[i] >= 0x7f) {
return 0;
        }
    }
return 1;
}

staticvoidbf_secret(int ts_lower_bound, int ts_upper_bound, constvoid* encrypted, int encrypted_len) {
/*
    char token[0x100];
    unsigned char* decrypted = malloc(encrypted_len);
    for (int ts = ts_upper_bound - 1; ts >= ts_lower_bound; ts--) {
        int token_len = generate_token(token, ts);
        for (int pin = 1; pin < 10000; pin++) {
            printf("r%d, %d: ", ts, pin);
            int decrypted_len = restoreSecret(decrypted, token, token_len, pin, encrypted, encrypted_len);
            if (is_printable(decrypted, decrypted_len)) {
                printf("r%d, %d: %sn", ts, pin, (char*) decrypted);
            }
        }
    }
    free(decrypted);
*/
unsignedchar* res_start = malloc(encrypted_len);
unsignedchar* decrypted = malloc(encrypted_len);
memset(decrypted, 0, encrypted_len);
unsignedchar* token_bytes = malloc(0x18);
unsignedchar* token_bytes_list = malloc(10000 * 0x10);
int res_len = b62decode(res_start, encrypted, encrypted_len);
char token[0x100];
for (int ts = ts_upper_bound - 1; ts >= ts_lower_bound; ts--) {
int token_len = generate_token(token, ts);
for (int pin_start = 1; pin_start < 9; pin_start++) {
// printf("r%d, %d: ", ts, pin_start);
int token_bytes_len = b62decode(token_bytes, (unsignedchar*) token, token_len);
for (int i = 0; i < 10000; i++) {
memcpy(token_bytes_list + i * token_bytes_len, token_bytes, token_bytes_len);
update_token_bytes(token_bytes, token_bytes_len, pin_start, i);
            }
for (int pin = pin_start; pin < 10000; pin += 8) {
if (restoreSecretWithPrecomputedAt(res_len - 1, token_bytes_list, token_bytes_len, pin, res_start, res_len) == '}') {
int decrypted_len = restoreSecretWithPrecomputed(decrypted, token_bytes_list, token_bytes_len, pin, res_start, res_len);
if (is_printable(decrypted, decrypted_len)) {
printf("r%d, %d: %sn", ts, pin, (char*) decrypted);
// exit(0);
                    }
                }
            }
        }
    }
free(token_bytes_list);
free(token_bytes);
free(decrypted);
free(res_start);
}

struct bf_secret_thread_struct {
int id;
int ts_lower_bound;
int ts_upper_bound;
constchar* encrypted;
};

#define THREAD_COUNT 16
#define SECONDS_PER_THREAD 60 * 60
#define SECONDS_PRE_LOG 60

staticvoidbf_secret_thread(struct bf_secret_thread_struct* arg) {
printf("thread %d started (from %d to %d)n", arg->id, arg->ts_lower_bound, arg->ts_upper_bound);
// while (1) {
constint ts_count = arg->ts_upper_bound - arg->ts_lower_bound;
assert(ts_count % SECONDS_PRE_LOG == 0);
constint log_count = ts_count / SECONDS_PRE_LOG;
for (int i = 0; i < log_count; i++) {
printf("thread %2d: %d / %dn", arg->id, i, log_count);
bf_secret(arg->ts_lower_bound + SECONDS_PRE_LOG * i, arg->ts_lower_bound + SECONDS_PRE_LOG * (i + 1), arg->encrypted, strlen(arg->encrypted));
        }
printf("thread %d finishedn", arg->id);
// prepare_next_arg(arg);
// }
free(arg);
}

intmain() {
/*
    unsigned char res[100];
    unsigned char res2[100];
    int l1 = b62encode(res, (unsigned char*) "0123456789abcdef", 16);
    printf("%d: %sn", l1, (char*) res);
    int l2 = b62decode(res2, res, l1);
    printf("%d: %sn", l2, (char*) res2);
    unsigned char res[100];
    generate_token(res, 1000);
    puts((char*) res);

    const int pin = 1000;
    const char* token = "aaaaaaaaaaa";
    const int token_len = strlen(token);

    unsigned char res[0x100];
    unsigned char res2[0x100];
    int l1 = saveSecret(res, token, token_len, pin, "0123456789abcdef", 16);
    printf("%d: %sn", l1, (char*) res);
    int l2 = restoreSecret(res2, token, token_len, pin, res, l1);
    printf("%d: %sn", l2, (char*) res2);
    */

setbuf(stdout, NULL);

/*
    const int lower_bound = 1691127420 + 60 + 8 * 60 * 60 - 12 * 60 * 60;
    const char* encrypted = "fmMf7mIMbHcPoQmLGx1CO0XVGBmhjTaYhB0";

    pthread_t threads[24];
    for (int i = 0; i < 24; i++) {
        struct bf_secret_thread_struct* s = malloc(sizeof(struct bf_secret_thread_struct));
        s->id = i;
        s->ts_upper_bound = lower_bound + i * 60 * 60;
        s->ts_lower_bound = s->ts_upper_bound - 10 * 60;
        s->encrypted = encrypted;
        assert(!pthread_create(threads + i,NULL, (void*) bf_secret_thread, s));
    }
    for (int i = 0; i < 24; i++) {
        assert(!pthread_join(threads[i], NULL));
    }

    puts("done");
    */

/*
    const int upper_bound[] = {
        1691127420 + 60 + 6 * 60 * 60,
        1725706320 + 60 + 6 * 60 * 60,
        1741010820 + 60 + 6 * 60 * 60
    };
    const char* encrypted[] = {
        "fmMf7mIMbHcPoQmLGx1CO0XVGBmhjTaYhB0",
        "5O6WRgCajs3QSTyohnu2hldds18mjkx",
        "fgv99dOvazsvEESh7DPKbb3k0I3RW"
    };

    const int idx = 2;
    bf_secret(upper_bound[idx] - 10 * 60, upper_bound[idx], encrypted[idx], strlen(encrypted[idx]));
    */

// const int upper_bound = 1741010820 + 60 + 8 * 60 * 60; // - THREAD_COUNT * SECONDS_PER_THREAD;
// const char* encrypted = "fgv99dOvazsvEESh7DPKbb3k0I3RW";

// pthread_t threads[THREAD_COUNT];
// for (int i = 0; i < THREAD_COUNT; i++) {
//     struct bf_secret_thread_struct* s = malloc(sizeof(struct bf_secret_thread_struct));
//     s->id = i;
//     s->ts_upper_bound = upper_bound - i * SECONDS_PER_THREAD;
//     s->ts_lower_bound = s->ts_upper_bound - SECONDS_PER_THREAD;
//     s->encrypted = encrypted;
//     assert(!pthread_create(threads + i,NULL, (void*) bf_secret_thread, s));
// }
// for (int i = 0; i < THREAD_COUNT; i++) {
//     assert(!pthread_join(threads[i], NULL));
// }

// puts("done");

// bf_secret_string(1691127420 + 60 + 8 * 60 * 60, "fmMf7mIMbHcPoQmLGx1CO0XVGBmhjTaYhB0");
// 1691149047, 8126: CTF{Ok4y_h4v3_u_0ptim1zed_
// bf_secret_string(1725706320 + 60 + 8 * 60 * 60, "5O6WRgCajs3QSTyohnu2hldds18mjkx");
// 1725727951, 5178: brUt3_f0rcE_0R_y0u_jUst
// bf_secret_string(1741010820 + 60 + 8 * 60 * 60, "fgv99dOvazsvEESh7DPKbb3k0I3RW");
// 

return 0;
}

// gcc ./main.c -o main -s -O3 -Wall -Wno-unused-function -lgmp -lcrypto && ./main

// CTF{Ok4y_h4v3_u_0ptim1zed_brUt3_f0rcE_0R_y0u_jUst

看雪ID：SleepAlone

https://bbs.kanxue.com/user-home-950548.htm

*本文为看雪论坛优秀文章，由 SleepAlone 原创，转载请注明来自看雪社区

看雪·2025 KCTF 将于8月15日正式开赛

欢迎来战

# 往期推荐

Pwn题解析｜L3CTF 2025 heack & heack_revenge

OLLVM-BR间接混淆去除

House of Einherjar

LLVM 基本块VMP保护之简易虚拟机示例实现

企业微信 – 白日梦之获取登录二维码

球分享

球点赞

球在看

点击阅读原文查看更多


```
// 0x358708:DecompressPointer r2
//     0x358708:add             x2, x2, HEAP, lsl #32
```



```
_QWORD (__usercall *)@<X0>(DartObjectPool *pool@<X27>, DartThread *thread@<X26>, _QWORD *stack@<X15>, _QWORD@<X1>, _QWORD@<X2>, _QWORD@<X4>)
```



```
staticintsaveSecret(unsignedchar* res, constvoid* token, int token_len, int pin, constvoid* secret, int secret_len) {
unsignedchar* token_bytes = malloc(token_len);
int token_bytes_len = b62decode(token_bytes, token, token_len);
assert(token_bytes_len == 8);
memcpy(res, secret, secret_len);
for (int i = 0; i < pin; i++) {
for (int j = 0; j < secret_len; j++) {
            res[j] = rol1(res[j] + token_bytes[j % token_bytes_len], j & 7);
        }
unsignedchar tmp = res[secret_len - 1];
memmove(res + 1, res, secret_len - 1);
        res[0] = tmp;
update_token_bytes(token_bytes, token_bytes_len, pin, i);
    }
free(token_bytes);
return b62encode(res, res, secret_len);
}
staticvoidupdate_token_bytes(unsignedchar* token_bytes, int token_bytes_len, int pin, int round) {
unsignedchar tmp = token_bytes[0];
memmove(token_bytes, token_bytes + 1, token_bytes_len - 1);
    token_bytes[token_bytes_len - 1] = tmp;
for (int j = 0; j < token_bytes_len; j++) {
        token_bytes[j] = ror1(token_bytes[j], (pin ^ ((round & 3) + 1)) & 7);
    }
}
```



```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <gmp.h>
#include <openssl/sha.h>
#include <pthread.h>
#include <assert.h>

staticunsignedcharrol1(unsignedchar x, int n) {
return (x << n) | (x >> (8 - n));
}

staticunsignedcharror1(unsignedchar x, int n) {
return (x >> n) | (x << (8 - n));
}

staticvoidreverse_str(unsignedchar* s, int n) {
for (int i = 0, j = n - 1; i < j; i++, j--) {
unsignedchar tmp = s[i];
        s[i] = s[j];
        s[j] = tmp;
    }
}

staticvoidbytes_to_long(mpz_t* res, constunsignedchar* s, int n) {
mpz_set_ui(*res, 0);
for (int i = 0; i < n; i++) {
mpz_mul_ui(*res, *res, 256);
mpz_add_ui(*res, *res, s[i]);
    }
}

staticintlong_to_bytes(unsignedchar* res, constmpz_t* v) {
mpz_t t;
mpz_init(t);
mpz_set(t, *v);
int l = 0;
while (mpz_cmp_ui(t, 0)) {
        res[l++] = mpz_get_ui(t) & 0xff;
mpz_fdiv_q_ui(t, t, 256);
    }
mpz_clear(t);
reverse_str(res, l);
return l;
}

staticconstchar* b62table = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
staticunsignedchar b62table_r[256];

staticvoidinit_b62table() {
for (int i = 0; i < strlen(b62table); i++) {
        b62table_r[b62table[i] & 0xff] = i;
    }
}

staticintb62encode(unsignedchar* res, constunsignedchar* s, int n) {
if (!b62table_r['z']) {
init_b62table();
    }
mpz_t v;
mpz_init(v);

bytes_to_long(&v, s, n);
int l = 0;
mpz_t mod;
mpz_init(mod);
while (mpz_cmp_ui(v, 0)) {
mpz_mod_ui(mod, v, 62);
        res[l++] = b62table[mpz_get_ui(mod)];
mpz_fdiv_q_ui(v, v, 62);
    }
mpz_clear(mod);
mpz_clear(v);
reverse_str(res, l);
    res[l] = 0;
return l;
}

staticintb62decode(unsignedchar* res, constunsignedchar* s, int n) {
if (!b62table_r['z']) {
init_b62table();
    }
mpz_t v;
mpz_init(v);
for (int i = 0; i < n; i++) {
mpz_mul_ui(v, v, 62);
mpz_add_ui(v, v, b62table_r[s[i]]);
    }
int l = long_to_bytes(res, &v);
mpz_clear(v);
    res[l] = 0;
return l;
}

staticintgenerate_token(char* res, time_t ts) {
if (!ts) {
        ts = time(NULL);
    }
char buffer[256];
sprintf(buffer, "gctf25_%ld", ts);
unsignedchar hash[20];
SHA1((unsignedchar*) buffer, strlen(buffer), hash);
return b62encode((unsignedchar*) res, hash, 8);
}

staticvoidupdate_token_bytes(unsignedchar* token_bytes, int token_bytes_len, int pin, int round) {
unsignedchar tmp = token_bytes[0];
memmove(token_bytes, token_bytes + 1, token_bytes_len - 1);
    token_bytes[token_bytes_len - 1] = tmp;
for (int j = 0; j < token_bytes_len; j++) {
        token_bytes[j] = ror1(token_bytes[j], (pin ^ ((round & 3) + 1)) & 7);
    }
}

staticintsaveSecret(unsignedchar* res, constvoid* token, int token_len, int pin, constvoid* secret, int secret_len) {
unsignedchar* token_bytes = malloc(token_len);
int token_bytes_len = b62decode(token_bytes, token, token_len);
assert(token_bytes_len == 8);
memcpy(res, secret, secret_len);
for (int i = 0; i < pin; i++) {
for (int j = 0; j < secret_len; j++) {
            res[j] = rol1(res[j] + token_bytes[j % token_bytes_len], j & 7);
        }
unsignedchar tmp = res[secret_len - 1];
memmove(res + 1, res, secret_len - 1);
        res[0] = tmp;
update_token_bytes(token_bytes, token_bytes_len, pin, i);
    }
free(token_bytes);
return b62encode(res, res, secret_len);
}

staticintrestoreSecret(unsignedchar* res, constvoid* token, int token_len, int pin, constvoid* encrypted, int encrypted_len) {
unsignedchar* token_bytes = malloc(0x18);
int token_bytes_len = b62decode(token_bytes, token, token_len);
int res_len = b62decode(res, encrypted, encrypted_len);
unsignedchar* token_bytes_list = malloc(pin * token_bytes_len);
for (int i = 0; i < pin; i++) {
memcpy(token_bytes_list + i * token_bytes_len, token_bytes, token_bytes_len);
update_token_bytes(token_bytes, token_bytes_len, pin, i);
    }
free(token_bytes);

for (int i = pin - 1; i >= 0; i--) {
unsignedchar* _token_bytes = token_bytes_list + i * token_bytes_len;
unsignedchar tmp = res[0];
for (int j = 0; j < res_len - 1; j++) {
            res[j] = res[j + 1];
        }
        res[res_len - 1] = tmp;
for (int j = 0; j < res_len; j++) {
            res[j] = ror1(res[j], j & 7) - _token_bytes[j % token_bytes_len];
        }
    }
free(token_bytes_list);
return res_len;
}

staticunsignedcharrestoreSecretWithPrecomputedAt(int index, constunsignedchar* token_bytes_list, int token_bytes_len, int pin, constunsignedchar* res_start, int res_len) {
assert(index >= 0 && index < res_len);

unsignedchar c = res_start[(index + pin) % res_len];
for (int i = pin - 1; i >= 0; i--) {
constunsignedchar* token_bytes = token_bytes_list + i * token_bytes_len;
constint c_index = (index + i) % res_len;
        c = ror1(c, c_index & 7) - token_bytes[c_index % token_bytes_len];
    }
return c;
}

staticintrestoreSecretWithPrecomputed(unsignedchar* res, constunsignedchar* token_bytes_list, int token_bytes_len, int pin, constunsignedchar* res_start, int res_len) {
memcpy(res, res_start, res_len);
for (int i = pin - 1; i >= 0; i--) {
constunsignedchar* token_bytes = token_bytes_list + i * token_bytes_len;
unsignedchar tmp = res[0];
memmove(res, res + 1, res_len - 1);
        res[res_len - 1] = tmp;
for (int j = 0; j < res_len; j++) {
// const int res_index = (j + pin - i) % res_len;
// res[res_index] = ror1(res[res_index], j & 7) - token_bytes[j % token_bytes_len];
            res[j] = ror1(res[j], j & 7) - token_bytes[j % token_bytes_len];
        }
    }
return res_len;
}

staticintis_printable(constunsignedchar* s, int n) {
for (int i = 0; i < n; i++) {
if (s[i] < 0x20 || s[i] >= 0x7f) {
return 0;
        }
    }
return 1;
}

staticvoidbf_secret(int ts_lower_bound, int ts_upper_bound, constvoid* encrypted, int encrypted_len) {
/*
    char token[0x100];
    unsigned char* decrypted = malloc(encrypted_len);
    for (int ts = ts_upper_bound - 1; ts >= ts_lower_bound; ts--) {
        int token_len = generate_token(token, ts);
        for (int pin = 1; pin < 10000; pin++) {
            printf("r%d, %d: ", ts, pin);
            int decrypted_len = restoreSecret(decrypted, token, token_len, pin, encrypted, encrypted_len);
            if (is_printable(decrypted, decrypted_len)) {
                printf("r%d, %d: %sn", ts, pin, (char*) decrypted);
            }
        }
    }
    free(decrypted);
*/
unsignedchar* res_start = malloc(encrypted_len);
unsignedchar* decrypted = malloc(encrypted_len);
memset(decrypted, 0, encrypted_len);
unsignedchar* token_bytes = malloc(0x18);
unsignedchar* token_bytes_list = malloc(10000 * 0x10);
int res_len = b62decode(res_start, encrypted, encrypted_len);
char token[0x100];
for (int ts = ts_upper_bound - 1; ts >= ts_lower_bound; ts--) {
int token_len = generate_token(token, ts);
for (int pin_start = 1; pin_start < 9; pin_start++) {
// printf("r%d, %d: ", ts, pin_start);
int token_bytes_len = b62decode(token_bytes, (unsignedchar*) token, token_len);
for (int i = 0; i < 10000; i++) {
memcpy(token_bytes_list + i * token_bytes_len, token_bytes, token_bytes_len);
update_token_bytes(token_bytes, token_bytes_len, pin_start, i);
            }
for (int pin = pin_start; pin < 10000; pin += 8) {
if (restoreSecretWithPrecomputedAt(res_len - 1, token_bytes_list, token_bytes_len, pin, res_start, res_len) == '}') {
int decrypted_len = restoreSecretWithPrecomputed(decrypted, token_bytes_list, token_bytes_len, pin, res_start, res_len);
if (is_printable(decrypted, decrypted_len)) {
printf("r%d, %d: %sn", ts, pin, (char*) decrypted);
// exit(0);
                    }
                }
            }
        }
    }
free(token_bytes_list);
free(token_bytes);
free(decrypted);
free(res_start);
}

struct bf_secret_thread_struct {
int id;
int ts_lower_bound;
int ts_upper_bound;
constchar* encrypted;
};

#define THREAD_COUNT 16
#define SECONDS_PER_THREAD 60 * 60
#define SECONDS_PRE_LOG 60

staticvoidbf_secret_thread(struct bf_secret_thread_struct* arg) {
printf("thread %d started (from %d to %d)n", arg->id, arg->ts_lower_bound, arg->ts_upper_bound);
// while (1) {
constint ts_count = arg->ts_upper_bound - arg->ts_lower_bound;
assert(ts_count % SECONDS_PRE_LOG == 0);
constint log_count = ts_count / SECONDS_PRE_LOG;
for (int i = 0; i < log_count; i++) {
printf("thread %2d: %d / %dn", arg->id, i, log_count);
bf_secret(arg->ts_lower_bound + SECONDS_PRE_LOG * i, arg->ts_lower_bound + SECONDS_PRE_LOG * (i + 1), arg->encrypted, strlen(arg->encrypted));
        }
printf("thread %d finishedn", arg->id);
// prepare_next_arg(arg);
// }
free(arg);
}

intmain() {
/*
    unsigned char res[100];
    unsigned char res2[100];
    int l1 = b62encode(res, (unsigned char*) "0123456789abcdef", 16);
    printf("%d: %sn", l1, (char*) res);
    int l2 = b62decode(res2, res, l1);
    printf("%d: %sn", l2, (char*) res2);
    unsigned char res[100];
    generate_token(res, 1000);
    puts((char*) res);

    const int pin = 1000;
    const char* token = "aaaaaaaaaaa";
    const int token_len = strlen(token);

    unsigned char res[0x100];
    unsigned char res2[0x100];
    int l1 = saveSecret(res, token, token_len, pin, "0123456789abcdef", 16);
    printf("%d: %sn", l1, (char*) res);
    int l2 = restoreSecret(res2, token, token_len, pin, res, l1);
    printf("%d: %sn", l2, (char*) res2);
    */

setbuf(stdout, NULL);

/*
    const int lower_bound = 1691127420 + 60 + 8 * 60 * 60 - 12 * 60 * 60;
    const char* encrypted = "fmMf7mIMbHcPoQmLGx1CO0XVGBmhjTaYhB0";

    pthread_t threads[24];
    for (int i = 0; i < 24; i++) {
        struct bf_secret_thread_struct* s = malloc(sizeof(struct bf_secret_thread_struct));
        s->id = i;
        s->ts_upper_bound = lower_bound + i * 60 * 60;
        s->ts_lower_bound = s->ts_upper_bound - 10 * 60;
        s->encrypted = encrypted;
        assert(!pthread_create(threads + i,NULL, (void*) bf_secret_thread, s));
    }
    for (int i = 0; i < 24; i++) {
        assert(!pthread_join(threads[i], NULL));
    }

    puts("done");
    */

/*
    const int upper_bound[] = {
        1691127420 + 60 + 6 * 60 * 60,
        1725706320 + 60 + 6 * 60 * 60,
        1741010820 + 60 + 6 * 60 * 60
    };
    const char* encrypted[] = {
        "fmMf7mIMbHcPoQmLGx1CO0XVGBmhjTaYhB0",
        "5O6WRgCajs3QSTyohnu2hldds18mjkx",
        "fgv99dOvazsvEESh7DPKbb3k0I3RW"
    };

    const int idx = 2;
    bf_secret(upper_bound[idx] - 10 * 60, upper_bound[idx], encrypted[idx], strlen(encrypted[idx]));
    */

// const int upper_bound = 1741010820 + 60 + 8 * 60 * 60; // - THREAD_COUNT * SECONDS_PER_THREAD;
// const char* encrypted = "fgv99dOvazsvEESh7DPKbb3k0I3RW";

// pthread_t threads[THREAD_COUNT];
// for (int i = 0; i < THREAD_COUNT; i++) {
//     struct bf_secret_thread_struct* s = malloc(sizeof(struct bf_secret_thread_struct));
//     s->id = i;
//     s->ts_upper_bound = upper_bound - i * SECONDS_PER_THREAD;
//     s->ts_lower_bound = s->ts_upper_bound - SECONDS_PER_THREAD;
//     s->encrypted = encrypted;
//     assert(!pthread_create(threads + i,NULL, (void*) bf_secret_thread, s));
// }
// for (int i = 0; i < THREAD_COUNT; i++) {
//     assert(!pthread_join(threads[i], NULL));
// }

// puts("done");

// bf_secret_string(1691127420 + 60 + 8 * 60 * 60, "fmMf7mIMbHcPoQmLGx1CO0XVGBmhjTaYhB0");
// 1691149047, 8126: CTF{Ok4y_h4v3_u_0ptim1zed_
// bf_secret_string(1725706320 + 60 + 8 * 60 * 60, "5O6WRgCajs3QSTyohnu2hldds18mjkx");
// 1725727951, 5178: brUt3_f0rcE_0R_y0u_jUst
// bf_secret_string(1741010820 + 60 + 8 * 60 * 60, "fgv99dOvazsvEESh7DPKbb3k0I3RW");
// 

return 0;
}

// gcc ./main.c -o main -s -O3 -Wall -Wno-unused-function -lgmp -lcrypto && ./main

// CTF{Ok4y_h4v3_u_0ptim1zed_brUt3_f0rcE_0R_y0u_jUst
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752834780-wxsync-2025-07-91e5f3127d698d291da2337308d27168.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752834781-wxsync-2025-07-ec39ff4f8a59c3bec1c34a48da1b264a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752834784-wxsync-2025-07-0951a20c9d38465cf59b7d969816e13d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752834791-wxsync-2025-07-71612baea187590d75a96ee2368782fc.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752834793-wxsync-2025-07-d2ca368f75092f5eee67f5eec75b95e9.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752834796-wxsync-2025-07-d2ca368f75092f5eee67f5eec75b95e9.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752834798-wxsync-2025-07-d2ca368f75092f5eee67f5eec75b95e9.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752834801-wxsync-2025-07-f3a6e530b80ade00f97deed30f426eb6.gif)