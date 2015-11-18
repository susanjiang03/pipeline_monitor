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
        feeds = Article.objects.filter(category=category)[:n]
        for each in feeds:
            if len(each.title) > 60:
                each.title = each.title[:60]+'...'.encode('utf-8')
            else:
                each.title = each.title.encode('utf-8')        

        dictcategory.append({
            "category" : category,
            "feeds" : feeds
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
        feeds = Article.objects.filter(newspaper=newspaper,category=category)[:n]
        for each in feeds:
            if len(each.title) > 60:
                each.title = each.title[:60]+'...'.encode('utf-8')
            else:
                each.title = each.title.encode('utf-8')        

        dictuserfeeds.append({
            "newspaper" : newspaper,
            "category" : category,
            "feeds" : feeds
            })

    return render(request, template, {'dictuserfeeds': dictuserfeeds})    

def newspaper(request,newspaperlink):
    template='newspaper.html'
    paper=newspapers[newspaperlink]
    query = Article.objects.filter(newspaper=paper).values_list('category').distinct()
    
    dictcategory = []
    
    for category in query:
        category = category[0].encode('utf-8')
        dictcategory.append({ "size": len( Article.objects.filter(newspaper=paper,category = category)),
                            "category" : category,
                            "title" : Article.objects.filter(newspaper=paper,category = category)
                            })
    
    
    return render(request, template, {'dictcategory' : dictcategory,'paper':paper})

