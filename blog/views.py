from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from my_user.models import MyUser
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


class ChangeUserInfoView(UpdateView):
    model = MyUser
    template_name = 'blog/profile_edit.html'
    success_url = 'profile'
    fields = ['birthday', 'first_name']

    def get_post(self, pk):
        return get_object_or_404(Post, pk=pk)

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['menu'] = menu
        return context

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})

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


class UserLogin(LoginView):
    template_name = 'blog/login.html'


class UserLoginOut(LoginRequiredMixin, LogoutView):
    template_name = 'blog/logout.html'


@login_required
def profile(request):
    return render(request, 'blog/profile.html', {'menu': menu})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
