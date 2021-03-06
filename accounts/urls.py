

from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('register/', views.Register.as_view(), name="register"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name="activate"),
    path('logout/', views.logout_view, name="logout"),
]
