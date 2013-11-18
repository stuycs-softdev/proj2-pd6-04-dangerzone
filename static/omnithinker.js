var URL = "ws://localhost:8000/socket";
var output;
var socket;

function display(message) {
    var p = document.createElement("p");
    p.innerHTML = message;
    output.appendChild(p);
}

function send(message) {
    display('<span style="color: green;">SENT:</span> ' + message);
    socket.send(message);
}

function init() {
    output = document.getElementById("output");
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
}

window.addEventListener("load", init, false);
