from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from system_hotkey import SystemHotkey


class HotKeyThread(QThread, SystemHotkey):
    trigger = pyqtSignal()

    def __init__(self, main_window):
        self.ui = main_window
        super(HotKeyThread, self).__init__()
        self.register(('control', 'y'), callback=lambda x: self.start())
        self.trigger.connect(self.hotKeyEvent)

    def run(self):
        self.trigger.emit()

    def hotKeyEvent(self):
        if self.ui.isHidden():
            self.ui.setHidden(False)
            if self.ui.windowState() == QtCore.Qt.WindowMinimized:
                self.ui.showNormal()
            self.ui.raise_()
            self.ui.activateWindow()
        else:
            self.ui.setHidden(True)

    def quitThread(self):
        if self.isRunning():
            self.quit()
