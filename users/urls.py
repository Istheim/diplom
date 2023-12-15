from django.urls import path

from users.apps import UsersConfig
from .views import UserAuthorizationView, UserAuthAPIView, UserProfileAPIView, UserReffAPIView, UserProfileRefAPIView

app_name = UsersConfig.name

urlpatterns = [
    # Регистация пользователя
    path('authorize/', UserAuthorizationView.as_view(), name='phone_authorization'),
    # Авторизация пользователя
    path('auth/', UserAuthAPIView.as_view(), name='code_authorization'),
    # Просмотр профиля пользователя
    path('user/<str:username>/', UserProfileAPIView.as_view(), name='user-search'),
    # Просмотр профилей который ввели чужой реферальный код
    path('ref/', UserReffAPIView.as_view(), name='ref-search'),
    # Ввод чужого реферального кода в профиле
    path('else-ref/', UserProfileRefAPIView.as_view(), name='else-ref'),

]
