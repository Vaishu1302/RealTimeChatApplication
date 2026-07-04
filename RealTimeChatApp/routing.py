from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({

    "websocket":
    URLRouter(
        websocket_urlpatterns
    ),
})
