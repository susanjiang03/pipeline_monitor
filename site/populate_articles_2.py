'''
Use os module to give terminal output
'''
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from news.models import RSSurl,Article
from pmonitor.models import Task, Status
import feedparser
import re
import sys
from datetime import datetime

import warnings
warnings.filterwarnings("ignore")

def initialize_tasks():
    Task.objects.all().delete()
    tasks = [
        dict(
            task_id='01',
            name='File Check',
            description='Loads the file containing urls.',
            status=Status.NOT_RUN
        ),
        dict(
            task_id='02',
            name='URL Retrieval',
            description='Retrieves urls.',
            status=Status.NOT_RUN
        )
    ]
    
    prev_task = None
    for task_meta in tasks:
        task = Task.objects.create(**task_meta)
        if tasks.index(task_meta) > 0:
            task.parent = prev_task
            task.save()
        prev_task = task

def populate():
    initialize_tasks()
    max_disp_len = 50
    #open file containing rss links
    #prompt whether you want to open all urls or only test ones
    #prompt with 0 or 1
    
    file_to_open = "testurls.txt"
    task1 = Task.objects.get(task_id='01')
    task1.status = Status.IN_PROGRESS
    task1.message = "Checking if {} can be accessed".format(file_to_open)
    task1.save()
    with open("logs.txt", "a") as text_file:
        text_file.write("Task1: {} Message: {} on {}\n".format(task1.status, task1.message, task1.last_run))
    try:
        with open(file_to_open) as f:
            task1.status = Status.SUCCESS
            task1.message = "File opened"
            task1.save()
            with open("logs.txt", "a") as text_file:
                text_file.write("Task1: {} Message: {} on {}\n".format(task1.status, task1.message, task1.last_run))

            task2 = Task.objects.get(task_id='02')
            task2.status = Status.IN_PROGRESS
            task2.message = "Checking validity of Feeds in {}".format(file_to_open)
            task2.save()
            with open("logs.txt", "a") as text_file:
                text_file.write("Task2: {} Message: {} on {}\n".format(task2.status, task2.message, task2.last_run))

            linenumber = 0
            lineerror = []
            urls = f.readlines()
            for url in urls:
                linenumber += 1
                rss = feedparser.parse(url)
                if rss.bozo == 0:
                    pass
                else:
                    if 'Xml' in url:
                        pass
                    else:
                        lineerror.append(linenumber)

            if not lineerror:
                task2.message = "All Feeds are valid"
                task2.status = Status.SUCCESS
            else:
                task2.message = "Feeds on linenumbers {} are invalid".format(lineerror)
                task2.status = Status.WARNING
            task2.save()
            with open("logs.txt", "a") as text_file:
                text_file.write("Task2: {} Message: {} on {}\n".format(task2.status, task2.message, task2.last_run))

    except IOError as e:
        task1.status = Status.ERROR
        task1.message = e
        task1.save()
        with open("logs.txt", "a") as text_file:
            text_file.write("Task1: {} Message: {} on {}\n".format(task1.status, task1.message, task1.last_run))
        return 0

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

