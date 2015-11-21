from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from news.views import index, filterfeeds, userfeeds, newspaper
from news.models import Article

#what to test on the home page?

class MainPageTest(TestCase):

    def test_main_page_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        expected_html = render_to_string('index.html')
        #this doesn't test anything atm

    #test that we have the 6 newspaper categories
    def test_main_page_has_six_categories(self):
        categories = ['World', 'Local', 'Technology', 'Business', 'Sports', 'Fashion']
        expected_html = render_to_string('index.html').encode('utf-8')

        #currently fails because it checks the template, not the populated page

class AritcleModeltest(TestCase):

    def test_saving_and_retrieving_articles(self):

        #article has title | url | description | newspaper | category
        article_1 = Article()
        article_1.newspaper = "Python Daily"
        article_1.category = "Programming"
        article_1.title = "Python in 10 minutes"
        article_1.url = "http://realpython.com"
        article_1.description = "Learn the Python programming language in 10 minutes"
        #gotta know the format before testing date
        article_1.save()

        #test 5 fields
        self.assertEqual(article_1, Article.objects.all()[0])
        self.assertEqual(article_1.newspaper, 'Python Daily')
        self.assertEqual(article_1.category, 'Programming')
        self.assertEqual(article_1.title, 'Python in 10 minutes')
        self.assertEqual(article_1.url, "http://realpython.com")
        self.assertEqual(article_1.description, "Learn the Python programming language in 10 minutes")

    def create_article(self, blah='hello, I like water'):
        return Article.objects.create(title=blah, url=blah, description=blah, 
                                      category=blah, newspaper=blah)

    def test_article_creation(self):
        a = self.create_article()
        self.assertTrue(isinstance(a, Article))
 
        self.assertEqual(a.__unicode__(), a.title)








