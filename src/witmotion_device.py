import serial
import pywitmotion as wit
import numpy as np
from typing import Optional, Tuple, List
import time

class WitmotionDevice:
    def __init__(self, serial_device: str = "/dev/rfcomm0"):
        """
        Initialize the Witmotion device connection.
        
        Args:
            serial_device (str): Path to the serial device (default: "/dev/rfcomm0")
        """
        self.serial_device = serial_device
        self.serial = None
        self.connected = False
        
    def connect(self) -> bool:
        """
        Connect to the Witmotion device.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            print(f"Connecting to Witmotion device on {self.serial_device}...")
            self.serial = serial.Serial(self.serial_device, 115200, timeout=1)
            
            # Wait for connection to stabilize
            time.sleep(1)
            
            self.connected = True
            print("Connected successfully")
            return True
        except Exception as e:
            print(f"Failed to connect to device: {e}")
            self.connected = False
            return False
            
    def disconnect(self):
        """Disconnect from the device."""
        if self.serial and self.serial.is_open:
            self.serial.close()
            self.connected = False
            
    def collect_data(self, duration: float) -> Tuple[np.ndarray, List[float], List[float]]:
        """
        Collect both acceleration and gyroscope data from the device for a specified duration.
        
        Args:
            duration (float): Duration to collect data in seconds
            
        Returns:
            Tuple[np.ndarray, List[float], List[float]]: Array of timestamps, list of acceleration data points,
                                                        and list of gyroscope data points
        """
        if not self.connected:
            raise RuntimeError("Device not connected")
            
        timestamps = []
        acceleration_points = []
        gyroscope_points = []
        angle_points = []
        mag_points = []
        q_points = []
        start_time = time.time()
        
        print(f"Collecting data for {duration} seconds...")
        
        while time.time() - start_time < duration:
            try:
                if self.serial.in_waiting:
                    data = self.serial.read_until(b'U')
                    if data:
                        # Get acceleration data
                        accel = wit.get_acceleration(data)
                        # Get gyroscope data
                        gyro = wit.get_gyro(data)
                        # # Get angle data
                        # angle = wit.get_angle(data)
                        # # Get magnetometer data
                        # mag = wit.get_magnetic(data)
                        # # Get quaternion data
                        # q = wit.get_quaternion(data)
                        
                        if accel is not None and gyro is not None:
                            current_time = time.time() - start_time
                            timestamps.append(current_time)
                            acceleration_points.append(accel)
                            gyroscope_points.append(gyro)
                            # angle_points.append(angle)
                            # mag_points.append(mag)
                            # q_points.append(q)
            except Exception as e:
                print(f"Error reading data: {e}")
                break
                
        print(f"Collected {len(acceleration_points)} data points")
        return np.array(timestamps), acceleration_points, gyroscope_points 