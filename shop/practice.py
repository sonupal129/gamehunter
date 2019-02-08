from shop.models import Brand

import csv


file_path = r'C:\Users\Sonu\Desktop\Python Test\pt.csv'
with open(file_path, 'r', encoding='utf-8', errors='ignore') as output_file:
        fields = ['Developer', 'Description']
        csv_file = csv.DictReader(output_file, fieldnames=fields)
        next(csv_file)

        for i in csv_file:
            developer = i.get("Developer").strip()
            description = i.get("Description").strip()
            obj = Brand.objects.create(name=developer, description=description, is_developer=True)
        print("All Data Save Successfully")
