from django.shortcuts import render
from news.models import Article
import feedparser
    
def index(request):
    template = 'index.html'    
    query = Article.objects.values_list('category').distinct()
    dictcategory = []
    n = 5 #Number of Titles to display on Category blocks
    for category in query:
        category = category[0].encode('utf-8')
        dictcategory.append({
            "category" : category,
            "title" : Article.objects.filter(category = category)[:n]
            })
    query = Article.objects.values_list('newspaper').distinct()
    dictpaper = []
    m = 5 #Number of Titles to display on Paper blocks
    for newspaper in query:
        newspaper = newspaper[0].encode('utf-8')
        dictpaper.append({
            "newspaper" : newspaper,
            "title" : Article.objects.filter(newspaper = newspaper)[:m]
            })

    return render(request, template, {'dictcategory' : dictcategory, 'dictpaper' : dictpaper})