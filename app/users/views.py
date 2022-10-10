import environ
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView as TokenObtainPairViewNoExample,
)


env = environ.Env()
test_user_email = env.str("DJANGO_TEST_USER_EMAIL", "email@example.com")
test_user_password = env.str("DJANGO_TEST_USER_PASSWORD", "password")


@extend_schema(
    examples=[
        OpenApiExample(
            "Тестовый пользователь",
            value={"email": test_user_email, "password": test_user_password},
            request_only=True,
        )
    ]
)
class TokenObtainPairView(TokenObtainPairViewNoExample):
    """
    Получение JWT для авторизации запросов.
    Для упрощения работы с локальным Swagger UI имеет пример реквизитов для входа.
    """
