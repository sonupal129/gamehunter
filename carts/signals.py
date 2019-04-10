from django.dispatch import Signal
# Code Starts from Here

order_payment_received = Signal(providing_args=["cart_id", "payment_status"])
new_order_received = Signal(providing_args=["suborder"])
new_subscription_order_received = Signal(providing_args=["suborder"])



