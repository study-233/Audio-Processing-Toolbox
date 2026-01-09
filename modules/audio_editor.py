"""
音频编辑工具模块
包含切分、静音去除、采样率调整等功能
"""
import numpy as np
import librosa
from scipy import signal as scipy_signal
from typing import Tuple, List


class AudioEditor:
    """音频编辑处理类"""
    
    @staticmethod
    def trim_audio(audio_data: np.ndarray, start_time: float, end_time: float, 
                   sample_rate: int) -> np.ndarray:
        """
        音频切分
        
        Args:
            audio_data: 音频数据
            start_time: 起始时间（秒）
            end_time: 结束时间（秒）
            sample_rate: 采样率
            
        Returns:
            切分后的音频数据
        """
        try:
            start_sample = int(start_time * sample_rate)
            end_sample = int(end_time * sample_rate)
            
            # 确保索引在有效范围内
            start_sample = max(0, start_sample)
            end_sample = min(len(audio_data), end_sample)
            
            return audio_data[start_sample:end_sample]
        except Exception as e:
            raise Exception(f"音频切分失败: {str(e)}")
    
    @staticmethod
    def remove_silence(audio_data: np.ndarray, sample_rate: int, 
                       threshold_db: float = -40, min_silence_duration: float = 0.3) -> np.ndarray:
        """
        去除较长静音段
        
        Args:
            audio_data: 音频数据
            sample_rate: 采样率
            threshold_db: 静音阈值（分贝）
            min_silence_duration: 最小静音持续时间（秒）
            
        Returns:
            去除静音后的音频数据
        """
        try:
            # 如果是立体声，转换为单声道进行检测
            if len(audio_data.shape) == 2:
                mono_audio = np.mean(audio_data, axis=1)
            else:
                mono_audio = audio_data
            
            # 计算短时能量
            frame_length = int(0.025 * sample_rate)  # 25ms
            hop_length = int(0.010 * sample_rate)    # 10ms
            
            energy = librosa.feature.rms(y=mono_audio, frame_length=frame_length, 
                                        hop_length=hop_length)[0]
            
            # 转换为dB
            energy_db = librosa.amplitude_to_db(energy, ref=np.max)
            
            # 检测非静音段
            non_silent = energy_db > threshold_db
            
            # 扩展到样本级别
            non_silent_samples = np.repeat(non_silent, hop_length)
            if len(non_silent_samples) < len(audio_data):
                non_silent_samples = np.pad(non_silent_samples, 
                                           (0, len(audio_data) - len(non_silent_samples)))
            else:
                non_silent_samples = non_silent_samples[:len(audio_data)]
            
            # 去除短静音段（保留短暂停顿）
            min_silence_samples = int(min_silence_duration * sample_rate)
            from scipy.ndimage import binary_dilation
            non_silent_samples = binary_dilation(non_silent_samples, 
                                                iterations=min_silence_samples // hop_length)
            
            return audio_data[non_silent_samples]
        except Exception as e:
            raise Exception(f"去除静音失败: {str(e)}")
    
    @staticmethod
    def trim_silence_edges(audio_data: np.ndarray, sample_rate: int, 
                          threshold_db: float = -40) -> np.ndarray:
        """
        去除首尾静音
        
        Args:
            audio_data: 音频数据
            sample_rate: 采样率
            threshold_db: 静音阈值（分贝）
            
        Returns:
            去除首尾静音后的音频数据
        """
        try:
            # 如果是立体声，分别处理
            if len(audio_data.shape) == 2:
                trimmed_data = []
                for i in range(audio_data.shape[1]):
                    trimmed, _ = librosa.effects.trim(audio_data[:, i], 
                                                     top_db=-threshold_db)
                    trimmed_data.append(trimmed)
                # 使用最长的结果
                max_len = max(len(t) for t in trimmed_data)
                result = np.zeros((max_len, audio_data.shape[1]))
                for i, t in enumerate(trimmed_data):
                    result[:len(t), i] = t
                return result
            else:
                trimmed, _ = librosa.effects.trim(audio_data, top_db=-threshold_db)
                return trimmed
        except Exception as e:
            raise Exception(f"去除首尾静音失败: {str(e)}")
    
    @staticmethod
    def resample(audio_data: np.ndarray, orig_sr: int, target_sr: int) -> np.ndarray:
        """
        重采样（调整采样率）
        
        Args:
            audio_data: 音频数据
            orig_sr: 原始采样率
            target_sr: 目标采样率
            
        Returns:
            重采样后的音频数据
        """
        try:
            if orig_sr == target_sr:
                return audio_data
            
            # 如果是立体声，分别处理每个声道
            if len(audio_data.shape) == 2:
                result = np.zeros((int(len(audio_data) * target_sr / orig_sr), 
                                 audio_data.shape[1]))
                for i in range(audio_data.shape[1]):
                    result[:, i] = librosa.resample(audio_data[:, i], 
                                                   orig_sr=orig_sr, 
                                                   target_sr=target_sr)
                return result
            else:
                return librosa.resample(audio_data, orig_sr=orig_sr, target_sr=target_sr)
        except Exception as e:
            raise Exception(f"重采样失败: {str(e)}")
    
    @staticmethod
    def convert_channels(audio_data: np.ndarray, target_channels: int) -> np.ndarray:
        """
        转换声道数
        
        Args:
            audio_data: 音频数据
            target_channels: 目标声道数（1或2）
            
        Returns:
            转换后的音频数据
        """
        try:
            current_channels = 1 if len(audio_data.shape) == 1 else audio_data.shape[1]
            
            if current_channels == target_channels:
                return audio_data
            
            if target_channels == 1:
                # 转换为单声道
                if len(audio_data.shape) == 2:
                    return np.mean(audio_data, axis=1)
                return audio_data
            else:
                # 转换为立体声
                if len(audio_data.shape) == 1:
                    return np.stack([audio_data, audio_data], axis=1)
                return audio_data
        except Exception as e:
            raise Exception(f"声道转换失败: {str(e)}")
