# Monitors System Load   
The script monitors you system's load every hour and the data is recorded in a file. A new file is created everyday. At the end of the day the file is read and a graph is generated. The data along with the graph is then sent via mail. 

# How to run the script
* Change the file permission to make it executable
```
chmod +x system_load
```
* Edit the cron file
``` 
crontab -e
```
**And voila!!! The script will run every hour and send an automated mail at 2300hr.** 
