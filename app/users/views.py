import environ
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView as TokenObtainPairViewNoExample,
)

from .serializers import TokenObtainPairSerializer

env = environ.Env()
test_access_token = env.str("TEST_ACCESS_TOKEN", "string")
test_refresh_token = env.str("TEST_REFRESH_TOKEN", "string")


@extend_schema(
    examples=[
        OpenApiExample(
            "Тестовый токен",
            value={
                "access": test_access_token,
                "refresh": test_refresh_token,
                "is_staff": True,
            },
            response_only=True,
        )
    ]
)
class TokenObtainPairView(TokenObtainPairViewNoExample):
    """
    Получение JWT для авторизации запросов.
    """

    serializer_class = TokenObtainPairSerializer
