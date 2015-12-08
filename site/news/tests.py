from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth.models import AnonymousUser, User

from news.views import index, filterfeeds, userfeeds, newspaper
from news.models import Article,Image

#news page
class NewsPageTest(TestCase):

    #checks that /news/ goes to index view
    def test_news_url_resolves_to_index_view(self):
        found = resolve('/news/')
        self.assertEqual(found.func, index)

    #checks that index view has the index html template
    def test_news_page_returns_correct_html(self):
        request = HttpRequest()
        request.user = AnonymousUser()
        response = index(request)
        expected_html = render_to_string('index.html')
        self.assertEqual(response.content.decode(), expected_html)

    #seems like I have to create the articles manually
    #every damn time
    def test_article_appears_on_news_page(self):
        article = Article.objects.create(newspaper="New York Times", title="Adele is back", url="www.flask.org", description="I don't know", category="Technology")

        response = self.client.get('/news/')
        self.assertContains(response, 'Technology')
        self.assertContains(response, 'New York Times')

    def test_Can_redirect_to_pipeline(self):
        response = self.client.get('/news/')
        self.assertContains(response, 'See pipeline')

#article model
class AritcleModeltest(TestCase):

    def test_saving_and_retrieving_articles(self):

        #article has title | url | description | newspaper | category
        article_1 = Article()
        article_1.newspaper = "Python Daily"
        article_1.category = "Programming"
        article_1.title = "Python in 10 minutes"
        article_1.url = "http://realpython.com"
        article_1.description = "Learn the Python programming language in 10 minutes"
        article_1.save()

        article_2 = Article()
        article_2.newspaper = "NYT"
        article_2.category = "Programming"
        article_2.title = "Kung Fu React"
        article_2.url = "http://flask.com"
        article_2.description = "Best tutorial to learning react on the web"
        article_2.save()

        saved_articles = Article.objects.all()
        self.assertEqual(saved_articles.count(), 2)

        self.assertEqual(article_1, Article.objects.all()[0])
        self.assertEqual(article_1.newspaper, 'Python Daily')
        self.assertEqual(article_1.category, 'Programming')
        self.assertEqual(article_1.title, 'Python in 10 minutes')
        self.assertEqual(article_1.url, "http://realpython.com")
        self.assertEqual(article_1.description, "Learn the Python programming language in 10 minutes")

        self.assertEqual(article_2, Article.objects.all()[1])
        self.assertEqual(article_2.newspaper, "NYT")
        self.assertEqual(article_2.category, "Programming")
        self.assertEqual(article_2.title, "Kung Fu React")
        self.assertEqual(article_2.url, "http://flask.com")
        self.assertEqual(article_2.description, "Best tutorial to learning react on the web")

class NewspaperViewTest(TestCase):

    #bad test because, the create of the article newspaper does
    #not directly affect the url creation, no relation
    def test_uses_newspaper_template(self):
        article = Article.objects.create()
        article.newspaper = "New York Times"
        response = self.client.get('/news/newspaper/nytimes/')
        self.assertTemplateUsed(response, 'newspaper.html')

    #can't populate pages for some reason
    def test_displays_article_from_that_newspaper(self):
        #create 2 aritcles from different newspaper
        #newspaper, title, url, description, category
        correct_article = Article.objects.create(newspaper="New York Times", title="Adele is back", url="www.flask.org", description="I don't know", category="Technology")

        response = self.client.get('/news/newspaper/nytimes/')
        
        self.assertContains(response, "New York Times")
        self.assertContains(response, "Technology")
        self.assertNotContains(response, "Los Angeles Times")
        self.assertNotContains(response, "Westside gang")


class FilterFeedsTest(TestCase):

    def test_uses_filterfeeds_template(self):
        response = self.client.get('/news/filterfeeds')
        self.assertTemplateUsed(response, 'filterfeeds.html')

    def test_displays_a_newspaper_block(self):
        an_article = Article.objects.create(newspaper="New York Times", title="Adele is back", url="www.flask.org", description="I don't know", category="Technology")
        response = self.client.get('/news/filterfeeds')
        
        self.assertContains(response, "New York Times")

    def test_displays_a_category(self):
        an_article = Article.objects.create(newspaper="New York Times", title="Adele is back", url="www.flask.org", description="I don't know", category="Technology")
        response = self.client.get('/news/filterfeeds')
        
        self.assertContains(response, "Technology")

#can't test for content
#that's an integration as it requires click selection of content
class UserFeedsTest(TestCase):
    
    def test_uses_userfeeds_template(self):
        response = self.client.get('/news/userfeeds')
        self.assertTemplateUsed(response, 'userfeeds.html')


class ArticleImagesTest(TestCase):

    def test_uses_images_template(self):
        #have to create article, as images belong to an article id
        an_article = Article.objects.create(newspaper="New York Times", title="Adele is back", url="www.flask.org", description="I don't know", category="Technology")

        response = self.client.get('/news/images/' + str(an_article.id))
        self.assertTemplateUsed(response, 'image_text.html')

    def test_has_article_attributes(self):

        an_article = Article.objects.create(newspaper="New York Times", title="Adele is back", url="www.flask.org", description="I don't know", category="Technology")

        response = self.client.get('/news/images/' + str(an_article.id))

        #test that newspaper, category and title display on page
        self.assertContains(response, an_article.newspaper)
        self.assertContains(response, an_article.category)
        self.assertContains(response, an_article.title)



'''Verify the main and test show on news/images/(article_id) page  if there is an image and main text extraced '''
class MainImageTest(TestCase):

    def test_image_text_tempalte(self):
        #create an article
        an_article = Article.objects.create(newspaper="New York Times", title="Adele is back", url="www.flask.org", description="I don't know", category="Fashion")

        image_text = Image.objects.create(article_id=an_article.id, image_url="http://helloworld.jpg", main_text="hello world")

        response = self.client.get('/news/images/'+str(an_article.id))

        '''test thte page'''
        self.assertContains(response, an_article.newspaper)
        self.assertContains(response, an_article.category)
        self.assertContains(response, an_article.title)
        
        image_url = Image.objects.filter(article_id=an_article.id)[0].image_url
        main_text = Image.objects.filter(article_id=an_article.id)[0].main_text
        self.assertContains(response, image_url)
        self.assertContains(response, main_text)








