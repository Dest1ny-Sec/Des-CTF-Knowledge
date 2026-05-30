# Realworld CTF 2023 Ferris_proxy

> 原文: https://www.ctfiot.com/106020.html
> ID: 106020

题目含有两个程序client和server以及一个包含flag传输的pcapng流量文件。打开题目一看，好消息是binary没去符号，坏消息是这是个rust。 用strace看了一下server端的监听端口是8888， 再打开pcapng看了一下，协议都是tcp，再上面一层的协议就只显示data了。 所以题目应该是要求我们逆向协议。

因为是有符号的，所以可以很轻松的找到main的函数。因为是协议，所以server和client的实现应该是对称的，这边以client端的为主进行分析。一打开client可以看到程序通过serde_yaml::de::
from_str::
h51d2279d81ebe645 读入了硬编码的rsa 密钥， client程序里硬编码的publickey实际上是server端的publickey，privatekey则是自己保存，和RSA公钥加密私钥解密的流程相符合。 所以协议某处肯定是用到了RSA加密方案。

继续往下看，程序在完成connect以后，有个lib::
protocol::
rc4::
Rc4$LT$T$C$V$GT$::
new::
h22d438f41ed76e26 的调用，而接下来跟着就是一个tokio::
task::
spawn的操作， 所以怀疑流量是经过了rc4加密，调试了一下发现加密密钥是explorer。因此可以从pcapng中把所有data取出来，分为server2client和client2server两个方向，各自使用rc4进行解密。可以得到如下的流量，含有明显是包头的12字节：

