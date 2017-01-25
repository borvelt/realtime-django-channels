var NotificationsEvent, notificationsSocket, showNotifications,
    increaseUserNotificationsBadge,
    addUserNotificationList, retrieveNotifications;
NotificationsEvent = {
    address: '/stream/chat/bindings',
    onOpen: function (event) {
        console.log('onOpen', event);
        retrieveNotifications();
    },
    onMessage: function (event) {
        var data = JSON.parse(event.data);
        console.log(data);
        if (!data.hasOwnProperty('error') && data.stream === 'notifications') {
            showNotifications(data.payload.data);
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
increaseUserNotificationsBadge = function () {
    var $userNotification = $("*[data-notification]");
    $userNotification.data("notification", parseInt($userNotification.data("notification")) + 1);
    $userNotification.text($userNotification.data("notification"));
};
addUserNotificationList = function (data) {
    var $notifications = $(".notifications-list");
    var $notification = $($(".notification-list-template").clone().html());
    $notification.find(".text-semibold").text(data.user[0]);
    $notification.find(".media-annotation").text(data.datetime.split("T")[1].split(".")[0]);
    $notification.find(".text-muted").text(data.text);
    if (data.isAjax) {
        $notifications.append($notification);
    } else {
        $notifications.prepend($notification);
    }

};
showNotifications = function (data, fromAjax) {
    data.isAjax = fromAjax;
    if (data.isAjax || (data.room !== room && data.is_seen === false)) {
        increaseUserNotificationsBadge();
        addUserNotificationList(data);
    }
};
retrieveNotifications = function () {
    $.ajax({
        method: "GET",
        url: "notifications"
    }).done(function (success) {
        success.notifications.forEach(function (value) {
            showNotifications(value.fields, true);
        });
        if (typeof callback === 'function') {
            callback();
        }
    })
};
$(document).ready(function () {
    notificationsSocket = new Socket(NotificationsEvent);
});