import csv
from shop.models import Brand

file_path = r'D:\Game Hunter\hunterbackend\Game Hunter\Product CSV Files for Upload\product for upload - 1.csv'
with open(file_path, 'r', encoding='utf-8', errors='ignore') as output_file:
        fields = ['Developer', 'Description', "Is_Developer", "Is_Publisher"]
        csv_file = csv.DictReader(output_file, fieldnames=fields)
        next(csv_file)

        for row in csv_file:
            if row.get("Developer"):
                if row.get("Is_Developer") == "Yes":
                    dev = True
                else:
                    dev = False
                if row.get("Is_Publisher") == "Yes":
                    pub = True
                else:
                    pub = False
                developer = row.get("Developer").strip()
                description = row.get("Description").strip()
                obj = Brand.objects.create(name=developer, description=description, is_developer=dev, is_publisher=pub)
        print("All Data Save Successfully")
