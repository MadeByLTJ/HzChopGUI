from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
import subprocess
import pathlib
import json

W = 600
H = 600

class LineEdit(QLineEdit):
    def __init__(self, endswith):
        super().__init__()
        self.endswith = endswith
    
    def dragEnterEvent(self, a0):
        if a0.mimeData().hasUrls():
            urls = a0.mimeData().urls()
            if urls:
                path = urls[0].toLocalFile().lower()
                if not path.endswith(self.endswith):
                    a0.ignore()
                    return
                a0.acceptProposedAction()
        else:
            a0.ignore()
    
    def dropEvent(self, a0):
        if a0.mimeData().hasUrls():
            path = a0.mimeData().urls()[0].toLocalFile()
            self.setText(path.replace("/", "\\"))
            a0.acceptProposedAction()

class MainActivity(QWidget):
    def __init__(self):
        super().__init__()
        self.langs = self.loadLang()
        self.defLang = self.langs["en"]
        self.onCreate()
    
    def onCreate(self):
        self.setFixedSize(W, H)
        self.setWindowTitle(self.defLang["windowTitle"])
        if QApplication.styleHints().colorScheme() == Qt.ColorScheme.Light:
            self.setWindowIcon(QIcon(f"{pathlib.Path(__file__).parent}/resources/icon0.png"))
        else:
            self.setWindowIcon(QIcon(f"{pathlib.Path(__file__).parent}/resources/icon1.png"))

        self.h1 = QHBoxLayout()
        self.h2 = QHBoxLayout()
        self.h3 = QHBoxLayout()
        self.h4 = QHBoxLayout()
        self.hParams = []
        self.params = []
        self.v = QVBoxLayout()

        self.menuBar = QMenuBar()
        self.menuLang = QMenu(self.defLang["langSettings"])
        self.langZh = QAction(self.defLang["langZh"])
        self.langEn = QAction(self.defLang["langEn"])
        self.menuAbout = QAction(self.defLang["about"])
        self.langZh.triggered.connect(self.setLangToZh)
        self.langEn.triggered.connect(self.setLangToEn)
        self.menuAbout.triggered.connect(lambda: QMessageBox.information(self, self.defLang["aboutTitle"], self.defLang["aboutText"]))
        self.menuLang.addAction(self.langZh)
        self.menuLang.addAction(self.langEn)
        self.menuBar.addMenu(self.menuLang)
        self.menuBar.addAction(self.menuAbout)

        self.whereIsHzChopLabel = QLabel(self.defLang["whereIsHzChop"])
        self.whereIsHzChopLabel.setFixedWidth(128)
        self.whereIsHzChopLabel.setStyleSheet("font-family: Consolas;")
        self.whereIsHzChopInput = LineEdit(".exe")
        self.whereIsHzChopInput.setStyleSheet("font-family: Consolas; color: #80a040;")
        self.whereIsHzChopButton = QPushButton(self.defLang["browse"])
        self.whereIsHzChopButton.clicked.connect(self.onClick_WhereIsHzChop)
        self.whereIsHzChopButton.setStyleSheet("color: green;")
        self.h1.addWidget(self.whereIsHzChopLabel)
        self.h1.addWidget(self.whereIsHzChopInput)
        self.h1.addWidget(self.whereIsHzChopButton)

        self.whereIsInputMIDILabel = QLabel(self.defLang["whereIsInputMIDI"])
        self.whereIsInputMIDILabel.setFixedWidth(128)
        self.whereIsInputMIDILabel.setStyleSheet("font-family: Consolas;")
        self.whereIsInputMIDIInput = LineEdit(".mid")
        self.whereIsInputMIDIInput.setStyleSheet("font-family: Consolas; color: #80a040;")
        self.whereIsInputMIDIButton = QPushButton(self.defLang["browse"])
        self.whereIsInputMIDIButton.clicked.connect(self.onClick_WhereIsInputMIDI)
        self.whereIsInputMIDIButton.setStyleSheet("color: green;")
        self.h2.addWidget(self.whereIsInputMIDILabel)
        self.h2.addWidget(self.whereIsInputMIDIInput)
        self.h2.addWidget(self.whereIsInputMIDIButton)

        
        self.whereIsOutputMIDILabel = QLabel(self.defLang["whereIsOutputMIDI"])
        self.whereIsOutputMIDILabel.setFixedWidth(128)
        self.whereIsOutputMIDILabel.setStyleSheet("font-family: Consolas;")
        self.whereIsOutputMIDIInput = LineEdit(".mid")
        self.whereIsOutputMIDIInput.setStyleSheet("font-family: Consolas; color: #80a040;")
        self.whereIsOutputMIDIButton = QPushButton(self.defLang["browse"])
        self.whereIsOutputMIDIButton.clicked.connect(self.onClick_WhereIsOutputMIDI)
        self.whereIsOutputMIDIButton.setStyleSheet("color: green;")
        self.h3.addWidget(self.whereIsOutputMIDILabel)
        self.h3.addWidget(self.whereIsOutputMIDIInput)
        self.h3.addWidget(self.whereIsOutputMIDIButton)

        self.logoIcon = QIcon(f"{pathlib.Path(__file__).parent}/resources/logo.png")
        self.startButton = QPushButton(self.logoIcon, self.defLang["start"])
        self.startButton.clicked.connect(self.onClick_Start)
        self.startButton.setIconSize(QSize(72, 36))
        self.startButton.setFont(QFont("新宋体", 18))
        self.startButton.setFixedSize(200, 100)
        self.startButton.setStyleSheet("color: red;")
        self.h4.addWidget(self.startButton)

        self.paramCheckBoxAttributes = [
            "-velSlope", "-phaseCount", "-phaseAmount", "-bassMode", "-ppq", "-bassBoost", 
            "-bassBoostVelo", "-trackMin", "-trackMax", "-channelMin", "-channelMax"
        ]
        self.paramCheckBoxToolTips = self.defLang["toolTips"]
        self.paramSetAttributes = [
            (1.0, 0.1, 5.0, 0.1, 1), (1, 1, 10, 1), (0.01, 0.001, 0.1, 0.001, 3), (0, 0, 5, 1), (1920, 1, 65535, 1), (0, 0, 127, 1),
            (0, 0, 127, 1), (0, 0, 65535, 1), (0, 0, 65535, 1), (0, 0, 15, 1), (15, 0, 15, 1)
        ]

        for c, t, s in zip(self.paramCheckBoxAttributes, self.paramCheckBoxToolTips, self.paramSetAttributes):
            c1 = QCheckBox(c)
            c1.setToolTip(t)
            if isinstance(s[0], float):
                s1 = QDoubleSpinBox()
                s1.setDecimals(s[4])
                s1.setMinimum(s[1])
                s1.setMaximum(s[2])
                s1.setValue(s[0])
                s1.setSingleStep(s[3])
            else:
                s1 = QSpinBox()
                s1.setMinimum(s[1])
                s1.setMaximum(s[2])
                s1.setValue(s[0])
                s1.setSingleStep(s[3])
            
            s1.setEnabled(False)
            c1.toggled.connect(s1.setEnabled)

            self.params.append([c1, s1])

            hTemp = QHBoxLayout()
            hTemp.addWidget(c1)
            hTemp.addWidget(s1)
            self.hParams.append(hTemp)
        
        self.loadLastConfig()

        self.v.addLayout(self.h1)
        self.v.addLayout(self.h2)
        self.v.addLayout(self.h3)
        for h in self.hParams:
            self.v.addLayout(h)
        self.v.addSpacing(20)
        self.v.addLayout(self.h4)
        self.v.addStretch()
        self.v.setMenuBar(self.menuBar)
        
        self.setLayout(self.v)
    
    def onClick_WhereIsHzChop(self):
        hzchop = QFileDialog.getOpenFileName(self, self.defLang["openHzChop"][0], None, self.defLang["openHzChop"][1])[0]
        if hzchop:
            self.whereIsHzChopInput.setText(hzchop.replace("/", "\\"))
    
    def onClick_WhereIsInputMIDI(self):
        input_midi = QFileDialog.getOpenFileName(self, self.defLang["openMIDI"][0], None, self.defLang["openMIDI"][1])[0]
        if input_midi:
            self.whereIsInputMIDIInput.setText(input_midi.replace("/", "\\"))
    
    def onClick_WhereIsOutputMIDI(self):
        output_midi = QFileDialog.getSaveFileName(self, self.defLang["saveMIDI"][0], None, self.defLang["saveMIDI"][1])[0]
        if output_midi:
            self.whereIsOutputMIDIInput.setText(output_midi.replace("/", "\\"))
    
    def onClick_Start(self):
        hzchop = self.whereIsHzChopInput.text()
        input_midi = self.whereIsInputMIDIInput.text()
        output_midi = self.whereIsOutputMIDIInput.text()
        if hzchop:
            if input_midi and output_midi:
                standardCmd = f"{hzchop} {input_midi} {output_midi}"
                for i in self.params:
                    if i[1].isEnabled():
                        standardCmd += f" {i[0].text()} {i[1].value()}"
                process = subprocess.Popen(standardCmd, stdout=subprocess.PIPE, text=True)
                for line in process.stdout:
                    print(line, end="")
                process.wait()
                QMessageBox.information(self, self.defLang["tips"]["infoTitle"], f"{self.defLang["tips"]["infoTextA"]}{pathlib.Path(output_midi).parent}{self.defLang["tips"]["infoTextB"]}")
            else:
                QMessageBox.critical(self, self.defLang["tips"]["errorTitle"], self.defLang["tips"]["error1Text"])
        else:
            QMessageBox.critical(self, self.defLang["tips"]["errorTitle"], self.defLang["tips"]["error2Text"])
        
        params_dict = {}
        for checkbox, spinbox in self.params:
            param_name = checkbox.text()
            params_dict[param_name] = {
                "enabled": checkbox.isChecked(),
                "value": spinbox.value()
            }

        config_data = {
            "hzchopPath": hzchop,
            "inputMIDIPath": input_midi,
            "outputMIDIPath": output_midi,
            "other": params_dict
        }

        self.saveThisConfig(config_data)
    
    def loadLastConfig(self):
        try:
            with open(f"{pathlib.Path(__file__).parent}/data/config.json", "r", encoding="utf-8") as f:
                config = json.loads(f.read())
            
            hzchop = config.get("hzchopPath").replace("/", "\\")
            input_midi = config.get("inputMIDIPath").replace("/", "\\")
            output_midi = config.get("outputMIDIPath").replace("/", "\\")
            
            if hzchop: self.whereIsHzChopInput.setText(hzchop)
            if input_midi: self.whereIsInputMIDIInput.setText(input_midi)
            if output_midi: self.whereIsOutputMIDIInput.setText(output_midi)
            
            other_params = config.get("other", {})
            for checkbox, spinbox in self.params:
                param_name = checkbox.text()
                if param_name in other_params:
                    param_data = other_params[param_name]
                    spinbox.setValue(param_data.get("value", spinbox.minimum()))
                    checkbox.setChecked(param_data.get("enabled", False))
            return config
        
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    def saveThisConfig(self, config_dict):
        try:
            with open(f"{pathlib.Path(__file__).parent}/data/config.json", "w", encoding="utf-8") as f:
                json.dump(config_dict, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(e)

    def loadLang(self):
        with open(f"{pathlib.Path(__file__).parent}/data/lang.json", "r", encoding="utf-8") as f:
            langs = json.loads(f.read())
        return langs
    
    def setLangToZh(self):
        if self.defLang != self.langs["zh"]:
            self.defLang = self.langs["zh"]
            self.retranslateUI(self.defLang)
        
    def setLangToEn(self):
        if self.defLang != self.langs["en"]:
            self.defLang = self.langs["en"]
            self.retranslateUI(self.defLang)
    
    def retranslateUI(self, defLang):        
        self.setWindowTitle(defLang["windowTitle"])
        
        self.menuLang.setTitle(defLang["langSettings"])
        self.menuAbout.setText(defLang["about"])
        self.whereIsHzChopLabel.setText(defLang["whereIsHzChop"])
        self.whereIsInputMIDILabel.setText(defLang["whereIsInputMIDI"])
        self.whereIsOutputMIDILabel.setText(defLang["whereIsOutputMIDI"])
        self.whereIsHzChopButton.setText(defLang["browse"])
        self.whereIsInputMIDIButton.setText(defLang["browse"])
        self.whereIsOutputMIDIButton.setText(defLang["browse"])
        self.startButton.setText(defLang["start"])
        
        for i, (checkbox, _) in enumerate(self.params):
            if i < len(defLang["toolTips"]):
                checkbox.setToolTip(defLang["toolTips"][i])
        
        self.updateGeometry()
        self.adjustSize()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = MainActivity()
    a.show()
    sys.exit(app.exec())
