from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views
urlpatterns = [
    path('profile/', login_required(views.ProfileView.as_view()), name="profile"),
    path("create_post/", login_required(views.CreatePostView.as_view()), name="create_post"),
    path("posts/<int:pk>/", login_required(views.PostDetailView.as_view()), name="post_detail"),
    path('users/', login_required(views.UserListView.as_view()), name='user_list'),
    path('users/<int:pk>/', login_required(views.UserDetailView.as_view()), name='user_detail'),
]