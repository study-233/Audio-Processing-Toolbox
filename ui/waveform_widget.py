"""
音频波形显示组件
"""
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
import pyqtgraph as pg


class WaveformWidget(QWidget):
    """音频波形显示组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建图形窗口
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#1e1e1e')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setLabel('left', '振幅')
        self.plot_widget.setLabel('bottom', '时间', units='s')
        self.plot_widget.setTitle('音频波形', color='#ffffff', size='12pt')
        
        # 设置颜色
        self.plot_widget.getAxis('left').setPen(pg.mkPen(color='#888888'))
        self.plot_widget.getAxis('bottom').setPen(pg.mkPen(color='#888888'))
        self.plot_widget.getAxis('left').setTextPen(pg.mkPen(color='#cccccc'))
        self.plot_widget.getAxis('bottom').setTextPen(pg.mkPen(color='#cccccc'))
        
        layout.addWidget(self.plot_widget)
        
        self.audio_data = None
        self.sample_rate = None
        self.plot_item = None
        
    def update_waveform(self, audio_data: np.ndarray, sample_rate: int):
        """
        更新波形显示
        
        Args:
            audio_data: 音频数据
            sample_rate: 采样率
        """
        self.audio_data = audio_data
        self.sample_rate = sample_rate
        
        # 清除之前的绘图
        self.plot_widget.clear()
        
        if audio_data is None or len(audio_data) == 0:
            return
        
        # 如果是立体声，只显示第一个声道
        if len(audio_data.shape) == 2:
            audio_to_plot = audio_data[:, 0]
        else:
            audio_to_plot = audio_data
        
        # 降采样以提高绘图性能（如果数据点太多）
        max_points = 10000
        if len(audio_to_plot) > max_points:
            step = len(audio_to_plot) // max_points
            audio_to_plot = audio_to_plot[::step]
        else:
            step = 1
        
        # 创建时间轴
        time_axis = np.arange(len(audio_to_plot)) * step / sample_rate
        
        # 绘制波形
        pen = pg.mkPen(color='#00ff88', width=1)
        self.plot_item = self.plot_widget.plot(time_axis, audio_to_plot, pen=pen)
        
    def clear(self):
        """清除波形显示"""
        self.plot_widget.clear()
        self.audio_data = None
        self.sample_rate = None
        self.plot_item = None
