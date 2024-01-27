from app.main import bp
from flask import render_template, request, jsonify
from app.forms.form import RSVP_Form
from app.main.mail import Email_notifi
from app import limiter
import json, os, ast, datetime



@bp.route('/',methods=['GET'])
def index():
    no_guests = True
    form = RSVP_Form()
    return render_template('index.html', form=form, no_guests=no_guests)


@bp.route('/<url_str>', methods=['GET'])
def index_guests(url_str):
    guest_url_dict = ast.literal_eval(os.environ.get("guest_url_dict"))
    form = RSVP_Form()
    guest,one_guest,two_guests,multiple_guests,no_guests = None,None,None,None,None
    visiting_guests = [guest for key, guests in guest_url_dict.items() if str(key) == url_str for guest in guests]
    if len(visiting_guests) == 1:
        one_guest = True
        guest = visiting_guests[0]
        form.Field1.data = f"{guest}"
    elif len(visiting_guests) == 2:
        two_guests = visiting_guests
        form.Field1.data = f"{visiting_guests[0]} oraz {visiting_guests[1]}"
    elif len(visiting_guests) > 2:
        multiple_guests=visiting_guests
        form.Field1.data = f"{','.join(visiting_guests)}"
    else:
        no_guests = True 
    return render_template('index.html',form=form,guest=guest,one_guest=one_guest,two_guests=two_guests,multiple_guests=multiple_guests,no_guests=no_guests)

@bp.route('/process_form', methods=['POST'])
@limiter.limit("10 per minute")
def process_form():
    form = RSVP_Form(request.form)
    success_msg = "Dzięki, wszystko się udało :)"
    if form.validate():
        with open("answers.json", 'r+') as file:
            existing_data = json.load(file)
            answer = {
                "Guest":form.data.get("Field1"),
                "Edited":False,
                "Datetime":str(datetime.datetime.now()),
                "Answers":
                {
                "Field2":form.data.get("Field2"),
                "Field3":form.data.get("Field3"),
                "Field4":form.data.get("Field4")
                }
            }
            for index, dict in enumerate(existing_data):
                if dict['Guest'] == answer['Guest'] and dict['Answers'] == answer['Answers']:
                    error_msg = "Już mam tą odpowiedź ;)"
                    return jsonify({'message':error_msg,"success": False})
                elif dict['Guest'] == answer['Guest']:
                    success_msg = "Dzięki, wszystko się udało, zmieniłem odpowiedź :)"
                    existing_data[index]['Answers']['Field2'] = answer["Answers"]["Field2"]
                    existing_data[index]['Answers']['Field3'] = answer["Answers"]["Field3"]
                    existing_data[index]['Answers']['Field4'] = answer["Answers"]["Field4"]
                    existing_data[index]["Edited"] = True
                    existing_data[index]["Datetime"] = str(datetime.datetime.now())
                    file.seek(0)
                    json.dump(existing_data, file, indent=2)
                    file.truncate()
                    # email_object = Email_notifi(answer)
                    # email_object.send_message()
                    return jsonify({'message': success_msg, "success": True })
            existing_data.append(answer)
            file.seek(0)
            json.dump(existing_data, file, indent=2)
            file.truncate()
            # email_object = Email_notifi(answer)
            # email_object.send_message()
            return jsonify({'message': success_msg, "success": True })
    else:
        error_msg = "Nie wszystkie pola zostały uzupełnione"
        return jsonify({'message':error_msg,"success": False})
    

