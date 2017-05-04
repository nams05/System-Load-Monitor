#!/usr/bin/python
import psutil
import sys
import os
import datetime
import time
import inspect
import sets

# Global variables
diskstats_before=psutil.disk_io_counters()
netstats_before=psutil.net_io_counters(pernic=False)

def get_directory():
	return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

def check_directory_exists(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

## Functions for collecting System Metrics ##
def get_epoch_time():
	return int(time.time())

def get_cpu_usage():
	cpu_usage=psutil.cpu_percent(interval=None)
	load_avg=os.getloadavg()
	return cpu_usage,load_avg[0]

def get_memory_usage():
	VM=psutil.virtual_memory()
	return VM[2]

def get_swap_usage():
	swap=psutil.swap_memory()
	return swap[3]

def get_running_process():
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

def get_disk_usage():
	diskstats_after=psutil.disk_io_counters()
	global diskstats_before
	read_speed=float(diskstats_after[2]-diskstats_before[2])/1048576
	write_speed=float(diskstats_after[3]-diskstats_before[3])/1048576
	diskstats_before=diskstats_after
	return "{0:.2f}".format(read_speed),"{0:.2f}".format(write_speed)


def get_network_usage():
	netstats_after=psutil.net_io_counters(pernic=False)
	global netstats_before
	egress_speed=float(netstats_after[0]-netstats_before[0])/1048576
	ingress_speed=float(netstats_after[1]-netstats_before[1])/1048576
	netstats_before=netstats_after
	return "{0:.2f}".format(egress_speed),"{0:.2f}".format(ingress_speed)

def get_logged_in_users():
	users=psutil.users()
	usernames=set([])
	for i in range(0,len(users)):
		usernames.add(users[i][0])
	return list(usernames)

if __name__ == '__main__':
	while  1 :
		check_directory_exists(get_directory()+'/data')
		check_directory_exists(get_directory()+'/graph')
		## get system statistics
		epoch_time=get_epoch_time()
		cpu_usage,cpu_load_avg=get_cpu_usage()
		memory=get_memory_usage()
		swap=get_swap_usage()
		total_process,running_process,zombie_process=get_running_process()
		read_speed,write_speed=get_disk_usage()
		ingress_speed,egress_speed=get_network_usage()
		usernames=get_logged_in_users()

		## store it in a dictionary
		system_stats={
		'epoch':epoch_time,
		'cpu usage':cpu_usage,
		'cpu load avg':cpu_load_avg,
		'memory':memory,
		'swap':swap,
		'total process':total_process,
		'running process':running_process,
		'zombie process':zombie_process,
		'read speed':read_speed,
		'write speed':write_speed,
		'egress speed':egress_speed,
		'ingress speed':ingress_speed,
		'usernames':usernames
		}

		with open(get_directory()+'/data/raw.ds','a' ) as f:
			f.write(str(system_stats['epoch'])+" , "+str(system_stats['cpu usage'])+" , "+str(system_stats['cpu load avg'])+" , "+str(system_stats['memory'])+" , "+str(system_stats['swap'])+" , "+str(system_stats['total process'])+" , "+str(system_stats['running process'])+" , "+str(system_stats['zombie process'])+" , "+str(system_stats['read speed'])+" , "+str(system_stats['write speed'])+" , "+str(system_stats['egress speed'])+" , "+str(system_stats['ingress speed'])+" , "+str(system_stats['usernames'])+"\n")

		time.sleep(1)