# Monitors System Load   
The script monitors you system's load (Cpu usage ,RAM usage,swap memory,download speed,upload speed,uptime,total processes,load average,read and write operations) every second and the data is recorded in a file. A new file is created everyday. At the end of the day the file is read and multiple graphs are generated. Average load per hour is calculated and sent with the graphs via mail. 

# How to run the script
```
Just edit the crontab once and reboot.(Much less tedious I hope)
```
* Edit the root's cron file
``` 
sudo crontab -e
```
**And voila!!! The script will run continuously and send an automated mail at 2359 hr.** 
