# local-whisper

Free, local push-to-talk dictation for macOS (Apple Silicon). Replaces Wispr Flow / OpenWhispr.
Hold a key, talk, release → text pastes into whatever app has focus. Audio never leaves the Mac.

## Run

```bash
cd local-whisper
.venv/bin/python dictate.py
```

First launch downloads the model (~1.5GB) once. Then:
**Hold Right Option, talk, release.** Ctrl+C to quit.

## One-time macOS permissions

The terminal app you run this from needs (System Settings → Privacy & Security):
- **Microphone** — to record
- **Input Monitoring** — for `pynput` to see the hotkey
- **Accessibility** — for the `Cmd+V` paste keystroke

macOS will prompt on first use; approve, then restart the script.

## Tune

Edit the top of `dictate.py`:
- `MODEL` — `whisper-large-v3-turbo` (default, best) or `mlx-community/whisper-small.en` (lighter/faster)
- `HOTKEY` — `keyboard.Key.alt_r` → e.g. `keyboard.Key.cmd_r`