0000000800000000000000000000000800000000000000010000004800000001000000000100
1db2ee547837c2b0394f9316a3c672109c854769d9627ce715aa82ae76af4fc7d468903ffa4f
7c9d4afcf139528ceb24cb5f64a192287282ee7fd076992f000000480000000100000000e73f
0a730b98e032e90afaf73b8ddab1e821432c3e1c2c51396914f53fb304f26cbc8f85ec68462f
f85dfb0979648d43003291ccb9418e7b4016f5d3325d4083000000480000000100000000d44c
5aff410f28c841fb51c2e982244d7f7370fb6b73d6e5caba56c1b4b8f96bea190aa8d66e7e37
d76fe2e5fef7f78b0de90e12eefda3a36177583412ca074e00000048000000010000000096a1
796af867e440a72ee81e36e05f3b73c3341f6166b804bf83c3d0b47df74cc77405595ce44d3c
cfb739496b8acb78fdb02bcd510851b3e3de015fc06eadb40000000a00000001000000000f8e
0000004800000001000000010100320b119809b793abf357a7f78b0742ee93a957e563a5a94f
db09804e89596f2597a2cb9ae9f5161d5fda88ff050e47b1d28bebc6563465d2e7959e8a624a
000000480000000100000001cd39b2053c17021f93030e3b9bc7149ff5423faf64693932f76a
8dbffa526fff7c076845b1d31967efca0b56b066e8bacedc1927e629c6d0e87f61bf14ee3039
000000480000000100000001053d668ef1855426257ce68cdbc2f66919a2f9efbcb632daa617
0cb8246ab7a2348032f48cefdbc3aadcee6b9ab867371346bbe90fd69d213705ed1de38922b3
00000048000000010000000145bbbf8e0b10c5436e5974f46426d3efdbeaba819ea5d049bb42
0219a426336e14bc36e5753cb71fb21a2b78f699918a0045a8badddd69646ed65a59e17feec8
0000000a0000000100000001b30c000000280000000100000001503fdd267309866142ae96b3
197515b72ccd766dedbc09d61c25f0c3fa79ebd40000002800000001000000002accc966ccaf
48a147471171fb9589c95c561100d6548ad979f328e43bcfe0750000002c0000000100000000
0000001023a5457e1fa2e2f4a23242b1e61a597d1458bee4871e6f44e9296820014728300000
002c000000010000000100000010bd688bc8657972730f1d9a5c340cd555602957fa44cf6434
23bb23734bf8490b0000003c000000010000000000000020a6f95ec809bac678aa1f4a74a009
4e00d33e42da057331c95a61c6b5c3cd24daefeb367e01d3765e91643e37e2ac95e90000003c
000000010000000100000020184ff5940c47e4fc42a2bd1f61b304f5fdfc5e453104a3946d06
c4897a86f7d2872c948ff06b270b4d024446df8b60fa00000048000000010000000000000200
44f4cf64a905e470a2d8091e5320c0b8a370193fe44728340c454361c84578f3b469963d12fa
608ab96bf2e8c9c2116010d50e151b6407308d3cb6a2000000480000000100000000bc02026a
76b5be1d66cf03d90ea5303a5091b48d370ac186402138606da35c90fe7efb0a21f0a177896f
496ba40f02e079b82218be0124ab7de5d4f48cfd921e000000480000000100000000323d2847
d03880fa5cb48533939141115c3dc15fa32a82be59d78826e3d37f5cac12010ce10c850df636
26f94657a5beacf7d502b59fc10f571959ce6101b8d6000000480000000100000000704e541c
930ca3a8d156d7f6122fda7bbdffed9b9bc6160f4ec8ace48978bd458869a636a7d8798d7dbd
503e0c41aad82496578df4fbffbd3c5c885dc0bd3dee0000004800000001000000006d6af1ef
c82365f1619286e7a612155d87038f4ccb39e25e0660f9f2d320ae4321996b69187ba68abdf3
e6ab41abfa2dd359c7eaa5d344fc1acb97b58dd44d86000000480000000100000000d444d17c
165ee78e1d55f5c42b1f1bcf9c0f302588b68d26d2a308250c42d1df13be07693aa0f42cefcb
9dc1688216478a1a041c9a0c66308b3e4a5135fd2f0f0000004800000001000000002c7d9df8
1c7c9ccb7422089f94c0fa54067e6c4fc634c725c9aa9710aaedd671f72cf9287f38de6111ac
e6c0c32ed568569b45743abfc519e23aabccdf30a9af000000480000000100000000d1bbcab1
224daf8ccfb5e6dbf42ee924935b990eee7abe70ac5537426236e0ff1b2ac4748c665d3aba61
c4685798ae62126d89220cd5ae8c6a7c32e33ce1236d0000001c0000000100000000b802088e
5e303c8389880c09c3925053cc21082500000008000000020000000000000048000000010000
0001000001d06fe6d3c4b7761ffea3dea5ca1b75305f3bd828925e041baabc00aa51f93e5d59
aa6c5c024e1de93ccabbcc7736271de03665a2b170a42faca2e8699800000048000000010000
00016c6b50fecd4e0e1a9ca070fafa04c06a12f27af94d5430ccce129ada67c3040d444b7727
58195366025267bfea9e35cbaaf816022b34755d5ac2a4d7df85773200000048000000010000
0001ede0bf60b0ca23f40635dcbda76eaf3b59faa140dee0b2480aacd8df765ba5cfd1347f22
c9415006210eb4f224332b5cfcac7be98e0da94f74693d8af22e1fad00000048000000010000
00010614feada5c2aa494e61a0b2a848b82833860d6c1213c4aceebcbe55f419403ecd843835
f14f2caa8310be6bfad7ad2054df500a54268b17530183ef4c49f1c500000048000000010000
00011ed33f223e632356012a42484c1241d41ec5426ba94c0c4887a8206b86b41ac73ca8b79d
90256d391190bcb2256e881642c5a0fbc178691cf9ec983e1f1db40000000048000000010000
00012c5043530d28ce81e89c0a71baeb821ff0240d18fbac0e01b0952bb62b91354597b9061d
c440318ce3eabd95742607546c414ebf3da32879b2af3500d08cb4e900000048000000010000
0001b404a5293b85aadaa3d595d38992c219ddd7a4e5f00c09af477eea99477b3d53ac6b67c4
9f0cbd5a7ff038904dfc1a3b58cabe2c25dcb86fa55a53f3d362f0510000002c000000010000
000128bf591667dcd1d600abe1db48f49b17a5ad9d5650f7793af7a24341b771a9247f1eb480
0000000800000002000000010000000800000000000000020000000800000000000000030000
004800000001000000030100abcf924576de63087c8695ccda3705e8670c770f2bfda1dafded
dcd09b2aa6d485c6a87ff31c14300ddb660576ceed52047318a30d3c05c9848b0a1fb0530000
0048000000010000000387d378e9cbb8914e496a633595c7f68da097afd4fbd0380b4eafe790
ffe999b81ceeff32eea4d8fa4279606c7c491ec4eb4a7ef5bf614307c21bd3a314db9d2e0000
00480000000100000003e9f505f08c464e1f5f123bcc180305bb5a30f2c382493a1cc6d6e5e1
89e75950f75c8a790aef2c1fae18436c9d6f4840a9eacbf04139a2b25042c27f3a3fd7560000
00480000000100000003faeaff92d731e354d03dc46cbe8a001188dde35e753c259de3591816
78d94e47d90709345f6c9975288dbecfe1a6cf2eb7a14978854bbc73d3ac7d0a72cc3ef40000
000a0000000100000003c41a0000004800000001000000020100d92f41b75bb8ced6be2fbbc0
ba1cfeeebdf15826ce92ba78ef4cd0f6d47ff04e9e593cfc5fc7eac8109effce7e75f547873a
b559186885edf0e519f73aed00000048000000010000000243421e08dea79fd12889b2845ca3
65803bb4aa23c50d0c298e6649121b6d9101f32d15a043ffdbc93e7665617fa7b4b3f01db76f
5472c5aa3a085da5683efcc4000000480000000100000002bf9a240df9afc3596d4b3613ae9a
2184340561c896a60cc577e6ca507b5e6548ccfcd8bccf27de73deaaf04fab707a20c6aa94fe
bdf8a0a5532c0f4c73958e11000000480000000100000002fc1437567ccd886b5496cabb1179
93f31afe25f53d92721877892e472bf8bba1743b827e277f500d51b7f74f4682e943be0d3ebf
dc30742e211dc3eba51dac8b0000000a00000001000000029074000000280000000100000003
e836256016a5f8ca1e29732b7332d9776bdc6694a9df6c1172183f65916f83d50000002c0000
00010000000300000010f46cbf6896be858f5c2f86ee3c162359c545b1f5bd1eec0cd03e2b7b
f9c1b4b90000003c000000010000000300000020c580aa8aad81a2800fadf74749e79c323da6
5a6d11e8fb517d60ba36a0113b345be7c0fce390fba664776b676d82fdbe0000004800000001
00000003000002002292a593b68fdbf615d43c123747cf1f1583619708368b471b4a37c8eed2
1e07d14a7bf309f45335592134c5cc7a18152de20bb7d2fb753bee9131d90000004800000001
000000033076a9d57efa379e4f7f4700116d786c586b49523454dd9b3ae7cfde0416d9bfbb48
6eed31f88fec8128cd1e0bf783c8978c04fde5f1bbe67ecbe1c76e0596f50000004800000001
00000003579bbdb311093c2a3bb58b848be88302ab2bb6c24bf076a694de2b2fa1a8eff53fca
a6800e938bdeee831498fcc72cc9b822dad5b2074d5bc292c766e44c13e00000004800000001
0000000331fffa94345676f294eceb259baa51107267136af1e829868e1a3c5e2514517bfcfa
ec78783afde2874c6d2f4cb8436ed421e67fe327e8c67c851da9446ef2260000004800000001
00000003daff3194609bf5a05c1e6ec1e085854275ee81dbee01c92e2cb357faeba811424b80
bd9b204d70675aaf026f2f23bb0e882271bad34ff5294cc05cd7fc0740ac0000004800000001
000000034b5b49ca009d1836cfa176112aaf7775fa8c241bd45f861c1eec34dd2b9654e8144c
74c1f80c9e0f23cae4503ae85de975f74d250be667a1f6285c9951a8f8c90000004800000001
000000032fb4e2dd32d6fdd7e93fe24e23b9762099e1b12f5d9cae6dae7df3401e33931a8af6
5803c1538716bdba05948c8818f92791010ef8d6d315fb97bccdf2c2fbbf0000004800000001
00000003b97cd2e80a232dcf417da8ac1b835bf9dab15816bc1e2e0c07214e531ac922ca2f5d
dbb26f8d599805feb5f6ae1c6e3fe08ef5cf7dbd60eb407892d6e72a67a30000001c00000001
00000003e7d781f18b675dad11f1f49600057e8094628ad00000002800000001000000024ac9
c87b674dcd932d2e9d3a4b7c16a3989e750fa3a8895e8dd0971c56fb96780000002c00000001
0000000200000010cf6ca67cfe59cd5f110c1586de9c2186cfb7213784043ffb017fdf5cfa74
ac320000003c000000010000000200000020a03a82bae4627fc74de8c75437e5b077aa3d63e5
745f61f47362954b80f53ede6867267605b7383f55e6a80aefcae15300000008000000020000
0003

