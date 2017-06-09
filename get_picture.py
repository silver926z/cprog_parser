# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import urllib,urllib2
import boto3
official = "http://www.niotv.com/"
tmp = "epg_content.php?epg_no=5683945&content_id=&ch_id=56&epg_name=進擊的巨人&stype=name"
def get_picture(URL):
    print URL
    request = urllib2.Request(URL) 
    response = urllib2.urlopen(request)
    html = response.read()
    soup = BeautifulSoup(html,'html.parser')
    tmp = soup.find_all('div',{'class','pictbox'})
    tmp = tmp[0].find_all('td')[0].find_all('a')[0]['href']
    print "=======\n",tmp,"\n========="


if __name__ =='__main__':
    get_picture(official+tmp)
    