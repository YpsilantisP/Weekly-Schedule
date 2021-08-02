# from scheduler import *
from helper import *

import os


class PopUpWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ---> empty Variables
        self.manual_inputs = [[None] * 7]
        # ---> Pop Up Window
        self.resize(800, 400)
        self.setWindowTitle('')
        self.setStyleSheet('background:#c5d9ed')
        # ---> Layouts
        vertical_final_layout = QVBoxLayout()
        horizontal_buttons_layout = QHBoxLayout()
        # ---> Label
        self._label = QLabel('Please fill in the days for scheduler', self)
        self._label.setFixedSize(400, 50)
        self._label.setStyleSheet('''font: bold; font-size: 18px''')
        # ---> Pop Up Table
        self.pop_up_table = QTableWidget(1, 7)
        self.pop_up_table.setHorizontalHeaderLabels(wk_days)
        [self.pop_up_table.horizontalHeader().setSectionResizeMode(
            i, QHeaderView.Stretch) for i in range(7)]
        # self.pop_up_table.verticalHeader().\
        #     setSectionResizeMode(0,QHeaderView.Stretch)
        # ---> Buttons
        self.add_rows_button = setButtonPopUpWindow('Add Rows')
        self.remove_rows_button = setButtonPopUpWindow('Remove Rows')
        self.ok_button = setButtonPopUpWindow('Ok')
        self.clear_button = setButtonPopUpWindow('Clear')
        self.exit_button = setButtonPopUpWindow('Exit')
        # ---> Filling the Layouts        
        horizontal_buttons_layout.addWidget(self.add_rows_button)
        horizontal_buttons_layout.addWidget(self.remove_rows_button)
        horizontal_buttons_layout.addWidget(self.ok_button)
        horizontal_buttons_layout.addWidget(self.clear_button)
        horizontal_buttons_layout.addWidget(self.exit_button)
        vertical_final_layout.addWidget(self._label, alignment=Qt.AlignTop)
        vertical_final_layout.addWidget(self.pop_up_table)
        vertical_final_layout.addLayout(horizontal_buttons_layout)
        self.setLayout(vertical_final_layout)
        self.widget = QWidget()
        self.widget.setLayout(vertical_final_layout)
        self.setCentralWidget(self.widget)
        # Actions
        # ---> Menu Bar
        self.add_rows_button.clicked.connect(self.addRow)
        self.remove_rows_button.clicked.connect(self.removeRow)
        self.ok_button.clicked.connect(self.UpdateList)
        self.clear_button.clicked.connect(self.clearTable)
        self.exit_button.clicked.connect(lambda: self.close())

    def addRow(self):
        rowCount = self.pop_up_table.rowCount()
        self.pop_up_table.insertRow(rowCount)
        self.manual_inputs.append([None] * 7)

    def removeRow(self):
        if self.pop_up_table.rowCount() > 0:
            self.pop_up_table.removeRow(self.pop_up_table.rowCount() - 1)
            self.manual_inputs = self.manual_inputs[0:len(self.manual_inputs) - 1]

    def UpdateList(self):
        """ Function used to refresh the table --
            removing previous values and updating with new"""
        """ Append input from User to List"""
        try:
            for i in range(self.pop_up_table.rowCount()):
                for j in range(self.pop_up_table.columnCount()):
                    if self.pop_up_table.item(i, j):
                        self.manual_inputs[i][j] = \
                            int(self.pop_up_table.item(i, j).text())
        except ValueError:
            setMsgBoxOnlyIntegersAllowed()
        if any(value is None for row in self.manual_inputs for value in row):
            setMsgBoxForMissingDays()
            return
        else:
            return

    def clearTable(self):
        self.pop_up_table.clear()
        self.manual_inputs = [[None] * 7]
        self.pop_up_table.setHorizontalHeaderLabels(wk_days)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # ---> Empty Vars
        self.list_from_csv = []
        self.pop_up_window = PopUpWindow()
        # ---> Specifications of MainWindow
        self.setGeometry(200, 200, 1137, 600)
        self.setWindowTitle('Weekly Scheduler')
        self.setStyleSheet('background:#c5d9ed')
        # ---> set Layouts
        vertical_final_layout = QVBoxLayout()
        horizontal_buttons_layout = QHBoxLayout()
        # ---> Tables
        self.names_model = QtGui.QStandardItemModel(self)
        self.employee_names_table = QTableView()
        self.employee_names_table.setModel(self.names_model)
        self.employee_names_table.setMaximumHeight(80)

        self.schedule_model = QtGui.QStandardItemModel(self)
        self.schedule_table = QTableView()
        self.schedule_table.setModel(self.schedule_model)

        self.summary_model = QtGui.QStandardItemModel(self)
        self.summary_table = QTableView()
        self.summary_table.setModel(self.summary_model)
        self.summary_table.setMaximumHeight(120)
        # ---> Buttons
        self.import_file_button = setButtonMainWindow('Import File')
        self.days_required_button = setButtonMainWindow('Add Requirements')
        self.calculate_schedule_button = setButtonMainWindow('Calculate')
        self.export_button = setButtonMainWindow('Export Schedule')
        self.clear_button = setButtonMainWindow('Clear')
        # ---> set Layouts
        horizontal_buttons_layout.addWidget(self.import_file_button)
        horizontal_buttons_layout.addWidget(self.days_required_button)
        horizontal_buttons_layout.addWidget(self.calculate_schedule_button)
        horizontal_buttons_layout.addWidget(self.export_button)
        horizontal_buttons_layout.addWidget(self.clear_button)
        vertical_final_layout.addLayout(horizontal_buttons_layout)
        vertical_final_layout.addWidget(self.employee_names_table)
        vertical_final_layout.addWidget(self.schedule_table)
        vertical_final_layout.addWidget(self.summary_table)
        self.setLayout(vertical_final_layout)
        self.widget = QWidget()
        self.widget.setLayout(vertical_final_layout)
        self.setCentralWidget(self.widget)
        # Actions
        # ---> Buttons
        self.import_file_button.clicked.connect(self.openFunc)
        self.import_file_button. \
            setStatusTip("Select a file to use for comparison")
        self.days_required_button.clicked.connect(self.setDaysForSchedule)
        self.calculate_schedule_button.clicked.connect(self.calculateSchedule)
        self.export_button.clicked.connect(self.exportResults)
        self.clear_button.clicked.connect(self.clearAll)

    def openFunc(self):
        """
        Try except is used prevent user from loading wrong data
        the small if statement 168 row will check if import a file or not"""
        try:
            self.file_name = \
                QFileDialog.getOpenFileName(self, 'Open File',
                                            os.path.expanduser('~/Desktop'),
                                            'Excel (*.csv)')
            if self.file_name[0] == "":
                self.file_name = []
                return
            else:
                self.list_from_csv = readUserFile(self.file_name[0])
                setNamesToQt(self.list_from_csv, self.names_model,
                             self.employee_names_table)
                return
        except:
            self.file_name = []
            return

    def setDaysForSchedule(self):
        self.pop_up_window.show()

    def calculateSchedule(self):
        day_reqs = None
        day_reqs = checkUsersInputs(self.pop_up_window.manual_inputs, self.list_from_csv)
        if day_reqs == None:
            return
        else:
            total_day_requirements = ([sum(x) for x in zip(*day_reqs)])
            department_names = setNamesForDepartments(len(day_reqs))
            total_users = max(total_day_requirements)
            tot_departments = len(day_reqs)
            days = 7

            self.user_sums, self.dashboard, self.status, self.day_sums = \
                schedule(self.list_from_csv, total_users, tot_departments,
                         day_reqs, days, department_names)

            while (self.user_sums > 5).any() or self.status == -1:
                print('Status infeasible -- adding one user: {}->{}'.format(
                    total_users, total_users + 1))
                total_users += 1
                self.user_sums, self.dashboard, self.status, self.day_sums = \
                    schedule(self.list_from_csv, total_users, tot_departments,
                             day_reqs, days, department_names)


            setRequirementsToQt(setMultiCols(wk_days), self.dashboard,
                                self.schedule_model, self.schedule_table)

            setSummaryToQt(self.user_sums, self.day_sums, self.summary_model,
                           self.summary_table)


    def exportResults(self):
        _df = self.dashboard.copy()
        _df.columns = pd.MultiIndex.from_tuples(setMultiCols(wk_days))
        _df.to_csv('Schedule {}.csv'.format(pd.to_datetime('today').date()))
        return

    def clearAll(self):
        self.employee_names_table.clear()
        self.pop_up_window.clear()
        return
