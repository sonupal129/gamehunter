from shop.models import *
import csv

file = r"/home/hunteradmin/hunter/gamehunter/media/csv_file_uploads/url_updator.csv"

with open(file, 'r') as inputfile:
      fields = ["ID", "url"]
      csv_reader = csv.DictReader(inputfile, fieldnames=fields)
      attr = Attribute.objects.get(name="source_url")
      for reader in csv_reader:
            try:
                  product = Product.objects.get(id=int(reader.get("ID")))
            except:
                  continue
            product_attribute = ProductAttribute.objects.get_or_create(attribute=attr, product=product, value=reader.get("url"))
      print ("DONE")