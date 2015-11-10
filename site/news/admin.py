from django.contrib import admin
from news.models import Article

class ArticleAdmin(admin.ModelAdmin):
    #need to format this better
    list_display = ('title', 'newspaper', 'category', 'publish_date') 
    list_filter = ('publish_date', 'newspaper', 'category')
    search_fields = ('title',)

# Register your models here.
admin.site.register(Article, ArticleAdmin)
