from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)

    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk} -- {self.title}] :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

class Comment(models.Model):
    # 어떤 포스트에 대한 댓글인지
    # 여러 댓글이 한 포스트의 댓글이 되므로 post 필드에 ForeignKey 사용
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # 댓글 작성자
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 댓글 내용
    content = models.TextField()
    # 댓글 작성 일시
    created_at = models.DateTimeField(auto_now_add=True)
    # 댓글 수정 일시
    modified_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.author} :: {self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

