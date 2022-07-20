from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .forms import LoginForm
# 17.07.22
from set_first.tasks import supper_sum
from .models import Post
from django.utils import timezone
from .forms import PostForm

menu = ["О сайте", "Обратная связь", "Войти", "Регистрация"]


class PostList(ListView):
    queryset = Post.objects.all()
    context_object_name = 'post_list'
    template_name = 'blog/post_list.html'
    paginate_by = 4

    def get_paginate_by(self, queryset):
        return self.paginate_by

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_post(self, pk):
        return get_object_or_404(Post, pk=pk)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Подробно'
        context['menu'] = menu
        return context

class PostNew(FormView):
    form_class = PostForm
    success_url = 'post_detail'
    template_name = 'blog/post_new.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Добавить статью'
        context['menu'] = menu
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.instance.pk})


class PostEdit(UpdateView):
    model = Post
    fields = ['title', 'text']
    success_url = 'post_detail'
    template_name = 'blog/post_edit.html'

    def get_post(self, pk):
        return get_object_or_404(Post, pk=pk)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Редактирование'
        context['menu'] = menu
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})
