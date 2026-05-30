/*
 * UMD definition
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define(['lodash', 'punycode', './char-list.js'], factory);
  } else if (typeof exports === 'object') {
    module.exports = factory(require('lodash'), require('punycode'), require('./char-list.js'));
  } else {
    root.CaesarShifter = factory(root._, root.punycode, root.CharList);
  }
}(this, function (_, punycode, CharList) {

  chars = _.flatten(_.map(CharList, function (char) { return punycode.ucs2.decode(char) }))
  // console.log(chars)

  function encrypt (text, key) {
    return _caesarShift(text, key)
  }

  function decrypt (text, key) {
    return _caesarShift(text, -key)
  }

  function _caesarShift (text, shift) {
    // if shift is 0 or undefined return string
    if (typeof shift === 'undefined' || shift == 0)
      return text

    // if shift is lower that 0 
    if (shift < 0)
      shift = shift + CharList.length
    // shift mod character list length
    shift = shift % CharList.length

    var output = ''
    for (var i = text.length-1; i >= 0; i--) {
      var c = text[i]
      if (_.includes(CharList, c)) {
        var index = _.findIndex(CharList, function (i) { return i === c })
        index = (index + shift) % CharList.length
        c = CharList[index]
      }
      output += c
    }

    return output.split('').reverse().join('')
  }

  return {
    encrypt: encrypt,
    decrypt: decrypt
  }
}));
