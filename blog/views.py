from django.views.generic import ListView
from .models import Post

# Create your views here.
class PostList(ListView):
    model = Post
    ordering = '-pk'