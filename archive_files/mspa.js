// embed the usual offline archive search pages inside a little public context
var noticeEl = document.createElement( 'div' )
noticeEl.innerHTML = '\
<style>.readmspa ul { margin-top: 2em; }\n\
.bbformat { font-size: 200%; }</style>\n\
<p>This is an unofficial extension to the <a href="http://www.mspaintadventures.com/search=menu">regular MS Paint Adventures search</a> adding words transcribed from media such as images &amp; Flashes. Corrections <a href="../offline/contact.html">welcome</a>!</p>\n\
';
noticeEl.setAttribute( 'style', 'font-size: 200%; padding: 2em; color: white; text-shadow: 2px 2px black' );
document.body.insertBefore( noticeEl, document.body.firstChild.nextSibling.nextSibling );

document.write( '<script src="../bbformat.js"><\/script>' );
