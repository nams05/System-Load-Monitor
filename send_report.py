import sys
from smtplib import SMTPException
import smtplib # to send email
import os
import time
from email.MIMEMultipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.MIMEText import MIMEText
import numpy as np
import matplotlib.pyplot as plt
import dotenv # to use .env file
import inspect # to get working directory
import socket # for hostname
from urllib2 import urlopen # to get IP address
import ast # str to appropriate datatype
import psutil
import logging
import Tkinter
import ConfigParser
import sets

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
		f=open(filename,'r')
		f.seek(line_offset[mid-1])
		for line in f:
			new_tuple=ast.literal_eval(line)
			if new_tuple[0]==key:
				f.close()
				return mid
			elif (new_tuple[0]<key):
				f.close()
				return binary_search(key,mid+1,end)
			elif (new_tuple[0]>key):
				f.close()
				return binary_search(key,start,mid-1)
	else:
			return None

def calculate_average(column_index_list, timestamp_start, timestamp_end): # avg of the interval timestamp_end - timestamp_start
	#intialize local variable
	start=time.time()
	global total_lines
	global line_offset
	attribute_averages=[0 for i in range(len(column_index_list))]
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
					for i in range(len(column_index_list)):
						if column_index_list[i]==12:
							continue
						attribute_averages[i]+=new_tuple[column_index_list[i]]
					count+=1
	except IOError as e:
		logger.exception(str(e))
		quit()

	if count==0:
		return attribute_averages
	for i in range(len(column_index_list)):
		if column_index_list[i]==12:
			attribute_averages[i]=get_unique_users(timestamp_start,timestamp_end)
			continue
		attribute_averages[i]=attribute_averages[i]/count
		if type(attribute_averages[i])==float:
			attribute_averages[i]=float("{0:.2f}".format(attribute_averages[i]))
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
def generate_report_table_html(column_index_list,timestamp_start, timestamp_end,total_attachments):
	#current time
	now=time.time()
	tm_struct=time.localtime(now)
	mail_time=time.strftime("%I:%M:%S %p",tm_struct) # time in 12hour format
	used_disk,free_disk=get_disk_usage()
	total_memory=get_total_memory()
	global graph_label_index
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
	html+="Mail triggered at: "+ date+" "+mail_time+"<br>Hostname: "+ get_hostname()+"<br>Public IP: "+get_public_ip()
	if column_index_list:
		html+='''<br>Following table contains various system metrics:<br><br>
				<table><tr><th>Time (hours)</th>'''
		for i in column_index_list:
			html+="<th>"+graph_label_index[i]+"</th>"
		html+="</tr>"	
		for i in range(0,24):
			if(timestamp_of_each_hour[i]>timestamp_end):
				break
			elif (timestamp_of_each_hour[i]<timestamp_start):
				continue
			elif (timestamp_of_each_hour[i]==timestamp_start):
				hour_timestamp_start=timestamp_of_each_hour[i]
				hour_timestamp_end=get_timestamp_for_next_hour(hour_timestamp_start)-1
				if(hour_timestamp_end>timestamp_end):
					hour_timestamp_end=timestamp_end
			elif (timestamp_of_each_hour[i]>timestamp_start):
				hour_timestamp_start=timestamp_of_each_hour[i]
				hour_timestamp_end=get_timestamp_for_next_hour(timestamp_of_each_hour[i])-1
				if(hour_timestamp_end>timestamp_end):
					hour_timestamp_end=timestamp_end
			averages=(calculate_average(column_index_list, hour_timestamp_start, hour_timestamp_end))

			if (averages[0]==0):
				continue
			html+="<tr>"
			html+="<td style=\"background-color:#7C7474\">"+str(i)+"</td>"
			for j in averages:
				html+="<td style=\"background-color:"+color(j)+"\">"+str(j)+"</td>"

			html+="</tr>"
		html+="</table><br><br>"
	for i in range(total_attachments):
		if (i+1)&1:
			html+="<img style=\"float:left\" src=\"cid:image"+str(i+1)+"\">"
		else:
			html+="<img src=\"cid:image"+str(i+1)+"\" style=\"float:right\">"
	html+="</body></html>"
	
	then=time.time()
	logger.info('Time taken to execute %s(): %s secs' %(inspect.currentframe().f_code.co_name, "{0:.2f}".format(then-now)))
	return html

