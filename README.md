# 🎙️ Local AI Meeting Recorder

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green.svg)
![AI](https://img.shields.io/badge/AI-100%25_Local-orange.svg)
![Privacy](https://img.shields.io/badge/Privacy-Offline-success.svg)

A desktop application that automatically records audio, transcribes speech to text (STT), and summarizes meeting notes (LLM) **100% locally on your PC without needing an internet connection or paid APIs.**

Perfect for summarizing sensitive internal meetings or personal brainstorming sessions securely without sending data to external servers.

## ✨ Key Features

- **One-Click Recording**: Intuitive GUI built with PyQt6 for easy audio recording and file management.
- **100% Local STT**: Utilizes `faster-whisper` for fast and highly accurate offline speech-to-text conversion.
- **100% Local LLM**: Powered by `Ollama` and open-source models (e.g., Llama 3.1) to automatically summarize the core topics, discussion points, and action items.
- **Multi-threading (QThread)**: Ensures the UI remains responsive and smooth even during heavy AI inference tasks.

## ⚙️ Prerequisites

To run this application, you need the following installed on your system:

1. **Python 3.11+**
2. **Ollama**: Required to run the local LLM. ([Download from the official website](https://ollama.com/))

## 🚀 Installation

1. Clone or download this repository.
   ```bash
   git clone https://github.com/username/ai_meeting_recorder.git
   cd ai_meeting_recorder
   ```

2. (Optional but recommended) Create and activate a virtual environment.
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install the required Python packages.
   ```bash
   pip install PyQt6 sounddevice soundfile numpy faster-whisper openai
   ```

4. Download the AI model for summarization via Ollama (First time only).
   ```bash
   ollama run llama3.1
   ```
   *(Once the download is complete and the `>>>` prompt appears, type `/bye` to exit. Ollama must remain running in the background.)*

## 💻 Usage

1. Run the main script from the root directory.
   ```bash
   python main.py
   ```
2. When the UI appears, set the **Audio Path** and **Summary Path** (or leave them as default).
3. Click **[Start Recording]** to begin recording your meeting.
4. When finished, click **[Stop & Summarize]**.
5. The AI will process the audio in the background. Once completed, a pop-up will notify you, and the summary will be saved to the specified path.

## 📂 Project Structure

```text
ai_meeting_recorder/
├── .gitignore
├── README.md
└── main.py                # Main application script (UI, Audio, AI logic combined)
```

## ⚠️ Troubleshooting

- **First-Run Delay**: The first time you run the app, `faster-whisper` will automatically download its base model (~150MB), which may take a few moments. Subsequent runs will be immediate.
- **Memory (RAM) Requirements**: Since the AI models run locally, a system with at least 16GB of RAM is highly recommended.
- **Microphone Access**: If you encounter an audio recording error, ensure that Python has permission to access your microphone in your OS settings.

## 📄 License

This project is licensed under the MIT License. Feel free to modify and distribute!