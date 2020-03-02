from bs4 import BeautifulSoup as bs4
import requests
import jdatetime

def getTrackingDetails(carNumber):
    login = "Guest"
    password = "123"
    current_date = str(jdatetime.date.today())[2:].replace('-', '')
    url_check = r"http://customers.rai.ir/Main/check.asp"
    url_detailed_info = r"http://customers.rai.ir/Wagon_Info/Tracking/Details.asp?WagonNO=" + str(carNumber) + "&Date=" + str(current_date)

    str_class_bs4_tag = "<class 'bs4.element.Tag'>"
    html_fields = ['Id', 'CarNumber', 'TrainNumber', 'StationName', 'ArriveDate', 'ArriveTime', 'DepartDate', 'DepartTime', 'FromStation', 'DestStation']

    session = requests.Session()
    session.post(url_check, data={'txtUserName': login, 'txtPassword': password})
    response = session.get(url_detailed_info)
    response.encoding = 'windows-1256'

    json_answer_empty = [{}]
    full_answer = bs4(response.text, 'lxml')
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
