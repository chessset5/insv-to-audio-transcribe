import torch
print(torch.version.cuda)
print(torch.cuda.is_available())

# List available GPUs
for i in range(torch.cuda.device_count()):
    print(f"GPU {i}: {torch.cuda.get_device_name(i)}")

# Check if CUDA is available
if torch.cuda.is_available():
    print(f"Using GPU: {torch.cuda.current_device()}")
else:
    print("No GPU found, using CPU.")