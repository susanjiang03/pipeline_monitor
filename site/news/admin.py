from django.contrib import admin
from news.models import Article, Image


class ArticleAdmin(admin.ModelAdmin):
    #need to format this better
    list_display = ('title', 'newspaper', 'category', 'publish_date') 
    list_filter = ('publish_date', 'newspaper', 'category')
    search_fields = ('title',)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('article_id', 'image_url')

# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(Image, ImageAdmin)
