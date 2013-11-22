var URL = "ws://localhost:8000/socket";
var output;
var textbox;
var socket;
var timeout_id = 0;
var last_text_hash = "";

function display(message) {
    var p = document.createElement("p");
    p.innerHTML = message;
    output.appendChild(p);
}

function send(message) {
    display('<span style="color: green;">SENT:</span> ' + message);
    socket.send(message);
}

function update_server() {
    var data = {"text": textbox.innerHTML};
    send("UPDATE " + JSON.stringify(data));
}

function gen_hash(s) {
    // http://stackoverflow.com/questions/7616461
    return s.split("").reduce(function(a,b){a=((a<<5)-a)+b.charCodeAt(0);return a&a},0);
}

function init() {
    output = document.getElementById("output");
    textbox = document.getElementById("textbox");
    socket = new WebSocket(URL);

    socket.onopen = function(event) {
        display('<span style="color: brown;">CONNECTED</span>');
        send("HELLO");
    };

    socket.onclose = function(evt) {
        display('<span style="color: brown;">DISCONNECTED</span>');
        $("#options").hide();
    };

    socket.onmessage = function(evt) {
        display('<span style="color: red;">RECEIVED:</span> ' + evt.data);
        if (evt.data == "GOODBYE") {
            socket.close();
        }
    };

    socket.onerror = function(evt) {
        display('<span style="color: brown;">ERROR:</span> ' + evt.data);
    };

    $("#send").click(function() {
        var msg = $("#sendbox").val();
        if (msg) {
            send("UPDATE " + msg);
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

    $("#textbox").keyup(function(e) {
        var this_hash = gen_hash(textbox.innerHTML);
        if (this_hash != last_text_hash) {
            last_text_hash = this_hash;
            window.clearTimeout(timeout_id);
            timeout_id = window.setTimeout(update_server, 500);
        }
    });
}

window.addEventListener("load", init, false);
