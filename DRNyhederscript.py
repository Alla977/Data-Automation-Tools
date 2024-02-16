
# Script that scrapes news items from DR Nyheder. 
# The script is split into two sections: 
# i) First the title of each news item is scraped using the BeautifulSoup package
# ii) Then the text associated to each news item is scraped by searching for the parent div section, where the Title occurs. 

######################### Check permission to scrape #########################################
import requests
from urllib.robotparser import RobotFileParser

# First we check whether we are allowed to scrape the data. 
url = "https://www.dr.dk/nyheder"
rp = RobotFileParser()
rp.set_url(url)
rp.read()
can_scrape = rp.can_fetch('*',url)


if can_scrape:
 # Get request for loading the html code
 response = requests.get(url)
 html = response.text
 # Parsing the html using BeautifulSoup package
 from bs4 import BeautifulSoup 
 soup = BeautifulSoup(html,'html.parser')

#################### Extract header and body for all news types #####################

# Extract all news items 
 all_news_items = soup.find_all("li", class_ = "hydra-latest-news-page__short-news-item")
 len(all_news_items)

 alle_nyheder = []
 for nyhed in all_news_items:

   header_item = nyhed.find("span",class_="dre-title-text").text #Extract header subitem
   para_items = nyhed.find_all('p') #Extract paragrahh subitems
   collect = []
   collect.append(header_item)
   for item in para_items:
     p = item.text
     collect.append(p)

   alle_nyheder.append(collect)

 len(alle_nyheder)

############### Create notifications #######################

 from winotify import Notification, audio
 import os 
 cwd = os.getcwd()
 icon_path = os.path.join(cwd, "DRlogo.png")


 for topic in alle_nyheder:
     title = topic[0]
     bodies = topic[1:]
  
     bodies = [str(body) for body in bodies]
     # Join the body paragraphs into a single string
     cleaned_string = '\n\n'.join(bodies)
  


     # Display the toast notification
     notification = Notification(app_id = "Kort Nyt",title=title, msg=cleaned_string, icon = icon_path)
    
     notification.add_actions(label="Læs videre her", launch="https://www.dr.dk/nyheder")
     notification.set_audio(audio.Mail, loop=False)
     notification.show()

else:
    pass 


