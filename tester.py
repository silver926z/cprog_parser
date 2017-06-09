# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import urllib,urllib2
import codecs,json,datetime
import boto3
import pytz

def get_data(channel_id):
    channel_id = int(channel_id)
    my_date = datetime.datetime.now(pytz.timezone('Asia/Taipei')).date()
    channel_data= {}
    url = "http://www.niotv.com/i_index.php?cont=day"
    request = urllib2.Request(url) 
    # request.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:43.0) Gecko/20100101 Firefox/43.0")
    form_data = {
        "act": "select", 
        "sch_id": channel_id,
        "day" : str(my_date),
        "grp_id":"-1",
        "cont":"day"
    }

    form_data = urllib.urlencode(form_data)
    response = urllib2.urlopen(request,data=form_data)  
    html = response.read()
    soup = BeautifulSoup(html,'html.parser')
    tmp = soup.find_all('div',{'class','day'})
    out = tmp[0] #class = day and div
    out = out.find_all('td',{'class','list'})
    cnt=0
    show = []
    attr = []
    channel=[]
    time = []
    # print out
    for idx,i in enumerate(out):
        if i.string not in ["",None,"\n",u'\xa0'] :
            print "#",idx,i.string.encode('utf-8')
            if idx % 5 == 0:
                channel.append(i.string.encode('utf-8'))
            elif idx % 5 == 1:
                time.append(i.string.encode('utf-8'))
            elif idx % 5 == 2:
                show.append(i.string.encode('utf-8'))
            elif idx % 5 == 3:
                attr.append(i.string.encode('utf-8'))
            elif idx % 5 == 4:
                pass
    print len(channel)
    body = []
    for i in range(len(channel)):
        channel_data = {}
        channel_data['fields'] = {}
        channel_data['type'] = 'add'
        channel_data['id'] = str(i)
        channel_data['fields']['channel'] = channel[i]
        channel_data['fields']['show'] = show[i]
        new_attr = [x for x in attr[i].split("-")]
        channel_data['fields']['attr'] = new_attr
        # channel_data['fields']['date'] = str(my_date)
        channel_data['fields']['time_start'] = str(my_date)+'T'+time[i].split("~")[0]+":00Z"
        channel_data['fields']['time_end'] = str(my_date)+'T'+time[i].split("~")[1]+":00Z"
        body.append(channel_data)
    # print body
    ss = json.dumps(body , encoding = 'UTF-8',ensure_ascii=False)
    ss = ss.encode('utf8')
    print ss
    # f = codecs.open("02_thsrc.json", 'w', encoding='utf-8')
    # f.write(ss)
    # f.close()
    return ss

if __name__ == '__main__':
    # get_data(84)
    for i in range(20,30,1):
        data = get_data(i)
        key = 'xd/'+str(i)+'.json'
        boto3.resource("s3").Bucket("final-105062550").put_object(Key = key, Body = data, ACL='public-read')
    # out = get_data(84)
    # f = codecs.open("tmp.json", 'w', encoding='utf-8')
    # f.write(out)
    # f.close()
    # f = codecs.open("02_thsrc.json", 'w', encoding='utf-8')
    # s3_client = boto3.client('s3')
    # s3_client.upload_file('tmp.json', 'silver-playing-bucket', 'hello-remote.txt')    
