# -*- coding: utf-8 -*-
# -----------------------------Импорт модулей-----------------------------------

from PyQt5 import QtSql
import os
import os.path
import shutil

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QTableWidget, QComboBox, \
    QSpinBox, QPushButton, QListWidgetItem, QLineEdit, QDoubleSpinBox

# -----------------------------------Форма--------------------------------------

class fvSolution_form_class(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.interface_lng_val = parent.interface_lng_val
        self.con = parent.con
        self.full_dir = parent.full_dir
        self.par = parent

        if self.con.open():

            table = QTableWidget(8, 2)
            table.setColumnWidth(0, 150)
            table.setColumnWidth(1, 230)
            table.setFixedSize(674, 480)
            table.setHorizontalHeaderLabels(["Параметр", "Значение"])

            # solver
            solver_lbl = QLabel('solver')
            self.solver = QComboBox()
            solver_list = ["GAMG", "demo"]
            self.solver.addItems(solver_list)
            table.setCellWidget(0, 1, self.solver)
            table.setCellWidget(0, 0, solver_lbl)

            # tolerance
            tolerance_lbl = QLabel('tolerance')
            self.tolerance = QLineEdit()
            table.setCellWidget(1, 1, self.tolerance)
            table.setCellWidget(1, 0, tolerance_lbl)

            # relTol
            relTol_lbl = QLabel('relTol')
            self.relTol = QDoubleSpinBox()
            table.setCellWidget(2, 1, self.relTol)
            table.setCellWidget(2, 0, relTol_lbl)

            # smoother
            smoother_lbl = QLabel('smoother')
            self.smoother = QComboBox()
            smoother_list = ["GaussSeidel", "demo"]
            self.smoother.addItems(smoother_list)
            table.setCellWidget(3, 1, self.smoother)
            table.setCellWidget(3, 0, smoother_lbl)

            # nCellsInCoarsestLevel
            nCellsInCoarsestLevel_lbl = QLabel('nCellsInCoarsestLevel')
            self.nCellsInCoarsestLevel = QSpinBox()
            table.setCellWidget(4, 1, self.nCellsInCoarsestLevel)
            table.setCellWidget(4, 0, nCellsInCoarsestLevel_lbl)

            # compactNormalStress
            compactNormalStress_lbl = QLabel('compactNormalStress')
            self.compactNormalStress = QComboBox()
            compactNormalStress_list = ["yes", "no"]
            self.compactNormalStress.addItems(compactNormalStress_list)
            table.setCellWidget(5, 1, self.compactNormalStress)
            table.setCellWidget(5, 0, compactNormalStress_lbl)

            # nCorrectors
            nCorrectors_lbl = QLabel('nCorrectors')
            self.nCorrectors = QSpinBox()
            table.setCellWidget(6, 1, self.nCorrectors)
            table.setCellWidget(6, 0, nCorrectors_lbl)

            # D
            D_lbl = QLabel('D')
            self.D = QLineEdit()
            table.setCellWidget(7, 1, self.D)
            table.setCellWidget(7, 0, D_lbl)

            # вывод значений параметров
            if 'fvSolution' in self.con.tables():
						
                query = QtSql.QSqlQuery()
                query.exec("SELECT * FROM fvSolution")
                if query.isActive():
                    query.first()
                    value_list = []
                    while query.isValid():
                        value_res = query.value('value')
                        value_list.append(value_res)
                        query.next()
						
                    
                    # solver
                    solver_mas = self.solver.count()   
                    for i in range(solver_mas):
                        if self.solver.itemText(i) == value_list[0]:
                            self.solver.setCurrentIndex(i)
							
                    # tolerance
                    self.tolerance.setText(value_list[1])
					
                    # relTol
                    self.relTol.setValue(value_list[2])
					
                    # smoother
                    smoother_mas = self.smoother.count()   
                    for i in range(smoother_mas):
                        if self.smoother.itemText(i) == value_list[3]:
                            self.smoother.setCurrentIndex(i)
							
                    # nCellsInCoarsestLevel
                    self.nCellsInCoarsestLevel.setValue(value_list[4])
					
                    # compactNormalStress
                    compactNormalStress_mas = self.compactNormalStress.count()   
                    for i in range(compactNormalStress_mas):
                        if self.compactNormalStress.itemText(i) == value_list[5]:
                            self.compactNormalStress.setCurrentIndex(i)
							
                    # nCorrectors
                    self.nCorrectors.setValue(value_list[6])
					
                    # D
                    self.D.setText(value_list[7])
					
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

        solver_txt = self.solver.currentText()
        tolerance_txt = self.tolerance.text()
        relTol_txt = self.relTol.value()
        smoother_txt = self.smoother.currentText()
        nCellsInCoarsestLevel_txt = self.nCellsInCoarsestLevel.value()
        compactNormalStress_txt = self.compactNormalStress.currentText()
        nCorrectors_txt = self.nCorrectors.value()
        D_txt = self.D.text()


        msg_list = []
        if tolerance_txt == '':
            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:red">Укажите параметр tolerance</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:red">Set tolerance parameter</span>')
            msg_list.append(msg_lbl)
        if D_txt == '':
            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:red">Укажите параметр D</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:red">Set D parameter</span>')
            msg_list.append(msg_lbl)

        if msg_list == []:
			
            if 'fvSolution' not in self.con.tables():
                query = QtSql.QSqlQuery()
                query.exec("CREATE TABLE fvSolution(param, value)")

                query.exec("INSERT INTO fvSolution(param, value) VALUES ('%s','%s')" % ('solver', ''))
                query.exec("INSERT INTO fvSolution(param, value) VALUES ('%s','%s')" % ('tolerance', ''))
                query.exec("INSERT INTO fvSolution(param, value) VALUES ('%s','%s')" % ('relTol', ''))
                query.exec("INSERT INTO fvSolution(param, value) VALUES ('%s','%s')" % ('smoother', ''))
                query.exec("INSERT INTO fvSolution(param, value) VALUES ('%s','%s')" % ('nCellsInCoarsestLevel', ''))
                query.exec("INSERT INTO fvSolution(param, value) VALUES ('%s','%s')" % ('compactNormalStress', ''))
                query.exec("INSERT INTO fvSolution(param, value) VALUES ('%s','%s')" % ('nCorrectors', ''))
                query.exec("INSERT INTO fvSolution(param, value) VALUES ('%s','%s')" % ('D', ''))



            if 'fvSolution' in self.con.tables():
                query = QtSql.QSqlQuery()

                query.prepare("UPDATE fvSolution SET value=? WHERE param='solver'")
                query.bindValue(0, solver_txt)
                query.exec_()

                query.prepare("UPDATE fvSolution SET value=? WHERE param='tolerance'")
                query.bindValue(0, tolerance_txt)
                query.exec_()

                query.prepare("UPDATE fvSolution SET value=? WHERE param='relTol'")
                query.bindValue(0, relTol_txt)
                query.exec_()

                query.prepare("UPDATE fvSolution SET value=? WHERE param='smoother'")
                query.bindValue(0, smoother_txt)
                query.exec_()

                query.prepare("UPDATE fvSolution SET value=? WHERE param='nCellsInCoarsestLevel'")
                query.bindValue(0, nCellsInCoarsestLevel_txt)
                query.exec_()

                query.prepare("UPDATE fvSolution SET value=? WHERE param='compactNormalStress'")
                query.bindValue(0, compactNormalStress_txt)
                query.exec_()

                query.prepare("UPDATE fvSolution SET value=? WHERE param='nCorrectors'")
                query.bindValue(0, nCorrectors_txt)
                query.exec_()

                query.prepare("UPDATE fvSolution SET value=? WHERE param='D'")
                query.bindValue(0, D_txt)
                query.exec_()

            # записываем файл fvSolution
            if os.path.exists(self.full_dir + '/system/fvSolution'):
                os.remove(self.full_dir + '/system/fvSolution')
		
            shutil.copyfile("./matches/Shablon/system/fvSolution", self.full_dir + '/system/fvSolution')

            fvS = open(self.full_dir + '/system/fvSolution', 'a')
            ###solvers###
            so_bl = '\n' + 'solvers' + '\n' + '{' + '\n' + '    ' + '"(D|T)"' + '\n' + '    ' + '{' + '\n' \
            + '        ' + 'solver' + '          ' + solver_txt + ';' + '\n' \
            + '        ' + 'tolerance' + '       ' + tolerance_txt + ';' + '\n' \
            + '        ' + 'relTol' + '          ' + str(relTol_txt) + ';' + '\n' \
            + '        ' + 'smoother' + '        ' + smoother_txt + ';' + '\n' \
            + '        ' + 'nCellsInCoarsestLevel' + ' ' + str(nCellsInCoarsestLevel_txt) + ';' + '\n' \
            + '    ' + '}' + '\n' + '}' + '\n\n'

            st_bl = 'stressAnalysis' + '\n' + '{' + '    ' + '\n' \
            + '    ' + 'compactNormalStress' + ' ' + compactNormalStress_txt + ';' + '\n' \
            + '    ' + 'nCorrectors' + '     ' + str(nCorrectors_txt) + ';' + '\n' \
            + '    ' + 'D' + '               ' + D_txt + ';' + '\n' \
            + '}' + '\n\n'

            fvS.write(so_bl + st_bl)
            close_str = '// ************************************************************************* //'
            fvS.write(close_str)

            fvS.close()

            self.par.cdw.setWidget(self.par.outf_scroll)
            outf = open(self.full_dir + '/system/fvSolution')

            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:green">Файл fvSolution сохранен</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:green">The fvSolution file was saved</span>')

            self.par.listWidget.clear()
            self.par.item = QListWidgetItem()
            self.par.listWidget.addItem(self.par.item)
            self.par.listWidget.setItemWidget(self.par.item, msg_lbl)

            data = outf.read()

            if self.interface_lng_val == 'Russian':
                self.par.outf_lbl.setText("Файл " + "<font color='peru'>" + 'fvSolution' + "</font>")
            elif self.interface_lng_val == 'English':
                self.par.outf_lbl.setText("<font color='peru'>" + 'fvSolution' + "</font>" + " file")
            self.par.outf_edit.setText(data)

            self.par.cdw.setTitleBarWidget(self.par.cdw_frame)
            outf.close()

        else:
            self.par.listWidget.clear()
            for msg_lbl in msg_list:
                self.par.item = QListWidgetItem()
                self.par.listWidget.addItem(self.par.item)
                self.par.listWidget.setItemWidget(self.par.item, msg_lbl)
