import os
import constants as const
import random
import videoutils as video
import preproc
import csv
from transcribe import get_hume_transcriptions, get_assembly_transcriptions

def write_snippets(id, snippets, stimuli, output_folder, worksheet):
    for snippet in snippets:
        snippet_name = "snippet_{}.mp4".format(id)
        output_file = os.path.join(output_folder, snippet_name)
        video.extract_and_save_snippet(stimuli[snippet.movie][snippet.chapter]["path"],
                                       snippet.start,
                                       snippet.end,
                                       output_file)
        worksheet.writerow([snippet_name, snippet.movie,snippet.chapter,snippet.text])
        id += 1

def test_transcription(transcription_set,
                       stimuli,
                       output_folder,
                       worksheet,
                       num_movies=1,
                       num_chapters=3,
                       num_snippets=5):
    chosen_movies = random.sample(transcription_set.movies, num_movies)
    f =open(worksheet, 'w', newline='')
    writer = csv.writer(f)
    id = 0
    for movie in chosen_movies:
        all_chapters = transcription_set.chapters[movie]
        chosen_chapters = random.sample(all_chapters, num_chapters)
        for chapter_num in chosen_chapters:
            snippets = transcription_set.get_snippets(movie, chapter_num)
            chosen_snippets = random.sample(snippets, num_snippets)
            write_snippets(id, chosen_snippets, stimuli, output_folder, writer)
            id+=len(chosen_snippets)
    f.close()


def test_hume_transcriptions(stimuli):
    transcriptions = get_hume_transcriptions()
    worksheet = const.DATA_ROOT_PATH + const.HUME_WORKSHHEET
    output_folder = const.DATA_ROOT_PATH + const.EXTRACTED_CLIPS_PATH_HUME
    test_transcription(transcriptions, stimuli, output_folder, worksheet)

def test_assembly_transcriptions(stimuli):
    transcriptions = get_assembly_transcriptions()
    worksheet = const.DATA_ROOT_PATH + const.ASSEMBLY_WORKSHEET
    output_folder = const.DATA_ROOT_PATH + const.EXTRACTED_CLIPS_PATH_ASSEMBLY
    test_transcription(transcriptions, stimuli, output_folder, worksheet)



if __name__ == "__main__":
    stimuli = preproc.load_stimuli()
    test_hume_transcriptions(stimuli)
    #test_assembly_transcriptions(stimuli)