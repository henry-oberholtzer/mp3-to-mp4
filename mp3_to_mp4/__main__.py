"""Mp3 to Mp4 entry point script"""
#mp3_to_mp4/__main__.py

from mp3_to_mp4 import cli, __app_name__

def main():
  cli.app(prog_name=__app_name__)

if __name__ == "__main__":
  main()
