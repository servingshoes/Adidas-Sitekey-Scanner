import sys
import time
import tweepy
import urllib2
import requests
from slacker import Slacker
from bs4 import BeautifulSoup

consumer_key = "Consumer API Key"
consumer_secret = "Consumer Secret API Key"
access_token = "Access Token API Key"
access_token_secret = "Access Token Secret API Key"

#Setting up tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

print('Please enter the amount of pages to scrape!')
page_amount = input('> ')
page_amount = page_amount - 1
page_amount = page_amount*120
i = 0

while i <= page_amount:
    try:
        request = requests.get('http://www.adidas.co.uk/men-shoes?sz=120&start=' + str(i), headers={'User-Agent' : "Magic Browser"})
        print("\033[92mPage Loaded\033[00m")
    except:
        print("\033[91mError, page was not able to be loaded!\033[00m")
        sys.exit()

    request_content = BeautifulSoup(request.content, "html.parser")

    all = request_content.find_all('div',{"class":"image plp-image-bg"})
    links =[]

    for products in all:
        links.append(products.find('a')['href'])

    print('\033[96m' + str(len(links)) + " links were found!\033[00m")

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
            print('\033[92m' + str(i) + "/" + str(len(links)) + ' Captcha has been found @ ' + link + ' !\033[00m')
            print("\033[92mCurrent Sitekey: " + captcha[0]['data-sitekey'] + '\033[00m')
            api.update_status("Current Sitekey: " + captcha[0]['data-sitekey'])
            sys.exit()
            break

        else:
            print('\033[93m' + str(i) + "/" + str(len(links)) + ' Captcha has not been found on product @ ' + link + " !\033[00m")
            continue

    i + 120
