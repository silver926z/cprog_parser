# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import urllib,urllib2
import time
import codecs,json,datetime
import boto3
import pytz


channel_map ={ # tv_id -- nio_id
"5":"16",
"6":"107",
"7":"11",
"9":"13",
"10":"80",
"11":"15",
"12":"26",
"13":"17",
"16":"133",
"17":"12",
"18":"59",
"19":"58",
"20":"62",
"21":"61",
"22":"65",
"23":"63",
"24":"148",
"25":"64",
"26":"24",
"27":"33",
"28":"21",
"29":"34",
"30":"35",
"31":"19",
"32":"23",
"33":"18",
"49":"173",
"50":"40",
"51":"42",
"52":"44",
"53":"45",
"54":"38",
"55":"41",
"56":"20",
"57":"43",
"58":"79",
"61":"55",
"62":"56",
"63":"57",
"64":"141",
"65":"46",
"66":"48",
"67":"50",
"68":"52",
"69":"47",
"70":"49",
"71":"53",
"72":"66",
"73":"67",
"74":"68",
"88":"84",
}
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
    for idx,i in enumerate(out):
        if i.string not in ["","\n",u'\xa0'] and ('valign' not in str(i)):
            # try:
            #     print "#",idx,i.string.encode('utf-8'),idx%5
            # except:
            #     pass
            if idx % 5 == 0:
                channel.append(i.string.encode('utf-8'))
            elif idx % 5 == 1:
                time.append(i.string.encode('utf-8'))
            elif idx % 5 == 2:
                print i.find('a')['href'].encode('utf-8')
                if i.string in [None,"","\n",u'\xa0']:
                    show.append("Can't encode utf-8".encode('utf-8'))
                else:
                    show.append(i.string.encode('utf-8'))
            elif idx % 5 == 3:
                if i.string in [None,"","\n",u'\xa0',' ']:
                    attr.append("NO data".encode('utf-8'))
                attr.append(i.string.encode('utf-8'))
            elif idx % 5 == 4:
                pass
    body = []
    for i in range(len(channel)):
        # print len(channel),len(show),len(attr)
        channel_data = {}
        channel_data['fields'] = {}
        channel_data['type'] = 'add'
        channel_data['id'] = str(i)
        channel_data['fields']['channel'] = channel[i]
        channel_data['fields']['show'] = show[i]
        new_attr = [x for x in attr[i].split("-")]
        channel_data['fields']['attr'] = new_attr
        # channel_data['fields']['date'] = str(my_date)
        my_date_tmp = str(my_date).split("-")
        # channel_data['fields']['time_start'] = str(my_date)+'T'+time[i].split("~")[0]+":00Z"
        time_start_hour = int(time[i].split("~")[0].split(":")[0])
        time_start_minute = int(time[i].split("~")[0].split(":")[1])
        time_end_hour = int(time[i].split("~")[1].split(":")[0])
        time_end_minute = int(time[i].split("~")[1].split(":")[1])
        channel_data['fields']['time_start'] = time_convert(int(my_date_tmp[0]),int(my_date_tmp[1]),int(my_date_tmp[2]),time_start_hour,time_start_minute,0)
        # channel_data['fields']['time_end'] = str(my_date)+'T'+time[i].split("~")[1]+":00Z"
        channel_data['fields']['time_start'] = time_convert(int(my_date_tmp[0]),int(my_date_tmp[1]),int(my_date_tmp[2]),time_end_hour,time_end_minute,0)        
        body.append(channel_data)
    ss = json.dumps(body , encoding = 'UTF-8',ensure_ascii=False)
    ss = ss.encode('utf8')
    # print ss
    # f = codecs.open("02_thsrc.json", 'w', encoding='utf-8')
    # f.write(ss)
    # f.close()
    return ss

def time_convert(year,month,day,hour,minute,second):
    # date_time = '29.08.2011@11:05:02'
    date_time = str(day)+"."+str(month)+"."+str(year)+"@"+str(hour)+":"+str(minute)+":"+str(second)
    pattern = '%d.%m.%Y@%H:%M:%S'
    epoch = int(time.mktime(time.strptime(date_time, pattern)))
    return epoch
if __name__ == '__main__':
    # get_data(84)
    print get_data(channel_map['62'])
    # for i in channel_map.keys():
    #     print i,'nio-id',channel_map[i]
    #     data = get_data(channel_map[i])
    #     key = 'xd/'+str(i)+'.json'
        # boto3.resource("s3").Bucket("final-105062550").put_object(Key = key, Body = data, ACL='public-read')
    # f = codecs.open("02_thsrc.json", 'w', encoding='utf-8')
    # s3_client = boto3.client('s3')
    # s3_client.upload_file('tmp.json', 'silver-playing-bucket', 'hello-remote.txt')    
