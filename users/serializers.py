from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def save(self, **kwargs):
        password = self.validated_data.get("password")
        self.validated_data["password"] = make_password(password)

        return super().save(**kwargs)
