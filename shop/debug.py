from django.utils import timezone
from django.http import HttpResponse
from .models import *
from django_slack import slack_message

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
                context = {
                    "time": timezone.now(),
                    "view_name": view_name,
                    "exception": str(e.__class__),
                    "message": str(e),
                }
                slack_message("shop/slack-notifications/error-notification.html", context)
                return HttpResponse(status=500)

        return wrapped_view

    return real_decorator
