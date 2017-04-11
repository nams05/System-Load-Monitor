import sys
import smtplib #to send email
import os
import time
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
import inspect #  to get working directory
import socket # for hostname
from urllib2 import urlopen # to get IP address 

#function to define color code of rows
def color(cpu):
	if(cpu<=10):
		return "#FDB22B"
	elif(cpu<=20):
		return "#F00088"
	elif(cpu<=30):
		return "#2A58C3"
	elif(cpu<=40):
		return "#FF7C03"
	elif(cpu<=50):
		return "#8408BA"
	elif(cpu<=60):
		return "#B2C300"
	elif(cpu<=70):
		return "#94D301"
	elif(cpu<=80):
		return "#01A5AD"
	elif(cpu<=90):
		return "#AEB18C"
	else:
		return "#01A5AD"

def typeOf(attribute):
	if type(attribute)==float:
		return 'f'
	elif type(attribute)==int:
		return 'i'

def renderHtml(hostname, ip,cpu_usage_avg,ram_usage_avg,swap_avg,uptime_avg,users_avg,total_process_avg,running_process_avg,sleeping_process_avg,zombie_process_avg,read_speed_avg,write_speed_avg,up_speed_avg,down_speed_avg,load_avg):
	html='''<!DOCTYPE html>
	<html>
	<head>
		<style type="text/css">
			table {
	    	border-spacing: 5px;
	    	width:100%;
	    	margin:auto;
	    	}
			th{
			background-color: black;
	    	color: white;
			}
			table, th, td {

	    	border: 2px solid white;
	    	border-collapse: collapse;
	    	}
	    	th, td {
	    	padding: 10px;
	    	text-align: center;
			}
			caption{
			font:15px Helvetica ;
			margin :8px;
			margin-bottom: 8px;	
			}
			img{
				
				border: 1px solid #ddd;
			    width: 49.75%;
			}


		</style>
	</head>
	<body>'''
	html+="Hostname : "+hostname+"<br>"+"Public IP : "+ip+'''<br>Following table contains various system metrics:<br><br>
			<table>

				<tr><th rowspan="2">Time (hours)</th><th colspan="2">CPU Utilization</th><th colspan="2">Memory Utilization</th><th rowspan="2">Uptime</th><th rowspan="2">Users</th><th colspan="4">No. of Processes</th><th colspan="2">Disk Speed</th><th colspan="2">Network Speed</th></tr>
				<tr><th>CPU Usage (%)</th><th>Load Average</th><th>RAM (%) </th><th>Swap (%)</th><th>Total</th><th>Running</th><th>Sleeping</th><th>Zombie</th><th>Read Speed (kB/s)</th><th>Write Speed (kB/s)</th><th>Up Speed (kB/s)</th><th>Down Speed (kB/s)</th></tr>
			'''
	for i in range(0,24):
	if (total_process_avg[i]==0 ):
		continue
	html+="<tr><td style=\"background-color:"+color(i*4)+"\" >"+str(i)+"</td><td style=\"background-color:"+color(cpu_usage_avg[i])+"\">"+str(cpu_usage_avg[i])+"</td><td style=\"background-color:"+color(load_avg[i]*20)+"\">"+str("{0:.2f}".format(load_avg[i]))+"</td><td style=\"background-color:"+color(ram_usage_avg[i])+"\">"+str(ram_usage_avg[i])+"</td><td style=\"background-color:"+color(swap_avg[i])+"\">"+str(swap_avg[i])+"</td><td style=\"background-color:"+color(uptime_avg[i]/1000)+"\">"+str(uptime_avg[i])+"</td><td style=\"background-color:"+color(users_avg[i]*7.5)+"\">"+str(users_avg[i])+"</td><td style=\"background-color:"+color(total_process_avg[i]/total_process_avg[i]*100)+"\">"+str(total_process_avg[i])+"</td><td style=\"background-color:"+color(running_process_avg[i]/total_process_avg[i]*100)+"\">"+str(running_process_avg[i])+"</td><td style=\"background-color:"+color(sleeping_process_avg[i]/total_process_avg[i]*100)+"\">"+str(sleeping_process_avg[i])+"</td><td style=\"background-color:"+color(zombie_process_avg[i]/total_process_avg[i]*100)+"\">"+str(zombie_process_avg[i])+"</td><td style=\"background-color:"+color(read_speed_avg[i]*10)+"\">"+str(read_speed_avg[i])+"</td><td style=\"background-color:"+color(write_speed_avg[i]*10)+"\">"+str(write_speed_avg[i])+"</td><td style=\"background-color:"+color(up_speed_avg[i]*10)+"\">"+str(up_speed_avg[i])+"</td><td style=\"background-color:"+color(down_speed_avg[i]*10)+"\">"+str(down_speed_avg[i])+"</td></tr>"
	html+="</table><br><br><img style=\"float:left\" src=\"cid:image1\"><img src=\"cid:image2\" style=\"float:right\"><img src=\"cid:image3\" style=\"float:left\"><img src=\"cid:image4\" style=\"float:right\"><img src=\"cid:image5\" style=\"float:left\"><img src=\"cid:image6\" style=\"float:right\"><img src=\"cid:image7\" style=\"float:left\"><img src=\"cid:image8\" style=\"float:right\"></body></html>"
	return html

