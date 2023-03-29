from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from dtwee_app.models import TweeUser
from dtwee_app.validators import unique


class UserEditForm(ModelForm):
    avatar = forms.ImageField(required=False)
    username = forms.CharField(max_length=150)
    # https://code.djangoproject.com/ticket/23547
    remove_avatar = forms.BooleanField(required=False)

    def save(self, commit=True):
        instance: User = super().save(commit=commit)
        t_user, created = TweeUser \
            .objects \
            .get_or_create(user=instance)

        if self.cleaned_data.get('remove_avatar', False):
            t_user.avatar.name = 'avatars/default.png'
            t_user.save()

        if self.cleaned_data.get('avatar', None) is not None:
            t_user.avatar = self.cleaned_data['avatar']
            t_user.save()

        return instance

    class Meta:
        fields = ('username', 'first_name', 'last_name', 'email', 'avatar')
        model = User
