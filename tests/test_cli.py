import pytest
import typer
import os
from typer.testing import CliRunner
from mp3_to_mp4 import cli, __app_name__, __version__, config
runner = CliRunner()

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
  def test_config_success(self):
    return pytest.fail("Not written")
  def test_config_failure(self):
    return pytest.fail("Not written")
  def test_config_bg_color(self):
    return pytest.fail("Not written")
  def test_config_output_dir(self):
    return pytest.fail("Not written")
  def test_config_width(self):
    return pytest.fail("Not written")
  def test_config_height(self):
    return pytest.fail("Not written")
  def test_config_image_padding(self):
    return pytest.fail("Not written")
  def test_config_soft_filename(self):
    return pytest.fail("Not written")
  def test_config_output_fps(self):
    return pytest.fail("Not written")

class TestCliInitconfig:
  def test_initconfig(self, temp_dir, monkeypatch):
    tmp_cfg_file = temp_dir / "config.ini"
    cfg = config.Config(config_dir_path=temp_dir, config_file_path=tmp_cfg_file)
    monkeypatch.setattr(cli, "user_cfg", cfg)
    # Check if file exists.
    assert os.path.isfile(tmp_cfg_file)
    os.remove(tmp_cfg_file)
    assert not os.path.isfile(tmp_cfg_file)
    result = runner.invoke(cli.app, "initconfig")
    assert result.output == "Configuration initialized to default settings.\n"
    assert os.path.isfile(tmp_cfg_file)
    

class TestCliMain:
  def test_version(self, temp_user_cfg):
    temp_user_cfg
    result = runner.invoke(cli.app, "--version")
    assert result.exit_code == 0
    assert result.output == f"{__app_name__} v{__version__}\n"
