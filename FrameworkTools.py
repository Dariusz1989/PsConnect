#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年11月29日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: FrameworkTools
@description: 
"""

import json
import traceback
from urllib.parse import unquote

from PyQt5.Qsci import QsciLexerJavaScript, QsciScintilla, QsciAPIs
from PyQt5.QtCore import QSettings, pyqtSlot, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QMessageBox, QProgressDialog

from UiFrameworkTools import Ui_FormFrameworkTools
from Utils.Protocol import Protocol
from Utils.TcpSocket import TcpSocket


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"

# 案例模版
Template = r"""#target photoshop

function test2() {
    return '{"version":"' + app.version +'", "method":"showMessage", "params": ["' + File.encode('测试内容') +'"]}';
}

// 等待2秒
$.sleep(2000);

// 这里是需要被替换的具体函数
// #Function#
// test2();
"""

CodeGetVersion = r"""#target photoshop
'{"version":"' + app.version +'"}';
"""


class Window(QWidget, Ui_FormFrameworkTools):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._passwordError = False
        self._initSocket()
        self._initCodeEdit()

        # 配置
        self._setting = QSettings('PsConnectFrameworkTools', 'Settings')
        # ip地址
        self.lineEditAddress.setText(self._setting.value(
            'lineEditAddress', '127.0.0.1', str))
        # ps端口
        self.spinBoxPsPort.setValue(
            self._setting.value('spinBoxPsPort', 49494, int))
        # ps密码
        self.lineEditPassword.setText(self._setting.value(
            'lineEditPassword', '', str))
        # 设置参数
        self.argsEdit.setPlainText(self._setting.value(
            'argsEdit', 'test2();', str))
        # 设置编辑器里的代码
        self.codeEdit.setText(self._setting.value('codeEdit', Template, str))

    def _initSocket(self):
        # 初始化client(用于连接ps)
        self._client = TcpSocket(self)
        self._client.messageReceived.connect(self.onMessageReceived)
        self._client.connected.connect(self.onConnectSuccessed)
        self._client.connectClosed.connect(self.onConnectClosed)

    def _initCodeEdit(self):
        # 初始化编辑器的工作
        self.codeEdit.setUtf8(True)
        self.codeEdit.linesChanged.connect(self.onLinesChanged)  # 行改变
        # 代码高亮
        self.codeEdit.setLexer(QsciLexerJavaScript(self))
        # 自动折叠
        self.codeEdit.setMarginType(3, QsciScintilla.SymbolMargin)
        self.codeEdit.setMarginLineNumbers(3, False)
        self.codeEdit.setMarginWidth(3, 15)
        self.codeEdit.setMarginSensitivity(3, True)
        # 显示行号
        #self.codeEdit.setMarginType(0, QsciScintilla.NumberMargin)
        self.codeEdit.setMarginLineNumbers(0, True)
        self.onLinesChanged()
        # 代码提示
        sciApi = QsciAPIs(self.codeEdit.lexer())
        sciApi.prepare()
        self.codeEdit.setAutoCompletionSource(QsciScintilla.AcsAll)  # 设置源
        self.codeEdit.setAutoCompletionCaseSensitivity(True)  # 设置自动补全大小写敏感
        self.codeEdit.setAutoCompletionThreshold(1)  # 设置每输入一个字符就会出现自动补全的提示
        # 设置字体
        self.codeEdit.setFont(QFont('Consolas', 16))
        self.codeEdit.setMarginsFont(self.codeEdit.font())
        # 设置编码
        self.codeEdit.SendScintilla(
            QsciScintilla.SCI_SETCODEPAGE, QsciScintilla.SC_CP_UTF8)

        self.codeEdit.setBraceMatching(QsciScintilla.StrictBraceMatch)

        # 设置当前行高亮
        self.codeEdit.setCaretLineVisible(True)
        self.codeEdit.setCaretLineBackgroundColor(Qt.lightGray)
        self.codeEdit.setCaretForegroundColor(Qt.white)

        # tab
        # table relative
        self.codeEdit.setIndentationsUseTabs(True)
        self.codeEdit.setIndentationWidth(4)
        self.codeEdit.setTabIndents(True)
        self.codeEdit.setAutoIndent(True)
        self.codeEdit.setBackspaceUnindents(True)
        self.codeEdit.setTabWidth(4)

        # indentation guides
        self.codeEdit.setIndentationGuides(True)

        # folding margin
        self.codeEdit.setFolding(QsciScintilla.PlainFoldStyle)
        self.codeEdit.setMarginWidth(2, 12)

        # 自动换行
        self.codeEdit.setWrapMode(QsciScintilla.WrapWord)

    def onLinesChanged(self):
        # 动态设置左边的边距
        self.codeEdit.setMarginWidth(
            0, self.codeEdit.fontMetrics().width(str(self.codeEdit.lines())) + 5)

    def onMessageReceived(self, data):
        # 接收到ps返回的结果就关闭进度条
        self.closeWait()
        if data.find(b'disconnecting') > -1:
            self._passwordError = True
            # 密码错误
            QMessageBox.critical(self, '错误', '密码错误')
            return
        self._passwordError = False
        # 解码数据
        try:
            message = Protocol.unpack(data)
            print('message:', message)
            data = message.data.decode()
            print('data:', data)
        except Exception as e:
            self.resultEdit.append('解码数据错误: ' + str(e))
            return
        self.resultEdit.append(data)
        if len(data) < 6:
            return
        # 尝试解析消息
        try:
            data = json.loads(data)
            # 获取版本
            version = data.get('version', '0.')
            if not version or int(version.split('.')[0]) < 18:
                QMessageBox.information(
                    self, '提示', '未能获取到版本或者版本号小于18（PS 2017）')
                return
            # 获取可能需要调用的函数和参数
            method = data.get('method', 'nomethod')
            params = data.get('params', [])
            if hasattr(self, method):  # 调用函数
                getattr(self, method)(*params)
        except Exception as e:
            print('解析数据错误:', e)
            traceback.print_exc()

    def onConnectSuccessed(self):
        # 连接成功发送代码验证密码是否正确
        self.closeWait()  # 关闭正在连接中的进度条
        self._client.write(Protocol.pack(CodeGetVersion, 2))
        self._client.flush()
        Protocol.increase()
        self.showWait('正在验证密码...')

    def onConnectClosed(self, message=None):
        # 连接被断开
        self.closeWait()
        if self._passwordError:
            return
        if QMessageBox.question(
                self, '错误', message + '\n是否重连？',
                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            # 重连
            self.on_buttonConnect_clicked()

    def showMessage(self, message):
        # 显示消息
        if message:
            # unquote 尝试对消息反编码
            QMessageBox.information(self, '提示', unquote(message))

    @pyqtSlot()
    def on_buttonResetCode_clicked(self):
        # 重置代码区域为默认
        self.codeEdit.setText(Template)

    @pyqtSlot()
    def on_buttonGetImage_clicked(self):
        # 获取ps中的图片过来显示
        pass

    @pyqtSlot()
    def on_buttonConnect_clicked(self):
        # 连接ps的按钮
        if self._client.state() == self._client.ConnectedState:
            # 如果已经连接上了则跳过
            return
        # 保存ps的地址端口和密码
        self._setting.setValue(
            'lineEditAddress', self.lineEditAddress.text().strip())
        self._setting.setValue('spinBoxPsPort', self.spinBoxPsPort.value())
        self._setting.setValue(
            'lineEditPassword', self.lineEditPassword.text().strip())
        self._setting.sync()
        # 构建协议类（用于传递数据的加密）
        Protocol.init(self.lineEditPassword.text().strip())
        # 开始连接ps
        self._client.connectToHost(
            self.lineEditAddress.text().strip(), self.spinBoxPsPort.value())
        # 显示进度条
        self.showWait('正在连接中')

    @pyqtSlot()
    def on_runButton_clicked(self):
        # 运行按钮
        code = self.codeEdit.text().strip()
        if not code:
            return
        if self._client.state() == self._client.ConnectedState and self._client.isWritable():
            # 保存参数和代码
            self._setting.setValue(
                'argsEdit', self.argsEdit.toPlainText().strip())
            self._setting.setValue(
                'codeEdit', self.codeEdit.text().strip())
            self._setting.sync()
            self._client.write(Protocol.pack(self.formatCode(code), 2))  # 发送数据
            self._client.flush()
            Protocol.increase()  # 自增1
            self.showWait('正在处理中...')  # 显示进度条
        else:
            QMessageBox.critical(self, '错误', '未连接或者不能发送数据')

    def formatCode(self, code):
        # 格式化code
        code = code.replace(
            '// #Function#', self.argsEdit.toPlainText().strip())
        print('格式化code, 长度: ', len(code))
        return code

    def showWait(self, text):
        # 显示等待进度条
        self._wdialog = QProgressDialog(text, '', 0, 0, self)
        self._wdialog.setWindowFlags(
            self._wdialog.windowFlags() | Qt.FramelessWindowHint)
        self._wdialog.setWindowModality(Qt.WindowModal)
        self._wdialog.setWindowTitle('请稍候')
        self._wdialog.setCancelButton(None)
        self._wdialog.show()

    def closeWait(self):
        # 隐藏或者关闭等待进度条
        self._wdialog.accept()

    def closeEvent(self, event):
        # 断开和ps的连接
        self._client.blockSignals(True)
        self._client.abort()
        self._client.deleteLater()
        super(Window, self).closeEvent(event)


if __name__ == '__main__':
    import sys
    import cgitb
    sys.excepthook = cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    w = Window()
    w.show()
    sys.exit(app.exec_())
