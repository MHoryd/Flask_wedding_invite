from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os


class Email_notifi():
    

    def __init__(self, form_data):
        self.sender = os.environ.get('Notification_email')
        self.receivers = os.environ.get('Notification_receivers_email').split(',')
        self.password = os.environ.get('Notification_pass')
        self.smtp_server = os.environ.get('Notification_smtp_server')
        self.form_data = form_data


    def send_message(self):
        print(self.receivers)
        for receiver in self.receivers:
            msg = MIMEMultipart()
            msg['From'] = self.sender
            msg['To'] = receiver
            msg['Subject'] = f"Odpowiedź z formularza ślubnego {datetime.now().date()}"
            body = str(self.form_data)
            msg.attach(MIMEText(body, 'plain'))
            try:
                server = SMTP(self.smtp_server)
                server.starttls()
                server.login(self.sender, self.password)
                server.sendmail(self.sender,receiver,msg.as_string())
                server.quit()
                # for testing purposes
                break
            except Exception as e:
                print(f"Error: Unable to establish an SMTP connection{datetime.now()}")
                print(e)