from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .models import Products, Category

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        # {'title': "Войти", 'url_name': 'login'}
        ]

number = 30

def search(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Products.objects.filter(Q(title__icontains=search_query))
    else:
        posts = Products.objects.all().order_by('-price')
    return posts

def paginator(request, posts, number):
    p = Paginator(posts, number)
    page_number = request.GET.get('page')
    page_range = p.page_range
    ln = p.num_pages
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return [page_obj, page_range, ln]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs

        cats = Category.objects.all()
        context['menu'] = menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context


class ProductsHome(DataMixin, ListView):
    model = Products
    template_name = 'shopmain/about.html'
    context_object_name = 'page_obj'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        context['menu'] = menu
        return context
    def get_queryset(self):
        return Products.objects.filter(title__icontains='дрель')


def index(request):
    posts = search(request)
    page_obj = paginator(request, posts, number)
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
        'page_obj': page_obj[0],
        'page_range': page_obj[1],
        'ln': page_obj[2],
    }
    return render(request, 'shopmain/index.html', context=data)


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Products.objects.filter(cat_id=category.pk)
    page_obj = paginator(request, posts, number)

    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
        'page_obj': page_obj[0],
        'page_range': page_obj[1],
        'ln': page_obj[2],
    }
    return render(request, 'shopmain/index.html', context=data)


def show_post(request, post_slug):
    post = get_object_or_404(Products, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'shopmain/post.html', data)


def addpage(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'shopmain/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'shopmain/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))
    def get_success_url(self):
      return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')
