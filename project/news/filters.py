from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from django import forms
from .models import Post, Category


class PostFilter(FilterSet):
    post_category = ModelChoiceFilter(
        field_name='category',
        required=False,
        queryset=Category.objects.all(),
        label='cCategory'
    )


    creation_time = DateFilter(
        field_name='release_date',
        widget=forms.DateInput(attrs={'type': 'date'}),
        lookup_expr='date__gte',
        label='Дата выпуска число которое позже данного',
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'post_category': ['exact'],
            'creation_time': ['exact'],
        }
