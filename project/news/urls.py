from django.urls import path
from .views import (NewsList, NewDetail, NewsSearch, NewsCreate, NewsUpdate, NewsDelete, CategoryView, subscribe,
                    unsubscribe, CategoryList, IndexView)
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(5)(NewsList.as_view()), name='news_list'),
    path('<int:pk>', cache_page(300)(NewDetail.as_view()), name='news_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', NewsCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', NewsUpdate.as_view(), name='articles_update'),
    path('articles/<int:pk>/delete/', NewsDelete.as_view(), name='articles_delete'),
    path('category/', CategoryList.as_view(), name='category_list'),
    path('category/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('category/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
    path('index/', IndexView.as_view, name='index')
]