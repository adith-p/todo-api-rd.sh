from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    ValidationError,
)
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(ModelSerializer):
    email = EmailField()
    password = CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password1 = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password1")

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise ValidationError(detail="email already exists")
        return data

    def validate_username(self, data):
        if User.objects.filter(username=data).exists():
            raise ValidationError(detail="username already exists")
        return data

    def validate(self, attrs):
        if attrs["password"] != attrs["password"]:
            raise ValidationError(detail="password does not match")
        try:
            validate_password(attrs["password"])
        except ValidationError as e:
            raise ValidationError(detail=f"Error{e} have occured")

    def create(self, validated_data):
        validate_password.pop("password2")
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])

        return user
