import glob


def enumerate_files(path: str) -> list[str]:
    safix = r"/**/*.mp3"
    return glob.glob(path + safix, recursive=True)
