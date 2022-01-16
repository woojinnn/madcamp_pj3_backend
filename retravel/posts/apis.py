from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import PostListSerializer, PostCreateSerializer, PostSerializer, PostUpdateSerializer
from .models import Post

from django.contrib.auth import get_user_model


User = get_user_model()

# View For List All Published Posts


@permission_classes((IsAuthenticated,))
@authentication_classes([TokenAuthentication])
@api_view(['GET'])
def your_functional_view(request):
    return Response(status=status.HTTP_200_OK)


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    lookup_field = 'slug'


# Create Post
@permission_classes((IsAuthenticated,))
@authentication_classes([TokenAuthentication])
@api_view(['POST'])
def create_post(request):
    if request.method == 'POST':
        user = request.user

        data = request.data
        data['author'] = user.pk  # Adding User ID Of The Author
        serializer = PostCreateSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'detail': 'Something Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)



# View To Update A Post For Logged In Users
@permission_classes((IsAuthenticated,))
@authentication_classes([TokenAuthentication])
@api_view(['POST'])
def post_update_view(request):
    if request.method == 'POST':

        logged_in_user = request.user

        updated_data = request.data
        instance = Post.objects.get(slug=updated_data.get('slug'))
        admin_user = User.objects.get(pk=1)  # PK Of Admin User Is 1

        if(instance.author == logged_in_user or logged_in_user == admin_user):
            updated_data.pop('slug')
            serializer = PostUpdateSerializer(instance, data=updated_data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'detail': 'Something Went Wrong.'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'detail': 'You Are Not Authorised To Edit This Post'}, status.HTTP_403_FORBIDDEN)

    else:
        return Response({'detail': 'You Are Not Authorised To Edit This Post'}, status.HTTP_403_FORBIDDEN)

# View To Delete A Post For Logged In Users
@permission_classes((IsAuthenticated,))
@authentication_classes([TokenAuthentication])
@api_view(['DELETE'])
def post_delete_view(request):
    if request.method == 'DELETE':
        logged_in_user = request.user

        print(request.data)

        instance = Post.objects.get(slug=request.data.get('slug'))
        admin_user = User.objects.get(pk=1)  # PK Of Admin User Is 1

        if(instance.author == logged_in_user or logged_in_user == admin_user):
            instance.delete()
            return Response({}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Something Went Wrong.'}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'detail': 'You Are Not Authorised To Edit This Post'}, status.HTTP_403_FORBIDDEN)


class PostDetail(APIView):
    @permission_classes((IsAuthenticated,))
    @authentication_classes([TokenAuthentication])
    def get(self, request, **kwargs):
        if kwargs.get('post_id') is None:
            user = User.objects.get(username = request.user)
            post_queryset = Post.objects.get(author = user)
            post_queryset_serializer = PostSerializer(post_queryset)
            return Response(post_queryset_serializer.data, status=status.HTTP_200_OK)
        else:
            post_id = kwargs.get('post_id')
            post_serializer = PostSerializer(Post.objects.get(id=post_id))
            return Response(post_serializer.data, status=status.HTTP_200_OK)


    @permission_classes((IsAuthenticated,))
    @authentication_classes([TokenAuthentication])
    def put(self, request, **kwargs):
        if kwargs.get('post_id') is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)

        else:
            post_id = kwargs.get('post_id')
            post_object = Post.objects.get(id=post_id)

            update_post_serializer = PostSerializer(post_object, data=request.data)
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
            post_id = kwargs.get('post_id')
            post_object = Post.objects.get(id=post_id)
            post_object.delete()
            return Response("test ok", status=status.HTTP_200_OK)