"""
音频输入输出模块
提供统一的音频读取和保存接口
"""
import numpy as np
import soundfile as sf
from typing import Tuple, Optional


class AudioIO:
    """音频输入输出类"""
    
    @staticmethod
    def load_audio(file_path: str) -> Tuple[np.ndarray, int]:
        """
        加载音频文件
        
        Args:
            file_path: 音频文件路径
            
        Returns:
            (audio_data, sample_rate): 音频数据和采样率
        """
        try:
            audio_data, sample_rate = sf.read(file_path, dtype='float32')
            return audio_data, sample_rate
        except Exception as e:
            raise Exception(f"加载音频文件失败: {str(e)}")
    
    @staticmethod
    def save_audio(file_path: str, audio_data: np.ndarray, sample_rate: int) -> bool:
        """
        保存音频文件
        
        Args:
            file_path: 保存路径
            audio_data: 音频数据
            sample_rate: 采样率
            
        Returns:
            是否成功
        """
        try:
            sf.write(file_path, audio_data, sample_rate)
            return True
        except Exception as e:
            raise Exception(f"保存音频文件失败: {str(e)}")
    
    @staticmethod
    def get_audio_info(file_path: str) -> dict:
        """
        获取音频文件信息
        
        Args:
            file_path: 音频文件路径
            
        Returns:
            音频信息字典
        """
        try:
            info = sf.info(file_path)
            return {
                'duration': info.duration,
                'sample_rate': info.samplerate,
                'channels': info.channels,
                'format': info.format,
                'subtype': info.subtype
            }
        except Exception as e:
            raise Exception(f"获取音频信息失败: {str(e)}")
    
    @staticmethod
    def convert_to_mono(audio_data: np.ndarray) -> np.ndarray:
        """
        将音频转换为单声道
        
        Args:
            audio_data: 音频数据
            
        Returns:
            单声道音频数据
        """
        if len(audio_data.shape) == 1:
            return audio_data
        return np.mean(audio_data, axis=1)
    
    @staticmethod
    def convert_to_stereo(audio_data: np.ndarray) -> np.ndarray:
        """
        将音频转换为立体声
        
        Args:
            audio_data: 音频数据
            
        Returns:
            立体声音频数据
        """
        if len(audio_data.shape) == 2:
            return audio_data
        return np.stack([audio_data, audio_data], axis=1)
