from django.urls import path, include
from .apis import RegisterAPI, LoginAPI, UserAPI, ProfileUpdateAPI
from knox import views as knox_views

urlpatterns = [
    path('api/auth', include('knox.urls')),

    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('api/auth/user', UserAPI.as_view()),
    path("auth/profile/<int:user_pk>/update/", ProfileUpdateAPI.as_view()),

]