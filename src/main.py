import numpy as np
from vibration_analyzer import VibrationAnalyzer
from witmotion_device import WitmotionDevice

def main():
    # Device configuration
    # DEVICE_ADDRESS = "00:0C:BF:07:6D:4A"  # Replace with your device's address
    SERIAL_DEVICE = "/dev/rfcomm0"  # Serial device for HC-06 module
    # default output rate is 10Hz, witmotion spec shows 0.2Hz to 200Hz
    SAMPLING_RATE = 10.0  # data output sample rate in Hz
    COLLECTION_DURATION = 120.0  # data collection duration in seconds
    
    # Initialize the vibration analyzer
    analyzer = VibrationAnalyzer(sampling_rate=SAMPLING_RATE)
    
    # Initialize and connect to the Witmotion device
    device = WitmotionDevice(serial_device=SERIAL_DEVICE)
    if not device.connect():
        print("Failed to connect to device. Exiting...")
        return
    
    try:
        print(f"Collecting data for {COLLECTION_DURATION} seconds...")
        
        # Collect both acceleration and gyroscope data simultaneously
        timestamps, acceleration_data, gyroscope_data = device.collect_data(
            duration=COLLECTION_DURATION
        )
        
        if not acceleration_data or not gyroscope_data:
            print("No data collected. Exiting...")
            return
            
        # Convert data to numpy arrays
        acceleration_array = np.array(acceleration_data)
        gyroscope_array = np.array(gyroscope_data)
        
        # Ensure both arrays have the same length by using the shorter one
        min_length = min(len(acceleration_array), len(gyroscope_array))
        acceleration_array = acceleration_array[:min_length]
        gyroscope_array = gyroscope_array[:min_length]
        timestamps = timestamps[:min_length]
        
        print(f"Using {min_length} data points for analysis")
        
        # Prepare data for analysis
        accel_data = {
            'X': acceleration_array[:, 0],
            'Y': acceleration_array[:, 1],
            'Z': acceleration_array[:, 2]
        }
        
        gyro_data = {
            'X': gyroscope_array[:, 0],
            'Y': gyroscope_array[:, 1],
            'Z': gyroscope_array[:, 2]
        }
        
        # Analyze both acceleration and gyroscope data
        accel_fft, gyro_fft = analyzer.analyze_vibration(
            timestamps=timestamps,
            accel_data=accel_data,
            gyro_data=gyro_data
        )
        
        # Print dominant frequencies for each axis
        print("\nDominant frequencies in acceleration data:")
        for axis in ['X', 'Y', 'Z']:
            print(f"\n{axis}-axis:")
            freq, magnitude = accel_fft[axis]
            peak_indices = np.argsort(magnitude)[-3:]  # Get top 3 peaks
            for idx in peak_indices:
                print(f"  {freq[idx]:.2f} Hz (magnitude: {magnitude[idx]:.2f})")
        
        print("\nDominant frequencies in gyroscope data:")
        for axis in ['X', 'Y', 'Z']:
            print(f"\n{axis}-axis:")
            freq, magnitude = gyro_fft[axis]
            peak_indices = np.argsort(magnitude)[-3:]  # Get top 3 peaks
            for idx in peak_indices:
                print(f"  {freq[idx]:.2f} Hz (magnitude: {magnitude[idx]:.2f})")
                
    except Exception as e:
        print(f"Error during analysis: {e}")
    finally:
        device.disconnect()
        print("\nAnalysis complete.")

if __name__ == "__main__":
    main() 