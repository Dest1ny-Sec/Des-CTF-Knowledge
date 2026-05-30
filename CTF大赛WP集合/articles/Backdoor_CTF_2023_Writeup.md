# Backdoor CTF 2023 Writeup

> 原文: https://www.ctfiot.com/152665.html
> ID: 152665


```
$ exiftool friend.jpeg
ExifTool Version Number : 12.40
File Name : friend.jpeg
Directory : .
File Size : 6.3 KiB
File Modification Date/Time : 2023:12:16 20:26:01+00:00
File Access Date/Time : 2023:12:16 20:26:01+00:00
File Inode Change Date/Time : 2023:12:16 20:26:01+00:00
File Permissions : -rw-r--r--
File Type : JPEG
File Type Extension : jpg
MIME Type : image/jpeg
JFIF Version : 1.01
Exif Byte Order : Big-endian (Motorola, MM)
X Resolution : 1
Y Resolution : 1
Resolution Unit : None
Artist : flag{7h3_r34l_ctf_15_7h3_fr13nd5_w3_m4k3_al0ng}
Y Cb Cr Positioning : Centered
Image Width : 266
Image Height : 190
Encoding Process : Baseline DCT, Huffman coding
Bits Per Sample : 8
Color Components : 3
Y Cb Cr Sub Sampling : YCbCr4:2:0 (2 2)
Image Size : 266x190
Megapixels : 0.051
```



