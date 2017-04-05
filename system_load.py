#!/usr/bin/python
import psutil
import sys
import os
import datetime
import time
import inspect

#calculate cpu usage
def CPU_usage():
	cpu=psutil.cpu_times()									
	total=0
	for i in cpu:
		total+=i
	cpu_usage=100-((cpu[3]/total)*100)
	return "{0:.2f}".format(cpu_usage)

def Time():
	now=datetime.datetime.now()	
	time_tuple=[]
	time_tuple.append(now.strftime("%H")) #time_tuple[0]=hours
	time_tuple.append(now.strftime("%M")) #time_tuple[1]=mins
	time_tuple.append(now.strftime("%S")) #time_tuple[2]=secs
	time_tuple.append(((int(time_tuple[0])*60)+(int(time_tuple[1])))*60 +int(time_tuple[2])) #time_tuple[3]=total secs
	return time_tuple

dir= os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory

now=datetime.datetime.now()
date=now.strftime("%d_%m_%y")

f=open(date+'.txt',"a" )

while  1 :
	time_tuple=Time()
	cpu_usage=CPU_usage()
	#calculate RAM usage
	VM=psutil.virtual_memory()
	f.write(str(time_tuple[3])+" "+str(cpu_usage)+" "+str(VM[2])+"\n")
	print (str(time_tuple[3])+" "+str(cpu_usage)+" "+str(VM[2])+"\n")
	time.sleep(1)
	#break the loop at EOD
	if (time_tuple[0] == "23") and (time_tuple[1] =="59") and (time_tuple[2] == "58"):
		break
	
f.close
# call the send_report script with 1 argument ie file of that day
sys.argv=['send_report.py',date+".txt"]
execfile("send_report.py")
time.sleep(1)
#call this script again
execfile("system_load.py")
