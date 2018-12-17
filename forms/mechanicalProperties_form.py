# -*- coding: utf-8 -*-
# -----------------------------Импорт модулей-----------------------------------

from PyQt5 import QtSql

import os
import os.path
import shutil

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QTableWidget, QComboBox, \
    QSpinBox, QPushButton, QListWidgetItem, QLineEdit

# -----------------------------------Форма--------------------------------------

class mechanicalProperties_form_class(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.interface_lng_val = parent.interface_lng_val
        self.con = parent.con
        self.full_dir = parent.full_dir
        self.par = parent

        if self.con.open():

            table = QTableWidget(7, 2)
            table.setColumnWidth(0, 150)
            table.setColumnWidth(1, 230)
            table.setFixedSize(674, 480)
            table.setHorizontalHeaderLabels(["Параметр", "Значение"])
            # rho.type
            rho_type_lbl = QLabel('rho.type')
            self.rho_type = QComboBox()
            rho_type_list = ["uniform", "demo"]
            self.rho_type.addItems(rho_type_list)
            table.setCellWidget(0, 1, self.rho_type)
            table.setCellWidget(0, 0, rho_type_lbl)
            # rho.value
            rho_value_lbl = QLabel('rho.value')
            self.rho_value = QLineEdit()
            table.setCellWidget(1, 1, self.rho_value)
            table.setCellWidget(1, 0, rho_value_lbl)

            # nu.type
            nu_type_lbl = QLabel('nu.type')
            self.nu_type = QComboBox()
            nu_type_list = ["uniform", "demo"]
            self.nu_type.addItems(nu_type_list)
            table.setCellWidget(2, 1, self.nu_type)
            table.setCellWidget(2, 0, nu_type_lbl)
            # nu.value
            nu_value_lbl = QLabel('nu.value')
            self.nu_value = QLineEdit()
            table.setCellWidget(3, 1, self.nu_value)
            table.setCellWidget(3, 0, nu_value_lbl)

            # E.type
            E_type_lbl = QLabel('E.type')
            self.E_type = QComboBox()
            E_type_list = ["uniform", "demo"]
            self.E_type.addItems(E_type_list)
            table.setCellWidget(4, 1, self.E_type)
            table.setCellWidget(4, 0, E_type_lbl)
            # E.value
            E_value_lbl = QLabel('E.value')
            self.E_value = QLineEdit()
            table.setCellWidget(5, 1, self.E_value)
            table.setCellWidget(5, 0, E_value_lbl)

            # planeStress
            planeStress_type_lbl = QLabel('planeStress')
            self.planeStress_type = QComboBox()
            planeStress_type_list = ["yes", "no"]
            self.planeStress_type.addItems(planeStress_type_list)
            table.setCellWidget(6, 1, self.planeStress_type)
            table.setCellWidget(6, 0, planeStress_type_lbl)

            # вывод значений параметров
            if 'mechanicalProperties' in self.con.tables():
                #print('вах')
						
                query = QtSql.QSqlQuery()
                query.exec("SELECT * FROM mechanicalProperties")
                if query.isActive():
                    query.first()
                    value_list = []
                    while query.isValid():
                        value_res = query.value('value')
                        value_list.append(value_res)
                        query.next()
						
                    # rho_type
                    rho_type_mas = self.rho_type.count()   
                    for i in range(rho_type_mas):
                        if self.rho_type.itemText(i) == value_list[0]:
                            self.rho_type.setCurrentIndex(i)
							
                    # rho_value
                    self.rho_value.setText(value_list[1])
					
                    # nu_type
                    nu_type_mas = self.nu_type.count()   
                    for i in range(nu_type_mas):
                        if self.nu_type.itemText(i) == value_list[2]:
                            self.nu_type.setCurrentIndex(i)
					
                    # nu_value
                    self.nu_value.setText(value_list[3])
					
                    # E_type
                    E_type_mas = self.E_type.count()   
                    for i in range(E_type_mas):
                        if self.E_type.itemText(i) == value_list[4]:
                            self.E_type.setCurrentIndex(i)
							
                    # E_value
                    self.E_value.setText(value_list[5])
					
                    # planeStress_type
                    planeStress_type_mas = self.planeStress_type.count()   
                    for i in range(planeStress_type_mas):
                        if self.planeStress_type.itemText(i) == value_list[6]:
                            self.planeStress_type.setCurrentIndex(i)
					
            btnSave = QPushButton()
            btnSave.setFixedSize(80, 25)
            btnSave.clicked.connect(self.on_btnSave_clicked)

            if self.interface_lng_val == 'Russian':
                btnSave.setText("Сохранить")
            elif self.interface_lng_val == 'English':
                btnSave.setText("Save")

            vbox = QVBoxLayout()
            vbox.addWidget(table)
            vbox.addWidget(btnSave)

# ---------------------Размещение на форме всех компонентов-------------------------

            form = QFormLayout()
            form.addRow(vbox)
            self.setLayout(form)

    def on_btnSave_clicked(self):
        rho_type_txt = self.rho_type.currentText()
        rho_value_txt = self.rho_value.text()
        nu_type_txt = self.nu_type.currentText()
        nu_value_txt = self.nu_value.text()
        E_type_txt = self.E_type.currentText()
        E_value_txt = self.E_value.text()
        planeStress_type_txt = self.planeStress_type.currentText()

        msg_list = []
        if rho_value_txt == '':
            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:red">Укажите параметр rho.value</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:red">Set rho.value parameter</span>')
            msg_list.append(msg_lbl)
        if nu_value_txt == '':
            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:red">Укажите параметр nu.value</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:red">Set nu.value parameter</span>')
            msg_list.append(msg_lbl)

        if E_value_txt == '':
            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:red">Укажите параметр E.value</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:red">Set E.value parameter</span>')
            msg_list.append(msg_lbl)

        if msg_list == []:
			
            if 'mechanicalProperties' not in self.con.tables():
                query = QtSql.QSqlQuery()
                query.exec("CREATE TABLE mechanicalProperties(param, value)")

                query.exec("INSERT INTO mechanicalProperties(param, value) VALUES ('%s','%s')" % ('rho_type', ''))
                query.exec("INSERT INTO mechanicalProperties(param, value) VALUES ('%s','%s')" % ('rho_value', ''))
                query.exec("INSERT INTO mechanicalProperties(param, value) VALUES ('%s','%s')" % ('nu_type', ''))
                query.exec("INSERT INTO mechanicalProperties(param, value) VALUES ('%s','%s')" % ('nu_value', ''))
                query.exec("INSERT INTO mechanicalProperties(param, value) VALUES ('%s','%s')" % ('E_type', ''))
                query.exec("INSERT INTO mechanicalProperties(param, value) VALUES ('%s','%s')" % ('E_value', ''))
                query.exec("INSERT INTO mechanicalProperties(param, value) VALUES ('%s','%s')" % ('planeStress', ''))

            if 'mechanicalProperties' in self.con.tables():

                query = QtSql.QSqlQuery()

                query.prepare("UPDATE mechanicalProperties SET value=? WHERE param='rho_type'")
                query.bindValue(0, rho_type_txt)
                query.exec_()

                query.prepare("UPDATE mechanicalProperties SET value=? WHERE param='rho_value'")
                query.bindValue(0, rho_value_txt)
                query.exec_()

                query.prepare("UPDATE mechanicalProperties SET value=? WHERE param='nu_type'")
                query.bindValue(0, nu_type_txt)
                query.exec_()

                query.prepare("UPDATE mechanicalProperties SET value=? WHERE param='nu_value'")
                query.bindValue(0, nu_value_txt)
                query.exec_()

                query.prepare("UPDATE mechanicalProperties SET value=? WHERE param='E_type'")
                query.bindValue(0, E_type_txt)
                query.exec_()

                query.prepare("UPDATE mechanicalProperties SET value=? WHERE param='E_value'")
                query.bindValue(0, E_value_txt)
                query.exec_()

                query.prepare("UPDATE mechanicalProperties SET value=? WHERE param='planeStress'")
                query.bindValue(0, planeStress_type_txt)
                query.exec_()

            # записываем файл mechanicalProperties
            if os.path.exists(self.full_dir + '/constant/mechanicalProperties'):
                os.remove(self.full_dir + '/constant/mechanicalProperties')
		
            shutil.copyfile("./matches/Shablon/constant/mechanicalProperties", self.full_dir + '/constant/mechanicalProperties')

            mP = open(self.full_dir + '/constant/mechanicalProperties', 'a')

            ###rho###
            rho_bl = '\n' + 'rho' + '\n' + '{' + '\n' \
            + '    ' + 'type' + '        ' + rho_type_txt + ';' + '\n' \
            + '    ' + 'value' + '       ' + rho_value_txt + ';' + '\n' \
            + '}' + '\n\n'

            ###nu###
            nu_bl = 'nu' + '\n' + '{' + '\n' \
            + '    ' + 'type' + '        ' + nu_type_txt + ';' + '\n' \
            + '    ' + 'value' + '       ' + nu_value_txt + ';' + '\n' \
            + '}' + '\n\n'

            ###E###
            E_bl = 'E' + '\n' + '{' + '\n' \
            + '    ' + 'type' + '        ' + E_type_txt + ';' + '\n' \
            + '    ' + 'value' + '       ' + E_value_txt + ';' + '\n' \
            + '}' + '\n\n'

            ###planeStress###
            planeStress_bl = 'planeStress' + '     ' + planeStress_type_txt + ';' + '\n\n'

            mP.write(rho_bl + nu_bl + E_bl + planeStress_bl)
            close_str = '// ************************************************************************* //'
            mP.write(close_str)

            mP.close()

            self.par.cdw.setWidget(self.par.outf_scroll)
            outf = open(self.full_dir + '/constant/mechanicalProperties')

            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:green">Файл mechanicalProperties сохранен</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:green">The mechanicalProperties file was saved</span>')

            self.par.listWidget.clear()
            self.par.item = QListWidgetItem()
            self.par.listWidget.addItem(self.par.item)
            self.par.listWidget.setItemWidget(self.par.item, msg_lbl)

            data = outf.read()

            if self.interface_lng_val == 'Russian':
                self.par.outf_lbl.setText("Файл " + "<font color='peru'>" + 'mechanicalProperties' + "</font>")
            elif self.interface_lng_val == 'English':
                self.par.outf_lbl.setText("<font color='peru'>" + 'mechanicalProperties' + "</font>" + " file")
            self.par.outf_edit.setText(data)

            self.par.cdw.setTitleBarWidget(self.par.cdw_frame)
            outf.close()

        else:
            self.par.listWidget.clear()
            for msg_lbl in msg_list:
                self.par.item = QListWidgetItem()
                self.par.listWidget.addItem(self.par.item)
                self.par.listWidget.setItemWidget(self.par.item, msg_lbl)
