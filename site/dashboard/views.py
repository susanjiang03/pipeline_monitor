from django.shortcuts import render
from django.contrib import admin
from django.db import models
from news.models import Article, Image, RSSurl
import csv
from django.utils.encoding import smart_str, smart_unicode
from django.http import HttpResponse
# Create your views here.

'''index page of dashboard app, this page will show  the statistic of data populated to database,
    show the number of valid  and invalid rss urls, the number of feed populated from each rss url,
    the number of image from each rss url and the number of article with main text extraced, and display 
the percentage for analysis, each valid rss url can link to  the dashboard for the artciles populated from this rss url'''


def total_summary(request):
    template = 'dash_base.html'
    #initialize
    feedurls=[]
    total_articles = 0
    total_images = 0
    total_text = 0
    pct_of_images = 0
    pct_of_text = 0
    
    #get the array of rss url from RSSurl and number of valid and invalid rssurl
    query = RSSurl.objects.all().distinct()
    num_urls = len(query)
    valid_query = RSSurl.objects.filter(valid=True)
    valid_urls = len(valid_query)
    pct_valid = valid_urls/float(num_urls) *100
    invalid_urls = num_urls - valid_urls
    
    #loop through the arrary
    for each in query:
        url = each.rss_url.encode('UTF-8')
        valid = each.valid
        articlequery = Article.objects.filter(rssurl_id=each.id)
        #initialize
        number_of_articles = len(articlequery)
        number_of_images = 0
        number_of_text= 0
        pct_of_images = 0
        pct_of_text = 0
        newspaper = ""
        category = ""
        
        #get the artcles for this rss url
        for article in articlequery:
            newspaper = article.newspaper
            category = article.category
            image = Image.objects.filter(article_id=article.id)
            
            if image :
                # get the stat of image
                if image[0].image_url :
                    number_of_images += 1
                        # get the stat of main_text
                if image[0].main_text :
                    number_of_text += 1
    
        #pct for each rss url
        if number_of_articles==0:
            pct_of_images = 0
            pct_of_text = 0
        else:
           pct_of_images = number_of_images/float(number_of_articles) *100
           pct_of_text = number_of_text/float(number_of_articles)
        
        total_articles += number_of_articles
        total_images += number_of_images
        total_text += number_of_text
        
        feedurls.append({
                        "rssurl_id":each.id,
                        "url": url,
                        "valid": valid,
                        "newspaper": newspaper,
                        "category": category,
                        "number_of_articles": number_of_articles,
                        "number_of_images": number_of_images,
                        "number_of_text" : number_of_text,
                        "pct_of_images": round(pct_of_images,2),
                        "pct_of_text": round(pct_of_images,2)
                        })
    #calculate the total pct
    if total_articles==0:
        pct_total_images = 0
        pct_total_text = 0
        pct_articles = 0
    else:
        pct_total_images = total_images/float(total_articles) *100
        pct_total_text   = total_text/float(total_articles) *100
        pct_articles = total_articles/float(len(query)*10) * 100
    summary={
    "num_urls": num_urls,
        "valid_urls": valid_urls,
            "invalid_urls": invalid_urls,
                "pct_valid": round(pct_valid,2),
                    "total_articles": total_articles,
                        "pct_articles": round(pct_articles,2),
                            "total_images": total_images,
                                "pct_total_images": round(pct_total_images,2),
                                    "total_text": total_text,
                                        "pct_total_text": round(pct_total_text,2),
                                        }
    
    return render(template, {'summary': summary})


def index(request):
    
    template = 'dash_index.html'
    #initialize
    feedurls=[]
    total_articles = 0
    total_images = 0
    total_text = 0
    pct_of_images = 0
    pct_of_text = 0
    
    #get the array of rss url from RSSurl and number of valid and invalid rssurl
    query = RSSurl.objects.all().distinct()
    num_urls = len(query)
    valid_query = RSSurl.objects.filter(valid=True)
    valid_urls = len(valid_query)
    pct_valid = valid_urls/float(num_urls) *100
    invalid_urls = num_urls - valid_urls
    
    #loop through the arrary
    for each in query:
        url = each.rss_url.encode('UTF-8')
        valid = each.valid
        articlequery = Article.objects.filter(rssurl_id=each.id)
        #initialize
        number_of_articles = len(articlequery)
        number_of_images = 0
        number_of_text= 0
        pct_of_images = 0
        pct_of_text = 0
        newspaper = ""
        category = ""
        
        #get the artcles for this rss url
        for article in articlequery:
            newspaper = article.newspaper
            category = article.category
            image = Image.objects.filter(article_id=article.id)
            
            if image :
                # get the stat of image
               if image[0].image_url :
                  number_of_images += 1
               # get the stat of main_text
               if image[0].main_text :
                  number_of_text += 1
    
        #pct for each rss url
        if number_of_articles==0:
            pct_of_images = 0
            pct_of_text = 0
        else:
            pct_of_images = number_of_images/float(number_of_articles) *100
            pct_of_text = number_of_text/float(number_of_articles)
        
        total_articles += number_of_articles
        total_images += number_of_images
        total_text += number_of_text
        
        feedurls.append({
            "rssurl_id":each.id,
            "url": url,
            "valid": valid,
            "newspaper": newspaper,
            "category": category,
            "number_of_articles": number_of_articles,
            "number_of_images": number_of_images,
            "number_of_text" : number_of_text,
            "pct_of_images": round(pct_of_images,2),
            "pct_of_text": round(pct_of_images,2)
            })
    #calculate the total pct
    if total_articles==0:
       pct_total_images = 0
       pct_total_text = 0
       pct_articles = 0
    else:
       pct_total_images = total_images/float(total_articles) *100
       pct_total_text   = total_text/float(total_articles) *100
       pct_articles = total_articles/float(len(query)*10) * 100
    summary={
           "num_urls": num_urls,
           "valid_urls": valid_urls,
           "invalid_urls": invalid_urls,
           "pct_valid": round(pct_valid,2),
           "total_articles": total_articles,
           "pct_articles": round(pct_articles,2),
           "total_images": total_images,
           "pct_total_images": round(pct_total_images,2),
           "total_text": total_text,
           "pct_total_text": round(pct_total_text,2),
           }

    return render(request,template,{'feedurls':feedurls,'summary':summary})



