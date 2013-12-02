var URL = "ws://localhost:8000/socket";
var output;
var title;
var socket;
var timeout_id = 0;
var last_text_hash = "";
var docid;
var textbox_obj;

function display(prefix, message) {
    var p = document.createElement("p");
    p.innerHTML = prefix + $("<div/>").text(message).html();
    output.appendChild(p);
}

function send(message) {
    display('<span style="color: green;">SENT:</span> ', message);
    socket.send(message);
}

function get_keywords() {
    var keywords = [];
    textbox_obj.find(".keyword").each(function() {
        if ($(this).text())
            keywords.push($(this).text());
    });
    return keywords;
}

function update_server() {
    keywords = get_keywords(textbox_obj);
    var data = {"title": title.val(), "text": textbox_obj.html(), "keywords": keywords};
    send("UPDATE " + JSON.stringify(data));
}

function gen_hash(s) {
    // http://stackoverflow.com/questions/7616461
    return s.split("").reduce(function(a,b){a=((a<<5)-a)+b.charCodeAt(0);return a&a},0);
}

function on_type() {
    var this_hash = gen_hash(title.val() + textbox_obj.html());
    if (this_hash != last_text_hash) {
        last_text_hash = this_hash;
        window.clearTimeout(timeout_id);
        timeout_id = window.setTimeout(update_server, 500, textbox_obj);
    }
}

$(document).ready(function() {
    $("#textbox").rte("/static/common.css", "/static/img/");
    output = document.getElementById("output");
    title = $("#title");
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
        if (evt.data.indexOf("READY") == 0) {
            var payload = JSON.parse(evt.data.substring(6));
            title.val(payload.title);
            textbox_obj.html(payload.text);
        }
        if (evt.data == "GOODBYE") {
            socket.close();
        }
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

    title.keyup(function(event) {
        on_type();
    });
});
