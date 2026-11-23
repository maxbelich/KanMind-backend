from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email

from .serializers import RegistrationSerializer, LoginSerializer, UserShortSerializer
from user_auth_app.models import User


def build_auth_data(user):
    token, _ = Token.objects.get_or_create(user=user)
    return {
        'token': token.key,
        'fullname': user.fullname,
        'email': user.email,
        'user_id': user.id,
    }

class RegistrationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(build_auth_data(user), status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response(build_auth_data(user), status=status.HTTP_200_OK)

class EmailCheckView(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response(
                {'email': 'This query parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            validate_email(email)
        except DjangoValidationError:
            return Response(
                {'email': 'Enter a valid email address.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.filter(email__iexact=email).first()
        if user is None:
            return Response(
                {'detail': 'No user with this email.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(UserShortSerializer(user).data)