'''dispaly the table for the stats of the artciles populated from this rssurl, to view if every data is valid or not '''
def rssurl(request,rssurl_id):

    template = 'rssfeed.html'
    articles = []
    rssurl = RSSurl.objects.filter(id=rssurl_id)[0].rss_url.encode('UTF-8')
    newspaper = ""
    category = ""
    #ge the array of articles from the rss url in Article
    rssquery = Article.objects.filter(rssurl_id=rssurl_id)
    
    for each in rssquery:
        newspaper = each.newspaper.encode('UTF-8')
        category = each.category.encode('UTF-8')
        title = each.title
        url = each.url
        publish_date = each.publish_date
        description = each.description

         #initialize
        image = ""
        text = ""
        # get the image or text for this article from Image
        image_text = Image.objects.filter(article_id=each.id)
        if image_text:
           image = image_text[0].image_url.encode('UTF-8')
           text = image_text[0].main_text.encode('UTF-8')
           if len(text) > 500:
               text = text[0:500]+"..."
        #append info to articles
        articles.append({
            "article_id": each.id,
            "title": title,
            "url": url,
            "publish_date": publish_date,
            "description": description,
            "image": image,
            "text": text,
         })

    return render(request,template,{'articles':articles,'rssurl':rssurl,'newspaper':newspaper,'category':category})


'''this will read info for all aritlces'''
def articles(request):
    
    template = 'articles.html'
    articles = []
    validrssurl = RSSurl.objects.filter(valid=True)
  
    for rss in validrssurl:
        
        feeds = Article.objects.filter(rssurl_id=rss.id)
        
        for each in feeds:
            # get data from artilces: newspapaer | category | title |url| publish_date |despcriton
            newspaper = each.newspaper.encode('UTF-8')
            category = each.category.encode('UTF-8')
            title = each.title
            articleurl = each.url
            publish_date = each.publish_date
            description = each.description
            if description > 100:
               description = description[0:100]+"..."
            # get data from Image:  Image | Text
            image = ""
            text = ""
            image_text = Image.objects.filter(article_id=each.id)
            if image_text:
               image = image_text[0].image_url.encode('UTF-8')
               text = image_text[0].main_text.encode('UTF-8')
               if len(text) > 300:
                   text = text[0:300]+"..."
        
             #append info to articles
            articles.append({
                         "newspaper": newspaper,
                         "category": category,
                         "title": title,
                         "article_url": articleurl,
                         "publish_date": publish_date,
                         "description": description,
                         "image": image,
                         "text": text,
                                    })

    return render(request,template,{'articles':articles})


'''download save all data to csv file'''
    
def downloadall(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="DataPopulationResults.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Number', 'RSS url', 'Valid','Newspaper', 'Category','Title','Article URL','Publish Date', 'Description','Image URL','Main Text'])
    rssurl = RSSurl.objects.all().distinct()
    number = 0
    for rss in rssurl:
        
        feeds = Article.objects.filter(rssurl_id=rss.id)
        
        for each in feeds:
            number += 1
            # get data from artilces: newspapaer | category | title |url| publish_date |despcriton
            newspaper = smart_str(each.newspaper)
            category = smart_str(each.category)
            title = smart_str(each.title)
            articleurl = smart_str(each.url)
            publish_date = smart_str(each.publish_date)
            description = smart_str(each.description)
            # get data from Image:  Image | Text
            image_url = ""
            clean_text = ""
            image_text = Image.objects.filter(article_id=each.id)
            if image_text:
                image_url = image_text[0].image_url
                clean_text = smart_str(image_text[0].main_text)

        writer.writerow([number, rss.rss_url,rss.valid,newspaper,category,title,articleurl,publish_date,description,image_url,clean_text])
    
    return response


'''view all images in database'''
def images(request):
    template = 'images.html'
    imagequery = Image.objects.all().distinct()
    return render(request,template,{'images':imagequery})




