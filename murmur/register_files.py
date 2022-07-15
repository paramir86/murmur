from ast import parse
import glob


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

    def get_syncsafe(self, data: bytes) -> int:
        data = [x & 0b01111111 for x in data]
        ans = (data[0] << 21) | (data[1] << 14) | (data[2] << 7) | data[3]
        return ans

    def load(self):
        with open(self.file_address, 'rb') as f:
            self.parse_header(f.read(10))
            self.frames = f.read(self.tag_size)
            self.parse_frames(self.frames)

    def parse_header(self, header: bytes):
        if header[0: 3] == b'ID3':
            self.is_ID3v2 = True
            major_version = str(header[3])
            revision_number = str(header[4])
            self.tag_version = "ID3v2." + major_version + "." + revision_number
            self.tag_flags = header[5]
            self.tag_size = self.get_syncsafe(header[6: 10])

    def parse_frames(self, frames: bytes):
        idx = 0
        for i in range(7):
            frame_id = frames[idx+0: idx+4]
            frame_size = self.get_syncsafe(frames[idx+4: idx+8])
            frame_flags = frames[idx+8: idx+10]
            print(frame_id, frame_size, frame_flags, frames[idx+10: idx+10+frame_size])
            idx += 10+frame_size
