from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
import subprocess
import pathlib
import json

W = 600
H = 600

class MainActivity(QWidget):
    def __init__(self):
        super().__init__()
        self.onCreate()
    
    def onCreate(self):
        self.setFixedSize(W, H)
        self.setWindowTitle("HzChop GUI 版 v1.0 - by LTJ")
        if QApplication.styleHints().colorScheme() == Qt.ColorScheme.Light:
            self.setWindowIcon(QIcon("resources/icon0.png"))
        else:
            self.setWindowIcon(QIcon("resources/icon1.png"))

        self.hzchop = None
        self.input_midi = None
        self.output_midi = None

        self.h1 = QHBoxLayout()
        self.h2 = QHBoxLayout()
        self.h3 = QHBoxLayout()
        self.h4 = QHBoxLayout()
        self.hParams = []
        self.params = []
        self.v = QVBoxLayout()

        self.whereIsHzChopLabel = QLabel("HzChop 所在路径:")
        self.whereIsHzChopLabel.setFixedWidth(128)
        self.whereIsHzChopLabel.setStyleSheet("font-family: Consolas;")
        self.whereIsHzChopInput = QLineEdit()
        self.whereIsHzChopInput.setStyleSheet("font-family: Consolas; color: #80a040;")
        self.whereIsHzChopButton = QPushButton("浏览...")
        self.whereIsHzChopButton.clicked.connect(self.onClick_WhereIsHzChop)
        self.whereIsHzChopButton.setStyleSheet("color: green;")
        self.h1.addWidget(self.whereIsHzChopLabel)
        self.h1.addWidget(self.whereIsHzChopInput)
        self.h1.addWidget(self.whereIsHzChopButton)

        self.whereIsInputMIDILabel = QLabel("输入 MIDI 所在路径:")
        self.whereIsInputMIDILabel.setFixedWidth(128)
        self.whereIsInputMIDILabel.setStyleSheet("font-family: Consolas;")
        self.whereIsInputMIDIInput = QLineEdit()
        self.whereIsInputMIDIInput.setStyleSheet("font-family: Consolas; color: #80a040;")
        self.whereIsInputMIDIButton = QPushButton("浏览...")
        self.whereIsInputMIDIButton.clicked.connect(self.onClick_WhereIsInputMIDI)
        self.whereIsInputMIDIButton.setStyleSheet("color: green;")
        self.h2.addWidget(self.whereIsInputMIDILabel)
        self.h2.addWidget(self.whereIsInputMIDIInput)
        self.h2.addWidget(self.whereIsInputMIDIButton)

        
        self.whereIsOutputMIDILabel = QLabel("输出 MIDI 所在路径:")
        self.whereIsOutputMIDILabel.setFixedWidth(128)
        self.whereIsOutputMIDILabel.setStyleSheet("font-family: Consolas;")
        self.whereIsOutputMIDIInput = QLineEdit()
        self.whereIsOutputMIDIInput.setStyleSheet("font-family: Consolas; color: #80a040;")
        self.whereIsOutputMIDIButton = QPushButton("浏览...")
        self.whereIsOutputMIDIButton.clicked.connect(self.onClick_WhereIsOutputMIDI)
        self.whereIsOutputMIDIButton.setStyleSheet("color: green;")
        self.h3.addWidget(self.whereIsOutputMIDILabel)
        self.h3.addWidget(self.whereIsOutputMIDIInput)
        self.h3.addWidget(self.whereIsOutputMIDIButton)

        self.logoIcon = QIcon("resources/logo.png")
        self.startButton = QPushButton(self.logoIcon, "开始")
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
        self.paramCheckBoxToolTips = [
            "力度斜率因子 （默认：1.0）", "移相层数（如果不指定：不进行移相处理）", 
            "移相量，以频率比表示（默认：0.01）", "在音符 64 之上/之下叠加的副本数量（默认：0 - 禁用）", 
            "输出的 PPQ（每四分音符脉冲数）值（默认：使用原始 PPQ）", "仅对低于此键位的音符进行 Hz 切分（默认：0 - 禁用）", 
            "低音增强的力度阈值（默认：0 - 无阈值）", "要处理的最小轨道编号（默认：0）", 
            "要处理的最大轨道编号（默认：所有轨道）", "要处理的最小通道编号（默认：0）", 
            "要处理的最大通道编号（默认：15）"
        ]
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
        
        self.setLayout(self.v)
    
    def onClick_WhereIsHzChop(self):
        self.hzchop = QFileDialog.getOpenFileName(self, "打开 hzchop.exe ...", None, "可执行文件 (*.exe)")[0]
        self.whereIsHzChopInput.setText(self.hzchop.replace("/", "\\"))
    
    def onClick_WhereIsInputMIDI(self):
        self.input_midi = QFileDialog.getOpenFileName(self, "打开 MIDI ...", None, "MIDI 文件 (*.mid *.midi)")[0]
        self.whereIsInputMIDIInput.setText(self.input_midi.replace("/", "\\"))
    
    def onClick_WhereIsOutputMIDI(self):
        self.output_midi = QFileDialog.getSaveFileName(self, "保存 MIDI ...", None, "MIDI 文件 (*.mid *.midi)")[0]
        self.whereIsOutputMIDIInput.setText(self.output_midi.replace("/", "\\"))
    
    def onClick_Start(self):
        if self.hzchop:
            if self.input_midi and self.output_midi:
                standardCmd = f"{self.hzchop} {self.input_midi} {self.output_midi}"
                for i in self.params:
                    if i[1].isEnabled():
                        standardCmd += f" {i[0].text()} {i[1].value()}"
                process = subprocess.Popen(standardCmd, stdout=subprocess.PIPE, text=True)
                for line in process.stdout:
                    print(line, end="")
                process.wait()
                QMessageBox.information(self, "提示", f"成功! 到 {pathlib.Path(self.output_midi).parent} 查看 MIDI!")
            else:
                QMessageBox.critical(self, "错误", "先填写输入和输出 MIDI 路径!!!")
        else:
            QMessageBox.critical(self, "错误", "先填写 hzchop.exe 的路径!!!")
        
        params_dict = {}
        for checkbox, spinbox in self.params:
            param_name = checkbox.text()
            params_dict[param_name] = {
                "enabled": checkbox.isChecked(),
                "value": spinbox.value()
            }

        config_data = {
            "hzchopPath": self.hzchop,
            "inputMIDIPath": self.input_midi,
            "outputMIDIPath": self.output_midi,
            "other": params_dict
        }

        self.saveThisConfig(config_data)
    
    def loadLastConfig(self):
        try:
            with open("data/config.json", "r", encoding="utf-8") as f:
                config = json.loads(f.read())
            
            self.hzchop = config.get("hzchopPath").replace("/", "\\")
            self.input_midi = config.get("inputMIDIPath").replace("/", "\\")
            self.output_midi = config.get("outputMIDIPath").replace("/", "\\")
            
            if self.hzchop: self.whereIsHzChopInput.setText(self.hzchop)
            if self.input_midi: self.whereIsInputMIDIInput.setText(self.input_midi)
            if self.output_midi: self.whereIsOutputMIDIInput.setText(self.output_midi)
            
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
            with open("data/config.json", "w", encoding="utf-8") as f:
                json.dump(config_dict, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = MainActivity()
    a.show()
    sys.exit(app.exec())
