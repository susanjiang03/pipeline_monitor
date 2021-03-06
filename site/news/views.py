'''
views file to render pages
'''
import re
import feedparser
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from news.models import Article, Image, Bookmark

newspapers = {'nytimes': 'New York Times', 'latimes': 'Los Angeles Times',
              'miamiherald': 'Miami Herald', 'seattletimes':'Seattle Times',
              'chron':'Houston Chronicles', 'denverpost':'Denver Post'}

#User Management Views
def user_login(request):
    """Renders The Login page"""
    template = 'login.html'
    return render(request, template)

def process_login(request):
    """Process the Login Form to login the user"""
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
            return redirect('news:index')
        elif previous_page == "":
            return redirect('news:index')
        else:
            return redirect(previous_page)

    return render(request, 'index.html')

def user_logout(request):
    """Logout the user"""
    logout(request)
    return redirect(request.GET['next'])

def register(request):
    """Renders the Register page"""
    template = 'register.html'
    return render(request, template)

def process_register(request):
    """Process the Register Form to create a user"""
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    # Validation
    required_fields = [email, first_name, last_name, password, confirm_password]
    trimmed = [i.strip() for i in required_fields]
    if "" in trimmed:
        return render(request, 'register.html', {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'message': 'Missing Required Fields'})

    # Password matching
    if password != confirm_password:
        return render(request, 'register.html', {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'message': 'Non-matching Passwords'})

    # Email validation
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return render(request, 'register.html', {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'message': 'Invalid Email'})

    user = User.objects.create_user(email, email, password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    return redirect('news:user_login')

def reset_password(request):
    """Renders the Reset Password page"""
    template = 'reset_password.html'
    return render(request, template)

def change_password(request):
    """Process the reset_password Form to reset the user's password"""
    email = request.POST['email']
    old_password = request.POST['old_password']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']

    # Validation
    required_fields = [email, old_password, new_password, confirm_password]
    trimmed = [i.strip() for i in required_fields]
    if "" in trimmed:
        return render(request, 'reset_password.html', {
            'email': email,
            'message': 'Missing Required Fields'})

    # Password matching
    if new_password != confirm_password:
        return render(request, 'reset_password.html', {
            'email': email,
            'message': 'New Password is different from Confirm Password'})

    # Email validation
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return render(request, 'reset_password.html', {
            'email': email,
            'message': 'Invalid Email'})

    user = authenticate(username=email, password=old_password)

    if user is not None:
        login(request, user)
        userget = User.get(username=email)
        userget.set_password(new_password)
        userget.save()
        logout(request)
        return redirect('news:user_login')
    else:
        return render(request, 'reset_password.html', {
            'email': email,
            'message': 'Incorrect Password to Email or Email does not exist'})

def index(request):
    """Renders the Index Page (Main Page)"""
    template = 'index.html'
    query = Article.objects.values_list('category').distinct()
    dictcategory = []
    article_has_image = []
    num = 5 #Number of Titles to display on Category blocks
    for categorys in query:
        categorys = categorys[0].encode('utf-8')
        feeds = Article.objects.filter(category=categorys).order_by('-publish_date')[:num]

        #find out if each article in feed has image and text in Image table
        for each in feeds:
            article = Image.objects.filter(article_id=each.id)
            if len(article) > 0:
                article_has_image.append(each.id)

        dictcategory.append({
            "category" : categorys,
            "feeds" : feeds
            })

    nums = 5
    query = Article.objects.values_list('newspaper').distinct()
    dictpaper = []
    for newspaper in query:
        newspaper = newspaper[0].encode('utf-8')
        link = [key for key, value in newspapers.iteritems() if value == newspaper][0]

        #find out if each article in feed has image and text in Image table
        for each in Article.objects.filter(newspaper=newspaper)[:nums]:
            article = Image.objects.filter(article_id=each.id)
            if len(article) > 0:
                article_has_image.append(each.id)

        dictpaper.append({
            "newspaperlink": link,
            "newspaper" : newspaper,
            "title" : Article.objects.filter(newspaper=newspaper).order_by('-publish_date')[:nums]
            })

    bookmarks = []
    for each in Bookmark.objects.filter(user_id=request.user.id):
        bookmarks.append(each.article_id)

    return render(request, template, {
        'dictcategory' : dictcategory,
        'dictpaper' : dictpaper,
        'bookmarks': bookmarks,
        'article_has_image':article_has_image,
        'n':num})

def about(request):
    '''About page'''
    return render(request, 'about.html')

def filterfeeds(request):
    """Renders the FilterFeeds Page"""
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
    """Process the FilterFeeds Form to renders the Userfeeds Page"""
    template = 'userfeeds.html'
    postlist = []
    for item in request.POST.getlist('newspapercategory[]'):
        postlist += [x.strip() for x in item.split(',')]
    dictuserfeeds = []
    num = 10

    for news, cat in zip(postlist[0::2], postlist[1::2]):
        feeds = Article.objects.filter(newspaper=news, category=cat).order_by('-publish_date')[:num]

        dictuserfeeds.append({
            "newspaper" : news,
            "category" : cat,
            "feeds" : feeds
            })

    dictuserinput = []
    for url in request.POST.getlist('userRSS[]'):
        if url != "":
            rss = feedparser.parse(url)
            titlelink = []
            size = len(rss.entries)
            for post in rss.entries[:num]:
                title = post.title.encode('utf-8')
                link = post.link
                titlelink.append({
                    "title" : title,
                    "url" : link
                    })
            dictuserinput.append({
                "rssurl" : url,
                "titlelink" : titlelink,
                "size" : size
                })

    return render(request, template, {
        'dictuserfeeds': dictuserfeeds,
        'dictuserinput': dictuserinput})

def newspaper(request, newspaperlink):
    """Renders the Newspaper Page for each Newspaper which display all the categories with a set amount of article titles"""
    template = 'newspaper.html'
    paper = newspapers[newspaperlink]
    query = Article.objects.filter(newspaper=paper).values_list('category').distinct()

    dictcategory = []
    article_has_image = []
    category_has_image = []
    for category in query:
        category = category[0].encode('utf-8')
        titles = Article.objects.filter(newspaper=paper, category=category)
        dictcategory.append({
            "size": len(titles),
            "category" : category,
            "title" : Article.objects.filter(newspaper=paper, category=category).order_by('-publish_date')
        })
        for each in titles:
            article = Image.objects.filter(article_id=each.id)
            if len(article) > 0:
                article_has_image.append(each.id)
                if category not in category_has_image:
                    category_has_image.append(category)

    bookmarkfilter = Bookmark.objects.filter(user_id=request.user.id)
    bookmark = []
    for each in bookmarkfilter:
        bookmark.append(each.article_id)

    return render(request, template,
                  {'dictcategory' : dictcategory,
                   'paper':paper,
                   'bookmark': bookmark,
                   'newspaperlink':newspaperlink,
                   'article_has_image':article_has_image,
                   'category_has_image':category_has_image})


#view image
def image_text(request, urlid):
    """Renders the Image Page of an Article"""
    template = 'image_text.html'
    article = Article.objects.filter(id=int(urlid))[0]
    imgurls = Image.objects.filter(article_id=int(urlid))
    return render(request, template, {'imgurls':imgurls, 'article':article})

#view top image and main text for all articles
def allarticles(request):
    """Renders the All Articles Page which displays One Image and The main text of all articles"""
    template = 'allarticles.html'

    image_text = Image.objects.all().distinct()
    article_main = []
    max_length = 2000
    num_article_display = 30
    if len(image_text)< 30:
        num_article_display = len(image_text)
    for each in image_text[0: num_article_display]:
        article = Article.objects.filter(id=each.article_id)[0]
        main_text = each.main_text
        if len(each.main_text) > max_length:
            main_text = main_text[0:max_length-1]+"...(MORE)"
        article_main.append({
            "title":article.title.encode('utf-8'),
            "url":article.url.encode('utf-8'),
            "newspaper":article.newspaper.encode('utf-8'),
            "category":article.category.encode('utf-8'),
            "image":each.image_url,
            "text":main_text
        })

    return render(request, template, {'article_main':article_main, 'num':num_article_display})

def add_to_bookmark(request, article_id):
    """Add an article linking to the current user to the bookmark database"""
    user_id = request.user.id
    bookmark = Bookmark(user_id=user_id, article_id=article_id)
    bookmark.save()

    return redirect(request.GET['next'])

def remove_from_bookmark(request, article_id):
    """Remove the link between the current user and the article from the bookmark database"""
    user_id = request.user.id
    Bookmark.objects.filter(user_id=user_id, article_id=article_id).delete()

    return redirect(request.GET['next'])

def bookmark(request):
    """Renders the Bookmark page which displays all the bookmarked article's title"""
    template = 'bookmark.html'

    bookmarkdict = {}
    bookmark_query = Bookmark.objects.filter(user_id=request.user.id)
    for each in bookmark_query:
        article_query = Article.objects.get(id=each.article_id)

        if len(article_query.title) > 60:
            article_query.title = article_query.title[:60] + '...'.encode('utf-8')
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
def category(request, thiscategory):
    """Renders the category page which displays all the articles in that category"""
    template = 'category.html'
    dictcate = Article.objects.filter(category=thiscategory)
    return render(request, template, {
        'category':dictcate,
        'catename':thiscategory,
        'size':len(dictcate)})

#for each category in newspaper, display top image and main text
def newspaper_category(request, newspaperlink, thiscategory):
    """Renders the newspaper_category which displays the top image and main text for each category in each newspaper"""
    template = 'newspaper_category.html'
    paper = newspapers[newspaperlink]
    #get a array of articles in this category of this newspaper
    articles = Article.objects.filter(category=thiscategory, newspaper=paper)
    article_main = []
    max_length = 3000
    for each in articles:
        article = Image.objects.filter(article_id=each.id)
        #if no image or text populated in image table
        if len(article) == 0:
            top_image = ""
            main_text = ""
        else:
            thisarticle = article[0]
            top_image = thisarticle.image_url.encode('utf-8')
            main_text = thisarticle.main_text.encode('utf-8')
            if len(main_text) > max_length:
                main_text = main_text[0:max_length-1]+"...MORE"

        article_main.append({
            "title":each.title.encode('utf-8'),
            "url":each.url.encode('utf-8'),
            "image":top_image,
            "text":main_text,
            })

    return render(request, template, {
        'paper':paper,
        'catename':thiscategory,
        'size':len(articles),
        'article_main':article_main})


#search keyword
def search_keyword(request):
    """Renders the search_keyword page which allows the user to search for a keyword in the main text of an article"""
    template = 'search_keyword.html'
    
    return render(request, template)

#return the articles text contains user's keywords
def article_by_keyword(request):
    """Processes the search_keyword and renders the allarticles page which displays the relevant searches"""
    template = 'allarticles.html'
    keyword = request.POST['userkeyword']
    query = Image.objects.filter(main_text__contains=keyword).distinct()
    num = len(query)
    by_keyword = 'True'
    articles = []
    for each in query:
        text = each.main_text
        image = each.image_url
        article = Article.objects.filter(id=each.article_id)[0]
        
        articles.append({
                            "newspaper": article.newspaper,
                            "category": article.category,
                            "title" : article.title,
                            "url" :   article.url,
                            "image": image,
                            "text": text,
                        })
    
    return render(request, template,
                  {'keyword':keyword,'article_main':articles,'num':num,'by_keyword':by_keyword})
