(function () {
    var Socket = function (event) {
        event = (typeof event === 'object') ? event : {};
        this.address = "ws://" + window.location.host + "/borvelt";
        this.address = event.hasOwnProperty('address') ? event.address : this.address;
        this.sendMiddleware = event.hasOwnProperty('sendMiddleware') ? event.sendMiddleware : null;
        this.closeMiddleware = event.hasOwnProperty('closeMiddleware') ? event.closeMiddleware : null;
        this._socket = new WebSocket(this.address);
        this._socket.onmessage = event.hasOwnProperty('onMessage') ? event.onMessage : null;
        this._socket.onopen = event.hasOwnProperty('onOpen') ? event.onOpen : null;
        this._socket.onerror = event.hasOwnProperty('onError') ? event.onError : null;
        this._socket.onclose = event.hasOwnProperty('onClose') ? event.onClose : null;
        this.send = function (data, next) {
            var middlewareResponse;
            if (this.sendMiddleware) {
                middlewareResponse = this.sendMiddleware(data);
                data = (typeof middlewareResponse !== 'undefined') ? middlewareResponse : data;
                this._socket.send(data);
                if (typeof next === 'function') {
                    next();
                }
                return;
            }
            this._socket.send(data);
        };
        this.close = function (next) {
            if (this.closeMiddleware) {
                this.closeMiddleware();
                this._socket.close();
                if (typeof next === 'function') {
                    next();
                }
                return;
            }
            this._socket.close();
        };
        return this;
    };
    window['Socket'] = Socket;
})();