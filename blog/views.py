from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm, SortItemsBy


def post_list(request):
    """
    Main page(only posts that have published date filled in)
    """
    if request.method == "POST":
        form = SortItemsBy(request.POST)
        print(form)
    # if sorted == 'old_first':
    #     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')\
    #         .annotate(num_votes=Count('votes__object_id'))
    # elif sorted == 'new_first':
    #     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')\
    #         .annotate(num_votes=Count('votes__object_id'))
    # else:
    posts = Post.objects.filter(published_date__lte=timezone.now()).annotate(num_votes=Count('votes__object_id'))\
            .order_by('num_votes')
    authors = Post.objects.filter(published_date__lte=timezone.now()).values('author__username')\
            .annotate(Count('author__username')).order_by('-author__username__count')
        # QuerySet with posts that were liked by user(who is authenticated now)
    user_likes = Post.votes.all(request.user.id)
    context = {
        'posts': posts,
        'authors': authors,
        'user_likes': user_likes
    }
    return render(request, 'blog/post_list.html', context)


def posts_author(request, author):
    """
    Page with posts for selected author
    """
    posts = Post.objects.filter(author__username=author).filter(published_date__lte=timezone.now()).\
        order_by('published_date').annotate(num_votes=Count('votes__object_id'))
    authors = Post.objects.filter(published_date__lte=timezone.now()).values('author__username')\
        .annotate(Count('author__username')).order_by('-author__username__count')
    user_likes = Post.votes.all(request.user.id)
    context = {
        'posts': posts,
        'authors': authors,
        'single_author': author,
        'user_likes': user_likes
    }
    return render(request, 'blog/posts_author.html', context)


def post_detail(request, pk):
    """
    Page for single post
    """
    post = Post.objects.filter(pk=pk).annotate(num_votes=Count('votes__object_id')).first()
    print(post)
    user_likes = Post.votes.all(request.user.id)
    context = {
        'post': post,
        'user_likes': user_likes
    }
    return render(request, 'blog/single.html', context)


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
    """
    Posts that were created by author but not published(raw posts)
    """
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date').filter(author__username=author)
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    """
    For 'publish' button
    """
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def sign_up(request):
    """
    User registration. Use UserCreationForm. After successful registration redirect to main page.
    """
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


def likes(request):
    """
    Add or remove like from post
    """
    article = Post.objects.get(pk=request.GET.get("post"))
    user_vote = article.votes.exists(request.user.id)
    if user_vote:
        article.votes.down(request.user.id)
        is_liked = False
    else:
        article.votes.up(request.user.id)
        is_liked = True
    context = {
        'num_likes': article.votes.count(),
        'is_liked': is_liked
    }
    return JsonResponse(context, safe=False)

