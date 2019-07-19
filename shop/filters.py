import django_filters
from shop.models import Product, Brand, Genre
from django import forms

def filtered_products(request):
      products = Product.objects.filter(developer__isnull=False).values_list('developer', flat=True).distinct()
      return products



class ProductFilter(django_filters.FilterSet):
      developer = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple)
      publisher = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple)
      genre = django_filters.ModelMultipleChoiceFilter(queryset=Genre.objects.all(), widget=forms.CheckboxSelectMultiple)
      
      class Meta:
            model = Product
            fields = ["developer", "publisher", "genre"]