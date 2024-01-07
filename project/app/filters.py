from .models import Product
from django_filters import FilterSet


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'product_name': ['icontains'],
            'quantity': ['gt'],
            'price': ['gt',
                      'lt', ],
        }
