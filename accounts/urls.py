from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet, basename="user")



urlpatterns = [
    path('auth/', include(router.urls)),
    path('auth/admin/', views.AdminListCreateView().as_view()),
    path('auth/', include('social_auth.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/login/', views.user_login, name="login_view"),
    path("auth/logout/", views.logout_view, name="logout_view"),
    path('auth/otp/verify/', views.otp_verification),
    path('auth/otp/new/', views.reset_otp),
    path('auth/fcm-token/', views.update_firebase_token),
    path("permissions/", views.PermissionList.as_view(), name="permissions"),
    path("activity-logs/", views.activity_logs),
    path("auth/profile-image-upload/", views.image_upload, name="image-upload"),
    path('auth/reset-password/', views.PasswordResetView.as_view(), name="reset_password_view"),
    path('organisations/verification/', views.pin_verification, name="organisation_verification"),

    path('auth/reset-password/verify/<str:uidb64>/<str:token>/', views.PasswordResetConfirmView.as_view(), name="reset_password_confirm_view"),
]
