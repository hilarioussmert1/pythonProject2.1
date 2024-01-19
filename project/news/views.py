from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (ListView, DetailView, UpdateView, DeleteView)
from django.views.generic.edit import CreateView
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from .tasks import send_notifications, notify_about_new_post


class NewsList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news/news.html'
    context_object_name = 'news'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


class NewDetail(DetailView):
    model = Post
    template_name = 'news/new.html'
    context_object_name = 'new'


class NewsSearch(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news/news_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/news_create.html'

    def form_valid(self, form):
        new = form.save(commit=False)
        if self.request.path == '/news/articles/create/':
            new.article_news = 'AR'
        new.save()
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/news_create.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list')


class ProtectedView(LoginRequiredMixin, TemplateView):
    model = Post
    template_name = 'news_create.html'
    form_class = PostForm
    login_url = 'news'


class CategoryView(NewsList):
    model = Post
    template_name = "news/categories.html"
    context_object_name = "category_news_list"

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs["pk"])
        queryset = Post.objects.filter(post_category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_not_subscriber"] = (
                self.request.user not in self.category.subscribers.all()
        )
        context["category"] = self.category
        return context


class CategoryList(ListView):
    model = Category
    template_name = 'news/categories.html'
    context_object_name = 'category_list'


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    category.subscribers.add(user)
    return redirect("category_list")


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(user)
    return redirect("category_list")


class IndexView(View):
    def get(self, request):
        send_notifications.delay()
        notify_about_new_post.delay()
        return HttpResponse('Hello!')
