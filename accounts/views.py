from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PerfilSignUpSerializer


# Create your views here.
class SignUpView(APIView):
    def post(self, request, format=None):
        serializer = PerfilSignUpSerializer(data=request.data)

        if serializer.is_valid():
            perfil = serializer.create(serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
