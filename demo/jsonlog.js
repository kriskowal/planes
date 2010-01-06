
include('base.js');
var http = require('http.js');
var json = require('json.js');

this.write = function (message, label) {
    http.requestText('/write/' + json.json([message, label]))
};

var n = 0;
this.read = function () {
    json.request('/read/' + n, function (messages) {
        n += getLength(messages);
        forEachArgs(messages, log);
    });
};

read();

setInterval(read, 2000);

