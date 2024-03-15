# mp3-to-mp4
A CLI application for converting audio files (.mp3, .wav, .flac, .aiff, etc) to mp4 file suitable for upload to social media sites like YouTube, Vimeo, etc.

# Technologies Used

- Python 3.12.0
- Typer 0.9.0
- MoviePy 1.0.3
- TinyTag 1.10.1
- PyTest
- ImageMagick
- Poetry (Dependency management)

# Installation Guide

1. Download the [repository](https://github.com/henry-oberholtzer/mp3-to-mp4.git)
2. Ensure Python and Pip are installed on your system: `python --v` and `pip --v`
3. If you do not have Python installed, install from [the official distribution](https://www.python.org/downloads/)
4. Check if you have Poetry installed for managing dependencies. `poetry --version`
5. If you do not have Poetry, [install it](https://python-poetry.org/docs/). You may also need Pipx.
6. If you render any files that do not provide an image, ImageMagick will be required. It can be installed from [here](https://imagemagick.org/script/download.php). Ensure that you select "Install legacy utilities" in the installation options.
6. After installing Poetry the directory folder, run `poetry install` in the project directory to install the required dependencies & application.

# Usage

mp3-to-mp4 is built with the intention of converting folders of tagged audio files to mp4 rapidly.

To convert an entire folder:
```
poetry run mp3-to-mp4 convert /c/my_folder/
```
It will default to using a specified image, failing that the file's ID3 image tag will be used.

If there is no image available, text will be generated based on the `artist` and `title` ID3 tags.

Other uses:

Converting a single file and image:
```
poetry run mp3-to-mp4 convert /c/my_folder/my_music.mp3 --image /c/other_folder/image.jpg
```


# Upcoming features

- Full Test Coverage.
- Default to in-folder image.
- Joining option for albums folders.
- Blurred Background Image option.
- .exe for no installation. (PyInstaller)
- Adjustable bitrate for audio encoding.
- Automatic YouTube Upload.
- Waveform Visualization.
- Initialize configuration command.
- Show current settings on config.
- Custom Progress Log
- File name parameters.

# Known Bugs & Issues

- Coming soon.

# License & Copyright

© [Henry Oberholtzer](https://www.henryoberholtzer.com) 2024

Original Code licensed under a GNU GPLv3

Packages & dependencies licensed as specified in their distributions.
