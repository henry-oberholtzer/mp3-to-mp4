import pytest
import os

from typer.testing import CliRunner

from mp3_to_mp4 import cli, __version__, __app_name__, config

runner = CliRunner()

# @pytest.fixture(scope="session")
# def temp_config_dir(config):
#   config.CONFIG_DIR_PATH = tmp_path

class TestCli:
  def test_version(self):
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout
  def test_configure(self):
    result = runner.invoke(cli.app, ["init"])
    assert result.exit_code == 0
