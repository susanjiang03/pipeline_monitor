'''
Use os module to give terminal output
'''
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from news.models import RSSurl,Article
import feedparser
import re
import sys
from datetime import datetime

import warnings
warnings.filterwarnings("ignore")

def populate():
    max_disp_len = 50
    #open file containing rss links
    #prompt whether you want to open all urls or only test ones
    #prompt with 0 or 1
    
    
    #find a way to differentiate the newspaper and category
    #two if checks

    #create dictionary here to match the patterns
    newspapers = {'nytimes': 'New York Times', 'latimes': 'Los Angeles Times', 'miamiherald': 'Miami Herald', 'seattletimes':'Seattle Times', 'denverpost':'Denver Post'}

    #only need a simple list here
    categories = ['world', 'business', 'technology', 'fashion', 'sports']


    #insert list of keywords that belong to a category
    urls=RSSurl.objects.filter(valid=True).distinct();
    for each in urls:
        url=each.rss_url.encode('utf-8')
        #now we have feeds
        rss = feedparser.parse(url)

        #match up the newspaper title
        for key in newspapers:
            if key in each.rss_url:
                newspaper = newspapers[key]

        #this loop creates all the articles and populates them in the db
        create_count = 0
        exist_count = 0

        #trim down entries, grab only first 10
        for post in rss.entries[:10]:
            #newspaper | category | title | url | description
            title = post.title.encode('utf-8')
            link = post.link

            #it doesn't always have a descr so...
            descr = ''
            clean_descr = ''
            try:
                #descr comes out cluttered with html crap
                descr = post.description.encode('utf-8')
                #clean it with regex
                clean_descr = re.sub(r'<[^>]*>', '', descr)
            except:
                pass

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
                sys.stderr.write(str(ve) + '\n')
                sys.stderr.flush()

            created = Article.objects.get_or_create(
                rssurl_id = each.id,
                newspaper = newspaper,
                category = category,
                title = title,
                url = link,
                description = clean_descr,
                publish_date = publish_date
            )

            if created:
                create_count += 1
                sys.stdout.write('Article created: %s\n' % clean_descr[:max_disp_len])
            else:
                exist_count += 1
                sys.stdout.write('Article exists!  %s\n' % clean_descr[:max_disp_len])
            sys.stdout.flush()

        total_count = len(rss.entries)
        if not total_count:
            total_count = 1
        create_pct = create_count * 100.0 / total_count
        exist_pct = exist_count * 100.0 / total_count
        sys.stdout.write('-- %s | %s  ---------------------------------------\n' % (newspaper, url))
        sys.stdout.write(
            '%d Total Feeds | %d (%3.2f%%) Created | %d (%3.2f%%) Existed\n'
            % (len(rss.entries), create_count, create_pct, exist_count, exist_pct)
        )
        sys.stdout.flush()


#execute here
if __name__ == '__main__':
    print "Starting article population script..."
    populate()

