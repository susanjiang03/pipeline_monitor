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
            "title" : [x.title[:60]+'...'.encode('utf-8') if len(x.title) > 60 else x for x in Article.objects.filter(category=category)[:n]]
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

def filterfeeds(request):
    template = 'filterfeeds.html'    
    query = Article.objects.values_list('newspaper').distinct()
    dictcheckbox = []
    for newspaper in query:
        newspaper = newspaper[0].encode('utf-8')
        category = Article.objects.filter(newspaper=newspaper).values_list('category').distinct()
        
        dictcheckbox.append({
            "title" : newspaper,
            "category" : [x[0].encode('utf-8') for x in category]
           	 })

    return render(request, template, {'dictcheckbox': dictcheckbox})

def userfeeds(request):
    template = 'userfeeds.html'
    y = []
    for key,value in request.POST.iteritems():
        y += [x.strip() for x in key.split(',')]
#    y.remove('V5kbcecFIUmKayAuo4dokXqjCJpBBuR4')
    y.remove('csrfmiddlewaretoken')
    dictuserfeeds = []
    n = 5
    for newspaper,category in zip(y[0::2],y[1::2]):
        dictuserfeeds.append({
            "newspaper" : newspaper,
            "category" : category,
            "feeds" : [x.title[:60]+'...'.encode('utf-8') if len(x.title) > 60 else x for x in Article.objects.filter(newspaper=newspaper,category=category)[:10]]
            })

    return render(request, template, {'dictuserfeeds': dictuserfeeds})    