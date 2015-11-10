from django.db import models
from datetime import datetime
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
    publish_date = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.title

