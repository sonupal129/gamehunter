import csv
from .models import *
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
        if row.get("Launch Date"):
            data["launch_date"] = row.get("Launch Date", "")
        data["condition"] = row.get("Condition")
        data["discount"] = int(row.get("Discount"))
        data["hunter_discount"] = int(row.get("Hunter Discount"))
        data["delivery_charges"] = int(row.get("Delivery Charges"))
        if row.get("Item Status") == "I":
            item_status = "I"
        elif row.get("Item Status") == "S":
            item_status = "S"
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
            product = Product.objects.filter(name__iexact=row.get("Name"), category=category).first()
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
                if row.get("Attribute: source_url"):
                    attribute = Attribute.objects.get(name="source_url")
                    ProductAttribute.objects.create(attribute=attribute, product=product, value=row.get("Attribute: source_url"))
                if row.get("Attribute: game_trailer"):
                    attribute = Attribute.objects.get(name="game_trailer")
                    product_attribute = ProductAttribute.objects.get_or_create(attribute=attribute, product=product)
                    if product_attribute:
                        product_attribute.value = row.get("Attribute: game_trailer")
                        product_attribute.save()
                product.save()
                product_updated += 1
            else:
                product = Product(name=row.get("Name"), item_status=item_status, mrp=row.get("MRP"),
                                  category=data.get("category"), is_featured=data.get("is_featured"),
                                  publisher=data.get("publisher"), active=data.get("active"))
                product.save()
                product.description = data.get("description")
                if row.get("Launch Date"):
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
                if row.get("Attribute: source_url"):
                    attribute = Attribute.objects.get(name="source_url")
                    ProductAttribute.objects.create(attribute=attribute, product=product, value=row.get("Attribute: source_url"))
                if row.get("Attribute: game_trailer"):
                    attribute = Attribute.objects.get(name="game_trailer")
                    product_attribute = ProductAttribute.objects.get_or_create(attribute=attribute, product=product)
                    if product_attribute:
                        product_attribute.value = row.get("Attribute: game_trailer")
                        product_attribute.save()
                new_product_added += 1
        else:
            raise ObjectDoesNotExist("Category Is Not Available")
    return f"{product_updated} products data updated & {new_product_added} new products added successfully"


