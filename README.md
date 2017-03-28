# Monitors System Load   
The script monitors you system's load every hour and the data is recorded in a file. A new file is created everyday. At the end of the day the file is read and a graph is generated. The data along with the graph is then sent via mail. 

# How to run the script
* Change the file permissions of the file to execute it
```
chmod 755 system_load
```
* Edit the crontab
``` 
crontab -e
```
*** And voila!!! The script will run every hour and send an automated mail at 2300hr. 
