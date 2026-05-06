
/*
 howler.js v2.1.1 | (c) 2013-2018, James Simpson of GoldFire Studios | MIT License | howlerjs.com  Spatial Plugin  @source http://purl.eligrey.com/github/FileSaver.js/blob/master/FileSaver.js */
 var $jscomp = $jscomp || {}
 $jscomp.scope = {}
 $jscomp.checkStringArgs = function (Y, q, x) {
   if (null == Y)
     throw new TypeError(
       "The 'this' value for String.prototype." +
         x +
         " must not be null or undefined"
     )
   if (q instanceof RegExp)
     throw new TypeError(
       "First argument to String.prototype." +
         x +
         " must not be a regular expression"
     )
   return Y + ""
 }
 $jscomp.ASSUME_ES5 = false
 $jscomp.ASSUME_NO_NATIVE_MAP = false
 $jscomp.ASSUME_NO_NATIVE_SET = false
 $jscomp.defineProperty =
   $jscomp.ASSUME_ES5 || "function" == typeof Object.defineProperties
     ? Object.defineProperty
     : function (Y, q, x) {
         Y != Array.prototype && Y != Object.prototype && (Y[q] = x.value)
       }
 $jscomp.getGlobal = function (Y) {
   return "undefined" != typeof window && window === Y
     ? Y
     : "undefined" != typeof global && null != global
     ? global
     : Y
 }
 $jscomp.global = $jscomp.getGlobal(this)
 $jscomp.polyfill = function (Y, q, x, B) {
   if (q) {
     x = $jscomp.global
     Y = Y.split(".")
     for (B = 0; B < Y.length - 1; B++) {
       var F = Y[B]
       F in x || (x[F] = {})
       x = x[F]
     }
     Y = Y[Y.length - 1]
     B = x[Y]
     q = q(B)
     q != B &&
       null != q &&
       $jscomp.defineProperty(x, Y, {
         configurable: true,
         writable: true,
         value: q,
       })
   }
 }
 $jscomp.polyfill(
   "String.prototype.startsWith",
   function (Y) {
     return Y
       ? Y
       : function (q, x) {
           var B = $jscomp.checkStringArgs(this, q, "startsWith")
           q += ""
           var F = B.length,
             N = q.length
           x = Math.max(0, Math.min(x | 0, B.length))
           for (var u = 0; u < N && x < F; ) if (B[x++] != q[u++]) return false
           return u >= N
         }
   },
   "es6",
   "es3"
 )
 $jscomp.polyfill(
   "Array.prototype.fill",
   function (Y) {
     return Y
       ? Y
       : function (q, x, B) {
           var F = this.length || 0
           0 > x && (x = Math.max(0, F + x))
           if (null == B || B > F) B = F
           B = Number(B)
           0 > B && (B = Math.max(0, F + B))
           for (x = Number(x || 0); x < B; x++) this[x] = q
           return this
         }
   },
   "es6",
   "es3"
 )
 $jscomp.polyfill(
   "String.prototype.endsWith",
   function (Y) {
     return Y
       ? Y
       : function (q, x) {
           var B = $jscomp.checkStringArgs(this, q, "endsWith")
           q += ""
           void 0 === x && (x = B.length)
           x = Math.max(0, Math.min(x | 0, B.length))
           for (var F = q.length; 0 < F && 0 < x; )
             if (B[--x] != q[--F]) return false
           return 0 >= F
         }
   },
   "es6",
   "es3"
 )
 $jscomp.SYMBOL_PREFIX = "jscomp_symbol_"
 $jscomp.initSymbol = function () {
   $jscomp.initSymbol = function () {}
   $jscomp.global.Symbol || ($jscomp.global.Symbol = $jscomp.Symbol)
 }
 $jscomp.Symbol = (function () {
   var Y = 0
   return function (q) {
     return $jscomp.SYMBOL_PREFIX + (q || "") + Y++
   }
 })()
 $jscomp.initSymbolIterator = function () {
   $jscomp.initSymbol()
   var Y = $jscomp.global.Symbol.iterator
   Y || (Y = $jscomp.global.Symbol.iterator = $jscomp.global.Symbol("iterator"))
   "function" != typeof Array.prototype[Y] &&
     $jscomp.defineProperty(Array.prototype, Y, {
       configurable: true,
       writable: true,
       value: function () {
         return $jscomp.arrayIterator(this)
       },
     })
   $jscomp.initSymbolIterator = function () {}
 }
 $jscomp.arrayIterator = function (Y) {
   var q = 0
   return $jscomp.iteratorPrototype(function () {
     return q < Y.length ? { done: false, value: Y[q++] } : { done: true }
   })
 }
 $jscomp.iteratorPrototype = function (Y) {
   $jscomp.initSymbolIterator()
   Y = { next: Y }
   Y[$jscomp.global.Symbol.iterator] = function () {
     return this
   }
   return Y
 }
 $jscomp.iteratorFromArray = function (Y, q) {
   $jscomp.initSymbolIterator()
   Y instanceof String && (Y += "")
   var x = 0,
     B = {
       next: function () {
         if (x < Y.length) {
           var F = x++
           return { value: q(F, Y[F]), done: false }
         }
         B.next = function () {
           return { done: true, value: void 0 }
         }
         return B.next()
       },
     }
   B[Symbol.iterator] = function () {
     return B
   }
   return B
 }
 $jscomp.polyfill(
   "Array.prototype.keys",
   function (Y) {
     return Y
       ? Y
       : function () {
           return $jscomp.iteratorFromArray(this, function (q) {
             return q
           })
         }
   },
   "es6",
   "es3"
 )
 $jscomp.polyfill(
   "String.prototype.codePointAt",
   function (Y) {
     return Y
       ? Y
       : function (q) {
           var x = $jscomp.checkStringArgs(this, null, "codePointAt"),
             B = x.length
           q = Number(q) || 0
           if (0 <= q && q < B) {
             q |= 0
             var F = x.charCodeAt(q)
             if (55296 > F || 56319 < F || q + 1 === B) return F
             q = x.charCodeAt(q + 1)
             return 56320 > q || 57343 < q ? F : 1024 * (F - 55296) + q + 9216
           }
         }
   },
   "es6",
   "es3"
 )