因为之前看到了RSA密钥，所以就在函数列表里搜了RSA，然后顺藤摸瓜到了key_exchange这个函数。除了rsa以外，还在函数列表里搜到了aes_128_cbc的字样。那么按照一般理解来说，这里应该是用rsa加密了aes的密钥作为key进行了key_exchange, 之后的流量就用aes进行对称加密了。

所以我们找一下两个关键的rsa_encrypt 和 rsa_decrypt 来看看key_exchange部分中，发出的数据和接收的数据怎么产生aes的密钥。

可以看到发出给对方的rsa加密数据是自己这边产生的随机数，而rsa解密出来的数据也是对方产生的随机数。之后的一系列zip，map等操作应该是执行了类似于python的map(lambda x, y: x + y, [1, 3, 5, 7, 9], [2, 4, 6, 8, 10]) 这种操作。但是因为不熟悉rust，所以找不到对应的操作函数。之后抄了一份官方样例自己编译了一份rust的binary，它的源码和binary如下：

fn main() { let a = vec![1,2,3]; let b = vec![2,3,4]; let c = a.into_iter().zip(b) .map(|(a,b)|a^b) .collect::<Vec<_>>();}

我发现rust同一个域下会生成一个map内的匿名函数，所以按着这个找题目程序里面应该也有。

