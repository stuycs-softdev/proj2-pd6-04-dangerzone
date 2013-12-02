var URL = "ws://localhost:8000/socket";
var socket;

var docid;
var title;
var textbox;

var timeout_id = 0;
var last_text_hash = "";

function get_keywords() {
    var keywords = [];
    textbox.find(".keyword").each(function() {
        if ($(this).text())
            keywords.push($(this).text());
    });
    return keywords;
}

function update_server() {
    keywords = get_keywords(textbox);
    var data = {"title": title.val(), "text": textbox.html(), "keywords": keywords};
    socket.send("UPDATE " + JSON.stringify(data));
}

function gen_hash(s) {
    // http://stackoverflow.com/questions/7616461
    return s.split("").reduce(function(a,b){a=((a<<5)-a)+b.charCodeAt(0);return a&a},0);
}

function on_type() {
    var this_hash = gen_hash(title.val() + textbox.html());
    if (this_hash != last_text_hash) {
        last_text_hash = this_hash;
        window.clearTimeout(timeout_id);
        timeout_id = window.setTimeout(update_server, 500, textbox);
    }
}

$(document).ready(function() {
    $("#textbox").rte("/static/common.css", "/static/img/");
    title = $("#title");
    socket = new WebSocket(URL);

    socket.onopen = function(event) {
        socket.send("HELLO " + docid);
    };

    socket.onmessage = function(evt) {
        if (evt.data.indexOf("READY") == 0) {
            var payload = JSON.parse(evt.data.substring(6));
            title.val(payload.title);
            textbox.html(payload.text);
        }
        if (evt.data == "GOODBYE") {
            socket.close();
        }
    };

    title.keyup(function(event) {
        on_type();
    });
});
