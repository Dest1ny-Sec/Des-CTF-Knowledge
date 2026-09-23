---
title: 使用docker调试和部署pwn题
contest: Docker PWN 调试部署
year: 2024
difficulty: easy
vuln_type: misc_unknown
tags:
- Dockerfile
- ubuntu
- pwndbg
- gef
- pwntools
- pwncli
- one_gadget
- seccomp-tools
- xinetd
- socat
- SYS_PTRACE
- --privileged
attack_chain:
- '调试环境: docker run -it --rm -v host:container -p port --cap-add=SYS_PTRACE IMAGE'
- --cap-add=SYS_PTRACE 允许 gdb 附加进程
- --privileged 给全部权限 (绕过 seccomp/apparmor)
- '完整 Dockerfile: ubuntu + python3+pwntools+pwncli + gdb+pwndbg+gef+Pwngdb'
- 'apt install: xinetd gdb gdbserver gcc ruby gem one_gadget seccomp-tools'
- gem install one_gadget + gem install seccomp-tools
- pip3 install pwntools pwncli ropper capstone z3-solver qiling lief
- 创建 ctf 普通用户 NOPASSWD ALL sudo
- oh-my-zsh + zsh-syntax-highlighting + zsh-autosuggestions
- '出题模板: xinetd (传统) 或 socat (新式)'
- 'update.sh: apt install + pwntools + gef 一键安装'
key_payload: '''docker run -it --rm --cap-add=SYS_PTRACE IMAGE + xinetd/socat 出题'''
one_liner: Docker 调试部署 PWN 题标准模板：ubuntu + pwndbg/gef + pwntools + one_gadget + seccomp-tools + xinetd/socat。
lesson: --cap-add=SYS_PTRACE 必备让 gdb 附加；--privileged 给全部权限 (绕过 docker seccomp) 才能 seccomp-tools dump；出题用 socat 比 xinetd 更现代。
quality: medium
full_path: 使用docker调试和部署pwn题.full.md
meta_path: 使用docker调试和部署pwn题.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '使用docker调试和部署pwn题。Docker 调试部署 PWN 题标准模板：ubuntu + pwndbg/gef + pwntools + one_gadget + seccomp-tools + xinetd/socat。。关键路径：调试环境: docker run -it --rm -v host:container -p port --cap-add=SYS_PTRACE IMA...'
category: misc
subcategory: misc_other
tools_used:
- GDB
- Python
- Z3
- pwntools
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/154995.html
reasoning_chain:
- pwn 题调试部署需要 docker → 触发点：环境隔离 + 镜像复用
- 动作：docker run -it --rm -v host:container -p port --cap-add=SYS_PTRACE IMAGE
- 假设：--cap-add=SYS_PTRACE 允许 gdb 附加进程 → --privileged 给全部权限绕过 seccomp
- '完整 Dockerfile: ubuntu + python3+pwntools+pwncli + gdb+pwndbg+gef+Pwngdb'
- 'apt install: xinetd gdb gdbserver gcc ruby gem one_gadget seccomp-tools'
- 假设：gem install one_gadget + gem install seccomp-tools → pip3 install pwntools pwncli ropper capstone z3-solver
- 创建 ctf 普通用户 NOPASSWD ALL sudo → oh-my-zsh + zsh 插件
- '出题模板: xinetd (传统) 或 socat (新式) → update.sh 一键安装'
failed_attempts:
- 试图不用 SYS_PTRACE 调 gdb → 失败：docker 默认禁 ptrace
- 试图用 docker 默认 seccomp 跑 seccomp-tools → 失败：被拦截
- 试图用 root 出题 → 失败：权限过大不安全
key_observations:
- --cap-add=SYS_PTRACE 必备让 gdb 附加
- --privileged 给全部权限 (绕过 docker seccomp) 才能 seccomp-tools dump
- 出题用 socat 比 xinetd 更现代
- Dockerfile ARG DEBIAN_FRONTEND=noninteractive 避免 tzdata 阻塞
prerequisites:
- Docker 基础（run/build/volume/port）
- Linux capability (SYS_PTRACE)
- xinetd/socat 出题模板配置
- pwntools/pwndbg 安装与配置
---
# 使用docker调试和部署pwn题

