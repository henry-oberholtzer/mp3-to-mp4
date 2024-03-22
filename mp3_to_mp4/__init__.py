# mp3-to-mp4 Copyright (C) 2024 Henry Oberholtzer

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
"""Top-level package for Mp3 to Mp4"""

__app_name__ = "mp3-to-mp4"
__version__ = "0.1.0"

from pathlib import Path


(
  SUCCESS,
  CONFIG_DIR_ERROR,
  CONFIG_FILE_ERROR,
  CONFIG_READ_ERROR,
  CONFIG_WRITE_ERROR,
  CONFIG_PARAM_ERROR,
  AUDIO_FILE_ERROR,
  AUDIO_DIR_ERROR,
  AUDIO_READ_ERROR,
  IMAGE_FILE_ERROR,
  IMAGE_DIR_ERROR,
  IMAGE_READ_ERROR,
  OUTPUT_DIR_ERROR,
  VIDEO_RENDER_ERROR,
) = range(14)

ERRORS = {
  CONFIG_DIR_ERROR: "Configuration directory error",
  CONFIG_FILE_ERROR: "Configuration file error",
  CONFIG_READ_ERROR: "Configuration read error",
  CONFIG_WRITE_ERROR: "Configuration rite error",
  CONFIG_PARAM_ERROR: "ERROR: Parameter value incompatible",
  AUDIO_FILE_ERROR: "Audio file error",
  AUDIO_DIR_ERROR: "Audio directory error",
  AUDIO_READ_ERROR: "Audio read error",
  IMAGE_FILE_ERROR: "Image file error",
  IMAGE_DIR_ERROR: "Image directory error",
  IMAGE_READ_ERROR: "Image read error",
  OUTPUT_DIR_ERROR: "Output directory error",
  VIDEO_RENDER_ERROR: "Error in rendering video",
}
