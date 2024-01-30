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
        for receiver in self.receivers:
            msg = MIMEMultipart()
            msg['From'] = self.sender
            msg['To'] = receiver
            msg['Subject'] = f"Odpowiedź z formularza ślubnego {datetime.now().date()}"
            body = self.format_message()
            msg.attach(MIMEText(body, 'plain'))
            try:
                server = SMTP(self.smtp_server)
                server.starttls()
                server.login(self.sender, self.password)
                server.sendmail(self.sender,receiver,msg.as_string())
                server.quit()
            except Exception as e:
                print(f"Error: Unable to establish an SMTP connection{datetime.now()}")
                print(e)
            break


    def format_message(self):
        question_dict ={
            'Will_attend':"Czy się pojawi",
            'Contact_email':'Email',
            'Alimentary_exclusion':"Wykluczenia żywieniowe",
            'Comment':"Komentarz",
            'Main_dish_details':"Szczegóły głównego dania",
            "Main_dish_details_for_main_guest":"Szczegóły głównego dania, jeden gość",
            "accompanying_person":"Czy będzie osoba towarzysząca",
            "accompanying_person_details":"Szczegóły osoby towarzyszącej",
            "Main_dish_details_first_guest":"Danie główne dla pierwszego gościa",
            "Main_dish_details_second_guest":"Danie główne dla drugiego gościa",
            "Main_dish_details_third_guest":"Danie główne dla trzeciego gościa",
            "Main_dish_details_fourth_guest":"Danie główne dla czwartego gościa"
        }
        mesage_string = f"Gość: {self.form_data['Guest']}\nEdytowano: {self.form_data['Edited']}\nData ostatniej edycji: {self.form_data['Datetime']}\nOdpowiedzi:\n"
        for question,answer in self.form_data['Answers'].items():
            mesage_string += f"Pytanie: {question_dict[question]}. Odpowiedź: {answer}\n"
        return mesage_string