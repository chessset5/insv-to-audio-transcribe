# THIS IS A GUI PROGRAM! PLEASE RUN FILE TO MAKE GUI!


import os
import sys
from datetime import timedelta

import whisper.utils

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_path not in sys.path:
    sys.path.append(project_path)

import whisper

from apps.misc.FileNameFunctions import (get_base_file_name,
                                         get_path_components,
                                         increment_filename)


def transcribe_audio_files(file_paths: list[str], output_dir: str) -> list[str]:
    # Load the Whisper model
    model: whisper.Whisper = whisper.load_model(
        name="turbo", in_memory=True
    )  # Use the second GPU (index 1)

    output_files = list[str]()

    for file_path in file_paths:
        # Check if the file exists
        if os.path.exists(file_path):
            print("transcribing: ", str(file_path))
            # Transcribe the audio file
            result = model.transcribe(file_path)

            # Create the output file path
            name = get_base_file_name(file_path=file_path)
            output_txt_file_path = os.path.normpath(path=os.path.join(output_dir, os.path.basename(name) + ".txt"))
            output_srt_file_path = os.path.normpath(path=os.path.join(output_dir, os.path.basename(name) + ".srt"))
            output_vtt_file_path = os.path.normpath(path=os.path.join(output_dir, os.path.basename(name) + ".vtt"))
            output_tsv_file_path = os.path.normpath(path=os.path.join(output_dir, os.path.basename(name) + ".tsv"))
            output_json_file_path = os.path.normpath(path=os.path.join(output_dir, os.path.basename(name) + ".json"))
            output_txt_file_path: str = increment_filename(file_path=output_txt_file_path)
            output_srt_file_path: str = increment_filename(file_path=output_srt_file_path)
            output_vtt_file_path: str = increment_filename(file_path=output_vtt_file_path)
            output_tsv_file_path: str = increment_filename(file_path=output_tsv_file_path)
            output_json_file_path: str = increment_filename(file_path=output_json_file_path)
            
            print(f"Writing the following transcription for {file_path} at\
                \n\t{output_txt_file_path}\
                \n\t{output_srt_file_path}\
                \n\t{output_vtt_file_path}\
                \n\t{output_tsv_file_path}\
                \n\t{output_json_file_path}")
            
            # file_dir: str = os.path.normpath(os.path.dirname(file_path))
            
            # Save as an SRT file
            output_txt_writer = whisper.utils.get_writer("txt", output_dir)
            output_txt_writer(result, output_txt_file_path,{})


            # Save as a VTT file
            output_srt_writer = whisper.utils.get_writer("srt", output_dir)
            output_srt_writer(result, output_srt_file_path,{})
            
            # Save as an SRT file
            output_vtt_writer = whisper.utils.get_writer("vtt", output_dir)
            output_vtt_writer(result, output_vtt_file_path,{})
            
            # Save as an SRT file
            output_tsv_writer = whisper.utils.get_writer("tsv", output_dir)
            output_tsv_writer(result, output_tsv_file_path,{})
            
            # Save as an SRT file
            output_json_writer = whisper.utils.get_writer("json", output_dir)
            output_json_writer(result, output_json_file_path,{})


            

            output_files.append(output_txt_file_path)
            output_files.append(output_srt_file_path)
            output_files.append(output_vtt_file_path)
            output_files.append(output_tsv_file_path)
            output_files.append(output_json_file_path)
            

            print(f"Transcript saved for {file_path} at {output_txt_file_path}")
            print(f"srt captions for {file_path} at {output_srt_file_path}")
        else:
            print(f"File not found: {file_path}")

    return output_files

def run_scripts(list:list[str])->None:
    for i in list:
        dir: str = get_path_components(file_path=i)[r"dir"]
        transcribe_audio_files(file_paths=[i],output_dir=dir)