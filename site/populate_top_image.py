# author: Jiang

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from news.models import Article
from news.models import Image
import re
import sys
from datetime import datetime

import warnings
warnings.filterwarnings("ignore")

from goose import Goose

def populate_top_image():
    
    total_create=0
    total_exist=0
    total_count=0
    
    #get the array of article
    Articlelinks=Article.objects.distinct()
    
    #change start and end here, to extra images for articles in a range
    for each in Articlelinks[start:end]:
        
        create_count=0
        exist_count=0
        total_create=0
        images_count=0
        
        #parse page using goose
        g = Goose()
        article = g.extract(url=each.url)
        if article.top_image is not None:

           top_image_url= article.top_image.src
           images_count=1
            #save in db     |article_id  | image_url |
           obj, created = Image.objects.get_or_create(
                    article_id=each.id,
                    image_url=top_image_url
             )
                    
           if created:
                create_count += 1
                total_create += 1
                sys.stdout.write('Image created: %s\n' % top_image_url)
           else:
                total_exist += 1
                exist_count += 1
                sys.stdout.write('Image exists!  %s\n' % top_image_url)

        sys.stdout.flush()
        
        total_create+=create_count
        total_exist+=exist_count
        total_count += images_count
        sys.stdout.write('\n+++++++++++++++++++++++++Populating Images Article %d :+++++++++++++++++++++++++\n' %each.id)
        #stat for each article
        if (images_count==0):
            sys.stdout.write('============Article Link:  %s\n' % each.url)
            sys.stdout.write('0 Images for this link | 0 (0.00 %) Created | 0 (0.00 %) Existed\n')
        else:
            create_pct = create_count * 100.0 / images_count
            exist_pct = exist_count * 100.0 / images_count
            sys.stdout.write('============Article Link:  %s\n' % each.url)
            sys.stdout.write(
                             '%d Images for this link | %d (%3.2f%%) Created | %d (%3.2f%%) Existed\n'
                             % (images_count, create_count, create_pct, exist_count, exist_pct))
            sys.stdout.flush()
                
                
                #stat in total
    if (total_count==0):
        sys.stdout.write('\nTotal Images: 0 | 0 (0.00 %) Created | 0 (0.00 %) Existed \n')
    else:
        total_create_pct = total_create * 100.0 / total_count
        total_exist_pct = total_exist * 100.0 / total_count
        sys.stdout.write('\nTotal Images: %d | %d (%3.2f%%) Created | %d (%3.2f%%) Existed \n'
                         %(total_count,total_create,total_create_pct,total_exist,total_exist_pct))
        sys.stdout.flush()


#execute here
if __name__ == '__main__':
    
    Articlelinks=Article.objects.distinct()
    num=len(Articlelinks)
    #specify the range
    print "Total number of articles is  %d." %num
    start=int(raw_input("Please enter the start index (range(0,%d))of articles to populate images:" %(num-1)))
    end=int(raw_input("Please enter the end index (range(%d,%d))of articles to populate images:"%(start,(num-1))))
    
    #start
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    print "Starting images population script..."
    begin=datetime.strptime(str(datetime.now()),date_format)
    
    populate_images()
    
    #end
    stop=datetime.strptime(str(datetime.now()),date_format)
    duration=stop-begin
    print "Total time of images population:  "+str(duration)
