from django.apps import AppConfig
# code starts from here


class ShopConfig(AppConfig):
    name = 'shop'

    def ready(self):
        print("App is Ready")
        import shop.signals
        import shop.emails
        import carts.signals
        import carts.emails
