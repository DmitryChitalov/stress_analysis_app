# -*- coding: utf-8 -*-
# -----------------------------Импорт модулей-----------------------------------

from PyQt5 import QtSql

import os
import os.path
import shutil

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QTableWidget, QComboBox, \
    QSpinBox, QPushButton, QListWidgetItem, QLineEdit

# -----------------------------------Форма--------------------------------------

class thermalProperties_form_class(QWidget):
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
            # C.type
            C_type_lbl = QLabel('C.type')
            self.C_type = QComboBox()
            C_type_list = ["uniform", "demo"]
            self.C_type.addItems(C_type_list)
            table.setCellWidget(0, 1, self.C_type)
            table.setCellWidget(0, 0, C_type_lbl)
            # C.value
            C_value_lbl = QLabel('C.value')
            self.C_value = QLineEdit()
            table.setCellWidget(1, 1, self.C_value)
            table.setCellWidget(1, 0, C_value_lbl)

            # k.type
            k_type_lbl = QLabel('k.type')
            self.k_type = QComboBox()
            k_type_list = ["uniform", "demo"]
            self.k_type.addItems(k_type_list)
            table.setCellWidget(2, 1, self.k_type)
            table.setCellWidget(2, 0, k_type_lbl)
            # k.value
            k_value_lbl = QLabel('k.value')
            self.k_value = QLineEdit()
            table.setCellWidget(3, 1, self.k_value)
            table.setCellWidget(3, 0, k_value_lbl)

            # alpha.type
            alpha_type_lbl = QLabel('alpha.type')
            self.alpha_type = QComboBox()
            alpha_type_list = ["uniform", "demo"]
            self.alpha_type.addItems(alpha_type_list)
            table.setCellWidget(4, 1, self.alpha_type)
            table.setCellWidget(4, 0, alpha_type_lbl)
            # alpha.value
            alpha_value_lbl = QLabel('alpha.value')
            self.alpha_value = QLineEdit()
            table.setCellWidget(5, 1, self.alpha_value)
            table.setCellWidget(5, 0, alpha_value_lbl)

            # thermalStress
            thermalStress_type_lbl = QLabel('thermalStress')
            self.thermalStress_type = QComboBox()
            thermalStress_type_list = ["yes", "no"]
            self.thermalStress_type.addItems(thermalStress_type_list)
            table.setCellWidget(6, 1, self.thermalStress_type)
            table.setCellWidget(6, 0, thermalStress_type_lbl)

            # вывод значений параметров
            if 'thermalProperties' in self.con.tables():
                query = QtSql.QSqlQuery()
                query.exec("SELECT * FROM thermalProperties")
                if query.isActive():
                    query.first()
                    value_list = []
                    while query.isValid():
                        value_res = query.value('value')
                        value_list.append(value_res)
                        query.next()
						
                    # C_type
                    C_type_mas = self.C_type.count()   
                    for i in range(C_type_mas):
                        if self.C_type.itemText(i) == value_list[0]:
                            self.C_type.setCurrentIndex(i)
							
                    # C_value
                    self.C_value.setText(value_list[1])
					
                    # k_type
                    k_type_mas = self.k_type.count()   
                    for i in range(k_type_mas):
                        if self.k_type.itemText(i) == value_list[2]:
                            self.k_type.setCurrentIndex(i)
					
                    # k_value
                    self.k_value.setText(value_list[3])
					
                    # alpha_type
                    alpha_type_mas = self.alpha_type.count()   
                    for i in range(alpha_type_mas):
                        if self.alpha_type.itemText(i) == value_list[4]:
                            self.alpha_type.setCurrentIndex(i)
							
                    # alpha_value
                    self.alpha_value.setText(value_list[5])
					
                    # thermalStress_type
                    thermalStress_type_mas = self.thermalStress_type.count()   
                    for i in range(thermalStress_type_mas):
                        if self.thermalStress_type.itemText(i) == value_list[6]:
                            self.thermalStress_type.setCurrentIndex(i)


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
        C_type_txt = self.C_type.currentText()
        C_value_txt = self.C_value.text()
        k_type_txt = self.k_type.currentText()
        k_value_txt = self.k_value.text()
        alpha_type_txt = self.alpha_type.currentText()
        alpha_value_txt = self.alpha_value.text()
        thermalStress_type_txt = self.thermalStress_type.currentText()

        msg_list = []
        if C_value_txt == '':
            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:red">Укажите параметр C.value</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:red">Set C.value parameter</span>')
            msg_list.append(msg_lbl)
        if k_value_txt == '':
            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:red">Укажите параметр k.value</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:red">Set k.value parameter</span>')
            msg_list.append(msg_lbl)

        if alpha_value_txt == '':
            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:red">Укажите параметр alpha.value</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:red">Set alpha.value parameter</span>')
            msg_list.append(msg_lbl)

        if msg_list == []:
			
            if 'thermalProperties' not in self.con.tables():
                query = QtSql.QSqlQuery()
                query.exec("CREATE TABLE thermalProperties(param, value)")

                query.exec("INSERT INTO thermalProperties(param, value) VALUES ('%s','%s')" % ('C_type', ''))
                query.exec("INSERT INTO thermalProperties(param, value) VALUES ('%s','%s')" % ('C_value', ''))
                query.exec("INSERT INTO thermalProperties(param, value) VALUES ('%s','%s')" % ('k_type', ''))
                query.exec("INSERT INTO thermalProperties(param, value) VALUES ('%s','%s')" % ('k_value', ''))
                query.exec("INSERT INTO thermalProperties(param, value) VALUES ('%s','%s')" % ('alpha_type', ''))
                query.exec("INSERT INTO thermalProperties(param, value) VALUES ('%s','%s')" % ('alpha_value', ''))
                query.exec("INSERT INTO thermalProperties(param, value) VALUES ('%s','%s')" % ('thermalStress', ''))

            if 'thermalProperties' in self.con.tables():
                query = QtSql.QSqlQuery()

                query.prepare("UPDATE thermalProperties SET value=? WHERE param='C_type'")
                query.bindValue(0, C_type_txt)
                query.exec_()

                query.prepare("UPDATE thermalProperties SET value=? WHERE param='C_value'")
                query.bindValue(0, C_value_txt)
                query.exec_()

                query.prepare("UPDATE thermalProperties SET value=? WHERE param='k_type'")
                query.bindValue(0, k_type_txt)
                query.exec_()

                query.prepare("UPDATE thermalProperties SET value=? WHERE param='k_value'")
                query.bindValue(0, k_value_txt)
                query.exec_()

                query.prepare("UPDATE thermalProperties SET value=? WHERE param='alpha_type'")
                query.bindValue(0, alpha_type_txt)
                query.exec_()

                query.prepare("UPDATE thermalProperties SET value=? WHERE param='alpha_value'")
                query.bindValue(0, alpha_value_txt)
                query.exec_()

                query.prepare("UPDATE thermalProperties SET value=? WHERE param='thermalStress'")
                query.bindValue(0, thermalStress_type_txt)
                query.exec_()
				
            # записываем файл thermalProperties
            if os.path.exists(self.full_dir + '/constant/thermalProperties'):
                os.remove(self.full_dir + '/constant/thermalProperties')
		
            shutil.copyfile("./matches/Shablon/constant/thermalProperties", self.full_dir + '/constant/thermalProperties')

            # записываем файл thermalProperties

            tP = open(self.full_dir + '/constant/thermalProperties', 'a')

            ###C###
            C_bl = '\n' + 'C' + '\n' + '{' + '\n' \
            + '    ' + 'type' + '        ' + C_type_txt + ';' + '\n' \
            + '    ' + 'value' + '       ' + C_value_txt + ';' + '\n' \
            + '}' + '\n\n'

            ###k###
            k_bl = 'k' + '\n' + '{' + '\n' \
            + '    ' + 'type' + '        ' + k_type_txt + ';' + '\n' \
            + '    ' + 'value' + '       ' + k_value_txt + ';' + '\n' \
            + '}' + '\n\n'

            ###alpha###
            alpha_bl = 'alpha' + '\n' + '{' + '\n' \
            + '    ' + 'type' + '        ' + alpha_type_txt + ';' + '\n' \
            + '    ' + 'value' + '       ' + alpha_value_txt + ';' + '\n' \
            + '}' + '\n\n'

            ###thermalStress###
            thermalStress_bl = 'thermalStress' + '     ' + thermalStress_type_txt + ';' + '\n\n'

            tP.write(C_bl + k_bl + alpha_bl + thermalStress_bl)
            close_str = '// ************************************************************************* //'
            tP.write(close_str)

            tP.close()

            self.par.cdw.setWidget(self.par.outf_scroll)
            outf = open(self.full_dir + '/constant/thermalProperties')

            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:green">Файл thermalProperties сохранен</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:green">The thermalProperties file was saved</span>')

            self.par.listWidget.clear()
            self.par.item = QListWidgetItem()
            self.par.listWidget.addItem(self.par.item)
            self.par.listWidget.setItemWidget(self.par.item, msg_lbl)

            data = outf.read()

            if self.interface_lng_val == 'Russian':
                self.par.outf_lbl.setText("Файл " + "<font color='peru'>" + 'thermalProperties' + "</font>")
            elif self.interface_lng_val == 'English':
                self.par.outf_lbl.setText("<font color='peru'>" + 'thermalProperties' + "</font>" + " file")
            self.par.outf_edit.setText(data)

            self.par.cdw.setTitleBarWidget(self.par.cdw_frame)
            outf.close()

        else:
            self.par.listWidget.clear()
            for msg_lbl in msg_list:
                self.par.item = QListWidgetItem()
                self.par.listWidget.addItem(self.par.item)
                self.par.listWidget.setItemWidget(self.par.item, msg_lbl)
