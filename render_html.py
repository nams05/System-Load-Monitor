import sys
import datetime

#function to define color code of rows
def color(cpu):
	if(cpu<=10):
		return "#FDB22B"
	elif(cpu<=20):
		return "#F00088"
	elif(cpu<=30):
		return "#2A58C3"
	elif(cpu<=40):
		return "#94D301"
	elif(cpu<=50):
		return "#8408BA"
	elif(cpu<=60):
		return "#01A5AD"
	elif(cpu<=70):
		return "#FF7C03"
	elif(cpu<=80):
		return "#B2C300"
	elif(cpu<=90):
		return "#AEB18C"
	else:
		return "#01A5AD"	

now=datetime.datetime.now()
date=now.strftime("%d_%m_%y")

html='''<!DOCTYPE html>
<html>
<head>
	<style type="text/css">
		table {
    	border-spacing: 5px;
    	width:60%;
    	}
		th{
		background-color: black;
    	color: white;
		}
		table, th, td {

    	border: 2px solid black;
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

	</style>
</head>
<body>

		<table>
			<caption>System Load</caption>
			<tr><th>Time(hr)</th><th>CPU Usage(%)</th><th>RAM Usage(%)</th></tr>
'''
total_memory=3758412.0
i=0
with open(sys.argv[1]) as f:
	content= f.read().split()
	for i in range(0,len(content),3):
		ram=((float(content[i+2]))/total_memory)*100.
		html+="<tr style=\"background-color:"+color(ram)+"\"><td>"+str(content[i])+"</td><td>"+str(content[i+1])+"</td><td>"+str(ram)+"</td></tr>"
html+="</table><img src=\""+date+'_graph.png'+"\"></body></html>"
