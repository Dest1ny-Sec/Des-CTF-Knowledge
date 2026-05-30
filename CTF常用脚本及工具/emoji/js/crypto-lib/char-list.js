/*
 * UMD definition
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof exports === 'object') {
    module.exports = factory();
  } else {
    root.CharList = factory();
  }
}(this, function (_, punycode) {
  // unicode ASCII 8 chars
  // hex  chars
  var chars = ""+
              // http://unicode-table.com/en/#basic-latin
              // 0020   ! " # $ % & ' ( ) * + , - . / ( first char is space) 
              "!\"#$%&'()*+,-./"  + // no 0020
              // 0030 0 1 2 3 4 5 6 7 8 9 : ; < = > ? 
              "0123456789:;<=>?"  +
              // 0040 @ A B C D E F G H I J K L M N O  
              "@ABCDEFGHIJKLMNO"  + 
              // 0050 P Q R S T U V W X Y Z [ \ ] ^ _ 
              "PQRSTUVWXYZ[\\]^_" + 
              // 0060 ` a b c d e f g h i j k l m n o 
              "`abcdefghijklmno"  + 
              // 0070 p q r s t u v w x y z { | } ~ ␡ 
              "pqrstuvwxyz{|}~"   + // no 0079
              // http://unicode-table.com/en/#latin-1-supplement
              // 0080                   
              // 0090                 
              // 00A0   ¡ ¢ £ ¤ ¥ ¦ § ¨ © ª « ¬ ® ¯ 
              "£¥" +
              // 00B0 ° ± ² ³ ´ µ ¶ · ¸ ¹ º » ¼ ½ ¾ ¿ 
              "¿"                 + // no 00B0 -> 00BE
              // 00C0 À Á Â Ã Ä Å Æ Ç È É Ê Ë Ì Í Î Ï 
              "ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏ"  +
              // 00D0 Ð Ñ Ò Ó Ô Õ Ö × Ø Ù Ú Û Ü Ý Þ ß  
              "ÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞß"  + // no 00D7
              // 00E0 à á â ã ä å æ ç è é ê ë ì í î ï 
              "àáâãäåæçèéêëìíîï"  + 
              // 00F0 ð ñ ò ó ô õ ö ÷ ø ù ú û ü ý þ ÿ 
              "ðñòóôõö÷øùúûüýþÿ"    // no 00F7

  return chars
}));
