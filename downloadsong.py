# -*- coding: gbk -*-
import json
import urllib
import re
from HTMLParser import HTMLParser
import urllib2
import traceback
import sys
strss = input("data")
strids="32924140,31249789,33794470,33794522,33794644,33794951,33794970,33794962,33794956,33794976,242343,209225,236989,1561243,7145740,246719,7340508,7144261,14850919,24944544,7340650,220457,7342856,290184,258145,1561255,240153,1296054,517155,292228,369585,1295984,7144448,205037,14850888,7338595,2070421,7339494,7144754,19062311,1295915,215983,1561345,211246,7145433,1561305,7339151,7338817,7145087,2103613"
def get_ids():

    try:
        j=0
        st=strss.replace("id",'"id"').replace("ctime",'"ctime"');
        data=json.loads(st)
        listsongid=[]
        songs=strids.split(",")
        print "一共%d歌曲" %(len(songs))
        if songs!=None:
            for i in songs:
                j=j+1
                if isinstance(i,str):
                    get_dowloadurl(i,j)
                else:
                    get_dowloadurl(i["id"],j)
    except Exception as li:
        print li       
    return listsongid
       

p=re.compile("\s+<a\shref=\"(.+\s)\"(\s+?)")
def get_dowloadurl(ids,j):
   
    try:  
        pp=str.format("http://music.baidu.com/song/{0}/download?title=&from=naga",ids)
        url=urllib.urlopen(pp)
        aa=url.readlines() 
        if aa!=None:
            for i in aa:          
                index1=i.find('" id="download"')      
                n=i.find("http://")
                if  index1!=-1:                  
                    geturl= i[n:index1]             
                    http=urllib2.urlopen(geturl,timeout=122)
                    b=http.read()
                    heads= http.info().headers
                    filename=str(j)+".mp3"
                    print heads
                    if heads:
                        headdict=returndict(heads)
                        filename=headdict["Content-Disposition"].split(";")[1].split("=")[1]         
                    print str.format("e:/music/{0}",filename)
                    filename=filename.replace('"',"").replace("\r\n","")
                    a=open(str.format("e:/music/{0}",filename),"wb")
                    a.write(b)            
                    a.close()
                    print "下载完成第%d首歌曲" %(j)
                   
            url.close()
    except Exception as e:
         print e
         exstr = traceback.format_exc()
         print exstr


def return_dict(ss):
    a={}
    for i in ss:
        jj=i.split(":")
        if len(jj)>=2:
            a[jj[0]]=jj[1]
   
    if len(a)>0:
        return a

if __name__=="__main__":
    get_ids()
