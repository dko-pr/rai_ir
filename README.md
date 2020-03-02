# rai_ir
работа с сервисом customers.rai.ir
1) через Flask служба запускается на заданном ip и порту, принимая там http запросы вида:
http://10.10.200.24:21523/rai.ir/<номер вагона>
2) приняв запрос от клиента, служба, написанная на python3, пытается соединяться с удалённым хостом customers.rai.ir
а) сначала по адресу http://customers.rai.ir/Main/check.asp отправляются данные общедоступной гостевой учётки портала (логин: Guest, пароль: 123)
б) потом по адресу http://customers.rai.ir/Wagon_Info/Tracking/Details.asp происходит запрос дислокации вагона.
при этом задаётся период запроса - все операции с датой <= текущей по персидскому календарю (это обязательно, согласно их Api)
3) ответ получаем в виде html, который парсится библиотеками bs4 и lxml. подготавливается и передаётся json ответ клиенту, содержащий информацию о вагоне (или пустой json {[]}, если вагон не найден)
4) клиент должен этот ответ преобразовать из json в таблицу, поменять даты из персидского календаря в грегорианский, время из тегеранского в московское, названия станций на фарси перевести в коды станций. у нас это всё делается на sql с использованием некоторых доп. библиотек c#
5) служба устанавливается на отдельном debian хосте: 10.10.200.24 (подключение через putty: localadmin, пароль стандартный)
а) файлы размещаются в каталоге /home/localadmin/repository/rai_ir/ (я их закидываю туда, например, через свою отдельную git учётку)
б) служба сейчас настроена на автозапуск вместе с сервером и на авторестарт в случае своего падения и использованием системы демонов systemd.
в) один из файлов - конфигурация юнита: rai_ir.service. Если он менялся, то его надо скопировать в папку описаний сервисов, например, командой:
sudo cp /home/localadmin/repository/rai_ir/rai_ir.service /etc/systemd/system/
после чего надо перечитать список демонов:
sudo systemctl daemon-reload
г) лог службы (только для текущего запуска) можно посмотреть так:
sudo journalctl -u rai_ir
д) кстати, на всякий случай, оставлю тут команды для принудительной работы со службой:
sudo systemctl stop rai_ir
sudo systemctl start rai_ir
sudo systemctl enable rai_ir
ведь после изменения файлов надо перезапустить службу
