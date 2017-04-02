# Monitors System Load   
The script monitors you system's load every second and the data is recorded in a file. A new file is created everyday. At the end of the day the file is read and a graph is generated. Average load per hour is calculated and sent with the graph via mail. 

# How to run the script
```
python /path/to/the/file/system_load.py
```
* Edit the root's cron file
``` 
sudo crontab -e
```
**And voila!!! The script will run continuously and send an automated mail at 2359 hr.** 
