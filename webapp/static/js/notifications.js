document.addEventListener("DOMContentLoaded", () => {
    socket = io.connect("https://sheltered-reaches-07912.herokuapp.com", { transports: ['websocket'] });

    socket.on("send_my_message", function(message) {
        alert(message['message'])
    });


});

function leaveRoom(room_id) {
    socket.emit("leave", { room_id: room_id });
}

function joinIntoRoom(room_id) {
    socket.emit("join", { room_id: room_id });
}

function notifications() {
    if (document.getElementById("login") != null) {
        login = document.getElementById("login").getAttribute('value')
        joinIntoRoom(login)
    }
}


function logout() {
    var url = 'https://' + location.host + '/sender/logout'

    if (document.getElementById("login") != null) {
        login = document.getElementById("login").getAttribute('value')
        leaveRoom(login)
    }

    window.location.replace(url);
}