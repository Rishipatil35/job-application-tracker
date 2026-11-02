from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tracker.api import ApplicationViewSet

router = DefaultRouter()
router.register('applications', ApplicationViewSet, basename='api-applications')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('tracker.urls')),
]
