import os
import sys

from concurrent.futures import ThreadPoolExecutor

# Add the directory containing your project to sys.path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_path not in sys.path:
    sys.path.append(project_path)


from apps.extractAudioFromInsv.extractAudioFromInsv import start_extraction
from apps.transcribeAudio.transcribeAudio import transcribe_audio_files


def run_audio_extract(file: str):
    directory = os.path.normpath(os.path.dirname(file))
    single_file_list = list[str]()
    single_file_list.append(file)
    audio_path: None | list[str] = start_extraction(
        video_files=single_file_list, output_folder=directory
    )

    if not audio_path:
        audio_path = [""]

    return {"path": audio_path[0], "dir": directory}


def run_scripts(file_paths: list[str]) -> None:
    """Placeholder function to process selected files."""

    set_paths = set(file_paths)
    file_paths = list(set_paths)

    with ThreadPoolExecutor() as executor:
        results = executor.map(run_audio_extract, file_paths)

    audio_paths: list[dict[str, str]] = list(results)
    print("transcribing files:", str(audio_paths))
    for audio in audio_paths:
        if audio["path"]:
            t_list = list()
            t_list.append(audio["path"])
            transcribe_audio_files(file_paths=t_list, output_dir=audio["dir"])

    print("Finished")


if __name__ == "__main__":
    file_list = [
        "",
    ]

    from files import FILES

    file_list: list[str] = FILES

    run_scripts(file_paths=file_list)
