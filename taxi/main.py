import datetime
import time

from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import *
import sys
import psycopg2
from pyqt5_plugins.examplebutton import QtWidgets
from pyqt5_plugins.examplebuttonplugin import QtGui

import sql


class MainWindow(QMainWindow):
    dbname = "db"
    dbhost = "localhost"
    directorName = "director"
    directorPassword = "director"
    managerName = "manager"
    managerPassword = " manager "
    fields = {
        "client": ["id", "name", "phone_number"],
        "employee": ["id", "name", "birthday_date"],
        "requests": ["id", "client_id", "name_manager", "start_date", "end_date", "car_type", "quantity"],
        "car_accessories": ["name", "cost"],
        "contracts": ["id", "requests_id", "cost"],
        "car": ["id", "car_number", "car_model", "car_color", "car_cost", "is_available"]
    }
    sqls_add = {
        "client": sql.SQL_ADD_CLIENT,
        "employee": sql.SQL_ADD_STUFF,
        "requests": sql.SQL_ADD_REQUEST,
        "car_accessories": sql.SQL_ADD_CAR_ACCESSORS,
        "contracts": sql.SQL_ADD_CONTRACTS,
        "car": sql.SQL_ADD_CAR
    }

    choice_fields = {
        "car_type": "car",
        "requests_id": "requests",
        "requisites": "client",
        "name_manager": "employee",
        "contract_data": "requests",
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_cursors()
        self.setupUi()

    def init_cursors(self):
        self.conn_director = psycopg2.connect(dbname=self.dbname, user=self.directorName,
                                              password=self.directorPassword, host=self.dbhost)
        self.directorCursor = self.conn_director.cursor()
        self.conn_manager = psycopg2.connect(dbname=self.dbname, user=self.managerName,
                                             password=self.managerPassword, host=self.dbhost)

        self.managerCursor = self.conn_manager.cursor()

    def setupUi(self):
        self.setWindowTitle("Car rental")
        self.move(300, 300)
        self.resize(600, 450)
        self.show_start()

    def init_widgets(self):
        self.main_widget = QWidget(self)
        self.main_widget.resize(600, 400)
        self.main_widget.show()
        self.list_widget = QWidget(self)
        self.list_widget.resize(600, 400)
        self.list_widget.hide()
        self.director_widget = QWidget(self)
        self.director_widget.resize(600, 400)
        self.director_widget.hide()
        self.manager_widget = QWidget(self)
        self.manager_widget.resize(600, 400)
        self.manager_widget.hide()
        self.get_widget = QWidget(self)
        self.get_widget.resize(600, 400)
        self.get_widget.hide()
        self.rem_widget = QWidget(self)
        self.rem_widget.resize(600, 400)
        self.rem_widget.hide()
        self.report_widget = QWidget(self)
        self.report_widget.resize(600, 400)
        self.report_widget.hide()
        self.costByRequest_widget = QWidget(self)
        self.costByRequest_widget.resize(600, 400)
        self.costByRequest_widget.hide()
        self.get_manager_widget = QWidget(self)
        self.get_manager_widget.resize(600, 400)
        self.get_manager_widget.hide()
        self.carInfo_widget = QWidget(self)
        self.carInfo_widget.resize(600, 400)
        self.carInfo_widget.hide()
        self.add_widget = QWidget(self)
        self.add_widget.resize(600, 400)
        self.add_widget.hide()

        self.resetBtn = QPushButton("В начало", self)

        self.resetBtn.resize(100, 30)
        self.resetBtn.move(450, 400)
        self.resetBtn.clicked.connect(self.event_reset)
        self.resetBtn.show()

    def show_start(self):

        self.init_widgets()
        if not self.main_widget.children():
            self.lbl = QLabel('Авторизуйтесь', self.main_widget)
            self.lbl.resize(120, 30)
            self.lbl.move(250, 0)
            self.btn1 = QPushButton("Директор", self.main_widget)
            self.btn1.resize(100, 30)
            self.btn1.move(250, 30)
            self.btn2 = QPushButton("Менеджер", self.main_widget)
            self.btn2.resize(100, 30)
            self.btn2.move(250, 70)
            self.btn1.clicked.connect(self.event_auth)
            self.btn2.clicked.connect(self.event_auth)
        self.main_widget.show()

    def show_list(self):
        if not self.list_widget.children():
            self.dirShowClients = QPushButton("Клиенты", self.list_widget)
            self.dirShowRequests = QPushButton("Заявки", self.list_widget)
            self.dirShowContracts = QPushButton("Договоры", self.list_widget)
            self.dirShowCars = QPushButton("Автомобили", self.list_widget)
            self.dirShowStuff = QPushButton("Сотрудники", self.list_widget)
            self.dirShowAccessories = QPushButton("Аксессуары", self.list_widget)

            for n, child in enumerate(self.list_widget.children()):
                child.resize(100, 30)
                child.move(100 * n, 20)
            self.add_events(self.list_widget)
            self.get_table = QTableWidget(self.list_widget)
            self.get_table.resize(600, 370)
            self.get_table.move(0, 60)

        self.list_widget.show()

    def director_list(self):
        if not self.director_widget.children():
            self.directorBtnCar = QPushButton("Добавить автомобиль", self.director_widget)
            self.directorBtnCarRemove = QPushButton("Удалить автомобиль", self.director_widget)
            self.directorBtnStuff = QPushButton("Добавить сотрудника", self.director_widget)
            self.directorBtnStuffRemove = QPushButton("Удалить сотрудника", self.director_widget)
            self.directorBtnAccessories = QPushButton("Добавить аксессуар", self.director_widget)
            self.directorBtnAccessoriesRemove = QPushButton("Удалить аксессуар", self.director_widget)
            self.directorBtnInfo = QPushButton("Сформировать отчет", self.director_widget)
            self.directorBtnCarInfo = QPushButton("Отчет по машине",
                                                  self.director_widget)
            self.directorBtnGetManager = QPushButton(
                "ФИО менеджера, оформлявшего заявку с клиентом", self.director_widget)
            self.directorBtnInfo = QPushButton("Получить справочную информацию", self.director_widget)

            self.add_events(self.director_widget)
        self.print_vertical(self.director_widget)

    def manager_list(self):
        if not self.manager_widget.children():
            self.managerBtnClients = QPushButton("Добавить клиента", self.manager_widget)
            self.managerBtnClientsRemove = QPushButton("Удалить клиента", self.manager_widget)
            self.managerBtnRequests = QPushButton("Добавить заявку", self.manager_widget)
            self.managerBtnRequestsRemove = QPushButton("Удалить заявку", self.manager_widget)
            self.managerBtnContracts = QPushButton("Добавить договор", self.manager_widget)
            self.managerBtnContactsRemove = QPushButton("Удалить договор", self.manager_widget)
            self.managerBtnInfo = QPushButton("Получить справочную информацию", self.manager_widget)
            self.managerBtnCostByRequest = QPushButton("Счёт за прокат автомобиля", self.manager_widget)
            self.add_events(self.manager_widget)

        self.print_vertical(self.manager_widget)

    def add_events(self, widget):
        for button in widget.children():
            text_split = button.text().split()
            if text_split[-1] == "отчет":
                event = self.report_event
            elif text_split[-1] == "автомобиля":
                event = self.costByRequest_event
            elif text_split[0] == "ФИО":
                event = self.get_manager_event
            elif text_split[-1] == "машине":
                event = self.carInfo_event
            elif len(text_split) == 3:
                event = self.event_info
            elif len(text_split) == 2:
                event = {"Добавить": self.add_event, "Удалить": self.remove_event}[text_split[0]]
            elif len(text_split) == 1:
                event = self.get_event
            else:
                print(text_split, "error")
                continue
            button.clicked.connect(self.decorator(event))
    def decorator(self, func):
        def func2():
            try:
                func()
            except:
                QMessageBox.critical(self, "Ошибка ", "Данные введены некорректно", QMessageBox.Ok)
        return func2

    def event_auth(self):
        sender = self.sender()
        self.refresh()
        self.role = sender.text()
        if self.role == "Менеджер":
            self.manager_list()
        else:
            self.director_list()

    def carInfo_event(self):
        self.refresh()
        if not any([i for i in self.carInfo_widget.children() if type(i) == QTableWidget]):
            self.carInfo_get_table = QTableWidget(self.carInfo_widget)
            self.carInfo_get_table.resize(500, 200)
            self.carInfo_get_table.move(50, 130)
        self.carInfo_lbl = QLabel("Выберите машину", self.carInfo_widget)
        self.carInfo_lbl.resize(500, 30)
        self.carInfo_lbl.move(50, 30)
        self.carInfo_box = QComboBox(self.carInfo_widget)
        self.carInfo_box.resize(500, 30)
        self.carInfo_box.move(50, 60)
        cursor = self.get_cursor()
        cursor.execute(sql.SQL_GET.format("car"))
        cars = cursor.fetchall()
        for car in cars:
            self.carInfo_box.addItem(car[2] + ", " + car[1], {"value": car[0]})
        self.carInfo_btn = QPushButton("Получить список клиентов, бравших эту машину на прокат", self.carInfo_widget)
        self.carInfo_btn.resize(500, 30)
        self.carInfo_btn.move(50, 100)

        self.carInfo_btn.clicked.connect(self.carInfo_get_event)
        self.carInfo_widget.show()

    def carInfo_get_event(self):
        car_id = self.carInfo_box.currentData()["value"]
        cursor = self.get_cursor()
        cursor.execute(sql.SQL_GET_INFO_BY_CAR.format(car_id))
        clients = cursor.fetchall()
        self.carInfo_get_table.setRowCount(len(clients))
        self.carInfo_get_table.setColumnCount(2)
        print(clients)
        for row, client in enumerate(clients):
            for column, field in enumerate(client):
                cell = QTableWidgetItem(field)
                self.carInfo_get_table.setItem(row, column, cell)
        self.carInfo_get_table.resizeColumnsToContents()
        self.carInfo_get_table.show()

    def get_manager_event(self):
        self.refresh()

        self.get_manager_box = QComboBox(self.get_manager_widget)
        self.get_manager_box.resize(500, 30)
        self.get_manager_box.move(50, 100)
        cursor = self.get_cursor()
        cursor.execute(
            """SELECT DISTINCT c.id, c.client_name from requests r left join client c on r.requisites =c.id;""")
        clients = cursor.fetchall()
        for client in clients:
            self.get_manager_box.addItem(client[1], {"value": client[0]})
        self.get_manager_btn = QPushButton("Установить ФИО менеджера", self.get_manager_widget)
        self.get_manager_btn.resize(300, 30)
        self.get_manager_btn.move(150, 140)
        self.get_manager_btn.clicked.connect(self.get_manager_result_event)
        if not any([x for x in self.get_manager_widget.children() if type(x) == QLabel]):
            self.get_manager_lbl = QLabel(
                "Выберите клиента, для которого хотите установить ФИО менеджера,\nоформлявшего заявку",
                self.get_manager_widget)
            self.get_manager_lbl.resize(500, 40)
            self.get_manager_lbl.move(50, 50)
            self.get_manager_lbl_answer = QLabel("", self.get_manager_widget)
            self.get_manager_lbl_answer.resize(500, 50)
            self.get_manager_lbl_answer.setStyleSheet("font-size:19pt; font-weight:400;")
            self.get_manager_lbl_answer.move(50, 250)
        self.get_manager_widget.show()

    def get_manager_result_event(self):
        id_client = self.get_manager_box.currentData()["value"]
        cursor = self.get_cursor()
        cursor.execute(sql.SQL_GET_MANAGER_WITH_REQUEST.format(id_client))
        manager = cursor.fetchone()
        self.get_manager_lbl_answer.setText(f"{manager[0]}")

    def event_info(self):
        self.refresh()
        self.show_list()

    def get_event(self):
        sender = self.sender()
        for child in self.list_widget.children():
            if type(child) != QPushButton:
                continue
            child.setStyleSheet("background-color : white")
            if child.text() == sender.text():
                child.setStyleSheet("background-color : yellow")
        cursor = self.get_cursor()
        obj = self.get_object_of_phrase(sender.text())
        cursor.execute(sql.SQL_GET.format(obj))
        result = cursor.fetchall()
        self.get_table.setRowCount(len(result))
        if len(result) > 0:
            self.get_table.setColumnCount(len(result[0]))
        else:
            self.get_table.setColumnCount(0)
        for n, name in enumerate(self.fields[obj]):
            self.get_table.setHorizontalHeaderItem(n, QTableWidgetItem(name))
        self.get_table.resize(600, 340)
        self.get_table.move(0, 60)
        for x in range(len(result)):
            for y in range(len(result[x])):
                cell = QTableWidgetItem(str(result[x][y]))
                self.get_table.setItem(x, y, cell)
        self.get_table.resizeColumnsToContents()
        self.list_widget.update()

    def add_event(self):
        self.refresh()
        sender = self.sender()
        obj = self.get_object_of_phrase(sender.text())
        fields = self.fields[obj]
        self.addFields = []
        self.lblFields = []
        self.current_obj = obj
        for n, field in enumerate(fields):
            lbl = QLabel(field, self.add_widget)
            if field in self.choice_fields:
                inp_field = QComboBox(self.add_widget)
                cursor = self.get_cursor()
                if "requests" == self.choice_fields[field]:
                    cursor.execute(sql.SQL_GET_REQUEST_INFO)
                    lines = cursor.fetchall()
                    for num in range(len(lines)):
                        el = lines[num]
                        lines[num] = (el[0], "Клиент: " + el[1], "Менеджер: " + el[2], el[3], el[4])
                elif "car" == self.choice_fields[field]:
                    cursor.execute(sql.SQL_GET_FREE_CARS)
                    lines = cursor.fetchall()
                elif "employee" == self.choice_fields[field]:
                    cursor.execute(sql.SQL_GET.format(self.choice_fields[field]))
                    lines = cursor.fetchall()
                    lines = [line[:-1] for line in lines]
                else:
                    cursor.execute(sql.SQL_GET.format(self.choice_fields[field]))
                    lines = cursor.fetchall()

                for line in lines:
                    inp_field.addItem(", ".join([str(i) for i in line[1:]]), {"value": line[0]})
            else:
                inp_field = QLineEdit(self.add_widget)
            if field == "id":
                cursor = self.get_cursor()
                cursor.execute(sql.SQL_GET_MAX_ID.format(obj))
                id_field = cursor.fetchone()
                inp_field.setText(str(1 + int(id_field[0])))

                inp_field.setEnabled(False)
            lbl.resize(110, 30)
            lbl.move(30, n * 40 + 20)
            inp_field.resize(300, 30)
            inp_field.move(140, n * 40 + 20)
            self.lblFields.append(lbl)
            self.addFields.append(inp_field)
        self.add_btn = QPushButton("Создать", self.add_widget)
        self.add_btn.resize(100, 30)
        self.add_btn.move(450, 50)
        self.add_btn.clicked.connect(self.decorator(self.new_item_event))
        self.add_widget.show()

    def remove_event(self):
        sender = self.sender()

        self.refresh()
        cursor = self.get_cursor()
        obj = self.get_object_of_phrase(sender.text())
        if "requests" == obj:
            cursor.execute(sql.SQL_GET_REQUEST_INFO)
            result = cursor.fetchall()
            for num in range(len(result)):
                el = result[num]
                result[num] = (el[0], "Клиент: " + el[1], "Менеджер: " + el[2], el[3], el[4])
        elif obj == "contracts":
            cursor.execute(sql.SQL_GET_CONTRACT_INFO)
            result = cursor.fetchall()
        else:
            cursor.execute(sql.SQL_GET.format(obj))
            result = cursor.fetchall()

        self.current_obj = obj

        self.rem_box = QComboBox(self.rem_widget)
        self.rem_box.resize(420, 30)
        self.rem_box.move(100, 100)
        self.rem_btn = QPushButton("Удалить", self.rem_widget)
        self.rem_btn.clicked.connect(self.delete_item_event)
        self.rem_btn.resize(100, 30)
        self.rem_btn.move(100, 150)

        self.remove_btns = []
        for x in range(len(result)):
            cell = ", ".join([str(i) for i in result[x]])
            self.rem_box.addItem(cell, {"value": result[x][0]})
        self.rem_widget.show()

    def report_event(self):
        self.refresh()
        cursor = self.get_cursor()
        time_range = (datetime.datetime.now() - datetime.timedelta(30), datetime.datetime.today())
        cursor.execute(
            sql.SQL_GET_REPORT.format(*time_range))
        report = cursor.fetchone()
        cursor.execute(sql.SQL_CARS_FOR_RANGE.format(*time_range))
        cars = cursor.fetchall()
        cursor.execute(sql.SQL_GET_PROFIT_FOR_RANGE.format(*time_range))
        profit = cursor.fetchone()
        self.lbl_report = QLabel(
            f"Месяц {datetime.datetime.strftime(time_range[0], '%Y/%m/%d')} - {datetime.datetime.strftime(time_range[1], '%Y/%m/%d')}\nОформлено заявок за месяц: " + str(
                report[0]), self.report_widget)
        self.lbl_report.resize(500, 40)
        self.lbl_report.move(10, 10)
        self.table_report = QTableWidget(self.report_widget)

        self.table_report.resize(600, 300)
        self.table_report.move(0, 100)
        self.table_report.setRowCount(len(cars))

        if len(cars) > 0:
            self.table_report.setColumnCount(2)
        for n, name in enumerate(["Number", "Model"]):
            self.table_report.setHorizontalHeaderItem(n, QTableWidgetItem(name))
        for x in range(len(cars)):
            for y in range(len(cars[x])):
                cell = QTableWidgetItem(str(cars[x][y]))
                self.table_report.setItem(x, y, cell)
        self.table_report.show()

        self.table_report.resizeColumnsToContents()
        self.lbl_profit_report = QLabel(
            "Заработано: " + str(profit[0]) + "\n\nАвтомобили, которые были взяты на прокат:", self.report_widget)
        self.lbl_profit_report.resize(500, 70)
        self.lbl_profit_report.move(10, 35)
        self.report_widget.show()

    def costByRequest_event(self):
        self.refresh()
        cursor = self.get_cursor()
        cursor.execute(sql.SQL_GET_REQUEST_INFO)
        requests = cursor.fetchall()

        self.costByRequestBox = QComboBox(self.costByRequest_widget)
        self.costByRequestBox.resize(580, 30)
        self.costByRequestBox.move(10, 50)
        for r in requests:
            self.costByRequestBox.addItem(str(r[1]), {"value": r[0]})
        # self.costByRequestBox.setCurrentIndex(self.costByRequestBox.currentData()["value"])
        self.costByRequestBtn = QPushButton("Посчитать", self.costByRequest_widget)
        self.costByRequestBtn.resize(150, 40)
        self.costByRequestBtn.move(225, 90)
        self.costByRequestBtn.clicked.connect(self.show_costByRequest_event)
        if not any([x for x in self.costByRequest_widget.children() if type(x) == QLabel]):
            self.lbl_costByRequest_title = QLabel("Выберите клиента, для которого хотите выставить счёт",
                                                  self.costByRequest_widget)
            self.lbl_costByRequest_title.resize(500, 30)
            self.lbl_costByRequest_title.move(100, 10)
            self.lbl_costByRequest = QLabel("", self.costByRequest_widget)
            self.lbl_costByRequest.setStyleSheet("font-size:19pt; font-weight:400;")

            self.lbl_costByRequest.resize(600, 300)
            self.lbl_costByRequest.move(20, 130)
        self.costByRequest_widget.show()

    def show_costByRequest_event(self):
        print(self.costByRequestBox.currentData()["value"])
        cursor = self.get_cursor()

        cursor.execute(sql.SQL_GET_COST_BY_REQUEST.format(self.costByRequestBox.currentData()["value"]))
        res = cursor.fetchone()
        text = ""
        if res is not None:
            for line, desc in zip(res, ["request_id", "Manager", "Client", "Car model", "Car number", "Total"]):
                text += str(desc) + ": " + str(line) + "\n"
        self.lbl_costByRequest.setText(text)
        self.costByRequest_widget.show()

    def event_reset(self):
        self.refresh()
        self.main_widget.show()

    def get_object_of_phrase(self, phrase):
        phrase_split = phrase.split()
        if len(phrase_split) in [1, 2]:
            return {"клиент": "client", "заявк": "requests", "договор": "contracts", "автомобил": "car",
                    "догово": "contracts", "сотрудник": "employee",
                    "аксессуар": "car_accessories",
                    "аксессуа": "car_accessories"}[phrase_split[-1][:-1].lower()]  # удаляем окончание
        print(phrase, phrase_split)

        return "err"

    def new_item_event(self):
        sender = self.sender()
        args = [i.text() if type(i) == QLineEdit else i.currentData()["value"] for i in self.addFields]
        cursor = self.get_cursor()
        sql_c = self.sqls_add[self.current_obj]
        print(sql_c)
        cursor.execute(sql_c.format(*args))
        self.get_conn().commit()
        self.event_reset()

    def delete_item_event(self):
        sender = self.sender()
        id_item = self.rem_box.currentData()["value"]

        cursor = self.get_cursor()
        if self.current_obj == "requests":
            cursor.execute(
                f"UPDATE car set is_available=TRUE WHERE id= (select car_type from car_requests where requests_id={id_item});")
        if self.current_obj == "car_accessories":
            cursor.execute(f"""DELETE FROM car_accessories WHERE accessories_name = '{id_item}'; """)

        else:
            cursor.execute(sql.SQL_DELETE.format(self.current_obj, id_item))

        self.get_conn().commit()
        self.event_reset()

    def get_conn(self):
        if self.role == "Менеджер":
            return self.conn_manager
        return self.conn_director

    def get_cursor(self):
        if self.role == "Менеджер":
            return self.managerCursor
        return self.directorCursor

    def refresh(self):
        self.main_widget.hide()
        self.list_widget.hide()
        self.director_widget.hide()
        self.manager_widget.hide()
        self.get_widget.hide()
        self.add_widget.hide()
        self.rem_widget.hide()
        self.report_widget.hide()
        self.costByRequest_widget.hide()
        self.get_manager_widget.hide()
        self.carInfo_widget.hide()
        for child in self.add_widget.children():
            child.hide()

    def print_vertical(self, widget):
        for n, child in enumerate(widget.children()):
            child.resize(200, 50)
            if n >= 6:
                child.resize(450, 40)
                child.move(75, n * 50 - 100)
            else:
                child.move(75 + 250 * (n % 2), (n // 2) * 60 + 20)

        widget.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.managerCursor.close()
        self.directorCursor.close()
        self.conn_director.close()
        self.conn_manager.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
