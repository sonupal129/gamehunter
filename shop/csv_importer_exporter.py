import csv
from .models import *
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import time

def upload_products(filepath):
    inputfile = open(filepath, 'r', encoding='utf-8', errors="ignore")
    reader = csv.DictReader(inputfile)
    games_category = [c.name for c in Category.objects.all()]
    product_updated = 0
    new_product_added = 0
    data = {}
    for row in reader:
        data["description"] = row.get("Description")
        data["launch_date"] = row.get("Launch Date", "")
        data["condition"] = row.get("Condition")
        data["discount"] = int(row.get("Discount"))
        print(data.get("discount"))
        data["hunter_discount"] = int(row.get("Hunter Discount"))
        data["delivery_charges"] = int(row.get("Delivery Charges"))
        if row.get("Item Status") == "I":
            item_status = "I"
            print(row.get("Item Status"))
        else:
            item_status = "O"
        if row.get("Active") == "Yes":
            data["active"] = True
        else:
            data["active"] = False
        print(data.get("active"))
        if row.get("Featured") == "Yes":
            data["is_featured"] = True
        else:
            data["is_featured"] = False
        if row.get("Developer"):
            data["developer"] = Brand.objects.get(name__iexact=row.get("Developer"), is_developer=True)
        else:
            data["developer"] = None
        print(data.get("developer"))
        if row.get("Publisher"):
            data["publisher"] = Brand.objects.get(name__iexact=row.get("Publisher"), is_publisher=True)
        else:
            data["publisher"] = None
        print(data.get("publisher"))
        if row.get("Manufacturer"):
            data["manufacturer"] = Brand.objects.get(name__iexact=row.get("Manufacturer"), is_manufacturer=True)
        else:
            data["manufacturer"] = None
        print(data.get("manufacturer"))
        if row.get("Genre"):
            data["genre"] = Genre.objects.get(genre__iexact=row.get("Genre"))
        else:
            data["genre"] = None
        if row.get("Category") in games_category:
            category = Category.objects.get(name__iexact=row.get("Category"))
            print(category)
            data["category"] = category
            print(data.get("category"))
            product = Product.objects.filter(name__iexact=data.get("name"), category=category).first()
            if not product:
                product = Product.objects.create(name=row.get("Name"), item_status=item_status, mrp=row.get("MRP"), active=False)
                print(product)
                time.sleep(1)
                # product.name = row.get("Name")
                # product.description = data.get("description")
                # product.launch_date = data.get("launch_date")
                # product.item_status = item_status
                # product.genre = data.get("genre")
                # product.condition = data.get("condition")
                # product.mrp = row.get("MRP")
                # product.discount = data.get("discount")
                # product.hunter_discount = data.get("hunter_discount")
                # product.delivery_charges = data.get("delivery_charges")
                # product.active = data.get("active")
                # product.is_featured = data.get("is_featured")
                # product.developer = data.get("developer")
                # product.publisher = data.get("publisher")
                # product.manufacturer = data.get("manufacturer")
                # product.genre = data.get("genre")
                # prod_plan = Plan.objects.get(name__iexact=row.get("Plan", ""))
                # product.plan.add(prod_plan)
                # product.save()
                # product_updated += 1
            #     pass
            # else:
            #     product = Product.objects.create(name=row.get("Name"), item_status=item_status, mrp=row.get("MRP"))
            #     print(data)
            #     # product.description = data.get("description")
                # product.launch_date = data.get("launch_date")
                # product.genre = data.get("genre")
                # product.condition = data.get("condition")
                # product.discount = data.get("discount")
                # product.hunter_discount = data.get("hunter_discount")
                # product.delivery_charges = data.get("delivery_charges")
                # product.active = data.get("active")
                # print(data.get("active"))
                # product.is_featured = data.get("is_featured")
                # product.developer = data.get("developer")
                # product.publisher = data.get("publisher")
                # product.manufacturer = data.get("manufacturer")
                # product.genre = data.get("genre")
        #         product.save()
        #         prod_plan = Plan.objects.get(name__iexact=row.get("Plan", ""))
        #         product.plan.add(prod_plan)
        #         new_product_added += 1
        # else:
        #     raise ObjectDoesNotExist("Category Is Not Available")
    return f"{product_updated} products data updated & {new_product_added} new products added successfully"