> 原文: https://www.ctfiot.com/154995.html
> ID: 154995

主要内容如下：

一

调试环境

docker run -it --rm -v host_path:
container_path -p host_port:
container_port --cap-add=SYS_PTRACE IMAGE_ID # auto update

docker run -it -rm -v host_path:
container_path -p host_port:
container_port --cap-add=SYS_PTRACE IMAGE_ID /bin/bash # do not update

docker run -it --rm -v host_path:
container_path -p host_port:
container_port --privileged IMAGE_ID # privileged enabled and auto update

ARG BUILD_VERSION

FROM ubuntu:$BUILD_VERSION

ARG DEBIAN_FRONTEND=noninteractive
ARG HUB_DOMAIN=github.com
ARG NORMAL_USER_NAME=ctf

ENV TZ=Etc/UTC
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

WORKDIR /root

RUN apt-get update && apt-get -y dist-upgrade && apt-get install -y --fix-missing python3 python3-pip python3-dev lib32z1
 xinetd curl gcc gdb gdbserver g++ git libssl-dev libffi-dev build-essential tmux
 vim iputils-ping gdb-multiarch
 file net-tools socat ruby ruby-dev locales autoconf automake libtool make &&
 gem install one_gadget &&
 gem install seccomp-tools &&
 sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen

# 先执行容易失败的操作
RUN git clone https://${HUB_DOMAIN}/pwndbg/pwndbg &&
 cd ./pwndbg &&
 ./setup.sh

RUN git clone https://${HUB_DOMAIN}/NixOS/patchelf.git &&
 cd ./patchelf &&
 ./bootstrap.sh &&
 ./configure &&
 make &&
 make install

RUN git clone https://${HUB_DOMAIN}/hugsy/gef.git &&
 git clone https://${HUB_DOMAIN}/RoderickChan/Pwngdb.git &&
 git clone https://${HUB_DOMAIN}/Gallopsled/pwntools &&
 (mv /usr/lib/python3.11/EXTERNALLY-MANAGED /usr/lib/python3.11/EXTERNALLY-MANAGED.old || true) &&
 pip3 install --upgrade --editable ./pwntools &&
 git clone https://${HUB_DOMAIN}/RoderickChan/pwncli.git &&
 pip3 install --upgrade --editable ./pwncli

COPY ./gdb-gef /bin
COPY ./gdb-pwndbg /bin
COPY ./update.sh /bin
COPY ./test-this-container.sh /bin
COPY ./.tmux.conf ./
COPY ./.gdbinit ./
COPY ./flag /
COPY ./flag /flag.txt

RUN chmod +x /bin/gdb-gef /bin/gdb-pwndbg /bin/update.sh /bin/test-this-container.sh &&
 echo "root:
root" | chpasswd &&
 python3 -m pip install --upgrade pip &&
 pip3 install ropper capstone z3-solver qiling lief

# normal user
RUN useradd ${NORMAL_USER_NAME} -d /home/${NORMAL_USER_NAME} -m -s /bin/bash -u 1001 &&
 echo "${NORMAL_USER_NAME}:${NORMAL_USER_NAME}" | chpasswd &&
 cp -r /root/pwndbg /home/${NORMAL_USER_NAME} &&
 cp -r /root/gef /home/${NORMAL_USER_NAME} &&
 cp -r /root/pwntools /home/${NORMAL_USER_NAME} &&
 cp -r /root/Pwngdb /home/${NORMAL_USER_NAME} &&
 cp -r /root/pwncli /home/${NORMAL_USER_NAME} &&

 cp /root/.tmux.conf /home/${NORMAL_USER_NAME} &&
 cp /root/.gdbinit /home/${NORMAL_USER_NAME} &&
 cp /flag /home/${NORMAL_USER_NAME} &&
 cp /flag.txt /home/${NORMAL_USER_NAME} &&
 chown -R ${NORMAL_USER_NAME}:${NORMAL_USER_NAME} /home/${NORMAL_USER_NAME}

