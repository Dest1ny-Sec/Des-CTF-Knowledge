# Square CTF 2022: Yet Another Reversing Activity

> 原文: https://www.ctfiot.com/77789.html
> ID: 77789


```
rule silent_banker : banker
{
 meta:
 description = "This is just an example"
 threat_level = 3
 in_the_wild = true

 strings:
 $a = {6A 40 68 00 30 00 00 6A 14 8D 91}
 $b = {8D 4D B0 2B C1 83 C0 27 99 6A 4E 59 F7 F9}
 $c = "UVODFRYSIHLNWPEJXQZAKCBGMT"

 condition:
 $a or $b or $c
}
```



```
int yr_execute_code(YR_SCAN_CONTEXT* context)
{

// cut for brevity
 while (!stop)
 {
 // Read the opcode from the address indicated by the instruction pointer.
 opcode = *ip;

 // Advance the instruction pointer, which now points past the opcode.
 ip++;

 switch (opcode)
 {
 case OP_NOP:
 YR_DEBUG_FPRINTF(2, stderr, "- case OP_NOP: // %s()\n", __FUNCTION__);
 break;

 case OP_HALT:
 YR_DEBUG_FPRINTF(2, stderr, "- case OP_HALT: // %s()\n", __FUNCTION__);
 assert(stack.sp == 0); // When HALT is reached the stack should be empty.
 stop = true;
 break;

// etc...
 }
}
```



```
#!/bin/sh
./bootstrap.sh
./configure --with-debug-verbose=8
make
```



```
yara-4.2.3% ./bootstrap.sh
yara-4.2.3% ./build.sh
```