def plotGraph(date,time_secs,time_mins,cpu_usage,ram_usage,swap,uptime,users,total_process,running_process,sleeping_process,zombie_process,read_speed,write_speed,up_speed,down_speed,average_load):
	#plotting the graph using the given lists
	dir= os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
	plt.close('all')
	fig_size = plt.rcParams["figure.figsize"] #set the size of the generated graph 
	# Set figure width to 20 and height to 10
	fig_size[0] = 20
	fig_size[1] = 10
	plt.rcParams["figure.figsize"] = fig_size
	cpu=plt.plot(time_secs,cpu_usage,'r',label='CPU Usage(%)') # plotting time,cpu_usage separately 
	# plt.xticks(np.arange(0, 24 , 2))
	plt.yticks(np.arange(0, 110 , 10))
	plt.setp(cpu,color='r', linewidth=1.0)
	plt.legend(loc='upper right')
	plt.xlabel('Time (secs)')
	plt.ylabel('CPU(%)')
	# plt.axis([0, 23,0,100],facecolor='b')
	plt.grid(True)
	plt.savefig(dir+'/graph/'+date+'_1_graph.jpg')

	plt.close('all')
	fig_size = plt.rcParams["figure.figsize"] 
	fig_size[0] = 20
	fig_size[1] = 10
	plt.rcParams["figure.figsize"] = fig_size
	ram=plt.plot(time_secs,ram_usage,'r',label='RAM Usage(%)') # plotting time,ram_usage separately
	Swap=plt.plot(time_secs,swap,'g',label='Swap Memory(%)')
	# plt.xticks(np.arange(0, 24 , 2))
	plt.yticks(np.arange(0, 110 , 10))
	plt.setp(ram,color='r', linewidth=1.0)
	plt.setp(Swap,color='g', linewidth=1.0)
	plt.legend(loc='upper right')
	plt.xlabel('Time (secs)')
	plt.ylabel('Memory(%)')
	# plt.axis([0, 23,0,100],facecolor='b')
	plt.grid(True)
	plt.savefig(dir+'/graph/'+date+'_2_graph.jpg')

	plt.close('all')
	fig_size = plt.rcParams["figure.figsize"] 
	fig_size[0] = 20
	fig_size[1] = 10
	plt.rcParams["figure.figsize"] = fig_size
	Uptime=plt.plot(time_secs,uptime,'r',label='Uptime') # plotting time,ram_usage separately
	# plt.xticks(np.arange(0, 24 , 2))
	#plt.yticks(np.arange(0, 110 , 10))
	plt.setp(Uptime,color='r', linewidth=1.0)
	plt.legend(loc='upper right')
	plt.xlabel('Time (secs)')
	plt.ylabel('Uptime')
	# plt.axis([0, 23,0,100],facecolor='b')
	plt.grid(True)
	plt.savefig(dir+'/graph/'+date+'_3_graph.jpg')

	plt.close('all')
	fig_size = plt.rcParams["figure.figsize"] 
	fig_size[0] = 20
	fig_size[1] = 10
	plt.rcParams["figure.figsize"] = fig_size
	Users=plt.plot(time_secs,users,'r',label='No. of Users') # plotting time,ram_usage separately
	# plt.xticks(np.arange(0, 24 , 2))
	# plt.yticks(np.arange(0, 110 , 10))
	plt.setp(Users,color='r', linewidth=1.0)
	plt.legend(loc='upper right')
	plt.xlabel('Time (secs)')
	plt.ylabel('No. of users')
	# plt.axis([0, 23,0,100],facecolor='b')
	plt.grid(True)
	plt.savefig(dir+'/graph/'+date+'_4_graph.jpg')

	plt.close('all')
	fig_size = plt.rcParams["figure.figsize"] 
	fig_size[0] = 20
	fig_size[1] = 10
	plt.rcParams["figure.figsize"] = fig_size
	TotalProcess=plt.plot(time_secs,total_process,'r',label='Total Processes') # plotting time,ram_usage separately
	Running=plt.plot(time_secs,running_process,'m',label='Running Processes')
	Sleeping=plt.plot(time_secs,sleeping_process,'g',label='Sleeping Processes')
	Zombie=plt.plot(time_secs,zombie_process,'c',label='Zombie Processes')
	# plt.xticks(np.arange(0, 24 , 2))
	# plt.yticks(np.arange(0, 110 , 10))
	plt.setp(TotalProcess,color='r', linewidth=1.0)
	plt.setp(Running,color='m', linewidth=1.0)
	plt.setp(Sleeping,color='g', linewidth=1.0)
	plt.setp(Zombie,color='c', linewidth=1.0)
	plt.legend(loc='upper right')
	plt.xlabel('Time (secs)')
	plt.ylabel('Processes')
	# plt.axis([0, 23,0,100],facecolor='b')
	plt.grid(True)
	plt.savefig(dir+'/graph/'+date+'_5_graph.jpg')

	plt.close('all')
	fig_size = plt.rcParams["figure.figsize"] 
	fig_size[0] = 20
	fig_size[1] = 10
	plt.rcParams["figure.figsize"] = fig_size
	Read=plt.plot(time_secs,read_speed,'r',label='Read Speed(kB/s)') # plotting time,ram_usage separately
	Write=plt.plot(time_secs,write_speed,'g',label='Write Speed(kB/s)')
	# plt.xticks(np.arange(0, 24 , 2))
	# plt.yticks(np.arange(0, 110 , 10))
	plt.setp(Read,color='r', linewidth=1.0)
	plt.setp(Write,color='g', linewidth=1.0)
	plt.legend(loc='upper right')
	plt.xlabel('Time (secs)')
	plt.ylabel('Disk Operations')
	# plt.axis([0, 23,0,100],facecolor='b')
	plt.grid(True)
	plt.savefig(dir+'/graph/'+ date+'_6_graph.jpg')

	plt.close('all')
	fig_size = plt.rcParams["figure.figsize"] 
	fig_size[0] = 20
	fig_size[1] = 10
	plt.rcParams["figure.figsize"] = fig_size
	Up=plt.plot(time_secs,up_speed,'r',label='Up Speed(kB/s)') # plotting time,ram_usage separately
	Down=plt.plot(time_secs,down_speed,'g',label='Down Speed(kB/s)')
	# plt.xticks(np.arange(0, 24 , 2))
	# plt.yticks(np.arange(0, 110 , 10))
	plt.setp(Up,color='r', linewidth=1.0)
	plt.setp(Down,color='g', linewidth=1.0)
	plt.legend(loc='upper right')
	plt.xlabel('Time (secs)')
	plt.ylabel('Network Speed (kB/s)')
	# plt.axis([0, 23,0,100],facecolor='b')
	plt.grid(True)
	plt.savefig(dir+'/graph/'+date+'_7_graph.jpg')

	plt.close('all')
	fig_size = plt.rcParams["figure.figsize"] 
	fig_size[0] = 20
	fig_size[1] = 10
	plt.rcParams["figure.figsize"] = fig_size
	Average_load=plt.plot(time_mins,average_load,'r',label='Average load(per min)') # plotting time,ram_usage separately
	# plt.xticks(np.arange(0, 24 , 2))
	# plt.yticks(np.arange(0, 110 , 10))
	plt.setp(Average_load,color='r', linewidth=1.0)
	plt.legend(loc='upper right')
	plt.xlabel('Time (mins)')
	plt.ylabel('Average Load')
	# plt.axis([0, 23,0,100],facecolor='b')
	plt.grid(True)
	plt.savefig(dir+'/graph/'+date+'_8_graph.jpg')

