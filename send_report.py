import sys
import smtplib
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

def render_html():
	html='''<!DOCTYPE html>
	<html>
	<head>
		<style type="text/css">
			table {
	    	border-spacing: 5px;
	    	width:60%;
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
				display: block;
				margin:auto;
				border: 1px solid #ddd;
			    width: 60%;
			}


		</style>
	</head>
	<body>

			<table>
				<tr><th>Time(hr)</th><th>CPU Usage(%)</th><th>RAM Usage(%)</th></tr>
	'''
	return html

def plot_graph(date,time_secs,time_mins,cpu_usage,ram_usage,swap,uptime,users,total_process,running_process,sleeping_process,zombie_process,read_speed,write_speed,up_speed,down_speed,load):
	#plotting the graph using the 3 lists
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
	plt.savefig(date_1+'_graph.jpg')

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
	plt.savefig(date_2+'_graph.jpg')

	fig_size = plt.rcParams["figure.figsize"] 
	fig_size[0] = 20
	fig_size[1] = 10
	plt.rcParams["figure.figsize"] = fig_size
	Uptime=plt.plot(time_secs,uptime,'r') # plotting time,ram_usage separately
	# plt.xticks(np.arange(0, 24 , 2))
	#plt.yticks(np.arange(0, 110 , 10))
	plt.setp(Uptime,color='r', linewidth=1.0)
	plt.legend(loc='upper right')
	plt.xlabel('Time (secs)')
	plt.ylabel('Uptime')
	# plt.axis([0, 23,0,100],facecolor='b')
	plt.grid(True)
	plt.savefig(date_3+'_graph.jpg')

	fig_size = plt.rcParams["figure.figsize"] 
	fig_size[0] = 20
	fig_size[1] = 10
	plt.rcParams["figure.figsize"] = fig_size
	Users=plt.plot(time_secs,users,'r') # plotting time,ram_usage separately
	# plt.xticks(np.arange(0, 24 , 2))
	# plt.yticks(np.arange(0, 110 , 10))
	plt.setp(Users,color='r', linewidth=1.0)
	plt.legend(loc='upper right')
	plt.xlabel('Time (secs)')
	plt.ylabel('No. of users')
	# plt.axis([0, 23,0,100],facecolor='b')
	plt.grid(True)
	plt.savefig(date_4+'_graph.jpg')

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
	plt.savefig(date_5+'_graph.jpg')

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
	plt.savefig(date_6+'_graph.jpg')

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
	plt.savefig(date_7+'_graph.jpg')

	fig_size = plt.rcParams["figure.figsize"] 
	fig_size[0] = 20
	fig_size[1] = 10
	plt.rcParams["figure.figsize"] = fig_size
	Load=plt.plot(time_mins,load,'r') # plotting time,ram_usage separately
	# plt.xticks(np.arange(0, 24 , 2))
	# plt.yticks(np.arange(0, 110 , 10))
	plt.setp(Load,color='r', linewidth=1.0)
	plt.legend(loc='upper right')
	plt.xlabel('Time (mins)')
	plt.ylabel('Load Average')
	# plt.axis([0, 23,0,100],facecolor='b')
	plt.grid(True)
	plt.savefig(date_8+'_graph.jpg')



dotenv.load()

#reading the file from bash script and making 3 lists for time,cpu usage , ram usage
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

with open(sys.argv[1]) as f:
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

j=0
hr2=[]
time_mins=[]
load=[]
with open(sys.argv[2]) as fs:
	for word in fs.read().split():
		if(j%2==0)
			time_mins.append(int(word))
		elif(j%2==1)
			load.append(float(word))
		j+=1

for i in time_mins:
	hr2.append(i/60)

load_avg=array.array('f',(0,)*24)
count2=array.array('i',(0,)*24)
load_avg[hr2[0]]+=load[0]	
count2[hr2[0]]+=1	
for i in range(1,len(hr2)):
		load_avg[hr2[i]]+=load[i]
		count2[hr2[i]]+=1	

for i in range(0,24):
	if (count2[i]==0):
		continue
	load_avg[i]=load_avg[i]/count2[i]

for i in time_secs:
	hr.append(i/3600)


