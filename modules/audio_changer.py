"""
音频变换工具模块
包含变声、语速调整、回声效果等功能
"""
import numpy as np
import librosa
from scipy import signal


class AudioChanger:
    """音频变换处理类"""
    
    @staticmethod
    def pitch_shift(audio_data: np.ndarray, sample_rate: int, n_steps: float) -> np.ndarray:
        """
        音高变换（变声）
        
        Args:
            audio_data: 音频数据
            sample_rate: 采样率
            n_steps: 音高偏移量（半音数），正值升调，负值降调
            
        Returns:
            变换后的音频数据
        """
        try:
            # 如果是立体声，分别处理每个声道
            if len(audio_data.shape) == 2:
                result = np.zeros_like(audio_data)
                for i in range(audio_data.shape[1]):
                    result[:, i] = librosa.effects.pitch_shift(
                        audio_data[:, i], sr=sample_rate, n_steps=n_steps
                    )
                return result
            else:
                return librosa.effects.pitch_shift(
                    audio_data, sr=sample_rate, n_steps=n_steps
                )
        except Exception as e:
            raise Exception(f"音高变换失败: {str(e)}")
    
    @staticmethod
    def time_stretch(audio_data: np.ndarray, rate: float) -> np.ndarray:
        """
        语速调整（时间拉伸）
        
        Args:
            audio_data: 音频数据
            rate: 速度倍率，>1 加速，<1 减速
            
        Returns:
            变换后的音频数据
        """
        try:
            # 如果是立体声，分别处理每个声道
            if len(audio_data.shape) == 2:
                result = np.zeros((int(audio_data.shape[0] / rate), audio_data.shape[1]))
                for i in range(audio_data.shape[1]):
                    result[:, i] = librosa.effects.time_stretch(
                        audio_data[:, i], rate=rate
                    )
                return result
            else:
                return librosa.effects.time_stretch(audio_data, rate=rate)
        except Exception as e:
            raise Exception(f"语速调整失败: {str(e)}")
    
    @staticmethod
    def add_echo(audio_data: np.ndarray, sample_rate: int, 
                 delay: float, decay: float) -> np.ndarray:
        """
        添加回声效果
        
        Args:
            audio_data: 音频数据
            sample_rate: 采样率
            delay: 延迟时间（秒）
            decay: 衰减系数（0-1）
            
        Returns:
            添加回声后的音频数据
        """
        try:
            # 计算延迟采样数
            delay_samples = int(delay * sample_rate)
            
            # 如果是立体声，分别处理每个声道
            if len(audio_data.shape) == 2:
                result = np.zeros((len(audio_data) + delay_samples, audio_data.shape[1]))
                for i in range(audio_data.shape[1]):
                    result[:len(audio_data), i] = audio_data[:, i]
                    result[delay_samples:, i] += audio_data[:, i] * decay
                return result
            else:
                # 创建输出数组
                result = np.zeros(len(audio_data) + delay_samples)
                # 原始信号
                result[:len(audio_data)] = audio_data
                # 延迟后的回声信号
                result[delay_samples:] += audio_data * decay
                return result
        except Exception as e:
            raise Exception(f"添加回声失败: {str(e)}")
    
    @staticmethod
    def change_volume(audio_data: np.ndarray, gain_db: float) -> np.ndarray:
        """
        调整音量
        
        Args:
            audio_data: 音频数据
            gain_db: 增益（分贝）
            
        Returns:
            调整后的音频数据
        """
        try:
            gain_linear = 10 ** (gain_db / 20.0)
            return audio_data * gain_linear
        except Exception as e:
            raise Exception(f"音量调整失败: {str(e)}")
