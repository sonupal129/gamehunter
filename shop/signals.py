from django.dispatch import Signal
# Code Starts from Here


new_user_profile_created = Signal(providing_args=["user"])