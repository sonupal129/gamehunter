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
        data["hunter_discount"] = int(row.get("Hunter Discount"))
        data["delivery_charges"] = int(row.get("Delivery Charges"))
        if row.get("Item Status") == "I":
            item_status = "I"
        else:
            item_status = "O"
        if row.get("Active") == "Yes":
            data["active"] = True
        else:
            data["active"] = False
        if row.get("Featured") == "Yes":
            data["is_featured"] = True
        else:
            data["is_featured"] = False
        if row.get("Developer"):
            data["developer"] = Brand.objects.get(name__iexact=row.get("Developer"), is_developer=True)
        else:
            data["developer"] = None
        if row.get("Publisher"):
            data["publisher"] = Brand.objects.get(name__iexact=row.get("Publisher"), is_publisher=True)
        else:
            data["publisher"] = None
        if row.get("Manufacturer"):
            data["manufacturer"] = Brand.objects.get(name__iexact=row.get("Manufacturer"), is_manufacturer=True)
        else:
            data["manufacturer"] = None
        if row.get("Genre"):
            data["genre"] = Genre.objects.get(genre__iexact=row.get("Genre"))
        else:
            data["genre"] = None
        if row.get("Category") in games_category:
            category = Category.objects.get(name__iexact=row.get("Category"))
            data["category"] = category
            print(category)
            print(row.get("Name"))
            product = Product.objects.filter(name__iexact=row.get("Name"), category=category).first()
            print(product)
            if product:
                product.name = row.get("Name")
                product.description = data.get("description")
                product.launch_date = data.get("launch_date")
                product.item_status = item_status
                product.genre = data.get("genre")
                product.condition = data.get("condition")
                product.mrp = row.get("MRP")
                product.discount = data.get("discount")
                product.hunter_discount = data.get("hunter_discount")
                product.delivery_charges = data.get("delivery_charges")
                product.active = data.get("active")
                product.is_featured = data.get("is_featured")
                product.developer = data.get("developer")
                product.publisher = data.get("publisher")
                product.manufacturer = data.get("manufacturer")
                product.genre = data.get("genre")
                if row.get("Plan"):
                    prod_plan = Plan.objects.get(name__iexact=row.get("Plan", ""))
                    product.plan.add(prod_plan)
                product.save()
                product_updated += 1
            else:
                product = Product(name=row.get("Name"), item_status=item_status, mrp=row.get("MRP"),
                                                 category=data.get("category"), is_featured=data.get("is_featured"),
                                                 publisher=data.get("publisher"), active=data.get("active"))
                product.save()
                product.description = data.get("description")
                product.launch_date = data.get("launch_date")
                product.genre = data.get("genre")
                product.condition = data.get("condition")
                product.discount = data.get("discount")
                product.hunter_discount = data.get("hunter_discount")
                product.delivery_charges = data.get("delivery_charges")
                product.developer = data.get("developer")
                product.manufacturer = data.get("manufacturer")
                product.genre = data.get("genre")
                product.save()
                if row.get("Plan"):
                    prod_plan = Plan.objects.get(name__iexact=row.get("Plan", ""))
                    product.plan.add(prod_plan)
                new_product_added += 1
                time.sleep(1)
        else:
            raise ObjectDoesNotExist("Category Is Not Available")
    return f"{product_updated} products data updated & {new_product_added} new products added successfully"


