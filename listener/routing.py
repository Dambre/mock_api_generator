from . import views
from .validators.messages import messages


# Routing by msg-id
def get_route(msg_id):
    _r = PREDEFINED_ROUTES.get(msg_id, None)
    if _r:
        return _r

    # I have added check if msg does not have custom view assigned
    # method returns GenericView or None

    if messages.get(msg_id, None):
        return views.GenericView
    return None


PREDEFINED_ROUTES = {
    'msgBookRide': views.BookRide,

    # Auth
    'msgRegisterUser': views.RegisterUser,
}
