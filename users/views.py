from rest_framework import generics
from users.models import User, Code
from users.serliazers import CodeSerializer
from rest_framework import status
from rest_framework.response import Response


#
## generics для модели User
# class UserCreateAPIView(generics.CreateAPIView):
#    serializer_class = UserSerializer
#
#
# class UserListAPIView(generics.ListAPIView):
#    serializer_class = UserSerializer
#    queryset = User.objects.all()
#
#
# class UserRetrieveAPIView(generics.RetrieveAPIView):
#    serializer_class = UserSerializer
#    queryset = User.objects.all()
#
#
# class UserUpdateApiView(generics.UpdateAPIView):
#    serializer_class = UserSerializer
#    queryset = User.objects.all()
#
#
# class UserDestroyAPIView(generics.DestroyAPIView):
#    queryset = User.objects.all()
#
#
# generics для модели Code
class AuthenticationCodeAPIView(generics.CreateAPIView):
    serializer_class = CodeSerializer

    def create(self, request, *args, **kwargs):
        phone = request.data.get('phone')

        try:
            user_code = Code.objects.get(user__phone=phone)
        except Code.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user_code)
        return Response({'code': serializer.data['code']})
