'''
views file to render pages
'''

from django.shortcuts import render
from news.models import Article
import feedparser

newspapers = {'nytimes': 'New York Times', 'latimes': 'Los Angeles Times',
              'miamiherald': 'Miami Herald', 'seattletimes':'Seattle Times',
              'chron':'Houston Chronicles', 'denverpost':'Denver Post'}

'''
index page
'''
def index(request):
    template = 'index.html'
    query = Article.objects.values_list('category').distinct()
    dictcategory = []
    n = 5 #Number of Titles to display on Category blocks
    for category in query:
        category = category[0].encode('utf-8')
        feeds = Article.objects.filter(category=category)[:n]

        #if title is too long .. it
        for each in feeds:
            if len(each.title) > 55:
                each.title = each.title[:55]+'...'.encode('utf-8')
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
    for item in request.POST.getlist('newspapercategory[]'):
        y += [x.strip() for x in item.split(',')]
    dictuserfeeds = []
    n = 10

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

    dictuserinput = []
    for url in request.POST.getlist('userRSS[]'):
        if url != "":
            rss = feedparser.parse(url)
            titlelink = []
            for post in rss.entries[:n]:
                if len(post.title.encode('utf-8')) > 60:
                    title = post.title[:60]+'...'.encode('utf-8')
                else:
                    title = post.title.encode('utf-8')

                link = post.link
                titlelink.append({
                    "title" : title,
                    "url" : link
                    })
            dictuserinput.append({
                "rssurl" : url,
                "titlelink" : titlelink
                })

    return render(request, template, {'dictuserfeeds': dictuserfeeds, 'dictuserinput': dictuserinput})

def newspaper(request, newspaperlink):
    template='newspaper.html'
    paper = newspapers[newspaperlink]
    query = Article.objects.filter(newspaper=paper).values_list('category').distinct()
 
    dictcategory = []

    for category in query:
        category = category[0].encode('utf-8')
        dictcategory.append({ "size": len( Article.objects.filter(newspaper=paper,category = category)),
                            "category" : category,
                            "title" : Article.objects.filter(newspaper=paper,category = category)
                            })


    return render(request, template, {'dictcategory' : dictcategory, 'paper':paper})

