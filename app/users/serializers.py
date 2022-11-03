from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        groups = []
        for group in self.user.groups.all():
            groups.append({"id": group.pk, "name": group.name})
        data["groups"] = groups
        return data
