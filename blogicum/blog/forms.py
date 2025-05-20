from django import forms
from django.contrib.auth import get_user_model

from .models import Post, Comment

User = get_user_model()


class PostForm(forms.ModelForm):
    """Опубликовать форму создания/обновления."""

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local'}
            )
        }


class ProfileEditForm(forms.ModelForm):
    """Обновите форму данных пользователя."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class CommentForm(forms.ModelForm):
    """Создать/редактировать форму комментариев."""

    class Meta:
        model = Comment
        fields = ('text',)
