'''
views file to render pages
'''
from django.shortcuts import render, redirect
from news.models import Article, Image, Bookmark
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
        elif previous_page == "":
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

    return redirect(user_login)

def reset_password(request):
    template = 'reset_password.html'
    return render(request, template)

def change_password(request):
    email = request.POST['email']
    old_password = request.POST['old_password']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']

    # Validation
    required_fields = [email, old_password, new_password, confirm_password]
    trimmed = [i.strip() for i in required_fields]
    if "" in trimmed:
        return render(request, 'reset_password.html', {'email': email, 'message': 'Missing Required Fields'})

    # Password matching
    if new_password != confirm_password:
        return render(request, 'reset_password.html', {'email': email, 'message': 'New Password is different from Confirm Password'})

    # Email validation
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return render(request, 'reset_password.html', {'email': email, 'message': 'Invalid Email'})

    user = authenticate(username=email, password=old_password)

    if user is not None:
        login(request, user)
        u = User.objects.get(username=email)
        u.set_password(new_password)
        u.save()
        logout(request)
        return redirect(user_login)
    else:
        return render(request, 'reset_password.html', {'email': email, 'message': 'Incorrect Password to Email or Email does not exist'})

'''
index page
'''
def index(request):
    template = 'index.html'
    query = Article.objects.values_list('category').distinct()
    dictcategory = []
    article_has_image=[]
    n = 5 #Number of Titles to display on Category blocks
    for category in query:
        category = category[0].encode('utf-8')
        feeds = Article.objects.filter(category=category).order_by('-publish_date')[:n]

        #find out if each article in feed has image and text in Image table
        for each in feeds:
            article=Image.objects.filter(article_id=each.id)
            if(len(article)>0):
                article_has_image.append(each.id)

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
        titles=Article.objects.filter(newspaper=newspaper)[:m]
        
        #find out if each article in feed has image and text in Image table
        for each in titles:
            article=Image.objects.filter(article_id=each.id)
            if(len(article)>0):
                article_has_image.append(each.id)

        dictpaper.append({
            "newspaperlink": link,
            "newspaper" : newspaper,
            "title" : Article.objects.filter(newspaper=newspaper).order_by('-publish_date')[:m]
            })
        
    bookmarkfilter = Bookmark.objects.filter(user_id=request.user.id)
    bookmark = []
    for each in bookmarkfilter:
        bookmark.append(each.article_id)

    return render(request, template, {'dictcategory' : dictcategory, 'dictpaper' : dictpaper, 'bookmark': bookmark,'article_has_image':article_has_image,'n':n})

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
        feeds = Article.objects.filter(newspaper=newspaper, category=category).order_by('-publish_date')[:n]
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
            
            size=len(rss.entries)
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
                "titlelink" : titlelink,
                "size":size
                })

    return render(request, template, {'dictuserfeeds': dictuserfeeds, 'dictuserinput': dictuserinput})



def newuserfeeds(request):
    template = 'userfeeds.html'
    y = []
    for item in request.POST.getlist('newspapercategory[]'):
        y += [x.strip() for x in item.split(',')]
    dictuserfeeds = []
    n = 10
    
    for newspaper, category in zip(y[0::2], y[1::2]):
        feeds = Article.objects.filter(newspaper=newspaper, category=category).order_by('-publish_date')[:n]
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

    updateinput=[]
    for item in request.POST.getlist('userInput[]'):
        if request.POST[item]!="":
            updateinput.append(request.POST[item])
        else:
            updateinput.append(item)

    dictuserinput = []
    for url in updateinput:
    
        rss = feedparser.parse(url)
        titlelink = []
            
        size=len(rss.entries)
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
                "titlelink" : titlelink,
                "size":size
            })

    return render(request, template,  {'dictuserfeeds': dictuserfeeds,'dictuserinput': dictuserinput})



