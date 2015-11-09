from django.contrib import admin
from news.models import Article

class ArticleAdmin(admin.ModelAdmin):
    #need to format this better
    list_display = ('newspaper', 'category', 'title') 

# Register your models here.
admin.site.register(Article, ArticleAdmin)