cpu_usage_avg=array.array('f',(0,)*24)
ram_usage_avg=array.array('f',(0,)*24)
swap_avg=array.array('f',(0,)*24)
uptime_avg=array.array('i',(0,)*24)
users_avg=array.array('i',(0,)*24)
total_process_avg=array.array('i',(0,)*24)
running_process_avg=array.array('i',(0,)*24)
sleeping_process_avg=array.array('i',(0,)*24)
zombie_process_avg=array.array('i',(0,)*24)
read_speed_avg=array.array('f',(0,)*24)
write_speed_avg=array.array('f',(0,)*24)
up_speed_avg=array.array('f',(0,)*24)
down_speed_avg=array.array('f',(0,)*24)
count=array.array('i',(0,)*24)

html=render_html()
cpu_usage_avg[hr[0]]+=cpu_usage[0]
ram_usage_avg[hr[0]]+=ram_usage[0]
swap_avg[hr[0]]+=swap[0]
uptime_avg[hr[0]]+=uptime[0]
users_avg[hr[0]]+=users[0]
total_process_avg[hr[0]]+=total_process[0]
running_process_avg[hr[0]]+=running_process[0]
sleeping_process_avg[hr[0]]+=sleeping_process[0]
zombie_process_avg[hr[0]]+=zombie_process[0]
read_speed_avg[hr[0]]+=read_speed[0]
write_speed_avg[hr[0]]+=write_speed[0]
up_speed_avg[hr[0]]+=up_speed[0]
down_speed[hr[0]]+=down_speed[0]
count[hr[0]]+=1

for i in range(1,len(hr)):
		cpu_usage_avg[hr[i]]+=cpu_usage[i]
		ram_usage_avg[hr[i]]+=ram_usage[i]
		swap_avg[hr[i]]+=swap[i]
		uptime_avg[hr[i]]+=uptime[i]
		users_avg[hr[i]]+=users[i]
		total_process_avg[hr[i]]+=total_process[i]
		running_process_avg[hr[i]]+=running_process[i]
		sleeping_process_avg[hr[i]]+=sleeping_process[i]
		zombie_process_avg[hr[i]]+=zombie_process[i]
		read_speed_avg[hr[i]]+=read_speed[i]
		write_speed_avg[hr[i]]+=write_speed[i]
		up_speed_avg[hr[i]]+=up_speed[i]
		down_speed[hr[i]]+=down_speed[i]
		count[hr[i]]+=1	

for i in range(0,24):
	if (count[i]==0):
		continue
	cpu_usage_avg[i]=cpu_usage_avg[i]/count[i]
	ram_usage_avg[i]=ram_usage_avg[i]/count[i]
	swap_avg[hr[i]]=swap[i]/count[i]
	uptime_avg[hr[i]]=uptime[i]/count[i]
	users_avg[hr[i]]=users[i]/count[i]
	total_process_avg[hr[i]]=total_process[i]/count[i]
	running_process_avg[hr[i]]=running_process[i]/count[i]
	sleeping_process_avg[hr[i]]=sleeping_process[i]/count[i]
	zombie_process_avg[hr[i]]=zombie_process[i]/count[i]
	read_speed_avg[hr[i]]=read_speed[i]/count[i]
	write_speed_avg[hr[i]]=write_speed[i]/count[i]
	up_speed_avg[hr[i]]=up_speed[i]/count[i]
	down_speed[hr[i]]=down_speed[i]/count[i]
	html+="<tr style=\"background-color:"+color(ram_usage_avg[i])+"\"><td>"+str(i)+"</td><td>"+str("{0:.2f}".format(cpu_usage_avg[i]))+"</td><td>"+str("{0:.2f}".format(ram_usage_avg[i]))+"</td></tr>"
html+="</table><br><br><img src=\"cid:image1\"></body></html>"


plot_graph(sys.argv[3],time_secs,time_mins,cpu_usage,ram_usage,swap,uptime,users,total_process,running_process,sleeping_process,zombie_process,read_speed,write_speed,up_speed,down_speed,load)

# compose the email
fromaddr = dotenv.get("From")
toaddr = dotenv.get("To")
cc= dotenv.get("Cc")
bcc= dotenv.get("Bcc")
rcpt=[cc]  + [bcc]+ [toaddr]
img_data = open(date+'_graph.jpg', 'rb').read()
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Bcc'] = bcc 
msg['Cc'] = cc
msg['Subject'] = "Report : " + sys.argv[3]
msg.preamble = "System Load Report"

html_body=html

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
server.login(dotenv.get("From"), dotenv.get("PASSWORD"))
text=msg.as_string() #object to string
#Send the mail
server.sendmail(fromaddr, rcpt, text)