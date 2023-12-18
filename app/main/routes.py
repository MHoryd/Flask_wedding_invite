from app.main import bp
from flask import render_template, request, jsonify
from app.forms.form import RSVP_Form
from app.main.mail import Email_notifi
import json

url_dict ={123:['AAA','BBB'],345:['CCC','DDD']}


@bp.route('/',methods=['GET'])
def index():
    no_guests = True
    form = RSVP_Form()
    return render_template('index.html', form=form, no_guests=no_guests)


@bp.route('/<int:url_num>', methods=['GET'])
def index_guests(url_num):
    second_guest = None
    second_guest = None
    form = RSVP_Form()
    for url, names_list in url_dict.items():
        if int(url) == url_num:
            first_guest = names_list[0]
            second_guest = names_list[1]
    form.Pole1.data = f"{first_guest} and {second_guest}"
    return render_template('index.html', first_guest=first_guest,second_guest=second_guest, form=form)

@bp.route('/process_form', methods=['POST'])
def process_form():
    form = RSVP_Form(request.form)
    success_msg = "Dzięki, wszystko się udało :)"
    if form.validate():
        with open("answers.json", 'r+') as file:
            existing_data = json.load(file)
            answer = {
                "Goście":form.data.get("Pole1"),
                "Pole2":form.data.get("Pole2"),
                "Pole3":form.data.get("Pole3")
            }
            for i in existing_data:
                if i == answer:
                    error_msg = "Już mam tą odpowiedź ;)"
                    return jsonify({'message':error_msg,"success": False})
            existing_data.append(answer)
            file.seek(0)
            json.dump(existing_data, file, indent=2)
            file.truncate()
            print(answer)
            email_object = Email_notifi(answer)
            email_object.send_message()
        return jsonify({'message': success_msg, "success": True })
    else:
        error_msg = "Nie wszystkie pola zostały uzupełnione"
        return jsonify({'message':error_msg,"success": False})