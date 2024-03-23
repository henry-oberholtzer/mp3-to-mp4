""" Handles combining the audio and image into a final mp4 file"""
from pathlib import Path
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.audio.AudioClip import concatenate_audioclips
from PIL import Image
import numpy
from mp3_to_mp4 import SUCCESS


def render(audio_list: list[Path], image: Image, filename: str, output_path: str, join: bool = False):
  audio = AudioFileClip(str(audio_list[0]))
  if join:
    audio = concatenate_audioclips([AudioFileClip(str(path)) for path in audio_list])
  image: ImageClip = ImageClip(numpy.array(image))
  image.duration = audio.duration
  image.audio = audio
  image.write_videofile(filename=f"{output_path}\\{filename}.mp4", fps=2, codec="libx264", audio_bitrate="320k", ffmpeg_params=['-tune','stillimage'])
  return SUCCESS

