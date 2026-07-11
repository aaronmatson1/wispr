# local-whisper

Free, local push-to-talk dictation for macOS (Apple Silicon). Replaces Wispr Flow / OpenWhispr.
Hold a key, talk, release → text pastes into whatever app has focus. Audio never leaves the Mac.

## Run

```bash
cd local-whisper
.venv/bin/python dictate.py
```

First launch downloads the model (~1.5GB) once. Then either:
- **Keyboard:** HOLD Right Option, talk, release → pastes.
- **Macro pad (Ampligame D6):** bind a key to **F13**, TAP to start, TAP to stop.

Ctrl+C to quit.

### Why these keys
Bare `Option`/`Cmd` held alone emit no character — safe as push-to-talk. Avoid `Option+Space`
(non-breaking space) and `Option+M` (`µ`): on Mac they type a character into your text field.
F13–F20 emit nothing and collide with nothing — ideal for a macro pad tap-toggle.

## One-time macOS permissions

The terminal app you run this from needs (System Settings → Privacy & Security):
- **Microphone** — to record
- **Input Monitoring** — for `pynput` to see the hotkey
- **Accessibility** — for the `Cmd+V` paste keystroke

macOS will prompt on first use; approve, then restart the script.

## Tune

Edit the top of `dictate.py`:
- `MODEL` — `whisper-large-v3-turbo` (default, best) or `mlx-community/whisper-small.en` (lighter/faster)
- `HOLD_KEY` — keyboard push-to-talk, `keyboard.Key.alt_r` → e.g. `keyboard.Key.cmd_r`
- `TOGGLE_KEY` — macro pad tap-toggle, `keyboard.Key.f13` → any of `f13`–`f20`
