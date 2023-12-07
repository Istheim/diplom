from rest_framework import generics
from users.models import User, Code
from users.serliazers import CodeSerializer, LoginSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serliazers import ProfileSerializer
from rest_framework.views import APIView


class LoginView(APIView):
    """
    Авторизация по номеру телефона.
    """

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# generics для модели Code
class AuthenticationCodeAPIView(generics.CreateAPIView):
    serializer_class = CodeSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        number_phone = request.data.get('number_phone')

        try:
            user_code = Code.objects.get(user__number_phone=number_phone)
        except Code.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user_code)
        return Response({'code': serializer.data['code']})


class ProfileView(RetrieveUpdateAPIView):
    """
    Представление для профиля пользователя.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        # Переопределение метода update для правильной обработки PUT-запроса
        return super().update(request, *args, **kwargs)
