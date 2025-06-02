import serial
import pywitmotion as wit
import numpy as np
from typing import Optional, Tuple, List
import time

class WitmotionDevice:
    def __init__(self, device_address: str):
        """
        Initialize the Witmotion device connection.
        
        Args:
            device_address (str): Bluetooth address of the Witmotion device
        """
        self.device_address = device_address
        self.serial = None
        self.connected = False
        
    def connect(self) -> bool:
        """
        Connect to the Witmotion device.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            print(f"Connecting to device {self.device_address}...")
            # Convert Bluetooth address to serial port
            # On Linux, HC-06 typically shows up as /dev/rfcomm0
            self.serial = serial.Serial('/dev/rfcomm0', 9600, timeout=1)
            
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
            
    def collect_data(self, duration: float, data_type: str = 'acceleration') -> Tuple[np.ndarray, List[float]]:
        """
        Collect data from the device for a specified duration.
        
        Args:
            duration (float): Duration to collect data in seconds
            data_type (str): Type of data to collect ('acceleration', 'gyro', 'angle', 'magnetic', 'quaternion')
            
        Returns:
            Tuple[np.ndarray, List[float]]: Array of timestamps and list of data points
        """
        if not self.connected:
            raise RuntimeError("Device not connected")
            
        timestamps = []
        data_points = []
        start_time = time.time()
        
        print(f"Collecting {data_type} data for {duration} seconds...")
        
        while time.time() - start_time < duration:
            try:
                if self.serial.in_waiting:
                    data = self.serial.read_until(b'U')
                    if data:
                        if data_type == 'acceleration':
                            q = wit.get_acceleration(data)
                        elif data_type == 'gyro':
                            q = wit.get_gyro(data)
                        elif data_type == 'angle':
                            q = wit.get_angle(data)
                        elif data_type == 'magnetic':
                            q = wit.get_magnetic(data)
                        elif data_type == 'quaternion':
                            q = wit.get_quaternion(data)
                        else:
                            raise ValueError(f"Unknown data type: {data_type}")
                            
                        if q is not None:
                            timestamps.append(time.time() - start_time)
                            data_points.append(q)
            except Exception as e:
                print(f"Error reading data: {e}")
                break
                
        print(f"Collected {len(data_points)} data points")
        return np.array(timestamps), data_points 