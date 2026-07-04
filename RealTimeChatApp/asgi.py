from chat.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
import os

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'RealTimeChatApp.settings'
)


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({

    "http": django_asgi_app,

    "websocket": AuthMiddlewareStack(

        URLRouter(
            websocket_urlpatterns
        )

    ),

})
