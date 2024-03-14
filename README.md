# Mp3_to_Mp4

A CLI application for converting audio files (mp3, wav, aiff, etc) to mp4 file suitable for upload to social media sites like YouTube, Vimeo, etc.

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
6. After installing Poetry the directory folder, run `poetry install` in the project directory to install the needed dependencies.
7. You can target a folder to convert with `poetry run mp3-to-mp4 render --folder /c/my_folder/`. If the folder contains multiple audio files, they will all be converted with their respective meta data s the image, unless an image is specified with `--image`.

# Known Bugs & Issues

- Coming soon.

# Upcoming features

- Joining option for albums folders.
- Full Test Coverage.
In Config:
- Blurred Background Image.
- Padding for Images.
- Automatic YouTube Upload.
- Waveform Visualization.

# License & Copyright
