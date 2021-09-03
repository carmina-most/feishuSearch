import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets
from base_main_window import BaseUiFeishuDoc
import asyncio
from feishu_doc import execute_search, to_feishu_doc
from auth import pre_auth
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QFont
from hot_key_thread import HotKeyThread


class MyWindow(QMainWindow, BaseUiFeishuDoc):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.hotKey = HotKeyThread(self)
        self.lineEdit.returnPressed.connect(self.search_enter)
        self.listWidget.itemActivated.connect(self.enter)
        self.login()

    def enter(self, item):
        url = item.toolTip()
        to_feishu_doc(url.strip())
        self.ui.setHidden(True)

    def login(self):
        asyncio.get_event_loop().run_until_complete(pre_auth())

    # 检测键盘回车按键
    def search_enter(self):
        text = self.lineEdit.text()
        if text.strip() == '':
            return
        feishu_list = asyncio.get_event_loop().run_until_complete(execute_search(text.strip()))
        if len(feishu_list) != 0:
            self.listWidget.clear()
            for content in feishu_list:
                item = QtWidgets.QListWidgetItem()
                self.set_item_style(item)
                item.setText(content['message'])
                item.setToolTip(content['url'])
                self.listWidget.addItem(item)
            self.set_item_style(self.listWidget.item(0), 0)
            self.set_listWidget_style(self.listWidget, self.listWidget.item(0))
            self.listWidget.show()
            self.listWidget.setFocus()
        else:
            self.listWidget.hide()


    def set_item_style(self, item, index=1):
        if index == 0:
            item.setSelected(True)
        font = QFont()
        font.setPointSize(15)
        item.setFont(font)
        item.setSizeHint(QSize(30, 60))
        item.setIcon(QIcon('link.png'))

    def set_listWidget_style(self, list_widget, item):
        list_widget.setIconSize(QSize(25, 25))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    app.setWindowIcon(QIcon('./antenna.png'))
    myWin.show()
    sys.exit(app.exec_())