def plot_graph(list_of_column_index_list,timestamp_start,timestamp_end,axis_label_list):
	plot_time_start=time.time()
	global column_index
	global graph_label_index
	date=get_date_from_timestamp(timestamp_start)
	input_list=[[] for i in range(len(column_index))]
	unique_columns=[column_index['timestamp']]
	for i in range(len(list_of_column_index_list)):
		for j in range(len(list_of_column_index_list[i])):
			unique_columns.append(list_of_column_index_list[i][j])

	## read file according to column number , segregate into lists
	try:
		with open(get_current_directory()+'/data/'+date+'.txt') as file:
			index=binary_search(timestamp_start,1,total_lines)
			if index == None: #if index is not found search the entire file
				index=1
			file.seek(line_offset[index-1])
			for each_line in file:
				modified_line=each_line.rstrip('\n')
				new_tuple=ast.literal_eval(modified_line) #convert line to list/tuple according to syntax
				if (new_tuple[0])>timestamp_end :
					break
				elif (new_tuple[0]>=timestamp_start):
				# segregate into lists
					for i in unique_columns:
						input_list[i].append(new_tuple[i])
		print input_list 
	except IOError as e:
		logger.exception(str(e))
		quit()

	## plot graph using input_list
	graphline_color={0:'r',1:'g',2:'b',3:'m'} # color of the graph lines
	for i in range(len(list_of_column_index_list)):
		plt.close('all')
		#set size of the graph image
		fig_size = plt.rcParams["figure.figsize"]
		fig_size[0] = 20
		fig_size[1] = 10
		plt.rcParams["figure.figsize"] = fig_size
		graph_name=[]
		for j in range(1,len(list_of_column_index_list[i])):
			graph_name.append(plt.plot(input_list[0],input_list[list_of_column_index_list[i][j]],'r',label=graph_label_index[list_of_column_index_list[i][j]])) # plotting each attribute against time
		# plt.xticks(np.arange(0, 24 , 2))
		# plt.yticks(np.arange(0, 110 , 10))
		for j in range(len(graph_name)):
			plt.setp(graph_name[j],color=graphline_color[j], linewidth=1.0)
		plt.legend(loc='upper right')
		plt.xlabel(axis_label_list[i][0])
		plt.ylabel(axis_label_list[i][1])
		# plt.axis([0, 23,0,100],facecolor='b')
		plt.grid(True)
		plt.savefig(get_current_directory()+'/graph/'+date+'_'+ str(i+1) +'_graph.jpg')
		log_str=""
		for j in range(1,len(list_of_column_index_list[i])):
			log_str+=graph_label_index[list_of_column_index_list[i][j]]+', '
		log_str=log_str.rstrip(", ")
		logger.debug('Graph: '+log_str+' plotted against Time(secs)')

	plot_time_end=time.time()
	logger.info('Time taken to plot all graphs: %s secs' %("{0:.2f}".format(plot_time_end-plot_time_start)))

def send_mail(date,fromaddr,toaddr,cc,bcc,rcpt,html_body,total_attachments):
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

		for i in range(1,total_attachments+1):
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

def main(timestamp_start,timestamp_end,column_index_list,list_of_column_index_list,axis_label_list):
	try:
		dotenv.load(get_current_directory()+'/.env')
		start_time=time.time()
		date=get_date_from_timestamp(timestamp_start)

		#plotting all graphs
		plot_graph(list_of_column_index_list, timestamp_start,timestamp_end,axis_label_list)
		total_attachments=len(list_of_column_index_list)
		# compose the email
		fromaddr = dotenv.get("From")
		toaddr = dotenv.get("To")
		cc = dotenv.get("Cc")
		bcc = dotenv.get("Bcc")
		rcpt =[cc] + [bcc] + [toaddr]
		
		html_body =(generate_report_table_html(column_index_list,timestamp_start,timestamp_end,total_attachments))
		send_mail(date,fromaddr,toaddr,cc,bcc,rcpt,html_body,total_attachments)
		end_time=time.time()
		logger.info('Time taken to execute %s(): %s secs' %(inspect.currentframe().f_code.co_name,"{0:.2f}".format(end_time-start_time)))

	except Exception,e:
		logger.exception(str(e))
		end_time=time.time()
		logger.info('Time taken to execute %s(): %s secs' %(inspect.currentframe().f_code.co_name,"{0:.2f}".format(end_time-start_time)))
		quit()


#<===========================================================MAIN PROGRAM=============================================================>

