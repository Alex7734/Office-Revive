from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment, Feedback
from users.models import Profile
import sys
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from .forms import NewCommentForm
from django.contrib.auth.decorators import login_required
from .serializers import UserSerializer, GroupSerializer, PostSerializer
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
import smtplib, ssl
from threading import Thread

def is_users(post_user, logged_user):
    return post_user == logged_user


def sendMail(userEmail, userName, eventName):
    port = 587
    smtp_server = "smtp.gmail.com"
    sender_email = "officeroomg1s1y1@gmail.com"
    password = 'hqkarbgcagncvnuy'
    message = f"""\
Subject: Event Notification
Hi, {userName.capitalize()}!
This is an automatically generated message to inform you about your attendance at {eventName}."""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, userEmail, message)


PAGINATION_COUNT = 3

#Leaderboard
class PeopleListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'blog/leaderboard.html'
    context_object_name = 'user'
    ordering = ["-score"]
    paginate_by = PAGINATION_COUNT


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        all_users = Profile.objects.all().order_by('-score')
        userProfile = Profile.objects.get(user=self.request.user)

        data['userProfile'] = Profile.objects.get(user=self.request.user) 
        data['all_users'] = all_users
        data['events_participated_in'] = Post.objects.filter(participants=userProfile).count()
        events_participated_in = Post.objects.filter(participants=userProfile).all()
        data['score'] = userProfile.score
        data['possible_score'] = userProfile.score + sum([event.score for event in events_participated_in])
        return data

    def get_queryset(self):
        return Post.objects.all().order_by('date_posted')

#Home 
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['date_posted']
    paginate_by = PAGINATION_COUNT


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        all_users = Profile.objects.all()
        checked_in_users = Profile.objects.filter(isChecked=True)
        userProfile = Profile.objects.get(user=self.request.user)

        data['userProfile'] = Profile.objects.get(user=self.request.user) 
        data['all_users'] = all_users
        data['checked_in_users'] = checked_in_users
        data['events_participated_in'] = Post.objects.filter(participants=userProfile).count()
        events_participated_in = Post.objects.filter(participants=userProfile).all()
        data['score'] = userProfile.score
        data['possible_score'] = userProfile.score + sum([event.score for event in events_participated_in])
        data['events'] = events_participated_in
        return data

    def get_queFryset(self):
        return Post.objects.all().order_by('date_posted')

#Profile page
class UserDetailView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'blog/user_detail.html'
    context_object_name = 'details'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        userProfile = Profile.objects.get(user=username)
        data['myProfile'] = Profile.objects.get(user=self.request.user)
        data['userProfile'] = userProfile
        data['events_participated_in'] = Post.objects.filter(participants=username).count()
        events_participated_in = Post.objects.filter(participants=userProfile).all()
        data['interests'] = userProfile.interests.all()
        data['score'] = userProfile.score
        data['possible_score'] = sum([event.score for event in events_participated_in])
        return data

    def get_queryset(self):
        return Post.objects.all().order_by('date_posted')



class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = PAGINATION_COUNT

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))


    def get_queryset(self):
        user = self.visible_user()
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comment.objects.filter(post_connected=self.get_object()).order_by('-date_posted')
        data['comments'] = comments_connected
        data['form'] = NewCommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),
                              author=self.request.user,
                              post_connected=self.get_object())
        new_comment.save()

        return self.get(self, request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    context_object_name = 'post'
    success_url = '/'

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['name','content', 'date_posted', 'score']
    template_name = 'blog/post_new.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Add an event'
        return data

class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    fields = ['type', 'content']
    template_name = 'blog/feedback.html'
    success_url = '/'
    fields = ['option', 'content']

    def form_valid(self):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Requests & Feedback'
        return data


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content', 'date_posted', 'interest', 'score']
    template_name = 'blog/post_new.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Edit an event'
        return data


@login_required
def isChecked(request):
    if request.method == "POST":
        userProfile = Profile.objects.get(user=request.user) 
        userProfile.isChecked = not (userProfile.isChecked)
        userProfile.save()
        if userProfile.isChecked:
            messages.success(request, f'Checked in for work!')
        else:
            messages.success(request, f'Checked out of work!')
    return redirect('blog-home')

@login_required
def appendToEvent(request, pk):
    if request.method == "POST":
        print(pk)
        post = Post.objects.get(id=pk)
        profile = Profile.objects.get(user=request.user)
        if not (profile in post.participants.all()):
            post.participants.add(profile)
            Thread(target=sendMail, args=(request.user.email, request.user.username, post.name)).start()
            messages.success(request,f"Registered to the event")
        else:
            post.participants.remove(profile)
            messages.success(request,f"Sorry you could not make it :(")
        post.save()
    return redirect('blog-home')



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]



@api_view(['GET', 'POST', 'DELETE'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        
        title = request.query_params.get('title', None)
        if title is not None:
            posts = posts.filter(title__icontains=title)
        
        posts_serializer = PostSerializer(posts, many=True)
        return JsonResponse(posts_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        post_data = JSONParser().parse(request)
        post_serializer = PostSerializer(data=post_data)
        if post_serializer.is_valid():
            post_serializer.save()
            return JsonResponse(post_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Post.objects.all().delete()
        return JsonResponse({'message': '{} Posts were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 