def newspaper(request, newspaperlink):
    template = 'newspaper.html'
    paper = newspapers[newspaperlink]
    query = Article.objects.filter(newspaper=paper).values_list('category').distinct()
 
    dictcategory = []
    article_has_image=[]
    category_has_image=[]
    for category in query:
        category = category[0].encode('utf-8')
        titles=Article.objects.filter(newspaper=paper, category=category)
        dictcategory.append({ "size": len( Article.objects.filter(newspaper=paper, category=category)),
                            "category" : category,
                            "title" : Article.objects.filter(newspaper=paper, category=category).order_by('-publish_date')
        })
        for each in titles:
            article=Image.objects.filter(article_id=each.id)
            if(len(article)>0):
                article_has_image.append(each.id)
                if category not in category_has_image:
                    category_has_image.append(category)

    bookmarkfilter = Bookmark.objects.filter(user_id=request.user.id)
    bookmark = []
    for each in bookmarkfilter:
        bookmark.append(each.article_id)

    return render(request, template, {'dictcategory' : dictcategory, 'paper':paper, 'bookmark': bookmark,'newspaperlink':newspaperlink,'article_has_image':article_has_image,'category_has_image':category_has_image})


#view image
def image_text(request, urlid):
    template = 'image_text.html'
    article = Article.objects.filter(id=int(urlid))[0]
    imgurls = Image.objects.filter(article_id=int(urlid))
    num = len(imgurls)
    return render(request, template, {'imgurls':imgurls, 'article':article})

#view top image and main text for all articles
def allarticles(request):
    template = 'allarticles.html'
    
    image_text = Image.objects.all().distinct()
    num = len(image_text)
    article_main=[]
    max_length=2000
    for each in image_text:
        article=Article.objects.filter(id=each.article_id)[0]
        
        if len(each.main_text)>max_length:
            text=each.main_text[0:max_length-1]+"...(MORE)"
        article_main.append({
            "title":article.title.encode('utf-8'),
            "url":article.url.encode('utf-8'),
            "newspaper":article.newspaper.encode('utf-8'),
            "category":article.category.encode('utf-8'),
            "image":each.image_url,
            "text":text,
        })
   
    return render(request, template, {'article_main':article_main, 'num':num})





def add_to_bookmark(request, article_id):
    user_id = request.user.id
    bookmark = Bookmark(user_id=user_id, article_id=article_id)
    bookmark.save()

    return redirect(request.GET['next'])

def remove_from_bookmark(request, article_id):
    user_id = request.user.id
    Bookmark.objects.filter(user_id=user_id,article_id=article_id).delete()

    return redirect(request.GET['next'])

def bookmark(request):
    template = 'bookmark.html'

    bookmarkdict = {}
    bookmark_query =  Bookmark.objects.filter(user_id=request.user.id)
    for each in bookmark_query:
        article_query = Article.objects.get(id=each.article_id)

        if len(article_query.title) > 60:
            article_query.title = article_query.title[:60]+'...'.encode('utf-8')
        else:
            article_query.title = article_query.title.encode('utf-8')

        if article_query.category in bookmarkdict:
            bookmarkdict[article_query.category].update({article_query})
        else:
            bookmarkdict[article_query.category] = {article_query}

    for key in bookmarkdict:
        bookmarkdict[key] = list(bookmarkdict[key])

    return render(request, template, {'bookmarkdict': bookmarkdict})



#category
def category(request,thiscategory):
    template='category.html'
    dictcate=Article.objects.filter(category=thiscategory)
    return render(request,template,{'category':dictcate,'catename':thiscategory,'size':len(dictcate)})

#for each category in newspaper, display top image and main text
def newspaper_category(request,newspaperlink,thiscategory):
    template='newspaper_category.html'
    paper = newspapers[newspaperlink]
    #get a array of articles in this category of this newspaper
    articles=Article.objects.filter(category=thiscategory,newspaper=paper)
    article_main=[]
    max_length=3000
    for each in articles:
        article=Image.objects.filter(article_id=each.id)
        #if no image or text populated in image table
        if len(article)==0:
           top_image=""
           main_text=""
        else:
           thisarticle=article[0]
           top_image=thisarticle.image_url.encode('utf-8')
           main_text=thisarticle.main_text.encode('utf-8')
           if len(main_text)>max_length:
               main_text=main_text[0:max_length-1]+"...MORE"

        article_main.append({
            "title":each.title.encode('utf-8'),
            "url":each.url.encode('utf-8'),
            "image":top_image,
            "text":main_text,
            })
    return render(request,template,{'paper':paper,'catename':thiscategory,'size':len(articles),'article_main':article_main})



