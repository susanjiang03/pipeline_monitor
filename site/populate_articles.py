import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from news.models import Newspaper, Category, Article 

def populate():
    #try adding one of each
    nytimes = add_newspaper('New York Times')
    tech = add_category('technology')
    
    blah = add_article(news=nytimes,
        cat=tech,
        title="test title",
        url="http://www.google.com",
        desc="what is going on??")

    for a in Article.objects.all():
        print a


def add_newspaper(name):
    news = Newspaper.objects.get_or_create(name=name)[0]
    news.save()
    return news

def add_category(name):
    category = Category.objects.get_or_create(name=name)[0]
    category.save()
    return category

def add_article(news, cat, title, url, desc):
    article = Article.objects.get_or_create(newspaper=news, category=cat, title=title, url=url, description=desc)[0]
    article.save()
    return article


#execute here
if __name__ == '__main__':
    print "Starting article population script..."
    populate()
