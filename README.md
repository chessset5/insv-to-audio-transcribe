# insv-to-audio-transcribe

Extracts audio from an insv file and creates a wav file. then transcribes the audio. requires ffmpeg in path, cuda toolkit if using an Nvidia gpu,ROCm (Radeon Open Compute) toolkit if using an AMD gpu.

Currently targeting the RTX 1000 ada laptop gpu

Libraries:

```bash
conda create -y -n transcribe python=3.11.11
conda activate transcribe
pip3 install openai-whisper srt
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```

## Nvidia GPUs

[https://developer.nvidia.com/cuda-12-6-0-download-archive](https://developer.nvidia.com/cuda-12-6-0-download-archive)

## AMD GPUs

[https://rocm.blogs.amd.com/artificial-intelligence/whisper/README.html](https://rocm.blogs.amd.com/artificial-intelligence/whisper/README.html)