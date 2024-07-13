from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
from django.contrib import messages
from braces.views import SelectRelatedMixin
from . import models
from django.contrib.auth import get_user_model
from typing import Any, Dict

User = get_user_model()

class PostList(SelectRelatedMixin, generic.ListView):
    """View to list all posts."""
    model = models.Post
    select_related = ('user', 'group')

class UserPosts(LoginRequiredMixin, generic.ListView):
    """View to list posts by a specific user."""
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self) -> Any:
        """Return posts for a specific user."""
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add the post user to the context data."""
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

class PostDetail(LoginRequiredMixin, SelectRelatedMixin, generic.DetailView):
    """View to display details of a specific post."""
    model = models.Post
    select_related = ('user', 'group')

    def get_queryset(self) -> Any:
        """Return the specific post for the user."""
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    """View to create a new post."""
    fields = ('message', 'group')
    model = models.Post

    def form_valid(self, form) -> Any:
        """Assign the user to the post before saving."""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    """View to delete a post."""
    model = models.Post
    select_related = ('user', 'group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self) -> Any:
        """Ensure that only the user's own posts can be deleted."""
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args: Any, **kwargs: Any) -> Any:
        """Display a success message after deleting the post."""
        messages.success(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs)
