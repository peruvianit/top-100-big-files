import sys
import os

from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction

import matplotlib
matplotlib.use('QtAgg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot as plt

from utils.FileHelper import FileDetails


class MplCanvas(FigureCanvas):

    def __init__(self):
        fig = plt.figure()
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        exportAct = QAction(QIcon('images/export.png'), '&Exit', self)
        exportAct.setShortcut('Ctrl+Q')
        exportAct.setStatusTip('Export json')
        exportAct.triggered.connect(QApplication.instance().quit)

        exitAct = QAction(QIcon('images/exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(QApplication.instance().quit)

        helpAct = QAction('&About', self)
        helpAct.setStatusTip('About')
        helpAct.triggered.connect(self.helpMenuClick)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        helpMenu = menubar.addMenu('&Help')
        fileMenu.addAction(exitAct)
        helpMenu.addAction(helpAct)

        # config windows
        self.setGeometry(300, 300, 900, 700)
        self.setWindowTitle('Top 100 Big files')

        # GUI elements
        # Create central widget and layout
        self._centralWidget = QWidget()
        self._verticalLayout = QVBoxLayout()
        self._centralWidget.setLayout(self._verticalLayout)

        # Set central widget
        self.setCentralWidget(self._centralWidget)

        self.addForm()
        self.addCopyRight()

    def addForm(self):
        formLayout = QFormLayout()

        self.nameField = QLineEdit("c:\\")
        self.nameField.setDisabled(True)

        buttonPath = QPushButton("Change directory")
        buttonPath.clicked.connect(self.change_directory)

        buttonRun = QPushButton("Run")
        buttonRun.clicked.connect(self.run_analizer)

        self.buttonDelete = QPushButton("Delete selection")
        self.buttonDelete.clicked.connect(self.delete_files)
        self.buttonDelete.setDisabled(True)

        buttonGroup = QGroupBox()
        buttonGroup.setStyleSheet("QGroupBox { border: 0px;}")

        horizontalButtonLayout = QHBoxLayout()
        horizontalButtonLayout.addWidget(buttonRun)
        horizontalButtonLayout.addWidget(self.buttonDelete)
        buttonGroup.setLayout(horizontalButtonLayout)

        listLabel = QLabel('Files')
        self.listFileField = QListWidget()
        self.listFileField.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.listFileField.setFixedHeight(200)

        filesGroup = QGroupBox()
        filesGroup.setStyleSheet("QGroupBox { border: 0px; }")
        horizontalFilesLayout = QHBoxLayout()
        horizontalFilesLayout.addWidget(self.listFileField)
        filesGroup.setLayout(horizontalFilesLayout)

        listExternsionsLabel = QLabel('Extensions')
        self.listExtensionsField = QListWidget()

        self.workFileField = QLineEdit()
        self.workFileField.setDisabled(True)

        self.canvas = MplCanvas()

        extensionsGroup = QGroupBox()
        extensionsGroup.setStyleSheet("QGroupBox { border: 1px; padding:0; margin: 0}")

        horizontalExtensionsLayout = QHBoxLayout()
        horizontalExtensionsLayout.addWidget(self.listExtensionsField, stretch=1)
        horizontalExtensionsLayout.addWidget(self.canvas, stretch=1)
        extensionsGroup.setLayout(horizontalExtensionsLayout)

        formLayout.addRow(buttonPath, self.nameField)
        formLayout.addRow(None, buttonGroup)
        formLayout.addRow(listLabel, filesGroup)
        formLayout.addRow(listExternsionsLabel, extensionsGroup)
        formLayout.addRow(None, self.workFileField)

        self._verticalLayout.addLayout(formLayout)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)


    def addCopyRight(self):
        copyRight = QLabel(
            'Copyright © <a href="https://peruvianit.github.io/">Peruvianit</a> 2023')
        copyRight.setOpenExternalLinks(True)
        self._verticalLayout.addWidget(copyRight, alignment=Qt.AlignmentFlag.AlignRight)


    def helpMenuClick(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Author")
        dlg.setText('''Author : Peruvianit
Email  : sergioarellanodiaz@gmail.com
        ''')
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Ok:
            dlg.close()

    def change_directory(self):
        self.clear_controls()
        folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.nameField.setText(folderpath)

    def run_analizer(self):
        self.clear_controls()
        FileDetails.clear_list_file()
        verify_top_files_big_size(self, self.nameField.text())
        self.update_chart()

    def delete_files(self):

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Delete files!")
        dlg.setText("Confirm to continue with the cancellation?")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Yes:
            for item in self.listFileField.selectedItems():
                try:
                    file_path = item.text().replace('/','\\').split("#-->")[0].strip()
                    FileDetails.remove_file(file_path)
                    self.listFileField.takeItem(self.listFileField.row(item))

                except OSError as e:
                    print(f'[{file_path}] {e.strerror}')

        self.refresh_list(FileDetails.get_list_file())

    def update_message(self, message):
        self.workFileField.setText(message)

    def clear_controls(self):
        self.listFileField.clear()
        self.listExtensionsField.clear()
        self.statusBar.clearMessage()
        self.workFileField.clear()

    def human_size(self, bytes, units=[' bytes','KB','MB','GB','TB', 'PB', 'EB']):
        """ Returns a human readable string representation of bytes """
        return str(bytes) + units[0] if bytes < 1024 else self.human_size(bytes>>10, units[1:])

    def refresh_list(self, listFiles):
        self.clear_controls()

        # files founds
        for file in listFiles:
            item = QListWidgetItem(f"{file.name} #--> ( {self.human_size(file.size)})")
            self.listFileField.addItem(item)

        # extensions founds
        for key, value in FileDetails.analizer_extensions().items():
            item = QListWidgetItem(f"{key} \t ({value}) concurrence")
            self.listExtensionsField.addItem(item)

        self.buttonDelete.setDisabled(False if len(listFiles) > 0 else True)

        self.update_chart()


    def update_chart(self):
        extensions = []
        value_extensions = []

        for key, value in FileDetails.analizer_extensions().items():
            extensions.append(key)
            value_extensions.append(value)
        self.canvas.figure.clf()
        self.ax = self.canvas.figure.add_axes([0,0,1,1])
        self.ax.pie(value_extensions, labels = extensions)

        self.canvas.draw()

def verify_top_files_big_size(mainWindows: MainWindow, path: str):

    totalFiles = 0
    totalSize = 0
    for base, dirs, files in os.walk(path):
        for file in files:
            try:
                path_file = os.path.join(base, file)
                file_size = os.path.getsize(path_file)

                if FileDetails.add_file(FileDetails(os.path.abspath(path_file), file_size)):
                    mainWindows.refresh_list(FileDetails.get_list_file())

                mainWindows.update_message(path_file)
                mainWindows.repaint()
                totalFiles += 1
                totalSize += file_size
                mainWindows.statusBar.showMessage(f"File analyzer count {totalFiles} with a total of ({mainWindows.human_size(totalSize)}) bytes")

            except:
                print(f'problemi con la lettura del file {path_file}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()

    sys.exit(app.exec())
