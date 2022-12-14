from django.views.generic import ListView, DetailView
from .models import Post, Category
from django.shortcuts import render

# Create your views here.
class PostList(ListView):
    model = Post
    paginate_by = 3
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        # get_context_data에서 기존에 제공했던 기능을 그대로 가져와 저장한다.
        context = super(PostList, self).get_context_data()
        # 모든 카테고리를 가져와서 'categories' 키에 연결해서 담는다.
        context['categories'] = Category.objects.all()
        # 카테고리가 지정되지 않은 포스트의 개수를 가져와서 'no_category_post_count'에 담는다.
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        # 인자로 받은 slug와 동일한 slug를 갖는 카테고리를 
        # 불러오는 쿼리셋을 만들어 categort 변수에 저장 
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request, 
        'blog/post_list.html',
        {   
            # 위에서 동일한 slug로 가져온 category만 가져오기
            'post_list' : post_list,
            # Post.objects.filter(category=category),
            'categories' : Category.objects.all(),
            'no_category_post_count' : Post.objects.filter(category=None).count(),
            # 페이지 타이틀 옆에 카테고리 이름
            'category' : category,
        }
    )