因此可以知道，密钥是通过双方生成的随机数异或而成。

最后，还可以注意到decrypt之后，算出des密钥后有个sha256并进行发送的过程，在往下找代码的话还能看到：

说明应该是发送des密钥的sha256，让传输双方进行校验。

说句实话，包头的解析这部分猜的成分很大hhh， 当然其实小标题里那个函数里面应该都包括了程序解析数据包的逻辑，慢慢看也行。

总的来说就是包头由三个4byte的数据组成，分别代表length，action和streamid。其中action里0代表开启一个stream，1是传输，2对应关闭。

每个stream都要进行key exchange，也就是接下来的流量是rsa加密的aes密钥，加密后应该有256字节长，但是流量里有258字节，发现前两个字节恰好是0100，估计也是长度。再后面跟了一个aes密钥的sha256。最后就是aes加密的流量了。

aes加密的流量也有head，是一个4字节的代表数据长度的值，其后跟着一个16字节的当前加密所用的iv。因此可以直接进行aes_128_cbc解密。

附件因为大小限制只传了client，由于两边对称所以其实看一个也行。两个text文件为rc4解密后的hex数据。

from Crypto.Cipher import ARC4from Crypto.PublicKey import RSAfrom Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipherimport base64import binasciiimport pickle
def get_key(key_file): with open(key_file) as f: data = f.read() key = RSA.importKey(data) return key def decrypt_data(encrypt_msg:
bytes, private_key): cipher = PKCS1_cipher.new(private_key) back_text = cipher.decrypt(encrypt_msg, "connot decrypt.") return back_text c2s_key = get_key('s_private.pem')with open('dec_c2s.txt','r') as f: lines =f.readlines()d_lst = [b'',b'',b'',b'']for line in lines: i = 0 content = binascii.unhexlify(line.strip()) while i<len(content): legth = int.from_bytes(content[i:i+4],'big') dontknow = int.from_bytes(content[i+4:i+8],'big') streamid = int.from_bytes(content[i+8:i+12],'big') data = content[i+12:i+4+legth] d_lst[streamid] += data i += 4+legthprint(d_lst)dec = [[],[],[],[]]for j in range(len(d_lst)): enc = d_lst[j] i = 0 tmp = b'' while i<len(enc): if(enc[i:i+2]==b'x01x00'): if(tmp != b''): dec[j].append(tmp) tmp = decrypt_data(d_lst[j][i+2:i+258],c2s_key) dec[j].append(tmp) tmp = b'' i += 258 else: tmp += bytes([enc[i]]) i += 1 if(tmp != b''): dec[j].append(tmp)print()with open('c2s_aesenc.list','wb') as f: # [[stream0_aes_key1,keyhash+enced_data],...] pickle.dump(dec, f)

