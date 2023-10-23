export const eel = window.eel;
eel.set_host("ws://127.0.0.1:8888");



eel.expose(Auth_setBlDisconnected);
function Auth_setBlDisconnected() {
    window.dispatchEvent(blTimeout);
}

eel.expose(bl_is_connected);
function bl_is_connected() {
    console.log("Bluetooth connection established");
    window.dispatchEvent(blConnected);
}


/* Custom Events */

const blTimeout = new CustomEvent('blTimeout', { detail: { message: 'Bluetooth connection timeout' } });
const blConnected = new CustomEvent('blConnected', { detail: { message: 'Bluetooth connection established' } });