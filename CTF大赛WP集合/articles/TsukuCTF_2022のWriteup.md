# TsukuCTF 2022のWriteup

> 原文: https://www.ctfiot.com/62137.html
> ID: 62137


```
問題文：
祖父からお誕生プレゼントが入った鍵付きの箱とa.outという名前のファイルをもらった。これを開けるには数字を入力すれば良いらしい。ヒントはこのファイルの計算結果が鍵であること、このファイルは1971年に冷蔵庫ほどもあるミニコンピューターで作成された実行ファイルであると言われた。
フラグ形式：Nは数値である。 TsukuCTF22{N}
$ file a.out
a.out: PDP-11 old overlay
$ hexdump -C a.out
00000000 05 01 34 00 00 00 00 00 00 00 00 00 01 0a 02 0a |..4.............|
00000010 81 0a 82 0a c1 0c c1 0c c1 0c c1 0c c2 0c 42 60 |..............B`|
00000020 ff 01 70 61 73 73 77 64 20 69 73 20 69 6e 20 52 |..passwd is in R|
00000030 32 20 00 0a |2 ..|
00000034
;
; pdp11dasm version 0.0.3
; disassembly of ../a.out
;
000000: 000405 br 14 ; ..
;
000002: 000064 invalid opcode ; 4.
000004: 000000 halt ; ..
000006: 000000 halt ; ..
000010: 000000 halt ; ..
000012: 000000 halt ; ..
;
000014: 005001 clr r1 ; ..
000016: 005002 clr r2 ; ..
000020: 005201 inc r1 ; ..
000022: 005202 inc r2 ; ..
000024: 006301 asl r1 ; A.
000026: 006301 asl r1 ; A.
000030: 006301 asl r1 ; A.
000032: 006301 asl r1 ; A.
000034: 006302 asl r2 ; B.
000036: 060102 add r1,r2 ; B`
000040: 000777 br 40 ; ..
;
000042: 060560 071563 add r5,71563(r0) ; pass
000046: 062167 064440 add (r1)+,64512 ; wd i
000052: 020163 067151 cmp r1,67151(r3) ; s in
000056: 051040 bis (r0),-(r0) ; R
000060: 020062 005000 cmp r0,5000(r2) ; 2 ..
問題文：
つくしくんは疑似時限爆弾解除競技の訓練として、３つの時限爆弾に関するそれぞれのデータ(DefBom1,DefBom2は回路図、DefBom3は基板製造データ)をもとに、３つそれぞれの爆弾解除を行う。各時限爆弾はタイマー(limit_timer)がON状態になったとき、爆弾(bomb)に電流が流れて爆発する。
切断可能な線はデータ内で示されており、DefBom1では１から６の番号が振られたハサミ、DefBom2 では１から５の番号が振られたハサミ, DefBom3 では１から５の番号が振られた矢印である。示された切断可能な線のうち、１つの線を切れば limit_timer が ON 状態になっても爆発せず解除に成功する。しかし、残りの線は切っても limit_timer が ON 状態になる、もしくは切断した瞬間に爆発する。

フラグ形式はTsukuCTF22{ここにDefbom1からDefbom3において切断した番号を順に書く}といった形です。例として、切断した線の番号が DefBom1 では"3"、DefBom2"では"1"、DefBom3 では"5"であった場合フラグ形式はTsukuCTF22{315}となります。

この問題は3回までフラグを提出できます。タイプミス等が無いように注意してフラグを提出して下さい！！
TsukuCTF22{442}
問題文：
つくしくんはある観光地を調査した際に訪れた駅で写真を撮影した。果たしてこの写真が撮られた駅はどこだろうか？ フラグは駅の郵便番号（ハイフンなし）を入力して下さい
e.g. 東京駅の場合は郵便番号が100-0005なのでフラグは TsukuCTF22{1000005} となります。
TsukuCTF22{8770013}
問題文：
どこ？ フラグは写真が撮影された場所の郵便番号(ハイフンを除く)を入れて下さい。例えば撮影された場所が東京都庁の場合、郵便番号は163-8001なのでTsukuCTF22{1638001}となります。
TsukuCTF22{6038361}
問題文：
つくし君は、はるばる飛行機で愛するパートナーのもとへやってきました。
ここはどこの空港かわかりますか？
TsukuCTF22{福岡}
問題文：
つくし君は愛知県犬山市にデートに来た時の思い出の写真を見返しています。 おいしそうな写真を見つけ、おやつが食べたくなりました。 写真のおやつの名前を教えてください。
※フラグの形式はTsukuCTF22{XXXXXXX ver.XXXXXX}です。
TsukuCTF22{和チーズケーキ ver.煎茶パウダー}
問題文：
旅行中のつくし君は迷子になってしまったようです。うつむいています。送られてきた写真から場所を特定できますか？
※フラグの形式はTsukuCTF22{緯度_経度}です。ただし、緯度経度は十進法で小数点以下五桁目を切り捨てたものとします。
TsukuCTF22{34.5763_136.5313}
イケメンのつくしくんは訪れている場所の写真をSNSに投稿したところ、ストーカーに特定されてしまった。ストーカー曰く「好きなゲームと新聞がコラボしたときの広告にこの場所が映っていたのを思い出した」とのことだった。
フラグは写真が撮影された場所の郵便番号(ハイフンを除く)を入れて下さい。例えば撮影された場所が東京都庁の場合、郵便番号は163-8001なので TsukuCTF22{1638001}となります。
TsukuCTF22{6491331}
問題文：
つくし君がロボット見学に訪れた施設はどこ？
フラグ形式は TsukuCTF22{施設名} となります。施設名の表記は、その施設の英語版ホームページの表記に従います。
TsukuCTF{TsukuCTF22{South China University of Technology}}
問題文：
つくし君からマイコンボードを借りたら、このマイコンを使って実験を行ったホテルと部屋番号がわかってしまった！！ マイコンのフラッシュメモリから読みだしたデータを渡すので、ホテル名と部屋番号を特定してください。 ※フラグの形式はTsukuCTF22{XXホテル&XXXXXXXXXXXX_部屋番号}です。
$ strings Flash.bin | grep 31
apa-316-2428
apa-316-2428
apa-316-2428
apa-316-2428
294315
apa-316-2428
TsukuCTF22{アパホテル&リゾート〈両国駅タワー〉_2428}
問題文：
日本の町は美しい。撮影地を答えてください。

フラグはこの建物の開業日(YYYY/MM/DD)です。たとえば、東京スカイツリーの開業日は2012年5月22日なので、フラグはTsukuCTF22{2012/05/22}となります。
TsukuCTF22{2019/03/29}
問題文：
私は世界一可愛い猫ちゃんの写真を見つけました。この猫ちゃんの生年月日を答えてください。

フラグフォーマットは TsukuCTF22{YYYY/MM/DD} です。
TsukuCTF22{2021/09/16}
問題文：
月の満ち欠けは美しい。この場所はどこだろうか。 ※フラグの形式はTsukuCTF22{緯度_経度}です。ただし、緯度経度は十進法で小数点以下五桁目を切り捨てたものとします。
TsukuCTF22{35.0120_135.6778}
問題文：
手前の電車は何時何分に発車するでしょうか？
フラグ形式はTsukuCTF22{xx:xx}で、24時間表記です。
提出回数制限: 5回
TsukuCTF22{15:23}
問題文：
つくし君はとある駅で友達を待っています。さて、つくし君はどこの駅にいるでしょうか？

TsukuCTF22{駅名(漢字、平仮名、英語可)}

注意

 駅名はWebページで公開されている表記を利用してください
 「駅」という漢字はFlagに含めないでください
 数字が含まれる場合は全て半角英数字にしてください
 例えば、六本木一丁目駅が答えなら、TsukuCTF22{六本木1丁目}、TsukuCTF22{ろっぽんぎ1ちょうめ}、TsukuCTF22{Roppongi itchome}が答えになります

提出回数は10回までです。
TsukuCTF22{西11丁目}
問題文：
D社の新入社員が、社内の機密データを持って蒸発してしまった！ 電話もメールも全くつながらない。唯一残されていたのは、消し忘れたと見られる本人の公開鍵のみ。この鍵の持ち主を特定してほしい。
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDGOfu3zT1ZBW+XWBsTJQAuk5+BXwfvbqkoH8vC8vqbp2BWjsRHBX8SSlP2i0YyN03PUkXkqRXpl8O4iBF8pL1msNA6kSOpB6kiYb84w8qY/MwZMocO7vklvwbwdSw9YLD05sKTXmWuvjBoGPYU+FYKcxxtNimP8emWByILrLrhuRSsD2hRLaK2c5CxC3IxWcfPFOP1v9QqFDiKaEaJ3vjUUfQPR7NCGleaTy2tv/cvgTD983yXSrIsai57R5b4ILptyy8Y+K4ElZd5B+7H4rZqY4h2I5SHBj0Y3ZTppB8PXZOD00JLPgycZCT49ipIXiemS/5WMWH1NWc26fmg7yTD
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC8MXOXvmOSPz+ZZDF/6aoYRwujqvYdlkVzfb249jNSx1YEqpJXGOdTJT+A1troE8rYfTNMRb6i7HGzAf+YYVQrY/IwXalbI2xMXDahjN7vwZzxAmoypY59k3IFYjYuZGCK9OMDX+Na4xSPbkmvSkPm1i30hnYznLwp+8oPIoqPc7DY1VR/UAh3fIBNDx6aoQgEIbMTeDyIy4YNPRWvKK0NzvvpwQ9aaU81k7hMtm6/oU6PNfmgsZBsDztlzidEjS60Ydrenk9lFx9FwVdXhL5HG/2rOWsZmd9QwDHKNt8VaSupzW6I757YnUBiIvH5U9C48zm+6BDcnbpUVB6bnzZ5
$ ssh -T git@github.com -i ./a
Hi Ann0nymusTsukushi! You've successfully authenticated, but GitHub does not provide shell access.
問題文：
謎の人物からDMが届きました。よく見ると脅迫文ののようです。DMを送った人物を調査して、この人物が使用している他のWebサービスを見つけてください。

注1: この人物は複数のWebサービスを使用していますが、そのいずれかのプロフィールにフラグが埋め込まれています。

注2: 画像に含まれているURLはこちらです。 https://bit.ly/3Ekih5M
$ python sherlock.py gross_poem
[*] Checking username gross_poem on:

[+] Instagram: https://www.instagram.com/gross_poem
[+] Trakt: https://www.trakt.tv/users/gross_poem
[+] XXXX

[*] Results: 3

[!] End: The processing has been finished.
TsukuCTF22{M4ny_0S1N7_700ls_3x157}
```
