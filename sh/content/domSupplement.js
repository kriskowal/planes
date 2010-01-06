window.domSupplement = (function () {
        
this.cloneNode = function(from) {
    if (from.nodeType == 1) {
        var to = document.createElement(from.nodeName);
        var fromChild = from.firstChild;
        while (fromChild) {
            to.insertBefore(cloneNode(fromChild), null);
            fromChild = fromChild.nextSibling;
        }
        for (var i = 0; i < from.attributes.length; i++) {
            var attribute = from.attributes.item(i);
            to.setAttribute(attribute.nodeName, attribute.nodeValue);
        }
    } else {
        to = from.cloneNode(1);
    }
    return to;
}


this.parseXML = function (string) {
    var element = document.createElement('root');
    element.innerHTML = string;
    try {
    var result = element.firstChild;
    } catch (x) {
        alert(element);
    }
    while (result && result.nodeType != 1) {
        result = result.nextSibling;
    }
    return result;
}

return this;
})();
