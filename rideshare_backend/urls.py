from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import UserViewSet, PassengerProfileViewSet, DriverProfileViewSet
from rides.views import RideViewSet, RideLocationViewSet, RatingViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'passengers', PassengerProfileViewSet, basename='passenger')
router.register(r'drivers', DriverProfileViewSet, basename='driver')
router.register(r'rides', RideViewSet, basename='ride')
router.register(r'locations', RideLocationViewSet, basename='location')
router.register(r'ratings', RatingViewSet, basename='rating')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
]
