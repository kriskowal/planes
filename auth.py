
from planes.lazy import BaseService
from planes.response import Restricted, Forbidden

#todo implement retries

class Service(BaseService):

    Forbidden = Forbidden
    Restricted = Restricted
    realm_name = 'Restricted'

    def __init__(
        self,
        service,
        realm_name = None,
        Forbidden = None,
        Restricted = None,
        *args,
        **kws
    ):
        self.service = service
        if realm_name is not None: self.realm_name = realm_name
        if Forbidden is not None: self.Forbidden = Forbidden
        if Restricted is not None: self.Restricted = Restricted
        super(Service, self).__init__(*args, **kws)

    def __call__(self, kit, *args, **kws):
        username, password = kit.username_claim, kit.password_claim
        if (not username and not password):
            return self.Restricted(self.realm_name)
        elif not self.authenticate(username, password):
            return self.Forbidden(self.realm_name)
        else:
            return self.service(kit, *args, **kws)

    def authenticate(self, username, password):
        return False

AuthService = Service
