window.ish = function (ishArgument, sendCommandsImmediately, urlBase) {

// configuration variables
var pollingInterval = 1100;
var pollingIntervalMin = 1100;
var pollingIntervalFactorUp = 1.5;
var pollingIntervalFactorDown = .95;
var pollingId = null;
var production = 1;
var debug = 0;

var session = '';
// just a bit more than a second.
//  The server drops sessions that poll
//  more frequently than one second.
var connectStatus = 0;
var initialConnectStatus = 0;
var away = 0;
var request = 0;

var enqueueMessage = window.messageBuffer.enqueueMessage; var enqueueException = window.messageBuffer.enqueueException;
var parseXML = window.domSupplement.parseXML;

var commandBox = document.getElementById('command');
var promptBox = document.getElementById('prompt');

var commands = [];

var escaper = function (text) {
    return escape(text).replace('+', '%2b')
}

try {

    var onreadystatechange = function () {
        try {
            if (request !== 0 && request.readyState == 4) {

                // isolate the status value request.  it tends to
                //  raise XPCOM exceptions intermitently.  This may be
                //  a bug.
                var status;
                try {
                    status = request.status;
                } catch (exception) {
                    status = 0;
                    request = 0;
                }

                if (status == 200) {

                    // maintain connection status
                    if (connectStatus == 0 && initialConnectStatus == 1) {
                        enqueueMessage(
                            'Your connection to the <b>service</b> ' +
                            'has been <b>restored</b>.'
                        )
                    }
                    connectStatus = 1;
                    initialConnectStatus = 1;

                    var response = parseXML(request.responseText);
                    var response = request.responseXML;
                    session = response.getElementsByTagName('session')[0].firstChild.data;
                    var prompt = response.getElementsByTagName('prompt')[0].firstChild.data;
                    var silent = response.getElementsByTagName('silent')[0].firstChild.data;
                    var titles = response.getElementsByTagName('title')[0];
                    var messages = response.getElementsByTagName('messages')[0];
                    var overlays = response.getElementsByTagName('overlays')[0];

                    promptBox.innerHTML = prompt;

                    window.messageBuffer.setSilent(silent == 'yes')

                    title = titles.firstChild;
                    if (title) {
                        window.messageBuffer.setTitle(title.data);
                    }

                    var message = messages.firstChild;
                    while (message) {
                        enqueueMessage(message.firstChild.data);
                        message = message.nextSibling;
                    }

                    var overlay = overlays.firstChild;
                    while (overlay) {
                        window.overlays.update(overlay.firstChild);
                        overlay = overlay.nextSibling;
                    }

                if (request.responseText.length > 8 * 1024) {
                        enqueueMessage(
                            "<p>The <b>server</b> sent <b>too much</b> information (8KB maximum +" +
                            Math.floor((request.responseText.length - 8 * 1024) / 1024) +
                            "KB).</p>"
                        );
                    }

                } else if (status == 0) {
                    if (connectStatus == 1) {
                        enqueueMessage(
                            'Sorry, this <b>service</b> has become temporarily ' +
                            '<b>unavailable</b>.'
                        );
                    }
                    connectStatus = 0;
                } else {
                    if (debug) {
                        enqueueException(
                            'The <b>service</b> unexpectedly responded ' +
                            'with an HTTP error status, ' +
                            '<tt>' + status + '</tt>, ' + 
                            'for <tt>' + request.url + '</tt>.'
                        );
                    }
                    connectStatus = 0;
                }

                // set request to 0 to release (in the semaphore sense) this requests
                //  lock on this function.  The poll function will not start a 
                //  new request otherwise.
                request = 0;
            }

        } catch (x) {
            if (request != 0 && connectStatus == 1) {
                if (production) {
                    enqueueMessage(
                        'You have been <b>disconnected</b> ' + 
                        'from the <b>service</b> ' +
                        'or are experiencing <b>lag</b>.'
                    );
                }
                if (debug) {
                    throw(x);
                }
                connectStatus = 0;
            }
        }

    };

    var poll = function () {
        try {

            // assure that only one xmlhttprequest is pending at any time
            if (request !== 0) {
                // increase the polling interval to 
                pollingInterval *= pollingIntervalFactorUp;
                return;
            }  else {
                pollingInterval *= pollingIntervalFactorDown;
                if (pollingInterval < pollingIntervalMin) {
                    pollingInterval = pollingIntervalMin;
                }
            }

            // get a request object
            if (window.XMLHttpRequest) {
                     // Mozilla (Firefox), Safari, & al
                    request = new XMLHttpRequest();
            } else if (window.ActiveXObject) {
                    // Microsoft Internet Explorer
                    request = new ActiveXObject("Microsoft.XMLHTTP");
            }

            // form a URL
            var url = urlBase + '?session=' + escaper(session);
            if (commands.length) {
                var command = commands.shift();
                url += '&command=' + escaper(command);
                request.command = command;
                request.silent = window.messageBuffer.getSilent();
            }
            url += '&ish=' + escaper(ishArgument);
            request.url = url;

            // setup the request event handler
            request.onreadystatechange = onreadystatechange;
            request.open("GET", url, true);
            request.send('');

        } finally {
            if (pollingId) {clearTimeout(pollingId);}
            pollingId = setTimeout(function () {poll()}, pollingInterval);
        }
    }

    poll();

    // todo: add polling synchronization
    window.messageBuffer.onStartTyping = function () {
    }

    window.messageBuffer.onCommand = function (command) {
        commands.push(command);
        if (sendCommandsImmediately) {
            poll();
        }
        away = 0;
    }

    window.onblur = function () {
        if (away == 0) {
            enqueueMessage('<hr/>');
        }
        away = 1;
    }

    window.onfocus = function () {
        // away is not set when you refocus, rather when a command is sent
    }

} catch (x) {
    enqueueException(x);
}

return this;
};
