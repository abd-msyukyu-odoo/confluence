from django.http import HttpResponseServerError
from django.utils.itercompat import is_iterable
import threading

class Sudo:
    def __init__(self, **kwargs):
        self.local = threading.local()

    def __enter__(self):
        if not hasattr(self.local, 'env'):
            return None
        if not self.local.env.is_superuser:
            self.local.env.is_sudo = True
        return self.local.env.is_superuser

    def __exit__(self, **kwargs):
        if not hasattr(self.local, 'env'):
            return
        if not self.local.env.is_superuser:
            self.local.env.is_sudo = False

class Environment:
    def __init__(self, user):
        if not user:
            self.uid = None
            return
        self.uid = user.id
        self.permissions = user.get_all_permissions()
        self.is_superuser = user.is_active and user.is_superuser
        self.is_sudo = self.is_superuser

    def has_perm(self, perm):
        if not self.uid:
            return True
        if self.is_sudo:
            return True
        return perm in self.permissions

    def has_perms(self, perm_list):
        if not is_iterable(perm_list) or isinstance(perm_list, str):
            raise ValueError("perm_list must be an iterable of permissions.")
        return all(self.has_perm(perm) for perm in perm_list)

class EnvironmentMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.local = threading.local()
        if hasattr(request.local, 'env'):
            raise HttpResponseServerError("There was an unrecoverable error during the handling of your request, please reload and try again...")
        if request.user and request.user.is_authenticated:
            request.local.env = Environment(request.user)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        if hasattr(request.local, 'env'):
            del request.local.env

        return response

    def process_exception(self, request, exception):
        if hasattr(request.local, 'env'):
            del request.local.env
