from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from blog.models import Post
from blog_api.serializers import PostSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def post_list(request):
    """
    Required user that was previously registrated
    List all posts, or create a new post(create and publish).
    Example of usage:
    Get all posts:
    curl http://127.0.0.1:8000/blog_api/ -u lera5:123
    Create a new post:
    curl -X POST http://127.0.0.1:8000/blog_api/ -u lera5:123 -d"title=hi&text=hihi"

    """
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, published_date=timezone.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
