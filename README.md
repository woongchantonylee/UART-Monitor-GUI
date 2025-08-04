# UART Monitor

A Python application that provides a graphical interface for monitoring and logging UART/Serial communication. Built with PyQt6 and pyserial.

## Features

- Real-time UART data monitoring
- Automatic COM port detection
- Data logging to CSV files with timestamps
- Configurable baud rate
- Simple and intuitive GUI interface

## Prerequisites

1. Install Visual C++ Build Tools:
   - Download from: [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - During installation, select "Desktop development with C++"
   - This is required for PyQt6 installation

## Installation

### 1. Create a Virtual Environment

```bash
# Create a new virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On Unix/MacOS:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install packages one by one
pip install pyserial
pip install PyQt6
```

If you still encounter installation errors, try:
```bash
pip install --only-binary :all: PyQt6
```

## Usage

1. Activate the virtual environment (if not already activated)
2. Run the program:
```bash
python uart_monitor.py
```

3. Using the interface:
   - Select the COM port from the dropdown menu
   - Choose the desired baud rate
   - Click "Connect" to start monitoring
   - Use "Start Logging" to save data to a CSV file
   - The CSV files are saved with timestamps in the filename

## Data Logging

The program automatically creates CSV files with the following format:
- Filename: `uart_log_YYYYMMDD_HHMMSS.csv`
- Columns: Timestamp, Data

## Requirements

- Python 3.7 or higher
- PyQt6
- pyserial
- Windows, MacOS, or Linux operating system

## Repository

This project is hosted at: https://github.com/woongchantonylee/UART-Monitor-GUI

### Clone the Repository

```bash
git clone https://github.com/woongchantonylee/UART-Monitor-GUI.git
cd UART-Monitor-GUI
```
