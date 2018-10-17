#!/usr/bin/python
# -*- coding: utf8 -*-
import json
import urllib
import re
from HTMLParser import HTMLParser
import urllib2
import traceback
import sys
#global 
strss = input("data")
strids = input("ids")
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
                    a=open(str.format("{1}/{0}",filename),"wb",__file__)
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
