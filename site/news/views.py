'''
views file to render pages
'''
from django.shortcuts import render, redirect
from news.models import Article, Image
import feedparser
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
import re
newspapers = {'nytimes': 'New York Times', 'latimes': 'Los Angeles Times',
              'miamiherald': 'Miami Herald', 'seattletimes':'Seattle Times',
              'chron':'Houston Chronicles', 'denverpost':'Denver Post'}

#User Management Views
def user_login(request):
    template = 'login.html'
    return render(request, template)

def process_login(request): 
    email = request.POST['email']
    password = request.POST['password']

    # Validation
    required_fields = [email, password]
    trimmed = [i.strip() for i in required_fields]
    if "" in trimmed:
        return render(request, 'login.html', {'email': email, 'message': 'Missing Required Fields'})

    # Email validation
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return render(request, 'login.html', {'email': email, 'message': 'Invalid Email'})

    user = authenticate(username=email, password=password)

    if user is not None:
        login(request, user)
        previous_page = request.GET['next']
        if previous_page == '/news/register':
            return redirect(index)
        else:
            return redirect(previous_page)

    return render(request, 'index.html')

def user_logout(request):
    logout(request)
    return redirect(request.GET['next'])

def register(request):
    template = 'register.html'
    return render(request, template)

def process_register(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    # Validation
    required_fields = [email, first_name, last_name, password, confirm_password]
    trimmed = [i.strip() for i in required_fields]
    if "" in trimmed:
        return render(request, 'register.html', {'first_name': first_name, 'last_name': last_name, 'email': email, 'message': 'Missing Required Fields'})

    # Password matching
    if password != confirm_password:
        return render(request, 'register.html', {'first_name': first_name, 'last_name': last_name, 'email': email, 'message': 'Non-matching Passwords'})

    # Email validation
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return render(request, 'register.html', {'first_name': first_name, 'last_name': last_name, 'email': email, 'message': 'Invalid Email'})

    user = User.objects.create_user(email, email, password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    return render(request, 'login.html')

def reset_password(request):
    template = 'reset_password.html'

    return render(request, template)

def new_password(request):
    template = 'reset_password.html'

    return render(request, template)
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
            "title" : Article.objects.filter(newspaper=newspaper)[:m]
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

    for newspaper, category in zip(y[0::2], y[1::2]):
        feeds = Article.objects.filter(newspaper=newspaper, category=category)[:n]
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
    template = 'newspaper.html'
    paper = newspapers[newspaperlink]
    query = Article.objects.filter(newspaper=paper).values_list('category').distinct()
 
    dictcategory = []

    for category in query:
        category = category[0].encode('utf-8')
        dictcategory.append({ "size": len( Article.objects.filter(newspaper=paper, category=category)),
                            "category" : category,
                            "title" : Article.objects.filter(newspaper=paper, category=category)
        })


    return render(request, template, {'dictcategory' : dictcategory, 'paper':paper})


#view image
def images(request, urlid):
    template = 'images.html'
    article = Article.objects.filter(id=int(urlid))[0]
    imgurls = Image.objects.filter(article_id=int(urlid))
    num = len(imgurls)
    Message = str(num) + " image(s) was/were extracted."
    if num == 0:
       Message = "\nThere is no image in this site or there is an error during the population."
 
    return render(request, template, {'imgurls':imgurls, 'article':article, 'Message':Message})

#view all image
def allimages(request):
    template = 'allimages.html'
    imgurls = Image.objects.all()
    num = len(imgurls)
    Message = str(num) +" image(s) was/were extracted."
    #if no image
    if num == 0:
        Message += "\nThere is no image in all sites or there are errors during the population."

    return render(request, template, {'imgurls':imgurls, 'Message':Message})