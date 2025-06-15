from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    ValidationError,
    IntegerField,
    Serializer,
)
from django.contrib.auth.password_validation import validate_password
from .models import User, Todo


class UserSerializer(ModelSerializer):
    email = EmailField()
    password1 = CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password2 = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise ValidationError(detail="email already exists")
        return data

    def validate_username(self, data):
        if User.objects.filter(username=data).exists():
            raise ValidationError(detail="username already exists")
        return data

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise ValidationError(detail="password does not match")
        try:
            validate_password(attrs["password1"])
        except ValidationError as e:
            raise ValidationError(detail=f"Error{e} have occured")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password1"])

        return user


class TodoSerializer(ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"


class GetAllTodoSerializer(Serializer):
    data = TodoSerializer(many=True)
    page = IntegerField()
    limit = IntegerField()
    total = IntegerField()
