#python3运行
from subprocess import *

def foo():
    stegoFile='flag.jpg'#隐写的图片
    extractFile='result.txt'#爆破的密码
    passFile='english.dic'#字典

    errors=['could not extract','steghide --help','Syntax error']
    cmdFormat='steghide extract -sf "%s" -xf "%s" -p "%s"'
    f=open(passFile,'r')

    for line in f.readlines():
        cmd=cmdFormat %(stegoFile,extractFile,line.strip())
        p=Popen(cmd,shell=True,stdout=PIPE,stderr=STDOUT)
        content=str(p.stdout.read(),'gbk')
        for err in errors:
            if err in content:
                break
        else:
            print (content),
            print ('the passphrase is %s' %(line.strip()))
            f.close()
            return

if __name__ == '__main__':
    foo()
    print ('ok')
    pass