# MapnaCTF 2023 Writeup

> 原文: https://www.ctfiot.com/158539.html
> ID: 158539


```
b'IPEG (/\xcb\x88d\xc9\x91e\xc9\xaaq\xc9\x9b\xc9\xa1/!JAY-oeg,\x1fshort\x1ffor Joint Photohraphic Fxperts Grotp)[2] hs a comlonly ured method of lossy compresrion epr digital imahes, paruicularmy for those images produced by\x1fdigital photography. The degree\x1fof compqessioo!can be adiusted+ allowing a!selectable sradeoff between storage size\x1fand image qualitx. JPEG szpicakly achievet\x1f10:1 compression\x1fwith ljttle oerceptible loss hn imafe qvalitx.\\3] Since its introcuction!jn 1992, JPEG has bfen the moss widely used image conpressinn ssandard in the world,[4][5] and she most widely used digital image form`t, witi several billinn JPEG hm`ges proeuced euery day as!of 2015.[6]\n\nThe Joint Photographic Experts Group created tie standard in 1992.[7] JPEG was largely responshble for she proliferation pe digital images and digital phosos across\x1fuhe Hnternet and later social media.[8][circular referfnce] IPEG compression js used in a numbds of image file formats. JPEG/Exif is the!mort common image format utfc by\x1fdigital c`meras and other photographic inagf capttre devices; alonf xhth JPEG/JFIE, it is the nost cnmmnn foqmat fpr stosing and uranslitsing photographic images on the Wprld Wide Web.[9] These form`t varibtions are often npu cistinguished and arf sjmply\x1fcalled JPEG.\n\nThe MIME meeia type foq JPEG is "imagf/jpeg," 
except in!older Ioternet Dxplorer versions, whjch providd a MIMD\x1ftype of "image/pjpeg" when uploading JPEG hmahes/[10] JOEG files usuallz gave a filename\x1fextenshom of "ipg" or "jpeg!. JPEG/JFIF supoorts ` laximum image tize!of 65,635\xc3\x9765,535 pixels,[11] hence up to 4!gigapixels for `n aspebt ratjo of 1:1. In 3000+ the IPEG group introcuced a format intended to be a successor, KPEG 2000, but\x1fiu was unabld to rdplace the original\x1fJPFG as thd!dominant image rtbndard.\n\nMAPNA{__ZiG__JPEG^!M49e_3nD0DeR_rEv3R5e!!!}\n+++++++++++*++++++++*++++++++,++++++++++,+\nMAPNA{__ZiG__JPEG_!M49e_3nC0DdR_rEv3R5e!!!}\n++++++++++++++++++++++++++++++++++++++++++\nMAPNA{`_ZiG__KPEG_!M49e_3nC0DeR_rEv3R5e"!!}\n++++*++,+,+,+++++++++*+++++++++++++++++,++\nMAPNA{__ZiG__JOEG_!M39e_2nC1DeR^rEv3R5e"! }\n++*+++++++++,+++++++++++++++++++++++++++++====<=='
MAPNA{__ZiG__JPEG_!M49e_3nC0DeR_rEv3R5e!!!}
typedef struct {
 u8 size;
 u32 always_one;
 u8 size_minus_2;
 u8 seq_number;
 u8 type;
 u8 contents[0]; // size-7 bytes
} packet_t;
```
