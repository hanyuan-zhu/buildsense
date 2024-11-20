from django.urls import path
from .views import RegisterView, LoginView, CompanyListView, ProjectListView, LogoutView, UserInfoView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('companies/<int:company_id>/projects/', ProjectListView.as_view(), name='project-list'),
    path('userinfo/', UserInfoView.as_view(), name='user-info'),
]