from .serializers import FavoriteSerializer, CommentSerializer, CommentAnswerSerializer
from .models import Favorite, Comment, CommentAnswer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from .permissions import IsAuthorOrReadOnly

class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorOrReadOnly,IsAdminUser]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]

class CommentViewSet(PermissionMixin,ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentAnswerViewSet(PermissionMixin,ModelViewSet):
    queryset = CommentAnswer.objects.all()
    serializer_class = CommentAnswerSerializer

# class FavoriteViewSet(PermissionMixin ,ModelViewSet):
#     queryset = Favorite.objects.all()
#     serializer_class = FavoriteSerializer