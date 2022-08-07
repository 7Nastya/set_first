from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from my_user.models import MyUser
from comment.models import Comment
from .models import Post
from django.utils import timezone
from .forms import PostForm, SignUpForm, UserCommentForm

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

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

    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        comment_form = UserCommentForm(request.POST or None)
        comments = Comment.objects.filter(post=pk)
        if comment_form.is_valid():
            content = request.POST['content']
            user = self.request.user
            post = get_object_or_404(Post, pk=pk)
            comment = comment_form.save()
            comment.post = post
            comment.user = user
            comment.save()
        return redirect('post_detail', pk=pk)

    def get_post(self, pk):
        return get_object_or_404(Post, pk=pk)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Подробно'
        context['menu'] = menu
        context['post'] = get_object_or_404(Post, pk=self.object.pk)
        context['comment_form'] = UserCommentForm()
        context['comments'] = Comment.objects.filter(post=self.object.pk)

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
    fields = ['birthday', 'first_name', 'last_name', 'email', 'username']

    def get_post(self, pk):
        return get_object_or_404(Post, pk=pk)

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

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
    next_page = 'post_list'


class SignUp(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "blog/signup.html"


@login_required
def profile(request, pk):
    return render(request, 'blog/profile.html',
                  {'username': request.user.username, 'first_name': request.user.first_name,
                   'last_name': request.user.last_name, 'email': request.user.email,
                   'birthday': request.user.birthday, 'menu': menu, 'pk': pk})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def comment_delete(request, pk, id):
    post = get_object_or_404(Post, pk=pk)
    selected_comment = get_object_or_404(Comment, id=id)
    selected_comment.delete()
    comment_form = UserCommentForm()
    comments = Comment.objects.filter(post=pk)
    return redirect('post_detail', pk=pk)

def comment_update(request, pk, id):
    post = get_object_or_404(Post, pk=pk)
    comment = get_object_or_404(Comment, id=id)
    form = UserCommentForm()
    if request.method == 'POST':
        form = UserCommentForm(request.POST, instance=comment.user)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    return redirect('post_list')