#reading the file from bash script and making 14 lists for time,cpu usage , ram usage
def readFile(filename):
	i=0
	time_secs=[]
	cpu_usage=[]
	ram_usage=[]
	swap=[]
	uptime=[]
	users=[]
	total_process=[]
	running_process=[]
	sleeping_process=[]
	zombie_process=[]
	read_speed=[]
	write_speed=[]
	up_speed=[]
	down_speed=[]
	hr=[]

	with open(filename) as f:
		for word in f.read().split():
			if (i%14==0):
				time_secs.append(int(word))
			elif (i%14==1):
				cpu_usage.append(float(word))
			elif (i%14==2):
				ram_usage.append(float(word))
			elif (i%14==3):
				swap.append(float(word))
			elif (i%14==4):
				uptime.append(int(word))
			elif (i%14==5):
				users.append(int(word))
			elif (i%14==6):
				total_process.append(int(word))
			elif (i%14==7):
				running_process.append(int(word))
			elif (i%14==8):
				sleeping_process.append(int(word))
			elif (i%14==9):
				zombie_process.append(int(word))
			elif (i%14==10):
				read_speed.append(float(word))
			elif (i%14==11):
				write_speed.append(float(word))
			elif (i%14==12):
				up_speed.append(float(word))
			elif (i%14==13):
				down_speed.append(float(word))
			i=i+1

	return [time_secs,cpu_usage,ram_usage,swap,uptime,users,total_process,running_process,sleeping_process,zombie_process,read_speed,write_speed,up_speed,down_speed]

