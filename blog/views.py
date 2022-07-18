from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
#10.07.22
# from rest_framework.response import Response
# from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from .forms import LoginForm
# 17.07.22
from set_first.tasks import supper_sum
from .models import Post
from django.utils import timezone
from .forms import PostForm

menu = ["О сайте", "Обратная связь", "Войти", "Регистрация"]



def post_list(request):
   # task = supper_sum.delay(900, 100)
    contact_list = Post.objects.all()
    paginator = Paginator(contact_list, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page': page, 'posts': contact_list, 'menu': menu, 'title':'Главная страница'})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post, 'menu':menu, 'title':'Подробно'})

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
        return reverse('post_detail',  kwargs={'pk': self.object.instance.pk } )

# def post_new(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_new.html', {'form': form, 'menu':menu, 'title':'Добавить статью'})

class PostEdit(UpdateView):
    model = Post
    fields = ['title', 'text']
    success_url = 'post_detail'
    template_name = 'blog/post_edit.html'

    def get_post(self, pk):
        return get_object_or_404(Post, pk=pk)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Подробно'
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

# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == 'POST':
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_edit.html', {'form': form, 'menu':menu, 'title':'Подробно'})

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

# class PostView(APIView):
#     def get(self, request):
#         post = Post.objects.all()
#         return Response({"post":post})


