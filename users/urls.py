from rest_framework.urls import path

from users.views import RegisterApiView

urlpatterns = [
    path("register/", RegisterApiView.as_view(), name="register"),
]
