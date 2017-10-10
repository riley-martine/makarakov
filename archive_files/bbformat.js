// These functions derived from PesterCopy user script by Violet CLM
// Get it here: http://www.mspaforums.com/showthread.php?56129

function BBCodify() {
    var nodeAndOffset = function( node, offset ) {
	if (node.parentNode.tagName === "SPAN") {
	    return { node: node.parentNode, offset: offset };
	} else if ((node.tagName !== undefined) && (node.tagName != "BR")) {
	    return { node : node.childNodes[1 + offset], offset: 0 };
	} else {
	    return { node: node, offset: offset };
	}
    };
    function isSelectionBackwards(sel) { //http://stackoverflow.com/questions/8038683/window-getselection-how-do-you-tell-if-the-anchor-node-comes-before-the-focus
	var backwards = false;
	if (!sel.isCollapsed) {
	        var range = document.createRange();
	        range.setStart(sel.anchorNode, sel.anchorOffset);
	        range.setEnd(sel.focusNode, sel.focusOffset);
	        backwards = range.collapsed;
	    }
	return backwards;
	}
    var selection = window.getSelection();

    var first = nodeAndOffset( selection.anchorNode, selection.anchorOffset );
    var last = nodeAndOffset( selection.focusNode, selection.focusOffset );
    if (isSelectionBackwards(selection)) {
	last = nodeAndOffset( selection.anchorNode, selection.anchorOffset );
	first = nodeAndOffset( selection.focusNode, selection.focusOffset );
    }

    var pageNode = first.node.parentNode;
    while (pageNode && pageNode.getAttribute('class') != 'page') { pageNode = pageNode.parentNode; }
    var link = pageNode.getElementsByTagName('a')[0];
    var result = "From [url=" + link.getAttribute('href') + "]page " + pageNode.getAttribute('id') +
             ", " + link.innerHTML + "[/url]\n[font=Courier New][b]\n";
    
    var currentNode = first.node;
    function appendText(text) {
	if (currentNode.nodeType === 3)
	    result += text.replace("\n", "");
	else if ((currentNode.tagName != 'BR') && (text != ''))
	    result += '[' + currentNode.getAttribute('style').replace(/.*color: /, 'color=').replace(/;.*/, '') + ']' + text + "[/color]";
    }
    
    if (first.node == last.node) {
	appendText(first.node.textContent.substring(first.offset, last.offset));
    } else {
	appendText(first.node.textContent.substring(first.offset));
	while ((currentNode = currentNode.nextSibling) != last.node) {
	    if (currentNode.tagName === "BR")
		result += "\n";
	    else
		appendText(currentNode.textContent);
	}
	if (last.node != null) appendText(last.node.textContent.substring(0, last.offset));
    }

    result += "\[/b][/font]";
    return result.replace( /&lt;/g, '<' ).replace( /&gt;/g, '>' ).replace( /&amp;/g, '&' ).replace( /&quot;/g, '"' );
}
function onCopyFunc(e) {
    if (document.getElementById('bbformat').checked) {
	e.preventDefault();
	e.clipboardData.setData("Text", BBCodify());
    }
}

var pesterlogs = document.getElementsByClassName("log");
if (pesterlogs.length > 0) {
    var control = document.createElement( 'div' );
    control.innerHTML += '<p class="bbformat" title="(does not work on Internet Explorer yet, sorry)" style="position: fixed; margin: 0; padding: 0.25em; background: black; color: white; top: 0;"><input id="bbformat" type="checkbox" checked></input><label for="bbformat">BBCode format copied pesterlogs (<a style="color: inherit" href="http://www.mspaforums.com/showthread.php?56129-Pesterlog-Formatter">for quoting on forums</a>)</label></p>';
    document.body.appendChild( control );
}
for (var i = 0; i < pesterlogs.length; ++i) {
    var logSection = pesterlogs[i].getElementsByTagName('section')[0];
    logSection.addEventListener("copy", onCopyFunc, false);
}
