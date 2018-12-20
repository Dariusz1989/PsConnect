#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QRectF, QPointF, QSizeF, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,\
    QPushButton, QApplication


# Created on 2018年7月24日
# author: Irony
# site: https://github.com/892768447
# email: 892768447@qq.com
# file: ImageWidget
# description:
__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


class ImageWidget(QGraphicsView):

    def __init__(self, *args, **kwargs):
        super(ImageWidget, self).__init__(*args, **kwargs)
        self.setObjectName('graphicsView')
        self.setBackgroundBrush(QColor(25, 25, 25))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing |
                            QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)
        self.setCacheMode(self.CacheBackground)
        self.setViewportUpdateMode(self.SmartViewportUpdate)

        self._zoomDelta = 0.1
        self._pixmap = None
        self._item = QGraphicsPixmapItem()
        self._item.setFlags(QGraphicsPixmapItem.ItemIsFocusable |
                            QGraphicsPixmapItem.ItemIsMovable)

        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)

        self._scene.addItem(self._item)

    def pixmap(self):
        return self._pixmap

    def setPixmap(self, pixmap, fitIn=True):
        self._pixmap = pixmap
        self._item.setPixmap(pixmap)
        self._item.update()
        self.setSceneDims()
        if fitIn:
            self.fitInView(QRectF(self._item.pos(), QSizeF(
                self._pixmap.size())), Qt.KeepAspectRatio)
        self.update()

    def setSceneDims(self):
        if not self._pixmap:
            return
        self.setSceneRect(
            QRectF(
                QPointF(0, 0),
                QPointF(self._pixmap.width(), self._pixmap.height()))
        )

    def fitInView(self, rect, flags=Qt.IgnoreAspectRatio):
        if not self.scene() or rect.isNull():
            return
        unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
        self.scale(1 / unity.width(), 1 / unity.height())
        viewRect = self.viewport().rect()
        sceneRect = self.transform().mapRect(rect)
        xratio = viewRect.width() / sceneRect.width()
        yratio = viewRect.height() / sceneRect.height()
        if flags == Qt.KeepAspectRatio:
            xratio = yratio = min(xratio, yratio)
        elif flags == Qt.KeepAspectRatioByExpanding:
            xratio = yratio = max(xratio, yratio)
        self.scale(xratio, yratio)
        self.centerOn(rect.center())

    def getPos(self, pos):
        spos = self.mapToScene(pos)
        pos = self._item.mapFromScene(spos)
        return pos.toPoint() if self._item.boundingRect().contains(pos) else QPoint()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoomIn()
        else:
            self.zoomOut()

    def zoomIn(self):
        """放大"""
        self.zoom(1 + self._zoomDelta)

    def zoomOut(self):
        """缩小"""
        self.zoom(1 - self._zoomDelta)

    def zoom(self, scaleFactor):
        """
        # 缩放
        :param scaleFactor: 缩放的比例因子
        """
        factor = self.transform().scale(
            scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()
        if factor < 0.07 or factor > 100:
            # 防止过大过小
            return
        self.scale(scaleFactor, scaleFactor)


class ImageView(ImageWidget):

    def __init__(self, *args, **kwargs):
        super(ImageView, self).__init__(*args, **kwargs)
        self.setWindowTitle('图片预览')
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        rect = QApplication.instance().desktop().availableGeometry(self)
#         self.setGeometry(rect)
        self.resize(int(rect.width() * 2 / 3), int(rect.height() * 2 / 3))
#         self.showMaximized()
        self.buttonClose = QPushButton(
            'r', self, objectName='buttonClose', visible=not self.parent())
        self.buttonClose.clicked.connect(self.close)
        self.buttonClose.setMinimumSize(30, 30)
        self.buttonClose.setMaximumSize(30, 30)
        self.buttonClose.setStyleSheet("""
        #buttonClose {
            border: none;
            color: balck;
            font: 16px "Webdings";
            background-color: rgba(255, 0, 0, 150);
        }
        #buttonClose:hover {
            background-color: rgba(255, 0, 0, 200);
        }
        #buttonClose:pressed {
            background-color: rgba(255, 0, 0, 150);
        }""")
        self.buttonClose.setGeometry(self.width() - 30, 0, 30, 30)

    def resizeEvent(self, event):
        super(ImageView, self).resizeEvent(event)
        if hasattr(self, 'buttonClose'):
            self.buttonClose.setGeometry(self.width() - 30, 0, 30, 30)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = ImageView()
    w.setPixmap(QPixmap('images/ScreenShot1.png'))
    w.show()
    sys.exit(app.exec_())
