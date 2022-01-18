from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CreatePostSerializer, PostListSerializer, PostSerializer
from .models import Post

from django.db.models import Count
from django.contrib.auth import get_user_model


User = get_user_model()


@permission_classes((IsAuthenticated,))
@authentication_classes([TokenAuthentication])
@api_view(['GET'])
def your_functional_view(request):
    return Response(status=status.HTTP_200_OK)

# Login not required
# Show all posts
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    lookup_field = 'contents'


# Create Post
# Login required
@permission_classes((IsAuthenticated,))
@authentication_classes([TokenAuthentication])
@api_view(['POST'])
def create_post(request):
    if request.method == 'POST':
        user = request.user

        print(request.data)
        request.data._mutable=True
        data = request.data.copy()
        data['author'] = user.pk  # Adding User ID Of The Author
        serializer = CreatePostSerializer(data=data)

        if serializer.is_valid():
            print("VALID")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("INVALID")
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'detail': 'Something Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)

# increment like
@permission_classes((IsAuthenticated,))
@authentication_classes([TokenAuthentication])
@api_view(['POST'])
def post_like(request, **kwargs):
    if request.method == 'POST':
        if kwargs.get('post_id') is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        post_id = kwargs.get('post_id')
        post_object = Post.objects.get(id=post_id)
        if(post_object == None):
            return Response("no such post")

        if (user not in post_object.like_users.all()):
            post_object.like_users.add(user)

        post_object.save()

        return Response({
            "updated": PostSerializer(post_object).data
        })

    else:
        return Response({'detail': 'You Are Not Authorised To Edit This Post'}, status.HTTP_403_FORBIDDEN)


# decrement like
@permission_classes((IsAuthenticated,))
@authentication_classes([TokenAuthentication])
@api_view(['POST'])
def post_unlike(request, **kwargs):
    if request.method == 'POST':
        if kwargs.get('post_id') is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        print(user)

        post_id = kwargs.get('post_id')
        post_object = Post.objects.get(id=post_id)
        if(post_object == None):
            return Response("no such post")
        
        if(user in post_object.like_users.all()):
            post_object.like_users.remove(user)
        post_object.save()

        return Response({
            "updated": PostSerializer(post_object).data
        })

    else:
        return Response({'detail': 'You Are Not Authorised To Edit This Post'}, status.HTTP_403_FORBIDDEN)

# get user's posts
@permission_classes((IsAuthenticated,))
@authentication_classes([TokenAuthentication])
@api_view(['GET'])
def get_user_post_with_city(request, **kwargs):
    if request.method == 'GET':
        if kwargs['city'] is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)

        else:
            user = User.objects.get(username = request.user)
            city = kwargs['city']
            post_queryset = Post.objects.filter(author = user, city = city)
            post_queryset_serializer = PostSerializer(post_queryset, many=True)
            return Response(post_queryset_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'This method is not allowed'}, status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
@authentication_classes([TokenAuthentication])
@api_view(['GET'])
def get_user_post_without_city(request, **kwargs):
    if request.method == 'GET':
        user = User.objects.get(username = request.user)
        post_queryset = Post.objects.filter(author = user)
        post_queryset_serializer = PostSerializer(post_queryset, many=True)
        return Response(post_queryset_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'This method is not allowed'}, status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
@authentication_classes([TokenAuthentication])
@api_view(['GET'])
def get_user_traveld_cities(request, **kwargs):
    if request.method == 'GET':
        city_list = []
        user = User.objects.get(username = request.user)
        post_queryset = Post.objects.filter(author = user)
        for post in post_queryset:
            if(post.city not in city_list):
                city_list.append(post.city)
        return Response(city_list, status=status.HTTP_200_OK)
    else:
        return Response({'This method is not allowed'}, status.HTTP_400_BAD_REQUEST)

# Top like posts
@api_view(['GET'])
def get_top_like_posts(request):
    if request.method == 'GET':
        post_queryset = Post.objects.all().annotate(like_cnt=Count('like_users')).order_by('-like_cnt')
        post_queryset_serializer = PostSerializer(post_queryset, many=True)
        return Response(post_queryset_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'This method is not allowed'}, status.HTTP_400_BAD_REQUEST)


# Top Liked Cities
@api_view(['GET'])
def get_top_like_cities(request):
    if request.method == 'GET':
        city_list = {}
        post_queryset = Post.objects.all().annotate(like_cnt=Count('like_users')).order_by('-like_cnt')
        print(post_queryset)
        for post in post_queryset:
            print(post.like_users.count())
            if post.city not in city_list:
                city_list[post.city] = post.like_users.count()
            else:
                city_list[post.city] += post.like_users.count()
        sorted_cities = sorted(city_list.items(), key=lambda x:x[1], reverse=True)
        print(type(sorted_cities))
        return Response(sorted_cities, status=status.HTTP_200_OK)
    else:
        return Response({'This method is not allowed'}, status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_city_posts(request, **kwargs):
    if request.method == 'GET':
        if kwargs['city'] is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)

        city = kwargs['city']
        post_queryset = Post.objects.filter(city = city)
        post_queryset_serializer = PostSerializer(post_queryset, many=True)
        return Response(post_queryset_serializer.data, status=status.HTTP_200_OK)

    else:
        return Response({'This method is not allowed'}, status.HTTP_400_BAD_REQUEST)


class PostModification(APIView):
    @permission_classes((IsAuthenticated,))
    @authentication_classes([TokenAuthentication])
    def put(self, request, **kwargs):
        if kwargs.get('post_id') is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)

        else:
            user = User.objects.get(username = request.user)
            post_id = kwargs.get('post_id')
            post_object = Post.objects.get(id=post_id)
            if(post_object.author != user):
                return Response("author doesn't match")

            update_data = request.data
            update_data['author'] = user.pk
            update_post_serializer = PostSerializer(post_object, data=update_data)
            if update_post_serializer.is_valid():
                update_post_serializer.save()
                return Response(update_post_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)

    @permission_classes((IsAuthenticated,))
    @authentication_classes([TokenAuthentication])
    def delete(self, request, **kwargs):
        if kwargs.get('post_id') is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)

        else:
            user = User.objects.get(username = request.user)
            post_id = kwargs.get('post_id')
            post_object = Post.objects.get(id=post_id)
            
            # Check author
            if(post_object.author != user):
                return Response("author doesn't match")

            # Delete related image
            if post_object.image:
                post_object.image.delete()
            post_object.delete()
            return Response("test ok", status=status.HTTP_200_OK)