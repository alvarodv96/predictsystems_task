from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.UserRegisterApiView.as_view()),
    path('posts/', views.PostsApiView.as_view()),
    path('posts/<int:id>/', views.PostApiView.as_view()),
    path('posts/like/<int:id>/', views.LikePostApiView.as_view()),
]