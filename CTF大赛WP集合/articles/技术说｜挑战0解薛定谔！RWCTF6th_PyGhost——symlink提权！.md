# 技术说｜挑战0解薛定谔！RWCTF6th PyGhost——symlink提权！

> 原文: https://www.ctfiot.com/169214.html
> ID: 169214

先

听我说

1、题目蕴藏某组件历史漏洞，如何在不了解该漏洞的情况下做出分析，进而利用？

2、Windows操作系统特性的考察也是本题的一道关卡。解题过程中，需要利用一些windows的文件操作相关特性来完成，不熟悉或不了解该领域的相关知识，都将造成难以通关的局面。

话不多说，开始挑战它！

正文揭晓

01

背景

This is an LPE(Local Privilege Escalation) challenge. Your task is to pop a highly-privileged(nt authoritysystem) cmd.exe as a low-privileged user. Follow these steps to deploy the challenge locally:

download and install the virtual machine from: https://developer.microsoft.com/en-us/windows/downloads/virtual-machines/

execute the installer (installer.exe in the attachment) as Administrator

the installer will set up the vulnerable component. You can then attempt to find the vulnerability and exploit it

Notes about the demo:

Send your exploit archive file to email and DM on Discord when you’re ready. Meanwhile, the email should also contains your team name and team token

You can choose to demo your exploit publicly or privately, according to your preference. If you choose to demo publicly, the entire process will be visible to everyone, so remember to remove sensitive information. If you choose to demo privately, we will set up a private discord channel that only includes the admin and your team members

Our demo VM is slightly configured, including:

a. Windows Defender is disabled. You don’t have to contend with it.

b. A standard user(not in the Administrator group, with the username being ctf) is created for demo purposes. We will run your exploit in the context of the standard user.

If your exploit needs multiple steps, please batch them in a single file. We will only execute one of your files and then wait for the result without more user interaction

I will not accept more than 3 emails per team. If you really need more, you will need to explain to me in detail why you messed up your first 3 tries and convince me that you deserve a 4th chance.

The running time for each try cannot exceed 3 minutes.

I will reward you with the flag if the highly-privileged cmd.exe pops up.

02

题目分析