from Crypto.Cipher import AESfrom Crypto.Hash import SHA256import pickle with open('c2s_aesenc.list','rb') as f: c2s_data = pickle.load(f)with open('s2c_aesenc.list','rb') as f: s2c_data = pickle.load(f) def decrypt(data,key,iv): bs = AES.block_size # unpad = lambda s : s[0:-ord(s[-1])] cipher = AES.new(key, AES.MODE_CBC, iv) data = (cipher.decrypt(data)) return (data) for streamid in range(0,4): c2s_key = c2s_data[streamid][0] s2c_key = s2c_data[streamid][0] key = bytes([s2c_key[i] ^ c2s_key[i] for i in range(16)]) data = s2c_data[streamid][1] assert(data[0:32] == SHA256.new(key).digest()) i=32 while i < len(data): legth = int.from_bytes(data[i:i+4],'big') enc = data[i+4:i+4+legth] iv = data[i+4+legth:i+4+legth+16] print(streamid, decrypt(enc,key,iv)) i+= 4+legth+16 print(i,len(data)) print('--------------------------------------')for streamid in range(4): c2s_key = c2s_data[streamid][0] s2c_key = s2c_data[streamid][0] key = bytes([s2c_key[i] ^ c2s_key[i] for i in range(16)]) data = c2s_data[streamid][1] assert(data[0:32] == SHA256.new(key).digest()) i=32 while i < len(data): legth = int.from_bytes(data[i:i+4],'big') enc = data[i+4:i+4+legth] iv = data[i+4+legth:i+4+legth+16] print(streamid, decrypt(enc,key,iv)) i+= 4+legth+16

最后可以在解密结果中看到flag， 不过我感觉这个pcapng也是不全的，比较server2client部分没有截取到streamid==3时action==2的关闭请求。

