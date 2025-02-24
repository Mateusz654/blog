from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models import F
from django.contrib import messages
from .models import Post, Comment, Like

# Create your views here.
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post-list')
    else:
        form = UserCreationForm()
    return render(request, 'posts/register.html', {'form':form})        


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('post-list')
        else:
            messages.error(request, "Niepoprawna nazwa użytkownika lub hasło.")
    return render(request, 'posts/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def show_posts(request):
    posts = Post.objects.all()
    comments = Comment.objects.all()
    return render(request, 'posts/posts.html', {'posts':posts, 'comments':comments})

def choose_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).select_related("user", "post")

    user_likes = Like.objects.filter(user=request.user, comment__in=comments).values_list("comment_id", flat=True)

    previous_url = request.META.get('HTTP_REFERER', request.path)
    return render(request, 'posts/choose_post.html', {
        'post': post,
        'comments': comments,
        'user_likes': list(user_likes), 
        'previous_url': previous_url,
    })


def add_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if not title.strip() or not description.strip():
            messages.error(request, "Musisz podać temat i opis!")
            return redirect('add-post')
        if title:
            Post.objects.create(user=request.user, title=title, description=description)
            return redirect('post-list')
        else:
            return redirect('add-post')
    return render(request, 'posts/add_post.html')    

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user:
        post.delete()
    return redirect(request.META.get('HTTP_REFERER', 'post-list'))

def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    next_url = request.GET.get('next') or request.POST.get('next') or request.META.get('HTTP_REFERER') or 'post-list'
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.description = request.POST.get('description')
        post.save()
        return redirect(next_url)
    
    return render(request, 'posts/edit_post.html', {'post': post, 'next': next_url})

def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        description = request.POST.get('description')
        previous_url = request.GET.get('next', None)
        
        if description:
            Comment.objects.create(user=request.user, post=post, description=description)
        
        if previous_url:
            return redirect(previous_url)
        return redirect('choose-post', post_id=post_id)


def delete_comment(request,comment_id,post_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    previous_url = request.META.get('HTTP_REFERER')
    if previous_url:
        return redirect(previous_url)
    return redirect('choose-post', post_id=post_id)

def edit_comment(request, comment_id, post_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    
    if request.method == "POST":
        description = request.POST.get("description")
        comment.description = description
        comment.save()
        return redirect('choose-post', post_id=post_id)
    else:
        context = {
            'post': post,
            'comments': comments,
            'edit_comment_id': str(comment_id),
        }
        return render(request, 'posts/choose_post.html', context)

def user_profile(request):
    posts = Post.objects.filter(user=request.user)
    comments = Comment.objects.filter(user=request.user)
    return render(request, 'posts/user_profile.html',{'posts':posts, 'comments':comments, 'user':request.user})

def comeback(request):
    next_url = request.GET.get('next')
    if next_url and next_url != "None":
        return redirect(next_url)
    return redirect('post-list')

@login_required
def toggle_like(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    existing_like = Like.objects.filter(user=request.user, comment=comment).first()

    if existing_like:
        existing_like.delete()
    else:
        Like.objects.create(user=request.user, comment=comment)

    return redirect(request.META.get('HTTP_REFERER', 'post-list'))

