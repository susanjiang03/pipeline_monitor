from django.shortcuts import render
from django.contrib import admin
from django.db import models
from news.models import Article, Image, RSSurl

# Create your views here.

'''index page of dashboard app'''
def index(request):
    
    template = 'dash_index.html'
    
    query = RSSurl.objects.all().distinct()
    num_urls = len(query)
    valid_urls = len(RSSurl.objects.filter(valid=True))
    pct_valid = valid_urls/float(num_urls) *100
    invalid_urls = num_urls - valid_urls
    feedurls=[]
    
    total_articles = 0
    total_images = 0
    total_text = 0
    pct_of_images = 0
    pct_of_text = 0
    
    for each in query:
        url = each.rss_url.encode('UTF-8')
        valid = each.valid
        articlequery = Article.objects.filter(rssurl_id=each.id)
        
        number_of_articles = len(articlequery)
        number_of_images = 0
        number_of_text= 0
        pct_of_images = 0
        pct_of_text = 0
        
        for article in articlequery:
            image = Image.objects.filter(article_id=article.id)
            
            if image :
               if image[0].image_url :
                  number_of_images += 1
               
               if image[0].main_text :
                  number_of_text += 1
    
        pct_of_images = number_of_images/float(number_of_articles) *100
        pct_of_text = number_of_text/float(number_of_articles)
        
        total_articles += number_of_articles
        total_images += number_of_images
        total_text += number_of_text
        
        feedurls.append({
            "url": url,
            "valid": valid,
            "number_of_articles": number_of_articles,
            "number_of_images": number_of_images,
            "number_of_text" : number_of_text,
            "pct_of_images": round(pct_of_images,2),
            "pct_of_text": round(pct_of_images,2)
            })
        
    pct_total_images = total_images/float(total_articles) *100
    pct_total_text   = total_text/float(total_articles) *100
    
    summary={
           "num_urls": num_urls,
           "valid_urls": valid_urls,
           "invalid_urls": invalid_urls,
           "pct_valid": round(pct_valid,2),
           "total_articles": total_articles,
           "total_images": total_images,
           "pct_total_images": round(pct_total_images,2),
           "total_text": total_text,
           "pct_total_text": round(pct_total_text,2),
           }

    
    return render(request,template,{'feedurls':feedurls,'summary':summary})













