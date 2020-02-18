from bs4 import BeautifulSoup as bs4
import requests
import jdatetime

def getTrackingDetails(carNumber):
    login = "Guest"
    password = "123"

    date = str(jdatetime.date.today())[2:].replace('-', '')
    url_check = r"http://customers.rai.ir/Main/check.asp"
    url_detailed_info = r"http://customers.rai.ir/Wagon_Info/Tracking/Details.asp?WagonNO=" + str(carNumber) + "&Date=" + str(date)

    str_class_bs4_tag = "<class 'bs4.element.Tag'>"

    session = requests.Session()
    session.post(url_check, data={'txtUserName': 'Guest', 'txtPassword': '123'})
    response = session.get(url_detailed_info)
    response.encoding = 'windows-1256'

    big_soup = bs4(response.text, 'lxml')
    fathers  = big_soup.find_all(id='AutoNumber2')
    if (fathers):
        father = fathers[0]
        list = []
        i = 0
        for first_child in father.children:
            if i > 3:
                if str(type(first_child)) == str_class_bs4_tag:
                    dict = {}
                    j=0
                    for second_child in first_child.children:
                        if str(type(second_child)) == str_class_bs4_tag:
                            small_soup = bs4(str(second_child), 'lxml')
                            font_tag = small_soup.find('font')
                            value = font_tag.text.strip()
                            if (j == 0):
                                dict['Id'] = value
                            elif (j == 1):
                                dict['CarNumber'] = value
                            elif (j == 2):
                                dict['TrainNumber'] = value
                            elif (j == 3):
                                dict['StationName'] = value
                            elif (j == 4):
                                dict['ArriveDate'] = value
                            elif (j == 5):
                                dict['ArriveTime'] = value
                            elif (j == 6):
                                dict['DepartDate'] = value
                            elif (j == 7):
                                dict['DepartTime'] = value
                            elif (j == 8):
                                dict['FromStation'] = value
                            elif (j == 9):
                                dict['DestStation'] = value
                            j+=1
                    list.append(dict)
            i+=1
        return str(list)
    else:
        return str([{}])
