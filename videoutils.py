from moviepy.editor import VideoFileClip
from scenedetect import SceneManager, open_video, ContentDetector
import scenedetect as sd
import constants as const

def extract_and_save_scenes(file_path, output_folder):
    video = open_video(file_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())
    scene_manager.detect_scenes(video)
    scenes = scene_manager.get_scene_list()
    sd.scene_manager.save_images(scenes, video, output_dir=output_folder, num_images=3)
    return scenes

def extract_and_save_snippet(file_path, start_time, end_time, output_file):
    clip = VideoFileClip(file_path).subclip(start_time, end_time)
    clip.write_videofile(output_file, codec='libx264', audio_codec='aac')


if __name__ == "__main__":
    file = "/Volumes/PortableSSD/data/stimuli/Embedded/Life_After_Beth/Life_After_Beth-ch7_padded.avi"
    print(extract_and_save_scenes(file, const.DATA_ROOT_PATH + const.SCENE_CUTS))