from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateApiView, UserDestroyAPIView, \
    AuthenticationCodeAPIView

app_name = UsersConfig.name

urlpatterns = [
    # urls для представлений User
    path('user/create/', UserCreateAPIView.as_view(), name='user-create'),
    path('user/', UserListAPIView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserRetrieveAPIView.as_view(), name='user-get'),
    path('user/update/<int:pk>/', UserUpdateApiView.as_view(), name='user-update'),
    path('user/delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user-delete'),

    # urls для представлений Code
    path('get-auth-code/', AuthenticationCodeAPIView.as_view(), name='get-auth-code'),

]
