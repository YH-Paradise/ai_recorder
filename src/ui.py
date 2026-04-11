import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox, QGroupBox)
from PyQt6.QtCore import QTimer

# Import the separated modules.
from src.audio import AudioRecorderThread
from src.ai_worker import TranscribeSummarizeThread


class MeetingRecorderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.recorder_thread = None
        self.summary_thread = None
        self.seconds_elapsed = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('AI Meeting Recorder')
        self.resize(450, 350)
        main_layout = QVBoxLayout()

        # [API Key Settings Area]
        api_group = QGroupBox("OpenAI Settings")
        api_layout = QHBoxLayout()
        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("sk-... (Enter OpenAI API Key, omit for test mode)")
        self.api_input.setEchoMode(QLineEdit.EchoMode.Password)
        api_layout.addWidget(QLabel("API Key:"))
        api_layout.addWidget(self.api_input)
        api_group.setLayout(api_layout)
        main_layout.addWidget(api_group)

        # [Timer and Status Display Area]
        self.status_label = QLabel("Ready...", self)
        self.status_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.time_label = QLabel("00:00", self)
        self.time_label.setStyleSheet("font-size: 32px; color: #d32f2f; font-weight: bold;")

        status_layout = QVBoxLayout()
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.time_label)
        main_layout.addLayout(status_layout)

        # [Save Path Settings Area]
        path_group = QGroupBox("Save Path Settings")
        path_layout = QVBoxLayout()

        audio_layout = QHBoxLayout()
        self.audio_path_input = QLineEdit(os.path.join(os.getcwd(), "meeting_audio.wav"))
        audio_btn = QPushButton("Audio Path")
        audio_btn.clicked.connect(lambda: self.select_save_path(self.audio_path_input, "WAV Files (*.wav)"))
        audio_layout.addWidget(self.audio_path_input)
        audio_layout.addWidget(audio_btn)

        summary_layout = QHBoxLayout()
        self.summary_path_input = QLineEdit(os.path.join(os.getcwd(), "meeting_summary.txt"))
        summary_btn = QPushButton("Summary Path")
        summary_btn.clicked.connect(lambda: self.select_save_path(self.summary_path_input, "Text Files (*.txt)"))
        summary_layout.addWidget(self.summary_path_input)
        summary_layout.addWidget(summary_btn)

        path_layout.addLayout(audio_layout)
        path_layout.addLayout(summary_layout)
        path_group.setLayout(path_layout)
        main_layout.addWidget(path_group)

        # [Recording Control Button]
        self.record_btn = QPushButton("Start Recording", self)
        self.record_btn.setStyleSheet("height: 50px; font-size: 16px; background-color: #4CAF50; color: white; font-weight: bold;")
        self.record_btn.clicked.connect(self.toggle_recording)
        main_layout.addWidget(self.record_btn)

        self.setLayout(main_layout)

    def select_save_path(self, line_edit, file_filter):
        path, _ = QFileDialog.getSaveFileName(self, "Select Save Path", line_edit.text(), file_filter)
        if path:
            line_edit.setText(path)

    def toggle_recording(self):
        if self.recorder_thread is None or not self.recorder_thread.isRunning():
            audio_path = self.audio_path_input.text()
            self.recorder_thread = AudioRecorderThread(audio_path)
            self.recorder_thread.finished_signal.connect(self.start_summarization)

            self.recorder_thread.start()

            self.record_btn.setText("Stop Recording & Start Summary")
            self.record_btn.setStyleSheet("height: 50px; font-size: 16px; background-color: #f44336; color: white; font-weight: bold;")
            self.status_label.setText("🎙️ Recording in progress...")
            self.seconds_elapsed = 0
            self.time_label.setText("00:00")
            self.timer.start(1000)
        else:
            self.recorder_thread.stop()
            self.timer.stop()
            self.record_btn.setEnabled(False)
            self.record_btn.setText("Processing AI Summary...")
            self.record_btn.setStyleSheet("height: 50px; font-size: 16px; background-color: #9e9e9e; color: white;")
            self.status_label.setText("⚙️ Transcribing & Summarizing...")

    def update_timer(self):
        self.seconds_elapsed += 1
        mins, secs = divmod(self.seconds_elapsed, 60)
        self.time_label.setText(f"{mins:02d}:{secs:02d}")

    def start_summarization(self, saved_audio_path):
        summary_path = self.summary_path_input.text()
        api_key = self.api_input.text()

        self.summary_thread = TranscribeSummarizeThread(saved_audio_path, summary_path, api_key)
        self.summary_thread.summary_ready.connect(self.on_process_complete)
        self.summary_thread.error_signal.connect(self.on_process_error)
        self.summary_thread.start()

    def on_process_complete(self, summary_path):
        QMessageBox.information(self, "Complete", f"Meeting summary completed!\n\nSaved at:\n{summary_path}")
        self.reset_ui()

    def on_process_error(self, error_msg):
        QMessageBox.critical(self, "Error Occurred", f"An error occurred during the process:\n\n{error_msg}")
        self.reset_ui()

    def reset_ui(self):
        self.record_btn.setEnabled(True)
        self.record_btn.setText("Start Recording")
        self.record_btn.setStyleSheet("height: 50px; font-size: 16px; background-color: #4CAF50; color: white; font-weight: bold;")
        self.status_label.setText("Ready...")
        self.time_label.setText("00:00")