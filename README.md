# Monitors System Load   
The script monitors your system's load (CPU usage ,RAM usage,swap memory,ingress speed,egress speed,total processes,load average,read and write operations) every second and raw data is recorded in a file named raw.ds. At the end of the day the file is read . Multiple graphs are generated and average load per hour is calculated which is embedded in an email . Email report in tabular form along with graphs are generated according to the flags and time interval set in config.ini file.

# How to run the script
```
Just edit the cron file once and reboot.(Much less tedious I hope)
```
* Edit the root's cron file 
``` 
sudo crontab -e
```
* Contents of the cron file

``` 
@reboot /path/to/python /absolute/path/to/system_load.py
59 23 * * *  /path/to/python /absolute/path/to/system_load.py 
 ```

**And voila!!! The script will run continuously and mail will be sent!** 
