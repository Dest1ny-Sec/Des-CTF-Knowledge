---
title: DefCon REST-AND-ATTEST
contest: DEFCON 31 (Quals 2023)
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [rust, firmware, attestation, smart-lock, socat, uploader, trusted-firmware, reverse]
attack_chain:
  - socat tcp4-listen:4444 fork exec:./wrapper.sh
  - wrapper.sh exec ./uploader
  - 菜单: upload/download/run/quit
  - 读取trusted_firmware.raw include_bytes!
  - get_new_image() 用户上传image
  - do_download() image to hex print
  - run_device() 启动SFM+launcher
  - SFM Secure Firmware Module 固件证明
key_payload: get_new_image()? // user input image
one_liner: DEFCON 31 REST-AND-ATTEST：智能锁固件证明Rust程序
lesson: 固件证明（attestation）基于Root of Trust的固件安全
quality: high
---

# DefCon REST-AND-ATTEST

## 题目信息
- 比赛：DEFCON 31（Quals 2023）
- 题目：REST-AND-ATTEST
- 类别：Reverse / Web 混合
- 描述：NI Securable Products 智能锁 + Secure Firmware Module 固件证明

## 关键攻击链
### 1. 服务端
```sh
#!/bin/sh
# simulates challenge running in production environment
socat tcp4-listen:4444,reuseaddr,fork exec:"./wrapper.sh"

#!/bin/sh
# wrapper.sh
exec 3<&- 4<&-
exec ./uploader
```

### 2. Rust uploader
```rust
fn io_loop() -> Result<(), Box<dyn Error>> {
    let mut image = include_bytes!("trusted_firmware.raw").to_vec();
    loop {
        let mut line = String::new();
        print!("> ");
        stdout().flush()?;
        stdin().read_line(&mut line)?;
        let command = line.trim();
        if command == "upload" {
            image = get_new_image()?;  // user input image
        } else if command == "download" {
            do_download(&image)?;  // image to hex stdout print
        } else if command == "run" {
            run_device(&image)?;  // so launcher connect sfm
        } else if command == "quit" {
            break;
        }
    }
}
```

### 3. 关键功能
- `get_new_image()`：用户上传固件镜像
- `do_download()`：image 转 hex 输出
- `run_device()`：启动 SFM（Secure Firmware Module）
- SFM 与 launcher 通信，launcher 持有 image，sfm 接收并运行

### 4. 攻击思路
- 上传恶意固件镜像
- 让 SFM 验证恶意固件
- 绕过固件证明（attestation）

## 评分
- quality: high（Rust uploader 源码 + 智能锁固件证明场景 + 完整 socat 启动）
