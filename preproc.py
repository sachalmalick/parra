import constants as const
import os
import re

def get_movie_name_embedded(folder):
    return folder

def get_movie_name_transcriptions(folder):
    ind = folder.rfind("_by")
    return folder[:ind]


def get_all_files(directory, chapter_regex):
    files = {}
    for file in os.listdir(directory):
        if not file.startswith("."):
            chapter = get_chapter(file, chapter_regex)
            entry = {"name": file,
                     "path": os.path.join(directory, file),
                     "chapter": chapter}
            files[chapter] = entry
    return files

def load_folder_contents(folder, get_movie_name, chapter_regex):
    files = {}
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isdir(path):
            files[get_movie_name(file)] = get_all_files(path, chapter_regex)
    return files

def get_chapter(filename, regex_pattern):
    match = re.search(regex_pattern, filename)
    return int(match.group(1))

def load_hume_transcriptions():
    transcriptions_folder = const.DATA_ROOT_PATH + const.TRANSCRIPTIONS_PATH
    transcriptions_files = load_folder_contents(transcriptions_folder,
                                                get_movie_name_transcriptions,
                                                const.TRANSCRIPTIONS_CHAPTER_REGEX)
    
    return transcriptions_files

def load_assembly_transcriptions():
    transcriptions_folder = const.DATA_ROOT_PATH + const.ASSEMBLY_TRANSCRIPTIONS
    transcriptions_files = load_folder_contents(transcriptions_folder,
                                                get_movie_name_embedded,
                                                const.EMBEDDED_CHAPTER_REGEX)
    
    return transcriptions_files

def load_stimuli():
    embedded_folder = const.DATA_ROOT_PATH + const.EMBEDDED_PATH
    stimuli_files = load_folder_contents(embedded_folder,
                                         get_movie_name_embedded,
                                         const.EMBEDDED_CHAPTER_REGEX)
    return stimuli_files
