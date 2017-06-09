
import requests
from bs4 import BeautifulSoup
import lxml
 
url = "http://www.niotv.com/i_index.php?cont=day"
headers = {
"Host": "www.niotv.com",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:43.0) Gecko/20100101 Firefox/43.0",
"Accept": "image/png,image/*;q=0.8,*/*;q=0.5",
"Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3",
"Accept-Encoding": "gzip, deflate",
"Referer": "http://www.niotv.com/i_index.php?cont=day",
"Cookie": "_ga=GA1.2.1557690102.1493724956; _gid=GA1.2.710482855.1493814386; __utma=43184058.1557690102.1493724956.1493803446.1493814295.4; __utmz=43184058.1493724956.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); PHPSESSID=mhkgpmh939ue0309db2aftpvr3; __utmb=43184058.4.10.1493814296; __utmc=43184058; __utmt=1; _gat=1",
"Connection": "keep-alive",
"If-Modified-Since": "Wed, 04 May 2017 12:01:45 GMT",
"If-None-Match": "4fc99fe0-38-6b903c40"
        }
form_data = {
    "act": "select", 
    "sch_id": "20",
    # "ch_name": "TVBS",
    "day" : "2017-06-09",
    "grp_id":"-1",
    "cont":"day"
}
 
s = requests.Session()
_h=dict(headers)
res = s.post(url,headers=_h,data=form_data)
with open('download.html',"w") as f:
    f.write(res.content)
soup = BeautifulSoup(res.content,"lxml")
# print soup
z=soup.find_all('img')
print len(z)
z = z[20]
print "##",z
print z['src']
dd=str(z)[23:-3]
print 'url',url[:-20] 
# url == http://www.niotv.com/
new=url[:-20]+z['src']

img = s.get(new,headers=_h)
# print img.content 
with open('tmp',"w") as f:
    f.write(img.content)