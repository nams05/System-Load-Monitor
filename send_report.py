import smtplib
import os
import time;
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

os.system('top -b -n1 > top.txt')

localtime = time.asctime( time.localtime(time.time()) )

#compose the message
fromaddr = "youremail@gmail.com"
toaddr = "toemail@gmail.com"
cc="someone@gmail.com"
bcc="somebody@gmail.com"
rcpt=[bcc] +[cc] + [toaddr]
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Bcc'] = bcc 
msg['Subject'] = "Report : " + localtime

f = open('top.txt')
Lines=f.readlines()
body = Lines[0]+ Lines[1]+ Lines[2]+ Lines[3]
f.close()
msg.attach(MIMEText(body, 'plain')) #attach body to MIME msg

#create SMTP object for connection
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.ehlo()

#Next, log in to the server
server.login("youremail@gmail.com", "password")

text=msg.as_string() #object to string
#Send the mail
server.sendmail(fromaddr, rcpt, text)