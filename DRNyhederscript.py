
# Script that scrapes news items from DR Nyheder. 
# The script is split into two sections: 
# i) First the title of each news item is scraped using the BeautifulSoup package
# ii) Then the text associated to each news item is scraped by searching for the parent div section, where the Title occurs. 

##################################################################
import requests
from urllib.robotparser import RobotFileParser

# First we check whether we are allowed to scrape the data. 
url = "https://www.dr.dk/nyheder"
rp = RobotFileParser()
rp.set_url(url)
rp.read()
can_scrape = rp.can_fetch('*',url)
print(can_scrape)

##################################################################
if can_scrape:
 # Get request for loading the html code
 response = requests.get(url)
 html = response.text


 # Parsing the html
 #i) Extracting the title for each news item on the page
 from bs4 import BeautifulSoup 
 soup = BeautifulSoup(html,'html.parser')

 headings = soup.find_all("div", class_ = "hydra-latest-news-page-short-news-article__top")
 titles=[]
 for heading in headings:
     title = heading.find("span",class_="dre-title-text")
     titles.append(title.text)



 # ii) Filtering on the div section of html code, which corresponds to a specific news item and then extracting the text
    
 alle_nyheder = []

 for title in titles:

   body = soup.find("article",class_="hydra-latest-news-page-short-news-article",attrs={'aria-label': title})
   body = body.find_parent('div')

   body = body.find_all("div", class_ = "dre-speech")

   bodies=[]
   for b in body:
       text = b.text
       bodies.append(text)

   alle_nyheder.append(bodies)



 from winotify import Notification, audio
 import os 
 cwd = os.getcwd()
 icon_path = os.path.join(cwd, "DRlogo.png")

 for topic in alle_nyheder:
     title = topic[0]
     bodies = topic[1:] 

     # Join the paragraphs into a single string
     body = '\n'.join(bodies)

     # Display the toast notification
     notification = Notification(app_id = " ",title=title, msg=body, icon = icon_path)
    
     notification.add_actions(label="Læs videre her", launch="https://www.dr.dk/nyheder")
     notification.set_audio(audio.Mail, loop=False)
     notification.show()

else:
   pass 