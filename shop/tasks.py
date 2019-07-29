from shop.models import ProductAttribute, Product
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import time
from background_task import background

# Start Writing Functions Below

@background(queue='biweekly-task')
def product_updater():
    """This Function is A Task which update products mrp, discount and status from gametheshop on daily"""
    qs = ProductAttribute.objects.select_related('product').filter(attribute__name="source_url")
    for atr in qs:
        time.sleep(2)
        single_product_update(atr.value, atr.product)
    return "All Product Data Updated"


def single_product_update(url, product):
    """Takes url and product objects as parameter and updated product price from gametheshop"""
    try:
        read_url = urlopen(url).read()
        url_data = soup(read_url, "html.parser")
        product_data = url_data.find("div", {"id": "ctl00_ContentPlaceHolder1_divOfferDetails"})
    except:
        print("Wrong Url Provided")
        pass
    try:
        image = product_data.find("div", {"class": "prc-mn-dv"}).img["src"]
    except AttributeError:
        try:
            image = product_data.find("img", {"class": "vrt-mdl"}).get("src")
        except AttributeError:
            pass
    if image == "https://s3-ap-southeast-1.amazonaws.com/cdn.gamestheshop.com/image/offer-available.png":
        product.mrp = int(product_data.find("span", {"class": "lnr-thr mrp-nmbr"}).text.replace(",", ""))
        product.item_status = "I"
        product.discount = int(product_data.find("span", {"class": "tf-percnt"}).text.replace("%", ""))
    elif image == "https://s3-ap-southeast-1.amazonaws.com/cdn.gamestheshop.com/image/in-stock.png":
        product.mrp = int(url_data.find("td", {"class": "gt-pr-blk vrt-top"}).text.replace(",", ""))
        product.item_status = "I"
        product.discount = 0
    elif image == "https://s3-ap-southeast-1.amazonaws.com/cdn.gamestheshop.com/image/sold-out.png":
        product.item_status = "O"
    product.save()
    return f"{product.name} Data Updated"


# product_updater(repeat=Task.DAILY, )



