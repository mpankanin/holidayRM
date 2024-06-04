"""
URL configuration for holidayRM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from holidayRM import views

# Create a schema view for the Swagger UI
schema_view = get_schema_view(
    openapi.Info(
        title="HolidayRM API",
        default_version='v1',
        description="API for managing vacations",
    ),
    public=True,
    permission_classes=([permissions.AllowAny,]),
)

# Define the URL patterns for the application
urlpatterns = [
    # Swagger schema in JSON or YAML format
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # Swagger UI
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # Redoc UI
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Admin site
    path('admin/', admin.site.urls),
    # List of vacations for the current user
    path('vacations', views.user_vacation_list),
    # List of all vacations
    path('vacations/all', views.all_vacations),
    # Add a new vacation
    path('vacations/add', views.vacation_post),
    # Detail of a specific vacation
    path('vacations/<int:id>', views.vacation_detail),
    # Approve a specific vacation
    path('vacations/approve/<int:id>', views.approve_vacation),
    # Login
    path('login', views.login),
    # Signup
    path('signup', views.signup),
    # Test token
    path('test_token', views.test_token)
]
