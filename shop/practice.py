

class Mobile:
      def __init__(self, name, model, price)
            self.name = name
            self.model = model
            self.price = price

      def get_complete_details(self):
            return f"Phone {self.name}, {self.model} at rupee {self.price} only!"

class Laptop:
      def __init__(self, name, model, price)
            self.name = name
            self.model = model
            self.price = price

      def get_complete_details(self):
            return f"Phone {self.name}, {self.model} at rupee {self.price} only!"

class Product:
      mobile = None
      laptop = None

      def __init__(self):
            self.mobile = Mobile("Nokia", "1100", 2500)
            self.laptop = Laptop("HP", "Pavellion", 10000)

      def get_mobile(self):
            return self.mobile

