from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    path("api/tutorials", views.tutorial_list),
    path("api/tutorials/<int:pk>", views.tutorial_detail),
    path("api/tutorials/published", views.tutorial_list_published),
    path("api/token/obtain/", views.ObtainTokenPairWithColorView.as_view(), name="token_create"),
    path("api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("api/user/create/", views.CustomUserCreate.as_view(), name="create_user"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("api/blacklist/", views.LogoutAndBlacklist.as_view(), name="blacklist")
]
