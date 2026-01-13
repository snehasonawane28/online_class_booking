from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    # DO NOT override username_field

    def validate(self, attrs):

        if attrs.get("email") is None:
            email = attrs.get("username")
        else:
            email = attrs.get("email")

        password = attrs.get("password")

        if not email or not password:
            email = attrs.get("email")
            raise AuthenticationFailed("Email and password are required")

        # Authenticate using email as username
        user = authenticate(
            request=self.context.get("request"),
            username=email,   # email stored as username
            password=password
        )

        if not user:
            raise AuthenticationFailed("Invalid email or password")

        # Let SimpleJWT generate tokens
        data = super().validate({
            "username": user.username,
            "password": password
        })

        # Add extra user info
        data["user"] = {
            "id": user.id,
            "email": user.email,
            "role": user.role,
        }

        return data
