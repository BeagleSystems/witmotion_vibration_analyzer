import numpy as np
from scipy.fft import fft
import matplotlib
matplotlib.use('Qt5Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
import os

class VibrationAnalyzer:
    def __init__(self, sampling_rate: float = 100.0):
        """
        Initialize the vibration analyzer.
        
        Args:
            sampling_rate (float): Sampling rate of the data in Hz
        """
        self.sampling_rate = sampling_rate
        # Create output directory for plots
        self.output_dir = "plots"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def compute_fft(self, time_series: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute the FFT of the time series data.
        
        Args:
            time_series (np.ndarray): Array of time series data
            
        Returns:
            Tuple[np.ndarray, np.ndarray]: Frequency array and magnitude array
        """
        # Compute FFT
        fft_result = fft(time_series)
        
        # Compute frequency array
        n = len(time_series)
        freq = np.fft.fftfreq(n, 1/self.sampling_rate)
        
        # Compute magnitude spectrum
        magnitude = np.abs(fft_result)
        
        # Only return positive frequencies
        positive_freq_mask = freq >= 0
        return freq[positive_freq_mask], magnitude[positive_freq_mask]
    
    def plot_all_data(self, accel_data: Dict[str, Tuple[np.ndarray, np.ndarray]], 
                     gyro_data: Dict[str, Tuple[np.ndarray, np.ndarray]]):
        """
        Plot time series and FFT analysis for both acceleration and gyroscope data.
        
        Args:
            accel_data (Dict[str, Tuple[np.ndarray, np.ndarray]]): Dictionary containing timestamps and time series data for acceleration
            gyro_data (Dict[str, Tuple[np.ndarray, np.ndarray]]): Dictionary containing timestamps and time series data for gyroscope
        """
        # Create figure with subplots for acceleration data
        fig_accel = plt.figure(figsize=(15, 10))
        fig_accel.suptitle('Acceleration Data Analysis', fontsize=16)
        
        # Create subplots for acceleration time series
        ax1 = fig_accel.add_subplot(231)
        ax2 = fig_accel.add_subplot(232)
        ax3 = fig_accel.add_subplot(233)
        
        # Create subplots for acceleration FFT
        ax4 = fig_accel.add_subplot(234)
        ax5 = fig_accel.add_subplot(235)
        ax6 = fig_accel.add_subplot(236)
        
        # Plot acceleration data
        for i, (axis, (timestamps, time_series)) in enumerate(accel_data.items()):
            ax = [ax1, ax2, ax3][i]
            ax.plot(timestamps, time_series, 'b-', label=f'{axis}-axis')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Acceleration (g)')
            ax.set_title(f'Time Series - {axis}-axis')
            ax.grid(True)
            ax.legend()
            
            # Compute and plot FFT
            freq, magnitude = self.compute_fft(time_series)
            ax_fft = [ax4, ax5, ax6][i]
            ax_fft.plot(freq, magnitude, 'r-', label='FFT')
            ax_fft.set_xlabel('Frequency (Hz)')
            ax_fft.set_ylabel('Magnitude')
            ax_fft.set_title(f'Frequency Spectrum - {axis}-axis')
            ax_fft.grid(True)
            ax_fft.legend()
            
            # Mark dominant frequencies
            peak_indices = np.argsort(magnitude)[-3:]  # Get top 3 peaks
            for idx in peak_indices:
                ax_fft.plot(freq[idx], magnitude[idx], 'go', markersize=10)
                ax_fft.annotate(f'{freq[idx]:.1f} Hz',
                              xy=(freq[idx], magnitude[idx]),
                              xytext=(10, 10),
                              textcoords='offset points')
        
        plt.tight_layout()
        
        # Create figure with subplots for gyroscope data
        fig_gyro = plt.figure(figsize=(15, 10))
        fig_gyro.suptitle('Gyroscope Data Analysis', fontsize=16)
        
        # Create subplots for gyroscope time series
        ax1 = fig_gyro.add_subplot(231)
        ax2 = fig_gyro.add_subplot(232)
        ax3 = fig_gyro.add_subplot(233)
        
        # Create subplots for gyroscope FFT
        ax4 = fig_gyro.add_subplot(234)
        ax5 = fig_gyro.add_subplot(235)
        ax6 = fig_gyro.add_subplot(236)
        
        # Plot gyroscope data
        for i, (axis, (timestamps, time_series)) in enumerate(gyro_data.items()):
            ax = [ax1, ax2, ax3][i]
            ax.plot(timestamps, time_series, 'g-', label=f'{axis}-axis')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Angular Velocity (deg/s)')
            ax.set_title(f'Time Series - {axis}-axis')
            ax.grid(True)
            ax.legend()
            
            # Compute and plot FFT
            freq, magnitude = self.compute_fft(time_series)
            ax_fft = [ax4, ax5, ax6][i]
            ax_fft.plot(freq, magnitude, 'r-', label='FFT')
            ax_fft.set_xlabel('Frequency (Hz)')
            ax_fft.set_ylabel('Magnitude')
            ax_fft.set_title(f'Frequency Spectrum - {axis}-axis')
            ax_fft.grid(True)
            ax_fft.legend()
            
            # Mark dominant frequencies
            peak_indices = np.argsort(magnitude)[-3:]  # Get top 3 peaks
            for idx in peak_indices:
                ax_fft.plot(freq[idx], magnitude[idx], 'go', markersize=10)
                ax_fft.annotate(f'{freq[idx]:.1f} Hz',
                              xy=(freq[idx], magnitude[idx]),
                              xytext=(10, 10),
                              textcoords='offset points')
        
        plt.tight_layout()
        plt.show(block=True)  # This will block until the window is closed
        
    def analyze_vibration(self, timestamps: np.ndarray, accel_data: Dict[str, np.ndarray], 
                         gyro_data: Dict[str, np.ndarray], plot: bool = True) -> Tuple[Dict[str, Tuple[np.ndarray, np.ndarray]], 
                                                                                      Dict[str, Tuple[np.ndarray, np.ndarray]]]:
        """
        Analyze both acceleration and gyroscope data using FFT.
        
        Args:
            timestamps (np.ndarray): Array of timestamps
            accel_data (Dict[str, np.ndarray]): Dictionary containing acceleration data for each axis
            gyro_data (Dict[str, np.ndarray]): Dictionary containing gyroscope data for each axis
            plot (bool): Whether to plot the results
            
        Returns:
            Tuple[Dict[str, Tuple[np.ndarray, np.ndarray]], Dict[str, Tuple[np.ndarray, np.ndarray]]]: 
                FFT results for both acceleration and gyroscope data
        """
        # Prepare data for plotting
        accel_plot_data = {axis: (timestamps, data) for axis, data in accel_data.items()}
        gyro_plot_data = {axis: (timestamps, data) for axis, data in gyro_data.items()}
        
        if plot:
            self.plot_all_data(accel_plot_data, gyro_plot_data)
            
        # Compute FFT for all axes
        accel_fft_results = {axis: self.compute_fft(data) for axis, data in accel_data.items()}
        gyro_fft_results = {axis: self.compute_fft(data) for axis, data in gyro_data.items()}
        
        return accel_fft_results, gyro_fft_results 