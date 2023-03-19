from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from users.serializers.users import UserRegistrationSerializer


User = get_user_model()

@extend_schema_view(
    post=extend_schema(summary='Регистрация пользователя', tags=['Пользователи']),
)
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
    http_method_names = ('post',)

