"""Endpoints de autenticação por Token para o app mobile."""
from rest_framework import permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(ObtainAuthToken):
    """Recebe usuário/senha e devolve um token de acesso + dados do usuário."""

    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # login não exige estar autenticado

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        if not serializer.is_valid():
            return Response(
                {'detail': 'Usuário ou senha inválidos.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'usuario': {'id': user.id, 'username': user.username},
        })


class LogoutView(APIView):
    """Invalida o token atual do usuário."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
