var openedSocket, attachMessage, left = 'left', right = 'right',
    MessageEvents, Message, getMessageText,
    sendMessage, enableChatRoom, scrollHeight,
    disableChatRoom, retrieveMessages;

Message = function (arg) {
    this.text = arg.text;
    this.messageSide = arg.messageSide;
    this.datetime = arg.datetime;
    this.draw = function (_this) {
        return function () {
            var $message;
            $message = $($('.message_template').clone().html());
            $message.addClass(_this.messageSide).find('.text').html(_this.text);
            $message.find(".datetime").addClass(_this.messageSide)
                .attr('title', _this.datetime.split(".")[0])
                .text(_this.datetime.split(" ")[1].split(".")[0]);
            $('.messages').append($message);
            return setTimeout(function () {
                return $message.addClass('appeared');
            }, 0);
        };
    }(this);
    return this;
};

scrollHeight = function () {
    var $message = $('.messages');
    $message.animate({
        scrollTop: $message.prop('scrollHeight')
    }, 300);

};

enableChatRoom = function () {
    $('.message_input').removeAttr('disabled')
        .attr('placeholder', 'تایپ کنید...')
        .focus();
    $('.send_message').removeClass('disabled');
    $('#buddy').text(buddy);
    scrollHeight();
};

disableChatRoom = function () {
    $('.message_input').prop('disabled', 'disabled').removeAttr('placeholder');
    $('.send_message').addClass('disabled');
    $('#buddy').text('');
};

getMessageText = function () {
    var $message_input;
    $message_input = $('.message_input');
    return $message_input.val();
};

retrieveMessages = function (callback) {
    $.ajax({
        method: "GET",
        url: buddy + "/retrieve"
    }).done(function (success) {
        success.chats.forEach(function (value) {
            attachMessage(value.fields, true);
        });
        if (typeof callback === 'function') {
            callback();
        }
    })
};

sendMessage = function (text) {
    openedSocket.send(text);
};

attachMessage = function (data, scrollHeightFlag) {
    var user = (Array.isArray(data.user)) ? data.user[0] : data.user;
    var side = (user === username) ? 'right' : 'left';
    var text = data.text;
    var $messages, message;
    message = new Message({
        text: text,
        messageSide: side,
        datetime: data.datetime.replace("T", " ")
    });
    if (side === right) {
        if (text.trim() === '') {
            return;
        }
        $('.message_input').val('');
    }
    message.draw();
    if (scrollHeightFlag !== true) {
        scrollHeight();
    }
};

$('.send_message').click(function () {
    sendMessage(getMessageText(), left);
});

$('.message_input').keyup(function (e) {
    if (e.which === 13) {
        sendMessage(getMessageText(), left);
    }
});

MessageEvents = {
    buddy: buddy,
    onMessage: function (event) {
        var data = event.data.replaceAll("\'", "\"");
        data = JSON.parse(data);
        if (!data.hasOwnProperty('error')) {
            attachMessage(data);
        } else {
            console.log(data);
        }
    },
    onOpen: function (event) {
        console.log('onOpen', event);
        retrieveMessages(function () {
            enableChatRoom();
        });
    },
    onError: function (event) {
        console.log('onError', event);
    },
    onClose: function (event) {
        console.log('onClose', event);
        disableChatRoom();
    },
    sendMiddleware: function (data) {
        return JSON.stringify({"text": data});
    }
};

$(document).ready(function () {
    openedSocket = new Socket(MessageEvents);
});