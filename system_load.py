#!/usr/bin/python
import psutil
import sys
import os
import datetime
import time
import inspect


def getEpocTime():
	return int(time.time())

def getDate()
	now=datetime.datetime.now()
	date=now.strftime("%d %b %Y")
	return date

def getCpuUsage():
	cpu=psutil.cpu_times()									
	total=0
	for i in cpu:
		total+=i
	cpu_usage=100-((cpu[3]/total)*100)
	load_avg=os.getloadavg()
	return "{0:.2f}".format(cpu_usage),load_avg

def getMemoryUsage():
	VM=psutil.virtual_memory()
	return VM[2]

def getSwapUsage():
	swap=psutil.swap_memory()
	return swap[3]

def getRunningProcess():
	total_process=0
	zombie_process=0
	running_process=0
	for proc in psutil.process_iter():
	    try:
	    	pinfo = proc.as_dict(attrs=['status'])
	    except psutil.NoSuchProcess:
	        pass
	    else:
	        total_process+=1
	        if (pinfo['status'] == "running"):
	        	running_process+=1
	        elif (pinfo['status']=="zombie"):
	        	zombie_process+=1

	return total_process,running_process,zombie_process


def getDiskUsage():
	diskstats=psutil.disk_io_counters()
	return diskstats

def getNetworkUsage():
	netstats=psutil.net_io_counters(pernic=False)
	return netstats

def getLoggedInUsers():
	users=psutil.users()
	usernames=[]
	for i in range(0,len(users)):
		usernames.append(users[i][0])
	return usernames


dir= os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory

while  1 :
	date_now=getDate()
	time.sleep(1)
	date_later=getDate()
	if(date_now ==date_later)
		f=open(dir+'/data/'+date_now,"a" )
	else
		f=open(dir+'/data/'+date_later,"a" )
	swap=psutil.swap_memory()
	uptime=int(time.time() - psutil.boot_time())
	proc=getProcessInfo()
	netstats_before=psutil.net_io_counters(pernic=False)
	diskstats_before=psutil.disk_io_counters()
	print (str(time_tuple[0])+" "+str(time_tuple[1])+" "+str(time_tuple[2])+" \n")
	time.sleep(1)
	netstats_after=psutil.net_io_counters(pernic=False)
	diskstats_after=psutil.disk_io_counters()
	read_speed=float(diskstats_after[2]-diskstats_before[2])/1024
	write_speed=float(diskstats_after[3]-diskstats_before[3])/1024
	up_speed=float(netstats_after[0]-netstats_before[0])/1024
	down_speed=float(netstats_after[1]-netstats_before[1])/1024
	f.write(str(time_tuple[3])+" "+str(cpu_usage)+" "+str(VM[2])+" "+str(swap[3])+" "+str(len(users))+" "+str(proc[0])+" "+str(proc[2])+" "+str(proc[1])+" "+str(proc[3])+" "+str("{0:.2f}".format(read_speed))+" "+str("{0:.2f}".format(write_speed))+" "+str("{0:.2f}".format(up_speed))+" "+str("{0:.2f}".format(down_speed))+" \n")
	#break the loop at EOD
	if (time_tuple[0] == "23") and (time_tuple[1] == "59") and (time_tuple[2] == "59"):
		break
	
f.close()