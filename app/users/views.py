import environ
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView as TokenObtainPairViewNoExample,
)

env = environ.Env()
test_access_token = env.str("TEST_ACCESS_TOKEN", "")
test_refresh_token = env.str("TEST_REFRESH_TOKEN", "")


@extend_schema(
    examples=[
        OpenApiExample(
            "Тестовый токен",
            value={"access": test_access_token, "refresh": test_refresh_token},
            response_only=True,
        )
    ]
)
class TokenObtainPairView(TokenObtainPairViewNoExample):
    """
    Получение JWT для авторизации запросов.
    """
