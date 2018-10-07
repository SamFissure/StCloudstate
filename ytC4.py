from PyQt5.QtCore import pyqtSlot
from selenium import webdriver
from pyqtgraph.Qt import QtGui, QtCore
import time
import numpy as np
import pyqtgraph as pg
from selenium.webdriver import Chrome
from PyQt5.QtWidgets import QLineEdit, QPushButton
from contextlib import closing
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout

common = ["she's", "shes", "i'm", "im", "i", "me", "the", "of", "and", "a", "to", "in", "is", "you", "that", "it", "he",
          "was", "for", "on", "are", "as", "with", "his", "they", "i", "at", "be", "this", "have", "from", "or", "one",
          "had", "by", "word", "but", "not", "what", "all", "were", "we", "when", "your", "can", "said", "there", "use",
          "an", "each", "which", "she", "do", "how", "their", "if", "will", "up", "other", "about", "out", "many",
          "then", "them", "these", "so", "some", "her", "would", "make", "like", "him", "into", "time", "has", "look",
          "two", "more", "write", "go", "see", "number", "no", "way", "could", "people", "my", "than", "does",
          "been", "call", "who", "its", "now", "find", "long", "down", "day", "did", "get", "come", "made",
          "may", "part", "and", "it's"]

options = webdriver.ChromeOptions()
options.binary_location = "/Program Files (x86)/Google/Chrome/Application/chrome.exe"
chrome_driver_binary = "/Users/gdutc/OneDrive/Documents/chromedriver_win32/chromedriver.exe"
options.add_argument("--headless")


def vid(url):
    from collections import Counter
    with closing(Chrome(chrome_driver_binary, chrome_options=options)) as driver:
        wait = WebDriverWait(driver, 10)
        driver.get(url)

        for item in range(5):  # by increasing the highest range you can get more content
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            time.sleep(3)

        x = []
        for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #content-text"))):
            x.append(comment.text)
            # print(comment.text)

    wordstring = ''

    for thing in x:
        try:
            wordstring = wordstring + str(thing)
        except:
            pass

    wordlist = wordstring.split()

    refinedWordList = []
    for w in wordlist:
        if w.lower() not in common:
            refinedWordList.append(w.lower())

    Counter = Counter(refinedWordList)
    most_occur = Counter.most_common(10)
    commonwordcount10 = []
    commonword10 = []

    for word, count in most_occur:
        commonword10.append(word)
        commonwordcount10.append(count)
        print(word, ": ", count)

    print(most_occur)

    top10 = []
    index = 0
    currentMAXINDEX = 0
    count = 0

    print("max index")
    print(currentMAXINDEX)
    print(str(wordlist[currentMAXINDEX]))

    print("top ten")
    for k in top10:
        print(k)

    return commonwordcount10, commonword10


class App(QWidget):
    def __init__(self):
        super().__init__()
        # for 'enter' button
        self.button = QPushButton('Enter', self)
        # for textbox to get user input
        self.textbox = QLineEdit(self)
        # for the bar graph
        self.barGraph = QWidget()
        # for the table
        self.tableWidget = QTableWidget()
        #type of layout
        self.layout = QVBoxLayout()
        # title of windos
        self.title = 'YTGUI'
        # initializes window size
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.textBox()

        # Add table, textbox, button to widget layout
        self.layout.addWidget(self.tableWidget)
        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        # Show widget
        self.show()

    def textBox(self):
        # textbox
        self.textbox.move(20, 20)

        # button
        self.button.move(20, 80)

        # to onClick
        self.button.clicked.connect(self.onClick)
        self.show()

    @pyqtSlot()
    def onClick(self):
        # to retrieve user input
        textboxValue = self.textbox.text()
        # gets the common word count and common word from the specified video
        commonwordcount10, commonword10 = vid(textboxValue)
        # clear text box
        self.textbox.setText("")
        # creates the table and bar graph for the user to view
        self.createTable(commonwordcount10, commonword10)
        self.createBarGraph(commonwordcount10, commonword10)

    def createTable(self, commonwordcount10, commonword10):
        # Create table
        rowCount = 10
        columnCount = 2

        # set the size of the table
        self.tableWidget.setRowCount(rowCount)
        self.tableWidget.setColumnCount(columnCount)

        # populates the table with the retrieved data
        i = 0
        for word in commonword10:
            self.tableWidget.setItem(i, 0, QTableWidgetItem(commonword10[i]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(commonwordcount10[i])))
            i += 1

        self.tableWidget.move(0, 0)

    def createBarGraph(self, commonwordcount10, commonword10):
        xdict = dict(enumerate(commonword10))

        # sets up bar graph
        self.barGraph = pg.PlotWidget()
        win = pg.plot()

        # properties
        self.barGraph.setLabel('left', "Occurrence")
        self.barGraph.setLabel('bottom', 'Word')
        self.barGraph.setXRange(0, 10)
        self.barGraph.setYRange(0, 50)
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict.items()])

        # fills bar graph with data
        self.barGraph = pg.BarGraphItem(x=list(xdict.keys()), height=commonwordcount10, width=0.6, brush='r')
        win.addItem(self.barGraph)

        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())