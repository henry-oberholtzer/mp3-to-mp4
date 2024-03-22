""" Handles combining the audio and image into a final mp4 file"""
from pathlib import Path
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.audio.AudioClip import concatenate_audioclips

from mp3_to_mp4 import SUCCESS


def render(audio_list: list[Path], image: Path, filename: str, output_path: str, join: bool):
  audio = AudioFileClip(audio_list[0])
  if join:
    audio = join_audio(AudioFileClip)
  image: ImageClip = ImageClip(str(image))
  image.duration = audio.duration
  image.audio = audio
  image.write_videofile(filename=f"{output_path}\\{filename}.mp4", fps=2, codec="libx264", audio_bitrate="320k", ffmpeg_params=['-tune','stillimage'])
  return SUCCESS

def join_audio(audio_list: list[Path]):
  return concatenate_audioclips([AudioFileClip(str(path)) for path in audio_list])
