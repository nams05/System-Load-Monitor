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

def renderHtml(hostname, ip,*args):
	now=datetime.datetime.now()
	mail_time=now.strftime("%I:%M:%S %p")
	date=now.strftime("%d %b %Y")
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
	html+="Mail triggered at: "+ date+" "+mail_time+"<br>Hostname: "+ hostname+"<br>Public IP: "+ip+'''<br>Following table contains various system metrics:<br><br>
			<table>

				<tr><th rowspan="2">Time (hours)</th><th colspan="2">CPU Utilization</th><th colspan="2">Memory Utilization</th><th rowspan="2">Uptime</th><th rowspan="2">Users</th><th colspan="4">No. of Processes</th><th colspan="2">Disk Speed</th><th colspan="2">Network Speed</th></tr>
				<tr><th>CPU Usage (%)</th><th>Load Average</th><th>RAM (%) </th><th>Swap (%)</th><th>Total</th><th>Running</th><th>Sleeping</th><th>Zombie</th><th>Read Speed (kB/s)</th><th>Write Speed (kB/s)</th><th>Up Speed (kB/s)</th><th>Down Speed (kB/s)</th></tr>
			'''
	for i in range(0,24):
		if (total_process_avg[i]==0 ):
			continue
		html+="<tr><td style=\"background-color:"+color(i*4)+"\" >"+str(i)+"</td><td style=\"background-color:"+color(args[0][i])+"\">"+str("{0:.2f}".format(args[0][i]))+"</td><td style=\"background-color:"+color(args[1][i]*20)+"\">"+str("{0:.2f}".format(args[1][i]))+"</td><td style=\"background-color:"+color(args[2][i])+"\">"+str("{0:.2f}".format(args[2][i]))+"</td><td style=\"background-color:"+color(args[3][i])+"\">"+str("{0:.2f}".format(args[3][i]))+"</td><td style=\"background-color:"+color(args[4][i]/1000)+"\">"+str(args[4][i])+"</td><td style=\"background-color:"+color(args[5][i]*7.5)+"\">"+str(args[5][i])+"</td><td style=\"background-color:"+color(args[6][i]/args[6][i]*100)+"\">"+str(args[6][i])+"</td><td style=\"background-color:"+color(args[7][i]/args[6][i]*100)+"\">"+str(args[7][i])+"</td><td style=\"background-color:"+color(args[8][i]/args[6][i]*100)+"\">"+str(args[8][i])+"</td><td style=\"background-color:"+color(args[9][i]/args[6][i]*100)+"\">"+str(args[9][i])+"</td><td style=\"background-color:"+color(args[10][i]*10)+"\">"+str("{0:.2f}".format(args[10][i]))+"</td><td style=\"background-color:"+color(args[11][i]*10)+"\">"+str("{0:.2f}".format(args[11][i]))+"</td><td style=\"background-color:"+color(args[12][i]*10)+"\">"+str("{0:.2f}".format(args[12][i]))+"</td><td style=\"background-color:"+color(args[13][i]*10)+"\">"+str("{0:.2f}".format(args[13][i]))+"</td></tr>"
	html+="</table><br><br><img style=\"float:left\" src=\"cid:image1\"><img src=\"cid:image2\" style=\"float:right\"><img src=\"cid:image3\" style=\"float:left\"><img src=\"cid:image4\" style=\"float:right\"><img src=\"cid:image5\" style=\"float:left\"><img src=\"cid:image6\" style=\"float:right\"><img src=\"cid:image7\" style=\"float:left\"><img src=\"cid:image8\" style=\"float:right\"></body></html>"
	return html

