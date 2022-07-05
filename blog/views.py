from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView

from .models import Post
from django.utils import timezone
from .forms import PostForm

menu = ["О сайте", "Обратная связь", "Войти", "Регистрация"]

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts, 'menu':menu, 'title':'Главная страница'})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post, 'menu':menu, 'title':'Подробно'})

def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form, 'menu':menu, 'title':'Добавить статью'})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'menu':menu, 'title':'Подробно'})

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class PostListView(ListView):
    template_name = 'blog/post_list.html'
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['posts'] = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        return context
