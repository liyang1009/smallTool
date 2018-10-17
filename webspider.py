import os
import urllib2
import Queue
import re
from threading import  Thread
queue=Queue.Queue()
content=Queue.Queue()
exist=set()
host=raw_input("host:")
#host="http://www.letao.com"
from HTMLParser import HTMLParser
class ParserHandler(HTMLParser,object):
    	def handle_starttag(self, tag, attrs):
		tag=str.upper(tag)
		if 'A'==tag:
			for i in attrs:
				if 'href'== i[0]:
					url =i[1]
					if url not  in exist and url.find("java")==-1:
						exist.add(url)
						if url.find("http")==-1:
							url=self.host+url
						queue.put(url)				
						print url
						break
		elif 'LINK'==tag:
			pass
		elif 'SCRIPT'==tag:
			pass
	def feed(self,content,host):
		self.host=host
		super(ParserHandler,self).feed(content)
	def handle_endtag(self, tag):
		pass
        def handle_data(self, data):
		pass
parser=ParserHandler();
class HtmlTask():
	def __init__(self,host):
		self.host=host
	def handler(self):
		while True:
			try:
				contentext=content.get()
				size= content.qsize()
				#print(str(size)+'   content')
				parser.feed(contentext,self.host)
			except Exception as e:
				print e
			finally:
				content.task_done()
	def sendhttp(self):
		pass
		

class HttpTask():
	def __init__(self,host):
		self.host=host
	def handler(self):
		while True:
			try:
				url=queue.get();
				#print url
				size= queue.qsize()
				#print("queue  :"+ str(size))
				if url.find('void')==-1:
					f = urllib2.urlopen(url)
					msg= f.info()
					if msg.getcode!=200:
						continue
					tt=""
					contenttype=msg.getheader("Content-Type")
					if contenttype:
						contype=contenttype.split(";")
						if contype and len(contype)==2:
							tt=contype[1].split("=")[1]
					text=f.read()
					if tt:
						print tt
						text=text.decode(tt)
						text=text.encode("ascii", "xmlcharrefreplace")
					content.put(text)
			except Exception as e:
				print e
				print('http error')
			finally:
				queue.task_done()
	def sendhttp(self):
		pass
		

class Execute():
	def __init__(self,htmlcount,httpcount,host):
		self.htmlcount=htmlcount
		self.httpcount=httpcount
		self.htmltask=HtmlTask(host)
		self.httptask=HttpTask(host)
		queue.put(host);
	def html(self):
		for i in range(self.htmlcount):
			t = Thread(target=self.htmltask.handler)
		#	t.setDaemon(True)
			t.start()
		#self.htmltask.handler()
	def http(self):
		for i in range(self.httpcount):
			t=Thread(target=self.httptask.handler)
		#	t.setDaemon(True)
			t.start()
		#self.httptask.handler()

	def exe(self):
		self.http()
		self.html()
		
if __name__=='__main__':
	if host:
		parse_thread_count = int(input("parse_thread_count"))
		net_thread_count = int(input("net_thread_count"))
		execute=Execute(parse_thread_count,net_thread_count,host)
		execute.exe();
		content.join()
		queue.join()
		print '#########################

