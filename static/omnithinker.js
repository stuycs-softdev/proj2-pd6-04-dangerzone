var URL = "ws://localhost:8000/socket";
var output;
var socket;
var timeout_id = 0;
var last_text_hash = "";
var docid;

function display(prefix, message) {
    var p = document.createElement("p");
    p.innerHTML = prefix + $("<div/>").text(message).html();
    output.appendChild(p);
}

function send(message) {
    display('<span style="color: green;">SENT:</span> ', message);
    socket.send(message);
}

function get_keywords(obj) {
    var keywords = [];
    obj.find(".keyword").each(function() {
        if ($(this).text())
            keywords.push($(this).text());
    });
    return keywords;
}

function update_server(obj) {
    keywords = get_keywords(obj);
    var data = {"text": obj.html(), "keywords": keywords};
    send("UPDATE " + JSON.stringify(data));
}

function gen_hash(s) {
    // http://stackoverflow.com/questions/7616461
    return s.split("").reduce(function(a,b){a=((a<<5)-a)+b.charCodeAt(0);return a&a},0);
}

function on_type(obj) {
    var this_hash = gen_hash(obj.html());
    if (this_hash != last_text_hash) {
        last_text_hash = this_hash;
        window.clearTimeout(timeout_id);
        timeout_id = window.setTimeout(update_server, 500, obj);
    }
}

$(document).ready(function() {
    output = document.getElementById("output");
    socket = new WebSocket(URL);

    socket.onopen = function(event) {
        display('<span style="color: brown;">CONNECTED</span>', '');
        send("HELLO " + docid);
    };

    socket.onclose = function(evt) {
        display('<span style="color: brown;">DISCONNECTED</span>', '');
        $("#options").hide();
    };

    socket.onmessage = function(evt) {
        display('<span style="color: red;">RECEIVED:</span> ', evt.data);
        if (evt.data == "GOODBYE") {
            socket.close();
        }
    };

    socket.onerror = function(evt) {
        display('<span style="color: brown;">ERROR:</span> ', evt.data);
    };

    $("#send").click(function() {
        var msg = $("#sendbox").val();
        if (msg) {
            send(msg);
            $("#sendbox").val("");
        }
    });
    $("#sendbox").keyup(function(event) {
        if (event.keyCode == 13)
            $("#send").click();
    });

    $("#disconnect").click(function() {
        send("BYE");
    });

    $("#textbox").rte("/static/common.css", "/static/img/");
});
