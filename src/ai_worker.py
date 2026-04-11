import time
from openai import OpenAI
from PyQt6.QtCore import QThread, pyqtSignal


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
            time.sleep(2)
            dummy_text = "[Test Mode] No API key entered, returning dummy text.\n1. Audio file saved successfully.\n2. UI thread separation confirmed working."
            with open(self.summary_path, "w", encoding="utf-8") as f:
                f.write(dummy_text)
            self.summary_ready.emit(self.summary_path)
            return

        try:
            client = OpenAI(api_key=self.api_key)

            # Step 1: STT (Whisper)
            with open(self.audio_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en",  # Changed from "ko" to "en"
                )
            raw_text = transcription.text

            # Step 2: LLM (GPT)
            system_prompt = (
                "You are a professional meeting minutes AI. "
                "Please summarize the meeting according to the following structure:\n"
                "1. Core Topic\n"
                "2. Key Discussions\n"
                "3. Conclusion and Action Items"
            )
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Meeting Transcript:\n\n{raw_text}"},
                ],
                temperature=0.3,
            )
            summary_result = response.choices[0].message.content

            # Step 3: Save Result
            with open(self.summary_path, "w", encoding="utf-8") as f:
                f.write(summary_result)

            self.summary_ready.emit(self.summary_path)

        except Exception as e:
            self.error_signal.emit(str(e))
