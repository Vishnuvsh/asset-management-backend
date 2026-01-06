from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainPairSerializer

class EmailLoginView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import EmployeeSerializer
from .permissions import IsAdmin

class EmployeeViewSet(ReadOnlyModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return User.objects.filter(role="EMPLOYEE")

# view for user profile

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import UserProfileSerializer

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


# view for listing technicians

class TechnicianListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        technicians = User.objects.filter(role="TECHNICIAN")
        serializer = UserProfileSerializer(technicians, many=True)
        return Response(serializer.data)
