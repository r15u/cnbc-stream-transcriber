import subprocess, pathlib, time, threading, sys
from datetime import datetime
import whisper
from urllib.parse import urlparse

SEG_LEN = 120         # seconds per AAC slice
MODEL   = "base"      # whisper model size

def recorder(stream_url: str, out_dir: pathlib.Path):
    """Continuously pull CNBC stream, cut into 2-min AAC chunks."""
    while True:
        ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] 🛰️  recorder connected")
        proc = subprocess.Popen([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-stats",
            "-reconnect", "1", "-reconnect_delay_max", "5",
            "-i", stream_url,
            "-c", "copy",
            "-f", "segment", "-segment_time", str(SEG_LEN),
            "-reset_timestamps", "1", "-strftime", "1",
            str(out_dir / "cnbc_%Y-%m-%d_%H-%M-%S.aac"),
        ])
        proc.wait()
        print("⚠️  ffmpeg exited – retrying in 5 s")
        time.sleep(5)

def transcriber(watch_dir: pathlib.Path, outfile: pathlib.Path):
    """Watch for new AAC slices and append their transcript to one file."""
    model = whisper.load_model(MODEL)
    done  = set()

    # create / truncate the outfile first time we start
    outfile.write_text(f"# CNBC live transcript – started {datetime.now()}\n\n")

    while True:
        for aac in sorted(watch_dir.glob("cnbc_*.aac")):
            if aac not in done and aac.stat().st_size:
                print("📝 transcribing", aac.name)
                result = model.transcribe(str(aac), fp16=False)
                with outfile.open("a", encoding="utf-8") as f:
                    f.write(result["text"].strip() + "\n\n")
                done.add(aac)
        time.sleep(10)

def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: stream_hls.py <HLS-playlist-URL> [outfile.txt]")
    stream_url = sys.argv[1]
    if not urlparse(stream_url).path.endswith(".m3u8"):
        sys.exit("❌ That doesn’t look like an HLS playlist – aborting.")

    root   = pathlib.Path(".")
    outtxt = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else root / "cnbc_live.txt"

    threading.Thread(target=recorder,   args=(stream_url, root), daemon=True).start()
    transcriber(root, outtxt)   # ← runs in main thread

if __name__ == "__main__":
    main()