```pythonimport socketimport win32serviceutilimport servicemanagerimport win32eventimport win32serviceimport win32pipeimport win32securityimport win32fileimport pywintypesimport randomimport matplotlib.pyplot as pltimport numpy as npimport osimport sysimport shutil

class SMWinservice(win32serviceutil.ServiceFramework): _svc_name_ = "RWCTF" _svc_display_name_ = 'try to hack me' _svc_description_ = ''
 @classmethod def parse_command_line(cls): if len(sys.argv) == 1: servicemanager.Initialize() servicemanager.PrepareToHostSingle() servicemanager.StartServiceCtrlDispatcher() win32serviceutil.HandleCommandLine(cls) else: win32serviceutil.HandleCommandLine(cls) def __init__(self, args): win32serviceutil.ServiceFramework.__init__(self, args) self.hWaitStop = win32event.CreateEvent(None, 0, 0, None) socket.setdefaulttimeout(60) def SvcStop(self): self.stop() self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING) win32event.SetEvent(self.hWaitStop) def SvcDoRun(self): self.start() servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, self._svc_name_) self.main() def start(self): pass def stop(self): pass def main(self): pass

class RWCTFService(SMWinservice): __qualname__ = 'RWCTFService' _svc_name_ = 'RWCTF' _svc_display_name_ = 'try to hack me' _svc_description_ = ''
 def start(self): self.LICENSE = 'n The Star And Thank Author License (SATA)n Version 2.0, April 2021nnCopyright <2024> <RWCTF>(info@realworldctf.com)nnProject Url: https://realworldctf.com/nnPermission is hereby granted, free of charge, to any person obtaining a copynof this software and associated documentation files (the "Software"), to dealnin the Software without restriction, including without limitation the rightsnto use, copy, modify, merge, publish, distribute, sublicense, and/or sellncopies of the Software, and to permit persons to whom the Software isnfurnished to do so, subject to the following conditions:
nnThe above copyright notice and this permission notice shall be included innall copies or substantial portions of the Software.nnAnd wait, the most important, you should star/+1/like the project(s) in project urlnsection above first, and then thank the author(s) in Copyright section.nnHere are some suggested ways:nn - Email the authors a thank-you letter, and make friends with him/her/them.n - Report bugs or issues.n - Tell friends what a wonderful project this is.n - And, sure, you can just express thanks in your mind without telling the world.nnContributors of this project by forking have the option to add his/her name andnforked project url at copyright and project url sections, but shall not deletenor modify anything else in these two sections.nnTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS ORnIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THEnAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHERnLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS INnTHE SOFTWARE.n' self.output_directory = 'C:\Windows\Temp' self.output_prefix = 'C:\Windows\Temp\res.' self.isrunning = True def stop(self): try: self.isrunning = False 
except FileNotFoundError: self.isrunning = False 
except: raise def challenge(self, option, key): RAND_32_64 = lambda: random.randint(32, 64) nonce = '' if option == b'png': nonce = random.getrandbits(RAND_32_64()) + 1 elif option == b'jpg': nonce = random.getrandbits(RAND_32_64()) * 2 elif option == b'eps': nonce = random.getrandbits(RAND_32_64()) + 4660 elif option == b'svg': nonce = random.getrandbits(RAND_32_64()) - 61769 elif option == b'pgf': nonce = random.getrandbits(RAND_32_64()) % random.getrandbits(RAND_32_64()) elif option == b'pdf': nonce = random.getrandbits(RAND_32_64()) // random.getrantbits(random.randint(2, 10)) else: return False if key == nonce: return True else: return False def loop(self, pipeHandle, data): RAND_0_100 = lambda: random.randint(0, 100) pieces = data.split(b'|') option = pieces[1] key = int(pieces[2]) if option == b'png': if self.challenge(option, key): x = np.linspace(0, 10, 200) plt.plot(x, np.sin(x)) plt.plot(x, np.cos(x)) plt.savefig(self.output_prefix + str(RAND_0_100()) + '.png') return None elif option == b'jpg': if self.challenge(option, key): l = [1, 2, 3, 4] plt.plot(l) plt.ylabel('some number') plt.savefig(self.output_prefix + str(RAND_0_100()) + '.jpg') return None elif option == b'svg': if self.challenge(option, key): x = ['A', 'B', 'C', 'D'] y = [3, 8, 1, 10] plt.bar(x, y) plt.savefig(self.output_prefix + str(RAND_0_100()) + '.svg') return None elif option == b'pdf': if self.challenge(option, key): x = [1, 2, 3, 4, 5] y = [1, 4, 9, 16, 25] plt.figure() plt.plot(x, y) plt.title('My first matplotlib plot') plt.xlabel('X') plt.ylabel('Y') plt.savefig(self.output_prefix + str(RAND_0_100()) + '.pdf') return None elif option == b'LICENSE': win32file.WriteFile(pipeHandle, 'Please read the LICENSE carefully: n' + self.LICENSE) return None elif option == b'I give up': pipeHandle.Close() self.stop() return None else: return 0 """ 通过反汇编能看出有这段，但是 try catch 的位置还没确认怎么放，不过这个影响不大 try: 
except Exception as e: servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, str(e))) e = None del e else: e = None del e """ def main(self): while self.isrunning: pipeName = '\\.\pipe\rwctf' openMode = win32pipe.PIPE_ACCESS_DUPLEX | win32file.FILE_FLAG_OVERLAPPED pipeMode = win32pipe.PIPE_TYPE_MESSAGE ACL = 'D:(A;;GA;;;SY)(A;;GA;;;BA)(A;;GA;;;AU)' sd = win32security.ConvertStringSecurityDescriptorToSecurityDescriptor(ACL, win32security.SDDL_REVISION_1) sa = pywintypes.SECURITY_ATTRIBUTES() sa.SECURITY_DESCRIPTOR = sd pipeHandle = win32pipe.CreateNamedPipe( pipeName, openMode, pipeMode, win32pipe.PIPE_UNLIMITED_INSTANCES, 0, 0, 6000, sa) # !!! 待检查 while self.isrunning: hr = win32pipe.ConnectNamedPipe(pipeHandle, None) hr, data = win32file.ReadFile(pipeHandle, 256) self.loop(pipeHandle, data) win32pipe.DisconnectNamedPipe(pipeHandle) """ 整个结构应该是包含在 while 里面的 同样也有一个 try-catch 虽然不确定位置但是影响不大 while self.isrunning: # ... while self.isrunning: # ... return None try: 
except Exception as details: NULL + print('Error connecting pipe!', details) pipeHandle.NULL | self + Close() details = None del details continue else: details = None del details """
if __name__ == "__main__": RWCTFService.parse_command_line()```

