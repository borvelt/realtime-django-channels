from channels import include

channel_routing = [

    include("chat.routing.websocket_routing",
            path=r"^/stream/chat"),

    include("chat.routing.custom_routing")

]