USER ${NORMAL_USER_NAME}:${NORMAL_USER_NAME}

WORKDIR /home/${NORMAL_USER_NAME}

RUN pip3 install --upgrade --editable ./pwntools &&
 pip3 install --upgrade --editable ./pwncli

# switch to root and install zsh
USER root:
root
RUN apt-get install -y sudo zsh &&
 echo "${NORMAL_USER_NAME} ALL=(ALL) NOPASSWD : ALL" | tee /etc/sudoers.d/ctfsudo

# switch 2 normal user
USER ${NORMAL_USER_NAME}:${NORMAL_USER_NAME}
WORKDIR /home/${NORMAL_USER_NAME}

# install zsh
RUN curl -fsSL -O https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh &&
 chmod +x ./install.sh &&
 sed -i -e 's/read[[:
space:]]*-r[[:
space:]]*opt/opt=n/g' ./install.sh &&
 ./install.sh &&
 git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting &&
 git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

COPY ./.zshrc ./

# expose some ports
EXPOSE 20 21 22 80 443 23946 10001 10002 10003 10004 10005

CMD ["/bin/update.sh"]

#!/bin/bash

set -ex

apt update && apt install -y tmux gdb gdbserver wget rpm file binutils socat python3 python3-pip procps

# 修改tmux配置
cat > ~/.tmux.conf << "EOF"
set -g prefix C-a #
unbind C-b # C-b即Ctrl+b键，unbind意味着解除绑定
bind C-a send-prefix # 绑定Ctrl+a为新的指令前缀

# 从tmux v1.6版起，支持设置第二个指令前缀
set-option -g prefix2 ` # 设置一个不常用的`键作为指令前缀，按键更快些
#set-option -g mouse on # 开启鼠标支持
# 修改分屏快捷键
unbind '"'
bind - splitw -v -c '#{pane_current_path}' # 垂直方向新增面板，默认进入当前目录
unbind %
bind | splitw -h -c '#{pane_current_path}' # 水平方向新增面板，默认进入当前目录

# 设置面板大小调整快捷键
bind j resize-pane -D 10
bind k resize-pane -U 10
bind h resize-pane -L 10
bind l resize-pane -R 10
EOF

# 安装pwntools和pwncli
pip3 install pwntools pwncli
bash -c "$(wget https://gef.blah.cat/sh -O -)"

#!/bin/bash

dnf install -y tmux gdb gdb-gdbserver wget which file binutils socat python3 python3-pip procps

cat > ~/.tmux.conf << "EOF"
set -g prefix C-a #
unbind C-b # C-b即Ctrl+b键，unbind意味着解除绑定
bind C-a send-prefix # 绑定Ctrl+a为新的指令前缀

# 从tmux v1.6版起，支持设置第二个指令前缀
set-option -g prefix2 ` # 设置一个不常用的`键作为指令前缀，按键更快些
#set-option -g mouse on # 开启鼠标支持
# 修改分屏快捷键
unbind '"'
bind - splitw -v -c '#{pane_current_path}' # 垂直方向新增面板，默认进入当前目录
unbind %
bind | splitw -h -c '#{pane_current_path}' # 水平方向新增面板，默认进入当前目录

# 设置面板大小调整快捷键
bind j resize-pane -D 10
bind k resize-pane -U 10
bind h resize-pane -L 10
bind l resize-pane -R 10
EOF

pip3 install pwntools pwncli
bash -c "$(wget https://gef.blah.cat/sh -O -)"

二

出题模板

三

使用技巧

看雪ID：roderick01

https://bbs.kanxue.com/user-home-956675.htm

