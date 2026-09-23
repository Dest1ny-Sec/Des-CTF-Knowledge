/*
 * UMD definition
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define(['lodash', './crypto-lib/caesar-shifter.js', './crypto-lib/emojifier.js'], factory);
  } else if (typeof exports === 'object') {
    module.exports = factory(require('lodash'), require('./crypto-lib/caesar-shifter.js'), require('./crypto-lib/emojifier.js'));
  } else {
    root.CryptoLib = factory(root._, root.CaesarShifter, root.Emojifier);
  }
}(this, function (_, CaesarShifter, Emojifier) {

  function encrypt (input, key) {
    var output = input
    key = _emoji2key(key)
    output = CaesarShifter.encrypt(output, key)
    output = Emojifier.encode(output)
    return output
  }

  function decrypt (input, key) {
    var output = input
    key = _emoji2key(key)
    output = Emojifier.decode(output)
    output = CaesarShifter.decrypt(output, key)
    return output
  }

  function generateEmojiSubsetFrom (key) {
    Emojifier.generateEmojiListFrom(key)
  }

  return {
    encrypt: encrypt,
    decrypt: decrypt,
    generateEmojiSubsetFrom: generateEmojiSubsetFrom,
  }

  function _emoji2key (key) {
    if (_isEmoji(key)) {
      key = Emojifier.toKey(key)
    }
    return key
  }

  function _isEmoji (text) {
    return isNaN(Number(text))
  }
}));
