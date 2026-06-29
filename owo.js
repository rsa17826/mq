// ==UserScript==
// @name        owowify website
// @description owowify website evewywhewe! >w<
// @author      rssaromeo
// @version     4
// @license     GPL-3.0-or-later
// @match       *://*/*
// @grant       none
// @run-at      document-end
// @copyright   All rights reserved. Licensed under GPL-3.0-or-later. View license at https://spdx.org/licenses/GPL-3.0-or-later.html
// @namespace https://greasyfork.org/users/1184528
// @downloadURL https://update.greasyfork.org/scripts/555951/owowify%20website.user.js
// @updateURL https://update.greasyfork.org/scripts/555951/owowify%20website.meta.js
// ==/UserScript==

/**
 * wincesed undew GNYU! GPL vewsion 3.0 -w-
 */

/**
 * @param {String} inputText
 * @returns {String}
 */
function owo(inputText) {
  const endSentencePattern = String.raw`([\w ,.!?]+)?` // endSentencePattern
  // const endSentencePattern1 = String.raw`([\w ,.?]+)?`; // endSentencePattern without "!" sign
  // const endSentencePattern2 = String.raw`([\w ,.]+)?`; // endSentencePattern without "!" and "?" sign
  const vowel = "[aiueo]"
  const vowelNoE = "[aiuo]" // vowel without e
  const vowelNoIE = "[auo]" // vowel without i and e
  const zackqyWord = "[jzckq]"
  var result = inputText
  // OwO emote
  result = result.replace(
    reg`/(i(?:'|)m(?:\s+|\s+so+\s+)bored)${endSentencePattern}/gi`,
    subOwoEmote("-w-")
  )
  result = result.replace(
    reg`/(love\s+(?:you|him|her|them))${endSentencePattern}/gi`,
    subOwoEmote("uwu")
  )
  result = result.replace(
    reg`/(i\s+don(?:'|)t\s+care|i\s*d\s*c)${endSentencePattern}/gi`,
    subOwoEmote("0w0")
  )
  // world substitution
  result = result.replace(reg`/l[ou]ve?/gi`, ($0) =>
    subSameCase($0, "luv")
  )
  // OwO translation
  // /*result = result replace all "r" to "w", no exception! */
  //     result = result.replace(/r/gi, $0 => subSameCase($0, "w"))
  /*result = result replace all "r" to "w", unless r is alone */
  result = result.replace(/(?<=\w)r/gi, ($0) => subSameCase($0, "w"))
  result = result.replace(/r(?=\w)/gi, ($0) => subSameCase($0, "w"))
  /* lame -> wame, goal -> goaw, gallery -> gallewy, lol -> lol, null -> null */
  // loaded -> woaded
  // url -> uwl instead of uww
  result = result.replace(
    reg`/(?<!([wl]${vowel}*))l(?!([wl]))/gi`,
    ($0) => subSameCase($0, "w")
  )
  /* na -> nya, nu -> nyu, no -> nyo, ne -> nye */
  // completionInfo -> compwetionInfo instead of compwetionYInfo
  result = result.replace(reg`/[nN](${vowelNoE}+)/g`, ($0, $vowel) =>
    subSameCase($0 + $vowel, `ny${$vowel}`)
  )
  result = result.replace(
    reg`/N(${vowelNoE.toUpperCase()}+)/g`,
    ($0, $vowel) => subSameCase($0 + $vowel, `ny${$vowel}`)
  )
  /* ma -> mya, mu -> myu, mo -> myo */
  result = result.replace(
    reg`/[mM](${vowelNoIE}+)(?!w*${zackqyWord})/g`,
    ($0, $vowel) => subSameCase($0 + $vowel, `my${$vowel}`)
  )
  result = result.replace(
    reg`/M(${vowelNoE.toUpperCase()}+)(?!w*${zackqyWord})/g`,
    ($0, $vowel) => subSameCase($0 + $vowel, `my${$vowel}`)
  )
  /* pa -> pwa, pu -> pwu, po -> pwo */
  // AhkStopAlt -> AhkStopAwt instead of AhkStopWAwt
  result = result.replace(
    reg`/[pP](${vowelNoIE}+)(?!w*${zackqyWord})/g`,
    ($0, $vowel) => subSameCase($0 + $vowel, `pw${$vowel}`)
  )
  result = result.replace(
    reg`/P(${vowelNoIE.toUpperCase()}+)(?!w*${zackqyWord})/g`,
    ($0, $vowel) => subSameCase($0 + $vowel, `pw${$vowel}`)
  )

  return result
}

function subOwoEmote(emote) {
  const matchEndSpace = /^\s+$/g

  return ($0, $setenceBeforeEnd, $endSentence) => {
    if (
      $endSentence == undefined ||
      matchEndSpace.test($endSentence)
    ) {
      return `${$setenceBeforeEnd} ${emote}`
    } else return $0
  }
}

/**
 * @param {string} inputText
 * @param {string} replaceText
 */
function subSameCase(inputText, replaceText) {
  let result = ""

  for (let i = 0; i < replaceText.length; i++) {
    if (inputText[i] != undefined && replaceText[i] != undefined) {
      if (inputText[i].toUpperCase() == inputText[i]) {
        result += replaceText[i].toUpperCase()
      } else if (inputText[i].toLowerCase() == inputText[i]) {
        result += replaceText[i].toLowerCase()
      } else {
        result += replaceText[i]
      }
    } else {
      result += replaceText[i]
    }
  }

  return result
}

/** @param {[string[], ...any[]]} templateArgs */
function reg(...templateArgs) {
  const rawString = String.raw(...templateArgs)
  const pattern = rawString.substring(1, rawString.lastIndexOf("/"))
  const flags = rawString.substring(
    rawString.lastIndexOf("/") + 1,
    rawString.length
  )

  return new RegExp(pattern, flags)
}
