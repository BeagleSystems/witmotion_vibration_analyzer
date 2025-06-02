# Witmotion Vibration Analysis

This project implements real-time vibration analysis using data from Witmotion Bluetooth devices. The analysis is performed using Fast Fourier Transform (FFT) on the time series data received from the device.

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Pair WitMotion device through Bluetooth at least once

   * Open bluetooth, go to settings
   * When the scan shows HC-06 or something similar, connect to it
   * Input the pairing code "1234"
   * HC-06 will show connected once, but disconnected quickly afterward, just make sure it shows paired, will be fine for using it as serial device /dev/rfcomm*

## Project Structure

- `src/`: Source code directory
- `tests/`: Test files directory
- `requirements.txt`: Python package dependencies

## Usage

```bash
python src/main.py
```

## Configuration Parameters

The following parameters can be configured in `src/main.py`:

### Device Configuration
- `SERIAL_DEVICE`: Path to the serial device for the HC-06 module
  - Default: "/dev/rfcomm0"
  - Example: "/dev/rfcomm1" if using two modules, check after pairing
  - Note: The device must be paired via Bluetooth first

### Data Collection
- `SAMPLING_RATE`: FFT sample rate in Hz
  - Default: 10.0 Hz
  - Should match the actual sampling rate of the Witmotion device
  - Witmotion specification shows it's configurable from 0.2Hz to 200Hz, default is 10Hz

- `COLLECTION_DURATION`: Duration of data collection in seconds
  - Default: 120.0 seconds
  - Longer durations provide more data points for analysis
  - Affects the time-domain resolution of the FFT
  - Consider memory usage for very long durations

### Output
The analysis results include:
- Time-domain plots for acceleration and gyroscope data
- Frequency-domain plots showing the FFT analysis
- Dominant frequencies for each axis (X, Y, Z)
- Magnitude of each dominant frequency

## Notes
- The device must be paired via Bluetooth before running the program
- The HC-06 module typically appears as /dev/rfcomm0 after pairing
- The program will automatically create a 'plots' directory for saving visualizations
- Both acceleration and gyroscope data are collected simultaneously for better time synchronization


