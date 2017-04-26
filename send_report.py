import sys
from smtplib import SMTPException
import smtplib #to send email
import os
import time
from email.MIMEMultipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.MIMEText import MIMEText
import numpy as np
import matplotlib.pyplot as plt
import dotenv #to use .env file
import inspect #  to get working directory
import socket # for hostname
from urllib2 import urlopen # to get IP address
import ast #str to appropriate datatype
import psutil
import logging
import timeit
import linecache


def check_directory_exists(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

def get_disk_usage():
	disk_stats=psutil.disk_usage('/')
	return disk_stats[1]/1048576,disk_stats[2]/1048576

def get_total_memory():
	tots_memory=psutil.virtual_memory()
	return tots_memory[0]/1048576

def get_date_from_timestamp(timestamp): 
	tm_struct=time.localtime(timestamp)
	return time.strftime("%d %b %Y",tm_struct)

def get_timestamp_for_00hr(timestamp):
	date=get_date_from_timestamp(timestamp) 
	tm_struct=time.strptime(date+" 00:00:00","%d %b %Y %H:%M:%S")
	timestamp_at_00hr=time.mktime(tm_struct)
	return int(timestamp_at_00hr)

def get_timestamp_for_next_hour(timestamp):
	return int(timestamp+3600)

def get_timestamp_of_each_hour(timestamp):
	timestamp_of_each_hour=[get_timestamp_for_00hr(timestamp)]
	for i in range(1,24):
		timestamp_of_each_hour.append(get_timestamp_for_next_hour(timestamp_of_each_hour[i-1]))
	return timestamp_of_each_hour

def get_current_directory():
	return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

def get_public_ip():
	return urlopen('http://ip.42.pl/raw').read()

def get_hostname():
	return socket.gethostname()

#function to define color code of each cell
def color(attribute_percent):
	if(attribute_percent<=30):
		return "#099E44"#green 
	elif(attribute_percent<=70):
		return "#0198AD"#blue
	elif(attribute_percent<=100):
		return "#CB202D"#red
	else:
		return "#FFB521"#yellow

def binary_search(key,start,end):
	if(start<=end):
		filename=get_current_directory()+'/data/'+date+'.txt'
		mid=(start+end)/2
		line=linecache.getline(filename,mid)
		new_tuple=ast.literal_eval(line)
		if new_tuple[0]==key:
			return mid
		elif (new_tuple[0]<key):
			return binary_search(key,mid+1,end)
		elif (new_tuple[0]>key):
			return binary_search(key,start,mid-1)
	else:
			return None

def calculate_average(column_number_list, timestamp_start, timestamp_end): # avg of the interval timestamp_end - timestamp_start
	#intialize local variable
	start=time.time()
	global total_lines
	global line_offset
	attribute_averages=[0 for i in range(len(column_number_list))]
	count=0
	try:
		#read file
		with open(get_current_directory()+'/data/'+date+'.txt') as file:
			index=binary_search(timestamp_start,1,total_lines)
			if index == None: #if index is not found search the entire file
				index=1
			file.seek(line_offset[index-1])
			for line in file:
				modified_line=line.rstrip('\n')
				new_tuple=ast.literal_eval(modified_line)
				if (new_tuple[0])>timestamp_end :
					break
				elif (new_tuple[0]>=timestamp_start):
					for i in range(len(column_number_list)):
						attribute_averages[i]+=new_tuple[column_number_list[i]]
					count+=1
	
	except IOError as e:
		logger.exception(str(e))
		quit()

	if count==0:
		return 0
	for i in range(len(column_number_list)):
		attribute_averages[i]=float(attribute_averages[i])/count
	stop=time.time()
	logger.info('Time taken to execute calculate_average(): %s secs' %"{0:.2f}".format(stop-start))
	return attribute_averages

def get_unique_users(timestamp_start, timestamp_end):
	unique_users=set([])
	global total_lines
	global line_offset
	with open(get_current_directory()+'/data/'+date+'.txt') as file:
		index=binary_search(timestamp_start,1,total_lines)
		if index == None: #if index is not found search the entire file
			index=1
		file.seek(line_offset[index-1])
		for line in file:
			modified_line=line.rstrip('\n')
			new_tuple=ast.literal_eval(modified_line)
			if (new_tuple[0])>timestamp_end :
				break
			elif (new_tuple[0]>=timestamp_start):
				for each_user in new_tuple[12]:
					unique_users.add(each_user)

	no_of_users=len(unique_users)
	users=""
	unique_users=list(unique_users)
	for each_user in unique_users :
		users+=each_user+","

	return users.rstrip(",") #remove the trailing comma

#produce html code for email body
def generate_report_table_html(timestamp_start, timestamp_end):
	#current time
	now=time.time()
	tm_struct=time.localtime(now)
	mail_time=time.strftime("%I:%M:%S %p",tm_struct) # time in 12hour format
	used_disk,free_disk=get_disk_usage()
	total_memory=get_total_memory()

	date=get_date_from_timestamp(now) # eg 03 Apr 2017
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
				
				border-style: solid; 
				border-color: #ddd;
			    border-width:0.20%;
			    width: 49%;
			    margin-bottom:.80%
			}


		</style>
	</head>
	<body>'''
	html+="Mail triggered at: "+ date+" "+mail_time+"<br>Hostname: "+ get_hostname()+"<br>Public IP: "+get_public_ip()+'''<br>Following table contains various system metrics:<br><br>
			<table>

				<tr><th rowspan="2">Time (hours)</th><th colspan="2">CPU </th><th rowspan="2">Memory ('''+str(int(total_memory))+'''MB) (Percentage)</th><th rowspan="2">Swap (Percentage)</th><th colspan="3">Processes</th><th colspan="2">Disk (Used= '''+str(int(used_disk))+"MB Free= "+str(int(free_disk))+'''MB)</th><th colspan="2">Network</th><th rowspan="2">Users</th></tr>
				<tr><th>Percentage</th><th>Load Average</th><th>Total</th><th>Running</th><th>Zombie</th><th>Read (MB/s)</th><th>Write (MB/s)</th><th>Egress (MB/s)</th><th>Ingress (MB/s)</th></tr>
			'''	
	for i in range(0,24):
		
		if (timestamp_of_each_hour[i]>=timestamp_start) and (timestamp_of_each_hour[i]<=timestamp_end):
			hour_timestamp_start=timestamp_of_each_hour[i]
			hour_timestamp_end=get_timestamp_for_next_hour(hour_timestamp_start)-1
			averages=(calculate_average([column_index['cpu usage'],column_index['cpu load avg'],column_index['memory'],column_index['swap'],column_index['total process'],column_index['running process'],column_index['zombie process'],column_index['read speed'],column_index['write speed'],column_index['egress speed'],column_index['ingress speed']], hour_timestamp_start, hour_timestamp_end))

			cpu=float("{0:.2f}".format(averages[0]))
			load=float("{0:.2f}".format(averages[1]))
			memory=float("{0:.2f}".format(averages[2]))
			swap=float("{0:.2f}".format(averages[3]))
			total_process=int(float("{0:.2f}".format(averages[4])))
			running=int(float("{0:.2f}".format(averages[5])))
			zombie=int(float(averages[6]))
			read=float("{0:.2f}".format(averages[7]))
			write=float("{0:.2f}".format(averages[8]))
			egress=float("{0:.2f}".format(averages[9]))
			ingress=float("{0:.2f}".format(averages[10]))
			usernames=get_unique_users(hour_timestamp_start, hour_timestamp_end)

			if (total_process==0):
				continue
			html+="<tr><td style=\"background-color:#7C7474\" >"+str(i)+"</td><td style=\"background-color:"+color(cpu)+"\">"+str(cpu)+"</td><td style=\"background-color:"+color(load*20)+"\">"+str(load)+"</td><td style=\"background-color:"+color(memory)+"\">"+str(memory)+"</td><td style=\"background-color:"+color(swap)+"\">"+str(swap)+"</td><td style=\"background-color:"+color(total_process*10)+"\">"+str(total_process)+"</td><td style=\"background-color:"+color(running/total_process*100)+"\">"+str(running)+"</td><td style=\"background-color:"+color(zombie/total_process*100)+"\">"+str(zombie)+"</td><td style=\"background-color:"+color(read*20)+"\">"+str(read)+"</td><td style=\"background-color:"+color(write*20)+"\">"+str(write)+"</td><td style=\"background-color:"+color(egress*20)+"\">"+str(egress)+"</td><td style=\"background-color:"+color(ingress*20)+"\">"+str(ingress)+"</td><td style=\"background-color:"+color(usernames)+"\">"+usernames+"</td></tr>"
			


	html+="</table><br><br><img style=\"float:left\" src=\"cid:image1\"><img src=\"cid:image2\" style=\"float:right\"><img src=\"cid:image3\" style=\"float:left\"><img src=\"cid:image4\" style=\"float:right\"><img src=\"cid:image5\" style=\"float:left\"><img src=\"cid:image6\" style=\"float:right\"></body></html>"
	
	then=time.time()
	logger.info('Time taken to execute %s(): %s secs' %(inspect.currentframe().f_code.co_name, "{0:.2f}".format(then-now)))
	return html

def plot_graph(column_number_list,timestamp_start,timestamp_end,attribute_label,axis_label,graph_no):

	date=get_date_from_timestamp(timestamp_start)
	input_list=[[] for i in range(len(column_number_list))]

	## read file according to column number , segregate into lists
	try:
		with open(get_current_directory()+'/data/'+date+'.txt') as file:
			for each_line in file:
				modified_line=each_line.rstrip('\n')
				new_tuple=ast.literal_eval(modified_line) #convert line to list/tuple according to syntax

				# segregate into lists
				for i in range(len(column_number_list)):
					input_list[i].append(new_tuple[column_number_list[i]])
	except IOError as e:
		logger.exception(str(e))

	## plot graph using input_list
	graphline_color={0:'r',1:'g',2:'b',3:'m'} # color of the graph lines
	plt.close('all')
	#set size of the graph image
	fig_size = plt.rcParams["figure.figsize"]
	fig_size[0] = 20
	fig_size[1] = 10
	plt.rcParams["figure.figsize"] = fig_size
	graph_name=[]
	for i in range(1,len(input_list)):
		graph_name.append(plt.plot(input_list[0],input_list[i],'r',label=attribute_label[i-1])) # plotting each attribute against time
	# plt.xticks(np.arange(0, 24 , 2))
	# plt.yticks(np.arange(0, 110 , 10))
	for i in range(0,len(graph_name)):
		plt.setp(graph_name[i],color=graphline_color[i], linewidth=1.0)
	plt.legend(loc='upper right')
	plt.xlabel(axis_label[0])
	plt.ylabel(axis_label[1])
	# plt.axis([0, 23,0,100],facecolor='b')
	plt.grid(True)
	plt.savefig(get_current_directory()+'/graph/'+date+'_'+graph_no+'_graph.jpg')
	log_str=""
	for i in attribute_label:
		log_str+=i+', '
	log_str=log_str.rstrip(", ")
	logger.debug('Graph: '+log_str+' plotted against Time(secs)')

def send_mail(date,fromaddr,toaddr,cc,bcc,rcpt,html_body):
	try:
		start_time=time.time()
		dir= get_current_directory()
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['To'] = toaddr
		msg['Bcc'] = bcc
		msg['Cc'] = cc
		msg['Subject'] = "Daily Report | Date: " + date +" | Hostname: "+ get_hostname()
		msg.preamble = "System Load Report"

		html_part=MIMEText(html_body,'html')
		msg.attach(html_part)

		for i in range(1,7):
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
		server.set_debuglevel(0)
		server.ehlo()
		server.starttls()
		server.ehlo()

		#Next, log in to the server
		server.login(dotenv.get("From"), dotenv.get("PASSWORD"))
		logger.debug('Successfully logged in')
		text=msg.as_string() #object to string
		#Send the mail
		error_report=server.sendmail(fromaddr, rcpt, text)
		if error_report:
			logger.error('Following recipients were refused with the error code\n'+error_report)
		else:
			logger.debug('Mail was successfully sent to all recipients')
		end_time=time.time()
		logger.info('Time taken to execute %s(): %s secs' %(inspect.currentframe().f_code.co_name,"{0:.2f}".format(end_time-start_time)))
	except SMTPException as e:
		logger.exception(str(e))
		quit()


#<===========================================================MAIN PROGRAM=============================================================>

if __name__=='__main__':
	try:
		start_time=time.time()

		if len(sys.argv)>1:
			timestamp_of_each_hour=get_timestamp_of_each_hour(int(sys.argv[1]))
			timestamp_start=int(sys.argv[1])
			timestamp_end=int(sys.argv[2])
		else:
			timestamp_of_each_hour=get_timestamp_of_each_hour(int(time.time()))
			timestamp_start=timestamp_of_each_hour[0]
			timestamp_end=get_timestamp_for_next_hour(timestamp_of_each_hour[23])-1

		date=get_date_from_timestamp(timestamp_start)

		check_directory_exists(get_current_directory()+'/log')
		#initialize logger
		logger=logging.getLogger(__name__)
		logger.setLevel(logging.DEBUG)
		formatter=logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
		file_handler=logging.FileHandler(get_current_directory()+'/log/'+date+'.log')
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)
		# logging.basicConfig(filename='file.log',level=logging.DEBUG,format='%(asctime)s [%(levelname)s] %(message)s')

		
		dotenv.load()

		column_index={
		'timestamp':0,
		'cpu usage':1,
		'cpu load avg':2,
		'memory':3,
		'swap':4,
		'total process':5,
		'running process':6,
		'zombie process':7,
		'read speed':8,
		'write speed':9,
		'egress speed':10,
		'ingress speed':11,
		'usernames':12
		}

		with open(get_current_directory()+'/data/'+date+'.txt') as file:
			line_offset = []
			offset = 0
			total_lines=0
			for line in file:
				line_offset.append(offset)
				offset += len(line)
				total_lines+=1
		plot_time_start=time.time()
		#plotting all graphs
		plot_graph([column_index['timestamp'],column_index['cpu usage']], timestamp_start,timestamp_end,['CPU Usage(%)'],['timestamp','CPU(%)'],'1')
		plot_graph([column_index['timestamp'],column_index['cpu load avg']], timestamp_start,timestamp_end,['Average load(per min)'],['timestamp','Average Load'],'2')
		plot_graph([column_index['timestamp'],column_index['memory']], timestamp_start,timestamp_end,['RAM Usage(%)'],['timestamp','Memory(%)'],'3')
		plot_graph([column_index['timestamp'],column_index['total process'],column_index['running process'],column_index['zombie process']], timestamp_start,timestamp_end,['Total Processes','Running Processes','Zombie Processes'],['timestamp','No. of Processes'],'4')
		plot_graph([column_index['timestamp'],column_index['read speed'],column_index['write speed']], timestamp_start,timestamp_end,['Read Speed(MB/s)','Write Speed(MB/s)'],['timestamp','Disk Operations'],'5')
		plot_graph([column_index['timestamp'],column_index['egress speed'],column_index['ingress speed']], timestamp_start,timestamp_end,['Egress Speed(MB/s)','Ingress Speed(MB/s)'],['timestamp','Network Speed (MB/s)'],'6')
		plot_time_end=time.time()
		logger.info('Time taken to plot all graphs: %s secs' %("{0:.2f}".format(plot_time_end-plot_time_start)))

		# compose the email
		fromaddr = dotenv.get("From")
		toaddr = dotenv.get("To")
		cc = dotenv.get("Cc")
		bcc = dotenv.get("Bcc")
		rcpt =[cc] + [bcc] + [toaddr]
		html_body =(generate_report_table_html(timestamp_start,timestamp_end))
		send_mail(date,fromaddr,toaddr,cc,bcc,rcpt,html_body)

		end_time=time.time()
		logger.info('Finished execution in %s secs\n' %("{0:.2f}".format(end_time-start_time)))
	except Exception,e:
		logger.exception(str(e))
		end_time=time.time()
		logger.info('Finished execution in %s secs\n' %("{0:.2f}".format(end_time-start_time)))
		quit()

