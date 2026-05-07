from PyQt6.QtCore import QThread, pyqtSignal

PROVIDER_LOCAL = "Local (Ollama)"
PROVIDER_OPENAI = "OpenAI"
PROVIDER_GEMINI = "Gemini"

_SYSTEM_PROMPT = (
    "You are a professional meeting minutes AI. "
    "Please summarize the meeting according to the following structure:\n"
    "1. Core Topic\n"
    "2. Key Discussions\n"
    "3. Conclusion and Action Items"
)

_WHISPER_MODEL = "base"
_OLLAMA_MODEL = "llama3.1"


class TranscribeSummarizeThread(QThread):
    summary_ready = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, audio_path, summary_path, provider, api_key=""):
        super().__init__()
        self.audio_path = audio_path
        self.summary_path = summary_path
        self.provider = provider
        self.api_key = api_key

    def run(self):
        try:
            if self.provider == PROVIDER_LOCAL:
                self._run_local()
            elif self.provider == PROVIDER_OPENAI:
                self._run_openai()
            elif self.provider == PROVIDER_GEMINI:
                self._run_gemini()
            else:
                self.error_signal.emit(f"Unknown provider: {self.provider}")
        except Exception as e:
            self.error_signal.emit(str(e))

    # ── Local (Ollama + faster-whisper) ──────────────────────────────────────

    def _run_local(self):
        raw_text = self._transcribe_local()
        summary = self._summarize_ollama(raw_text)
        self._save(summary)
        self.summary_ready.emit(self.summary_path)

    def _transcribe_local(self) -> str:
        from faster_whisper import WhisperModel
        model = WhisperModel(_WHISPER_MODEL, device="cpu", compute_type="int8")
        segments, _ = model.transcribe(self.audio_path, language="en")
        return " ".join(segment.text for segment in segments)

    def _summarize_ollama(self, text: str) -> str:
        import ollama
        response = ollama.chat(
            model=_OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": f"Meeting Transcript:\n\n{text}"},
            ],
        )
        return response.message.content

    # ── OpenAI ───────────────────────────────────────────────────────────────

    def _run_openai(self):
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        raw_text = self._transcribe_openai(client)
        summary = self._summarize_openai(client, raw_text)
        self._save(summary)
        self.summary_ready.emit(self.summary_path)

    def _transcribe_openai(self, client) -> str:
        with open(self.audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en",
            )
        return transcription.text

    def _summarize_openai(self, client, text: str) -> str:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": f"Meeting Transcript:\n\n{text}"},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content

    # ── Gemini ───────────────────────────────────────────────────────────────

    def _run_gemini(self):
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        raw_text = self._transcribe_gemini(genai)
        summary = self._summarize_gemini(genai, raw_text)
        self._save(summary)
        self.summary_ready.emit(self.summary_path)

    def _transcribe_gemini(self, genai) -> str:
        model = genai.GenerativeModel("gemini-1.5-flash")
        audio_file = genai.upload_file(path=self.audio_path, mime_type="audio/wav")
        try:
            response = model.generate_content(
                ["Please transcribe this audio file verbatim:", audio_file]
            )
            return response.text
        finally:
            genai.delete_file(audio_file.name)

    def _summarize_gemini(self, genai, text: str) -> str:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"{_SYSTEM_PROMPT}\n\nMeeting Transcript:\n\n{text}"
        )
        return response.text

    # ── Common ───────────────────────────────────────────────────────────────

    def _save(self, text: str):
        with open(self.summary_path, "w", encoding="utf-8") as f:
            f.write(text)
