from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
from django.contrib import messages
from braces.views import SelectRelatedMixin
from .models import Post
from django.contrib.auth import get_user_model
from typing import Any, Dict

User = get_user_model()

class PostList(SelectRelatedMixin, generic.ListView):
    """View to list all posts with related user and group information."""
    model = Post
    select_related = ('user', 'group')
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10  # Paginate the posts to show 10 per page

    def get_queryset(self):
        """Return all posts ordered by most recent."""
        return Post.objects.select_related('user', 'group').order_by('-created_at')

class UserPosts(LoginRequiredMixin, generic.ListView):
    """View to list all posts by a specific user."""
    model = Post
    template_name = 'posts/user_post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self) -> Any:
        """Return posts of a specific user, ordered by most recent."""
        self.post_user = get_object_or_404(User, username__iexact=self.kwargs.get('username'))
        return self.post_user.posts.select_related('group').order_by('-created_at')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add user to context data to display in the template."""
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

class PostDetail(LoginRequiredMixin, SelectRelatedMixin, generic.DetailView):
    """View to display details of a specific post."""
    model = Post
    select_related = ('user', 'group')
    context_object_name = 'post'
    template_name = 'posts/post_detail.html'

    def get_queryset(self) -> Any:
        """Ensure the post belongs to the user specified in the URL."""
        return Post.objects.filter(user__username__iexact=self.kwargs.get('username')).select_related('group', 'user')

class CreatePost(LoginRequiredMixin, generic.CreateView):
    """View to create a new post."""
    model = Post
    fields = ('message', 'group')
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('posts:all')

    def form_valid(self, form) -> Any:
        """Set the current user as the post's author before saving."""
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        messages.success(self.request, 'Post created successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add additional context to the template."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Post'
        return context

class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    """View to delete a post."""
    model = Post
    select_related = ('user', 'group')
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:all')

    def get_queryset(self) -> Any:
        """Allow deletion only if the post belongs to the logged-in user."""
        return Post.objects.filter(user_id=self.request.user.id)

    def delete(self, request, *args: Any, **kwargs: Any) -> Any:
        """Display a success message after post deletion."""
        messages.success(self.request, 'Post deleted successfully.')
        return super().delete(request, *args, **kwargs)
