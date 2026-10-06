import hashlib

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QApplication, QPushButton,
    QGridLayout, QFileDialog, QLabel, QLineEdit
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SHA-256 File Hash Checker")
        self.file = None          # path of the selected file
        self.file_hash = None     # the computed hash

        layout = QGridLayout()

        # row 0: pick a file
        selectButton = QPushButton("Select File", self)
        selectButton.clicked.connect(self.SelectFile)
        self.fileLabel = QLabel("No File Selected", self)

        # row 1: compute and show the hash
        computeButton = QPushButton("Compute Hash", self)
        computeButton.clicked.connect(self.ComputeHash)
        self.hashOutput = QLineEdit(self)
        self.hashOutput.setReadOnly(True)   # user can copy it but not edit it
        self.hashOutput.setPlaceholderText("File hash will appear here")

        # row 2: paste the expected hash
        expectedLabel = QLabel("Expected hash:", self)
        self.hashInput = QLineEdit(self)
        self.hashInput.setPlaceholderText("Paste the hash you want to check against")

        # row 3: compare and show the result
        compareButton = QPushButton("Compare", self)
        compareButton.clicked.connect(self.CompareHash)
        self.resultLabel = QLabel("", self)

        # place everything in the grid: (widget, row, column)
        layout.addWidget(selectButton, 0, 0)
        layout.addWidget(self.fileLabel, 0, 1)
        layout.addWidget(computeButton, 1, 0)
        layout.addWidget(self.hashOutput, 1, 1)
        layout.addWidget(expectedLabel, 2, 0)
        layout.addWidget(self.hashInput, 2, 1)
        layout.addWidget(compareButton, 3, 0)
        layout.addWidget(self.resultLabel, 3, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.resize(700, 180)

    # attempt based on the practice2 txt file from class
    # def SelectFile(self):
    #     f = QFileDialog.getOpenFileName(self, "Select file clicked", filter=None)
    #     self.file = f[0]
    #     self.fileLabel.setText("File Selected: " + self.file)
 
    def SelectFile(self):
        f = QFileDialog.getOpenFileName(self, "Select a File", filter=None)
        if f[0]:                       # empty string = user canceled
            self.file = f[0]
            self.file_hash = None      # old hash does not apply to the new file
            self.fileLabel.setText("File Selected: " + self.file)
            self.hashOutput.clear()
            self.resultLabel.setText("")
 
    def ComputeHash(self):
        # check if a file was selected
        if not self.file:
            self.resultLabel.setText("Please select a file first.")
            return
 
        # read the file in 4096-byte chunks so large files don't fill up memory
        sha = hashlib.sha256()
        try:
            with open(self.file, "rb") as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    sha.update(chunk)
        except OSError:
            self.file_hash = None
            self.hashOutput.clear()
            self.resultLabel.setText("Could not read this file.")
            return
            
        # save the result and display it
        self.file_hash = sha.hexdigest()
        self.hashOutput.setText(self.file_hash)
        self.resultLabel.setText("")   # clear past comparson result
 

    def CompareHash(self):
        if not self.file_hash:
            self.resultLabel.setText("Please compute the hash first.")
            return 
        expected = self.hashInput.text().strip().lower()
        if not expected:
            self.resultLabel.setText("Please paste a hash to compare.")
            return
        if expected == self.file_hash:
            self.resultLabel.setText("Hash matches!")
        else:
            self.resultLabel.setText("Hash does not match.")


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
