# Pipeline Monitor (pmonitor)
### A Django Site to Monitor Processes

## Purpose
This application will monitor arbitrary processes and display 
visualizations of the process state. 

## How to use
* Clone repository
* Create database tables with 'python manage.py migrations'
* At this point you can run the site with 'python manage.py runserver', but it is empty
* Now you need to run the necessary scripts
* First run 'python populate_rssurls.py', this populates the urls into the DB and the tasks
* After this you can start the Tornado server, open up a new terminal, go to the tndo/ directory and run 'python server.py'
* Check out the the pipeline site, the tasks should have been initiated
* Next you can populate the articles through the button on the dropdown on the top right
* This should be pretty fast, you will notice that only	the third task still hasn't run
* Run 'python populate_image_text.py', this will take a minute or so
* Check the dashboard as you populate things, you'll see the changes there 
* TODO, create button for 'populate_image_text.py'

## Version Info
Version: 0.01

Date: 10/26/2015

## Authors
 * Daniel Chia
 * Eddie Chan
 * James Hohman
 * Susan Jiang


## Requirements
 * Python 2.7.10
 * Django 1.8.5


## License, Copyright
License should go here.

## Main packages
| path | description |
-------|--------------
| site/ | contains the django site. |
| simulator/ | contains a simple process that can be monitored. |
 

