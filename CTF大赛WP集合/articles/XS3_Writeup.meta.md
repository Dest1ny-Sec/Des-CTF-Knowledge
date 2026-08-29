---
title: XS3 Writeup (AWS Cognito + S3 + Web 攻击链)
contest: Ricotecki CTF (XS3)
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [s3_presigned_url, content_type_filter_bypass, xss_cookie_steal, cognito_id_token, aws_get_credentials_for_identity, s3_special_flag_bucket, s3_sync_download, js_blob_url_xss, content_type_toLowerCase_trim, deny_mime_subtypes]
attack_chain: 1) S3 预签名 URL + createPresignedPost content-length-range 0-100MB + starts-with $Content-Type 'image' + 内置 denyMimeSubTypes 过滤 html/javascript/xml/json/svg/xhtml/xsl / 2) bypass:contentType text/html;x=image/png → endsWith('image/png') 命中但 S3 仍存储 text/html / 3) 注入 XSS:window.parent.document.cookie 跨域读 parent / 4) Cognito IdentityPool 凭据链:get-id → get-credentials-for-identity → 临时 AccessKeyId/SecretKey/SessionToken → aws s3 ls → specialflagbucket-5250c0a74f-adv3-special-flag → s3 sync 下载 flag.txt
key_payload: {"contentType":"text/html;x=image/png"} / 17 关渐进式 contentType 过滤 / aws cognito-identity get-id --identity-pool-id ap-northeast-1:05611045-eb46-41e2-9f6c-f41d87547e4d --logins {ISS}={IDTOKEN}
one_liner: XS3 (ricotecki) 17 关 S3 contentType 过滤 bypass + Cognito Identity Pool 临时凭据 + s3 sync 拉 specialflagbucket 完整攻击链，覆盖 endsWith/startsWith/includes/RegExp/数组等多种过滤。
lesson: S3 starts-with $Content-Type 'image' 是早期常见过滤漏洞，可通过 ;parameter 注入绕过；Cognito Identity Pool 是 AWS 临时凭据颁发的低门槛入口。
quality: high
---
