from django import forms

from .models import Comment


class CreateCommentForm(forms.ModelForm):
    body = forms.CharField(label="Add a comment", label_suffix="", widget=forms.Textarea(attrs={'rows': "1", 'class': 'form-field resize', "placeholder": "Comment"}))

    class Meta:
        model = Comment
        fields = ['body']



