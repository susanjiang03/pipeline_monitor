'''
This script looks through rssurls.txt, get the rss feed links
then it loops through each rss feed link and stores contents in a
database. Current content is title, link and description
TODO, download rss feeds instead?
for error handling, if the link is bad, feed.bozo = 1
'''

import feedparser
import re

#provide loop to store url links in a list

#need to pass link as an argument
rss = feedparser.parse('http://rss.nytimes.com/services/xml/rss/nyt/Education.xml')

#write the titles in a file
titles = open('titles.txt', 'w')
links = open('links.txt', 'w')
descriptions = open('desc.txt', 'w')

for post in rss.entries:
    title = post.title.encode('utf-8')
    link = post.link
    #descr comes out cluttered with html crap
    descr = post.description.encode('utf-8')

    #clean it with regex
    clean_descr = re.sub(r'<[^>]*>', '', descr) 

    #write to respective files
    titles.write(title + '\n\n')
    links.write(link + '\n\n')
    descriptions.write(clean_descr + '\n\n')

titles.close()
links.close()
descriptions.close()

#create list for urls
'''
with open('rssurls.txt') as f:
    urls = f.readlines()
'''
#urls in order, Business, Tech, Sports, Environment, US
#check whether the links are good or not
#need to parse through the 3 main items 











