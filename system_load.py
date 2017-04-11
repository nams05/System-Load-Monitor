#!/usr/bin/python
import psutil
import sys
import os
import datetime
import time
import inspect

#calculate cpu usage
def getCpuUsage():
	cpu=psutil.cpu_times()									
	total=0
	for i in cpu:
		total+=i
	cpu_usage=100-((cpu[3]/total)*100)
	return "{0:.2f}".format(cpu_usage)

def getTime():
	now=datetime.datetime.now()	
	time_tuple=[]
	time_tuple.append(now.strftime("%H")) #time_tuple[0]=hours
	time_tuple.append(now.strftime("%M")) #time_tuple[1]=mins
	time_tuple.append(now.strftime("%S")) #time_tuple[2]=secs
	time_tuple.append(((int(time_tuple[0])*60)+(int(time_tuple[1])))*60 +int(time_tuple[2])) #time_tuple[3]=total secs
	time_tuple.append((int(time_tuple[0])*60)+int(time_tuple[1])) #time_tuple[4]=total mins
	return time_tuple

def getProcessInfo():
	total_process=0
	sleeping_process=0
	zombie_process=0
	running_process=0
	for proc in psutil.process_iter():
	    try:
	    	pinfo = proc.as_dict(attrs=['status'])
	    except psutil.NoSuchProcess:
	        pass
	    else:
	        total_process+=1
	        if (pinfo['status'] == "sleeping"):
	        	sleeping_process+=1
	        elif (pinfo['status'] == "running"):
	        	running_process+=1
	        elif (pinfo['status']=="zombie"):
	        	zombie_process+=1

	return [total_process,sleeping_process,running_process,zombie_process]

dir= os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory

now=datetime.datetime.now()
date=now.strftime("%d-%m-%y")

f=open(dir+'/data/'+date+'_per_sec.txt',"a" )
fs=open(dir+'/data/'+date+'_per_min.txt',"a" )

while  1 :
	time_tuple=getTime()
	cpu_usage=getCpuUsage()
	#calculate RAM usage
	VM=psutil.virtual_memory()
	swap=psutil.swap_memory()
	uptime=int(time.time() - psutil.boot_time())
	users=psutil.users()
	load_avg=os.getloadavg()
	proc=getProcessInfo()
	if (time_tuple[2] == "00"):
		fs.write(str(time_tuple[4])+" "+str(load_avg[0])+"\n")
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
	f.write(str(time_tuple[3])+" "+str(cpu_usage)+" "+str(VM[2])+" "+str(swap[3])+" "+str(uptime)+" "+str(len(users))+" "+str(proc[0])+" "+str(proc[2])+" "+str(proc[1])+" "+str(proc[3])+" "+str("{0:.2f}".format(read_speed))+" "+str("{0:.2f}".format(write_speed))+" "+str("{0:.2f}".format(up_speed))+" "+str("{0:.2f}".format(down_speed))+" \n")
	#break the loop at EOD
	if (time_tuple[0] == "23") and (time_tuple[1] == "59") and (time_tuple[2] == "59"):
		break
	
f.close()
fs.close()
# call the send_report script with 2 argument 
sys.argv=['send_report.py',dir+"/data/"+date+"_per_sec.txt",dir+"/data/"+date+"_per_min.txt",date]
execfile("send_report.py")
time.sleep(1)
print "calling system_load.py"
#call this script again
execfile("system_load.py")