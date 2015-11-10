import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from news.models import Article 
import feedparser
import re
import sys
from datetime import datetime

#Todo, update this script so that it populates the articles based on an RSS feed

def populate():
    
    #open file containing rss links
    with open('rssurls.txt') as f:
        urls = f.readlines()

    #find a way to differentiate the newspaper and category
    #two if checks

    #create dictionary here to match the patterns
    newspapers = {'nytimes': 'New York Times', 'latimes': 'Los Angeles Times', 'miamiherald': 'Miami Herald', 'seattletimes':'Seattle Times', 'chron':'Houston Chronicles', 'denverpost':'Denver Post'}

    #only need a simple list here
    categories = ['world', 'business', 'technology', 'fashion', 'sports']


    #insert list of keywords that belong to a category
    for url in urls:

        #now we have feeds
        rss = feedparser.parse(url) 

        #match up the newspaper title
        for key in newspapers:
            if key in url:
                newspaper = newspapers[key] 

        #this loop creates all the articles and populates them in the db
        for post in rss.entries:
            #newspaper | category | title | url | description
            title = post.title.encode('utf-8')
            link = post.link

            #descr comes out cluttered with html crap
            descr = post.description.encode('utf-8')
            #clean it with regex
            clean_descr = re.sub(r'<[^>]*>', '', descr) 

            #match up the newspaper title
            for key in newspapers:
                if key in url:
                    newspaper = newspapers[key] 


            #find the category
            category = ''
            for cat in categories:
                #found category
                #this logic sucks, at the end it doesnt match so it ends up putting local
                if cat in url.lower():
                    category = cat.capitalize()

            #if category was not found, its local
            if category.lower() not in categories:
                category = 'Local'

            # u'Tue, 10 Nov 2015 19:35:48 GMT'
            try:
                publish_date = datetime.strptime(post.published, '%a, %d %b %Y %H:%M:%S %Z')
            except ValueError as ve:
                publish_date = datetime.now()
                sys.stderr.write(ve + '\n')
                sys.stderr.flush()

            Article.objects.get_or_create(
                newspaper=newspaper,
                category=category,
                title=title, 
                url=link, 
                description=clean_descr,
                publish_date=publish_date
            )[0]

#             add_article(newspaper, category, title, link, clean_descr)


#add article, pass newspaper, category, title, url, description
# def add_article(news, cat, title, url, desc):
#     #the 3 main fields are the only unique ones
#     article = Article.objects.get_or_create(title=title, url=url, description=desc)[0]
#     article.newspaper = news
#     article.category = cat
#     article.save()
#     return article


#execute here
if __name__ == '__main__':
    print "Starting article population script..."
    populate()