```
public class com.example.open_sesame.MainActivity extends androidx.appcompat.app.AppCompatActivity {
 /* .source "MainActivity.java" */
 /* # static fields */
 private static final valid_password;
 private static final java.lang.String valid_user;
 /* # instance fields */
 private android.widget.Button buttonLogin;
 private android.widget.EditText editTextPassword;
 private android.widget.EditText editTextUsername;
 /* # direct methods */
 static com.example.open_sesame.MainActivity ( ) {
 /* .locals 1 */
 int v0 = 7; // const/4 v0, 0x7
 /* new-array v0, v0, [I */
 /* fill-array-data v0, :array_0 */
 return;
 /* nop */
 /* :array_0 */
 /* .array-data 4 */
 /* 0x34 */
 /* 0x6c */
 /* 0x31 */
 /* 0x62 */
 /* 0x61 */
 /* 0x62 */
 /* 0x61 */
 } // .end array-data
} // .end method
public com.example.open_sesame.MainActivity ( ) {
 /* .locals 0 */
 /* .line 11 */
 /* invoke-direct {p0}, Landroidx/appcompat/app/AppCompatActivity;-><init>()V */
 return;
} // .end method
static void access$000 ( com.example.open_sesame.MainActivity p0 ) { //synthethic
 /* .locals 0 */
 /* .line 11 */
 /* invoke-direct {p0}, Lcom/example/open_sesame/MainActivity;->validateCredentials()V */
 return;
} // .end method

private java.lang.String flag ( java.lang.String p0, java.lang.String p1 ) {
 /* .locals 4 */
 /* .line 91 */
 /* new-instance v0, Ljava/lang/StringBuilder; */
 /* invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V */
 int v1 = 0; // const/4 v1, 0x0
 /* .line 92 */
} // :goto_0

v2 = (( java.lang.String ) p2 ).length ( ); // invoke-virtual {p2}, Ljava/lang/String;->length()I
/* if-ge v1, v2, :cond_0 */
/* .line 93 */
v2 = (( java.lang.String ) p2 ).charAt ( v1 ); // invoke-virtual {p2, v1}, Ljava/lang/String;->charAt(I)C
v3 = (( java.lang.String ) p1 ).length ( ); // invoke-virtual {p1}, Ljava/lang/String;->length()I
/* rem-int v3, v1, v3 */
v3 = (( java.lang.String ) p1 ).charAt ( v3 ); // invoke-virtual {p1, v3}, Ljava/lang/String;->charAt(I)C
/* xor-int/2addr v2, v3 */
/* int-to-char v2, v2 */
/* .line 94 */
(( java.lang.StringBuilder ) v0 ).append ( v2 ); // invoke-virtual {v0, v2}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;
/* add-int/lit8 v1, v1, 0x1 */
/* .line 96 */
} // :cond_0
(( java.lang.StringBuilder ) v0 ).toString ( ); // invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
} // .end method
private it4chi ( java.lang.String p0 ) {
	/* .locals 3 */
	/* .line 68 */
	v0 = (( java.lang.String ) p1 ).length ( ); // invoke-virtual {p1}, Ljava/lang/String;->length()I
	/* new-array v0, v0, [I */
	int 
	v1 = 0; // const/4 v1, 0x0
	/* .line 69 */
	} // :goto_0
	v2 = (( java.lang.String ) p1 ).length ( ); // invoke-virtual {p1}, Ljava/lang/String;->length()I
	/* if-ge v1, v2, :cond_0 */
	/* .line 70 */
	v2 = (( java.lang.String ) p1 ).charAt ( v1 ); // invoke-virtual {p1, v1}, Ljava/lang/String;->charAt(I)C
	/* aput v2, v0, v1 */
	/* add-int/lit8 v1, v1, 0x1 */
	} // :cond_0
} // .end method

private Boolean n4ut1lus ( java.lang.String p0 ) {
	/* .locals 4 */
	/* .line 54 */
	/* invoke-direct {p0, p1}, Lcom/example/open_sesame/MainActivity;->it4chi(Ljava/lang/String;)[I */
	/* .line 55 */
	/* array-length v0, p1 */
	v1 = com.example.open_sesame.MainActivity.valid_password;
	/* array-length v1, v1 */
	int v2 = 0; // const/4 v2, 0x0
	/* if-eq v0, v1, :cond_0 */
} // :cond_0

/* move v0, v2 */
/* .line 59 */
} // :goto_0
/* array-length v1, p1 */
/* if-ge v0, v1, :cond_2 */
/* .line 60 */
/* aget v1, p1, v0 */
v3 = com.example.open_sesame.MainActivity.valid_password;
/* aget v3, v3, v0 */
/* if-eq v1, v3, :cond_1 */
} // :cond_1
/* add-int/lit8 v0, v0, 0x1 */
} // :cond_2
int p1 = 1; // const/4 p1, 0x1
} // .end method

private java.lang.String sh4dy ( java.lang.String p0 ) {
	/* .locals 4 */
	/* .line 76 */
	/* new-instance v0, Ljava/lang/StringBuilder; */
	/* invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V */
	int v1 = 0; // const/4 v1, 0x0
	/* .line 78 */
} // :goto_0

v2 = (( java.lang.String ) p1 ).length ( ); // invoke-virtual {p1}, Ljava/lang/String;->length()I
/* if-ge v1, v2, :cond_1 */
/* .line 79 */
v2 = (( java.lang.String ) p1 ).charAt ( v1 ); // invoke-virtual {p1, v1}, Ljava/lang/String;->charAt(I)C
/* .line 80 */
v3 = java.lang.Character .isDigit ( v2 );
if ( v3 != null) { // if-eqz v3, :cond_0
/* .line 81 */
(( java.lang.StringBuilder ) v0 ).append ( v2 ); // invoke-virtual {v0, v2}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;
} // :cond_0
/* add-int/lit8 v1, v1, 0x1 */
/* .line 84 */
} // :cond_1
(( java.lang.StringBuilder ) v0 ).toString ( ); // invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
} // .end method
private void showToast ( java.lang.String p0 ) {
/* .locals 1 */
int v0 = 0; // const/4 v0, 0x0
	/* .line 100 */
	android.widget.Toast .makeText ( p0,p1,v0 );
	(( android.widget.Toast ) p1 ).show ( ); // invoke-virtual {p1}, Landroid/widget/Toast;->show()V
	return;
} // .end method
private Integer sl4y3r ( java.lang.String p0 ) {
	/* .locals 0 */
	/* .line 87 */
	p1 = java.lang.Integer .parseInt ( p1 );
	/* add-int/lit8 p1, p1, -0x1 */
} // .end method

private void validateCredentials ( ) {
	/* .locals 3 */
	v0 = this.editTextUsername;
	/* .line 38 */
	(( android.widget.EditText ) v0 ).getText ( ); // invoke-virtual {v0}, Landroid/widget/EditText;->getText()Landroid/text/Editable;
	(( java.lang.Object ) v0 ).toString ( ); // invoke-virtual {v0}, Ljava/lang/Object;->toString()Ljava/lang/String;
	(( java.lang.String ) v0 ).trim ( ); // invoke-virtual {v0}, Ljava/lang/String;->trim()Ljava/lang/String;
	
	v1 = this.editTextPassword;
	/* .line 39 */
	(( android.widget.EditText ) v1 ).getText ( ); // invoke-virtual {v1}, Landroid/widget/EditText;->getText()Landroid/text/Editable;
	(( java.lang.Object ) v1 ).toString ( ); // invoke-virtual {v1}, Ljava/lang/Object;->toString()Ljava/lang/String;
	(( java.lang.String ) v1 ).trim ( ); // invoke-virtual {v1}, Ljava/lang/String;->trim()Ljava/lang/String;
	final String v2 = "Jack Ma"; // const-string v2, "Jack Ma"

 /* .line 41 */
	v0 = (( java.lang.String ) v0 ).equals ( v2 ); // invoke-virtual {v0, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

	if ( v0 != null) { // if-eqz v0, :cond_0
	v0 = /* invoke-direct {p0, v1}, Lcom/example/open_sesame/MainActivity;->n4ut1lus(Ljava/lang/String;)Z */
	}

	if ( v0 != null) { // if-eqz v0, :cond_0
 /* .line 42 */
 // 4l1baba から数字の抽出？
 /* invoke-direct {p0, v1}, Lcom/example/open_sesame/MainActivity;->sh4dy(Ljava/lang/String;)Ljava/lang/String; */
 /* .line 43 */

 v0 = /* invoke-direct {p0, v0}, Lcom/example/open_sesame/MainActivity;->sl4y3r(Ljava/lang/String;)I */
 /* .line 45 */
 
 /* new-instance v1, Ljava/lang/StringBuilder; */
 final String v2 = "flag{"; // const-string v2, "flag{"
 /* invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V */

 java.lang.Integer .toString ( v0 );
 final String v2 = "U|]rURuoU^PoR_FDMo@X]uBUg"; // const-string v2, "U|]rURuoU^PoR_FDMo@X]uBUg"

 /* invoke-direct {p0, v0, v2}, Lcom/example/open_sesame/MainActivity;->flag(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String; */ 
 (( java.lang.StringBuilder ) v1 ).append ( v0 ); // invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
 final String v1 = "}"; // const-string v1, "}"
 (( java.lang.StringBuilder ) v0 ).append ( v1 ); // invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
 (( java.lang.StringBuilder ) v0 ).toString ( ); // invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
	} // :cond_0

	final String v0 = "Invalid credentials.Please try again."; // const-string v0, "Invalid credentials.Please try again."
	/* .line 49 */
	/* invoke-direct {p0, v0}, Lcom/example/open_sesame/MainActivity;->showToast(Ljava/lang/String;)V */
	} // :goto_0
	return;
} // .end method
/* # virtual methods */
protected void onCreate ( android.os.Bundle p0 ) {
/* .locals 1 */
/* .line 22 */
/* invoke-super {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->onCreate(Landroid/os/Bundle;)V */
/* .line 23 */
(( com.example.open_sesame.MainActivity ) p0 ).setContentView ( p1 ); // invoke-virtual {p0, p1}, Lcom/example/open_sesame/MainActivity;->setContentView(I)V
/* .line 25 */
(( com.example.open_sesame.MainActivity ) p0 ).findViewById ( p1 ); // invoke-virtual {p0, p1}, Lcom/example/open_sesame/MainActivity;->findViewById(I)Landroid/view/View;
/* check-cast p1, Landroid/widget/EditText; */
this.editTextUsername = p1;
/* .line 26 */
(( com.example.open_sesame.MainActivity ) p0 ).findViewById ( p1 ); // invoke-virtual {p0, p1}, Lcom/example/open_sesame/MainActivity;->findViewById(I)Landroid/view/View;
/* check-cast p1, Landroid/widget/EditText; */
this.editTextPassword = p1;
/* .line 27 */
(( com.example.open_sesame.MainActivity ) p0 ).findViewById ( p1 ); // invoke-virtual {p0, p1}, Lcom/example/open_sesame/MainActivity;->findViewById(I)Landroid/view/View;
/* check-cast p1, Landroid/widget/Button; */
this.buttonLogin = p1;
/* .line 29 */
/* new-instance v0, Lcom/example/open_sesame/MainActivity$1; */
/* invoke-direct {v0, p0}, Lcom/example/open_sesame/MainActivity$1;-><init>(Lcom/example/open_sesame/MainActivity;)V */
(( android.widget.Button ) p1 ).setOnClickListener ( v0 ); // invoke-virtual {p1, v0}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V
return;
} // .end method
```



