from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

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
    '''

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

    #he sees a plethora of articles each of different category, he clicks on a the first link in the Local category and is directed to the chose article

    
    

    #user story #2 - user clicks the 'see images' link and goes to a page with article relevant images


    #user story #3 - user goes to news paper page
    #can repeat the same test for sincle article click


    #user story #4 - user goes to the all images tab and see images


    #user story #5 - user provided url feed





