"""Top-level package for Mp3 to Mp4"""

__app_name__ = "mp3-to-mp4"
__version__ = "0.1.0"

(
  SUCCESS,
  CONFIG_DIR_ERROR,
  CONFIG_FILE_ERROR,
  CONFIG_READ_ERROR,
  CONFIG_WRITE_ERROR,
  AUDIO_FILE_ERROR,
  AUDIO_DIR_ERROR,
  AUDIO_READ_ERROR,
  IMAGE_FILE_ERROR,
  IMAGE_DIR_ERROR,
  IMAGE_READ_ERROR,
  OUTPUT_DIR_ERROR,
  VIDEO_RENDER_ERROR,
) = range(13)

ERRORS = {
  CONFIG_DIR_ERROR: "Configuration directory error",
  CONFIG_FILE_ERROR: "Configuration file error",
  CONFIG_READ_ERROR: "Configuration read error",
  CONFIG_WRITE_ERROR: "Configurationwrite error",
  AUDIO_FILE_ERROR: "Audio file error",
  AUDIO_DIR_ERROR: "Audio directory error",
  AUDIO_READ_ERROR: "Audio read error",
  IMAGE_FILE_ERROR: "Image file error",
  IMAGE_DIR_ERROR: "Image directory error",
  IMAGE_READ_ERROR: "Image read error",
  OUTPUT_DIR_ERROR: "Output directory error",
  VIDEO_RENDER_ERROR: "Error in rendering video",
}
