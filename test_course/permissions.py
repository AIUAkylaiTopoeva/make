from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Разрешаем любые действия администраторам
        if request.user and request.user.is_staff:
            return True

        # Разрешаем чтение всем пользователям, включая аутентифицированных
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True

        # Разрешаем аутентифицированным пользователям отправку ответов (метод POST)
        if request.method == 'POST' and request.user.is_authenticated:
            return True

        return False
    
class IsAuthenticatedAndOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user