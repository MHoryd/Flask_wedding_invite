from datetime import datetime
import os,requests


class Email_notifi():
    

    def __init__(self, form_data):
        self.sender = os.getenv('Notification_email')
        self.receivers = os.getenv('Notification_receivers_email').split(',')
        self.password = os.getenv('Notification_pass')
        self.form_data = form_data
        self.url = os.getenv('Notification_api_url')


    def send_message(self):
        for receiver in self.receivers:
            try:
                request = requests.post(
                    self.url,
                    auth=("api",f"{self.password}"),
                    data={
                        "from":f'Wedding {self.sender}',
                        "to":[receiver],
                        "subject":f"Odpowiedź z formularza ślubnego {datetime.now().date()}",
                        "text":self.format_message()
                        })
                request.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(e)


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