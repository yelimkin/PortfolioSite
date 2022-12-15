from django.contrib import admin
from .models import Post, Category, Tag
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
# admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
