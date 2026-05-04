from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import User
from .serializers import SignUpSerializer
from rest_framework.authtoken.models import Token


# Create your views here.

class SignUpView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # create token for user
        token, _ = Token.objects.get_or_create(user=user)
        data = serializer.data
        # include token in response
        data['token'] = token.key
        return Response(data, status=status.HTTP_201_CREATED)
