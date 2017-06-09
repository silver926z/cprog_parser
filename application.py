# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import urllib,urllib2
import codecs,json,datetime
import boto
import json
import boto3
import json
import logging
import flask
from flask import request, Response
import pytz

# Create and configure the Flask app
application = flask.Flask(__name__)
application.config.from_object('default_config')
application.debug = application.config['FLASK_DEBUG'] in ['true', 'True']


SUBJECT = "Thanks for signing up!"
BODY = "Hi %s!\n\nWe're excited that you're excited about our new product! We'll let you know as soon as it's available.\n\nThanks,\n\nA New Startup"


@application.route('/', methods=['POST'])
def message_get():
    if request.json is None:
        # Expect application/json request
        response = Response("", status=415)
        print "??"
    else:
        boto3.resource("s3").Bucket("silver-playing-bucket").put_object(Key = "why", Body = "damn")
    
        print "starting..."
        data = request.get_json()
        # data = json.loads(data)
        ch_id = data["chid"]
        print "ch_id",ch_id
        print "type ch_id",type(ch_id)
        out_data = get_data(ch_id)
        file_name = str(ch_id)+".json"
        print "complete!"
        boto3.resource("s3").Bucket("silver-playing-bucket").put_object(Key = file_name, Body = out_data)
        boto3.resource("s3").Bucket("silver-playing-bucket").put_object(Key = "my_send", Body = data["chid"])
            
        
    return 'OK'

def get_data(channel_id):
    channel_id = int(channel_id)
    date = datetime.datetime.now(pytz.timezone('Asia/Taipei')).date()
    channel_data= {}
    url = "http://www.niotv.com/i_index.php?cont=day"
    request = urllib2.Request(url) 
    request.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:43.0) Gecko/20100101 Firefox/43.0")
    form_data = {
        "act": "select", 
        "sch_id": channel_id,
        "day" :str(date),
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
    print "bug?"
    for idx,i in enumerate(out):
        if i.string not in ["",None,"\n",u'\xa0'] :
            print "#",idx,i.string.encode('utf-8')
            if cnt % 3 == 0:
                channel.append(i.string.encode('utf-8'))
            elif cnt % 3 == 1:
                show.append(i.string.encode('utf-8'))
            elif cnt % 3 == 2:
                attr.append(i.string.encode('utf-8'))
            cnt +=1
    print "bug2?"
        
    for i in range(len(channel)):
        channel_data[i] = {}
        channel_data[i]['channel'] = channel[i]
        channel_data[i]['show'] = show[i]
        channel_data[i]['attr'] = attr[i]
        channel_data[i]['time'] = str(date)  
    ss = json.dumps(channel_data , encoding = 'UTF-8',ensure_ascii=False)
    ss = ss.encode('utf8')
    return ss


if __name__ == '__main__':
    application.run(host='0.0.0.0')