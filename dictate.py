#!/usr/bin/env python3
"""Local push-to-talk dictation. Hold the hotkey, talk, release -> text pastes into focused app.

Free replacement for Wispr Flow / OpenWhispr. Runs Whisper locally via MLX (Apple Silicon).
Nothing leaves the machine.
"""
import subprocess
import sys
import threading

import numpy as np
import sounddevice as sd
import mlx_whisper
from pynput import keyboard

# --- config ---
MODEL = "mlx-community/whisper-large-v3-turbo"  # fast + accurate on M-series. small.en if you want lighter.
HOLD_KEY = keyboard.Key.alt_r                   # keyboard: HOLD Right Option to talk (bare modifier = no char emitted).
TOGGLE_KEY = keyboard.Key.f13                   # macro pad (Ampligame D6): TAP to start, TAP to stop. F13-F20 emit no char.
SAMPLE_RATE = 16000                             # whisper wants 16k mono
# ---------------

_frames = []
_stream = None
_recording = False
_lock = threading.Lock()


def _paste(text):
    """Clipboard + Cmd+V. Reliable for unicode; needs Accessibility permission."""
    text = text.strip()
    if not text:
        return
    subprocess.run(["pbcopy"], input=text.encode(), check=True)
    subprocess.run([
        "osascript", "-e",
        'tell application "System Events" to keystroke "v" using command down',
    ], check=True)
    print(f"  -> {text}")


def _start():
    global _stream, _frames, _recording
    with _lock:
        if _recording:
            return  # ignore key autorepeat
        _recording = True
        _frames = []
    print("[rec] listening...")

    def cb(indata, frames, time, status):
        _frames.append(indata.copy())

    _stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32", callback=cb)
    _stream.start()


def _stop():
    global _stream, _recording
    with _lock:
        if not _recording:
            return
        _recording = False
    _stream.stop()
    _stream.close()
    _stream = None
    if not _frames:
        return
    audio = np.concatenate(_frames, axis=0).flatten()
    if len(audio) < SAMPLE_RATE * 0.3:  # <0.3s = accidental tap
        print("[skip] too short")
        return
    print("[...] transcribing")
    result = mlx_whisper.transcribe(audio, path_or_hf_repo=MODEL)
    _paste(result["text"])


def main():
    print(f"Loading {MODEL} (first run downloads it)...")
    # warm the model so first real dictation isn't slow
    mlx_whisper.transcribe(np.zeros(SAMPLE_RATE, dtype=np.float32), path_or_hf_repo=MODEL)
    print(f"Ready. HOLD {HOLD_KEY} (keyboard) or TAP {TOGGLE_KEY} (macro pad) to dictate. Ctrl+C to quit.")

    def on_press(key):
        if key == HOLD_KEY:
            _start()
        elif key == TOGGLE_KEY:
            _stop() if _recording else _start()

    def on_release(key):
        if key == HOLD_KEY:
            _stop()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