*本文为看雪论坛优秀文章，由 roderick01 原创，转载请注明来自看雪社区

# 往期推荐

1、区块链智能合约逆向-合约创建-调用执行流程分析

2、在Windows平台使用VS2022的MSVC编译LLVM16

3、神挡杀神——揭开世界第一手游保护nProtect的神秘面纱

4、为什么在ASLR机制下DLL文件在不同进程中加载的基址相同

5、2022QWB final RDP

6、华为杯研究生国赛 adv_lua

球分享

球点赞

球在看


```
一
调试环境
docker run -it --rm -v host_path:
container_path -p host_port:
container_port --cap-add=SYS_PTRACE IMAGE_ID # auto update

docker run -it -rm -v host_path:
container_path -p host_port:
container_port --cap-add=SYS_PTRACE IMAGE_ID /bin/bash # do not update

docker run -it --rm -v host_path:
container_path -p host_port:
container_port --privileged IMAGE_ID # privileged enabled and auto update
ARG BUILD_VERSION

FROM ubuntu:$BUILD_VERSION

ARG DEBIAN_FRONTEND=noninteractive
ARG HUB_DOMAIN=github.com
ARG NORMAL_USER_NAME=ctf

ENV TZ=Etc/UTC
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

WORKDIR /root

RUN apt-get update && apt-get -y dist-upgrade && apt-get install -y --fix-missing python3 python3-pip python3-dev lib32z1
 xinetd curl gcc gdb gdbserver g++ git libssl-dev libffi-dev build-essential tmux
 vim iputils-ping gdb-multiarch
 file net-tools socat ruby ruby-dev locales autoconf automake libtool make &&
 gem install one_gadget &&
 gem install seccomp-tools &&
 sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen

# 先执行容易失败的操作
RUN git clone https://${HUB_DOMAIN}/pwndbg/pwndbg &&
 cd ./pwndbg &&
 ./setup.sh

RUN git clone https://${HUB_DOMAIN}/NixOS/patchelf.git &&
 cd ./patchelf &&
 ./bootstrap.sh &&
 ./configure &&
 make &&
 make install

RUN git clone https://${HUB_DOMAIN}/hugsy/gef.git &&
 git clone https://${HUB_DOMAIN}/RoderickChan/Pwngdb.git &&
 git clone https://${HUB_DOMAIN}/Gallopsled/pwntools &&
 (mv /usr/lib/python3.11/EXTERNALLY-MANAGED /usr/lib/python3.11/EXTERNALLY-MANAGED.old || true) &&
 pip3 install --upgrade --editable ./pwntools &&
 git clone https://${HUB_DOMAIN}/RoderickChan/pwncli.git &&
 pip3 install --upgrade --editable ./pwncli

COPY ./gdb-gef /bin
COPY ./gdb-pwndbg /bin
COPY ./update.sh /bin
COPY ./test-this-container.sh /bin
COPY ./.tmux.conf ./
COPY ./.gdbinit ./
COPY ./flag /
COPY ./flag /flag.txt

RUN chmod +x /bin/gdb-gef /bin/gdb-pwndbg /bin/update.sh /bin/test-this-container.sh &&
 echo "root:
root" | chpasswd &&
 python3 -m pip install --upgrade pip &&
 pip3 install ropper capstone z3-solver qiling lief

# normal user
RUN useradd ${NORMAL_USER_NAME} -d /home/${NORMAL_USER_NAME} -m -s /bin/bash -u 1001 &&
 echo "${NORMAL_USER_NAME}:${NORMAL_USER_NAME}" | chpasswd &&
 cp -r /root/pwndbg /home/${NORMAL_USER_NAME} &&
 cp -r /root/gef /home/${NORMAL_USER_NAME} &&
 cp -r /root/pwntools /home/${NORMAL_USER_NAME} &&
 cp -r /root/Pwngdb /home/${NORMAL_USER_NAME} &&
 cp -r /root/pwncli /home/${NORMAL_USER_NAME} &&

 cp /root/.tmux.conf /home/${NORMAL_USER_NAME} &&
 cp /root/.gdbinit /home/${NORMAL_USER_NAME} &&
 cp /flag /home/${NORMAL_USER_NAME} &&
 cp /flag.txt /home/${NORMAL_USER_NAME} &&
 chown -R ${NORMAL_USER_NAME}:${NORMAL_USER_NAME} /home/${NORMAL_USER_NAME}

USER ${NORMAL_USER_NAME}:${NORMAL_USER_NAME}

WORKDIR /home/${NORMAL_USER_NAME}

RUN pip3 install --upgrade --editable ./pwntools &&
 pip3 install --upgrade --editable ./pwncli

# switch to root and install zsh
USER root:
root
RUN apt-get install -y sudo zsh &&
 echo "${NORMAL_USER_NAME} ALL=(ALL) NOPASSWD : ALL" | tee /etc/sudoers.d/ctfsudo

# switch 2 normal user
USER ${NORMAL_USER_NAME}:${NORMAL_USER_NAME}
WORKDIR /home/${NORMAL_USER_NAME}

# install zsh
RUN curl -fsSL -O https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh &&
 chmod +x ./install.sh &&
 sed -i -e 's/read[[:
space:]]*-r[[:
space:]]*opt/opt=n/g' ./install.sh &&
 ./install.sh &&
 git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting &&
 git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

COPY ./.zshrc ./

# expose some ports
EXPOSE 20 21 22 80 443 23946 10001 10002 10003 10004 10005

CMD ["/bin/update.sh"]
#!/bin/bash

set -ex

apt update && apt install -y tmux gdb gdbserver wget rpm file binutils socat python3 python3-pip procps

# 修改tmux配置
cat > ~/.tmux.conf << "EOF"
set -g prefix C-a #
unbind C-b # C-b即Ctrl+b键，unbind意味着解除绑定
bind C-a send-prefix # 绑定Ctrl+a为新的指令前缀

# 从tmux v1.6版起，支持设置第二个指令前缀
set-option -g prefix2 ` # 设置一个不常用的`键作为指令前缀，按键更快些
    #set-option -g mouse on # 开启鼠标支持
