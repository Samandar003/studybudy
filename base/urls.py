from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logoutPage, name='logout'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerUser, name='register'),
    path("", views.home, name="home"),
    path("room/<str:pk>/", views.room, name="room"),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('delete/<str:pk>/', views.deleteRoom, name='delete-room'),
]