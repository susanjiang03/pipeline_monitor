from django.db import models
from datetime import datetime

#in order to create urls, newspaper and categories can be slugified
class Article(models.Model):
    """
    Model to store all the article data coming from the RSS feeds
    obtained through feedparser
    """
    #Newspaper | Category | Title | Link | Description
    newspaper = models.CharField(max_length=20) 
    category = models.CharField(max_length=15)
    title = models.TextField(default='')
    url = models.URLField()
    description = models.TextField(default='')
    publish_date = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return self.title

class Image(models.Model):
    """
    Image model to grab image from a particular url and attach it to an article in the db
    will store image source and main article text
    """
    # article_id | images_url
    article_id=models.IntegerField()
    image_url=models.URLField()
    main_text=models.TextField(null=True, blank=True)

class Bookmark(models.Model):
    """
    Bookmark model to store saved articles based on user id
    """
    # user_id | article_id
    user_id=models.IntegerField()
    article_id=models.IntegerField()
