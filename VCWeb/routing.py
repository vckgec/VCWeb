from channels import include

# The channel routing defines what channels get handled by what consumers,
# including optional matching on message attributes. In this example, we match
# on a path prefix, and then include routing from the chat module.
channel_routing = [
    # Include sub-routing from an app.
    include("chat.routing.websocket_routing", path=r"^/chat"),
    include("mess.routing.websocket_routing", path=r"^/mess"),
    include("library.routing.websocket_routing", path=r"^/library"),
    include("account.routing.websocket_routing", path=r"^/account"),
]