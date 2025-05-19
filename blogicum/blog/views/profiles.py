from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

from django.views.generic import (
    ListView, UpdateView
)
from ..models import Post
from ..forms import ProfileEditForm

User = get_user_model()


class ProfileListView(ListView):
    """Показать страницу пользователя с сообщениями."""

    model = Post
    paginate_by = 10
    template_name = 'blog/profile.html'

    def get_queryset(self):
        """Возврат сообщений для автора <username>."""
        filters = {'author__username': self.kwargs['username']}
        if self.request.user.username != self.kwargs['username']:
            # Hide unpublished posts for other users.
            filters.update({
                'is_published__exact': True,
                'pub_date__lte': timezone.now()
            })
        return (self.model.objects.select_related('author')
                .filter(**filters).order_by('-pub_date')
                .annotate(comment_count=Count("comment")))

    def get_context_data(self, **kwargs):
        """Добавьте профиль в контекст."""
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Показать форму редактирования для данного пользователя."""

    template_name = 'blog/user.html'
    form_class = ProfileEditForm

    def get_object(self, queryset=None):
        """Вернуть объект пользователя."""
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user])
