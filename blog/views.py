from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category, Tag
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from .forms import PostForm, CommentForm
from django.utils.text import slugify

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
        context['comment_form'] = CommentForm
        return context

class PostCreate(CreateView, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    # fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def form_valid(self, form):
        current_user = self.request.user
        
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user

            response = super(PostCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')
            # return super(PostCreate, self).form_valid(form)

            if tags_str:
                tags_str = tags_str.strip()

                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)

            return response

        else:
            # return redirect('/blog/')
            return redirect('/blog/')

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    template_name = 'blog/post_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tags_str_list)

        return context

    def dispatch(self, request, *args, **kwargs):
        # 사용자가 로그인 상태이고 사용자가 포스트의 소유자인지
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            return PermissionDenied
    
    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tag_str = self.request.POST.get('tags_str')
        if tag_str:
            tag_str = tag_str.strip()
            tag_str = tag_str.replace(',', ';')
            tags_list = tag_str.split(';')

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response

def category_page(request, slug):
    if slug == 'no_category':
        category = 'no category'
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

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    print(post_list)
    # 선택한 태그 리스트 -> bootstrap 태그인 리스트 <QuerySet [<Post: [14 -- 태그_테스트1] :: bbb>, <Post: [16 -- 태그_테스트3] :: aaa>]>

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list' : post_list,
            'tag' : tag,
            'categories' : Category.objects.all(),
            'no_category_post_count' : Post.objects.filter(category=None).count(),
        }
    )

def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied