import sys
import smtplib
import os
import time;
from email.MIMEMultipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.MIMEText import MIMEText
import numpy as np
import math
import matplotlib.pyplot as plt
import Tkinter
import datetime
import dotenv #to use .env file
import array
import render_html

dotenv.load()

now=datetime.datetime.now()
date=now.strftime("%d_%m_%y")
#reading the file from bash script and making 3 lists for time,cpu usage , ram usage
i=0
time=[]
cpu_usage=[]
ram_usage=[]
total_memory=3758412.0
with open(sys.argv[1]) as f:
	for word in f.read().split():
		if (i%3==0):
			time.append(int(word))
		elif (i%3==1):
			cpu_usage.append(float(word))
		elif (i%3==2):
			ram=((float(word))/total_memory)*100.
			ram_usage.append(ram)
		i=i+1
hr=[]	
for i in time:
	hr.append(i/3600)

cpu_usage_avg=array.array('f',(0,)*24)
ram_usage_avg=array.array('f',(0,)*24)
count=array.array('i',(0,)*24)

cpu_usage_avg[hr[0]]+=cpu_usage[0]
ram_usage_avg[hr[0]]+=ram_usage[0]
count[hr[0]]+=1
for i in range(1,len(hr)):
		cpu_usage_avg[hr[i]]+=cpu_usage[i]
		ram_usage_avg[hr[i]]+=ram_usage[i]
		count[hr[i]]+=1	
for i in range(0,24):
	if (count[i]==0):
		continue
	cpu_usage_avg[i]=cpu_usage_avg[i]/count[i]
	ram_usage_avg[i]=ram_usage_avg[i]/count[i]
	render_html.html+="<tr style=\"background-color:"+render_html.color(ram_usage_avg)+"\"><td>"+str(i)+"</td><td>"+str(cpu_usage_avg[i])+"</td><td>"+str(ram_usage_avg[i])+"</td></tr>"

render_html.html+="</table><br><br><img src=\"cid:image1\"></body></html>"


#plotting the graph using the 3 lists
plt.close('all')
fig_size = plt.rcParams["figure.figsize"] #set the size of the generated graph 
# Set figure width to 20 and height to 10
fig_size[0] = 20
fig_size[1] = 10
plt.rcParams["figure.figsize"] = fig_size
cpu=plt.plot(time,cpu_usage,'r',label='CPU Usage(%)') # plotting time,cpu_usage separately 
ram=plt.plot(time,ram_usage,'g',label='RAM Usage(%)') # plotting time,ram_usage separately
# Get current size

 
# plt.xticks(np.arange(0, 24 , 2))
plt.yticks(np.arange(0, 110 , 10))
plt.setp(cpu,color='r', linewidth=1.0)
plt.setp(ram, color='g', linewidth=1.0)
plt.legend(loc='upper right')
plt.xlabel('time (secs)')
plt.ylabel('load(%)')
# plt.axis([0, 23,0,100],facecolor='b')
plt.grid(True)
plt.savefig(date+'_graph.jpg')

# compose the email
fromaddr = "namrata.gupta05@gmail.com"
toaddr = "hemant6488@gmail.com"
cc="chipndale134@gmail.com"
bcc="namrata.gupta05@gmail.com"
rcpt=[cc]  + [bcc]+ [toaddr]
img_data = open(date+'_graph.jpg', 'rb').read()
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Bcc'] = bcc 
msg['Cc'] = cc
msg['Subject'] = "Report : " + date
msg.preamble = "System Load Report"

html_body=render_html.html

html_part=MIMEText(html_body,'html')
msg.attach(html_part)


image = MIMEImage(img_data, name=os.path.basename(date+'_graph.jpg'))
image.add_header('Content-ID', '<image1>')
msg.attach(image)
# f = open('top.txt')
# Lines=f.readlines()
# body = Lines[0]+ Lines[1]+ Lines[2]+ Lines[3]
# f.close()
# msg.attach(MIMEText(body, 'plain')) #attach body to MIME msg

#create SMTP object for connection
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.ehlo()

#Next, log in to the server
server.login("namrata.gupta05@gmail.com", dotenv.get("PASSWORD"))
text=msg.as_string() #object to string
#Send the mail
server.sendmail(fromaddr, rcpt, text)