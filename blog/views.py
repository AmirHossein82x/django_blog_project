from django.shortcuts import render, redirect, reverse
from .models import Post
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .forms import PostForm, CommentForm
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
def post_list_view(request):
    # posts_list = Post.objects.all()
    posts_list = Post.objects.filter(status='pub').order_by("-datetime_modified")
    return render(request, 'blog/posts_list.html', {'posts_list': posts_list})

class PostListView(generic.ListView):
    # model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        return Post.objects.filter(status='pub').order_by("-datetime_modified")

@login_required
def post_detail_view(request, pk):
    posts = get_object_or_404(Post, pk=pk)
    comments = posts.comments.all()
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new = comment_form.save(commit=False)
            new.post = posts
            new.user = request.user
            new.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()


    # try:
    #    posts = Post.objects.get(pk=pk)
    # except Post.DoesNotExist:  we can use this
    # except ObjectDoesNotExist:  # we can use this too
    #     posts = None

    return render(request, 'blog/post_detail.html', {"posts": posts, 'comments': comments, 'comment_form': comment_form})

# class PostDetailView(generic.DetailView):
#     template_name = 'blog/post_detail.html'
#     model = Post
#     context_object_name = 'posts'


def post_create_view(request):
    # if request.method == "POST":
    #     post_title = request.POST.get('title')
    #     post_text = request.POST.get('text')
    #     user = User.objects.all()[0]
    #     Post.objects.create(title=post_title,
    #                         text=post_text,
    #                         author=user,
    #                         status='pub')
    # print(request.POST)
    # print(request.POST.get('title'))

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            form = PostForm()
            return redirect('posts_list')
    else:  # GET request
        form = PostForm()
    return render(request, 'blog/post_create.html', context={'form': form})

class PostCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = PostForm
    template_name = 'blog/post_create.html'
    context_object_name = 'form'

def post_update_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts_list')

    return render(request, "blog/post_create.html", context={'form': form})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    form_class = PostForm
    model = Post
    template_name = "blog/post_create.html"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # print(request.method)
    if request.method == "POST":
        post.delete()
        return redirect('posts_list')
    return render(request, "blog/post_delete.html", context={"post": post})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy('posts_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

