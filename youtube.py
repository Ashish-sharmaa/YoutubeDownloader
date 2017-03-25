import urllib.request
import urllib.parse
import requests
from bs4 import BeautifulSoup
import pafy
def down_sub(url,name):													       #downloading subtitles
	des=name+'.srt'
	print(url)
	urllib.request.urlretrieve(url,des)
def subtitle(url,name):                                #finding extension for subtitle
	sp='http://ccsubs.com/video/yt:'
	sp=sp+url[32:]
	sp=sp+r'/abc/download?format=srt&lang=en'	
	print(sp)
	down_sub(sp,name)
def make_choice(url):																    #make choice of whether audio or video
	myvid=pafy.new(url)
	i=input('Enter 1 for audio only else enter 2\n')
	if(int(i) is 1):
		dnl=myvid.getbestaudio()                                          #downloading best audio
		dnl.download()
		print('Downloaded')
	elif(int(i) is 2):
		print("Available qualities, extensions and respective size")      #Printing respective resolutions, ext. and sizes respectively
		stream=myvid.streams
		i=1
		for s in stream:
			j=float(s.get_filesize())                                       #Taking much time, can ommit to save time
			j=j/1048576
			jj=str(j)
			print(str(i)+". quality ="+str(s.resolution)+"  extensions ="+str(s.extension)+" size ="+jj[:6]+"MB")
			i+=1
		j=0
		print("\nChoose one out of the above index")                     #Select one out of given indices
		while(j<=0 or j>=i):
			j=int(input())
			if(j<=0 or j>=i):
				print("Invalid option")
		stream[j-1].download()                                            #Video download
		subtitle(url,myvid.title)																				 #subtitle download
		print('Downloaded')	
	else:
		print('Wrong keyword')																						 
def find(url):                                           # Finding top 15 matches. Print their names and durations
	sourcecode=requests.get(url)
	sp="yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink      spf-link "
	plain=sourcecode.text
	soup=BeautifulSoup(plain,'lxml')
	href=[]
	stt=[]
	i=1
	for link in soup.findAll("a",{"class": sp}):
		href=href+[link.get('href')]
		stt=stt+[str(link.string)]
		i+=1
		if i>15:
			break
	i=1
	for link in soup.findAll("span",{"class": "accessible-description"}):		
		stt[i-1]=stt[i-1]+str(link.string)
		i+=1
		if i>15:
		 	break
	if(i is 1):
		print('Not found')
	else:
		j=1
		for ii in stt:
				href[j-1]="http://www.youtube.com/"+href[j-1]
				print(str(j)+". "+ii)
				j+=1;
		print('Type the index you want to download')
		j=0
		while(j<=0 or j>15):
			j=input() 
			j=int(j)
			if(j<=0 or j>15):
				print("invalid input")
		if(j<=15 and j>0):
			hg=href[j-1]
			make_choice(hg)
def main():                                                        #converting name into youtube querry
	print("Enter the Name")
	query_string = urllib.parse.urlencode({"search_query" :input()})  
	html="https://www.youtube.com/results?"
	html=html +query_string
	find(html)
main()

