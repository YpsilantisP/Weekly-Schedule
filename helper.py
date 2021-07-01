from datetime import date, timedelta
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

import pandas as pd

wk_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def setMultiCols(week_days):
    i = 0
    while True:
        if (date.today() + timedelta(days=i)).strftime("%A") == 'Sunday':
            break
        else:
            i += 1
    dates = [(date.today() + timedelta(days=i + j)).strftime("%d %B %y")
             for j in range(7)]
    _list =  list(zip(dates, week_days))
    _list.append(('','Weekly Summary'))
    return _list


def setButtonMainWindow(name):
    button = QPushButton(name)
    button.setCursor(Qt.PointingHandCursor)
    button.setMaximumHeight(110)
    button.setMaximumWidth(250)
    button.setSizePolicy(QSizePolicy.Expanding,
                         QSizePolicy.Expanding)
    button.setStyleSheet(
        # setting variable margins
        '''
        border: 4px solid 'black';
        background-color: wheat;
        color: Black;
        font: 'bold';
        font-size: 18px;
        border-radius: 25px;
        padding: 15px 0;
        margin-top: 20px;
        }
        *:hover{
            background: #dcdcde;
        }
        ''')
    return button


def setButtonPopUpWindow(name):
    button = QPushButton(name)
    button.setCursor(Qt.PointingHandCursor)
    button.setMaximumHeight(50)
    button.setMaximumWidth(100)
    button.setSizePolicy(QSizePolicy.Expanding,
                         QSizePolicy.Expanding)
    button.setStyleSheet(
        # setting variable margins
        '''
        border: 2px solid 'black';
        background-color: wheat;
        color: Black;
        font: 'bold';
        font-size: 12px;
        border-radius: 12px;
        padding: 7px 0;
        margin-top: 10px;
        }
        *:hover{
            background: #dcdcde;
        }
        ''')
    return button


def readUserFile(file_name):
    _list = []
    if file_name[-3:] == 'csv':
        imported_file = pd.read_csv(file_name, squeeze=True, header=None,
                                    index_col=False)
        if imported_file.ndim != 1:
            setMsgBoxWrongFile()
            return None
        else:
            imported_file = imported_file.to_list()
            return imported_file


def setMsgBoxForMissingDays():
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setText('You need to fill in all days of the week')
    msg_box.setWindowTitle("Error")
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()


def setMsgBoxGoodJob():
    msg_box = QMessageBox()
    msg_box.setText('All done Job!')
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()


def setMsgBoxOnlyIntegersAllowed():
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setText('Only Integers are allowed')
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()


def setMsgBoxWrongFile():
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setText('Tabular data not supported.'
                    '\nPlease input file with one column only')
    msg_box.setWindowTitle("Error")
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()


def setMsgBoxNoCsvFile():
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setText('Please import CSV file with employees')
    msg_box.setWindowTitle("Error")
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()


def setMsgBoxNoUserInputs():
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setText('CSV or Requirements are missing')
    msg_box.setWindowTitle("Error")
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()


def setNamesForDepartments(len_day_reqs):
    keys = [key for key in range(len_day_reqs)]
    diction = dict.fromkeys(keys)
    for i in range(len(keys)):
        diction[i] = 'Department_{}'.format(i + 1)
    return diction


def checkUsersInputs(manual_inputs, file_inputs):
    if any(v is None for v in manual_inputs[0]) and len(file_inputs) == 0:
        setMsgBoxNoUserInputs()
        return None
    elif any(v is not None for v in manual_inputs[0]) and len(file_inputs) != 0:
        return manual_inputs
    elif any(v is not None for v in manual_inputs[0]) and len(file_inputs) == 0:
        setMsgBoxNoCsvFile()
        return None
    elif any(v is None for v in manual_inputs[0]) and len(file_inputs) != 0:
        setMsgBoxNoUserInputs()
        return None
    else:
        return None


def setNamesToQt(series_csv, qt_model, qt_table):
    rows = []
    vertical_header = ['Employees']
    for i in series_csv:
        value = QtGui.QStandardItem(str(i))
        value.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        rows.append(value)
    qt_model.appendRow(rows)
    qt_model.setVerticalHeaderLabels(vertical_header)
    qt_table.setStyleSheet("""color: Black; font: 'bold'; font-size: 16px;""")
    qt_table.verticalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
    qt_table.horizontalHeader().setVisible(False)
    qt_table.verticalHeader().setVisible(True)
    qt_table.setShowGrid(False)


def setRequirementsToQt(multi_col, a_df, qt_model, qt_table):
    qt_model.clear()
    rows = []
    cols = []
    indexes = []
    for i in range(7):
        cols.append(multi_col[i][0])
        value = QtGui.QStandardItem(str(multi_col[i][1]))
        value.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        rows.append(value)
    qt_model.setHorizontalHeaderLabels(cols)
    qt_model.appendRow(rows)

    indexes.append('Week Days')
    for multi_index in a_df.index:
        value = '{}, {}'.format(multi_index[0], multi_index[1])
        indexes.append(value)

    rows = []
    for index, row in a_df.iterrows():
        for i in row:
            binomial_val = QtGui.QStandardItem(str(i))
            binomial_val.setTextAlignment(Qt.AlignHCenter)
            rows.append(binomial_val)
        qt_model.appendRow(rows)
        rows = []
    qt_model.setVerticalHeaderLabels(indexes)

    for i in range(7):
        qt_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
    qt_table.setStyleSheet("""color: Black; font: 'bold'; font-size: 16px;""")

def setSummaryToQt(user_sums, day_sums, qt_model, qt_table):
    rows_users = []
    rows_days = []
    user_sums.sort_values(inplace=True)
    for index, value in user_sums.iteritems():
        value = QtGui.QStandardItem('{}: {}'.format(index,value))
        # value.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        rows_users.append(value)
        print()

    for index, value in day_sums.iteritems():
        value = QtGui.QStandardItem('{}: {}'.format(index,value))
        # value.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        rows_days.append(value)

    qt_model.appendRow(rows_users)
    qt_model.appendRow(rows_days)
    qt_model.setVerticalHeaderLabels(['Sum Per Person', 'Sum Per Day'])
    qt_table.horizontalHeader().setVisible(False)
    qt_table.setShowGrid(False)
    qt_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
    qt_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
    qt_table.setStyleSheet("""color: Black; font: 'bold'; font-size: 16px;""")
