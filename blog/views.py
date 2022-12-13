from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.
class PostList(ListView):
    model = Post
    paginate_by = 3
    ordering = '-pk'

class PostDetail(DetailView):
    model = Post;
    # 