03

Pyinstaller 漏洞分析

def _rmtree_unsafe(path, onexc): try: with os.scandir(path) as scandir_it: entries = list(scandir_it) 
except OSError as err: onexc(os.scandir, path, err) entries = [] for entry in entries: fullname = entry.path try: is_dir = entry.is_dir(follow_symlinks=False) 
except OSError: is_dir = False
 if is_dir and not entry.is_junction(): try: if entry.is_symlink(): # This can only happen if someone replaces # a directory with a symlink after the call to # os.scandir or entry.is_dir above. raise OSError("Cannot call rmtree on a symbolic link") 
except OSError as err: onexc(os.path.islink, fullname, err) continue _rmtree_unsafe(fullname, onexc) else: try: os.unlink(fullname) 
except OSError as err: onexc(os.unlink, fullname, err) try: os.rmdir(path) 
except OSError as err: onexc(os.rmdir, path, err)

04

总结

END

点击卡片👇  get本期征稿详情


```
```pythonimport socketimport win32serviceutilimport servicemanagerimport win32eventimport win32serviceimport win32pipeimport win32securityimport win32fileimport pywintypesimport randomimport matplotlib.pyplot as pltimport numpy as npimport osimport sysimport shutil

class SMWinservice(win32serviceutil.ServiceFramework): _svc_name_ = "RWCTF" _svc_display_name_ = 'try to hack me' _svc_description_ = ''
 @classmethod def parse_command_line(cls): if len(sys.argv) == 1: servicemanager.Initialize() servicemanager.PrepareToHostSingle() servicemanager.StartServiceCtrlDispatcher() win32serviceutil.HandleCommandLine(cls) else: win32serviceutil.HandleCommandLine(cls) def __init__(self, args): win32serviceutil.ServiceFramework.__init__(self, args) self.hWaitStop = win32event.CreateEvent(None, 0, 0, None) socket.setdefaulttimeout(60) def SvcStop(self): self.stop() self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING) win32event.SetEvent(self.hWaitStop) def SvcDoRun(self): self.start() servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, self._svc_name_) self.main() def start(self): pass def stop(self): pass def main(self): pass

class RWCTFService(SMWinservice): __qualname__ = 'RWCTFService' _svc_name_ = 'RWCTF' _svc_display_name_ = 'try to hack me' _svc_description_ = ''
 def start(self): self.LICENSE = 'n The Star And Thank Author License (SATA)n Version 2.0, April 2021nnCopyright <2024> <RWCTF>(info@realworldctf.com)nnProject Url: https://realworldctf.com/nnPermission is hereby granted, free of charge, to any person obtaining a copynof this software and associated documentation files (the "Software"), to dealnin the Software without restriction, including without limitation the rightsnto use, copy, modify, merge, publish, distribute, sublicense, and/or sellncopies of the Software, and to permit persons to whom the Software isnfurnished to do so, subject to the following conditions:
