from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["is_staff"] = self.user.is_staff
        return data
