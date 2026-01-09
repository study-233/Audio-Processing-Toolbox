"""
音频处理工具箱 - 主程序入口
"""
import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from PyQt5.QtGui import QIcon


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/dsp.ico"))   # 全局应用图标（任务栏/窗口）
    app.setApplicationName("音频处理工具箱")
    app.setOrganizationName("Audio Tools")
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
