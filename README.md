# insv-to-audio-transcribe

Extracts audio from an insv file and creates a wav file. then transcribes the audio. requires ffmpeg in path, cuda toolkit if using an Nvidia gpu,ROCm (Radeon Open Compute) toolkit if using an AMD gpu.

Currently targeting the RTX 1000 ada laptop gpu

Libraries:

```bash
pip install openai-whisper srt
```
