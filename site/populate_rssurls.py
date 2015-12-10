'''
Use os module to give terminal output
'''
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from news.models import RSSurl
import feedparser
import re
import sys
from datetime import datetime

import warnings
warnings.filterwarnings("ignore")

def populate_rssurls():
   
    #open file containing rss links
    #prompt whether you want to open all urls or only test ones
    #prompt with 0 or 1
    urls_to_open = raw_input("Choose 0 for 5 urls, 1 for all urls\n")

    #check here
    if urls_to_open == '0':
        file_to_open = 'testurls.txt'
    else:
        file_to_open = 'rssurls.txt'

    print file_to_open

    #set urls to small or large batch
    with open(file_to_open) as f:
        urls = f.readlines()

    create_count = 0
    exist_count = 0
    valid_count = 0
    invalid_count = 0

    #insert list of keywords that belong to a category
    for url in urls:
        
        #this loop creates all the rssurls and populates them in the db
    
        rss = feedparser.parse(url)
    
        if len(rss.entries) > 0:
            valid = True
            valid_count += 1
        else:
            valid = False
            invalid_count += 1

        created = RSSurl.objects.get_or_create(
                 rss_url = url,
                 valid = valid
           )

        if created:
            create_count += 1
            sys.stdout.write('\nRSS url created: %s' % url)
            sys.stdout.write('Valid RSS url: %s\n' % valid)
        else:
            exist_count += 1
            sys.stdout.write('\nRSS url exists!  %s' % url)
            sys.stdout.write('Valid RSS url: %s\n' % valid)
        sys.stdout.flush()

    total_count = len(urls)
    if not total_count:
        total_count = 1
                
    create_pct = create_count * 100.0 / total_count
    exist_pct = exist_count * 100.0 / total_count
    valid_pct = valid_count * 100.0 / total_count
    invalid_pct = invalid_count * 100.0 /total_count
    sys.stdout.write('-----%s  -----------------------------\n' % url)
    sys.stdout.write(
        '%d Total RSS url: | %d (%3.2f%%) Created | %d (%3.2f%%) Existed\n'
        % (len(urls), create_count, create_pct, exist_count, exist_pct)
    )
    sys.stdout.write(
                 '%d Total RSS url: | %d (%3.2f%%) Valid | %d (%3.2f%%) Invalid\n'
                 % (len(urls), valid_count, valid_pct, invalid_count, invalid_pct)
                 )
    sys.stdout.flush()


#execute here
if __name__ == '__main__':
    print "Starting RSS url population script..."
    populate_rssurls()

