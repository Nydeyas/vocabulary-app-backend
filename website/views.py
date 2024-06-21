from .models import User, Category, Word
from .serializer import UserSerializer, CategorySerializer, WordSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class HomeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': "Successfully connected to the API"}
        return Response(content)


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate data
        if not username or not email or not password:
            return Response(
                {'detail': 'Username, email, and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate password
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({'detail': e.messages}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Return response
        if user:
            return Response({'detail': 'User created successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Failed to create user.'}, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Get the User by ID
        """
        user = User.objects.filter(id=request.data.get("user"))
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create the User with given user data
        """
        data = {
            'username': request.data.get('username'),
            'email': request.data.get('email'),
            'password': request.data.get('password')
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, user_id):
        """
        Helper method to get the object with given user_id
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def get(self, request, user_id, *args, **kwargs):
        """
        Get the User with given user_id
        """
        user_instance = self.get_object(user_id)
        if not user_instance:
            return Response(
                {"res": "Object with this user id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserSerializer(user_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id, *args, **kwargs):
        """
        Updates the User item with given user_id if exists
        """
        user_instance = self.get_object(user_id)
        if not user_instance:
            return Response(
                {"res": "Object with this user id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'username': request.data.get('username'),
            'email': request.data.get('email'),
            'password': request.data.get('password')
        }
        serializer = UserSerializer(instance=user_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, *args, **kwargs):
        """
        Deletes the User item with given user_id if exists
        """
        user_instance = self.get_object(user_id)
        if not user_instance:
            return Response(
                {"res": "Object with this user id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


class CategoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Get all the category items for given requested user
        """
        categories = Category.objects.filter(user=request.data.get("user"))
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create the Category with given category data
        """
        data = {
            'name': request.data.get('name'),
            'word_language': request.data.get('word_language'),
            'translation_language': request.data.get('translation_language'),
            'user': request.data.get('user')
        }
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, category_id):
        """
        Helper method to get the object with given category_id
        """
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return None

    def get(self, request, category_id, *args, **kwargs):
        """
        Get the Category with given category_id
        """
        category_instance = self.get_object(category_id)
        if not category_instance:
            return Response(
                {"res": "Object with this category id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CategorySerializer(category_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, category_id, *args, **kwargs):
        """
        Updates the Category item with given category_id if exists
        """
        category_instance = self.get_object(category_id)
        if not category_instance:
            return Response(
                {"res": "Object with this category id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'name': request.data.get('name'),
            'word_language': request.data.get('word_language'),
            'translation_language': request.data.get('translation_language'),
            'user': request.data.get('user')
        }
        serializer = CategorySerializer(instance=category_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id, *args, **kwargs):
        """
        Deletes the Category item with given category_id if exists
        """
        category_instance = self.get_object(category_id)
        if not category_instance:
            return Response(
                {"res": "Object with this category id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        category_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )



class WordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Get all the Word items for given requested category
        """
        words = Word.objects.filter(category=request.data.get("category"))
        serializer = WordSerializer(words, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create the Word with given word data
        """
        data = {
            'word': request.data.get('word'),
            'translation': request.data.get('translation'),
            'is_learned': request.data.get('is_learned'),
            'category': request.data.get('category')
        }
        serializer = WordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WordDetailApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, word_id):
        """
        Helper method to get the object with given word_id
        """
        try:
            return Word.objects.get(id=word_id)
        except Word.DoesNotExist:
            return None

    def get(self, request, word_id, *args, **kwargs):
        """
        Get the Word with given word_id
        """
        word_instance = self.get_object(word_id)
        if not word_instance:
            return Response(
                {"res": "Object with this word id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = WordSerializer(word_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, word_id, *args, **kwargs):
        """
        Updates the Word item with given word_id if exists
        """
        word_instance = self.get_object(word_id)
        if not word_instance:
            return Response(
                {"res": "Object with this word id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'word': request.data.get('word'),
            'translation': request.data.get('translation'),
            'is_learned': request.data.get('is_learned'),
            'category': request.data.get('category')
        }
        serializer = WordSerializer(instance=word_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, word_id, *args, **kwargs):
        """
        Deletes the Word item with given word_id if exists
        """
        word_instance = self.get_object(word_id)
        if not word_instance:
            return Response(
                {"res": "Object with this word id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        word_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
