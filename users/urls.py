from django.urls import path

from users.apps import UsersConfig
from users.views import AuthenticationCodeAPIView, ProfileView, LoginView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    # urls для представлений Code
    path('get-auth-code/', AuthenticationCodeAPIView.as_view(), name='get-auth-code'),

    path('profile/', ProfileView.as_view(), name='profile'),

]
