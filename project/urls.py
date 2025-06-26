from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="College Management API",
        default_version='v1',
        description="API for College Management System",
        contact=openapi.Contact(email="admin@college.edu"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/', include('users.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/academics/', include('academics.urls')),
    path('api/assessment/', include('assessment.urls')),
    path('api/student-services/', include('student_services.urls')),
    path('api/professor/', include('professor_dashboard.urls')),
    path('api/notifications/', include('notifications.urls')),

    # Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]