```
% echo "flag{test}" > test.txt
% ./yara-4.2.3/yara -C flag.yarc test.txt
0.000000 006981 + yr_initialize() {
0.001316 006981 - hash__initialize() {}
0.001332 006981 } // yr_initialize()
0.001434 006981 - yr_scanner_create() {}
0.001485 006981 + yr_scanner_scan_mem(buffer=0x7f91d236d000 buffer_size=11) {
0.001492 006981 + yr_scanner_scan_mem_blocks() {
0.001505 006981 - _yr_get_first_block() {} = 0x7ffc0c7f9650 // default iterator; single memory block, blocking
0.001517 006981 + _yr_scanner_scan_mem_block(block_data=0x7f91d236d000 block->base=0x0 block->size=11) {
0.001532 006981 } = 0 AKA ERROR_SUCCESS 0 // _yr_scanner_scan_mem_block()
0.001542 006981 - _yr_get_next_block() {} = (nil) // default iterator; single memory block, blocking
0.001549 006981 - _yr_get_file_size() {} = 11 // default iterator; single memory block, blocking
0.001556 006981 + yr_execute_code() {
0.001576 006981 - case OP_INIT_RULE: // yr_execute_code()
0.001583 006981 - case OP_PUSH_8: r1.i=0 // yr_execute_code()
0.001590 006981 - case OP_INT8: // yr_execute_code()
0.001595 006981 - _yr_get_first_block() {} = 0x7ffc0c7f9650 // default iterator; single memory block, blocking
0.001604 006981 - case OP_PUSH_8: r1.i=95 // yr_execute_code()
0.001612 006981 - case OP_PUSH_8: r1.i=57 // yr_execute_code()
0.001619 006981 - case OP_BITWISE_XOR: // yr_execute_code()
0.001627 006981 - case OP_INT_EQ: // yr_execute_code()
0.001634 006981 - case OP_JFALSE: // yr_execute_code()
0.001642 006981 - case OP_PUSH_8: r1.i=1 // yr_execute_code()
0.001650 006981 - case OP_INT8: // yr_execute_code()
0.001657 006981 - _yr_get_first_block() {} = 0x7ffc0c7f9650 // default iterator; single memory block, blocking
0.001664 006981 - case OP_PUSH_8: r1.i=51 // yr_execute_code()
0.001671 006981 - case OP_PUSH_8: r1.i=95 // yr_execute_code()
0.001678 006981 - case OP_BITWISE_XOR: // yr_execute_code()
0.001685 006981 - case OP_INT_EQ: // yr_execute_code()
0.001693 006981 - case OP_AND: // yr_execute_code()
0.001700 006981 - case OP_JFALSE: // yr_execute_code()
0.001707 006981 - case OP_PUSH_8: r1.i=2 // yr_execute_code()
0.001714 006981 - case OP_INT8: // yr_execute_code()
0.001721 006981 - _yr_get_first_block() {} = 0x7ffc0c7f9650 // default iterator; single memory block, blocking
0.001729 006981 - case OP_PUSH_8: r1.i=248 // yr_execute_code()
0.001741 006981 - case OP_PUSH_8: r1.i=153 // yr_execute_code()
0.001745 006981 - case OP_BITWISE_XOR: // yr_execute_code()
0.001753 006981 - case OP_INT_EQ: // yr_execute_code()
0.001762 006981 - case OP_AND: // yr_execute_code()
0.001767 006981 - case OP_JFALSE: // yr_execute_code()
0.001772 006981 - case OP_PUSH_8: r1.i=3 // yr_execute_code()
0.001777 006981 - case OP_INT8: // yr_execute_code()
0.001782 006981 - _yr_get_first_block() {} = 0x7ffc0c7f9650 // default iterator; single memory block, blocking
0.001790 006981 - case OP_PUSH_8: r1.i=83 // yr_execute_code()
0.001799 006981 - case OP_PUSH_8: r1.i=52 // yr_execute_code()
0.001806 006981 - case OP_BITWISE_XOR: // yr_execute_code()
0.001813 006981 - case OP_INT_EQ: // yr_execute_code()
0.001819 006981 - case OP_AND: // yr_execute_code()
0.001828 006981 - case OP_JFALSE: // yr_execute_code()
0.001839 006981 - case OP_PUSH_8: r1.i=4 // yr_execute_code()
0.001849 006981 - case OP_INT8: // yr_execute_code()
0.001856 006981 - _yr_get_first_block() {} = 0x7ffc0c7f9650 // default iterator; single memory block, blocking
0.001865 006981 - case OP_PUSH_8: r1.i=248 // yr_execute_code()
0.001876 006981 - case OP_PUSH_8: r1.i=131 // yr_execute_code()
0.001885 006981 - case OP_BITWISE_XOR: // yr_execute_code()
0.001892 006981 - case OP_INT_EQ: // yr_execute_code()
0.001899 006981 - case OP_AND: // yr_execute_code()
0.001906 006981 - case OP_JFALSE: // yr_execute_code()
0.001913 006981 - case OP_PUSH_8: r1.i=5 // yr_execute_code()
0.001922 006981 - case OP_INT8: // yr_execute_code()
0.001929 006981 - _yr_get_first_block() {} = 0x7ffc0c7f9650 // default iterator; single memory block, blocking
0.001937 006981 - case OP_PUSH_8: r1.i=154 // yr_execute_code()
0.001944 006981 - case OP_PUSH_8: r1.i=247 // yr_execute_code()
0.001952 006981 - case OP_BITWISE_XOR: // yr_execute_code()
0.001959 006981 - case OP_INT_EQ: // yr_execute_code()
0.001964 006981 - case OP_AND: // yr_execute_code()
0.001969 006981 - case OP_JFALSE: // yr_execute_code()
0.001974 006981 - case OP_JFALSE: // yr_execute_code()
0.001979 006981 - case OP_JFALSE: // yr_execute_code()
0.001983 006981 - case OP_JFALSE: // yr_execute_code()
0.001988 006981 - case OP_JFALSE: // yr_execute_code()
0.001993 006981 - case OP_JFALSE: // yr_execute_code()
0.001998 006981 - case OP_JFALSE: // yr_execute_code()
0.002003 006981 - case OP_JFALSE: // yr_execute_code()
0.002008 006981 - case OP_JFALSE: // yr_execute_code()
0.002013 006981 - case OP_JFALSE: // yr_execute_code()
0.002017 006981 - case OP_JFALSE: // yr_execute_code()
0.002022 006981 - case OP_JFALSE: // yr_execute_code()
0.002028 006981 - case OP_JFALSE: // yr_execute_code()
0.002033 006981 - case OP_JFALSE: // yr_execute_code()
0.002037 006981 - case OP_JFALSE: // yr_execute_code()
0.002042 006981 - case OP_JFALSE: // yr_execute_code()
0.002047 006981 - case OP_JFALSE: // yr_execute_code()
0.002051 006981 - case OP_JFALSE: // yr_execute_code()
0.002056 006981 - case OP_JFALSE: // yr_execute_code()
0.002061 006981 - case OP_JFALSE: // yr_execute_code()
0.002066 006981 - case OP_MATCH_RULE: // yr_execute_code()
0.002071 006981 - case OP_HALT: // yr_execute_code()
0.002093 006981 } = 0 AKA ERROR_SUCCESS 0 // yr_execute_code()
0.002108 006981 - _yr_scanner_clean_matches() {}
0.002122 006981 } = 0 AKA ERROR_SUCCESS 0 // yr_scanner_scan_mem_blocks()
0.002130 006981 } = 0 AKA ERROR_SUCCESS 0 // yr_scanner_scan_mem()
0.002146 006981 - yr_scanner_destroy() {}
0.002156 006981 + yr_finalize() {
0.002162 006981 - hash__finalize() {}
0.002167 006981 } // yr_finalize()
```



