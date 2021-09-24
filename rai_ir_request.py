from bs4 import BeautifulSoup as bs4
import requests
import jdatetime
import solve_captchas_with_model
import time

def getTrackingDetails(carNumber):
    login = "Guest"
    password = "123"
    print(jdatetime.date.today())
    current_date = str(jdatetime.date.today())[2:].replace('-', '')
    # url_main = r"http://customers.rai.ir/Main/Main.asp"
    url_captcha = r"https://customers.rai.ir/Main/captcha.asp"
    url_check = r"https://customers.rai.ir/Main/check.asp"
    url_detailed_info = r"https://customers.rai.ir/Wagon_Info/Tracking/Details.asp?WagonNO=" + str(carNumber) + "&Date=" + str(current_date)
    image_captcha_file = 'captcha.bmp'

    str_class_bs4_tag = "<class 'bs4.element.Tag'>"
    html_fields = ['Id', 'CarNumber', 'TrainNumber', 'StationName', 'ArriveDate', 'ArriveTime', 'DepartDate', 'DepartTime', 'FromStation', 'DestStation']

    session = requests.Session()
    img_captcha_data = session.get(url_captcha, verify=False).content
    with open(image_captcha_file, 'wb') as handler:
        handler.write(img_captcha_data)

    captcha_text = solve_captchas_with_model.solve_captcha_from_file(image_captcha_file)
    response_check = session.post(url_check, data={'txtUserName': login, 'txtPassword': password, 'txtCaptcha': captcha_text, 'B1':'%E6%D1%E6%CF'}, timeout=(5, 30))

    json_answer_empty = [{}]
    if response_check.status_code == 200:
        response_detailed_info = session.get(url_detailed_info)
        response_detailed_info.encoding = 'windows-1256'
        if response_detailed_info.status_code = 200:
            full_answer = bs4(response_detailed_info.text, 'lxml')
            fathers  = full_answer.find_all(id='AutoNumber2')
            if (fathers):
                father = fathers[0]
                json_answer_list = []
                childs_counter = 0
                for first_child in father.children:
                    if childs_counter > 3:
                        if str(type(first_child)) == str_class_bs4_tag:
                            json_answer_dict = {}
                            field_order_position = 0
                            for second_child in first_child.children:
                                if str(type(second_child)) == str_class_bs4_tag:
                                    one_operation = bs4(str(second_child), 'lxml')
                                    wrapper = one_operation.find('font')
                                    value = wrapper.text.strip()
                                    json_answer_dict[html_fields[field_order_position]] = value
                                    field_order_position += 1
                            json_answer_list.append(json_answer_dict)
                    childs_counter += 1
                return str(json_answer_list)
            else:
                return str(json_answer_empty)
        else:
            return str(json_answer_empty)
    else:
        return str(json_answer_empty)

print(getTrackingDetails(52583077))
