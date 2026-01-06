from rest_framework.permissions import BasePermission

class IsAdminUserRole(BasePermission):
    """
    Admin role ഉള്ളവർക്ക് മാത്രമേ create / update / delete ചെയ്യാൻ പറ്റൂ
    """

    def has_permission(self, request, view):
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return request.user.is_authenticated and request.user.role == "ADMIN"

        # GET / view → എല്ലാവർക്കും
        return True
