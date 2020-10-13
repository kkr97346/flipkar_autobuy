# import required libraries 
import imaplib 
import email 
from email.header import decode_header 
import webbrowser 
import re

def Gmail_Otp(username,password):
	imap = imaplib.IMAP4_SSL("imap.gmail.com") 
	imap.login(username, password) 

	# Use "[Gmail]/Sent Mails" for fetching 
	imap.select('"[Gmail]/All Mail"', 
	readonly = True) 

	response, messages = imap.search(None, 'UnSeen') 
	messages = messages[0].split() 

		# take it from last 
	latest = int(messages[-1]) 

	for i in range(latest, latest-1, -1): 
		# fetch 
		res, msg = imap.fetch(str(i), "(RFC822)") 
			
		for response in msg: 
			if isinstance(response, tuple): 
				msg = email.message_from_bytes(response[1]) 
				# print required information 
				otp = (msg["Subject"]) 

	try:
		res = (re.search('\d{6}',otp))
		emailotp = (res.group())
		return emailotp
	except:
		return print("otp problem")