from django.db import models


class RSS(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    today_visited = models.IntegerField(default=0)
    total_visited = models.IntegerField(default=0)

    def __str__(self):
        return self.title