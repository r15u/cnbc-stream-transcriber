# cnbc-stream-transcriber
Continuously records CNBC’s TuneIn HLS feed, slices it into 2-minute AAC chunks
with `ffmpeg`, and uses OpenAI Whisper (Python) to append everything into a
single rolling text file.
