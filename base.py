import sys
import time
import tweepy
import urllib2
import requests
from slacker import Slacker
from bs4 import BeautifulSoup

# custom coded libraries
from classes.logger import logger
log = logger().log

# if you plan on using this script, please dont delete the below line

consumer_key = "Consumer API Key"
consumer_secret = "Consumer Secret API Key"
access_token = "Access Token API Key"
access_token_secret = "Access Token Secret API Key"

#Setting up tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

try:
    request = requests.get('http://www.adidas.com/us/men-shoes?sz=120&start=0', headers={'User-Agent' : "Magic Browser"})
    log("Page Loaded", "success")
except:
    log("Error, page was not able to be loaded!", "error")
    sys.exit()

request_content = BeautifulSoup(request.content, "html.parser")

all = request_content.find_all('div',{"class":"image plp-image-bg"})
links =[]
i = 0

for products in all:
    links.append(products.find('a')['href'])

log(str(len(links)) + " links were found!")

for link in links:
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'Accept': 'text/html, application/xhtml+xml, application/xml',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,da;q=0.6',
        'DNT': '1'
    })
    response = session.get(link)
    response_content = BeautifulSoup(response.content, "html.parser")
    captcha = response_content.find_all('div',{"class":"g-recaptcha"})
    i += 1
    if captcha:
        log(str(i) + "/" + str(len(links)) + ' Captcha has been found @ ' + link + ' !', "success")
        log("Current Sitekey: " + captcha[0]['data-sitekey'])
        api.update_status("Current Sitekey: " + captcha[0]['data-sitekey'])
        break

    else:
        log(str(i) + "/" + str(len(links)) + ' Captcha has not been found on product @ ' + link + " !", "yellow")
        continue
