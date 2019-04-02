from django.utils import timezone
from django.http import HttpResponse
from .models import *


def log_exceptions(view_name):
    """
        Logs all the exceptions occuring in a Django view, to the
        ExceptionLog model.
        'view_name' denotes an identifier for the view that is
        being debug-logged.
        """
    def real_decorator(actual_view):
        """This is the actual decorator."""

        def wrapped_view(request):
            """
            This is the version of the view that will monitor
            itself for any un-expected Exception, and maintain basic
            logs of the same.
            """
            try:
                response = actual_view(request)
                print(actual_view)
                return response
            except Exception as e:
                debug_entry = ExceptionLog(timestamp=timezone.now(), views=view_name,
                                           exceptionclass=str(e.__class__), message=str(e))
                debug_entry.save()
                print("Kuch To Locha Hai JO Samajh Nahi Aa raha hai")
                return HttpResponse(status=500)

        return wrapped_view

    return real_decorator