if __name__=='__main__':
	try:
		start_time=time.time()
		check_directory_exists(get_current_directory()+'/log')

		if len(sys.argv)>1:
			timestamp_of_each_hour=get_timestamp_of_each_hour(int(sys.argv[1]))
			timestamp_start=int(sys.argv[1])
			timestamp_end=int(sys.argv[2])
		else:
			timestamp_of_each_hour=get_timestamp_of_each_hour(int(time.time()))
			timestamp_start=timestamp_of_each_hour[0]
			timestamp_end=get_timestamp_for_next_hour(timestamp_of_each_hour[23])-1

		date=get_date_from_timestamp(timestamp_start)

		#initialize logger
		logger=logging.getLogger(__name__)
		logger.setLevel(logging.DEBUG)
		formatter=logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
		file_handler=logging.FileHandler(get_current_directory()+'/log/'+date+'.log')
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)
		# logging.basicConfig(filename='file.log',level=logging.DEBUG,format='%(asctime)s [%(levelname)s] %(message)s')

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
			'users':12
			}

		graph_label_index={
		0:'Time',
		1:'CPU Percentage',
		2:'Average load (per min)',
		3:'RAM Usage (%)',
		4:'Swap Memory (%)',
		5:'Total Processes',
		6:'Running Processes',
		7:'Zombie Processes',
		8:'Read Speed (MB/s)',
		9:'Write Speed (MB/s)',
		10:'Egress Speed (MB/s)',
		11:'Ingress Speed (MB/s)',
		12:'Users'
		}

		with open(get_current_directory()+'/data/'+date+'.txt') as file:
			line_offset = []
			offset = 0
			total_lines=0
			for line in file:
				line_offset.append(offset)
				offset += len(line)
				total_lines+=1

		config = ConfigParser.RawConfigParser()
		config.read('config.ini')
		# column_index_list=[];list_of_column_index_list=[];axis_label_list=set([]);
		# if config.getboolean('Report','report'):
		# 	if config.getboolean('Graph','report.graph'):
		# 		if config.getboolean('Graph','report.graph.cpu'):
		# 			if config.getboolean('Graph','report.graph.cpu.percent'):
		# 				list_of_column_index_list.append([column_index['timestamp'],column_index['cpu usage']])
		# 				axis_label_list.append(['timestamp','CPU(%)'])
		# 			if config.boolean('Graph','report.graph.cpu.load_avg'):
		# 				list_of_column_index_list([column_index['timestamp'],column_index['cpu load avg']])
		# 				axis_label_list.append(['timestamp','Average Load'])

		# 		if config.getboolean('Graph','report.graph.memory'):
		# 			temp=[column_index['timestamp']]
		# 			if config.getboolean('Graph','report.graph.memory.ram'):
		# 				temp.append(column_index['memory'])
		# 			if config.boolean('Graph','report.graph.memory.swap'):
		# 				temp.append(column_index['swap'])
		# 			if config.getboolean('Graph','report.graph.memory.ram') or config.getboolean('Graph','report.graph.memory.swap'):
		# 				axis_label_list.append(['timestamp','Memory(%)'])

		# 		if config.getboolean('Graph','report.graph.processes'):
		# 			if config.getboolean('Graph','report.graph.processes.total'):
		# 				column_index_list.append(column_index['total process'])
		# 			if config.getboolean('Graph','report.graph.processes.running'):
		# 				column_index_list.append(column_index['running process'])
		# 			if config.getboolean('Graph','report.graph.processes.zombie'):
		# 				column_index_list.append(column_index['zombie process'])
		# 			if config.getboolean('Graph','report.graph.processes.total') or config.getboolean('Graph','report.graph.processes.running') or config.getboolean('Graph','report.graph.processes.zombie') :
		# 				axis_label_list.append(['timestamp','No. of Processes'])
	
		# 		if config.getboolean('Graph','report.graph.disk_speed'):
		# 			if config.getboolean('Graph','report.graph.disk_speed.read'):
		# 				column_index_list.append(column_index['read speed'])
		# 			if config.boolean('Graph','report.graph.disk_speed.write'):
		# 				column_index_list.append(column_index['write speed'])
		# 			if config.getboolean('Graph','report.graph.disk_speed.read') or config.getboolean('Graph','report.graph.disk_speed.write'):
		# 				axis_label_list.append(['timestamp','Disk Operations'])
				
		# 		if config.getboolean('Graph','report.graph.network_speed'):
		# 			if config.getboolean('Graph','report.graph.network_speed.egress'):
		# 				column_index_list.append(column_index['egress speed'])
		# 			if config.boolean('Graph','report.graph.network_speed.ingress'):
		# 				column_index_list.append(column_index['ingress speed'])
		# 			if config.getboolean('Graph','report.graph.network_speed.egress') orconfig.getboolean('Graph','report.graph.network_speed.ingress'):
		# 				axis_label_list.append(['timestamp','Network Speed (MB/s)'])

		# 		column_index_list.append(column_index['cpu usage'])
		# 		column_index_list.append(column_index['cpu load avg'])
		# 		column_index_list.append(column_index['memory'])
		# 		column_index_list.append(column_index['swap'])
		# else:
		column_index_list=[column_index['cpu usage'],column_index['cpu load avg'],column_index['memory'],column_index['swap'],column_index['total process'],column_index['running process'],column_index['zombie process'],column_index['read speed'],column_index['write speed'],column_index['egress speed'],column_index['ingress speed'],column_index['users']]

		list_of_column_index_list=[[column_index['cpu usage']],[column_index['cpu load avg']],[column_index['memory'],column_index['swap']],[column_index['total process'],column_index['running process'],column_index['zombie process']],[column_index['read speed'],column_index['write speed']],[column_index['egress speed'],column_index['ingress speed']]]

		axis_label_list=[['timestamp','CPU(%)'],['timestamp','Average Load'],['timestamp','Memory(%)'],['timestamp','No. of Processes'],['timestamp','Disk Operations'],['timestamp','Network Speed (MB/s)']]

		main(timestamp_start,timestamp_end,column_index_list,list_of_column_index_list,axis_label_list)
		end_time=time.time()
		logger.info('Finished execution in %s secs\n' %("{0:.2f}".format(end_time-start_time)))
	except Exception,e:
		logger.exception(str(e))
		end_time=time.time()
		logger.info('Finished execution in %s secs\n' %("{0:.2f}".format(end_time-start_time)))
		quit()