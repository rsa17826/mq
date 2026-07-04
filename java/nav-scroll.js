////////////////////////
//
// nav-scroll.js   version 9
//
//      Looks for divs with class .stickyAdDiv and positions them so that one is always
//      at the top of #stickyContainer uniformly as the user scrolls. The basic concept
//      is to look for a container <div> with id stickyContainer that holds everything.
//      inside of that is a <div> with id stickyMover that holds all of the ads, and
//      that container gets CSS fixed positioned when scrolling happens. Inside of that
//      <div> are individual ads all of which are a <div> with a CSS class stickyAdDiv.
//      The code looks for a header and footer to with ids of stickyHeader and
//      stickyFooter, and it uses those to know when the ads need to be scrolled at the
//      top of the page and also to prevent ads from overlapping the footer at the
//      bottom of the page.
//
//      Does nothing if width is 600 or less (assumes mobile layout and that you've got
//      CSS media queries that handle the layout.)
//
//      This JavaScript file requires jQuery.
//
// Important CSS bits to note...
//
//    #stickyHeader     - Unique ID assigned to the header element on the page.
//                        Ad divs will scroll normally until this moves off the page,
//                        and we need to determine the height of this to know when to
//                        lock the first ad to the top.
//
//    #stickyContainer  - Unique ID assigned to the div container element holding
//                        the #stickyMover div. This div should have no top/bottom
//                        margin set to avoid stuttering during scrolling at the top
//                        of the page.
//
//    #stickyMover      - Unique ID assigned to the div container element holding all
//                        ads to be positioned. This div should have no top/bottom
//                        margin set to avoid stuttering during scrolling at the top
//                        of the page.
//
//    .stickyAdDiv      - Class assigned to each div that contains an ad inside
//                        #stickyMover. Your CSS file should set margin-top
//                        for this class and should NOT have a bottom margin set.
//                        The JavaScript here will read the top margin and use it to
//                        make sure the ads look spaced the same when they are
//                        in position:fixed or position:static, and also the margin
//                        is used to calculate the offscreen position when scrolling
//                        #stickyMover in a way that it looks consistent during the
//                        transition.
//
//   Sample CSS:         #stickyHeader, #stickyFooter {
//                       }
//
//                       #stickyContainer, #stickyMover {
//                            margin: 0;
//                       }
//
//                       .stickyAdDiv {
//                           margin-top: 10px;
//                       }
//
//   Sample HTML:        <div id=stickyHeader> [...header in here... ] </div>
//                       <div id=stickyContainer>
//                          <div id=stickyMover>
//                              <div class=stickyAdDiv> [...Ad #1... ] </div>
//                              <div class=stickyAdDiv> [...Ad #2... ] </div>
//                              <div class=stickyAdDiv> [...Ad #3... ] </div>
//                          </div>
//                       </div>
//                       <div id=stickyFooter> [...footer in here... ] </div>
//
////////////////////////

var gPositionScroll_priorScroll = 0

