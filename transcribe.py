import assemblyai as aai
import os
import constants as const
import json
from util import load_json_file
import itertools
import preproc

aai.settings.api_key = "REDACTED"
transcriber = aai.Transcriber()

def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def process_files(directory, outdir):
    print(directory)
    for filename in os.listdir(directory):
        if filename.endswith('.avi') and not filename.startswith('.'):
            result = transcriber.transcribe(os.path.join(directory, filename))
            newfn = filename.replace('.avi', '.json')
            write_json(result.json_response, os.path.join(outdir, newfn))
            print("done with", filename)

class Transcription:
    def __init__(self, text, start, end, transcription_type, movie, chapter):
        self.text = text
        self.start = start
        self.end = end
        self.transcription_type = transcription_type
        self.movie = movie
        self.chapter = chapter

class HumeTranscriptionSet:
    def __init__(self, transcriptions_files):
        self.transcriptions_files = transcriptions_files
        self.movies = list(transcriptions_files.keys())
        print(self.movies)
        self.chapters = {movie: list(transcriptions_files[movie].keys())
                                for movie in self.movies}

    def get_snippets(self, movie_name, chapter_num):
        chapter = self.transcriptions_files[movie_name][chapter_num]
        transcription_json = load_json_file(chapter["path"])
        phrases = transcription_json["supervisions"]
        word_dics = [phrase["alignment"]["word"] for phrase in phrases]
        words_flat = list(itertools.chain.from_iterable(word_dics))
        word_snippets = [self.get_word_transcription(word, movie_name, chapter_num)
                for word in words_flat]
        phrase_snippets = [self.get_phrase_transcription(phrase, movie_name, chapter_num)
                for phrase in phrases]
        return word_snippets + phrase_snippets
    
    def get_word_transcription(self, word, movie, chapter):
        start = word[1]
        end = word[2]
        text = word[0]
        return Transcription(text, start, end, "word", movie, chapter)
    
    def get_phrase_transcription(self, phrase, movie, chapter):
        text = phrase["text"]
        start = phrase["start"]
        duration = phrase["duration"]
        end = start + duration
        return Transcription(text, start, end, "phrase", movie, chapter)
    
class AssemblyTranscriptionSet:
    def __init__(self, transcriptions_files):
        self.transcriptions_files = transcriptions_files
        self.movies = list(transcriptions_files.keys())
        print(self.movies)
        self.chapters = {movie: list(transcriptions_files[movie].keys())
                                for movie in self.movies}

    def get_snippets(self, movie_name, chapter_num):
        chapter = self.transcriptions_files[movie_name][chapter_num]
        transcription_json = load_json_file(chapter["path"])
        return [self.get_word_transcription(word, movie_name, chapter_num)
                for word in transcription_json["words"]]
    
    def get_word_transcription(self, word, movie, chapter):
        start = word["start"] / 1000
        end = word["end"] / 1000
        text = word["text"]
        return Transcription(text, start, end, "word", movie, chapter)
        
def get_assembly_transcriptions():
    assembly_files = preproc.load_assembly_transcriptions()
    return AssemblyTranscriptionSet(assembly_files)
    
def get_hume_transcriptions():
    transcription_files = preproc.load_hume_transcriptions()
    return HumeTranscriptionSet(transcription_files)
    
if __name__ == "__main__":
    directory = const.DATA_ROOT_PATH + const.EMBEDDED_PATH + "/Life_After_Beth"
    outdir = const.DATA_ROOT_PATH + const.ASSEMBLY_TRANSLATIONS
    process_files(directory, outdir)
