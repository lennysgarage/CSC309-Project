from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.GetUsers.as_view()),
    path('register/', views.RegisterUser.as_view()),
    path('login/', views.CustomTokenObtainPairView.as_view()),
    path('user/<int:user_id>', views.GetUserFromId.as_view()),
    path('profile/view/', views.GetUser.as_view()),
    path('profile/edit/', views.EditUser.as_view()),
    path('notifications/', views.GetNotifications.as_view()),
    path('notification/<int:id>/', views.DeleteNotification.as_view()),
]