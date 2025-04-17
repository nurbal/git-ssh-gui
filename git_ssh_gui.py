import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QPushButton, QLineEdit, QLabel,
                           QTextEdit, QFormLayout, QMessageBox)
from PyQt6.QtCore import Qt
import paramiko
from git import Repo
import os

class GitSSHGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Git SSH GUI")
        self.setMinimumSize(800, 600)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # SSH Connection Form
        ssh_form = QFormLayout()
        self.host_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        ssh_form.addRow("Host:", self.host_input)
        ssh_form.addRow("Username:", self.username_input)
        ssh_form.addRow("Password:", self.password_input)
        
        # Connect Button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_ssh)
        
        # Git Operations
        git_layout = QVBoxLayout()
        self.repo_path_input = QLineEdit()
        self.clone_url_input = QLineEdit()
        
        git_form = QFormLayout()
        git_form.addRow("Repository Path:", self.repo_path_input)
        git_form.addRow("Clone URL:", self.clone_url_input)
        
        self.clone_button = QPushButton("Clone Repository")
        self.clone_button.clicked.connect(self.clone_repository)
        
        # Output Area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        
        # Add all layouts to main layout
        layout.addLayout(ssh_form)
        layout.addWidget(self.connect_button)
        layout.addLayout(git_form)
        layout.addWidget(self.clone_button)
        layout.addWidget(self.output_area)
        
        # SSH client
        self.ssh_client = None
        
    def connect_ssh(self):
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            host = self.host_input.text()
            username = self.username_input.text()
            password = self.password_input.text()
            
            self.ssh_client.connect(host, username=username, password=password)
            self.output_area.append("Successfully connected to SSH server!")
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", str(e))
            self.output_area.append(f"Connection error: {str(e)}")
            
    def clone_repository(self):
        if not self.ssh_client:
            QMessageBox.warning(self, "Warning", "Please connect to SSH server first!")
            return
            
        try:
            repo_path = self.repo_path_input.text()
            clone_url = self.clone_url_input.text()
            
            # Execute git clone command on remote server
            stdin, stdout, stderr = self.ssh_client.exec_command(f"git clone {clone_url} {repo_path}")
            
            # Read output
            output = stdout.read().decode()
            error = stderr.read().decode()
            
            if output:
                self.output_area.append(output)
            if error:
                self.output_area.append(f"Error: {error}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.output_area.append(f"Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GitSSHGUI()
    window.show()
    sys.exit(app.exec()) 