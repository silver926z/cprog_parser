import time
date_time = '29.8.2011@11:05:02'
pattern = '%d.%m.%Y@%H:%M:%S'
epoch = int(time.mktime(time.strptime(date_time, pattern)))
print epoch

# with open("channel_mapper.txt","r") as f:
#     dic = f.read()
#     dic = eval(dic)
#     print dic
#     print type(dic)
#     print dic.keys()
# # print c
# res = dict((v,k) for k,v in dic.iteritems())
# for i in dic.iteritems():
#     print i
# for i in res.iteritems():
#     print i