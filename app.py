import os
from PyQt5.QtCore import QObject, pyqtSlot, QVariant
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5 import QtGui
from core.render import Render
import nepali_datetime
import shutil
from core.nse import NSE

render = Render()
nse = NSE()


class CallHandler(QObject):

    @pyqtSlot(QVariant, result=QVariant)
    def exportFile(self, type):
        self.parent.getSaveFileName(type)
        return QVariant({"status": "success", "message": "File exported successfully"})

    @pyqtSlot(result=QVariant)
    def reloadData(self):
        nse.reload()
        print('Data Updated !')
        return QVariant({
            "status": "success",
            "message": "Data reloaded successfully",
            "data": {
                "table": nse.read_html(),
                "last_modified": nse.status['last_modified']
            }
        })

    @pyqtSlot(QVariant, result=QVariant)
    def console_log(self, message):
        print("js : " + message)
        return "success"


class WebView(QWebEngineView):

    def __init__(self):
        super(WebView, self).__init__()
        self.setWindowIcon(QtGui.QIcon('assets/icon.png'))
        self.setWindowTitle("Nepali Stock Exchange")
        self.setMinimumSize(950, 530)
        self.channel = QWebChannel()
        self.handler = CallHandler()
        self.handler.parent = self
        self.channel.registerObject('handler', self.handler)
        self.page().setWebChannel(self.channel)
        self.setHtml(render.master())

    @pyqtSlot()
    def getSaveFileName(self, type):
        file_filter = ''
        error = False
        extension = ''
        content = ''
        dt = nepali_datetime.datetime.now()
        if(type == "excel"):
            extension = '.xlsx'
            file_filter = 'Excel File (*.xlsx)'
            content = 'data/data.xlsx'
        elif(type == "csv"):
            extension = '.csv'
            file_filter = 'CSV File (*.csv)'
            content = 'data/data.csv'
        elif(type == "json"):
            extension = '.json'
            file_filter = 'JSON File (*.json)'
            content = 'data/data.json'
        else:
            print("Invalid file type")
        if(error == False):
            response = QFileDialog.getSaveFileName(
                parent=self,
                caption='Select a data file',
                directory=str(dt)+extension,
                filter=file_filter,
                initialFilter='Excel File (*.xlsx)'
            )
            print(response[0])
            if(response[0] != ''):
                if(os.path.exists(response[0])):
                    os.remove(response[0])
                shutil.copyfile(content, response[0])


if __name__ == "__main__":
    app = QApplication([])
    view = WebView()
    view.show()
    app.exec_()
