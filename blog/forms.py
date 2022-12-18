from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
        widgets = {
            'content' : SummernoteWidget(
                attrs= {
                    'summernote' : {
                        'width' : '100%',
                        'height' : '400px',
                        'iframe' : False,
                        'lang' : 'ko-KR',
                        'codemirror' : {
                            'mode' : 'htmlmixed',
                        },
                    }
                }
            ),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )