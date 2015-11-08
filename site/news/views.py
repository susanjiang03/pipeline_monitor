from django.shortcuts import render
#from news.models import RSS
import feedparser

'''
def index(request):
    template = 'index.html'
    with open('news/rssurls.txt') as f:
        for line in f:
            rss = feedparser.parse(line)
            for post in rss.entries:
                if not RSS.objects.filter(link = post.link):
                    post_description = post.description.encode('utf-8')
                    q_description = post.description[:post.description.find('<br clear=')]
                    q = RSS(title = post.title.encode('utf-8'), link = post.link, description = q_description, today_visited = 0, total_visited = 0,)
                    q.save()
    trending = RSS.objects.all().order_by('today_visited')[:10]

    return render(request, template, {'trending': trending})
'''
    
def index(request):
    return render(request, 'index.html', {}) 
