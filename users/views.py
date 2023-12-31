from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User
from users.serliazers import UserSerializer
from users.utils import generate_invite_code
import time
from rest_framework import status

from django.shortcuts import get_object_or_404


class UserAuthorizationView(APIView):
    """
    Отправляем post запрос на регистрацию пользователя по заданный полям. Проверяем на ввод заданных полей.
    Создаем пользователя с указанными данными и если у него нет значения поля referral_code, то присваиваем ему
    значение с помошью метода generate_invite_code, который описан в utils.py, так же проверяем на пустоту поле
    else_referral_code, если оно заполнено то полю activated присваиваем True, в дефолтном значении False, возвращаем
    данные в ответе.
    """
    def post(self, request):
        username = request.data.get('username')
        phone = request.data.get('phone')
        password = request.data.get('password')
        else_referral_code = request.data.get('else_referral_code')

        if not password:
            return Response({'detail': 'Введите password'}, status=status.HTTP_400_BAD_REQUEST)

        if not phone:
            return Response({'detail': 'Введите phone'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(username=username, phone=phone, password=password,
                                                   else_referral_code=else_referral_code)

        if created or not user.referral_code:
            user.referral_code = generate_invite_code()
            user.save()
            time.sleep(2)
        if else_referral_code is not None:
            user.activated = True
            user.save()

        return Response(
            {'phone': phone, 'username': username, 'referral_code': user.referral_code, 'password': password,
             'else_referral_code': else_referral_code})


class UserAuthAPIView(APIView):
    """
    Отправляем post запрос для авторизации по 4-ому коду. Задаем поля username (для поиска нужного пользователя)
    и code (код смотрим в админке). Проверяем на ввод этих полей. Если код правильный, то антифицируем пользователя,
    иначе ошибка.
    """
    def post(self, request):
        username = request.data.get('username')
        code = request.data.get('code')

        if not code:
            return Response({'detail': 'Введите code'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'Пользователь не найден'}, status=status.HTTP_400_BAD_REQUEST)

        if code == user.code:
            user.is_active = True
            user.save()
            time.sleep(2)
            return Response({'detail': 'Авторизация успешна'}, status=status.HTTP_200_OK)

        else:
            return Response({'detail': 'Неверный код'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(APIView):
    """
    Отправляем get запрос на получения профиля пользователя (Имя пользователя указывается прямо в url)
    """
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileRefAPIView(APIView):
    """
    Отправляем post запрос для ввода чужого реферального кода, если он был введен при регистрации то
    обрабатываем ошибку присваивания, если при регистрации он не был введен то присваиваем полю введенный
    пользователем реферальный код и ставим поле activated в True.
    """
    def post(self, request):
        else_referral_code = request.data.get('else_referral_code')
        username = request.data.get('username')

        if not else_referral_code:
            return Response({'detail': 'Введите else_referral_code'}, status=status.HTTP_400_BAD_REQUEST)

        if not username:
            return Response({'detail': 'Введите username'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, username=username)
        if user.activated:
            return Response({'detail': 'Вы уже вводили реферальный код'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.else_referral_code = else_referral_code
            user.activated = True
            user.save()
            return Response({'detail': 'Код успешно активирован'}, status=status.HTTP_400_BAD_REQUEST)


class UserReffAPIView(APIView):
    """
    Отправляем get запрос на получения профилей тех, кто ввел один и тот же реферальный код (возврат данных происходит
    в виде списка содержащий словари профилей)
    """
    def get(self, request):
        referral_code = request.data.get('referral_code')

        if not referral_code:
            return Response({'detail': 'Введите referral_code'}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(else_referral_code=referral_code).values('username', 'phone')

        users_list = list(users)

        return Response(users_list, status=status.HTTP_200_OK)
