from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import EmailLoginView   # ✅ IMPORT THIS

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('assets.urls')),
    path('api/', include('users.urls')),
    # path("api/", include("tickets.urls")),


    # ✅ CUSTOM EMAIL LOGIN
    path('api/login/', EmailLoginView.as_view()),

    path('api/refresh/', TokenRefreshView.as_view()),
]
