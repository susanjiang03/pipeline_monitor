from django.db import models

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

#3 main classes, newspaper, category and articles
class Newspaper(models.Model):
    name = models.CharField(max_length=20, unique=True)

    #will need to create slug here, for the urls

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.name


class Article(models.Model):
    #Newspaper | Category | Title | Link | Description
    newspaper = models.ForeignKey(Newspaper)
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title





