#!/usr/bin/python
import psutil
import sys
import os
import datetime
import time
import inspect

# print os.path.realpath(__file__)
# print inspect.stack()[0][1] 
# print inspect.getfile(inspect.currentframe()) # script filename (usually with path)
dir= os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory

now=datetime.datetime.now()
date=now.strftime("%d_%m_%y")

f=open(date+'.txt',"a" )
hours=now.strftime("%H")
mins=now.strftime("%M")
secs=now.strftime("%S")

while  1 :
	now=datetime.datetime.now()
	hours=now.strftime("%H")
	mins=now.strftime("%M")
	secs=now.strftime("%S")
	total_secs=((int(hours)*60)+(int(mins)))*60 +int(secs)
	cpu=psutil.cpu_times()									
	total=0
	for i in cpu:
		total+=i
	cpu_usage=100-((cpu[3]/total)*100)
	VM=psutil.virtual_memory()
	f.write(str(total_secs)+" "+str(cpu_usage)+" "+str(VM[2])+"\n")
	time.sleep(1)
	if (hours == "23") and (mins =="38") and (secs == "59"):
		break
	
f.close
sys.argv=['send_report.py',date+".txt"]
execfile("send_report.py")
sleep(1)
execfile("system_load.py")
