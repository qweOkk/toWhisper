import os
import ctypes
import librosa
from multiprocessing import Pool
from tqdm import tqdm

# Load shared library
lib = ctypes.CDLL('/home/qjw/toWhisper/libtoWhisper.so')

# Function to process a single audio file
def process_audio(input_file):
    input_path = input_file
    # Assuming input_file is the full path, determine relative path inside the input directory
    relative_path = os.path.relpath(input_file, input_directory)
    output_file = os.path.join(output_directory, relative_path)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure directories exist
    
    # Create argv parameters
    argv = [b"./toWhisper", b"-o", output_file.encode(), b"-l", b"0.6", input_file.encode()]
    argc = len(argv)
    argv_array = (ctypes.POINTER(ctypes.c_char) * (argc + 1))()
    for i, arg in enumerate(argv):
        argv_array[i] = ctypes.create_string_buffer(arg)
    argv_array[argc] = None
    
    # Call genwave function
    result = lib.main(argc, argv_array)
    if result != 0:
        print(f"Failed to process {input_file}: {result}")
    else:
        return input_file

# Main function to process all audio files in a directory
def process_directory(input_dir):
    global input_directory, output_directory
    input_directory = input_dir
    output_directory = '/home/qjw/Amphion/LJSpeech-1.1/whisper'  # Specify your output directory here
    
    # Find all WAV files recursively
    wav_files = []
    for root, _, files in os.walk(input_directory):
        for file in files:
            if file.endswith('.wav'):
                wav_files.append(os.path.join(root, file))
    
    # Process each WAV file using multiprocessing pool with tqdm progress bar
    with Pool() as pool, tqdm(total=len(wav_files)) as pbar:
        for _ in pool.imap_unordered(process_audio, wav_files):
            pbar.update(1)

# Example usage
if __name__ == "__main__":
    input_directory = '/home/qjw/Amphion/LJSpeech-1.1/wavs'
    process_directory(input_directory)
