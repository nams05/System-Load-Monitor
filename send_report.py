import sys
import smtplib
import os
import time;
from email.MIMEMultipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.MIMEText import MIMEText
from numpy import *
import math
import matplotlib.pyplot as plt
import Tkinter
import datetime


now=datetime.datetime.now()
date=now.strftime("%d_%m_%y")
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

plt.plot(time,cpu_usage,'r',label='CPU Usage(%)') # plotting time,cpu_usage separately 
plt.plot(time,ram_usage,'b',label='RAM Usage(%)') # plotting time,ram_usage separately 
plt.legend(loc='upper right')
plt.savefig(date+'_graph.png')

#compose the message
fromaddr = "namrata.gupta05@gmail.com"
toaddr = "hemant6488@gmail.com"
cc="namrata.gupta05@gmail.com"
bcc="namrata.gupta05@gmail.com"
rcpt=[bcc] +[cc] + [toaddr]
img_data = open(date+'_graph.png', 'rb').read()
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Bcc'] = bcc 
msg['Subject'] = "Report : " + date
image = MIMEImage(img_data, name=os.path.basename(date+'_graph.png'))
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
server.login("namrata.gupta05@gmail.com", "password")

text=msg.as_string() #object to string
#Send the mail
server.sendmail(fromaddr, rcpt, text)