from datetime import datetime
from django.shortcuts import render
from .filters import ProductFilter
from .forms import ProductForm
from .models import Product
from django.views.generic import ListView, DetailView, CreateView
from django.core.cache import cache


class ProductsList(ListView):
    model = Product
    ordering = 'product_name'
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 4

    #Фильтры на страничке
    def get_queryset(self):
        #идем в родительский класс
        queryset = super().get_queryset()
        self.filterset  = ProductFilter(self.request.GET,queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class ProductDetail(DetailView):
    template_name = 'product.html'
    queryset = Product.objects.all()

    def get_object(self,  *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)
            return obj


class ProductCreate(CreateView):
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'



