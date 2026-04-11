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
            dummy_text = "[테스트 모드] API 키가 입력되지 않아 더미 텍스트를 반환합니다.\n1. 오디오 파일 정상 저장됨\n2. UI 스레드 분리 정상 작동 확인"
            with open(self.summary_path, 'w', encoding='utf-8') as f:
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
                    language="ko"
                )
            raw_text = transcription.text

            # Step 2: LLM (GPT)
            system_prompt = (
                "당신은 전문적인 회의록 작성 AI입니다. "
                "다음 구조에 맞게 회의록을 요약해주세요:\n"
                "1. 핵심 주제\n"
                "2. 주요 논의 사항\n"
                "3. 결론 및 Action Items"
            )
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"회의 녹취록:\n\n{raw_text}"}
                ],
                temperature=0.3
            )
            summary_result = response.choices[0].message.content

            # Step 3: Save Result
            with open(self.summary_path, 'w', encoding='utf-8') as f:
                f.write(summary_result)

            self.summary_ready.emit(self.summary_path)

        except Exception as e:
            self.error_signal.emit(str(e))