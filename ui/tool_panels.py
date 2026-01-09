"""
工具面板组件
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QSlider, QSpinBox, QDoubleSpinBox,
                             QGroupBox, QComboBox, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal


class BaseToolPanel(QWidget):
    """工具面板基类"""
    
    process_requested = pyqtSignal(dict)  # 发送处理参数
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI - 子类需要实现"""
        pass
    
    def get_parameters(self) -> dict:
        """获取参数 - 子类需要实现"""
        return {}


class AudioChangerPanel(BaseToolPanel):
    """音频变换工具面板"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # 变声参数
        pitch_group = QGroupBox("变声")
        pitch_layout = QVBoxLayout()
        
        pitch_label_layout = QHBoxLayout()
        pitch_label_layout.addWidget(QLabel("音高偏移 (半音):"))
        self.pitch_value_label = QLabel("0")
        pitch_label_layout.addWidget(self.pitch_value_label)
        pitch_label_layout.addStretch()
        pitch_layout.addLayout(pitch_label_layout)
        
        self.pitch_slider = QSlider(Qt.Horizontal)
        self.pitch_slider.setMinimum(-12)
        self.pitch_slider.setMaximum(12)
        self.pitch_slider.setValue(0)
        self.pitch_slider.valueChanged.connect(
            lambda v: self.pitch_value_label.setText(str(v))
        )
        pitch_layout.addWidget(self.pitch_slider)
        
        self.pitch_btn = QPushButton("应用变声")
        self.pitch_btn.clicked.connect(self.process_pitch_shift)
        pitch_layout.addWidget(self.pitch_btn)
        
        pitch_group.setLayout(pitch_layout)
        layout.addWidget(pitch_group)
        
        # 语速调整
        speed_group = QGroupBox("语速调整")
        speed_layout = QVBoxLayout()
        
        speed_label_layout = QHBoxLayout()
        speed_label_layout.addWidget(QLabel("语速倍率:"))
        self.speed_spinbox = QDoubleSpinBox()
        self.speed_spinbox.setMinimum(0.5)
        self.speed_spinbox.setMaximum(2.0)
        self.speed_spinbox.setValue(1.0)
        self.speed_spinbox.setSingleStep(0.1)
        speed_label_layout.addWidget(self.speed_spinbox)
        speed_label_layout.addStretch()
        speed_layout.addLayout(speed_label_layout)
        
        self.speed_btn = QPushButton("应用语速调整")
        self.speed_btn.clicked.connect(self.process_time_stretch)
        speed_layout.addWidget(self.speed_btn)
        
        speed_group.setLayout(speed_layout)
        layout.addWidget(speed_group)
        
        # 回声效果
        echo_group = QGroupBox("回声效果")
        echo_layout = QVBoxLayout()
        
        delay_layout = QHBoxLayout()
        delay_layout.addWidget(QLabel("延迟时间 (秒):"))
        self.delay_spinbox = QDoubleSpinBox()
        self.delay_spinbox.setMinimum(0.1)
        self.delay_spinbox.setMaximum(2.0)
        self.delay_spinbox.setValue(0.3)
        self.delay_spinbox.setSingleStep(0.1)
        delay_layout.addWidget(self.delay_spinbox)
        delay_layout.addStretch()
        echo_layout.addLayout(delay_layout)
        
        decay_layout = QHBoxLayout()
        decay_layout.addWidget(QLabel("衰减系数:"))
        self.decay_spinbox = QDoubleSpinBox()
        self.decay_spinbox.setMinimum(0.1)
        self.decay_spinbox.setMaximum(0.9)
        self.decay_spinbox.setValue(0.5)
        self.decay_spinbox.setSingleStep(0.1)
        decay_layout.addWidget(self.decay_spinbox)
        decay_layout.addStretch()
        echo_layout.addLayout(decay_layout)
        
        self.echo_btn = QPushButton("应用回声效果")
        self.echo_btn.clicked.connect(self.process_echo)
        echo_layout.addWidget(self.echo_btn)
        
        echo_group.setLayout(echo_layout)
        layout.addWidget(echo_group)
        
        layout.addStretch()
        
    def process_pitch_shift(self):
        params = {
            'type': 'pitch_shift',
            'n_steps': self.pitch_slider.value()
        }
        self.process_requested.emit(params)
        
    def process_time_stretch(self):
        params = {
            'type': 'time_stretch',
            'rate': self.speed_spinbox.value()
        }
        self.process_requested.emit(params)
        
    def process_echo(self):
        params = {
            'type': 'echo',
            'delay': self.delay_spinbox.value(),
            'decay': self.decay_spinbox.value()
        }
        self.process_requested.emit(params)


class AudioEditorPanel(BaseToolPanel):
    """音频编辑工具面板"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # 音频切分
        trim_group = QGroupBox("音频切分")
        trim_layout = QVBoxLayout()
        
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("开始时间 (秒):"))
        self.start_spinbox = QDoubleSpinBox()
        self.start_spinbox.setMinimum(0)
        self.start_spinbox.setMaximum(10000)
        self.start_spinbox.setValue(0)
        self.start_spinbox.setSingleStep(0.1)
        start_layout.addWidget(self.start_spinbox)
        start_layout.addStretch()
        trim_layout.addLayout(start_layout)
        
        end_layout = QHBoxLayout()
        end_layout.addWidget(QLabel("结束时间 (秒):"))
        self.end_spinbox = QDoubleSpinBox()
        self.end_spinbox.setMinimum(0)
        self.end_spinbox.setMaximum(10000)
        self.end_spinbox.setValue(10)
        self.end_spinbox.setSingleStep(0.1)
        end_layout.addWidget(self.end_spinbox)
        end_layout.addStretch()
        trim_layout.addLayout(end_layout)
        
        self.trim_btn = QPushButton("应用切分")
        self.trim_btn.clicked.connect(self.process_trim)
        trim_layout.addWidget(self.trim_btn)
        
        trim_group.setLayout(trim_layout)
        layout.addWidget(trim_group)
        
        # 静音去除
        silence_group = QGroupBox("静音处理")
        silence_layout = QVBoxLayout()
        
        self.trim_edges_btn = QPushButton("去除首尾静音")
        self.trim_edges_btn.clicked.connect(self.process_trim_edges)
        silence_layout.addWidget(self.trim_edges_btn)
        
        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(QLabel("静音阈值 (dB):"))
        self.threshold_spinbox = QSpinBox()
        self.threshold_spinbox.setMinimum(-60)
        self.threshold_spinbox.setMaximum(-10)
        self.threshold_spinbox.setValue(-40)
        threshold_layout.addWidget(self.threshold_spinbox)
        threshold_layout.addStretch()
        silence_layout.addLayout(threshold_layout)
        
        self.remove_silence_btn = QPushButton("去除长静音段")
        self.remove_silence_btn.clicked.connect(self.process_remove_silence)
        silence_layout.addWidget(self.remove_silence_btn)
        
        silence_group.setLayout(silence_layout)
        layout.addWidget(silence_group)
        
        # 采样率调整
        resample_group = QGroupBox("采样率调整")
        resample_layout = QVBoxLayout()
        
        sr_layout = QHBoxLayout()
        sr_layout.addWidget(QLabel("目标采样率 (Hz):"))
        self.sr_combo = QComboBox()
        self.sr_combo.addItems(['8000', '16000', '22050', '44100', '48000'])
        self.sr_combo.setCurrentText('44100')
        sr_layout.addWidget(self.sr_combo)
        sr_layout.addStretch()
        resample_layout.addLayout(sr_layout)
        
        self.resample_btn = QPushButton("应用重采样")
        self.resample_btn.clicked.connect(self.process_resample)
        resample_layout.addWidget(self.resample_btn)
        
        resample_group.setLayout(resample_layout)
        layout.addWidget(resample_group)
        
        # 声道转换
        channel_group = QGroupBox("声道转换")
        channel_layout = QVBoxLayout()
        
        self.mono_btn = QPushButton("转换为单声道")
        self.mono_btn.clicked.connect(self.process_to_mono)
        channel_layout.addWidget(self.mono_btn)
        
        self.stereo_btn = QPushButton("转换为立体声")
        self.stereo_btn.clicked.connect(self.process_to_stereo)
        channel_layout.addWidget(self.stereo_btn)
        
        channel_group.setLayout(channel_layout)
        layout.addWidget(channel_group)
        
        layout.addStretch()
        
    def process_trim(self):
        params = {
            'type': 'trim',
            'start_time': self.start_spinbox.value(),
            'end_time': self.end_spinbox.value()
        }
        self.process_requested.emit(params)
        
    def process_trim_edges(self):
        params = {
            'type': 'trim_edges',
            'threshold_db': self.threshold_spinbox.value()
        }
        self.process_requested.emit(params)
        
    def process_remove_silence(self):
        params = {
            'type': 'remove_silence',
            'threshold_db': self.threshold_spinbox.value()
        }
        self.process_requested.emit(params)
        
    def process_resample(self):
        params = {
            'type': 'resample',
            'target_sr': int(self.sr_combo.currentText())
        }
        self.process_requested.emit(params)
        
    def process_to_mono(self):
        params = {'type': 'to_mono'}
        self.process_requested.emit(params)
        
    def process_to_stereo(self):
        params = {'type': 'to_stereo'}
        self.process_requested.emit(params)