# 修改分屏快捷键
unbind '"'
bind - splitw -v -c '#{pane_current_path}' # 垂直方向新增面板，默认进入当前目录
unbind %
bind | splitw -h -c '#{pane_current_path}' # 水平方向新增面板，默认进入当前目录

# 设置面板大小调整快捷键
bind j resize-pane -D 10
bind k resize-pane -U 10
bind h resize-pane -L 10
bind l resize-pane -R 10
EOF

# 安装pwntools和pwncli
pip3 install pwntools pwncli
bash -c "$(wget https://gef.blah.cat/sh -O -)"
#!/bin/bash

dnf install -y tmux gdb gdb-gdbserver wget which file binutils socat python3 python3-pip procps

cat > ~/.tmux.conf << "EOF"
set -g prefix C-a #
unbind C-b # C-b即Ctrl+b键，unbind意味着解除绑定
bind C-a send-prefix # 绑定Ctrl+a为新的指令前缀

# 从tmux v1.6版起，支持设置第二个指令前缀
set-option -g prefix2 ` # 设置一个不常用的`键作为指令前缀，按键更快些
    #set-option -g mouse on # 开启鼠标支持
# 修改分屏快捷键
unbind '"'
bind - splitw -v -c '#{pane_current_path}' # 垂直方向新增面板，默认进入当前目录
unbind %
bind | splitw -h -c '#{pane_current_path}' # 水平方向新增面板，默认进入当前目录

# 设置面板大小调整快捷键
bind j resize-pane -D 10
bind k resize-pane -U 10
bind h resize-pane -L 10
bind l resize-pane -R 10
EOF

pip3 install pwntools pwncli
bash -c "$(wget https://gef.blah.cat/sh -O -)"
二
出题模板
三
使用技巧
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]