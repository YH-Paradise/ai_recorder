import numpy as np
import sounddevice as sd
import soundfile as sf
from PyQt6.QtCore import QThread, pyqtSignal


class AudioRecorderThread(QThread):
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, save_path, fs=44100):
        super().__init__()
        self.save_path = save_path
        self.fs = fs
        self.is_recording = True
        self.audio_data = []

    def run(self):
        try:
            with sd.InputStream(samplerate=self.fs, channels=1, dtype="float32") as stream:
                while self.is_recording:
                    data, _ = stream.read(self.fs)
                    self.audio_data.append(data)

            if not self.audio_data:
                self.error_signal.emit("No audio was recorded.")
                return

            audio_concat = np.concatenate(self.audio_data, axis=0)
            sf.write(self.save_path, audio_concat, self.fs)
            self.finished_signal.emit(self.save_path)
        except Exception as e:
            self.error_signal.emit(str(e))

    def stop(self):
        self.is_recording = False
