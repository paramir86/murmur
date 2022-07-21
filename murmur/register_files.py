import glob
from io import BufferedReader
import re


def enumerate_files(path: str) -> list[str]:
    safix = r"/**/*.mp3"
    return glob.glob(path + safix, recursive=True)


class ID3:
    def __init__(self, file_address: str):
        self.file_address = file_address
        self.load()

    def get_syncsafe(self, data: bytes) -> int:
        data = [x & 0b01111111 for x in data]
        ans = (data[0] << 21) | (data[1] << 14) | (data[2] << 7) | data[3]
        return ans

    def load(self):
        with open(self.file_address, 'rb') as f:
            self.parse_header(f)
            self.parse_frames(self.tag_size, f)

    def parse_header(self, buffer: BufferedReader):
        if buffer.read(3) == b'ID3':
            self.is_ID3v2 = True
            major_version = str(buffer.read(1)[0])
            revision_number = str(buffer.read(1)[0])
            self.tag_version = "ID3v2." + major_version + "." + revision_number
            self.tag_flags = buffer.read(1)
            self.tag_size = self.get_syncsafe(buffer.read(4))

    def parse_frames(self, tag_size: int, buffer: BufferedReader):
        self.frames = {}
        while buffer.tell() + 10 < tag_size:
            frame_id = buffer.read(4).decode()
            frame_size = self.get_syncsafe(buffer.read(4))
            frame_flags = buffer.read(2)
            if list(frame_id)[0] == "T":
                character_code = buffer.read(1)
                text = buffer.read(frame_size - 1).decode()
                pattern = "^(.*?)\x00"
                regex_result = re.match(pattern, text)
                if regex_result is None:
                    frame_body = text
                else:
                    frame_body = regex_result.groups()[0]
            else:
                frame_body = buffer.read(frame_size)
            self.frames[frame_id] = frame_body
