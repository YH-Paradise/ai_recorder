import time
from openai import OpenAI
from PyQt6.QtCore import QThread, pyqtSignal

_SYSTEM_PROMPT = (
    "You are a professional meeting minutes AI. "
    "Please summarize the meeting according to the following structure:\n"
    "1. Core Topic\n"
    "2. Key Discussions\n"
    "3. Conclusion and Action Items"
)

_DUMMY_SUMMARY = (
    "[Test Mode] No API key entered, returning dummy text.\n"
    "1. Audio file saved successfully.\n"
    "2. UI thread separation confirmed working."
)


class TranscribeSummarizeThread(QThread):
    summary_ready = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, audio_path, summary_path, api_key):
        super().__init__()
        self.audio_path = audio_path
        self.summary_path = summary_path
        self.api_key = api_key

    def run(self):
        if not self.api_key.strip():
            self._run_test_mode()
            return

        try:
            client = OpenAI(api_key=self.api_key)
            raw_text = self._transcribe(client)
            summary = self._summarize(client, raw_text)
            self._save(summary)
            self.summary_ready.emit(self.summary_path)
        except Exception as e:
            self.error_signal.emit(str(e))

    def _transcribe(self, client: OpenAI) -> str:
        with open(self.audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en",
            )
        return transcription.text

    def _summarize(self, client: OpenAI, text: str) -> str:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": f"Meeting Transcript:\n\n{text}"},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content

    def _save(self, text: str):
        with open(self.summary_path, "w", encoding="utf-8") as f:
            f.write(text)

    def _run_test_mode(self):
        time.sleep(2)
        self._save(_DUMMY_SUMMARY)
        self.summary_ready.emit(self.summary_path)
