from pathlib import Path
import pytest
import typer
import os
import configparser
import tempfile
from typer.testing import CliRunner
from mp3_to_mp4 import CONFIG_PARAM_ERROR, SUCCESS, cli, renderer, ERRORS, CONFIG_DIR_ERROR, __app_name__, __version__, config
runner = CliRunner()

def os_error(mode: int = 511, parents: bool = False, exist_ok: bool = False):
  raise OSError

parser = configparser.ConfigParser()

class TestCliConvert:
  def test_render_if_path(self):
    result = runner.invoke(cli.app, ["convert", os.path.expanduser('~')])
    assert result.output == f"No viable audio files available in directory. Aborting.\n"
  def test_render_fail(self):
    result = runner.invoke(cli.app, "convert")
    assert result.output == "Please specify a target path or file.\n"
  
class TestCliConfig:
  def test_config_success(self, temp_user_cfg: config.Config):
    result = runner.invoke(cli.app, "config")
    assert result.output == f"Configuration file written to: {temp_user_cfg.config_file_path}\n"
  def test_config_failure(self, monkeypatch: pytest.MonkeyPatch, temp_user_cfg: config.Config):
    monkeypatch.setattr(Path, "mkdir", os_error)
    result = runner.invoke(cli.app, "config")
    assert result.output == f'Creating the config file failed with {ERRORS[CONFIG_DIR_ERROR]}\n'
    assert result.exit_code == 1
  def test_config_bg_color(self, temp_user_cfg: config.Config):
    color = "#343434"
    runner.invoke(cli.app, ["config", "--bg-color", color])
    parser.read(temp_user_cfg.config_file_path)
    assert parser[temp_user_cfg.GENERAL]["bg_color"] == color
  def test_config_bg_color_invalid(self, temp_user_cfg: config.Config):
    bad_color= "#HsAW12"
    result = runner.invoke(cli.app, ["config", "--bg-color", bad_color])
    assert result.output == f'Creating the config file failed with {ERRORS[CONFIG_PARAM_ERROR]}\n'
    assert result.exit_code == 1
    
  def test_config_output_dir(self, temp_dir, temp_user_cfg: config.Config):
    path = temp_dir
    runner.invoke(cli.app, ["config", "--output", path])
    parser.read(temp_user_cfg.config_file_path)
    assert parser[temp_user_cfg.GENERAL]["output_dir"] == str(path)
  def test_config_output_dir_bad_path(self, temp_mp3, temp_user_cfg: config.Config):
    path = temp_mp3
    result = runner.invoke(cli.app, ["config", "--output", path])
    assert result.exit_code == 1
  def test_config_output_dir_non_existent(self, temp_user_cfg: config.Config):
    path = tempfile.TemporaryDirectory(delete=True)
    result = runner.invoke(cli.app, ["config", "--output", path])
    assert result.exit_code == 1
  def test_config_width(self, temp_user_cfg: config.Config):
    width = 2160
    runner.invoke(cli.app, ["config", "--width", width])
    parser.read(temp_user_cfg.config_file_path)
    assert parser[temp_user_cfg.GENERAL]["width"] == str(width)
  def test_config_height(self, temp_user_cfg: config.Config):
    height = 1920
    runner.invoke(cli.app, ["config", "--height", height])
    parser.read(temp_user_cfg.config_file_path)
    assert parser[temp_user_cfg.GENERAL]["height"] == str(height)
  def test_config_image_padding(self, temp_user_cfg: config.Config):
    padding = 200
    runner.invoke(cli.app, ["config", "--padding", padding])
    parser.read(temp_user_cfg.config_file_path)
    assert parser[temp_user_cfg.GENERAL]["image_padding"] == str(padding)
  def test_config_sort_filename(self, temp_user_cfg: config.Config):
    runner.invoke(cli.app, ["config", "--sort-filename"])
    parser.read(temp_user_cfg.config_file_path)
    assert parser[temp_user_cfg.GENERAL]["sort_filename"] == str(False)
  def test_config_output_fps(self, temp_user_cfg: config.Config):
    fps = 30
    runner.invoke(cli.app, ["config", "--fps", fps])
    parser.read(temp_user_cfg.config_file_path)
    assert parser[temp_user_cfg.GENERAL]["output_fps"] == str(fps)

class TestCliInitconfig:
  def test_initconfig(self, temp_dir: Path, monkeypatch: pytest.MonkeyPatch):
    tmp_cfg_file = temp_dir / "config.ini"
    cfg = config.Config(config_dir_path=temp_dir, config_file_path=tmp_cfg_file)
    monkeypatch.setattr(cli, "user_cfg", cfg)
    # Check if file exists.
    assert os.path.isfile(tmp_cfg_file)
    # Remove the file.
    os.remove(tmp_cfg_file)
    assert not os.path.isfile(tmp_cfg_file)
    # Initialize the configuration.
    result = runner.invoke(cli.app, "initconfig")
    assert result.output == "Configuration initialized to default settings.\n"
    assert os.path.isfile(tmp_cfg_file)
    

class TestCliMain:
  def test_version(self, temp_user_cfg):
    temp_user_cfg
    result = runner.invoke(cli.app, "--version")
    assert result.exit_code == 0
    assert result.output == f"{__app_name__} v{__version__}\n"
