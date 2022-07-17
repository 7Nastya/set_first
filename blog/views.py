from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView
#10.07.22
# from rest_framework.response import Response
# from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from .forms import LoginForm
#
from .models import Post
from django.utils import timezone
from .forms import PostForm

menu = ["О сайте", "Обратная связь", "Войти", "Регистрация"]

def post_list(request):
    contact_list = Post.objects.all()
    paginator = Paginator(contact_list, 4)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page': page, 'posts': contact_list, 'menu': menu, 'title':'Главная страница'})

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
    return redirect(request, 'blog/post_edit.html', {'form': form, 'menu':menu, 'title':'Подробно'})

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class PostListView(ListView):
    template_name = 'blog/post_list.html'
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['posts'] = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        return context

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # next = request.META.get('HTTP_REFERER', None) or '/'
                    # response = HttpResponseRedirect(next)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})
# class PostView(APIView):
#     def get(self, request):
#         post = Post.objects.all()
#         return Response({"post":post})


