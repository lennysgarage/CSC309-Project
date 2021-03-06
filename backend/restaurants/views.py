from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from .serializers import AddPhotoSerializer, CreateRestaurantSerializer, EditMenuItemSerializer, FakeFollowSerializer, FakeLikeRestaurantSerializer, FollowsSerializer, LikeRestaurantSerializer, LikesSerializer, MenuItemSerializer, RemovePhotoSerializer, RestaurantSerializer, \
 AddCommentSerializer, CommentSerializer, AddMenuItemSerializer, FollowSerializer
from .models import Like, MenuItem, Restaurant, RestaurantImage, User, Comment, Follow
from django.db.models import Count
from django.db.models import Q



class CreateRestaurant(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateRestaurantSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return JsonResponse({
                'status_code': 403,
                'error': 'User can only create a single restaurant.'
            })


class GetRestaurants(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class EditRestaurant(generics.UpdateAPIView):
    queryset = Restaurant.objects.all().select_related('owner')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateRestaurantSerializer

    def get_object(self):
        return get_object_or_404(self.queryset, owner__email=self.request.user.email)

class GetRestaurant(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all().select_related('owner')
    serializer_class = RestaurantSerializer

    def get_object(self):
        if (self.request.user.is_anonymous):
            return None
        return get_object_or_404(self.queryset, owner__email=self.request.user.email)

class ViewRestaurant(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_object(self):
        return get_object_or_404(self.queryset, id=self.kwargs['restaurant_id'])

class SearchRestaurants(generics.ListAPIView):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        query = self.request.GET.get('q') or ""
        object_list = Restaurant.objects.filter(
            Q(name__icontains=query) | Q(address__icontains=query) | Q(owner__menus_restaurant__name__icontains=query)
            | Q(owner__menus_restaurant__description__icontains=query)
        ) \
        .annotate(num_likes=Count('liked_restaurant')) \
        .order_by('-num_likes')
        return object_list

class ViewMenuItems(generics.ListAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        query = get_object_or_404(Restaurant, id=self.kwargs['restaurant_id'])
        object_list = MenuItem.objects.filter(restaurant__email = query.owner)
        return object_list

class AddMenuItem(generics.CreateAPIView):
    queryset = MenuItem.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddMenuItemSerializer


class EditMenuItem(generics.UpdateAPIView):
    queryset = MenuItem.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EditMenuItemSerializer

    def get_object(self):
        return get_object_or_404(self.queryset, id=self.kwargs['menuitem_id'], restaurant__email=self.request.user.email)

class GetMenuItem(generics.RetrieveAPIView):
    queryset = MenuItem.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EditMenuItemSerializer

    def get_object(self):
        return get_object_or_404(self.queryset, id=self.kwargs['menuitem_id'], restaurant__email=self.request.user.email)

class AddComment(generics.CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddCommentSerializer

class ViewComments(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        query = get_object_or_404(Restaurant, id=self.kwargs['restaurant_id'])
        object_list = Comment.objects.filter(restaurant__id = query.id)
        return object_list

class FollowView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return JsonResponse({
                'status_code': 403,
                'error': 'User can only follow the same restaurant once.'
            })

class FakeFollowView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FakeFollowSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return JsonResponse({
                'status_code': 403,
                'error': 'User can only follow the same restaurant once.'
            })

class Unfollow(generics.DestroyAPIView):
    queryset = Follow.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer
    
    def get_object(self):
        return get_object_or_404(self.queryset, restaurant=self.kwargs['restaurant_id'], follower__email=self.request.user.email)

class ViewFollowers(generics.ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowsSerializer

    # def get_queryset(self):
    #     query = get_object_or_404(Restaurant, id=self.kwargs['restaurant_id'])
    #     object_list = Follow.objects.filter(restaurant__id = query.id)
    #     return object_list

class Likes(generics.ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikesSerializer

class GetLikes(generics.ListAPIView):
    serializer_class = LikeRestaurantSerializer

    def get_queryset(self):
        object_list = Like.objects.filter(restaurant=self.kwargs['restaurant_id'])
        return object_list

class LikeRestaurantView(generics.CreateAPIView):
    queryset = Like.objects.all()
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = LikeRestaurantSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return JsonResponse({
                'status_code': 403,
                'error': 'User can only like the same restaurant once.'
            })

class FakeLikeRestaurantView(generics.CreateAPIView):
    queryset = Like.objects.all()
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = FakeLikeRestaurantSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return JsonResponse({
                'status_code': 403,
                'error': 'User can only like the same restaurant once.'
            })

class UnLikeRestaurantView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeRestaurantSerializer

    def get_object(self):
        return get_object_or_404(self.queryset, restaurant=self.kwargs['restaurant_id'], likedby__email=self.request.user.email)


class AddPhoto(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddPhotoSerializer

    def get_object(self):
        return get_object_or_404(self.queryset, restaurant__id=self.kwargs['restaurant_id'], restaurant__email=self.request.user.email)
    
class RemovePhoto(generics.DestroyAPIView):
    queryset = RestaurantImage.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RemovePhotoSerializer

    def get_object(self):
        return get_object_or_404(self.queryset, id=self.kwargs['restaurantimage_id'], restaurant__id=self.kwargs['restaurant_id'])

class GetPhotos(generics.ListAPIView):
    serializer_class = RemovePhotoSerializer

    def get_queryset(self):
        query = get_object_or_404(Restaurant, id=self.kwargs['restaurant_id'])
        object_list = RestaurantImage.objects.filter(restaurant__id = query.id)
        return object_list
