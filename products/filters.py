import django_filters
from .models import Variants,Products

class ProductFilter(django_filters.FilterSet):
    size = django_filters.CharFilter(field_name='variants__size__code')
    print("+++++++++++++++++++SIZE+++++++++++++++++++++++",size)
    color = django_filters.CharFilter(field_name='variants__color__name')
    brand = django_filters.CharFilter(field_name='variants__products__product_brand__brand_title')
    class Meta:
        model = Products
        fields = ['product_brand','size', 'color', 'price']