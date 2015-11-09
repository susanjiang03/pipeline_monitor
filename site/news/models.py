from django.db import models
from django.template.defaultfilters import slugify
'''
class RSS(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    today_visited = models.IntegerField(default=0)
    total_visited = models.IntegerField(default=0)

    def __str__(self):
        return self.title
'''

#in order to create urls, newspaper and categories can be slugified
class Article(models.Model):
    #Newspaper | Category | Title | Link | Description
    newspaper = models.CharField(max_length=20) 
    category = models.CharField(max_length=15)
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.CharField(max_length=200)
    #2 slug fields for urls
    news_slug = models.SlugField(unique=True)
    cat_slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.news_slug = slugify(self.newspaper)
        self.cat_slug = slugify(self.category)
        super(Article, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title



