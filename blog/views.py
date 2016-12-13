from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    authors = Post.objects.filter(published_date__lte=timezone.now()).values('author__username')\
        .annotate(Count('author__username')).order_by('-author__username__count')
    return render(request, 'blog/post_list.html', {'posts': posts, 'authors': authors})


def posts_author(request, author):
    posts = Post.objects.filter(author__username=author).filter(published_date__lte=timezone.now()).order_by('published_date')
    authors = Post.objects.filter(published_date__lte=timezone.now()).values('author__username')\
        .annotate(Count('author__username')).order_by('-author__username__count')
    context = {
        'posts': posts,
        'authors': authors,
        'single_author': author
    }
    return render(request, 'blog/posts_author.html', context)


def post_detail(request, pk):
    post = Post.objects.filter(pk=pk).first()
    return render(request, 'blog/single.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request, author):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date').filter(author__username=author)
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/sign_up.html',{'form': form})



