"""
主窗口
"""
import os
import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QListWidget, QPushButton, QFileDialog, QLabel,
                             QStatusBar, QMessageBox, QStackedWidget, QSplitter)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from modules import AudioIO, AudioChanger, AudioEditor, AudioNoiseRemover
from ui import WaveformWidget, AudioChangerPanel, AudioEditorPanel, NoiseRemoverPanel


class ProcessThread(QThread):
    """音频处理线程"""
    
    finished = pyqtSignal(np.ndarray, int)
    error = pyqtSignal(str)
    
    def __init__(self, audio_data, sample_rate, process_type, params):
        super().__init__()
        self.audio_data = audio_data
        self.sample_rate = sample_rate
        self.process_type = process_type
        self.params = params
        
    def run(self):
        try:
            result = self.audio_data
            sr = self.sample_rate
            
            # 音频变换
            if self.process_type == 'pitch_shift':
                result = AudioChanger.pitch_shift(result, sr, self.params['n_steps'])
            elif self.process_type == 'time_stretch':
                result = AudioChanger.time_stretch(result, self.params['rate'])
            elif self.process_type == 'echo':
                result = AudioChanger.add_echo(result, sr, self.params['delay'], 
                                              self.params['decay'])
            
            # 音频编辑
            elif self.process_type == 'trim':
                result = AudioEditor.trim_audio(result, self.params['start_time'],
                                               self.params['end_time'], sr)
            elif self.process_type == 'trim_edges':
                result = AudioEditor.trim_silence_edges(result, sr, 
                                                        self.params['threshold_db'])
            elif self.process_type == 'remove_silence':
                result = AudioEditor.remove_silence(result, sr, 
                                                    self.params['threshold_db'])
            elif self.process_type == 'resample':
                result = AudioEditor.resample(result, sr, self.params['target_sr'])
                sr = self.params['target_sr']
            elif self.process_type == 'to_mono':
                result = AudioEditor.convert_channels(result, 1)
            elif self.process_type == 'to_stereo':
                result = AudioEditor.convert_channels(result, 2)
            
            # 降噪
            elif self.process_type == 'spectral_subtraction':
                result = AudioNoiseRemover.spectral_subtraction(
                    result, sr, self.params['strength'], self.params['gate']
                )
            
            self.finished.emit(result, sr)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.audio_data = None
        self.sample_rate = None
        self.current_file = None
        self.process_thread = None
        
        self.setup_ui()
        self.apply_dark_theme()
        
    def setup_ui(self):
        """设置UI"""
        self.setWindowTitle("音频处理工具箱")
        self.setGeometry(100, 100, 1400, 800)
        
        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧工具列表
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        tool_label = QLabel("工具箱")
        tool_label.setFont(QFont("Arial", 14, QFont.Bold))
        left_layout.addWidget(tool_label)
        
        self.tool_list = QListWidget()
        self.tool_list.addItems([
            "音频变换工具",
            "音频编辑工具",
            "语音降噪工具"
        ])
        self.tool_list.currentRowChanged.connect(self.switch_tool)
        left_layout.addWidget(self.tool_list)
        
        # 文件操作按钮
        self.load_btn = QPushButton("加载音频")
        self.load_btn.clicked.connect(self.load_audio)
        left_layout.addWidget(self.load_btn)
        
        self.save_btn = QPushButton("保存音频")
        self.save_btn.clicked.connect(self.save_audio)
        self.save_btn.setEnabled(False)
        left_layout.addWidget(self.save_btn)
        
        splitter.addWidget(left_widget)
        
        # 中间和右侧区域
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # 文件信息
        self.info_label = QLabel("未加载音频文件")
        self.info_label.setStyleSheet("padding: 5px; background-color: #2d2d2d;")
        right_layout.addWidget(self.info_label)
        
        # 波形显示
        self.waveform_widget = WaveformWidget()
        right_layout.addWidget(self.waveform_widget, stretch=2)
        
        # 工具面板容器
        self.tool_stack = QStackedWidget()
        
        # 创建各工具面板
        self.changer_panel = AudioChangerPanel()
        self.changer_panel.process_requested.connect(self.process_audio)
        self.tool_stack.addWidget(self.changer_panel)
        
        self.editor_panel = AudioEditorPanel()
        self.editor_panel.process_requested.connect(self.process_audio)
        self.tool_stack.addWidget(self.editor_panel)
        
        self.noise_panel = NoiseRemoverPanel()
        self.noise_panel.process_requested.connect(self.process_audio)
        self.tool_stack.addWidget(self.noise_panel)
        
        right_layout.addWidget(self.tool_stack, stretch=1)
        
        splitter.addWidget(right_widget)
        
        # 设置分割器比例
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)
        
        main_layout.addWidget(splitter)
        
        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
        
        # 默认选择第一个工具
        self.tool_list.setCurrentRow(0)
        
    def apply_dark_theme(self):
        """应用深色主题"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QListWidget {
                background-color: #252526;
                border: 1px solid #3c3c3c;
                color: #cccccc;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 3px;
            }
            QListWidget::item:selected {
                background-color: #094771;
            }
            QListWidget::item:hover {
                background-color: #2a2d2e;
            }
            QPushButton {
                background-color: #0e639c;
                color: #ffffff;
                border: none;
                padding: 8px 16px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
            QPushButton:pressed {
                background-color: #0d5a8f;
            }
            QPushButton:disabled {
                background-color: #3c3c3c;
                color: #6c6c6c;
            }
            QLabel {
                color: #cccccc;
            }
            QGroupBox {
                border: 1px solid #3c3c3c;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                color: #ffffff;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #3c3c3c;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #0e639c;
                width: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #1177bb;
            }
            QSpinBox, QDoubleSpinBox, QComboBox {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                padding: 4px;
                border-radius: 3px;
                color: #ffffff;
            }
            QSpinBox::up-button, QDoubleSpinBox::up-button {
                background-color: #555555;
            }
            QSpinBox::down-button, QDoubleSpinBox::down-button {
                background-color: #555555;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #555555;
            }
            QComboBox QAbstractItemView {
                background-color: #252526;
                selection-background-color: #094771;
                color: #ffffff;
            }
            QStatusBar {
                background-color: #007acc;
                color: #ffffff;
            }
        """)
        
    def switch_tool(self, index):
        """切换工具"""
        self.tool_stack.setCurrentIndex(index)
        tool_names = ["音频变换工具", "音频编辑工具", "语音降噪工具"]
        self.status_bar.showMessage(f"当前工具: {tool_names[index]}")
        
    def load_audio(self):
        """加载音频文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择音频文件", "",
            "音频文件 (*.wav *.mp3 *.flac *.ogg *.m4a);;所有文件 (*.*)"
        )
        
        if file_path:
            try:
                self.audio_data, self.sample_rate = AudioIO.load_audio(file_path)
                self.current_file = file_path
                self.save_btn.setEnabled(True)
                
                # 更新波形显示
                self.waveform_widget.update_waveform(self.audio_data, self.sample_rate)
                
                # 更新信息
                duration = len(self.audio_data) / self.sample_rate
                channels = "单声道" if len(self.audio_data.shape) == 1 else f"{self.audio_data.shape[1]}声道"
                self.info_label.setText(
                    f"文件: {os.path.basename(file_path)} | "
                    f"时长: {duration:.2f}秒 | "
                    f"采样率: {self.sample_rate}Hz | "
                    f"{channels}"
                )
                
                self.status_bar.showMessage(f"已加载: {os.path.basename(file_path)}")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"加载音频失败:\n{str(e)}")
                
    def save_audio(self):
        """保存音频文件"""
        if self.audio_data is None:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存音频文件", "",
            "WAV文件 (*.wav);;FLAC文件 (*.flac);;OGG文件 (*.ogg)"
        )
        
        if file_path:
            try:
                AudioIO.save_audio(file_path, self.audio_data, self.sample_rate)
                QMessageBox.information(self, "成功", "音频文件保存成功!")
                self.status_bar.showMessage(f"已保存: {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存音频失败:\n{str(e)}")
                
    def process_audio(self, params):
        """处理音频"""
        if self.audio_data is None:
            QMessageBox.warning(self, "警告", "请先加载音频文件!")
            return
            
        if self.process_thread and self.process_thread.isRunning():
            QMessageBox.warning(self, "警告", "正在处理中,请稍候...")
            return
            
        # 创建处理线程
        self.process_thread = ProcessThread(
            self.audio_data.copy(), 
            self.sample_rate,
            params['type'],
            params
        )
        self.process_thread.finished.connect(self.on_process_finished)
        self.process_thread.error.connect(self.on_process_error)
        
        self.status_bar.showMessage("处理中...")
        self.process_thread.start()
        
    def on_process_finished(self, audio_data, sample_rate):
        """处理完成"""
        self.audio_data = audio_data
        self.sample_rate = sample_rate
        
        # 更新波形显示
        self.waveform_widget.update_waveform(self.audio_data, self.sample_rate)
        
        # 更新信息
        duration = len(self.audio_data) / self.sample_rate
        channels = "单声道" if len(self.audio_data.shape) == 1 else f"{self.audio_data.shape[1]}声道"
        current_name = os.path.basename(self.current_file) if self.current_file else "处理后"
        self.info_label.setText(
            f"文件: {current_name} | "
            f"时长: {duration:.2f}秒 | "
            f"采样率: {self.sample_rate}Hz | "
            f"{channels}"
        )
        
        self.status_bar.showMessage("处理完成")
        QMessageBox.information(self, "成功", "音频处理完成!")
        
    def on_process_error(self, error_msg):
        """处理错误"""
        self.status_bar.showMessage("处理失败")
        QMessageBox.critical(self, "错误", f"处理失败:\n{error_msg}")
