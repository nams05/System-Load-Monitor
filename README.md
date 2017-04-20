# Monitors System Load   
The script monitors your system's load (CPU usage ,RAM usage,swap memory,ingress speed,egress speed,total processes,load average,read and write operations) every second and the data is recorded in a file. A new file is created everyday. At the end of the day the file is read and multiple graphs are generated. Average load per hour is calculated and sent with the graphs via mail. 

# How to run the script
```
Just edit the cron file once and reboot.(Much less tedious I hope)
```
* Edit the root's cron file 
``` 
sudo crontab -e
```
* Contents of the cron file

``` @reboot /path/to/python /absolute/path/to/system_load.py  ```

**And voila!!! The script will run continuously** 