```
local_20 = *(long *)(in_FS_OFFSET + 0x28);
if (param_1 != 2) {
std::operator<<((basic_ostream *)std::cout,"Just try to get the door");
/* WARNING: Subroutine does not return */
exit(0);
}

sVar2 = strlen(*(char **)(param_2 + 8));
if (sVar2 != 0x11) {
std::operator<<((basic_ostream *)std::cout,"that\'s not even a door :p");
/* WARNING: Subroutine does not return */
exit(0);
}
```



```
local_f4 = 0;
std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string();
local_68 = 0x42;
local_64 = 0x77;
local_60 = 0x65;
local_5c = 0x71;
local_58 = 0x7b;
local_54 = 0x62;
local_50 = 0x72;
local_4c = 0x7d;
local_48 = 0x77;
local_44 = 0x59;
local_40 = 0x73;
local_3c = 0x7d;
local_38 = 0x6f;
local_34 = 0x6d;
local_30 = 0x3e;
local_2c = 1;
local_28 = 0;
for (; local_f4 < 0x11; local_f4 = local_f4 + 1) {
 /* try { // try from 00102fa1 to 00102fa5 has its CatchHandler @ 00103183 */
 /* } // end try from 00102fa1 to 00102fa5 */
std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::push_back
 ((char)local_e8);
}
std::allocator<char>::allocator();
 /* try { // try from 00102fe0 to 00102fe4 has its CatchHandler @ 00103126 */
 /* } // end try from 00102fe0 to 00102fe4 */
std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::
basic_string<std::allocator<char>>(local_c8,"ThatsHardcoded!!!",&local_f5);
std::allocator<char>::~allocator((allocator<char> *)&local_f5);
 /* try { // try from 00103005 to 00103009 has its CatchHandler @ 0010316b */
 /* } // end try from 00103005 to 00103009 */
std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string
 (local_88);
 /* try { // try from 0010301e to 00103022 has its CatchHandler @ 00103156 */
 /* } // end try from 0010301e to 00103022 */
std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string
 (local_a8);
 /* try { // try from 00103034 to 00103038 has its CatchHandler @ 0010313e */
 /* } // end try from 00103034 to 00103038 */
func_5(SUB81(local_a8,0),SUB81(local_88,0));
std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string
 ((basic_string<char,std::char_traits<char>,std::allocator<char>> *)local_a8);
std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string
 ((basic_string<char,std::char_traits<char>,std::allocator<char>> *)local_88);
 /* try { // try from 00103059 to 001030ed has its CatchHandler @ 0010316b */
local_f0 = (int *)operator.new[](0x44);
piVar3 = (int *)func_4(local_e8,*(char **)(param_2 + 8));
local_f0 = (int *)func_3(piVar3,(basic_string *)local_c8);
cVar1 = func_2(local_f0);
if (cVar1 == '\0') {
 func_1(*local_f0,local_f0[0x10]);
}
else {
 /* } // end try from 00103059 to 001030ed */
 std::operator<<((basic_ostream *)std::cout,"Wrong door");
}
```



```
basic_string<std::allocator<char>>(local_448,"encoded.bin",local_468);
std::allocator<char>::~allocator((allocator<char> *)local_468);
 /* try { // try from 0010276b to 0010276f has its CatchHandler @ 001029a5 */
 /* } // end try from 0010276b to 0010276f */
std::basic_ifstream<char,std::char_traits<char>>::basic_ifstream

***

for (local_48c = 0; (int)local_48c < 0x16086; local_48c = local_48c + 1) {
if ((local_48c & 1) == 0) {
 pbVar1 = (byte *)std::vector<char,std::allocator<char>>::operator[]
 ((vector<char,std::allocator<char>> *)local_468,
 (long)(int)local_48c);
 *pbVar1 = *pbVar1 ^ (byte)param_1;
}
else {
 pbVar1 = (byte *)std::vector<char,std::allocator<char>>::operator[]
 ((vector<char,std::allocator<char>> *)local_468,
 (long)(int)local_48c);
 *pbVar1 = *pbVar1 ^ (byte)param_2;
}
}
```
