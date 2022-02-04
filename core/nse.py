import requests
import json
import datetime
import nepali_datetime
import os
from openpyxl import Workbook
import csv


class NSE:
    def __init__(self):
        self.status = json.loads(open('core/status.json', 'r').read())
        if(os.path.isfile('data/data.json') and os.path.isfile('data/data.html')):
            self.json = self.read_json()
            self.html = self.read_html()
            print("Loaded from cache")
        else:
            self.reload()
            print("Data Reloaded")

        if(self.check_internet()):
            if(self.status['last_modified'] != self.todaysdate()):
                self.reload()
            else:
                print("data is update data!")
        else:
            print("Unable to update data,No internet connection !")

    def save_file(self, filename, content):
        csv = open('data/data.csv', 'r')
        data = []
        for x in csv:
            data.append(x.split(',')[:-1])
        open('data/data.json', 'w').write(json.dumps(data))

    def read_json(self):
        try:
            return open('data/data.json', 'r').read()
        except:
            return False

    def read_html(self):
        try:
            return open('data/data.html', 'r').read()
        except:
            return False

    def masterPage(self):
        script = open('assets/main.js', 'r').read()
        css = open('assets/main.css', 'r').read()
        return """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
                <style>
                """+css+"""
                </style>
                </head>
                <body>
                        <div id="app"></div>
                        <script>
                        const saved_date=`"""+self.todaysdate()+"""`;
                        const table=`
                        """+self.read_html()+"""
                        `;
                        """+script+"""
                        </script>
                </body>
                </html>
                """

    def todaysdate(self):
        datetime.date.today()
        return str(nepali_datetime.date.today())

    def check_internet(self):
        url = "https://www.google.com"
        timeout = 5
        try:
            request = requests.get(url, timeout=timeout)
            print("Connected to the Internet")
            return True
        except (requests.ConnectionError, requests.Timeout) as exception:
            print("No internet connection.")
            return False

    def reload(self):
        self.html = requests.get(
            'http://www.nepalstock.com/todaysprice/export').text
        self.save_file('data.html', self.html)
        self.save_csv()
        self.save_excel()
        self.save_json()
        self.status['last_modified'] = self.todaysdate()
        open('core/status.json', 'w').write(json.dumps(self.status))

    def save_csv(self):
        try:
            html = open('data/data.html', 'r').read()
            html = html.replace('<table border="1">', '')
            html = html.replace('</table>', '')
            html = html.replace('<tr>', '\n')
            html = html.replace('</tr>', '')
            html = html.replace('<td>', '')
            html = html.replace('<th>', '')
            html = html.replace('</td>', ',')
            html = html.replace('</th>', ',')
            open('data/data.csv', 'w').write(html.strip())
            return True
        except:
            return False

    def save_excel(self):
        wb = Workbook()
        ws = wb.active
        with open('data/data.csv', 'r') as f:
            for row in csv.reader(f):
                ws.append(row)
        wb.save('data/data.xlsx')

    def save_json(self):
        csv = open('data/data.csv', 'r')
        data = []
        for x in csv:
            data.append(x.split(',')[:-1])
        open('data/data.json', 'w').write(json.dumps(data))
