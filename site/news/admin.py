from django.contrib import admin
from news.models import Article

#customize admin
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'news_slug':('newspaper',),
                           'cat_slug':('category',)}


# Register your models here.
admin.site.register(Article, ArticleAdmin)