```
0.001604 006981 - case OP_PUSH_8: r1.i=95 // yr_execute_code()
0.001612 006981 - case OP_PUSH_8: r1.i=57 // yr_execute_code()
0.001619 006981 - case OP_BITWISE_XOR: // yr_execute_code()
$
0.001664 006981 - case OP_PUSH_8: r1.i=51 // yr_execute_code()
0.001671 006981 - case OP_PUSH_8: r1.i=95 // yr_execute_code()
0.001678 006981 - case OP_BITWISE_XOR: // yr_execute_code()

0.001729 006981 - case OP_PUSH_8: r1.i=248 // yr_execute_code()
0.001741 006981 - case OP_PUSH_8: r1.i=153 // yr_execute_code()
0.001745 006981 - case OP_BITWISE_XOR: // yr_execute_code()

0.001790 006981 - case OP_PUSH_8: r1.i=83 // yr_execute_code()
0.001799 006981 - case OP_PUSH_8: r1.i=52 // yr_execute_code()
0.001806 006981 - case OP_BITWISE_XOR: // yr_execute_code()

0.001865 006981 - case OP_PUSH_8: r1.i=248 // yr_execute_code()
0.001876 006981 - case OP_PUSH_8: r1.i=131 // yr_execute_code()
0.001885 006981 - case OP_BITWISE_XOR: // yr_execute_code()

0.001937 006981 - case OP_PUSH_8: r1.i=154 // yr_execute_code()
0.001944 006981 - case OP_PUSH_8: r1.i=247 // yr_execute_code()
0.001952 006981 - case OP_BITWISE_XOR: // yr_execute_code()
```



```
>>> chr(95 ^ 57)
'f'
>>> chr(51 ^ 95)
'l'
>>> chr(248 ^ 153)
'a'
>>> chr(83 ^ 52)
'g'
>>> chr(248 ^ 131)
'{'
>>> chr(154 ^ 247)
'm'
```



```
#!/bin/bash

# get these last 3 lines from the trace:
# 0.001937 006981 - case OP_PUSH_8: r1.i=154 // yr_execute_code()
# 0.001944 006981 - case OP_PUSH_8: r1.i=247 // yr_execute_code()
# 0.001952 006981 - case OP_BITWISE_XOR: // yr_execute_code()
#
# extract the 2 values (154 and 247), xor them and convert to char

get_next() {
 ./yara-4.2.3/yara -C flag.yarc test.txt 2>&1 | grep -B2 OP_BITWISE_XOR: | tail -3 \
 | sed -n 's/.*r1.i=\([0-9]*\).*$/\1/p' | xargs \
 | python -c "x,y=[int(_) for _ in input().split()]; print(chr(x^y), end='')" 2>/dev/null
}

rm -f test.txt

#
# get flag char by char
#
flag=""

for x in $(seq 32); do
 c="`get_next`"
 flag="${flag}${c}"
 echo $flag > test.txt
 cat test.txt
done
```



```
% sh bruteforce.sh

f
fl
fla
flag
flag{
flag{m
flag{m3
flag{m33
flag{m33t
flag{m33t_
flag{m33t_m
flag{m33t_me
flag{m33t_me_
flag{m33t_me_1
flag{m33t_me_1n
flag{m33t_me_1n_
flag{m33t_me_1n_7
flag{m33t_me_1n_7h
flag{m33t_me_1n_7h3
flag{m33t_me_1n_7h3_
flag{m33t_me_1n_7h3_a
flag{m33t_me_1n_7h3_ar
flag{m33t_me_1n_7h3_ar3
flag{m33t_me_1n_7h3_ar3n
flag{m33t_me_1n_7h3_ar3n4
flag{m33t_me_1n_7h3_ar3n4}
flag{m33t_me_1n_7h3_ar3n4}}
flag{m33t_me_1n_7h3_ar3n4}}}
flag{m33t_me_1n_7h3_ar3n4}}}}
flag{m33t_me_1n_7h3_ar3n4}}}}}
flag{m33t_me_1n_7h3_ar3n4}}}}}}
```
