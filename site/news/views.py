from django.shortcuts import render
from news.models import Article
import feedparser


newspapers = {'nytimes': 'New York Times', 'latimes': 'Los Angeles Times', 'miamiherald': 'Miami Herald', 'seattletimes':'Seattle Times', 'chron':'Houston Chronicles', 'denverpost':'Denver Post'}
    
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
        link = [key for key, value in newspapers.iteritems() if value ==newspaper][0]
        dictpaper.append({
            "newspaperlink": link,
            "newspaper" : newspaper,
            "title" : Article.objects.filter(newspaper = newspaper)[:m]
            })

    return render(request, template, {'dictcategory' : dictcategory, 'dictpaper' : dictpaper})



def newspaper(request,newspaperlink):
    template='newspaper.html'
    paper=newspapers[newspaperlink]
    
    query = Article.objects.filter(newspaper__startswith=paper).values_list('category').distinct()
    
    dictcategory = []
    
    for category in query:
        category = category[0].encode('utf-8')
        dictcategory.append({
                            "size": len( Article.objects.filter(category = category)),
                            "category" : category,
                            "title" : Article.objects.filter(category = category)
                            })
    
    
    return render(request, template, {'dictcategory' : dictcategory,'paper':paper})