
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
   # Extracting header and paragraph items
   header_item = nyhed.find("span",class_="dre-title-text").text #Extract header subitem
   para_items = nyhed.find_all('p') #Extract paragrahh subitems
  # Extracting hyperlink for the specific article. If there is none (e.g. Kort Nyt, set to a default value of '')
   hyper_ref_item = nyhed.find("a",class_="hydra-latest-news-page-short-news-card__link")
   if hyper_ref_item is not None:
         full_hyper_ref = 'https://www.dr.dk' + hyper_ref_item['href']
   else: 
      full_hyper_ref = ''
  # Collecting the strings corresponding to a new item in a list 
   collect = []
   collect.append(full_hyper_ref)
   collect.append(header_item)
   for item in para_items:
     p = item.text
     collect.append(p)

   alle_nyheder.append(collect)

 print(alle_nyheder[0])

############### Create notifications #######################

 from winotify import Notification, audio
 import os 
 cwd = os.getcwd()
 icon_path = os.path.join(cwd, "DRlogo.png")

 for topic in alle_nyheder:
     if topic[0] != '':
      href = topic[0] 
     else: 
      href = "https://www.dr.dk/nyheder"
     title = topic[1]
     bodies = topic[2:]
  
     bodies = [str(body) for body in bodies]
     # Join the body paragraphs into a single string
     cleaned_string = '\n\n'.join(bodies)

     # Display the toast notification
     notification = Notification(app_id = "Kort Nyt",title=title, msg=cleaned_string, icon = icon_path)
     if href != "https://www.dr.dk/nyheder":
      notification.add_actions(label="Læs videre her", launch=href)
     notification.set_audio(audio.Mail, loop=False)
     notification.show()

else:
    pass 


