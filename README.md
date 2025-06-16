# cnbc-stream-transcriber

A small command-line utility that

1. records CNBC’s TuneIn HLS audio feed with **FFmpeg**  
2. cuts the stream into two-minute AAC segments  
3. transcribes each segment with **OpenAI Whisper**  
4. appends every transcript to a single rolling text file.

The project is designed for unattended, long-running use on any machine that supports Python 3.9+ and FFmpeg.

---

## Features

* Automatic reconnection if the network drops
* Fixed-length audio segments (default: 120 s)
* Incremental transcription as soon as each segment finishes
* Single output text file (`cnbc_live.txt`)
* Works on CPU or GPU

---

## Requirements

* Python 3.9 or later  
* FFmpeg in the system path  
* An internet connection that can reach `tunein.com`  
* (Optional) CUDA-capable GPU for faster transcription

---

## Installation

```bash
git clone https://github.com/YOUR-USER/cnbc-stream-transcriber.git
cd cnbc-stream-transcriber

python3 -m venv .venv
source .venv/bin/activate          # Windows: .\.venv\Scripts\activate
python -m pip install --upgrade pip wheel
pip install -r requirements.txt

