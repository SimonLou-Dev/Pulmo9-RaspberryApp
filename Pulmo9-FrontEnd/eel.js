export const eel = window.eel;




eel.expose(Auth_setBlDisconnected);
function Auth_setBlDisconnected() {
    console.log("Disconnected");
}

eel.expose(Auth_setBlConnected);
function Auth_setBlConnected() {
    console.log("Connected");
}