from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    post_list,
    isChecked,
    appendToEvent,
    UserDetailView,
    PeopleListView,
    FeedbackCreateView)
from .import views
from django.urls import include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/del/', PostDeleteView.as_view(), name='post-delete'),
    path('l/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/posts', post_list),
    path('isChecked', isChecked, name="isChecked"),
    path('appendToEvent/<int:pk>/', appendToEvent, name="appendToEvent"),
    path('user_detail/<int:username>', UserDetailView.as_view(), name='user-detail'),
    path('leaderboard/', PeopleListView.as_view(), name='leaderboard'),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback'),
]
