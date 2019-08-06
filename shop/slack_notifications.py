from django_slack import slack_message
from shop.models import User
from background_task import background
# Code Starts Below

@background(schedule=3, queue="default")
def new_user_registered(user_id):
    user = User.objects.get(id=user_id)
    
    context = {
            "user": user
        }
    return slack_message("shop/slack-notifications/new_user_registered.html", context)
