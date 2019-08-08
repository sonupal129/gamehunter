import django_filters
from shop.models import Product, Brand, Genre
from django import forms

def is_developer(field_name):
      brands = Brand.objects.all()
      products = Product.objects.filter(item_status__in=["I", "S"], active=True)
      if field_name == "developer":
            obj = brands.filter(id__in=products.values_list('developer', flat=True).distinct(), is_developer=True)
            return obj
      return brands

def is_publisher(field_name):
      brands = Brand.objects.all()
      products = Product.objects.filter(item_status__in=["I", "S"], active=True)
      if field_name == "publisher":
            obj = brands.filter(id__in=products.values_list('publisher', flat=True).distinct(), is_developer=True)
            return obj
      return brands

def filtered_genre(field_name):
      genres = Genre.objects.all()
      products = Product.objects.filter(item_status__in=["I", "S"], active=True)
      if field_name == "genre":
            obj = genres.filter(id__in=products.values_list('genre', flat=True).distinct())
            return obj
      return genres
      


class ProductFilter(django_filters.FilterSet):
      ordering_choices =  {
            ("date", "Newest first"),
            ("name", "Name (a-z)"),
            ("mrp", "Price (low to high)"),
      }

      developer = django_filters.ModelMultipleChoiceFilter(queryset=is_developer("developer"), widget=forms.CheckboxSelectMultiple)
      publisher = django_filters.ModelMultipleChoiceFilter(queryset=is_publisher("publisher"), widget=forms.CheckboxSelectMultiple)
      genre = django_filters.ModelMultipleChoiceFilter(queryset=filtered_genre("genre"), widget=forms.CheckboxSelectMultiple)
      sort_by = django_filters.ChoiceFilter(label="Sort By", choices=ordering_choices, method="get_sorted_products")
      # name = django_filters.CharFilter(field_name="name", label="Search", lookup_expr="icontains")
      # mrp = django_filters.RangeFilter(field_name='mrp')
      
      class Meta:
            model = Product
            fields = ["developer", "publisher", "genre"]

      def get_sorted_products(self, queryset, name, value):
            if value:
                  return queryset.order_by(value)
            return queryset

      
