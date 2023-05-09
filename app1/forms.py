from django.forms import ModelForm
from .models import Post, User
from django import forms

from tinymce.widgets import TinyMCE

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False
    
class PostForm(ModelForm):
    body = forms.CharField(
        widget=TinyMCEWidget(attrs=
                       {'cols': 30, 'rows': 12}))
    class Meta:
        model = Post 
        fields = '__all__'
        exclude = ['Author',  'time_created']

    image = forms.ImageField(required=False, label='Post Image')