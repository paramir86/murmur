import glob
import re


def enumerate_files(path: str) -> list[str]:
    safix = r"/**/*.mp3"
    return glob.glob(path + safix, recursive=True)


class ID3:
    def __init__(self, file_address: str):
        self.file_address = file_address
        self.load()

        self.title = None
        self.artist = None
        self.album = None
        self.album_artist = None
        self.track = None
        self.disc_number = None
        self.year = None

    def load(self):
        with open(self.file_address, 'rb') as f:
            header = f.read(10)

        if header[0: 3] == b'ID3':
            self.is_ID3v2 = True
            major_version = str(header[3])
            revision_number = str(header[4])
            self.version = "ID3v2." + major_version + "." + revision_number
