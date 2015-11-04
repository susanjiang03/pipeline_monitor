'''
This script looks through rssurls.txt, get the rss feed links
then it loops through each rss feed link and stores contents in a
database. Current content is title, link and description
'''

import feedparser

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
    descr = post.description.encode('utf-8')
    
    #write to respective files
    titles.write(title + '\n\n')
    links.write(link + '\n\n')
    descriptions.write(descr + '\n\n')

titles.close()
links.close()
descriptions.close()

