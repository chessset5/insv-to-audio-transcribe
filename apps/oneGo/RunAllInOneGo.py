import os
import sys

from concurrent.futures import ThreadPoolExecutor

# Add the directory containing your project to sys.path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_path not in sys.path:
    sys.path.append(project_path)


from apps.FileNameFunctions import (
    increment_filename,
    get_base_file_name,
    get_path_components,
)


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


def run_make_lrv_srt(file_paths: list[str], transcribe_list: list[str]) -> None:

    srt_dict = dict[str, str]()
    for file in transcribe_list:
        if file.endswith("srt"):
            insv_name: str = get_base_file_name(file_path=file)
            srt_dict.update({insv_name: file})

    for file in file_paths:
        # get lrv name
        insv_path_components: dict[str, str] = get_path_components(file_path=file)
        insv_directory: str = insv_path_components["dir"]
        insv_name: str = insv_path_components["filename"]
        insv_ext: str = insv_path_components["ext"]
        lrv_ext: str = ".lrv"

        # replace VID components with LRV component and check to see if path exits of LRV video
        if insv_name.startswith("VID"):
            # lrv_name: str = insv_name.replace("VID", "LRV")
            #TODO FINISH THIS!!!
            lrv_name :str = insv_name[3:]

            # check if the LRV file exists
            if os.path.exists(
                os.path.normpath(os.path.join(insv_directory, lrv_name + lrv_ext))
            ):
                # check to see if a srt was just created
                # copy srt of INSV and make one for LRV
                if insv_name in srt_dict:
                    insv_srt_path: str = srt_dict[insv_name]
                    insv_srt_path_components: dict[str, str] = get_path_components(
                        file_path=insv_srt_path
                    )
                    insv_srt_dir: str = insv_srt_path_components["dir"]
                    lrv_srt_path: str = os.path.normpath(
                        path=os.path.join(insv_srt_dir, lrv_name + ".srt")
                    )
                    with open(
                        file=insv_srt_path, mode="r", encoding="utf-8"
                    ) as insv_srt_file:
                        with open(
                            file=lrv_srt_path, mode="w", encoding="utf-8"
                        ) as lrv_srt_file:
                            lrv_srt_file.writelines(insv_srt_file.readlines())


def run_scripts(file_paths: list[str]) -> None:
    """Placeholder function to process selected files."""

    set_paths = set(file_paths)
    file_paths = list(set_paths)

    with ThreadPoolExecutor() as executor:
        results = executor.map(run_audio_extract, file_paths)

    audio_paths: list[dict[str, str]] = list(results)
    print("transcribing files:", str(audio_paths))

    transcribe_files = list[str]()
    for audio in audio_paths:
        if audio["path"]:
            t_list = list()
            t_list.append(audio["path"])
            output_list = transcribe_audio_files(
                file_paths=t_list, output_dir=audio["dir"]
            )
            transcribe_files.extend(output_list)

    print("making srt for lrv")
    run_make_lrv_srt(file_paths=file_paths, transcribe_list=transcribe_files)

    print("Finished")


if __name__ == "__main__":
    file_list = [
        "",
    ]

    from files import FILES

    file_list: list[str] = FILES

    run_scripts(file_paths=file_list)
