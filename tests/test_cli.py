from typer.testing import CliRunner

from mp3_to_mp4 import cli, __version__, __app_name__

runner = CliRunner()

class TestCli:
  def test_version(self):
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout
