import smtplib
import pyotp
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendEmail(message, toaddr, subject):
	fromaddr = "fcsgrp7@gmail.com"
	toaddr = toaddr
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = subject
	 
	
	body = message
	msg.attach(MIMEText(body, 'plain'))

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()

	server.login(fromaddr,"adgms111")

	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	return True
def OTPSend():
	# print("random")
	fromaddr = "fcsgrp7@gmail.com"
	toaddr = "mayank15056@iiitd.ac.in"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "OTP for banking"
	 
	totp = pyotp.TOTP('base32secret3232',interval=300)
	body = "Your OTP for the this banking session is " + totp.now()
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
	server.quit()
	return totp
def OTPVerify(user_otp):
	totp = pyotp.TOTP('base32secret3232',interval=300)
	otp_verification=totp.verify(user_otp)
	print(otp_verification)
	return otp_verification