def plotGraph(date,*args):
	#plotting the graph using the given lists
	gr_color={0:'r',1:'g',2:'b',3:'m'}
	dir= os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
	
	plt.close('all')
	fig_size = plt.rcParams["figure.figsize"] 
	fig_size[0] = 20
	fig_size[1] = 10
	plt.rcParams["figure.figsize"] = fig_size
	gr_name=[]
	for i in range(1,len(args[0])):
		gr_name.append(plt.plot(args[0][0],args[0][i],'r',label=args[1][i-1])) # plotting time,ram_usage separately
	# plt.xticks(np.arange(0, 24 , 2))
	# plt.yticks(np.arange(0, 110 , 10))
	for i in range(0,len(gr_name)):
		plt.setp(gr_name[i],color=gr_color[i], linewidth=1.0)
	plt.legend(loc='upper right')
	plt.xlabel(args[2][0])
	plt.ylabel(args[2][1])
	# plt.axis([0, 23,0,100],facecolor='b')
	plt.grid(True)
	plt.savefig(dir+'/graph/'+date+'_'+args[3]+'_graph.jpg')

	

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
	for i in range(0,24):
		if(count[i]==0):
			continue
		attribute_avg[i]=attribute_avg[i]/count[i]
	return attribute_avg.tolist()   #return the array as a list

def  sendMail(date,fromaddr,toaddr,cc,bcc,rcpt,html_body):

	hostname=socket.gethostname() 
	ip= urlopen('http://ip.42.pl/raw').read() #for ip
	dir= os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Bcc'] = bcc 
	msg['Cc'] = cc
	msg['Subject'] = "Daily Report | Date: " + date +" | Hostname: "+ hostname
	msg.preamble = "System Load Report"

	html_part=MIMEText(html_body,'html')
	msg.attach(html_part)

	for i in range(1,9):
		img_data = open(dir+'/graph/'+date+'_'+str(i)+'_graph.jpg', 'rb').read()
		image= MIMEImage(img_data, name=os.path.basename(dir+'/graph/'+date+'_'+str(i)+'_graph.jpg'))
		image.add_header('Content-ID', '<image'+str(i)+'>')
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


#<---------------------------------MAIN PROGRAM-------------------------------------->


dotenv.load()
hr=[]
hr2=[]

metrics=readFile(sys.argv[1])
metrics2=readFile2(sys.argv[2])
print "reading files..."

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

#time in mins/secs is converted to hours

for i in time_secs:
	hr.append(i/3600)
for i in time_mins:
	hr2.append(i/60)

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

plotGraph(sys.argv[3],[time_secs,cpu_usage],['CPU Usage(%)'],['Time (sec)','CPU(%)'],'1')
plotGraph(sys.argv[3],[time_secs,ram_usage,swap],['RAM Usage(%)','Swap Memory(%)'],['Time (sec)','Memory(%)'],'2')
plotGraph(sys.argv[3],[time_secs,uptime],['Uptime'],['Time (sec)','Uptime'],'3')
plotGraph(sys.argv[3],[time_secs,users],['No. of Users'],['Time (sec)','No. of Users'],'4')
plotGraph(sys.argv[3],[time_secs,total_process,running_process,sleeping_process,zombie_process],['Total Processes','Running Processes','Sleeping Processes','Zombie Processes'],['Time (sec)','No. of Processes'],'5')
plotGraph(sys.argv[3],[time_secs,read_speed,write_speed],['Read Speed(kB/s)','Write Speed(kB/s)'],['Time (sec)','Disk Operations'],'6')
plotGraph(sys.argv[3],[time_secs,up_speed,down_speed],['Up Speed(kB/s)','Down Speed(kB/s)'],['Time (sec)','Network Speed (kB/s)'],'7')
plotGraph(sys.argv[3],[time_mins,average_load],['Average load(per min)'],['Time (sec)','Average Load'],'8')

print "plotting graph..."
hostname=socket.gethostname() 
ip= urlopen('http://ip.42.pl/raw').read() #for ip
# compose the email
fromaddr = dotenv.get("From")
toaddr = dotenv.get("To")
cc= dotenv.get("Cc")
bcc= dotenv.get("Bcc")
rcpt=[cc]  + [bcc]+ [toaddr]
html_body=renderHtml(hostname, ip,cpu_usage_avg,load_avg,ram_usage_avg,swap_avg,uptime_avg,users_avg,total_process_avg,running_process_avg,sleeping_process_avg,zombie_process_avg,read_speed_avg,write_speed_avg,up_speed_avg,down_speed_avg)
sendMail(sys.argv[3],fromaddr,toaddr,cc,bcc,rcpt,html_body)
print "email sent!!!"