class NoiseRemoverPanel(BaseToolPanel):
    """降噪工具面板"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # 频谱减法降噪
        spectral_group = QGroupBox("频谱减法降噪")
        spectral_layout = QVBoxLayout()
        
        strength_layout = QHBoxLayout()
        strength_layout.addWidget(QLabel("降噪强度:"))
        self.strength_slider = QSlider(Qt.Horizontal)
        self.strength_slider.setMinimum(0)
        self.strength_slider.setMaximum(100)
        self.strength_slider.setValue(50)
        self.strength_value_label = QLabel("0.50")
        self.strength_slider.valueChanged.connect(
            lambda v: self.strength_value_label.setText(f"{v/100:.2f}")
        )
        strength_layout.addWidget(self.strength_slider)
        strength_layout.addWidget(self.strength_value_label)
        spectral_layout.addLayout(strength_layout)
        
        gate_layout = QHBoxLayout()
        gate_layout.addWidget(QLabel("噪声门限:"))
        self.gate_slider = QSlider(Qt.Horizontal)
        self.gate_slider.setMinimum(0)
        self.gate_slider.setMaximum(50)
        self.gate_slider.setValue(10)
        self.gate_value_label = QLabel("0.10")
        self.gate_slider.valueChanged.connect(
            lambda v: self.gate_value_label.setText(f"{v/100:.2f}")
        )
        gate_layout.addWidget(self.gate_slider)
        gate_layout.addWidget(self.gate_value_label)
        spectral_layout.addLayout(gate_layout)
        
        self.spectral_btn = QPushButton("应用降噪")
        self.spectral_btn.clicked.connect(self.process_spectral_subtraction)
        spectral_layout.addWidget(self.spectral_btn)
        
        spectral_group.setLayout(spectral_layout)
        layout.addWidget(spectral_group)
        
        layout.addStretch()
        
    def process_spectral_subtraction(self):
        params = {
            'type': 'spectral_subtraction',
            'strength': self.strength_slider.value() / 100,
            'gate': self.gate_slider.value() / 100
        }
        self.process_requested.emit(params)
