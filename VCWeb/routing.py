from channels import include
from mess.views import Boarder_Update

Boarder_Update()

# The channel routing defines what channels get handled by what consumers,
# including optional matching on message attributes. In this example, we match
# on a path prefix, and then include routing from the chat module.
channel_routing = [
    # Include sub-routing from an app.
    include("chat.routing.websocket_routing", path=r"^/chat"),

    # Custom handler for message sending (see Room.send_message).
    # Can't go in the include above as it's not got a `path` attribute to match on.
    include("mess.routing.websocket_routing", path=r"^/mess"),

    # A default "http.request" route is always inserted by Django at the end of the routing list
    # that routes all unmatched HTTP requests to the Django view system. If you want lower-level
    # HTTP handling - e.g. long-polling - you can do it here and route by path, and let the rest
    # fall through to normal views.
]
