import os
import sys
from pathlib import Path


def read_lines(filename, start=0, end=-1):
    """
    Read (lazy) specific chunk of filename line by line
    filename: json file containing tweet data (big file)
    start: byte position to read from (defaults to start of file)
    end: byte position to read to (defaults to end of file)
    """

    if end < 0:
        end = os.path.getsize(filename)

    with open(filename, encoding="utf8") as f:
        f.seek(start)
        while f.tell() < end:
            yield f.readline()


if __name__ == "__main__":
    root = Path(sys.argv[1])  # project directory

    # Test synthetic data
    datafile = root / "test" / "data.txt"
    with open(datafile, 'w') as f:
        f.write("Hello World!\nHow are you today?\nThank you!")
    print(*read_lines(datafile, end=15), sep="\n")
    print(*read_lines(datafile, start=15, end=20), sep="\n")
    print(*read_lines(datafile, start=20), sep="\n")

    # Test real data
    datafile = root/"data"/"tinyTwitter.json"
    lines = read_lines(datafile)
    print(next(lines))  # 1st line
    print(next(lines))  # 2nd line
    print(next(lines))  # 3rd line
