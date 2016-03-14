from rest_framework import generics
from .models import Post
from .serializers import PostSerializer


class PostUpdateView(generics.UpdateAPIView):

    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostDeleteView(generics.DestroyAPIView):

    serializer_class = PostSerializer
    queryset = Post.objects.all()
