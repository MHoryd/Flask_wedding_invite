from app.main import bp
from flask import render_template, request, jsonify
from app.forms.form import AnonymForm,OneGuestForm,TwoGuestForm, MultipeGuestForm
from app.main.mail import Email_notifi
from app import limiter
import json, os, ast, datetime



@bp.route('/',methods=['GET'])
def index():
    no_guests = True
    form = AnonymForm()
    return render_template('index.html', form=form, no_guests=no_guests)


@bp.route('/<url_str>', methods=['GET'])
def index_guests(url_str):
    guest_url_dict = ast.literal_eval(os.getenv("guest_url_dict"))
    guest,one_guest,two_guests,multiple_guests,no_guests = None,None,None,None,None
    visiting_guests = [guest for key, guests in guest_url_dict.items() if str(key) == url_str for guest in guests]
    if len(visiting_guests) == 0:
        no_guests = True
        form = AnonymForm()
    if len(visiting_guests) == 1:
        form = OneGuestForm()
        one_guest = True
        guest = visiting_guests[0]
        form.base_form.Field1.data = f"{guest}"
    elif len(visiting_guests) == 2:
        form = TwoGuestForm()
        two_guests = visiting_guests
        form.base_form.Field1.data = f"{visiting_guests[0]} oraz {visiting_guests[1]}"
    elif len(visiting_guests) > 2:
        form = MultipeGuestForm()
        multiple_guests=visiting_guests
        form.base_form.Field1.data = f"{','.join(visiting_guests)}"
    else:
        no_guests = True 
    return render_template('index.html',form=form,guest=guest,one_guest=one_guest,two_guests=two_guests,multiple_guests=multiple_guests,no_guests=no_guests)

@bp.route('/process_form', methods=['POST'])
@limiter.limit("10 per minute")
def process_form():
    form_type = request.form['form_type']
    if form_type == 'AnonymForm':
        form = AnonymForm(request.form)
        answer = format_form_data(form.data,form_type)
    elif form_type == 'OneGuestForm':
        form = OneGuestForm(request.form)
        answer = format_form_data(form.data,form_type)
    elif form_type == 'TwoGuestForm':
        form = TwoGuestForm(request.form)
        answer = format_form_data(form.data,form_type)
    elif form_type == 'MultipeGuestForm':
        form = MultipeGuestForm(request.form)
        answer = format_form_data(form.data,form_type)
    form.base_form.csrf_token.data = request.form.get('csrf_token')
    if form.validate():
        response_msg = handle_json_data(answer,form_type)
        return jsonify(response_msg)
    else:
        error_msg = "Nie wszystkie pola zostały uzupełnione"
        return jsonify({'message':error_msg,"success": False})


def format_form_data(data, type):
    base_answer = {
                "Guest":data['base_form']['Field1'],
                "Edited":False,
                "Datetime":str(datetime.datetime.now()),
                "Answers":
                {
                "Will_attend":data['base_form'].get('Field2'),
                "Contact_email":data['base_form'].get('Field3'),
                "Alimentary_exclusion":data['base_form'].get('Field4'),
                "Comment":data['base_form'].get('Field9')
                }
            }
    if type == 'AnonymForm':
        base_answer["Answers"]["Main_dish_details"]=data.get("Field5")
    elif type == 'OneGuestForm':
        base_answer["Answers"]["Main_dish_details_for_main_guest"]=data.get("Field5")
        base_answer["Answers"]["accompanying_person"]=data.get("Field6")
        base_answer["Answers"]["accompanying_person_details"]=data.get("Field7")
    elif type == 'TwoGuestForm':
        base_answer["Answers"]["Main_dish_details_first_guest"]=data.get("Field5")
        base_answer["Answers"]["Main_dish_details_second_guest"]=data.get("Field6")
    elif type == 'MultipeGuestForm':
        base_answer["Answers"]["Main_dish_details_first_guest"]=data.get("Field5")
        base_answer["Answers"]["Main_dish_details_second_guest"]=data.get("Field6")
        base_answer["Answers"]["Main_dish_details_third_guest"]=data.get("Field7")
        base_answer["Answers"]["Main_dish_details_fourth_guest"]=data.get("Field8")
    return base_answer


def handle_json_data(answer,form_type):
    existing_data = load_existing_data()
    return save_data(existing_data,answer,form_type)
    

def load_existing_data():
    try:
        with open("answers.json", 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_data(existing_data, answer, type):
    success_msg = "Dzięki, wszystko się udało :)"
    for index, dict in enumerate(existing_data):
        if dict['Guest'] == answer['Guest'] and dict['Answers'] == answer['Answers']:
            error_msg = "Już mam tą odpowiedź ;)"
            return {'message':error_msg,"success": False}
        elif dict['Guest'] == answer['Guest']:
            success_msg = "Dzięki, wszystko się udało, zmieniłem odpowiedź :)"
            existing_data[index]["Edited"]=True
            existing_data[index]['Datetime']=str(datetime.datetime.now())
            existing_data[index]['Answers']['Will_attend'] = answer["Answers"]["Will_attend"]
            existing_data[index]['Answers']['Contact_email'] = answer["Answers"]["Contact_email"]
            existing_data[index]['Answers']['Alimentary_exclusion'] = answer["Answers"]["Alimentary_exclusion"]
            existing_data[index]['Answers']['Comment'] = answer["Answers"]["Comment"]
            if type == 'OneGuestForm':
                existing_data[index]["Answers"]["Main_dish_details_for_main_guest"]=answer["Answers"]["Main_dish_details_for_main_guest"]
                existing_data[index]["Answers"]["accompanying_person"]=answer["Answers"]["accompanying_person"]
                existing_data[index]["Answers"]["accompanying_person_details"]=answer["Answers"]["accompanying_person_details"]
            elif type == 'TwoGuestForm':
                existing_data[index]["Answers"]["Main_dish_details_first_guest"]=answer["Answers"]["Main_dish_details_first_guest"]
                existing_data[index]["Answers"]["Main_dish_details_second_guest"]=answer["Answers"]["Main_dish_details_second_guest"]
            elif type == 'MultipeGuestForm':
                existing_data[index]["Answers"]["Main_dish_details_first_guest"]=answer["Answers"]["Main_dish_details_first_guest"]
                existing_data[index]["Answers"]["Main_dish_details_second_guest"]=answer["Answers"]["Main_dish_details_second_guest"]
                existing_data[index]["Answers"]["Main_dish_details_third_guest"]=answer["Answers"]["Main_dish_details_third_guest"]
                existing_data[index]["Answers"]["Main_dish_details_fourth_guest"]=answer["Answers"]["Main_dish_details_fourth_guest"]
            elif type == 'AnonymForm':
                existing_data[index]['Answers']['Main_dish_details']=answer['Answers']['Main_dish_details']
            try:
                with open("answers.json",'w') as file:
                    json.dump(existing_data, file, indent=2)
            except:
                pass
            email_object = Email_notifi(existing_data[index])
            email_object.send_message()
            return {'message': success_msg, "success": True }
    try:
        with open("answers.json",'w') as file:
            existing_data.append(answer)
            json.dump(existing_data, file, indent=2)
    except:
        pass
    email_object = Email_notifi(answer)
    email_object.send_message()
    return {'message': success_msg, "success": True}


            
