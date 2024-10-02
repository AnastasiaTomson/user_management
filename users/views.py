from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializers import RegisterSerializer, UserSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer = RegisterSerializer

    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return User.objects.all()  # Администраторы видят всех пользователей
        else:
            user_pk = self.kwargs.get('pk', 0)
            if int(user_pk) == user.id or user_pk == 0:
                return User.objects.filter(id=user.id)  # Обычные пользователи видят только себя
        raise PermissionDenied("You do not have permission.")

    def get_permissions(self):
        # Ограничиваем доступ к действиям создания, обновления, частичного обновления и удаления
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            user = self.request.user

            if not user.is_authenticated:
                raise PermissionDenied("You must be logged in to perform this action.")

            # Проверяем роль и принадлежность пользователя к запрашиваемому ресурсу
            user_pk = self.kwargs.get('pk', 0)
            if user.role != 'admin' and user.id != int(user_pk):
                raise PermissionDenied("You do not have permission to perform this action.")

        return super().get_permissions()
