// document.addEventListener('DOMContentLoaded', () =>{
//      var socket = io();


// });
var socket = io({autoconnect: false});
     document.getElementById("message-box")
     document.getElementById("username")
     document.getElementById("login-btn").addEventListener("click", () =>{
        let username = document.getElementById("us ername").value
     })
var currentRoom = null;
    socket.connect()