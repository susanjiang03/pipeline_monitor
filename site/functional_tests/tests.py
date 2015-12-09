from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from news.models import Article 
import unittest
import time #sleep for timed delays

#User Story
class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        #waits for site to load before checking things
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    '''
    def test_title_is_news_aggregator(self):
        self.browser.get(self.live_server_url + '/news/')
        self.assertEqual('News Aggregator | Main', self.browser.title)
        
    #user story #1 - following the link
    #Timothy has been recently informed that there is a pipeline monitor web app and that he should check it out
    #he goes to the home page and it says 'Pipeline Monitor'
    def test_title_is_pipeline_monitor(self):
        self.browser.get(self.live_server_url + '/pipeline/')
        self.assertEqual('Pipeline Monitor | Main', self.browser.title)

    #news app can go see the pipeline
    def test_pipeline_app_link(self):
        self.browser.get(self.live_server_url + '/news/')
        link = self.browser.find_element_by_link_text('See pipeline')
        #click on it
        link.send_keys(Keys.RETURN)

        pipe_url = self.live_server_url + '/pipeline/' 
        self.assertEqual(pipe_url, self.browser.current_url)
        self.assertEqual('Pipeline Monitor | Main', self.browser.title)

    #he then asks himself, what exactly is the the pipeline monitoring?
    #he sees a link that directs him to the news aggregator app that this pipeline monitors
    #the news homepage is titled 'News Aggregator' 
    def test_news_app_link(self):
        self.browser.get(self.live_server_url + '/pipeline/')     
        link = self.browser.find_element_by_id("newsApp")
        #can click on the link, cool
        link.send_keys(Keys.RETURN)

        news_url = self.live_server_url + '/news/' 
        self.assertEqual(news_url, self.browser.current_url)
        self.assertEqual('News Aggregator | Main', self.browser.title)

    #he sees an article, he clicks on it 
    def test_following_article_link_correctly(self):
        #use a nyt article cuz, miami herald is giving me ads
        an_article = Article.objects.create(newspaper="New York Times", title="China hacking data of us workers a crime, not a state act", url="http://www.nytimes.com/2015/12/03/world/asia/china-hacking-us-opm.html?partner=rss&emc=rss", description="China won't take responsibility for what they did", category="World")
    
        self.browser.get(self.live_server_url + '/news/')
        article_link = self.browser.find_element_by_link_text('China hacking data of us workers a crime, not a state act')
        article_link.send_keys(Keys.RETURN)
        
        # print self.browser.current_url
        self.assertIn("nytimes", self.browser.current_url.encode('utf-8'))
        self.assertIn(an_article.category.lower(), self.browser.current_url)

    
    '''

    #user story #2 - user clicks the 'see images' link and goes to a page with article relevant images


    #user story #3 - user goes to news paper page
    #can repeat the same test for sincle article click


    #user story #4 - user goes to the all images tab and see images


    #user story #5 - user provided url feed
    #test for both correct and incorrect input
    #don't use contain, use assertIn
    def test_bad_user_provided_url(self):
        #go to that tab
        filter_url = self.live_server_url + '/news/filterfeeds'
        self.browser.get(filter_url)

        #find input box, throw a url at it, follow one of the links and check that the response has the newspaper title
        inputbox = self.browser.find_element_by_id('userRSS')
        inputbox.send_keys('hello')

        # time.sleep(3)

        filterbutton = self.browser.find_element_by_id('filter_button') 
        filterbutton.send_keys(Keys.RETURN)

        #test url
        filtered_url = self.live_server_url + '/news/userfeeds'
        self.assertEqual(filtered_url, self.browser.current_url)

        invalid_msg = self.browser.find_element_by_tag_name('ol')

        self.assertIn("Invalid rss url", invalid_msg.text.encode('utf-8'))
        # self.assertContains(self.browser.page_source.encode('utf-8'), "Invalid rss url")

        time.sleep(3)




