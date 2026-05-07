# 🎙️ Local AI Meeting Recorder

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green.svg)
![AI](https://img.shields.io/badge/AI-Local%20%7C%20OpenAI%20%7C%20Gemini-orange.svg)
![Privacy](https://img.shields.io/badge/Privacy-Offline_Ready-success.svg)

A desktop application that records audio, transcribes speech to text, and summarizes meeting notes using your choice of AI provider — fully local with no API key, or powered by OpenAI/Gemini with your own key.

## ✨ Key Features

- **Provider Selection**: Choose between **Local (Ollama)**, **OpenAI**, or **Gemini** from a dropdown — switch anytime without restarting.
- **100% Local Mode**: Uses `faster-whisper` for offline STT and `Ollama` (Llama 3.1) for summarization. No internet or API key required.
- **Cloud Mode**: Plug in your OpenAI or Gemini API key for higher accuracy transcription and summarization.
- **Non-blocking UI**: Heavy AI tasks run on background QThreads so the interface stays responsive throughout.

## 📦 Download (macOS — No Installation Required)

Download the pre-built app from the [Releases page](https://github.com/YH-Paradise/ai_recorder/releases):

1. Download `AI_Meeting_Recorder_macOS.zip`
2. Unzip and move `AI_Meeting_Recorder.app` to your Applications folder
3. On first launch: right-click → **Open** (bypasses Gatekeeper for unsigned apps)

> **Apple Silicon (arm64) only.** Intel Mac support is not included in this build.

## ⚙️ Environment Requirements

### All Modes
- macOS 11.0+ (Apple Silicon recommended)
- Microphone access permission

### Local (Ollama) Mode
- [Ollama](https://ollama.com/) installed and running
- Llama 3.1 model pulled:
  ```bash
  ollama run llama3.1
  # Once the >>> prompt appears, type /bye to exit
  # Ollama must keep running in the background
  ```
- ~16GB RAM recommended
- First run auto-downloads the Whisper `base` model (~145MB)

### OpenAI Mode
- OpenAI API key (`sk-...`)

### Gemini Mode
- Google AI API key (`AIza...`) from [Google AI Studio](https://aistudio.google.com/)

## 🚀 Running from Source

```bash
# Clone
git clone https://github.com/YH-Paradise/ai_recorder.git
cd ai_recorder

# Create and activate conda environment
conda create -n ai_recorder python=3.11
conda activate ai_recorder

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

## 💻 Usage

1. Launch the app
2. Select your **AI Provider** from the dropdown
3. Enter your API key if using OpenAI or Gemini (hidden for Local mode)
4. Set **Audio Path** and **Summary Path** (defaults are fine)
5. Click **[Start Recording]**
6. Click **[Stop Recording & Start Summary]** when done
7. A dialog will appear when the summary is saved

## ⚠️ Troubleshooting

| Issue | Solution |
|---|---|
| First-run delay (Local mode) | Whisper base model downloads on first use (~145MB) — wait a moment |
| Ollama error | Make sure `ollama serve` is running before starting Local mode |
| Microphone error | Grant Python/app microphone access in System Settings → Privacy |
| "App is damaged" warning | Right-click → Open, or run `xattr -cr AI_Meeting_Recorder.app` in Terminal |

## 📄 License

MIT License — free to modify and distribute.
