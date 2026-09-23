/*
 * UMD definition
 */

(function (root, factory){
  if (typeof define === 'function' && define.amd) {
    define(['lodash', 'punycode', './emoji-list.js', './char-list.js'], factory)
  } else if (typeof exports === 'object') {
    module.exports = factory(require('lodash'), require('punycode'), require('./emoji-list.js'), require('./char-list.js'))
  } else {
    root.Emojifier = factory(root._, root.punycode, root.EmojiList, root.CharList)
  }
}(this, function (_, punycode, EmojiList, CharList) {
 
  // make chars unicode codepoints
  var chars = _.flatten(_.map(CharList, function (c) { return punycode.ucs2.decode(c) }))
  var emojis = EmojiList.slice(0, CharList.length)

  function encode (text) {
    // convert text into unicode points ( from ucs2 )
    var points = punycode.ucs2.decode(text)
    // map points with emoji indexes
    points = _.map(points, function (point) {
      // if point is not a valid symbol return it
      if (!_.includes(chars, point)) return point
      // get index of point in CharList array
      var index = _.findIndex(chars, function (c) { return c == point }) 
      // return emoji char at index position
      return emojis[index]
    })
    // encode in ucs2
    return punycode.ucs2.encode(points)
  }

  function decode (text) {
    // convert text into unicode points ( from ucs2 )
    var points = punycode.ucs2.decode(text)
    // map points with emojis index
    points = _.map(points, function (point) {
      // find index of point in emojis ( or -1 )
      var index = _.findIndex(emojis, function (el) { return el === point })
      // if point is found return it
      if (index >= 0) return CharList[index]
      // else convert point to char and return it
      return String.fromCodePoint(point)
    })
    // join points to create a string
    return points.join('')
  }

  function generateEmojiListFrom (key) {
    key = toNumber(key)
    // if key is undefined reset emoji list
    if (_.isUndefined(key)) {
      emojis = EmojiList.slice(0, CharList.length)
    } else { 
      var z = key
      var m = EmojiList.length
      function getNext(x) { return (x * z) % m }

      var newEmojis = []
      _.times(CharList.length, function (i) {
        newEmojis.push(EmojiList[getNext(i)])
      })
      emojis = newEmojis
    }
  }

  function toKey (emoji) {
    emoji = toNumber(emoji)
    emoji = emoji  % CharList.length
    return emoji
  }

  function toNumber (emoji) {
    emoji = _.toString(emoji)
    if (_.isEmpty(emoji)) throw 'Emojifier.generateEmojiSubset needs a non-empty string'
    return _.head(punycode.ucs2.decode(emoji))
  }

  return {
    encode: encode,
    decode: decode,
    generateEmojiListFrom: generateEmojiListFrom,
    toNumber: toNumber,
    toKey: toKey,
  }
}));
