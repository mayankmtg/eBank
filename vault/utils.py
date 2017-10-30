import smtplib
import pyotp
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def OTPSend(to_addr, OTP):
	fromaddr = "fcsgrp7@gmail.com"
	toaddr=to_addr
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "OTP for Vault Bank"
	 
	# totp = pyotp.TOTP('base32secret3232',interval=300)

	body = "Your OTP for the this banking session is " +OTP
	msg.attach(MIMEText(body, 'plain'))

	server = smtplib.SMTP('smtp.gmail.com', 587)

	#'------call to starttls() before you login:---------------------'
	server.ehlo()
	server.starttls()

	#------------Next, log in to the server--------------------------
	server.login(fromaddr,"adgms111")

	#----------Send the mail-----------------------------------------
	# msg = "Hello!"

	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	
	# otp_verification=totp.verify(user_otp)
	server.quit()
def OTP(to_addr):
	totp = pyotp.TOTP('base32secret3232',interval=300)
	OTPSend(to_addr, totp.now())
	
