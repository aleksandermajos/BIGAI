import os
import subprocess

current_path = os.getcwd()
lang = 'French'
learning_path = '../DATA/PHRASES/LEARNING/'+lang

def get_all_names(path):
    d = os.listdir(path)
    return d

def convert_all_mp3_to_16kbwav(path,delete=True):
    list_of_files = get_all_names(path)
    for name in list_of_files:
        filename, file_extension = os.path.splitext(name)
        if file_extension == '.mp3':
            full_input_path = path + '/' + name
            full_output_path = path + '/' + filename+'.wav'
            subprocess.call(['ffmpeg', '-y', '-i', full_input_path, '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le', full_output_path])
            if delete == True:
                os.remove(full_input_path)


convert_all_mp3_to_16kbwav(path=learning_path,delete=True)
