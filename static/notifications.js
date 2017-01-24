var notificationsSocket;
var NotificationsEvent = {
    address: '/stream/chat/bindings',
    onOpen: function (event) {
        console.log('onOpen', event);
    },
    onMessage: function (event) {
        console.log(event.data);
        var data = JSON.parse(event.data);
        if (!data.hasOwnProperty('error')) {

        } else {
            console.log(data);
        }
    },
    onError: function (event) {
        console.log('onError', event);
    },
    onClose: function (event) {
        console.log('onClose', event);
    },
    sendMiddleware: function (data) {

    }
};
$(document).ready(function () {
    notificationsSocket = new Socket(NotificationsEvent);
});