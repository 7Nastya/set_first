from rest_framework import serializers
from blog.models import Post
from comment.models import Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["user", "content", "post", "created_date"]


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
