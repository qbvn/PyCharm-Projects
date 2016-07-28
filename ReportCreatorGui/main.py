# -*- coding: iso-8859-1 -*-

from PySide.QtGui import QDialog, QVBoxLayout, QDialogButtonBox, QApplication, QListWidget, \
    QAbstractItemView, QLabel, QGridLayout, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PySide.QtCore import Qt, QDateTime
import PySide.QtCore, PySide.QtGui
import os, pickle, time
import XmlAnalysis
# Load the dictionary back from the pickle file.


PICKLE_TEMP_FILE = "tempPath.p"

class ConfigLineDir(QGridLayout):
    def __init__(self, label, mode):
        QGridLayout.__init__(self)

        self.labelTestRuns = QLabel(label)
        self.editText = QLineEdit()
        self.mode = mode
        self.fileDlg = QFileDialog
        self.editText.setText(os.getcwd())
        if mode == "dir":
            self.editText.setStyleSheet("* { background-color: rgba(0, 0, 0, 0); }")
            self.editText.setReadOnly(True)
            self.buttonDir = QPushButton("Verzeichnis")
            self.buttonDir.clicked.connect(self.dirDialog)
        else:
            self.buttonDir = QPushButton("Datei")
            self.buttonDir.clicked.connect(self.dirFile)

        self.setColumnMinimumWidth(0, 120)
        self.addWidget(self.labelTestRuns, 0, 0, Qt.AlignLeft)
        self.addWidget(self.editText, 0, 1)
        self.addWidget(self.buttonDir, 0, 2)
        self.editText.textChanged.connect(self.checkLineEdits)
        self.OrgStyle = self.editText.styleSheet()

    def checkLineEdits(self):
        if self.mode == "dir":
            state = self.checkDir(self.editText.text())
            self.markLineEditFalse(self.editText, state)
        else:
            state = self.checkFile(self.editText.text())
            self.markLineEditFalse(self.editText, state)

    def checkDir(self, dir):
        return (os.path.isdir(dir))

    def checkFile(self, file):
        return (os.path.exists(file))

    def markLineEditFalse(self, le, state):
        if not state:
            le.setStyleSheet("border: 1px solid red;")
        else:
            le.setStyleSheet(self.OrgStyle)

    def dirDialog(self):
        dateipfad = self.fileDlg.getExistingDirectory(None, u"Verzeichnis wählen", self.getText())
        if os.path.isdir(dateipfad):
            pickle.dump(dateipfad, open(PICKLE_TEMP_FILE, "wb"))
            self.editText.setText(dateipfad)
        #print(dateipfad)

    def dirFile(self):
        dateipfad = QFileDialog.getOpenFileName(None, u"Datei wählen",
                                                u"../../")
        if dateipfad != "":
            self.editText.setText(dateipfad)
            # print(dateipfad)

    def getText(self):
        return (self.editText.text())

    def setText(self, text):
        self.editText.setText(text)


class MultiListDialog(QDialog):
    def __init__(self, items):  # , parent=None
        super(MultiListDialog, self).__init__()  # parent
        self.resize(800, 550)
        self.entries = items
        layout = QVBoxLayout(self)

        self.listWidget = QListWidget(self)
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.HlineInputfiles = ConfigLineDir(u"Verzeichnis NI XML:", "dir")
        self.HlineOutputfiles = ConfigLineDir(u"Verzeichnis Report:", "dir")
        if os.path.isfile(PICKLE_TEMP_FILE):
            pkl_file = open(PICKLE_TEMP_FILE, 'rb')
            inPath = pickle.load(pkl_file)
            outPath = pickle.load(pkl_file)
            pkl_file.close()
            if os.path.isdir(inPath):
                self.HlineInputfiles.editText.setText(inPath)
            if os.path.isdir(outPath):
                self.HlineOutputfiles.editText.setText(outPath)
        layout.addLayout(self.HlineInputfiles)
        layout.addLayout(self.HlineOutputfiles)
        layout.addWidget(self.listWidget)

        layout.addWidget(QLabel("Mehrfachauswahl -> Strg + Mausklick"))

        # OK and Cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Close, Qt.Horizontal, self)
        # Apply before Close
        buttons.setStyleSheet("* { button-layout: 2 }")
        layout.addWidget(buttons)

        buttons.rejected.connect(self.close)
        buttons.button(QDialogButtonBox.Apply).clicked.connect(self.Apply_Clicked)

        self.SetListItems()
        self.HlineInputfiles.editText.textChanged.connect(self.RefreshList)
        self.HlineInputfiles.editText.textChanged.connect(self.SetListItems)

    # def SetOutputDir(self):
    #     self.HlineOutputfiles.editText.setText(self.HlineInputfiles.getText())

    def SetListItems(self, parent=None):
        itemslist = os.listdir(self.HlineInputfiles.getText())
        for it in itemslist:
            if it.endswith(".xml"):
                self.listWidget.addItem(it)

    def GetMarkedItems(self):
        results = []
        try:
            for el in self.listWidget.selectedItems():
                results.append(str(el.text()))
            return (results)

        except:
            return (None)

    def RefreshList(self):
        self.listWidget.clear()
        print "refresh"

    def Apply_Clicked(self):
        SelectedItems = self.GetMarkedItems()
        textMsg = "Selektierte Dateie(n):\r\n"
        if len(SelectedItems) > 0:
            for file in SelectedItems:
                filePath = os.path.join(self.HlineInputfiles.getText(), file)
                textMsg += (file + "\r\n")
                XmlAnalysis.XmlAnalysis(filePath, self.HlineOutputfiles.getText())

            #QMessageBox.information(self, "Report", textMsg)
            textMsg += "\r\nReport-Verzeichnis öffnen?\r\n"
            msgBox = QMessageBox.StandardButton.Yes
            msgBox |= QMessageBox.StandardButton.No
            if QMessageBox.question(self, "Report", textMsg, msgBox) == QMessageBox.Yes:
                os.startfile(self.HlineOutputfiles.getText())

        else:
            QMessageBox.warning(self, "Achtung", "Keine Datei selektiert!")
            pass

if __name__ == "__main__":
    app = QApplication([])
    pixmap = PySide.QtGui.QPixmap("MarvelSS.png")
    splash = PySide.QtGui.QSplashScreen(pixmap)
    splash.show()
    time.sleep(1)
    dialog = MultiListDialog([])
    splash.finish(dialog)
    dialog.exec_()
    pkl_file = open(PICKLE_TEMP_FILE, 'wb')
    pickle.dump(dialog.HlineInputfiles.getText(), pkl_file)
    pickle.dump(dialog.HlineOutputfiles.getText(), pkl_file)
    pkl_file.close()
    del app