function positionStickyElements() {
  var viewportWidth = parseInt($(window).width())
  var scrollTop = parseInt($(window).scrollTop())
  var headerElement = $("#stickyHeader")
  var headerHeight = parseInt(headerElement.height())
  var $mover = $("#stickyMover")
  var moverHeight = parseInt($mover.height())
  var windowHeight = parseInt($(window).height())

  // find the left edge of the outer container

  var stickyContainer = $("#stickyContainer")
  var stickyContainerOffset = stickyContainer.offset()
  var stickyContainerPosition = stickyContainer.position()
  var scrollLeft = parseInt($(window).scrollLeft())

  var leftEdge = $("#rightMenuPage").offset().left - scrollLeft

  // see if it all fits...

  var stickyContainerHeight = stickyContainer.height()
  var totalContentHeight = headerHeight + moverHeight
  var $rightSideBarContent = $("#rightMenuContent")

  //console.log( "totalContentHeight="+totalContentHeight+"  windowHeight="+windowHeight )

  if (totalContentHeight < windowHeight) {
    //console.log( "  totalContentHeight < windowHeight" )

    // undo any weird positioning of the mover in case we jumped here because of
    // a window resize...

    if ($mover.css("position") != "static") {
      headerElement.css({ visibility: "visible" })

      $mover.css({ transition: "0s linear", position: "static" })
    }

    $rightSideBarContent.css({
      transition: "0s linear",
      position: "fixed",
      top: "0px",
      left: leftEdge + "px",
    })
    return
  } else {
    if ($rightSideBarContent.css("position") != "static") {
      //console.log( "  totalContentHeight >= windowHeight  --> setting static from " + $rightSideBarContent.css('position')  )
      headerElement.css({ visibility: "visible" })
      $rightSideBarContent.css({
        transition: "0s linear",
        position: "static",
      })
    }
  }

  // Handle the sticky scrolling ads in the right column

  adDivs = $("#stickyContainer .stickyAdDiv")
  var adCount = adDivs.length

  if (
    adDivs.length > 0 &&
    viewportWidth > 600 &&
    headerElement.length
  ) {
    //console.log( "scrollTop="+scrollTop+"  headerHeight="+headerHeight )

    if (scrollTop <= headerHeight / 3) {
      // Header's still visible, use position:static for everything.
      $mover.css({ transition: "0s linear", position: "static" })
      headerElement.css({ visibility: "visible" })
    } else {
      headerElement.css({ visibility: "hidden" })

      // Get some stuff we need to know for later...

      var someMargin = 10

      var adHeights = []
      $(adDivs.get()).each(function () {
        var m1 = (someMargin = parseInt($(this).css("marginBottom")))
        var h = parseInt($(this).height())
        adHeights.push(m1 + h)
      })

      // build an array that and use that to figure out which ad should
      // be at the top of the display based on any given scroll percentage

      var adAtTop = []
      var chunksOfAds = 100 / adCount

      for (adIndex = 0; adIndex < adCount; adIndex++)
        for (i = 0; i < chunksOfAds; i++) adAtTop.push(adIndex)

      while (adAtTop.length < 100) adAtTop.push(adCount - 1)

      // now figure out the scroll percentage...

      var documentHeight = parseInt($(document).height())
      var yDelta = documentHeight - windowHeight
      if (yDelta < 1) {
        scrollTop = 0
        yDelta = 1
      }

      var scrollPercent = Math.min(
        100,
        Math.max(0, Math.floor((100 * scrollTop) / yDelta)),
      )

      // Now it's easy figure out which ad we want at the top...

      if (moverHeight <= windowHeight)
        // if it all fits, just pin it under the header
        scrollPercent = 0

      var adIndexAtTopOfPage = adAtTop[scrollPercent]

      // ...and calculate how far down the we need to shift everything to put this ad at the top

      var displacementForTopAd = 0
      for (adIndex = 0; adIndex < adIndexAtTopOfPage; adIndex++)
        displacementForTopAd -= adHeights[adIndex]

      //console.log( "scrollPercent="+scrollPercent+"  adIndexAtTopOfPage="+adIndexAtTopOfPage+"  displacementForTopAd="+displacementForTopAd )

      // Let's also make sure we're tight against the footer, and not overlapping it...

      var thisTransitionDelay = 0.2
      var footerElement = $("#stickyFooter")
      var footerVisibleTop = 9999999
      if (footerElement.length)
        footerVisibleTop = footerElement.offset().top - scrollTop

      var adVisBottom =
        displacementForTopAd + moverHeight + someMargin

      //    console.log( "footerVisibleTop="+footerVisibleTop+"  adVisBottom="+adVisBottom+"  moverHeight="+moverHeight )

      var lowestSpot = windowHeight
      if (footerVisibleTop < windowHeight) {
        var delta = windowHeight - footerVisibleTop
        lowestSpot -= delta
      }

      if (adVisBottom > footerVisibleTop) {
        var delta = adVisBottom - footerVisibleTop
        displacementForTopAd -= delta
        thisTransitionDelay = 0
        //    console.log( "   ===> SHIFT UP to avoid footer overlap delta="+delta )
      } else if (adVisBottom < lowestSpot && adIndexAtTopOfPage > 0) {
        var delta = lowestSpot - adVisBottom
        displacementForTopAd += delta
        thisTransitionDelay = 0
        //    console.log( "   ===> SHIFT DOWN to use available whitespace delta="+delta )
      }

      // Finally, move it...

      var curTop = parseInt($mover.css("top"))
      var movePixels = Math.abs(displacementForTopAd - curTop)
      var pixelsPerSecond = 1000.0
      var delay = (movePixels * thisTransitionDelay) / pixelsPerSecond

      //console.log( "final  displacementForTopAd="+displacementForTopAd + "    curTop="+curTop + "    delay="+delay)

      $mover.css({
        transition: delay.toFixed(2) + "s linear",
        position: "fixed",
        top: displacementForTopAd + "px",
        left: leftEdge + "px",
      })
    }
  }
}

$(window).scroll(positionStickyElements)
$(window).resize(positionStickyElements)
