from rest_framework import serializers
from blog.models import Post
from comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class PostCommentSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['author',
                  'title',
                  'text',
                  'foto',
                  'created_date',
                  'published_date',
                  'comments']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author',
                  'title',
                  'text',
                  'foto',
                  'created_date',
                  'published_date']