def readFile2(filename):
	j=0
	hr2=[]
	time_mins=[]
	average_load=[]
	with open(filename) as fs:
		for word in fs.read().split():
			if(j%2==0):
				time_mins.append(int(word))
			elif(j%2==1):
				average_load.append(float(word))
			j+=1
	return [time_mins,average_load]

def calculateAvg(hour,attribute):
	attribute_avg=array.array(typeOf(attribute[0]),(0,)*24)
	count=array.array('i',(0,)*24)
	attribute_avg[hour[0]]+=attribute[0]
	count[hour[0]]+=1
	for i in range(1,len(hour)):
		attribute_avg[hour[i]]+=attribute[i]
		count[hour[i]]+=1
	for i in range(0,24)
		if(count[hour[i]]==0)
			continue
		attribute_avg[i]=attribute_avg[i]/count[i]
	return attribute_avg.tolist()   #return the array as a list

def  sendMail(date,fromaddr,toaddr,cc,bcc,rcpt,html_body):
	hostname=socket.gethostname() 
	ip= urlopen('http://ip.42.pl/raw').read() #for ip
	dir= os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
	img_data_1 = open(dir+'/graph/'+date+'_1_graph.jpg', 'rb').read()
	img_data_2 = open(dir+'/graph/'+date+'_2_graph.jpg', 'rb').read()
	img_data_3 = open(dir+'/graph/'+date+'_3_graph.jpg', 'rb').read()
	img_data_4 = open(dir+'/graph/'+date+'_4_graph.jpg', 'rb').read()
	img_data_5 = open(dir+'/graph/'+date+'_5_graph.jpg', 'rb').read()
	img_data_6 = open(dir+'/graph/'+date+'_6_graph.jpg', 'rb').read()
	img_data_7 = open(dir+'/graph/'+date+'_7_graph.jpg', 'rb').read()
	img_data_8 = open(dir+'/graph/'+date+'_8_graph.jpg', 'rb').read()
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Bcc'] = bcc 
	msg['Cc'] = cc
	msg['Subject'] = "Report : " + date +" from "+ hostname
	msg.preamble = "System Load Report"

	html_part=MIMEText(html_body,'html')
	msg.attach(html_part)


	image_1 = MIMEImage(img_data_1, name=os.path.basename(dir+'/graph/'+date+'_1_graph.jpg'))
	image_2 = MIMEImage(img_data_2, name=os.path.basename(dir+'/graph/'+date+'_2_graph.jpg'))
	image_3 = MIMEImage(img_data_3, name=os.path.basename(dir+'/graph/'+date+'_3_graph.jpg'))
	image_4 = MIMEImage(img_data_4, name=os.path.basename(dir+'/graph/'+date+'_4_graph.jpg'))
	image_5 = MIMEImage(img_data_5, name=os.path.basename(dir+'/graph/'+date+'_5_graph.jpg'))
	image_6 = MIMEImage(img_data_6, name=os.path.basename(dir+'/graph/'+date+'_6_graph.jpg'))
	image_7 = MIMEImage(img_data_7, name=os.path.basename(dir+'/graph/'+date+'_7_graph.jpg'))
	image_8 = MIMEImage(img_data_8, name=os.path.basename(dir+'/graph/'+date+'_8_graph.jpg'))
	image_1.add_header('Content-ID', '<image1>')
	image_2.add_header('Content-ID', '<image2>')
	image_3.add_header('Content-ID', '<image3>')
	image_4.add_header('Content-ID', '<image4>')
	image_5.add_header('Content-ID', '<image5>')
	image_6.add_header('Content-ID', '<image6>')
	image_7.add_header('Content-ID', '<image7>')
	image_8.add_header('Content-ID', '<image8>')
	msg.attach(image_1)
	msg.attach(image_2)
	msg.attach(image_3)
	msg.attach(image_4)
	msg.attach(image_5)
	msg.attach(image_6)
	msg.attach(image_7)
	msg.attach(image_8)
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
	server.login(dotenv.get("From"), dotenv.get("PASSWORD"))
	text=msg.as_string() #object to string
	#Send the mail
	server.sendmail(fromaddr, rcpt, text)





