from pathlib import Path


def check_make_dir(path):
    Path(path).expanduser().mkdir(parents=True, exist_ok=True)


def make_file_path(base_path, filename):
    fpath = Path(base_path, filename).expanduser()
    check_make_dir(fpath.parent)
    return str(fpath)


def touch_file(filepath):
    fpath = Path(filepath).expanduser()
    if not fpath.exists():
        print(f"Touching file {fpath}\n")
        fpath.touch(exist_ok=True)


def edit_file(filename, data):
    fpath = Path(filename).expanduser()
    if not data in fpath.read_text():
        with open(fpath, "a") as f:
            print(f"Adding {data} to file {fpath}\n")
            f.write(str(data))
            f.write("\n")


def delete_file(filename):
    fpath = Path(filename).expanduser()
    if fpath.exists():
        print(f"Deleting file {fpath}\n")
        fpath.unlink()


# returns false if a file exists
def check_file(path):
    fpath = Path(path).expanduser()
    if fpath.exists():
        return False
    if not fpath.exists():
        return True
