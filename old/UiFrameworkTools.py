# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FormFrameworkTools(object):
    def setupUi(self, FormFrameworkTools):
        FormFrameworkTools.setObjectName("FormFrameworkTools")
        FormFrameworkTools.resize(909, 628)
        self.gridLayout = QtWidgets.QGridLayout(FormFrameworkTools)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.codeEdit = Qsci.QsciScintilla(FormFrameworkTools)
        self.codeEdit.setToolTip("")
        self.codeEdit.setWhatsThis("")
        self.codeEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.codeEdit.setObjectName("codeEdit")
        self.gridLayout.addWidget(self.codeEdit, 1, 0, 3, 1)
        self.pathEdit = QtWidgets.QLineEdit(FormFrameworkTools)
        self.pathEdit.setObjectName("pathEdit")
        self.gridLayout.addWidget(self.pathEdit, 0, 0, 1, 1)
        self.selectButton = QtWidgets.QPushButton(FormFrameworkTools)
        self.selectButton.setObjectName("selectButton")
        self.gridLayout.addWidget(self.selectButton, 0, 1, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(FormFrameworkTools)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.resultEdit = QtWidgets.QTextBrowser(self.groupBox_3)
        self.resultEdit.setObjectName("resultEdit")
        self.verticalLayout_2.addWidget(self.resultEdit)
        self.gridLayout.addWidget(self.groupBox_3, 3, 1, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(FormFrameworkTools)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.argsEdit = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.argsEdit.setObjectName("argsEdit")
        self.verticalLayout_3.addWidget(self.argsEdit)
        self.gridLayout.addWidget(self.groupBox_2, 1, 1, 1, 1)
        self.runButton = QtWidgets.QPushButton(FormFrameworkTools)
        self.runButton.setObjectName("runButton")
        self.gridLayout.addWidget(self.runButton, 2, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 3)

        self.retranslateUi(FormFrameworkTools)
        QtCore.QMetaObject.connectSlotsByName(FormFrameworkTools)

    def retranslateUi(self, FormFrameworkTools):
        _translate = QtCore.QCoreApplication.translate
        FormFrameworkTools.setWindowTitle(_translate("FormFrameworkTools", "框架测试工具"))
        self.selectButton.setText(_translate("FormFrameworkTools", "浏览"))
        self.groupBox_3.setTitle(_translate("FormFrameworkTools", "返回结果"))
        self.groupBox_2.setTitle(_translate("FormFrameworkTools", "设置运行参数"))
        self.runButton.setText(_translate("FormFrameworkTools", "运行"))

from PyQt5 import Qsci

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormFrameworkTools = QtWidgets.QWidget()
    ui = Ui_FormFrameworkTools()
    ui.setupUi(FormFrameworkTools)
    FormFrameworkTools.show()
    sys.exit(app.exec_())