dotenv.load()
hr=[]
hr2=[]

#time in mins/secs is converted to hours

for i in time_secs:
	hr.append(i/3600)
for i in time_mins:
	hr2.append(i/60)

html=renderHtml(hostname,ip)

metrics=readFile(sys.argv[1])
metrics2=readFile2(sys.argv[2])

#assign values read from file to respective lists
time_mins=metrics2[0]
time_secs=metrics[0]
cpu_usage=metrics[1]
average_load=metrics2[1]
ram_usage=metrics[2]
swap=metrics[3]
uptime=metrics[4]
users=metrics[5]
total_process=metrics[6]
running_process=metrics[7]
sleeping_process=metrics[8]
zombie_process=metrics[9]
read_speed=metrics[10]
write_speed=metrics[11]
up_speed=metrics[12]
down_speed=metrics[13]

#calculate avg of each attribute
cpu_usage_avg=calculateAvg(hr,cpu_usage)
load_avg=calculateAvg(hr2,average_load)
ram_usage_avg=calculateAvg(hr,ram_usage)
swap_avg=calculateAvg(hr,swap)
uptime_avg=calculateAvg(hr,uptime)
users_avg=calculateAvg(hr,users)
total_process_avg=calculateAvg(hr,total_process)
running_process_avg=calculateAvg(hr,running_process)
sleeping_process_avg=calculateAvg(hr,sleeping_process)
zombie_process_avg=calculateAvg(hr,zombie_process)
read_speed_avg=calculateAvg(hr,read_speed)
write_speed_avg=calculateAvg(hr,write_speed)
up_speed_avg=calculateAvg(hr,up_speed)
down_speed_avg=calculateAvg(hr,down_speed)

plotGraph(sys.argv[3],time_secs,time_mins,cpu_usage,ram_usage,swap,uptime,users,total_process,running_process,sleeping_process,zombie_process,read_speed,write_speed,up_speed,down_speed,average_load)

# compose the email
fromaddr = dotenv.get("From")
toaddr = dotenv.get("To")
cc= dotenv.get("Cc")
bcc= dotenv.get("Bcc")
rcpt=[cc]  + [bcc]+ [toaddr]
html_body=renderHtml(hostname, ip,cpu_usage_avg,ram_usage_avg,swap_avg,uptime_avg,users_avg,total_process_avg,running_process_avg,sleeping_process_avg,zombie_process_avg,read_speed_avg,write_speed_avg,up_speed_avg,down_speed_avg,load_avg)
sendMail(sys.argc[3],fromaddr,toaddr,cc,bcc,rcpt,html_body)