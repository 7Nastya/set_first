# GET - для пост лист, для одного поста, для одного комментария, для всех комментариев
# Post - удаление, добавление, изменение

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostSerializer, CommentSerializer, CommentCreateSerializer, PostCreateSerializer
from blog.models import Post
from comment.models import Comment


class PostListApiView(APIView):
    def get(self, request):
        post = Post.objects.all()
        serializer = PostSerializer
        return Response(serializer.data)


class PostDetailApiView(APIView):
    def get(self, request, pk):
        post = Post.objects.get(Post, pk=pk)
        serializer = Post(post)
        return Response(serializer.data)


class PostCreateView(APIView):
    def post(self, request):
        post = PostCreateSerializer(data=request.data)
        if post.is_valid():
            post.save()
        return Response(status=201)


class CommentListApiView(APIView):
    def get(self, request):
        post = Comment.objects.all()
        serializer = CommentSerializer
        return Response(serializer.data)


class CommentDetailApiView(APIView):
    def get(self, request, pk, id):
        post = Post.objects.get(Post, pk=pk)
        comment = Comment.objects.get(Comment, id=id)
        serializer = Comment(comment)
        return Response(serializer.data)


class CommentCreateView(APIView):
    def post(self, request):
        comment = CommentCreateSerializer(data=request.data)
        if comment.is_valid():
            comment.save()
        return Response(status=201)
