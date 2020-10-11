from django.urls import path
from core.views import (registration_view, update_user, delete_view)
from rest_framework.authtoken.views import obtain_auth_token

app_name = "core"

urlpatterns = [
    path('register', registration_view, name="register"),
    path('login',obtain_auth_token,name="login"),
    path('<pk>/update',update_user.as_view(), name="update"),
    path('<pk>/delete',delete_view, name="delete"),
]
