# import csv
# from shop.models import Product, Attribute
# file_path = r'D:\GH Operation\Product CSV Files for Upload\Subscription Only Product Uploading\games_trailor.csv'
#
#
# def upload_trailer(file):
#     with open(file, 'r', encoding='utf-8', errors='ignore') as input_file:
#             fields = ['Name', 'Trailer', 'Category']
#             csv_file = csv.DictReader(input_file, fieldnames=fields)
#             next(csv_file)
#             count = 0
#             for row in csv_file:
#                 if row.get("Trailer") and row.get("Name"):
#                     print(row.get("Trailer"))
#                     print(row.get("Name"))
#                     print(row.get("Category"))
#                     pd = Product.objects.filter(name__iexact=row.get("Name"), category__name__iexact=row.get("Category")).first()
#                     attribute = Attribute.objects.get(attribute="game_trailer")
#                     if pd:
#                         print(pd)
#                         print(pd.category)
#                         pd.productattribute.create(attribute=attribute, product=pd, value=row.get("Trailer"))
#                         count += 1
#                     continue
#                 continue
#             print(f"{count} Products Trailer Saved in System")



name = "/assassins-creed-syndicate-by-ubisoft-for-ps-4"

print(name.replace("/", ""))