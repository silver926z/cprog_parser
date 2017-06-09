from bs4 import BeautifulSoup
import codecs,json,datetime
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
with open("tmp.html",'r') as f:
    data = f.read()
soup = BeautifulSoup(data)
# print soup
tmp = soup.find_all('form')
dic = {}
for idx,i in enumerate(tmp):
    form_data = i.find("input",attrs={'name':'sch_id', 'type':'hidden'})
    form_data2 = i.find("input",attrs={'name':'ch_name', 'type':'hidden'})
    if form_data != None and form_data2 != None:
        print form_data['value'].encode('utf-8'),form_data2['value'].encode('utf-8')

        s = form_data['value'].encode('utf-8') +' <---> '+form_data2['value'].encode('utf-8')
        
        # print idx,form_data['value']
        # print idx,form_data2['value']
        # dic[form_data['value']] = {}
        # dic[form_data['value']] = form_data2['value'].encode('utf-8')        
        # ss = json.dumps(dic , encoding = 'UTF-8',ensure_ascii=False)
        # f = codecs.open("test.txt", 'w', encoding='utf-8')
        # f.write(ss+'\n')
        # f.close()