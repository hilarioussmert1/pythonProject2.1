from .models import Post, Category
from django import forms


class PostForm(forms.ModelForm):
    post_category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Категория',
    )

    class Meta:
        model = Post
        fields = [
            'creator',
            'title',
            'content_text',
            'post_category',
        ]