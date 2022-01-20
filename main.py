#####################
# IMPORTING MODULES #
##################### 

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import hashlib
import re
import os

#Chrome driver settings for my mac

options = webdriver.ChromeOptions()
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
chrome_driver_binary = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chrome_driver_binary, chrome_options = options)


#Browser settings for windows:
#driver = webdriver.Chrome()


############################# SCRAPING BING TO MAKE A URL LIST #############################

with open('list.txt') as file:
    for line in file:

         #Number of Bing pages
         page = 1

         for i in range(page):
            counter = 0
            driver.get('https://www.bing.com/search?q=' + line.rstrip() + f'&first={i}1')
            links = driver.find_elements_by_xpath(f'//li[@class="b_algo"]/h2/a')
          
            for link in links:
                
             link = links[counter].get_attribute('href')
            
             #saving links in a txt file
             file = open('link.txt','a+',encoding='utf-8')
             if 'pdf' not in link and 'amazon' not in link and 'ebay' not in link and '.doc' not in link and 'pinterest' not in link and 'PDF' not in link and 'google' not in link:
              
              split_string = link.split("//",1)

              substring = split_string[1]

              split_string = substring.split("/",1)

              substring = split_string[0]

              file.write(substring + '\n')
             counter += 1

driver.close()


############################# REMOVE DUPLICATE LINES FROM FILE #############################


output_file_path = "link2.txt"
input_file_path = "link.txt"
completed_lines_hash = set()
output_file = open(output_file_path, "w")

for line in open(input_file_path, "r"):

  hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
  if hashValue not in completed_lines_hash:
    output_file.write(line)
    completed_lines_hash.add(hashValue)

output_file.close()
os.remove("link.txt") 



############################# SCRAPING DATA FROM WEBSITES #############################


templist = []
with open('link2.txt') as file:
    for line in file:
        try:
         html_doc = requests.get("https://" + line.rstrip(), verify=False, timeout = 5).text
        except:
            continue

        soup = BeautifulSoup(html_doc, 'html.parser')

        #Regex
        facebooks = re.findall(r'(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\W\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?',html_doc)
        twitters = re.findall(r'(?:(?:http|https):\/\/)?(?:www.)?twitter.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\W\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?',html_doc)
        instagrams = re.findall(r'(?:(?:http|https):\/\/)?(?:www.)?(?:instagram.com|instagr.am|instagr.com)\/(\w+)',html_doc)
        emails = re.findall(r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""",html_doc)

        
        facebooks = list(set(facebooks))
        facebook_address = ''
        for facebook in facebooks:
                if len(facebook) < 30 and facebook != 'tr' and facebook != 'share' and facebook!= 'sharer':
                 f = ('https://www.facebook.com/'+facebook)
                 facebook_address = f + ' , ' + facebook_address


        twitters = list(set(twitters))
        twitters_address = ''
        for twitter in twitters:
                if len(twitter) < 30 and twitter != 'tr' and twitter != 'share' and twitter!= 'sharer' and twitter != 'intent':
                 t = ('https://www.twitter.com/'+twitter)
                 twitters_address = t + ' , ' + twitters_address

        instagram_address = ''
        instagrams = list(set(instagrams))
        for instagram in instagrams:
                if len(instagram) < 30:
                 i = ('https://www.instagram.com/'+instagram)
                 instagram_address = i + ' , ' + instagram_address

        email_address = ''
        emails = list(set(emails))
        for email in emails:
                if '//' not in email and 'jpg' not in email and '{' not in email and  len(email) < 30:
                 email_address = email + ' , ' + email_address


        linkedin_list = []
        linkedin_address = []
        linkedins = soup.findAll('a',href=True)
        for linkedin in linkedins:
            if 'linkedin' in linkedin['href'] and 'share' not in linkedin['href']:
                linkedin_list.append(linkedin['href'])
            linkedin = list(set(linkedin_list))
            linkedins = ' , '
            linkedin_address = linkedins.join(linkedin)

        
        phone_list = []
        phone_number = []
        phone_numbers = soup.findAll('a',href=True)
        for phone_number in phone_numbers:
            if 'tel:' in phone_number['href'] and len(phone_number['href']) < 20:
                phone_list.append(phone_number['href'])
            phone = list(set(phone_list))
            phones = ' , '
            phone_number = phones.join(phone)


############################# MAKE DICTIONARY FROM DATA #############################


        Table_dict={ 
    
        "Website url" : line,
        "Facebook" : facebook_address,
        "Twitter" : twitters_address,
        "Instagram" : instagram_address,
        "Linkedin" : linkedin_address,
        "Phone number" :  phone_number,
        "Email" : email_address
        }

############################# MAKE DATAFRAME FROM DICTIONARY #############################

        templist.append(Table_dict) 
        df = pd.DataFrame(templist)

        

############################# REMOVE MISSING VALUES AND SAVE DATA AS CSV FILE  #############################

os.remove("link2.txt") 
df.to_csv('result.csv',index=False) 
df = pd.read_csv("result.csv")
df = df.dropna(thresh=3)
df = df.reset_index(drop=True)
df.to_csv('result.csv')
