from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config["SECRET_KEY"] = "chat-app"

socketio = SocketIO(app, cors_allowed_origins="*")

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Chat App</title>
<style>
body { margin:0; font-family:Arial; background:#1e1e1e; color:white; }
#chat { height:90vh; overflow-y:auto; padding:10px; }
#input { display:flex; }
input { flex:1; padding:10px; border:none; }
button { padding:10px; background:#5865f2; color:white; border:none; }
.msg { margin:5px 0; }
</style>
</head>
<body>

<h3 style="padding:10px;">Simple Chat 💬</h3>
<div id="chat"></div>

<div id="input">
<input id="msg" placeholder="Type message..." />
<button onclick="sendMsg()">Send</button>
</div>

<script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
<script>
let socket = io();

let username = sessionStorage.getItem("user");

if (!username) {
    username = prompt("Enter username:");
    sessionStorage.setItem("user", username);
}

socket.on("message", function(data){
    document.getElementById("chat").innerHTML +=
    "<div class='msg'><b>" + data.user + ":</b> " + data.msg + "</div>";

    document.getElementById("chat").scrollTop =
    document.getElementById("chat").scrollHeight;
});

function sendMsg(){
    let msg = document.getElementById("msg").value;
    if (!msg) return;

    socket.send({user: username, msg: msg});
    document.getElementById("msg").value = "";
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@socketio.on("message")
def handle(msg):
    send(msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)