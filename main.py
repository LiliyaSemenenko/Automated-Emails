from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders

import ssl
import smtplib


email_sender = '@example.com'
email_password = 'somepass'  # a generated app password from your Google account

email_receiver = '@example.com'

subject = 'Email with attachment'
body = 'Please find attached the Hello.'

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

em.add_alternative(body, subtype='html')

context = ssl.create_default_context()


with open('Hello.pdf', 'rb') as attachment_file:
    file_data = attachment_file.read()
    file_name = attachment_file.name.split('/')[-1]
    file_type = file_name.split('.')[-1]

attachment = MIMEBase('application', 'octet-stream')
attachment.set_payload(file_data)
encoders.encode_base64(attachment)
attachment.add_header('Content-Disposition', 'attachment', filename='Hello.pdf')
em.attach(attachment)

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
