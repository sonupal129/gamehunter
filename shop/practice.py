my_file = r"/home/hunteradmin/hunter/gamehunter/media/csv_file_uploads/product_import_CWBlW0C.csv"
from shop.models import Product
import csv
with open(my_file, 'r') as inputfile:
      fields = ["ID", "MRP", "Active", "Status", "Discount"]
      csv_reader = csv.DictReader(inputfile, fieldnames=fields)
      next(csv_reader)
      for reader in csv_reader:
            product = Product.objects.get(id=int(reader.get("ID")))
            product.mrp = int(reader.get("MRP"))
            product.discount = int(reader.get("Discount"))
            product.status = reader.get("Status")
            product.active = True if reader.get("Active") == "Yes" else False
            product.save()
            print(product)
      print("All Done")