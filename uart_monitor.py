import sys
import serial
import serial.tools.list_ports
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QComboBox, QPushButton, QTextEdit,
                            QLabel)
from PyQt6.QtCore import QTimer
import csv
from datetime import datetime

class UARTMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UART Monitor")
        self.setGeometry(100, 100, 600, 400)
        
        self.serial_port = None
        self.is_logging = False
        self.csv_file = None
        self.csv_writer = None
        
        self.baud_rates = ['9600', '19200', '38400', '57600', '115200']
        
        self.init_ui()
        self.update_ports()
        
        # Timer for reading serial data
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial)
        self.timer.start(100)  # Read every 100ms

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Port selection and connection
        port_layout = QHBoxLayout()
        self.port_combo = QComboBox()
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.update_ports)
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.toggle_connection)
        
        port_layout.addWidget(QLabel("Port:"))
        port_layout.addWidget(self.port_combo)
        port_layout.addWidget(self.refresh_button)
        port_layout.addWidget(self.connect_button)
        
        # Add baud rate selection
        port_layout.addWidget(QLabel("Baud:"))
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(self.baud_rates)
        port_layout.addWidget(self.baud_combo)
        
        # Logging controls
        log_layout = QHBoxLayout()
        self.log_button = QPushButton("Start Logging")
        self.log_button.clicked.connect(self.toggle_logging)
        log_layout.addWidget(self.log_button)
        
        # Data display
        self.data_display = QTextEdit()
        self.data_display.setReadOnly(True)
        
        layout.addLayout(port_layout)
        layout.addLayout(log_layout)
        layout.addWidget(self.data_display)

    def update_ports(self):
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(port.device)

    def toggle_connection(self):
        if self.serial_port is None:
            try:
                port = self.port_combo.currentText()
                baud = int(self.baud_combo.currentText())
                self.serial_port = serial.Serial(port, baud, timeout=0)
                self.connect_button.setText("Disconnect")
                self.port_combo.setEnabled(False)
            except serial.SerialException as e:
                self.data_display.append(f"Error: {str(e)}")
        else:
            self.serial_port.close()
            self.serial_port = None
            self.connect_button.setText("Connect")
            self.port_combo.setEnabled(True)

    def toggle_logging(self):
        if not self.is_logging:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"uart_log_{timestamp}.csv"
            self.csv_file = open(filename, 'w', newline='')
            self.csv_writer = csv.writer(self.csv_file)
            self.csv_writer.writerow(['Timestamp', 'Data'])
            self.is_logging = True
            self.log_button.setText("Stop Logging")
        else:
            if self.csv_file:
                self.csv_file.close()
                self.csv_file = None
            self.is_logging = False
            self.log_button.setText("Start Logging")

    def read_serial(self):
        if self.serial_port and self.serial_port.is_open:
            try:
                if self.serial_port.in_waiting:
                    data = self.serial_port.readline().decode().strip()
                    self.data_display.append(data)
                    
                    if self.is_logging and self.csv_writer:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                        self.csv_writer.writerow([timestamp, data])
            except serial.SerialException as e:
                self.data_display.append(f"Error: {str(e)}")
                self.toggle_connection()

def main():
    app = QApplication(sys.argv)
    window = UARTMonitor()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
