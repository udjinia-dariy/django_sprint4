from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse

from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Post, Comment
from ..forms import CommentForm


class CommentMixin(LoginRequiredMixin):
    """Установите модель по умолчанию и шаблон для просмотров комментариев."""

    model = Comment
    template_name = 'blog/comment.html'


class CommentCreateView(CommentMixin, CreateView):
    """Создать комментарий."""

    form_class = CommentForm
    _post = None

    def dispatch(self, request, *args, **kwargs):
        """Get post object or 404."""
        self._post = get_object_or_404(
            Post, pk=kwargs['post_id'],
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Сохранить экземпляр модели."""
        form.instance.author = self.request.user
        form.instance.post = self._post
        return super().form_valid(form)

    def get_success_url(self):
        """Вернуться на страницу сведений о публикации (blog:post_detail)."""
        return reverse('blog:post_detail', kwargs={'post_id': self._post.pk})


class CommentUpdDelMixin(CommentMixin, View):
    """Mixin для обновления комментариев и удаления просмотров."""

    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        """Проверка, является ли текущий пользователь автором комментария."""
        comment = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if comment.author != request.user:
            return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("blog:post_detail",
                       kwargs={'post_id': self.kwargs['post_id']})


class CommentUpdateView(CommentUpdDelMixin, UpdateView):
    """Изменить существующий текст комментария."""

    form_class = CommentForm


class CommentDeleteView(CommentUpdDelMixin, DeleteView):
    """Удалить существующий комментарий."""

    pass
