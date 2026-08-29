---
title: 使用docker调试和部署pwn题
contest: Docker PWN 调试部署
year: 2024
difficulty: easy
vuln_type: misc_unknown
tags: [Dockerfile, ubuntu, pwndbg, gef, pwntools, pwncli, one_gadget, seccomp-tools, xinetd, socat, SYS_PTRACE, --privileged]
attack_chain:
  - 调试环境: docker run -it --rm -v host:container -p port --cap-add=SYS_PTRACE IMAGE
  - --cap-add=SYS_PTRACE 允许 gdb 附加进程
  - --privileged 给全部权限 (绕过 seccomp/apparmor)
  - 完整 Dockerfile: ubuntu + python3+pwntools+pwncli + gdb+pwndbg+gef+Pwngdb
  - apt install: xinetd gdb gdbserver gcc ruby gem one_gadget seccomp-tools
  - gem install one_gadget + gem install seccomp-tools
  - pip3 install pwntools pwncli ropper capstone z3-solver qiling lief
  - 创建 ctf 普通用户 NOPASSWD ALL sudo
  - oh-my-zsh + zsh-syntax-highlighting + zsh-autosuggestions
  - 出题模板: xinetd (传统) 或 socat (新式)
  - update.sh: apt install + pwntools + gef 一键安装
key_payload: 'docker run -it --rm --cap-add=SYS_PTRACE IMAGE + xinetd/socat 出题'
one_liner: Docker 调试部署 PWN 题标准模板：ubuntu + pwndbg/gef + pwntools + one_gadget + seccomp-tools + xinetd/socat。
lesson: --cap-add=SYS_PTRACE 必备让 gdb 附加；--privileged 给全部权限 (绕过 docker seccomp) 才能 seccomp-tools dump；出题用 socat 比 xinetd 更现代。
quality: medium
---

# 使用docker调试和部署pwn题

## 概览
- **来源**: 看雪 roderick01
- **类型**: Docker PWN 调试部署模板
- **难度**: ⭐⭐

## 调试环境 (3 种模式)

### 1. 普通模式 + auto update
```bash
docker run -it --rm \
  -v host_path:container_path \
  -p host_port:container_port \
  --cap-add=SYS_PTRACE \
  IMAGE_ID
```

### 2. 固定版本模式
```bash
docker run -it --rm \
  -v host_path:container_path \
  -p host_port:container_port \
  --cap-add=SYS_PTRACE \
  IMAGE_ID /bin/bash
```

### 3. 特权模式 (绕过 seccomp)
```bash
docker run -it --rm \
  -v host_path:container_path \
  -p host_port:container_port \
  --privileged \
  IMAGE_ID
```

## 完整 Dockerfile
```dockerfile
ARG BUILD_VERSION
FROM ubuntu:$BUILD_VERSION

ARG DEBIAN_FRONTEND=noninteractive
ARG HUB_DOMAIN=github.com
ARG NORMAL_USER_NAME=ctf

ENV TZ=Etc/UTC LANG=en_US.UTF-8

WORKDIR /root

RUN apt-get update && apt-get install -y \
  python3 python3-pip python3-dev lib32z1 \
  xinetd curl gcc gdb gdbserver g++ git libssl-dev libffi-dev \
  build-essential tmux vim iputils-ping gdb-multiarch \
  file net-tools socat ruby ruby-dev locales autoconf automake libtool make && \
  gem install one_gadget && gem install seccomp-tools && \
  sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen

# pwndbg
RUN git clone https://${HUB_DOMAIN}/pwndbg/pwndbg && \
    cd ./pwndbg && ./setup.sh

# patchelf
RUN git clone https://${HUB_DOMAIN}/NixOS/patchelf.git && \
    cd ./patchelf && ./bootstrap.sh && ./configure && make && make install

# gef + Pwngdb + pwntools + pwncli
RUN git clone https://${HUB_DOMAIN}/hugsy/gef.git && \
    git clone https://${HUB_DOMAIN}/RoderickChan/Pwngdb.git && \
    git clone https://${HUB_DOMAIN}/Gallopsled/pwntools && \
    pip3 install --upgrade --editable ./pwntools && \
    git clone https://${HUB_DOMAIN}/RoderickChan/pwncli.git && \
    pip3 install --upgrade --editable ./pwncli

COPY ./gdb-gef /bin
COPY ./gdb-pwndbg /bin
COPY ./update.sh /bin
COPY ./test-this-container.sh /bin
COPY ./.tmux.conf ./
COPY ./.gdbinit ./
COPY ./flag /

RUN pip3 install ropper capstone z3-solver qiling lief

# 普通用户
RUN useradd ${NORMAL_USER_NAME} -d /home/${NORMAL_USER_NAME} -m -s /bin/bash -u 1001 && \
    echo "${NORMAL_USER_NAME}:${NORMAL_USER_NAME}" | chpasswd && \
    cp -r /root/pwndbg /root/gef /root/pwntools /root/Pwngdb /root/pwncli /home/${NORMAL_USER_NAME}/ && \
    cp /root/.tmux.conf /root/.gdbinit /home/${NORMAL_USER_NAME}/ && \
    chown -R ${NORMAL_USER_NAME}:${NORMAL_USER_NAME} /home/${NORMAL_USER_NAME}

USER ${NORMAL_USER_NAME}:${NORMAL_USER_NAME}
WORKDIR /home/${NORMAL_USER_NAME}

USER root:root
RUN apt-get install -y sudo zsh && \
    echo "${NORMAL_USER_NAME} ALL=(ALL) NOPASSWD:ALL" | tee /etc/sudoers.d/ctfsudo

USER ${NORMAL_USER_NAME}:${NORMAL_USER_NAME}
RUN bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended && \
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/ && \
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/

EXPOSE 20 21 22 80 443 23946 10001-10005
CMD ["/bin/update.sh"]
```

## update.sh (Debian/Ubuntu)
```bash
#!/bin/bash
set -ex
apt update && apt install -y tmux gdb gdbserver wget rpm file binutils \
  socat python3 python3-pip procps

# tmux 配置 (Ctrl-a 前缀)
cat > ~/.tmux.conf << "EOF"
set -g prefix C-a
unbind C-b
bind C-a send-prefix
set-option -g prefix2 `
unbind '"'
bind - splitw -v -c '#{pane_current_path}'
unbind %
bind | splitw -h -c '#{pane_current_path}'
bind j resize-pane -D 10
bind k resize-pane -U 10
bind h resize-pane -L 10
bind l resize-pane -R 10
EOF

pip3 install pwntools pwncli
bash -c "$(wget https://gef.blah.cat/sh -O -)"
```

## 出题模板

### xinetd 传统
```conf
service ctf
{
    disable = no
    socket_type = stream
    protocol = tcp
    wait = no
    user = ctf
    server = /home/ctf/run.sh
    type = UNLISTED
    port = 9999
}
```

### socat 现代
```bash
socat tcp-l:9999,reuseaddr,fork EXEC:./pwn
```

## 关键点
- `--cap-add=SYS_PTRACE` 必备 (否则 gdb 报错)
- `--privileged` 给全部权限 (绕过 docker 默认 seccomp)
- one_gadget/seccomp-tools 通过 gem 安装
- 普通用户 + sudo NOPASSWD 容器内调试
