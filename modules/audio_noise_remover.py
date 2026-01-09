"""
音频降噪模块
基于频谱减法的降噪处理
"""
import numpy as np
from scipy import signal as scipy_signal
from scipy.fft import fft, ifft


class AudioNoiseRemover:
    """音频降噪处理类"""
    
    @staticmethod
    def spectral_subtraction(audio_data: np.ndarray, sample_rate: int, 
                            noise_reduction_strength: float = 0.5,
                            noise_gate_threshold: float = 0.1) -> np.ndarray:
        """
        频谱减法降噪
        
        Args:
            audio_data: 音频数据
            sample_rate: 采样率
            noise_reduction_strength: 降噪强度 (0-1)
            noise_gate_threshold: 噪声门限阈值
            
        Returns:
            降噪后的音频数据
        """
        try:
            # 如果是立体声，分别处理每个声道
            if len(audio_data.shape) == 2:
                result = np.zeros_like(audio_data)
                for i in range(audio_data.shape[1]):
                    result[:, i] = AudioNoiseRemover._process_channel(
                        audio_data[:, i], sample_rate, 
                        noise_reduction_strength, noise_gate_threshold
                    )
                return result
            else:
                return AudioNoiseRemover._process_channel(
                    audio_data, sample_rate, 
                    noise_reduction_strength, noise_gate_threshold
                )
        except Exception as e:
            raise Exception(f"降噪处理失败: {str(e)}")
    
    @staticmethod
    def _process_channel(audio_data: np.ndarray, sample_rate: int,
                        noise_reduction_strength: float,
                        noise_gate_threshold: float) -> np.ndarray:
        """
        处理单个声道的降噪
        """
        # 参数设置
        frame_size = 2048
        hop_size = frame_size // 4
        
        # 估计噪声谱（使用前几帧作为噪声样本）
        noise_frames = 10
        noise_estimate = AudioNoiseRemover._estimate_noise_spectrum(
            audio_data[:frame_size * noise_frames], frame_size, hop_size
        )
        
        # 分帧处理
        num_frames = (len(audio_data) - frame_size) // hop_size + 1
        output = np.zeros(len(audio_data))
        window = np.hanning(frame_size)
        
        for i in range(num_frames):
            start = i * hop_size
            end = start + frame_size
            
            if end > len(audio_data):
                break
            
            # 提取帧并加窗
            frame = audio_data[start:end] * window
            
            # FFT
            spectrum = fft(frame)
            magnitude = np.abs(spectrum)
            phase = np.angle(spectrum)
            
            # 频谱减法
            clean_magnitude = magnitude - noise_reduction_strength * noise_estimate
            
            # 应用噪声门限
            clean_magnitude = np.where(
                clean_magnitude < noise_gate_threshold * magnitude,
                0,
                clean_magnitude
            )
            
            # 确保非负
            clean_magnitude = np.maximum(clean_magnitude, 0)
            
            # 重构信号
            clean_spectrum = clean_magnitude * np.exp(1j * phase)
            clean_frame = np.real(ifft(clean_spectrum))
            
            # 重叠相加
            output[start:end] += clean_frame * window
        
        # 归一化
        max_val = np.max(np.abs(output))
        if max_val > 0:
            output = output / max_val * np.max(np.abs(audio_data))
        
        return output.astype(np.float32)
    
    @staticmethod
    def _estimate_noise_spectrum(noise_sample: np.ndarray, 
                                frame_size: int, hop_size: int) -> np.ndarray:
        """
        估计噪声频谱
        """
        num_frames = (len(noise_sample) - frame_size) // hop_size + 1
        window = np.hanning(frame_size)
        noise_spectrum = np.zeros(frame_size)
        
        for i in range(num_frames):
            start = i * hop_size
            end = start + frame_size
            
            if end > len(noise_sample):
                break
            
            frame = noise_sample[start:end] * window
            spectrum = np.abs(fft(frame))
            noise_spectrum += spectrum
        
        noise_spectrum /= num_frames
        return noise_spectrum
    
    @staticmethod
    def wiener_filter(audio_data: np.ndarray, sample_rate: int,
                     noise_level: float = 0.01) -> np.ndarray:
        """
        维纳滤波降噪
        
        Args:
            audio_data: 音频数据
            sample_rate: 采样率
            noise_level: 噪声水平估计
            
        Returns:
            降噪后的音频数据
        """
        try:
            # 如果是立体声，分别处理每个声道
            if len(audio_data.shape) == 2:
                result = np.zeros_like(audio_data)
                for i in range(audio_data.shape[1]):
                    result[:, i] = AudioNoiseRemover._wiener_filter_channel(
                        audio_data[:, i], noise_level
                    )
                return result
            else:
                return AudioNoiseRemover._wiener_filter_channel(audio_data, noise_level)
        except Exception as e:
            raise Exception(f"维纳滤波失败: {str(e)}")
    
    @staticmethod
    def _wiener_filter_channel(audio_data: np.ndarray, noise_level: float) -> np.ndarray:
        """
        对单个声道应用维纳滤波
        """
        frame_size = 2048
        hop_size = frame_size // 4
        window = np.hanning(frame_size)
        
        num_frames = (len(audio_data) - frame_size) // hop_size + 1
        output = np.zeros(len(audio_data))
        
        for i in range(num_frames):
            start = i * hop_size
            end = start + frame_size
            
            if end > len(audio_data):
                break
            
            frame = audio_data[start:end] * window
            spectrum = fft(frame)
            power = np.abs(spectrum) ** 2
            
            # 维纳滤波
            noise_power = noise_level ** 2
            wiener_gain = np.maximum(1 - noise_power / (power + 1e-10), 0)
            
            filtered_spectrum = spectrum * wiener_gain
            filtered_frame = np.real(ifft(filtered_spectrum))
            
            output[start:end] += filtered_frame * window
        
        return output.astype(np.float32)
