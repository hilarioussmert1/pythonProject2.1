from datetime import datetime
from django.shortcuts import render
from .filters import ProductFilter
from .forms import ProductForm
from .models import Product
from django.views.generic import ListView, DetailView, CreateView


class ProductsList(ListView):
    model = Product
    ordering = 'product_name'
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 2

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
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'


class ProductCreate(CreateView):
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'