0 b'x15xbf@;xe8Kx9exb0xd6x9fZ-xe4x9a}xc8'0 b'xe3x9ax0c/xf3x11.x05(Rxb6!xadxc6x8dx80'0 b'xe5x9cqfW?6xf2qx0exa5x84x0ex80(,HTTP/1.0 200 OKrnServer: SimpleHTTP/0.6 Python/3.6.9rnDate: Fri, 06 Jan 2023 18:16:47 GMTrnContent-type: text/html; charset=utf-8rnContent-Length: 338rnrn<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">n<html>n<head>n<meta http-equiv="Content-Type" content="text/html; charset=utf-8">n<title>Directory listing for /</title>n</head>nn<h1>Directory listing for /</h1>n<hr>nn<li>[flag.txt](flag.txt)</li>nn<hr>nn<html>n <head>n <meta http-equiv="Content-Type" content="text/html;charset=utf-8">n <title>Error response</title>n </head>n n <h1>Error response</h1>n Error code: 404n Message: File not found.n Error code explanation: HTTPStatus.NOT_FOUND - Nothing matches the given URI.n >();}
from Crypto.Cipher import ARC4from Crypto.PublicKey import RSAfrom Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipherimport base64import binasciiimport pickle
def get_key(key_file): with open(key_file) as f: data = f.read() key = RSA.importKey(data) return key def decrypt_data(encrypt_msg:
bytes, private_key): cipher = PKCS1_cipher.new(private_key) back_text = cipher.decrypt(encrypt_msg, "connot decrypt.") return back_text c2s_key = get_key('s_private.pem')with open('dec_c2s.txt','r') as f: lines =f.readlines()d_lst = [b'',b'',b'',b'']for line in lines: i = 0 content = binascii.unhexlify(line.strip()) while i<len(content): legth = int.from_bytes(content[i:i+4],'big') dontknow = int.from_bytes(content[i+4:i+8],'big') streamid = int.from_bytes(content[i+8:i+12],'big') data = content[i+12:i+4+legth] d_lst[streamid] += data i += 4+legthprint(d_lst)dec = [[],[],[],[]]for j in range(len(d_lst)): enc = d_lst[j] i = 0 tmp = b'' while i<len(enc): if(enc[i:i+2]==b'x01x00'): if(tmp != b''): dec[j].append(tmp) tmp = decrypt_data(d_lst[j][i+2:i+258],c2s_key) dec[j].append(tmp) tmp = b'' i += 258 else: tmp += bytes([enc[i]]) i += 1 if(tmp != b''): dec[j].append(tmp)print()with open('c2s_aesenc.list','wb') as f: # [[stream0_aes_key1,keyhash+enced_data],...] pickle.dump(dec, f)
from Crypto.Cipher import AESfrom Crypto.Hash import SHA256import pickle with open('c2s_aesenc.list','rb') as f: c2s_data = pickle.load(f)with open('s2c_aesenc.list','rb') as f: s2c_data = pickle.load(f) def decrypt(data,key,iv): bs = AES.block_size # unpad = lambda s : s[0:-ord(s[-1])] cipher = AES.new(key, AES.MODE_CBC, iv) data = (cipher.decrypt(data)) return (data) for streamid in range(0,4): c2s_key = c2s_data[streamid][0] s2c_key = s2c_data[streamid][0] key = bytes([s2c_key[i] ^ c2s_key[i] for i in range(16)]) data = s2c_data[streamid][1] assert(data[0:32] == SHA256.new(key).digest()) i=32 while i < len(data): legth = int.from_bytes(data[i:i+4],'big') enc = data[i+4:i+4+legth] iv = data[i+4+legth:i+4+legth+16] print(streamid, decrypt(enc,key,iv)) i+= 4+legth+16 print(i,len(data)) print('--------------------------------------')for streamid in range(4): c2s_key = c2s_data[streamid][0] s2c_key = s2c_data[streamid][0] key = bytes([s2c_key[i] ^ c2s_key[i] for i in range(16)]) data = c2s_data[streamid][1] assert(data[0:32] == SHA256.new(key).digest()) i=32 while i < len(data): legth = int.from_bytes(data[i:i+4],'big') enc = data[i+4:i+4+legth] iv = data[i+4+legth:i+4+legth+16] print(streamid, decrypt(enc,key,iv)) i+= 4+legth+16
0 b'x15xbf@;xe8Kx9exb0xd6x9fZ-xe4x9a}xc8'0 b'xe3x9ax0c/xf3x11.x05(Rxb6!xadxc6x8dx80'0 b'xe5x9cqfW?6xf2qx0exa5x84x0ex80(,HTTP/1.0 200 OKrnServer: SimpleHTTP/0.6 Python/3.6.9rnDate: Fri, 06 Jan 2023 18:16:47 GMTrnContent-type: text/html; charset=utf-8rnContent-Length: 338rnrn<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">n<html>n<head>n<meta http-equiv="Content-Type" content="text/html; charset=utf-8">n<title>Directory listing for /</title>n</head>nn<h1>Directory listing for /</h1>n<hr>nn<li>[flag.txt](flag.txt)</li>nn<hr>nn<html>n <head>n <meta http-equiv="Content-Type" content="text/html;charset=utf-8">n <title>Error response</title>n </head>n n <h1>Error response</h1>n Error code: 404n Message: File not found.n Error code explanation: HTTPStatus.NOT_FOUND - Nothing matches the given URI.n </b'780 7802 b'evxe5x1a=Gxb3bxaexa5xda2x9e5xb0x9c'2 b'x02jx8c$xbexc53mx0f#xce+xbax11xcbx03'104 1043 b'xa1{qxb2;xe4{bd)xe4(x81xd0xf01'3 b'xbaxc9xc6QGxa5;xf8xdc&xd6x1cx91I-L'3 b'%gxb8xf6xe7x13Px985x95#xc0(xdfxdex13HTTP/1.0 200 OKrnServer: SimpleHTTP/0.6 Python/3.6.9rnDate: Fri, 06 Jan 2023 18:16:49 GMTrnContent-type: text/plainrnContent-Length: 38rnLast-Modified: Fri, 06 Jan 2023 18:15:52 GMTrnrnrwctf{l1fe_1s_sh0rt_DO0'348 348
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/9-1680013627.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/4-1680013628.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/0-1680013628.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/1-1680013629.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/3-1680013629.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/10-1680013630.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/2-1680013630.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/9-1680013631.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/1-1680013632.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/7-1680013633.jpeg)