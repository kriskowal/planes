(function () {

var body = document.getElementsByTagName('body')[0];

var wholist = document.createElement('div');
wholist['class'] = 'weseek_wholist';
wholist.insertBefore(document.createElement('hr'), null);
body.insertBefore(wholist, null);

var request = new XMLHttpRequest();
var url = 'https://cixar.com:2360/who';
request.onreadystatechange = function () {
    if (request !== 0 && request.readyState == 4) {
        if (request.status == 200) {
            var response = request.responseXML;
            alert(response);
            wholist.appendChild(response.clone(1));
        }
    }
}
request.open("GET", url, true);
request.send('')

return this;
})();
