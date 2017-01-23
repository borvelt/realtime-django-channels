var openedSocket, attachMessage, left = 'left', right = 'right',
    MessageEvents, Message, getMessageText,
    sendMessage, enableChatRoom,
    disableChatRoom;

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

enableChatRoom = function () {
    $('.message_input').removeAttr('disabled')
        .attr('placeholder', 'تایپ کنید...')
        .focus();
    $('.send_message').removeClass('disabled');
    $('#buddy').text(buddy);
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

sendMessage = function (text) {
    openedSocket.send(text);
};
attachMessage = function (data) {
    var side = (data.user === username) ? 'right' : 'left';
    var text = data.body;
    var $messages, message;
    message = new Message({
        text: text,
        messageSide: side,
        datetime: data.datetime
    });
    $messages = $('.messages');
    if (side === right) {
        if (text.trim() === '') {
            return;
        }
        $('.message_input').val('');
    }
    message.draw();
    $messages.animate({scrollTop: $messages.prop('scrollHeight')}, 300);
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
        if(!data.hasOwnProperty('error')){
            attachMessage(data);
        } else {
            console.log(data);
        }
    },
    onOpen: function (event) {
        console.log('onOpen', event);
        enableChatRoom();
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