from django.contrib import admin
from news.models import Newspaper, Category, Article

# Register your models here.
admin.site.register(Newspaper)
admin.site.register(Category)
admin.site.register(Article)
