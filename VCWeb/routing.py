from channels import include
from mess.views import Boarder_Update

Boarder_Update()

# The channel routing defines what channels get handled by what consumers,
# including optional matching on message attributes. In this example, we match
# on a path prefix, and then include routing from the chat module.
channel_routing = [
    # Include sub-routing from an app.
    include("chat.routing.websocket_routing", path=r"^/chat"),
    include("mess.routing.websocket_routing", path=r"^/mess"),
    include("account.routing.websocket_routing", path=r"^/account"),
]
