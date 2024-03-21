# mp3-to-mp4

A CLI application for converting audio files (.mp3, .wav, .flac, .aiff, etc) to mp4 file suitable for upload to social media sites like YouTube, Vimeo, etc.

# Features

- Batch folder rendering
- Saved renderer defaults
- Adjustable background color
- Adjustable dimensions
- High test coverage (97%)

# Technologies Used

- Python 3.12.0
- Typer 0.9.0
- MoviePy 1.0.3
- TinyTag 1.10.1
- PyTest
- ImageMagick
- Poetry (Dependency management)

# Installation Guide

## Distribution
1. mp3-to-mp4 is available under [pypi](htts://pypi.org) as `mp3-to-mp4`.
2. Simply run `pip install mp3-to-mp4` to install.

## From Source
1. Download the [repository](https://github.com/henry-oberholtzer/mp3-to-mp4.git)
2. Ensure Python and Pip are installed on your system: `python --v` and `pip --v`
3. If you do not have Python installed, install from [the official distribution](https://www.python.org/downloads/)
4. Check if you have Poetry installed for managing dependencies. `poetry --version`
5. If you do not have Poetry, [install it](https://python-poetry.org/docs/). You may also need Pipx.
6. If you render any files that do not provide an image, ImageMagick will be required. It can be installed from [here](https://imagemagick.org/script/download.php). Ensure that you select "Install legacy utilities" in the installation options.
7. After installing Poetry the directory folder, run `poetry install` in the project directory to install the required dependencies & application.

# Usage

mp3-to-mp4 is built with the intention of converting folders of tagged audio files to mp4 rapidly.

### Basic:

To convert an entire folder:

```
poetry run mp3-to-mp4 convert /c/my_folder/
```

Converting a single file and specific (optional) image:

```
poetry run mp3-to-mp4 convert /c/my_folder/my_music.mp3 --image /c/other_folder/image.jpg
```

**NOTE**: If your path includes parentheses, you may need to place it in single quotes to avoid bash errors. e.g. '/c/my path (with mp3s)'

### Image Selection:

Images can be specified with the `--image` or `-i` flag.

If no image is specified, mp3-to-mp4 will try to grab the image from the file's metadata.

If no image is present in the metadata, it will search the folder for a suitable image and use the first one it finds.

At the moment, mp3-to-mp4 considers .png and .jpeg/.jpg files that match the following as suitable images.

`folder, album_art, albumart, art`

If there is no image available, text will be generated based on the `artist` and `title` ID3 tags, unless a join command has been given, where the `album artist` and `album title` tags will be used instead.

### Configuration Flags:

Flags used under the `config` command.

Running `initconfig` will restore the `config.ini` file to defaults.

| Flag                 | Type              | Default Value | Usage                                                                   |
| -------------------- | ----------------- | ------------- | ----------------------------------------------------------------------- |
| `--output, -o`       | String (path)     | ~/mp3-to-mp4  | Sets video output directory.                                            |
| `--bg-color, -bg`    | String (Hex Code) | #000000       | Sets the color the image is rendered against.                           |
| `--width, -w`        | Integer (pixels)  | 1920          | Sets the video width.                                                   |
| `--height,-h`        | Integer (pixels)  | 1080          | Sets the video height.                                                  |
| `--padding,-p`       | Integer (pixels)  | 0             | Sets a padding for the album art.                                       |
| `--sort-filename,-s` | Boolean           | True          | Determines if filenames should be used to sort albums `--join` command. |

# Upcoming features

- Changeable config location?
- Default to in-folder image.
- Blurred Background Image option.
- Switch to PIL for text drawing.
- .exe for no installation. (PyInstaller)
- Adjustable bitrate for audio encoding.
- Text file with description & information output option.
- Automatic YouTube Upload.
- Waveform Visualization.
- Custom Progress Log
- File name parameters.

# Known Bugs & Issues

- [Open an issue](https://github.com/henry-oberholtzer/mp3-to-mp4/issues) if you encounter any.

# License & Copyright

© [Henry Oberholtzer](https://www.henryoberholtzer.com) 2024

Original Code licensed under a GNU GPLv3

Packages & dependencies licensed as specified in their distributions.
