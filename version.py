from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

file_path = "./__init__.py"


def replace(file_path):
    version = str
    # Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for i, line in enumerate(old_file):
                if i == 5:
                    version = line[16] + '.' + line[19] + '.' + line[22]
                    new_file.write('"version": (1, 4, ' + int(line[22]) + 1 + '),')
    # Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    # Remove original file
    remove(file_path)
    # Move new file
    move(abs_path, file_path)
    return version


with open(file_path) as fp:
    for i, line in enumerate(fp):
        if i == 5:
            version = line.replace('"version": (', '').replace('),', '')
            print(version)
            print(int(line[16]))
            break
