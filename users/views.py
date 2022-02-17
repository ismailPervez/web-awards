from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .forms import CreateReviewForm, RegisterForm, CreateNewPost
from django.contrib.auth.decorators import login_required
from .models import Post, Rating, Review
from django.contrib import messages
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, PostsSerializer

def home(request):
    ratings = Rating.objects.order_by('-value').all()
    ranked_posts = []
    for rating in ratings:
        ranked_posts.append(rating.post)
    return render(request, 'users/index.html', {'posts': ranked_posts})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'you have successfully registered. You can now login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    posts = Post.objects.filter(user=user).all()
    return render(request, 'users/dashboard.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = CreateNewPost(request.POST, request.FILES)
        if form.is_valid():
            new_post = Post(
                title=form.cleaned_data['title'],
                link=form.cleaned_data['link'],
                desc=form.cleaned_data['desc'],
                preview_image=form.cleaned_data['preview_image'],
                user=request.user
            )
            new_post.save()
            messages.success(request, 'You have successfully created a new post')
    else:
        form = CreateNewPost()
    return render(request, 'users/post.html', {'form': form})

def full_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CreateReviewForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                new_review = Review(
                    content=form.cleaned_data['content'],
                    user=request.user,
                    post=post
                )
                new_review.save()
                print('new review saved')
                form = CreateReviewForm()

        else:
            messages.info(request, 'You need to be logged in to post a review')
    
    else:
        form = CreateReviewForm()
        
    if request.user.is_authenticated:
        return render(request, 'users/full_post.html', {'post': post, 'form': form, 'is_rated': post.is_rated(current_user=request.user)})

    else:
        return render(request, 'users/full_post.html', {'post': post, 'form': form, 'is_rated': False})

def add_ratings(request, post_id):
    value = request.GET.get('value', '')
    post = get_object_or_404(Post, pk=post_id)
    if request.user.is_authenticated:
        rating = Rating.objects.filter(post=post, user=request.user).first()
        if rating:
            return JsonResponse({'msg': 'you cannot rate twice'})
        else:
            rating = Rating(
                value=value,
                post=post,
                user=request.user
            )
            rating.save()
            return JsonResponse({'msg': 'added a rating', 'status_code': 200})

    else:
        return JsonResponse({'msg': 'login required', 'status_code': 302})

def results(request, query):
    posts = Post.objects.all()
    filtered_posts = []
    for post in posts:
        if (query in post.title) or (query in post.desc) or (query in post.user.username):
            filtered_posts.append(post)
    return render(request, 'users/results.html', {'posts': filtered_posts})


# API views
@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    json_users = UserSerializer(users, many=True)
    return Response(json_users.data)

@api_view(['GET'])
def get_user(request, username):
    user = get_object_or_404(User, username=username)
    json_user = UserSerializer(user)
    return Response(json_user.data)

@api_view(['GET'])
def get_posts(request):
    posts = Post.objects.all()
    json_posts = PostsSerializer(posts, many=True)
    return Response(json_posts.data)