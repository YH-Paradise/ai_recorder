import numpy as np
import sounddevice as sd
import soundfile as sf
from PyQt6.QtCore import QThread, pyqtSignal


class AudioRecorderThread(QThread):
    finished_signal = pyqtSignal(str)

    def __init__(self, save_path, fs=44100):
        super().__init__()
        self.save_path = save_path
        self.fs = fs
        self.is_recording = True
        self.audio_data = []

    def run(self):
        with sd.InputStream(samplerate=self.fs, channels=1, dtype='float32') as stream:
            while self.is_recording:
                data, overflowed = stream.read(self.fs)
                self.audio_data.append(data)

        if self.audio_data:
            audio_concat = np.concatenate(self.audio_data, axis=0)
            sf.write(self.save_path, audio_concat, self.fs)
            self.finished_signal.emit(self.save_path)

    def stop(self):
        self.is_recording = False