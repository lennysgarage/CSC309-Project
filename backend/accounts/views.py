from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from .serializers import EditUserSerializer, NotificationSerializer, RegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer, ViewUserSerializer
from .models import Notification, User
from rest_framework_simplejwt.views import TokenObtainPairView

# users/
class GetUsers(generics.ListAPIView):
    """
    API endpoint that shows all users.
    """
    queryset = User.objects.all().order_by('date_joined') 
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]

# register/
class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return JsonResponse({
                'status_code': 403,
                'error': 'User with that email already exists.'
            })

# login/
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer    


# profile/view/
class GetUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ViewUserSerializer

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, email=self.request.user.email)

class GetUserFromId(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ViewUserSerializer

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, id=self.kwargs['user_id'])


# profile/edit/
class EditUser(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EditUserSerializer
    lookup_field = 'email'

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.object.set_password(serializer.data.get('password'))
            self.object.save()
        # return 
        return JsonResponse({'status_code': 200})

# notifications/
class GetNotifications(generics.ListAPIView):
    queryset = Notification.objects.all().order_by('-date') 
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

# notification/1/
class DeleteNotification(generics.DestroyAPIView):
    queryset = Notification.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_object(self):
        return get_object_or_404(self.queryset, id=self.kwargs['id'])

# notification/add
# class AddNotification(generics.CreateAPIView):
#     queryset = Notification.objects.all()
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = AddNotificationSerializer
