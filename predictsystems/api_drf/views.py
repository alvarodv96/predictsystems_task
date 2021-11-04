from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, PostCreateSerializer, PostSerializer
from .models import Post
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class UserRegisterApiView(APIView):

    def post(self, request):
        """
        Create new user
        ---
            Auth: Public
        parameters:
            - in: body
                name: first_name
                description: User first name
                required: true
                type: str
            - in: body
                name: last_name
                description: User last name
                required: true
                type: str
            - in: body
                name: username
                description: User username
                required: true
                type: str
            - in: body
                name: email
                description: User email
                required: true
                type: str
            - in: body
                name: password
                description: User password
                required: true
                type: str
        responses:
            - response_code: 500
              Description: Server error
            - response_code: 201
              Description: Data stored in database
        """
        try:
            serializer_input = UserSerializer(data=request.data)
            if serializer_input.is_valid():
                user = User()
                user.first_name = serializer_input.data['first_name']
                user.last_name = serializer_input.data['last_name']
                user.email = serializer_input.data['email']
                user.username = serializer_input.data['username']
                user.set_password(serializer_input.data['password'])
                user.save()
                return Response(serializer_input.data, status=status.HTTP_201_CREATED)
            return Response(serializer_input.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)



class PostsApiView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Get all posts
        ---
            Auth: Authenticated user
        parameters:
            - none
        responses:
            - response_code: 500
              Description: Server error
            - response_code: 200
              Description: Ok
        """
        try:
            response = PostSerializer(Post.objects.filter(active=True).order_by('-created_date'), many=True)
            return Response(response.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
        Create new post
        ---
            Auth: Authenticated user
        parameters:
            - in: body
                name: name
                description: Post name
                required: true
                type: str
        responses:
            - response_code: 500
              Description: Server error
            - response_code: 201
              Description: Data stored in database
        """
        try:
            serializer_input = PostCreateSerializer(data=request.data)
            if serializer_input.is_valid():
                post = Post()
                post.creator_id = request.user.id
                post.name = serializer_input.data['name']
                post.save()
                response = PostSerializer(post)
                return Response(response.data, status=status.HTTP_201_CREATED)
            return Response(serializer_input.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class PostApiView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        """
        Get a post form user
        ---
            Auth: Authenticated user
        parameters:
            - none
        responses:
            - response_code: 500
              Description: Server error
            - response_code: 400
              Description: Error
            - response_code: 200
              Description: Ok
        """
        try:
            response = PostSerializer(Post.objects.get(creator_id=request.user.id, active=True, id=id))
            return Response(response.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        """
        Update an existing post
        ---
            Auth: Authenticated user
        parameters:
            - in: body
                name: name
                description: Post name
                required: true
                type: str
        responses:
            - response_code: 500
              Description: Server error
            - response_code: 400
              Description: Error
            - response_code: 200
              Description: Ok
        """
        try:
            serializer_input = PostCreateSerializer(data=request.data)
            if serializer_input.is_valid():
                post = Post.objects.get(id=id, creator_id=request.user.id, active=True)
                post.name = serializer_input.data['name']
                post.save()
                response = PostSerializer(post)
                return Response(response.data, status=status.HTTP_200_OK)
            return Response(serializer_input.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """
        Delete an existing post
        ---
            Auth: Authenticated user
        parameters:
            - none
        responses:
            - response_code: 500
              Description: Server error
            - response_code: 400
              Description: Error
            - response_code: 200
              Description: Ok
        """
        try:
            post = Post.objects.get(id=id, creator_id=request.user.id, active=True)
            post.active = False
            post.save()
            response = PostSerializer(post)
            return Response(response.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class LikePostApiView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def put(self, request, id):
        """
        Like an existing post
        ---
            Auth: Authenticated user
        parameters:
            - none
        responses:
            - response_code: 500
              Description: Server error
            - response_code: 400
              Description: Error
            - response_code: 200
              Description: Ok
        """
        try:
            post = Post.objects.get(id=id, active=True)
            post.likes.add(request.user.id)
            response = PostSerializer(post)
            return Response(response.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)