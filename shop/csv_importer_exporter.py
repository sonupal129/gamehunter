import csv
from .models import *
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist


def upload_products(filepath):
    inputfile = open(filepath, 'r', encoding='utf-8', errors="ignore")
    reader = csv.DictReader(inputfile)
    games_category = ["PS 4", "PS 3", "Xbox One", "Xbox 360"]

    for row in reader:
        data = {"name": row.get("Name"), "category": Category.objects.get(name__iexact=row.get("Category")),
                "description": row.get("Description"), "launch_date": row.get("Launch Date"),
                "item_status": row.get("Item Status"), "genre": row.get("Genre", None),
                "condition": row.get("Condition"), "developer": row.get("Developer", None),
                "publisher": row.get("Publisher", None), "manufacturer": row.get("Manufacturer", None),
                "mrp": row.get("MRP"), "discount": row.get("Discount"), "hunter_discount": row.get("Hunter Discount"),
                "delivery_charges": row.get("Delivery Charges")}
        if row.get("Active") == "Yes":
            data["active"] = True
        else:
            data["active"] = False
        if row.get("Featured") == "Yes":
            data["is_featured"] = True
        else:
            data["is_featured"] = False
        if row.get("Category") in games_category:
            name = data.get("name")
            category = data.get("category")
            try:
                product = Product.objects.get(name=name, category=category)
            except ObjectDoesNotExist("Product Not Found Creating New Produt"):
                product = product.objects.create(**data)
                prod_plan = Plan.objects.get(name__iexact=row.get("Plan", ""))
                product.plan.add(prod_plan)
            else:
                product.update(**data)
                product.save()
        else:
            raise ObjectDoesNotExist
            print("Category Is Not Available")
    return "Product Added Successfully"


