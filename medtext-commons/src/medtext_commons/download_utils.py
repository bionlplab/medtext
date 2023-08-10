import hashlib
import os
from os import PathLike
from pathlib import Path
from typing import NewType, Union

import requests
import tqdm


MEDTEXT_RESOURCES_GITHUB = 'https://github.com/bionlplab/medtext/tree/main/medtext-resources'
MedTextPath = NewType('MedTextPath', Union[str, PathLike, bytes])


def get_md5(path: MedTextPath) -> str:
    """
    Get the MD5 value of a path.
    """
    with open(path, 'rb') as fin:
        data = fin.read()
    return hashlib.md5(data).hexdigest()


def assert_file_exists(path: MedTextPath, md5: str=None):
    assert os.path.exists(path), "Could not find file at %s" % path
    if md5:
        file_md5 = get_md5(path)
        assert file_md5 == md5, "md5 for %s is %s, expected %s" % (path, file_md5, md5)


def file_exists(path: MedTextPath, md5: str=None):
    """
    Check if the file at `path` exists and match the provided md5 value.
    """
    if md5 is None:
        return os.path.exists(path)
    else:
        return os.path.exists(path) and get_md5(path) == md5


def ensure_dir(path: MedTextPath):
    """
    Create dir in case it does not exist.
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def download_file(url: str, path: MedTextPath, proxies=None, raise_for_status=False) -> int:
    """
    Download a URL into a file as specified by `path`.
    """
    desc = 'Downloading ' + url
    print(desc)
    r = requests.get(url, stream=True, proxies=proxies)
    with open(path, 'wb') as f:
        file_size = int(r.headers.get('content-length'))
        default_chunk_size = 131072

        with tqdm.tqdm(total=file_size, unit='B', unit_scale=True, desc=desc) as pbar:
            for chunk in r.iter_content(chunk_size=default_chunk_size):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    pbar.update(len(chunk))
    if raise_for_status:
        r.raise_for_status()
    return r.status_code


def request_file(url: str, path: MedTextPath, proxies=None, md5: str=None, raise_for_status=False):
    """
    Download a URL into a file as specified by `path`.
    """
    ensure_dir(path)
    if file_exists(path, md5):
        print(f'File exists: {path}.')
        return
    download_file(url, path, proxies, raise_for_status)
    assert_file_exists(path, md5)


def request_medtext(dst, src=None, md5: str=None, proxies=None):
    base = os.path.basename(dst)
    if src is None:
        request_file('{}/{}'.format(MEDTEXT_RESOURCES_GITHUB, base), dst, md5=md5, proxies=proxies)
    else:
        request_file(src, dst, md5=md5, proxies=proxies)
