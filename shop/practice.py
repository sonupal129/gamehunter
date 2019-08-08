my_file = r"/home/hunteradmin/hunter/gamehunter/media/csv_file_uploads/product_export_7.csv"
from shop.models import Product, ProductAttribute, Attribute
import csv
with open(my_file, 'r') as inputfile:
      fields = ["ID", "Youtube Url"]
      csv_reader = csv.DictReader(inputfile, fieldnames=fields)
      next(csv_reader)
      attribute = Attribute.objects.get(name="game_trailer")
      for reader in csv_reader:
            product = Product.objects.get(id=int(reader.get("ID")))
            product_attribute = ProductAttribute.objects.get_or_create(attribute=attribute, product=product)
            product_attribute[0].value = reader.get("Youtube Url")
            product_attribute[0].save()
            print(product)
      print("All Done")