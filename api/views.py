from rest_framework.decorators import api_view
from rest_framework.response import Response
from app1.models import Post

from .serializers import PostSerializer



@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/posts',
        'GET /api/posts/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getPosts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getRoomCategories(request, pk):
    posts = Post.objects.get(category=pk)
    serializer = PostSerializer(posts, many=False)
    return Response(serializer.data)