nnThe above copyright notice and this permission notice shall be included innall copies or substantial portions of the Software.nnAnd wait, the most important, you should star/+1/like the project(s) in project urlnsection above first, and then thank the author(s) in Copyright section.nnHere are some suggested ways:nn - Email the authors a thank-you letter, and make friends with him/her/them.n - Report bugs or issues.n - Tell friends what a wonderful project this is.n - And, sure, you can just express thanks in your mind without telling the world.nnContributors of this project by forking have the option to add his/her name andnforked project url at copyright and project url sections, but shall not deletenor modify anything else in these two sections.nnTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS ORnIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THEnAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHERnLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS INnTHE SOFTWARE.n' self.output_directory = 'C:\Windows\Temp' self.output_prefix = 'C:\Windows\Temp\res.' self.isrunning = True def stop(self): try: self.isrunning = False 
except FileNotFoundError: self.isrunning = False 
except: raise def challenge(self, option, key): RAND_32_64 = lambda: random.randint(32, 64) nonce = '' if option == b'png': nonce = random.getrandbits(RAND_32_64()) + 1 elif option == b'jpg': nonce = random.getrandbits(RAND_32_64()) * 2 elif option == b'eps': nonce = random.getrandbits(RAND_32_64()) + 4660 elif option == b'svg': nonce = random.getrandbits(RAND_32_64()) - 61769 elif option == b'pgf': nonce = random.getrandbits(RAND_32_64()) % random.getrandbits(RAND_32_64()) elif option == b'pdf': nonce = random.getrandbits(RAND_32_64()) // random.getrantbits(random.randint(2, 10)) else: return False if key == nonce: return True else: return False def loop(self, pipeHandle, data): RAND_0_100 = lambda: random.randint(0, 100) pieces = data.split(b'|') option = pieces[1] key = int(pieces[2]) if option == b'png': if self.challenge(option, key): x = np.linspace(0, 10, 200) plt.plot(x, np.sin(x)) plt.plot(x, np.cos(x)) plt.savefig(self.output_prefix + str(RAND_0_100()) + '.png') return None elif option == b'jpg': if self.challenge(option, key): l = [1, 2, 3, 4] plt.plot(l) plt.ylabel('some number') plt.savefig(self.output_prefix + str(RAND_0_100()) + '.jpg') return None elif option == b'svg': if self.challenge(option, key): x = ['A', 'B', 'C', 'D'] y = [3, 8, 1, 10] plt.bar(x, y) plt.savefig(self.output_prefix + str(RAND_0_100()) + '.svg') return None elif option == b'pdf': if self.challenge(option, key): x = [1, 2, 3, 4, 5] y = [1, 4, 9, 16, 25] plt.figure() plt.plot(x, y) plt.title('My first matplotlib plot') plt.xlabel('X') plt.ylabel('Y') plt.savefig(self.output_prefix + str(RAND_0_100()) + '.pdf') return None elif option == b'LICENSE': win32file.WriteFile(pipeHandle, 'Please read the LICENSE carefully: n' + self.LICENSE) return None elif option == b'I give up': pipeHandle.Close() self.stop() return None else: return 0 """ 通过反汇编能看出有这段，但是 try catch 的位置还没确认怎么放，不过这个影响不大 try: 
except Exception as e: servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, str(e))) e = None del e else: e = None del e """ def main(self): while self.isrunning: pipeName = '\\.\pipe\rwctf' openMode = win32pipe.PIPE_ACCESS_DUPLEX | win32file.FILE_FLAG_OVERLAPPED pipeMode = win32pipe.PIPE_TYPE_MESSAGE ACL = 'D:(A;;GA;;;SY)(A;;GA;;;BA)(A;;GA;;;AU)' sd = win32security.ConvertStringSecurityDescriptorToSecurityDescriptor(ACL, win32security.SDDL_REVISION_1) sa = pywintypes.SECURITY_ATTRIBUTES() sa.SECURITY_DESCRIPTOR = sd pipeHandle = win32pipe.CreateNamedPipe( pipeName, openMode, pipeMode, win32pipe.PIPE_UNLIMITED_INSTANCES, 0, 0, 6000, sa) # !!! 待检查 while self.isrunning: hr = win32pipe.ConnectNamedPipe(pipeHandle, None) hr, data = win32file.ReadFile(pipeHandle, 256) self.loop(pipeHandle, data) win32pipe.DisconnectNamedPipe(pipeHandle) """ 整个结构应该是包含在 while 里面的 同样也有一个 try-catch 虽然不确定位置但是影响不大 while self.isrunning: # ... while self.isrunning: # ... return None try: 
except Exception as details: NULL + print('Error connecting pipe!', details) pipeHandle.NULL | self + Close() details = None del details continue else: details = None del details """
if __name__ == "__main__": RWCTFService.parse_command_line()```
def _rmtree_unsafe(path, onexc): try: with os.scandir(path) as scandir_it: entries = list(scandir_it) 
except OSError as err: onexc(os.scandir, path, err) entries = [] for entry in entries: fullname = entry.path try: is_dir = entry.is_dir(follow_symlinks=False) 
except OSError: is_dir = False
 if is_dir and not entry.is_junction(): try: if entry.is_symlink(): # This can only happen if someone replaces # a directory with a symlink after the call to # os.scandir or entry.is_dir above. raise OSError("Cannot call rmtree on a symbolic link") 
except OSError as err: onexc(os.path.islink, fullname, err) continue _rmtree_unsafe(fullname, onexc) else: try: os.unlink(fullname) 
except OSError as err: onexc(os.unlink, fullname, err) try: os.rmdir(path) 
except OSError as err: onexc(os.rmdir, path, err)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/7-1711087600.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/10-1711087602.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/1-1711087603.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/7-1711087603.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/10-1711087603.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/5-1711087604.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/5-1711087604.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/2-1711087604.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/6-1711087605.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/3-1711087605.png)