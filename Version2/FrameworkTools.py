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
import os
import subprocess
import tempfile

from PyQt5.Qsci import QsciLexerJavaScript, QsciScintilla, QsciAPIs
from PyQt5.QtCore import QSettings, pyqtSlot, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtNetwork import QTcpServer, QHostAddress
from PyQt5.QtWidgets import QFileDialog, QWidget, QMessageBox
import xxtea

from UiFrameworkTools import Ui_FormFrameworkTools


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"

# 案例模版
Template = r"""#target photoshop

// 首先就是要删除自己
(new File($.fileName)).remove();

// 引入加密函数库xxtea
#include "#2#"

// 引入混淆后的功能脚本路径
#include "#3#"

try {
    var socket = new Socket;        // 创建socket连接
    socket.timeout = 20;            // 设置超时20秒
    if(socket.open("127.0.0.1:49496")) {
        // 如果连接上软件客服端才能继续操作
        // 开始发送请求参数的命令
        
        // 发送一行代码,使用xxtea加密并编码为base64
        // getArgs表示要调用的远程方法名字|[参数数组], 后面的16位为密匙, 密匙要和服务端一致, 或者不同的函数用不同的密匙
        socket.writeln(XXTEA.encryptToBase64("getCode|[]", "0123456789abcdef"));

        // 接收传回来的一行消息
        var data = socket.readln().split("\n").splice(0, 1)[0];
        // 对数据进行解密
        method = XXTEA.decryptFromBase64(data, "0123456789abcdef");
        
        try {
            (new Function(method))();        // 动态执行字符串函数method
            alert('调用函数' + method + ' 完毕');
        } catch(e) {
            // 脚本执行失败
            socket.writeln(XXTEA.encryptToBase64("showError|['" + e.message.replace("'", "").replace('"', "") + "']", "0123456789abcdef"));
        }

        // 处理完成关闭连接
        socket.close();
        delete socket;
    }
} catch(e) {
    alert(e);
}
"""


class Window(QWidget, Ui_FormFrameworkTools):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # 初始化server
        self._server = QTcpServer(self)
        self._server.newConnection.connect(self.onNewConnection)
        self._server.listen(QHostAddress.LocalHost, 49496)
        self._getPsPath()
        self._initCodeEdit()

        # 设置默认代码和参数
        self.argsEdit.setPlainText('testColor("{}")'.format(
            os.path.abspath('Resources/GM6C6860.jpg').replace('\\', '/')))

        self.codeEdit.setText(self._formatArgs(Template))

    def _formatArgs(self, code):
        code = code.replace('#1#', os.path.abspath(
            'Resources/ProgressBar.jsx').replace('\\', '/'))
        code = code.replace('#2#', os.path.abspath(
            'Resources/Core.jsx').replace('\\', '/'))
        code = code.replace('#3#', os.path.abspath(
            'Resources/test.jsx').replace('\\', '/'))
        return code

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

    def _getPsPath(self):
        # 获取ps的路径
        settings = QSettings('FrameworkTools', 'Settings')
        psPath = settings.value('path', '')
        if not psPath:  # 如果没有找到自己保存的路径则去找系统安装的路径
            settings = QSettings(
                'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\Photoshop.exe', QSettings.NativeFormat)
            psPath = settings.value('.', '')
        self.pathEdit.setText(psPath)

    def onNewConnection(self):
        # 当有新的连接来时
        while self._server.hasPendingConnections():
            socket = self._server.nextPendingConnection()
            socket.readyRead.connect(self.onReadyRead)
            if socket.bytesAvailable() > 0:
                # 如果已有数据发送过来
                self.doRecv(socket)

    def onReadyRead(self):
        # 准备接收数据
        socket = self.sender()
        if socket.bytesAvailable() > 0:
            self.doRecv(socket)

    def doRecv(self, socket):
        # 接收数据
        try:
            data = socket.readAll().data().decode()
            # 对数据解密
            data = xxtea.decryptFromBase64(data, '0123456789abcdef')
            method, args = data.split('|')
            self.resultEdit.append('被调用函数: {}, 参数: {}'.format(method, args))
            try:
                args = eval(args)
            except Exception as e:
                args = []
            # 动态执行函数
            if hasattr(self, method):
                getattr(self, method)(socket, *args)
        except Exception as e:
            self.resultEdit.append(str(e))

    def getCode(self, socket):
        # 传递参数的函数
        args = self.argsEdit.toPlainText().strip()
        args = xxtea.encryptToBase64(args, '0123456789abcdef') + '\n'
        print('发送加密数据: ', args)
        socket.write(args.encode())
        socket.flush()

    def showError(self, _, message):
        # 显示错误消息
        if message:
            QMessageBox.critical(self, '错误', message)

    @pyqtSlot()
    def on_selectButton_clicked(self):
        # 手动选择路径
        path, _ = QFileDialog.getOpenFileName(
            self, '选择Ps路径', '', 'Photoshop.exe')
        if path:
            self.pathEdit.setText(path)
            settings = QSettings('FrameworkTools', 'Settings')
            settings.setValue('path', path)
            settings.sync()

    @pyqtSlot()
    def on_runButton_clicked(self):
        # 运行按钮
        code = self.codeEdit.text().strip()
        if not code:
            return
        if not code.startswith('#target'):
            code = '#target photoshop\n' + code
        path = tempfile.mktemp('.jsx')
        open(path, 'wb').write(code.encode('utf-8'))
        subprocess.call([self.pathEdit.text().strip(), path])

    def closeEvent(self, event):
        if self._server.isListening():
            self._server.close()
            self._server.deleteLater()
        super(Window, self).closeEvent(event)


if __name__ == '__main__':
    import sys
    import cgitb
    sys.excepthook = cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
