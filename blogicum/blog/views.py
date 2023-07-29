from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from .forms import CommentForm, PostForm, UserForm
from .models import Category, Comment, Post

User = get_user_model()


def posts():
    return Post.objects.select_related(
        'location', 'author', 'category'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.now()
    )


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = posts()
    ordering = '-pub_date'
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.kwargs['pk']:
            reverse_lazy('blog:index')
        get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments
            .select_related('author')
            .order_by('created_at')
        )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:post_detail')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('blog:post_detail', pk=self.kwargs['pk'])
        get_object_or_404(Post, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['pk']}
        )


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


class CategoryListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_queryset(self):
        category = get_object_or_404(
            Category,
            is_published=True,
            slug=self.kwargs['category_slug']
        )
        return posts().filter(category=category).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            is_published=True,
            slug=self.kwargs['category_slug']
        )
        return context


class ProfileListView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = 10

    def get_queryset(self):
        profile = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.select_related(
            'location', 'author', 'category'
        ).filter(author=profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.publication = get_object_or_404(Post, pk=kwargs['pk'])
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.publication = self.publication
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'pk': self.publication.pk}
        )


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('blog:post_detail', pk=self.kwargs['post_id'])
        get_object_or_404(Comment, pk=kwargs['pk'])

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['post_id']}
        )


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('blog:post_detail', pk=self.kwargs['post_id'])
        get_object_or_404(Comment, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['post_id']}
        )
