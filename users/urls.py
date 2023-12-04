from django.urls import path

from users.apps import UsersConfig
from users.views import AuthenticationCodeAPIView

app_name = UsersConfig.name

urlpatterns = [

    # urls для представлений Code
    path('get-auth-code/', AuthenticationCodeAPIView.as_view(), name='get-auth-code'),

]
