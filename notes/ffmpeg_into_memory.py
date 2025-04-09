import subprocess
import io

def transcribe_to_memory(input_file):
    # Create an in-memory buffer
    buffer = io.BytesIO()

    # Run ffmpeg command
    process = subprocess.Popen(
        args=['ffmpeg', '-i', input_file, '-f', 'wav', 'pipe:1'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Read the output into the buffer
    stdout, stderr = process.communicate()
    buffer.write(stdout)

    # Reset buffer position to the beginning
    buffer.seek(0)

    return buffer

# Example usage
input_file = 'your_input_file.mp4'
audio_buffer: io.BytesIO = transcribe_to_memory(input_file=input_file)

# Now you can use audio_buffer as needed
