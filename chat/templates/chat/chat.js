var openedSocket, attachMessage, left = 'left', right = 'right',
    MessageEvents, Message, getMessageText,
    sendMessage, enableChatRoom,
    disableChatRoom;

Message = function (arg) {
    this.text = arg.text;
    this.messageSide = arg.messageSide;
    this.draw = function (_this) {
        return function () {
            var $message;
            $message = $($('.message_template').clone().html());
            $message.addClass(_this.messageSide).find('.text').html(_this.text);
            $('.messages').append($message);
            return setTimeout(function () {
                return $message.addClass('appeared');
            }, 0);
        };
    }(this);
    return this;
};

enableChatRoom = function () {
    $('.message_input').removeAttr('disabled').attr('placeholder', 'Please Type Your Message...');
    $('.send_message').removeClass('disabled');
};

disableChatRoom = function () {
    $('.message_input').prop('disabled', 'disabled').removeAttr('placeholder');
    $('.send_message').addClass('disabled');
};

getMessageText = function () {
    var $message_input;
    $message_input = $('.message_input');
    return $message_input.val();
};

sendMessage = function (text) {
    openedSocket.send(text);
};
attachMessage = function (text, side) {
    var $messages, message;
    message = new Message({
        text: text,
        messageSide: side
    });
    $messages = $('.messages');
    if (side === left) {
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
    onMessage: function (event) {
        console.log('onMessage', event);
        attachMessage(event.data, left);
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

    }
};

$(document).ready(function () {
    openedSocket = new Socket(MessageEvents);
});