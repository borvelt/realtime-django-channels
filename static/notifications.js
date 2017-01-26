var NotificationsEvent, notificationsSocket, showNotifications,
    increaseUserNotificationsBadge, checkNotification, packNotificationsList,
    addUserNotificationList, retrieveNotifications, markAsRead;
NotificationsEvent = {
    address: '/stream/chat/bindings',
    onOpen: function (event) {
        retrieveNotifications();
    },
    onMessage: function (event) {
        var data = JSON.parse(event.data);
        console.log(data);
        if (!data.hasOwnProperty('error') && data.stream === 'notifications' && data.payload.action === 'create') {
            checkNotification(data);
            showNotifications(data.payload.data);
        }
    },
    onError: function (event) {
    },
    onClose: function (event) {
    },
    sendMiddleware: function (data) {

    }
};
checkNotification = function (data) {
    if (data.payload.data.room === room) {
        markAsRead(data);
    }
};
markAsRead = function (data) {
    console.log(data.pk);
    notificationsSocket.send(JSON.stringify({
        "stream": data.stream,
        "payload": {
            "pk": data.payload.pk,
            "action": "update",
            "data": {
                "is_seen": true
            }
        }
    }));
};
increaseUserNotificationsBadge = function () {
    var $userNotification = $("*[data-notification]");
    $userNotification.data("notification", parseInt($userNotification.data("notification")) + 1);
    $userNotification.text($userNotification.data("notification"));
};
addUserNotificationList = function (data) {
    var $notifications = $(".notifications-list");
    var $notification = $($(".notification-list-template").clone().html());
    $notification.attr('user', data.user[0]);
    $notification.find(".notification-link").attr('href', '/chat/' + data.user[0]);
    $notification.find(".text-semibold").text(data.user[0]);
    $notification.find(".media-annotation").text(data.datetime.split("T")[1].split(".")[0]);
    $notification.find(".text-muted").text(data.text);
    if (typeof data.numOfItems !== typeof undefined) {
        $notification.find(".collected-item").text(data.numOfItems);
    }
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
    window['notifications_attached'] = true;
};
packNotificationsList = function () {
    var list = {};
    $('li[user]').each(function (i, el) {
        var $el = $(el);
        var user = $el.attr('user');
        if (list.hasOwnProperty(user)) {
            list[user].count += 1;
        } else {
            list[user] = {};
            list[user].count = 1;
        }
        list[user].lastData = $el;
    });
    for (var key in list) {
        var user = list[key].lastData.find('.text-semibold').text();
        $(".notifications-list li[user='" + user +"']").remove();
        list[key].lastData.find('.collected-item').text(list[key].count);
        $(".notifications-list").append(list[key].lastData);
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
        packNotificationsList();
        if (typeof callback === 'function') {
            callback();
        }
    })
};
$(document).ready(function () {
    notificationsSocket = new Socket(NotificationsEvent);
});