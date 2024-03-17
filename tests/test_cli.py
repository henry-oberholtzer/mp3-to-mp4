from pathlib import Path
import pytest
import typer
import os
import configparser
from typer.testing import CliRunner
from mp3_to_mp4 import CONFIG_PARAM_ERROR, cli, ERRORS, CONFIG_DIR_ERROR, __app_name__, __version__, config
runner = CliRunner()

def os_error(mode: int = 511, parents: bool = False, exist_ok: bool = False):
  raise OSError

parser = configparser.ConfigParser()

class TestCliConvert:
  def test_path_dir(self):
    return pytest.fail("Not written")
  def test_path_file(self):
    return pytest.fail("Not written")
  def test_path_err(self):
    return pytest.fail("Not written")
  def test_path_image(self):
    return pytest.fail("Not written")
  def test_path_image_err(self):
    return pytest.fail("Not written")
  def test_path_join(self):
    return pytest.fail("Not written")

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
    
  def test_config_output_dir(self, temp_user_cfg: config.Config):
    return pytest.fail("Not written")
  def test_config_width(self, temp_user_cfg: config.Config):
    return pytest.fail("Not written")
  def test_config_height(self, temp_user_cfg: config.Config):
    return pytest.fail("Not written")
  def test_config_image_padding(self, temp_user_cfg: config.Config):
    return pytest.fail("Not written")
  def test_config_sort_filename(self, temp_user_cfg: config.Config):
    return pytest.fail("Not written")
  def test_config_output_fps(self, temp_user_cfg: config.Config):
    return pytest.fail("Not written")

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
